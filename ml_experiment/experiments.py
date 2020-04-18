from typing import *
from functools import wraps, partial
from inspect import isgeneratorfunction, getfile
import sys
from math import ceil
from datetime import timedelta
import mlflow
import ray
import numpy as np
from pytictoc import TicToc
import optuna

from .logging import logger, setup_logging
from .config import parse_config, get_validation_model, ValidationError
from .config.models import GroupConfig, ExperimentConfig, JobTypes, \
    JobConfig, Metric, RayConfig, create_model_from_signature, replace_model_field
from .mlflow import create_mlflow_experiment, log_experiment_results, \
    setup_autologging, AutologgingBackendParam
from .optuna import create_optuna_study, optimize_optuna_study, prune_trial, sample_params_from_distributions
from .exceptions import NoMetricSpecified, ExperimentError, DataNotLoaded


class DataLoader(object):
    @classmethod
    def load_data(cls):
        raise DataNotLoaded()


class Trial(object):
    @classmethod
    def get_current(cls) -> optuna.Trial:
        raise DataNotLoaded()


def _parse_experiment_arguments(experiment_func: Callable) -> JobConfig:
    try:
        config = parse_config(sys.argv[1], get_validation_model)
        """
        params_model = create_model_from_signature(experiment_func, 'Parameters')
        model = replace_model_field(config.name, config.__class__, params=params_model)

        if isinstance(config, GroupConfig):
            param_space_model = create_model_from_signature(experiment_func,
                                                            config.name,
                                                            allow_factory_types=True)
            model = replace_model_field(config.name, model, param_space=param_space_model)

        import pprint
        print(pprint.pprint(model.__fields__['param_space']))
        model.validate(config.dict(exclude_defaults=True))
        """
        return config
    except ValidationError:
        exit(1)


def _calculate_concurrent_workers(cpu: float, gpu: float, num_trials: int) -> int:
    available_resources = ray.available_resources()
    available_gpus = available_resources.get('GPU', 0)
    available_cpus = available_resources.get('CPU', 1)
    concurrent_workers_by_cpu = available_cpus / cpu
    concurrent_workers_by_gpu = available_gpus / gpu if gpu else np.inf
    return int(min([concurrent_workers_by_cpu, concurrent_workers_by_gpu, num_trials]))


def _extract_metrics_and_artifacts(result):
    result = result if isinstance(result, tuple) else (result,)
    metrics = result[0] if len(result) >= 1 else None
    artifacts = result[1] if len(result) >= 2 else None
    return metrics, artifacts


def _run_group(func: Callable,
               config: GroupConfig,
               data_loader: Optional[DataLoader],
               **kwargs):
    optimize_metric = config.metric

    if not optimize_metric:
        raise NoMetricSpecified()

    cpu = config.resources_per_worker.cpu
    gpu = config.resources_per_worker.gpu
    concurrent_workers = _calculate_concurrent_workers(cpu, gpu, config.num_trials)
    data_object_id = None
    data_loader_class = None
    futures = []

    if data_loader:
        data = data_loader.load_data()
        data_object_id = ray.put(data)
        data_loader_class = data_loader.__class__

    remote_func = ray.remote(num_cpus=cpu, num_gpus=gpu)(_run_group_remote)

    study = create_optuna_study(config)

    for i in range(concurrent_workers):
        num_trials = config.num_trials // concurrent_workers

        if i == 0:
            num_trials += config.num_trials % concurrent_workers

        new_group_config = config.copy(update={'num_trials': num_trials})
        object_id = remote_func.remote(func=func,
                                       study=study,
                                       optimize_metric=optimize_metric,
                                       group_config=new_group_config,
                                       object_id=data_object_id,
                                       data_loader_class=data_loader_class,
                                       **kwargs)
        futures.append(object_id)

    return ray.get(futures)


def _run_group_remote(func: Callable,
                      study: optuna.Study,
                      optimize_metric: Optional[Metric],
                      group_config: GroupConfig,
                      object_id: Optional[int],
                      data_loader_class: Optional[Type],
                      autologging_backends: AutologgingBackendParam,
                      log_seeds: bool,
                      log_system_info: bool):
    is_generator = isgeneratorfunction(func)
    setup_logging(experiment_name=group_config.name)
    mlflow.set_experiment(group_config.name)

    if object_id:
        data = ray.get(object_id)
        data_loader_class.load_data = lambda: data

    def objective(trial):
        with mlflow.start_run(run_name=f'Trial {trial.number}') as run:
            setup_autologging(func, autologging_backends, log_seeds, log_system_info)
            mlflow.set_tag('mlflow.source.name', getfile(func))
            Trial.get_current = lambda: trial
            param_space = sample_params_from_distributions(trial, group_config.param_space)
            all_params = {**group_config.params, **param_space}
            results = func(**all_params)
            metrics = {}
            trial.set_user_attr('mlflow_run_id', run.info.run_id)

            if results is None:
                raise ExperimentError('Group main functions should always return something!')

            if is_generator:
                for i, result in enumerate(results):
                    metrics, artifacts = _extract_metrics_and_artifacts(result)
                    trial.report(metrics[optimize_metric.name], i)
                    log_experiment_results(all_params, metrics, artifacts)
                    if trial.should_prune():
                        prune_trial()
            else:
                metrics, artifacts = _extract_metrics_and_artifacts(results)
                log_experiment_results(all_params, metrics, artifacts)
            return metrics[optimize_metric.name]

    optimize_optuna_study(study, objective=objective, group_config=group_config)


def _run_experiment(func: Callable,
                    config: ExperimentConfig,
                    autologging_backends: AutologgingBackendParam,
                    log_seeds: bool,
                    log_system_info: bool):
    mlflow.set_experiment(config.name)
    with mlflow.start_run():
        setup_autologging(func, autologging_backends, log_seeds, log_system_info)
        mlflow.set_tag('mlflow.source.name', getfile(func))
        results, all_params = _run_job(func, config)
        if not results:
            return
        results = results if isgeneratorfunction(func) else [results]
        for result in results:
            if result:
                metrics, artifacts = _extract_metrics_and_artifacts(result)
                log_experiment_results(all_params, metrics, artifacts)


def _run_job(func: Callable, config: JobConfig):
    return func(**config.params)


def _initialize_ray(config: JobConfig):
    params = config.ray_config.dict() if config.ray_config else {}
    return ray.init(**params, log_to_driver=True)


def _job_runner(remote_func: Callable, ray_config: Optional[RayConfig], *args, **kwargs):
    if ray_config:
        object_id = ray.remote(remote_func).remote(*args, **kwargs)
        return ray.get(object_id)
    else:
        return remote_func(*args, **kwargs)


def experiment(func: Optional[Callable] = None, *,
               autologging_backends: AutologgingBackendParam = None,
               optimization_metric: Union[Metric, str, None] = None,
               data_loader: Optional[DataLoader] = None,
               log_seeds: bool = True,
               log_system_info: bool = True,
               **kwargs):
    if func is None:
        return partial(experiment,
                       autologging_backends=autologging_backends,
                       optimize_metric=optimization_metric)

    if isinstance(optimization_metric, str):
        optimization_metric = Metric(name=optimization_metric)

    if optimization_metric:
        kwargs['metric'] = optimization_metric

    @wraps(func)
    def wrapper():
        config = _parse_experiment_arguments(func)
        config = config.copy(update=kwargs)

        setup_logging(experiment_name=config.name)
        logger.info(f'======== Starting job {config.name} in {sys.argv[0]} =========')

        if config.kind == JobTypes.GROUP:
            config = cast(GroupConfig, config)

        if config.kind == JobTypes.EXPERIMENT:
            config = cast(ExperimentConfig, config)

        logger.info(f"Job Config -> {config.dict()}")

        if config.kind == JobTypes.GROUP or config.ray_config:
            _initialize_ray(config)

        t = TicToc()
        t.tic()

        if config.kind == JobTypes.JOB:
            _job_runner(_run_job, config.ray_config, func=func, config=config)
        else:
            create_mlflow_experiment(experiment_name=config.name)
            call_params = dict(func=func,
                               config=config,
                               autologging_backends=autologging_backends,
                               log_seeds=log_seeds,
                               log_system_info=log_system_info)
            if config.kind == JobTypes.GROUP:
                _run_group(data_loader=data_loader, **call_params)
            else:
                _job_runner(_run_experiment, config.ray_config, **call_params)

        elapsed_time = timedelta(seconds=ceil(t.tocvalue()))
        logger.info(f"Finished job {config.name} in {elapsed_time}")
        ray.shutdown()

    return wrapper

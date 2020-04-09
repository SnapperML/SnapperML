from typing import Union, Optional, Callable, cast
from functools import wraps, partial
from inspect import isgeneratorfunction
import sys
from math import ceil
from datetime import timedelta
import mlflow
import ray
import numpy as np
from pytictoc import TicToc
from optuna import Study

from .logging import logger, setup_logging
from .cli import create_argument_parse_from_function, get_default_params_from_func
from .config import parse_config, get_validation_model
from .config.models import GroupConfig, ExperimentConfig, JobTypes, JobConfig, Metric, RayConfig
from .mlflow import create_mlflow_experiment, log_experiment_results, \
    setup_autologging, AutologgingBackendParam
from .optuna import create_optuna_study, optimize_optuna_study, prune_trial
from .exceptions import NoMetricSpecified, ExperimentError, DataNotLoaded


class DataLoader(object):
    @classmethod
    def load_data(cls):
        raise DataNotLoaded()


def _parse_experiment_arguments(experiment_func: Callable):
    parser = create_argument_parse_from_function(experiment_func, all_keywords=True, all_optional=True)
    parser.add_argument('--experiment_name', type=str, default=None)
    parser.add_argument('config_file', type=str)
    arguments = parser.parse_args()
    params = vars(arguments)
    config_file = params.pop('config_file')
    config = parse_config(config_file, get_validation_model)
    experiment_name = params.pop('experiment_name') or config.name
    config.name = experiment_name
    return params, config


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
               overridden_params: dict,
               config: GroupConfig,
               data_loader: Optional[DataLoader],
               **kwargs):
    optimize_metric = config.metric

    if not optimize_metric:
        raise NoMetricSpecified()

    cpu = config.resources_per_trial.cpu
    gpu = config.resources_per_trial.gpu
    concurrent_workers = _calculate_concurrent_workers(cpu, gpu, config.num_trials)
    data_object_id = None
    futures = []

    if data_loader:
        data = data_loader.load_data()
        data_object_id = ray.put(data)

    remote_func = ray.remote(num_cpus=cpu, num_gpus=gpu)(_run_group_remote)

    study = create_optuna_study(config)

    for i in range(concurrent_workers):
        num_trials = config.num_trials // concurrent_workers

        if i == 0:
            num_trials += config.num_trials % concurrent_workers

        new_group_config = config.copy(update={'num_trials': num_trials})
        object_id = remote_func.remote(func=func,
                                       overridden_params=overridden_params,
                                       study=study,
                                       optimize_metric=optimize_metric,
                                       group_config=new_group_config,
                                       object_id=data_object_id,
                                       **kwargs)
        futures.append(object_id)

    return ray.get(futures)


def _run_group_remote(func: Callable,
                      overridden_params: dict,
                      study: Study,
                      optimize_metric: Optional[Metric],
                      group_config: GroupConfig,
                      object_id: Optional[int],
                      autologging_backends: AutologgingBackendParam,
                      log_seeds: bool,
                      log_system_info: bool):
    is_generator = isgeneratorfunction(func)
    default_params = get_default_params_from_func(func)
    setup_logging(experiment_name=group_config.name)
    mlflow.set_experiment(group_config.name)

    if object_id:
        data = ray.get(object_id)
        DataLoader.load_data = lambda: data

    def objective(trial):
        with mlflow.start_run(run_name=f'Trial {trial.number}') as run:
            setup_autologging(func, autologging_backends, log_seeds, log_system_info)

            param_space = {k: v(k, trial) if callable(v) else v for k, v in group_config.param_space.items()}
            all_params = {**default_params, **group_config.params, **param_space, **overridden_params}
            results = func(**all_params)
            metrics = {}
            trial.set_user_attr('mlflow_run_id', run.info.run_id)

            if not results:
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

    optimize_optuna_study(study,
                          objective=objective,
                          group_config=group_config,
                          add_mlflow_callback=(not is_generator))


def _run_experiment(func: Callable,
                    overridden_params: dict,
                    config: ExperimentConfig,
                    autologging_backends: AutologgingBackendParam,
                    log_seeds: bool,
                    log_system_info: bool):
    mlflow.set_experiment(config.name)

    with mlflow.start_run():
        setup_autologging(func, autologging_backends, log_seeds, log_system_info)
        results, all_params = _run_job(func, overridden_params, config)
        if not results:
            return
        results = results if isgeneratorfunction(func) else [results]
        for result in results:
            if result:
                metrics, artifacts = _extract_metrics_and_artifacts(result)
                log_experiment_results(all_params, metrics, artifacts)


def _run_job(func: Callable, params: dict, config: JobConfig):
    default_params = get_default_params_from_func(func)
    all_params = {**default_params, **config.params, **params}
    return func(**all_params), all_params


def _initialize_ray(config: JobConfig):
    if config.ray_config and config.ray_config.cluster_address:
        ray.init(address=config.ray_config.cluster_address)
    else:
        ray.init(log_to_driver=True)


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
        overridden_params, config = _parse_experiment_arguments(func)
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
            _job_runner(_run_job,
                        config.ray_config,
                        func=func,
                        overridden_params=overridden_params,
                        config=config)
        else:
            create_mlflow_experiment(experiment_name=config.name)
            call_params = dict(func=func,
                               overridden_params=overridden_params,
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

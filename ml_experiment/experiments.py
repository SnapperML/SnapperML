from typing import *
from functools import wraps, partial
from inspect import isgeneratorfunction, getfile
import sys
from math import ceil
from datetime import timedelta

import mlflow
from mlflow.entities import RunStatus
import ray
import numpy as np
import traceback
from pytictoc import TicToc
import optuna

from .callbacks.core import Callback, CallbacksHandler
from .logging import logger, setup_logging
from .config import parse_config, get_validation_model
from .config.models import GroupConfig, ExperimentConfig, JobTypes, \
    JobConfig, Metric, RayConfig, Settings
from .mlflow import create_mlflow_experiment, log_experiment_results, \
    setup_autologging, AutologgingBackendParam, log_text_file
from .optuna import create_optuna_study, optimize_optuna_study, sample_params_from_distributions
from .exceptions import NoMetricSpecified, ExperimentError, DataNotLoaded, TrialNotAvailable


class DataLoader(object):
    """
    Base class for Data loaders.

    The main purpose of data loaders is to provide an easy way to share data
    across processes when running a group of experiments, also known as
    hyperparameter tuning.

    When this abstract class is implemented (using a subclass)
    and that subclass is added as the argument *data_loader* to the experiment main function
    decorator, a shared resource will be created. This shared resource is the result
    of executing the implemented function, load_data. The key point here is that the load_data
    function will be only called once by the master process and then its result will be shared among
    the rest workers. In this way, we can avoid expensive computation being duplicated for each worker.

    The shared data will be stored in the Plasma Object Store of ray, so you should take into account
    its limitations: https://docs.ray.io/en/latest/serialization.html
    """
    @classmethod
    def load_data(cls):
        raise DataNotLoaded()


class Trial(object):
    """
    This class makes the current Optuna Trial object accessible.

    It can be used to model complex hyperparameter spaces.
    More information here: https://optuna.readthedocs.io/en/latest/tutorial/configurations.html
    """
    @classmethod
    def get_current(cls) -> optuna.Trial:
        raise TrialNotAvailable()


class MlflowRunWithErrorHandling:
    def __init__(self,
                 callbacks_handler: CallbacksHandler,
                 delete_if_failed: bool,
                 trial: Optional[optuna.Trial] = None,
                 *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.delete_if_failed = delete_if_failed
        self.callbacks_handler = callbacks_handler
        self.trial = trial
        self.run = None
        self.finish_callback_params = {}

    def handle_exception(self, exception):
        mlflow.set_tag('Status', 'Failed')
        if self.delete_if_failed:
            mlflow.end_run(RunStatus.to_string(RunStatus.FAILED))
            mlflow.delete_run(self.run.info.run_id)
        else:
            log_text_file('traceback.txt', traceback.format_exc())
            mlflow.end_run(RunStatus.to_string(RunStatus.FAILED))
            logger.exception(exception)

    def __enter__(self):
        self.run = mlflow.start_run(*self.args, **self.kwargs)
        if not self.trial:
            self.callbacks_handler.on_job_start(run_id=self.run.info.run_id)
        return self.run, self.finish_callback_params

    def __exit__(self, exception_type, exception_value, _):
        is_pruned_exception = exception_type == optuna.exceptions.TrialPruned
        exception_value = None if is_pruned_exception else exception_value

        if self.trial:
            self.callbacks_handler.on_trial_end(trial=self.trial,
                                                exception=exception_value,
                                                **self.finish_callback_params)
        else:
            self.callbacks_handler.on_job_end(exception=exception_value,
                                              **self.finish_callback_params)

        if exception_type and not is_pruned_exception:
            self.handle_exception(exception_value)
        else:
            mlflow.end_run(RunStatus.to_string(RunStatus.FINISHED))

        return exception_type is None


def _parse_experiment_arguments() -> JobConfig:
    return parse_config(sys.argv[1], get_validation_model)


def _calculate_concurrent_workers(config: GroupConfig) -> int:
    cpu = config.resources_per_worker.cpu
    gpu = config.resources_per_worker.gpu
    available_resources = ray.available_resources()
    available_cpus = (config.ray_config and config.ray_config.num_cpus) or available_resources.get('CPU', 1)
    available_gpus = (config.ray_config and config.ray_config.num_gpus) or available_resources.get('GPU', 0)
    concurrent_workers_by_cpu = available_cpus / cpu
    concurrent_workers_by_gpu = available_gpus / gpu if gpu else np.inf
    return int(min([concurrent_workers_by_cpu, concurrent_workers_by_gpu, config.num_trials]))


def _extract_metrics_and_artifacts(result):
    result = result if isinstance(result, tuple) else (result,)
    metrics = result[0] if len(result) >= 1 else None
    artifacts = result[1] if len(result) >= 2 else None
    return metrics, artifacts


def _run_group(func: Callable,
               config: GroupConfig,
               data_loader_func: Optional[Callable[[], Any]],
               callbacks_handler: CallbacksHandler,
               settings: Settings,
               **kwargs):
    optimize_metric = config.metric

    if not optimize_metric:
        raise NoMetricSpecified()

    concurrent_workers = _calculate_concurrent_workers(config)
    data_object_id = None
    futures = []

    callbacks_handler.on_job_start()

    if data_loader_func:
        data = data_loader_func()
        data_object_id = ray.put(data)

    remote_func = ray.remote(num_cpus=config.resources_per_worker.cpu,
                             num_gpus=config.resources_per_worker.gpu)(_run_group_remote)

    study = create_optuna_study(config, settings)

    for i in range(concurrent_workers):
        num_trials = config.num_trials // concurrent_workers

        if i == 0:
            num_trials += config.num_trials % concurrent_workers

        new_group_config = config.copy(update={'num_trials': num_trials})
        object_id = remote_func.remote(func=func,
                                       study=study,
                                       optimize_metric=optimize_metric,
                                       group_config=new_group_config,
                                       data=data_object_id,
                                       callbacks_handler=callbacks_handler,
                                       **kwargs)
        futures.append(object_id)

    try:
        result = ray.get(futures)
    except Exception as e:
        callbacks_handler.on_job_end(exception=e)
    else:
        callbacks_handler.on_job_end(exception=None)
        return result


def _run_group_remote(func: Callable,
                      study: optuna.Study,
                      optimize_metric: Optional[Metric],
                      group_config: GroupConfig,
                      data: Optional[Any],
                      autologging_backends: AutologgingBackendParam,
                      callbacks_handler: CallbacksHandler,
                      log_seeds: bool,
                      delete_if_failed: bool,
                      log_system_info: bool):
    is_generator = isgeneratorfunction(func)
    setup_logging(experiment_name=group_config.name)
    mlflow.set_experiment(group_config.name)

    if data:
        DataLoader.load_data = lambda: data

    def objective(trial: optuna.Trial):
        with MlflowRunWithErrorHandling(callbacks_handler=callbacks_handler,
                                        delete_if_failed=delete_if_failed,
                                        trial=trial,
                                        run_name=f'Trial {trial.number}') as (run, finish_param):
            # Connect mlflow runs with optuna trials
            run_id = run.info.run_id
            finish_param['metric'] = None
            trial.set_user_attr('mlflow_run_id', run_id)

            logger.info(f'======== Starting Trial {trial.number} =========')

            setup_autologging(func, autologging_backends, log_seeds, log_system_info)
            Trial.get_current = lambda: trial

            # Fix default_worker.py name in Mlflow server
            mlflow.set_tag('mlflow.source.name', getfile(func))

            sampled_params = sample_params_from_distributions(trial, group_config.param_space)
            callbacks_handler.on_trial_start(trial=trial, sampled_params=sampled_params)

            all_params = {**group_config.params, **sampled_params}
            results = func(**all_params)
            metrics = {}

            if results is None:
                raise ExperimentError(
                    'Group main functions should always return a metric and/or an artifacts dictionary')

            if is_generator:
                for i, result in enumerate(results):
                    metrics, artifacts = _extract_metrics_and_artifacts(result)
                    trial.report(metrics[optimize_metric.name], i)
                    log_experiment_results(all_params, metrics, artifacts)
                    callbacks_handler.on_info_logged(metrics=metrics, artifacts=artifacts)
                    if trial.should_prune():
                        raise optuna.exceptions.TrialPruned()
            else:
                metrics, artifacts = _extract_metrics_and_artifacts(results)
                log_experiment_results(all_params, metrics, artifacts)
                callbacks_handler.on_info_logged(metrics=metrics, artifacts=artifacts)

            metric = metrics[optimize_metric.name]
            finish_param['metric'] = metric

            logger.info(f'======== Finished Trial {trial.number} =========')
            return metric

    optimize_optuna_study(study, objective=objective, group_config=group_config)


def _run_experiment(func: Callable,
                    config: ExperimentConfig,
                    autologging_backends: AutologgingBackendParam,
                    callbacks_handler: CallbacksHandler,
                    data_loader_func: Optional[Callable[[], Any]],
                    log_seeds: bool,
                    log_system_info: bool,
                    delete_if_failed: bool):
    mlflow.set_experiment(config.name)
    with MlflowRunWithErrorHandling(callbacks_handler, delete_if_failed=delete_if_failed):
        setup_autologging(func, autologging_backends, log_seeds, log_system_info)
        mlflow.set_tag('mlflow.source.name', getfile(func))

        if data_loader_func:
            DataLoader.load_data = data_loader_func

        results = _run_job(func, config)
        if not results:
            return
        results = results if isgeneratorfunction(func) else [results]
        for result in results:
            if result:
                metrics, artifacts = _extract_metrics_and_artifacts(result)
                log_experiment_results(config.params, metrics, artifacts)
                callbacks_handler.on_info_logged(metrics=metrics, artifacts=artifacts)


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


def _validate_project_settings(config: JobConfig, settings: Settings):
    settings = settings or Settings()
    if config.kind == JobTypes.GROUP and not settings.OPTUNA_STORAGE_URI:
        raise Exception('OPTUNA_STORAGE_URI not specified. Please, create or update your .env file.')
    return settings


def job(func: Optional[Callable] = None, *,
        callbacks: Optional[Iterable[Callback]] = None,
        autologging_backends: AutologgingBackendParam = None,
        optimization_metric: Union[Metric, str, None] = None,
        data_loader_func: Optional[Callable[[], Any]] = None,
        settings: Optional[Settings] = None,
        log_seeds: bool = True,
        log_system_info: bool = True,
        delete_if_failed: bool = False,
        **kwargs):
    """
    Experiment decorator.

    This decorator must be used as a wrapper for the main function of the experiment.
    It handles the tracking of the following information:
    - Parameters
    - Metrics
    - Artifacts
    - System information
    - Randomness (Numpy, Pytorch and TF seeds)

    It also handles the job execution on clusters and the hyperparameter optimization logic.

    :param func: Experiment main function
    :param callbacks: List of callbacks to notify when some event occur
    :param autologging_backends: List of frameworks whose autologging functionality will be enabled.
           To specify a supported framework you need to use the AutologgingBackend enum.
    :param optimization_metric: Metric to optimize. It is mandatory when running a group job, and it will be
           ignored when running a single experiment. The name of the metric should be the same as one of the
           keys that the experiment function returns.
    :param data_loader_func: Custom data loader class (not instance). It is necessary to specify this argument
           when using a DataLoader to share data across multiples processes.
    :param settings: Custom object that overrides environment variables.
    :param log_seeds: If true, it will log the seed of Numpy, Pytorch, or Python random's generator
           when the corresponding function to set the seed is called. Eg. when calling numpy.random.sed(...)
    :param log_system_info: Whether or not the system information, CPU, GPU, installed packages..., etc,
           should be logged
    :param delete_if_failed: If true, the experiment information will be removed in case of failure.
    :return: The wrapped function
    """
    if func is None:
        return partial(job,
                       callbacks=callbacks,
                       autologging_backends=autologging_backends,
                       optimize_metric=optimization_metric,
                       data_loader_func=data_loader_func,
                       log_seeds=log_seeds,
                       settings=settings,
                       log_system_info=log_system_info,
                       delete_if_failed=delete_if_failed,
                       **kwargs)

    if isinstance(optimization_metric, str):
        optimization_metric = Metric(name=optimization_metric)

    if optimization_metric:
        kwargs['metric'] = optimization_metric

    @wraps(func)
    def wrapper():
        config = _parse_experiment_arguments()
        config = config.copy(update=kwargs)
        callbacks_handler = CallbacksHandler(callbacks=list(callbacks or []), config=config)

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

        safe_project_settings = _validate_project_settings(config, settings)

        create_mlflow_experiment(experiment_name=config.name, settings=safe_project_settings)

        call_params = dict(func=func,
                           config=config,
                           autologging_backends=autologging_backends,
                           log_seeds=log_seeds,
                           callbacks_handler=callbacks_handler,
                           delete_if_failed=delete_if_failed,
                           data_loader_func=data_loader_func,
                           log_system_info=log_system_info)

        if config.kind == JobTypes.GROUP:
            _run_group(settings=safe_project_settings, **call_params)
        else:
            _job_runner(_run_experiment, config.ray_config, **call_params)

        elapsed_time = timedelta(seconds=ceil(t.tocvalue()))
        logger.info(f"Finished job {config.name} in {elapsed_time}")
        ray.shutdown()

    return wrapper

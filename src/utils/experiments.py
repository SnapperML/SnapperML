from typing import Union, List, Optional, Callable, cast
from functools import wraps, partial
from inspect import isgeneratorfunction
import sys
from math import ceil
from datetime import timedelta
import mlflow
from pytictoc import TicToc
from .logging import logger, setup_logging
from .cli import create_argument_parse_from_function, get_default_params_from_func
from .config import parse_config, get_validation_model
from .config.models import GroupConfig, ExperimentConfig, JobTypes, JobConfig, Metric
from .mlflow import AutologgingBackend, create_mlflow_experiment, log_experiment_results, setup_autologging
from .optuna import create_optuna_study
from .exceptions import NoMetricSpecified, ExperimentError
from optuna.exceptions import TrialPruned


def parse_experiment_arguments(experiment_func: Callable):
    parser = create_argument_parse_from_function(experiment_func, all_keywords=True, all_optional=True)
    parser.add_argument('--experiment_name', type=str, default=None)
    parser.add_argument('config_file', type=str)
    arguments = parser.parse_args()
    params = vars(arguments)
    config_file = params.pop('config_file')
    config = parse_config(config_file, get_validation_model)
    experiment_name = params.pop('experiment_name') or config.name
    return experiment_name, params, config


def run_group(func: Callable, overridden_params: dict, optimize_metric: Optional[Metric], group_config: GroupConfig):
    is_generator = isgeneratorfunction(func)
    default_params = get_default_params_from_func(func)

    if not optimize_metric:
        raise NoMetricSpecified()

    def objective(trial):
        with mlflow.start_run(run_name=f'Trial {trial.number}'):
            config_params = {k: v(k, trial) if callable(v) else v for k, v in group_config.param_space.items()}
            all_params = {**default_params, **config_params, **overridden_params}
            results = func(**all_params)
            metrics = {}

            if not results:
                raise ExperimentError('Group main functions should always return something!')

            if is_generator:
                # This overrides metrics variable
                for i, (metrics, artifacts) in enumerate(results):
                    trial.report(metrics[optimize_metric.name], i)
                    log_experiment_results(all_params, metrics, artifacts)
                    if trial.should_prune():
                        raise TrialPruned()
            else:
                metrics, artifacts = results
                log_experiment_results(overridden_params, metrics, artifacts)
            return metrics[optimize_metric.name]

    return create_optuna_study(objective,
                               group_config, metric=optimize_metric,
                               add_mlflow_callback=(not is_generator))


def run_experiment(func: Callable, overridden_params: dict, config: ExperimentConfig):
    with mlflow.start_run():
        results = run_job(func, overridden_params, config)
        if results:
            results = results if isgeneratorfunction(func) else results[func(**overridden_params)]
            for metrics, artifacts in results:
                log_experiment_results(overridden_params, metrics, artifacts)


def run_job(func: Callable, params: dict, config: JobConfig):
    default_params = get_default_params_from_func(func)
    all_params = {**default_params, **config.params, **params}
    return func(**all_params)


def experiment(func: Optional[Callable] = None, *,
               autologging_backends: Union[List[AutologgingBackend], AutologgingBackend, None] = None,
               optimize_metric: Union[Metric, str, None] = None):
    if func is None:
        return partial(experiment,
                       autologging_backends=autologging_backends,
                       optimize_metric=optimize_metric)

    if isinstance(optimize_metric, str):
        optimize_metric = Metric(name=optimize_metric)

    @wraps(func)
    def wrapper():
        experiment_name, overridden_params, config = parse_experiment_arguments(func)
        setup_logging(experiment_name=experiment_name)

        logger.info(f'======== Starting job {experiment_name} in {sys.argv[0]} =========')

        if config.kind == JobTypes.GROUP:
            config = cast(GroupConfig, config)
            logger.info(f"======== Group Config ========\n{config}")

        if config.kind == JobTypes.EXPERIMENT:
            config = cast(ExperimentConfig, config)
            logger.info(f"======== Experiment Config ========\n{config}")

        if config.kind == JobTypes.JOB:
            logger.info(f"======== Job Config ========\n{config}")

        t = TicToc()
        t.tic()

        if config.kind == JobTypes.JOB:
            run_job(func, overridden_params, config)
        else:
            create_mlflow_experiment(experiment_name=experiment_name)
            setup_autologging(autologging_backends)
            if config.kind == JobTypes.GROUP:
                run_group(func, overridden_params, optimize_metric, config)
            else:
                run_experiment(func, overridden_params, config)

        elapsed_time = timedelta(seconds=ceil(t.tocvalue()))
        logger.info(f"Finished job {experiment_name} in {elapsed_time}")

    return wrapper

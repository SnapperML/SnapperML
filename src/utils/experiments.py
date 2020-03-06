from functools import wraps, partial
from inspect import signature, isgeneratorfunction
import os
import json
import sys
from enum import Enum
from math import ceil
from datetime import timedelta
import mlflow
from pytictoc import TicToc
from .logging import logger, setup_logging
from .cli import create_argument_parse_from_function
from .config import parse_config
from .config.models import GroupConfig
from .optuna import create_optuna_study
from optuna.exceptions import TrialPruned


class AutologgingBackend(Enum):
    TENSORFLOW = "tensorflow"
    KERAS = "keras"
    FASTAI = "fastai"
    PYTORCH = "pytorch"


def create_mlflow_experiment(experiment_name, mlflow_tracking_uri="./experiments", mlflow_artifact_location=None):
    """
    Try to create an experiment if it doesn't exist
    Args:
        experiment_name (str): experiment name
        mlflow_tracking_uri (str): path or sql url for mlflow logging
        mlflow_artifact_location (str): path or s3bucket url for artifact
            logging. If none, it will default to a standard.
    Returns:
        None
    """
    try:
        exp = mlflow.create_experiment(
            experiment_name, artifact_location=mlflow_artifact_location)
        mlflow.set_tracking_uri(mlflow_tracking_uri)
        logger.info(f"mlflow - Created new experiment id: {exp}")
    except Exception as E:
        logger.info(f"ml-flow - {E}. Writing to same URI/artifact store")
    mlflow.set_experiment(experiment_name)


def log_experiment_results(params, metrics=None, artifacts=None):
    """
    Evaluate the model and log it with mlflow
    Args:
        params (dict): dictionary of parameters to log
        metrics (dict): dictionary of metrics to log
        artifacts (dict): dictionary of artifacts (path) to log
    Returns:
        None
    """
    metrics = metrics or {}
    artifacts = artifacts or {}
    logger.info(f"Logging params {params}")
    logger.info(f"Logging metrics {metrics}")
    logger.info(f"Logging artifacts {artifacts}")
    for key, val in params.items():
        mlflow.log_param(key, val)
    for key, val in metrics.items():
        mlflow.log_metric(key, val)
    for key, val in artifacts.items():
        mlflow.log_artifact(val)


def setup_autologging(backend):
    if isinstance(backend, list):
        for b in backend:
            setup_autologging(b)
    elif backend == AutologgingBackend.TENSORFLOW:
        import mlflow.tensorflow
        mlflow.tensorflow.autolog()
        logger.info("Enabled autologging for Tensorflow")
    elif backend == AutologgingBackend.KERAS:
        import mlflow.keras
        mlflow.keras.autolog()
        logger.info("Enabled autologging for Keras")
    elif backend == AutologgingBackend.FASTAI:
        # TODO: implement autologging for fastai
        logger.info("Enabled autologging for Fastai")
    elif backend == AutologgingBackend.PYTORCH:
        # TODO: implement autologging for pytorch
        logger.info("Enabled autologging for Pytorch")
    elif backend:
        raise Exception(f'Not supported Autologging backend {backend}')


def parse_experiment_arguments(experiment_func):
    parser = create_argument_parse_from_function(experiment_func, all_keywords=True)
    parser.add_argument('--experiment_name', type=str, default=generate_experiment_name())
    parser.add_argument('--group_config', type=str, default=None)
    arguments = parser.parse_args()
    params = vars(arguments)
    experiment_name = params.pop('experiment_name', None)
    group_config = params.pop('group_config', None)

    if group_config:
        try:
            group_config = json.loads(group_config)
        except json.JSONDecodeError:
            if os.path.exists(group_config):
                group_config = parse_config(group_config)
        group_config = GroupConfig(**group_config)

    return experiment_name, params, group_config


def generate_experiment_name():
    base = os.path.basename(sys.argv[0])
    return os.path.splitext(base)[0]


def run_group(func, params, optimize_metric: str, group_config: GroupConfig):
    is_generator = isgeneratorfunction(func)

    def objective(trial):
        new_params = {k: v(trial) if callable(v) else v for k, v in group_config.param_space.items()}
        all_params = {**params, **new_params}
        results = func(**all_params)

        if not results:
            raise Exception('Group main functions should always return something!')

        results = results if is_generator else results[func(**params)]
        metrics = {}

        if is_generator:
            # This overrides metrics variable
            for i, (metrics, artifacts) in enumerate(results):
                trial.report(metrics[optimize_metric], i)
                log_experiment_results(params, metrics, artifacts)
                if trial.should_prune():
                    raise TrialPruned()
        else:
            metrics, artifacts = results
            log_experiment_results(params, metrics, artifacts)
        return metrics[optimize_metric]

    return create_optuna_study(objective, group_config)


def run_experiment_main(func, params):
    results = func(**params)
    if results:
        results = results if isgeneratorfunction(func) else results[func(**params)]
        for metrics, artifacts in results:
            log_experiment_results(params, metrics, artifacts)


def experiment(func=None, *, autologging_backends=None, optimize_metric=None):
    if func is None:
        return partial(experiment, autologging_backends=autologging_backends)

    sig = signature(func)

    default_params = {
        param.name: param.default for param in sig.parameters.values()
        if param.kind == param.POSITIONAL_OR_KEYWORD and param.default != param.empty
    }

    @wraps(func)
    def wrapper():
        experiment_name, params, group_config = parse_experiment_arguments(func)
        setup_logging(experiment_name=experiment_name)

        create_mlflow_experiment(experiment_name=experiment_name)

        logger.info(f'Starting job {experiment_name} in {sys.argv[0]}')
        t = TicToc()
        t.tic()

        with mlflow.start_run():
            setup_autologging(autologging_backends)
            params = {**default_params, **params}
            if group_config:
                run_group(func, params, optimize_metric, group_config)
            else:
                run_experiment_main(func, params)

        logger.info(f"Finished job {experiment_name} in {timedelta(seconds=ceil(t.tocvalue()))}")

    return wrapper

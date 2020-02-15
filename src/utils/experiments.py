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
from .input import DataLoader


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


def log_experiment(params, metrics=None, artifacts=None):
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
    parser.add_argument('--input', type=str, default=None)
    arguments = parser.parse_args()
    params = vars(arguments)
    experiment_name = params.pop('experiment_name', None)
    input_config = params.pop('input', None)

    if input_config:
        try:
            input_config = json.loads(input_config)
        except json.JSONDecodeError:
            if os.path.exists(input_config):
                input_config = parse_config(input_config)

    return experiment_name, params, input_config


def generate_experiment_name():
    base = os.path.basename(sys.argv[0])
    return os.path.splitext(base)[0]


def experiment(func=None, *, autologging_backends=None):
    if func is None:
        return partial(experiment, autologging_backends=autologging_backends)

    sig = signature(func)

    default_params = {
        param.name: param.default for param in sig.parameters.values()
        if param.kind == param.POSITIONAL_OR_KEYWORD and param.default != param.empty
    }

    @wraps(func)
    def wrapper():
        experiment_name, params, input_config = parse_experiment_arguments(func)
        setup_logging(experiment_name=experiment_name)
        if input_config:
            DataLoader.initialize_instance(**input_config)
        create_mlflow_experiment(experiment_name=experiment_name)
        logger.info(f'Starting job {experiment_name} in {sys.argv[0]}')
        t = TicToc()
        t.tic()

        with mlflow.start_run():
            setup_autologging(autologging_backends)
            params = {**default_params, **params}
            results = func(**params) if isgeneratorfunction(func) else [func(**params)]
            for metrics, artifacts in results:
                log_experiment(params, metrics, artifacts)
        logger.info(f"Finished job {experiment_name} in "
                    f"{timedelta(seconds=ceil(t.tocvalue()))}")

    return wrapper

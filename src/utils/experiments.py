from functools import wraps
from inspect import signature
import sys
from math import ceil
from datetime import timedelta
import mlflow
from pytictoc import TicToc
from .logging import logger, setup_logging
from .cli import cli_decorator
from .config import parse_config


def log_experiment(
        experiment_name,
        params,
        metrics=None,
        artifacts=None,
        mlflow_tracking_uri="./experiments",
        mlflow_artifact_location=None,
):
    """
    Evaluate the model and log it with mlflow
    Args:
        params (dict): dictionary of parameters to log
        metrics (dict): dictionary of metrics to log
        artifacts (dict): dictionary of artifacts (path) to log
        experiment_name (str): experiment name
        mlflow_tracking_uri (str): path or sql url for mlflow logging
        mlflow_artifact_location (str): path or s3bucket url for artifact
            logging. If none, it will default to a standard.
    Returns:
        None
    """
    metrics = {} if not metrics else artifacts
    artifacts = {} if not artifacts else artifacts

    # Try to create an experiment if it doesn't exist
    try:
        exp = mlflow.create_experiment(
            experiment_name, artifact_location=mlflow_artifact_location)
        mlflow.set_tracking_uri(mlflow_tracking_uri)
        logger.info(f"mlflow - Created new experiment id: {exp}")
    except Exception as E:
        logger.info(f"ml-flow - {E}. Writing to same URI/artifact store")

    mlflow.set_experiment(experiment_name)

    with mlflow.start_run():
        for key, val in params.items():
            logger.info(f"Logging param {key}")
            mlflow.log_param(key, val)
        for key, val in metrics.items():
            logger.info(f"Logging metric {key}")
            mlflow.log_metric(key, val)
        for key, val in artifacts.items():
            logger.info(f"Logging artifact {key}")
            mlflow.log_artifact(val)


def experiment(func):
    sig = signature(func)
    default_params = {
        param.name: param.default for param in sig.parameters.values()
        if param.kind == param.POSITIONAL_OR_KEYWORD and param.default != param.empty
    }

    @wraps(func)
    def wrapper(config_file):
        config = parse_config(config_file)
        experiment_name = config_file["experiment"]

        setup_logging(experiment_name=experiment_name)
        logger.info(f"Starting job {func.__name__}() in {sys.argv[0]}")
        t = TicToc()
        t.tic()

        params = config.get('params', {})
        params = {**default_params, **params}
        metrics, artifacts = func(**params)

        log_experiment(
            experiment_name=experiment_name,
            params=params,
            metrics=metrics,
            artifacts=artifacts
        )

        logger.info(f"Finished job {func.__name__}() in "
                    f"{timedelta(seconds=ceil(t.tocvalue()))}")

    return cli_decorator(wrapper)

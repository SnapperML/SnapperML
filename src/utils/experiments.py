from functools import wraps
from inspect import signature
import os
import sys
from math import ceil
from datetime import timedelta
import mlflow
from pytictoc import TicToc
from .logging import logger, setup_logging
from .cli import create_argument_parse_from_signature


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

    logger.info(f"Logging params {params}")
    logger.info(f"Logging metrics {metrics}")
    logger.info(f"Logging artifacts {artifacts}")

    with mlflow.start_run():
        for key, val in params.items():
            mlflow.log_param(key, val)
        for key, val in metrics.items():
            mlflow.log_metric(key, val)
        for key, val in artifacts.items():
            mlflow.log_artifact(val)


def parse_experiment_arguments(experiment_signature):
    parser = create_argument_parse_from_signature(experiment_signature, all_keywords=True)
    parser.add_argument('--experiment_name', type=str, default=generate_experiment_name())
    arguments = parser.parse_args()
    params = vars(arguments)
    experiment_name = params.pop('experiment_name', None)
    return experiment_name, params


def generate_experiment_name():
    base = os.path.basename(sys.argv[0])
    return os.path.splitext(base)[0]


def experiment(func):
    sig = signature(func)
    default_params = {
        param.name: param.default for param in sig.parameters.values()
        if param.kind == param.POSITIONAL_OR_KEYWORD and param.default != param.empty
    }

    @wraps(func)
    def wrapper():
        experiment_name, params = parse_experiment_arguments(sig)

        if not experiment_name:
            experiment_name = generate_experiment_name()

        setup_logging(experiment_name=experiment_name)
        logger.info(f'Starting job {experiment_name} in {sys.argv[0]}')
        t = TicToc()
        t.tic()

        params = {**default_params, **params}
        metrics, artifacts = func(**params)
        log_experiment(
            experiment_name=experiment_name,
            params=params,
            metrics=metrics,
            artifacts=artifacts
        )

        logger.info(f"Finished job {experiment_name} in "
                    f"{timedelta(seconds=ceil(t.tocvalue()))}")

    return wrapper

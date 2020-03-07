from enum import Enum
from typing import Optional, Union, List

import mlflow
import mlflow.keras
import mlflow.tensorflow

from src.utils.logging import logger


class AutologgingBackend(Enum):
    TENSORFLOW = "tensorflow"
    KERAS = "keras"
    FASTAI = "fastai"
    PYTORCH = "pytorch"


def create_mlflow_experiment(experiment_name: str,
                             mlflow_tracking_uri: str ="./experiments",
                             mlflow_artifact_location: str = None):
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


def log_experiment_results(params: dict,
                           metrics: Optional[dict] = None,
                           artifacts: Optional[dict] = None):
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


def setup_autologging(backend: Union[List[AutologgingBackend], AutologgingBackend]):
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

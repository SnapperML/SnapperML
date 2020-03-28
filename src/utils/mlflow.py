from enum import Enum
from typing import Optional, Union, List

import mlflow

from src.utils.logging import logger


class AutologgingBackend(Enum):
    TENSORFLOW = "tensorflow"
    KERAS = "keras"
    FASTAI = "fastai"


def create_mlflow_experiment(experiment_name: str):
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
        exp = mlflow.create_experiment(experiment_name)
        logger.info(f"mlflow - Created new experiment id: {exp}")
    except Exception:
        logger.info(f"mlflow - Experiment already exists. Writing to same URI/artifact store")
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
    mlflow.log_params(params)
    mlflow.log_metrics(metrics)
    for key, val in artifacts.items():
        mlflow.log_artifact(val)
    all_logs = {'params': params, 'metrics': metrics, 'artifacts': artifacts}
    logger.info(f"- mlflow - Logging experiment results to Mlflow: {all_logs}")


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
        import mlflow.fastai
        mlflow.fastai.fastai.autolog()
        logger.info("Enabled autologging for Fastai")
    elif backend:
        raise Exception(f'Autologging backend {backend} not supported')

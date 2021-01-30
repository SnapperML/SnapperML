from enum import Enum
import random
import os
import sys
import tempfile
import shutil
from typing import Optional, Union, List, Callable, Any
import gorilla
import mlflow
from easyprocess import EasyProcess, EasyProcessError
from cpuinfo import get_cpu_info

from .logging import logger
from .utils import monkey_patch_imported_function
from .config.models import Settings


class AutologgingBackend(Enum):
    TENSORFLOW = "tensorflow"
    KERAS = "keras"
    FASTAI = "fastai"
    XGBOOST = 'xgboost'
    LIGHTGBM = 'lightgbm'


AutologgingBackendParam = Union[List[AutologgingBackend], AutologgingBackend, None]


def create_mlflow_experiment(experiment_name: str, settings: Settings):
    """
    Try to create an experiment if it doesn't exist
    Args:
        experiment_name (str): experiment name
        settings(str): Config object
    Returns:
        None
    """
    try:
        mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)
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


def _get_seed_initializer_patch(target: Callable, module: Any, module_name: str, function_name: str):
    current_seed = None

    def seed(new_seed):
        nonlocal current_seed
        if not current_seed:
            mlflow.set_tag(f'{module_name} seed', new_seed)
        current_seed = new_seed
        original = gorilla.get_original_attribute(module, function_name)
        original(new_seed)

    original_func = getattr(module, function_name)
    monkey_patch_imported_function(original_func, seed, target)
    settings = gorilla.Settings(allow_hit=True, store_hit=True)
    return gorilla.Patch(module, function_name, seed, settings)


def _log_system_info():
    mlflow.set_tag('Python', sys.version)
    cpu_info = get_cpu_info().get('brand')

    if cpu_info:
        mlflow.set_tag('CPU', cpu_info)

    try:
        nvidia_info = EasyProcess('nvidia-smi').call().stdout
        mlflow.set_tag('gpu', nvidia_info)
    except EasyProcessError:
        pass

    try:
        pip_packages = EasyProcess('pip3 freeze').call().stdout
        log_text_file('requirements.txt', pip_packages)
    except EasyProcessError:
        pass


def log_text_file(filename: str, content: str):
    tempdir = tempfile.mkdtemp()
    try:
        filepath = os.path.join(tempdir, filename)
        with open(filepath, 'w') as f:
            f.write(content)
        mlflow.log_artifact(filepath)
    finally:
        shutil.rmtree(tempdir)


def _setup_autologging(target: Callable, backend: AutologgingBackend, log_seeds: bool):
    patch = None

    if backend == AutologgingBackend.TENSORFLOW:
        import mlflow.tensorflow
        import tensorflow as tf
        patch = log_seeds and _get_seed_initializer_patch(target, tf.random, 'Tensorflow', 'set_seed')
        mlflow.tensorflow.autolog()
        logger.info("Enabled autologging for Tensorflow")
    elif backend == AutologgingBackend.KERAS:
        import mlflow.keras
        import tensorflow as tf
        patch = log_seeds and _get_seed_initializer_patch(target, tf.random, 'Tensorflow', 'set_seed')
        mlflow.keras.autolog()
        logger.info("Enabled autologging for Keras")
    elif backend == AutologgingBackend.FASTAI:
        import mlflow.fastai
        import torch
        mlflow.fastai.autolog()
        patch = log_seeds and _get_seed_initializer_patch(target, torch.random, 'Pytorch', 'manual_seed')
        logger.info("Enabled autologging for Fastai")
    elif backend == AutologgingBackend.XGBOOST:
        import mlflow.xgboost
        mlflow.xgboost.autolog()
        # patch = log_seeds and _get_seed_initializer_patch(target, torch.random, 'Pytorch', 'manual_seed')
        logger.info("Enabled autologging for Xgboost")
    elif backend == AutologgingBackend.LIGHTGBM:
        import mlflow.lightgbm
        mlflow.lightgbm.autolog()
        # patch = log_seeds and _get_seed_initializer_patch(target, torch.random, 'Pytorch', 'manual_seed')
        logger.info("Enabled autologging for LightGBM")
    elif backend:
        raise Exception(f'Autologging backend {backend} not supported')

    if patch:
        gorilla.apply(patch)


def setup_autologging(target: Callable,
                      backend: AutologgingBackendParam,
                      log_seeds: bool,
                      log_system_info: bool):
    if isinstance(backend, list):
        for b in backend:
            _setup_autologging(target, b, log_seeds)
    elif backend:
        _setup_autologging(target, backend, log_seeds)

    if log_seeds:
        patches = [_get_seed_initializer_patch(target, random, 'Python Random', 'seed')]
        try:
            import numpy as np
            patches.append(_get_seed_initializer_patch(target, np.random, 'Numpy', 'seed'))
        except ModuleNotFoundError:
            pass
        for patch in patches:
            gorilla.apply(patch)

    if log_system_info:
        _log_system_info()

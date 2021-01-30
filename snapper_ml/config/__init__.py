import os
import yaml
from pathlib import Path
import json

from ..logging import logger
from typing import Callable, Type, TypeVar, Union
from pydantic import BaseModel, ValidationError
from .models import JobConfig, JobTypes, GroupConfig, ExperimentConfig


T = TypeVar('T', bound=BaseModel)
ModelFactory = Callable[[dict], Type[T]]
SUPPORTED_EXTENSIONS = ['.yaml', '.yml', '.json']


def parse_config(config_file: Union[str, Path], model: Union[BaseModel, ModelFactory] = None) -> T:
    if isinstance(config_file, str):
        config_file = Path(config_file)

    with config_file.open('r') as f:
        document = os.path.expandvars(f.read())
        ext = config_file.suffix
        config = yaml.safe_load(document) if ext in ['.yml', '.yaml'] else json.loads(document)
        if model:
            try:
                model = model(config) if callable(model) else model
                return model.parse_obj(config)
            except ValidationError as e:
                logger.error(e)
                raise e


def get_validation_model(config: dict) -> Type[JobConfig]:
    kind = config.get('kind')
    if kind == JobTypes.GROUP.value:
        return GroupConfig
    if kind == JobTypes.JOB.value:
        return JobConfig
    else:
        return ExperimentConfig

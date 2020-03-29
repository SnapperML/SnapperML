import os
import sys
import yaml

from ..logging import logger
from typing import Callable, Type, TypeVar, Union
from pydantic import BaseModel, ValidationError
from .models import JobConfig, JobTypes, GroupConfig, ExperimentConfig


T = TypeVar('T', bound=BaseModel)

ModelFactory = Callable[[dict], Type[T]]


def parse_config(config_file: str, model: Union[BaseModel, ModelFactory] = None) -> T:
    with open(config_file, "r") as f:
        yaml_document = os.path.expandvars(f.read())
        config = yaml.safe_load(yaml_document)
        if model:
            try:
                model = model(config) if callable(model) else model
                return model(**config)
            except ValidationError as e:
                logger.error(e)
                sys.exit(1)


def get_validation_model(config: dict) -> Type[JobConfig]:
    kind = config.get('kind')
    if kind == JobTypes.GROUP.value:
        return GroupConfig
    if kind == JobTypes.EXPERIMENT.value:
        return ExperimentConfig
    else:
        return JobConfig

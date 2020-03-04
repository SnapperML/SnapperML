"""
This module is for config utility functions.
"""
import yaml
import os
import sys
from typing import Callable, Union, Type, TypeVar
from src.utils.logging import logger
from pydantic import BaseModel, ValidationError

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

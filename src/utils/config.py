"""
This module is for config utility functions.
"""
import yaml
import os
import sys
from schema import Schema, SchemaError
from src.utils.logging import logger


def parse_config(config_file, schema=None):
    with open(config_file, "r") as f:
        yaml_document = os.path.expandvars(f.read())
        config = yaml.safe_load(yaml_document)
        if schema:
            try:
                return Schema(schema).validate(config)
            except SchemaError as e:
                logger.error(f'SchemaValidationError: {e}')
                sys.exit(1)

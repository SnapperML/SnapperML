"""
This module is for config utility functions.
"""
import yaml
import os
from schema import Schema


def parse_config(config_file, schema=None):
    with open(config_file, "r") as f:
        yaml_document = os.path.expandvars(f.read())
        config = yaml.safe_load(yaml_document)
        if schema:
            return Schema(schema).validate(config)

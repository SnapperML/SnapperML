"""
This module is for config utility functions.
"""
import yaml
import os


def parse_config(config_file):
    with open(config_file, "r") as f:
        yaml_document = os.path.expandvars(f.read())
        return yaml.safe_load(yaml_document)

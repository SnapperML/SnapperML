"""
This module is for config utility functions.
"""
import yaml


def parse_config(config_file):
    with open(config_file, "rb") as f:
        return yaml.safe_load(f)

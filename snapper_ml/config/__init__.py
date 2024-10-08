import os
import yaml
from pathlib import Path
import json
import termcolor
import ruamel.yaml


from ..loggings import logger
from typing import Callable, Type, TypeVar, Union
from pydantic import BaseModel, ValidationError
from .models import JobConfig, JobTypes, GroupConfig, ExperimentConfig


T = TypeVar('T', bound=BaseModel)
ModelFactory = Callable[[dict], Type[T]]
SUPPORTED_EXTENSIONS = ['.yaml', '.yml', '.json']


def _print_error_line(document_lines, first_line, last_line, error_locations):
    lines = []

    for i in range(first_line, last_line):
        line = f'    {i}: {document_lines[i]}'

        if error_locations and document_lines[i].lstrip().startswith(f'{error_locations[-1]}:'):
            line = termcolor.colored(line, color='red')

        lines.append(line)

    logger.error('\n'.join(lines))


def _print_validation_error(config_file: Union[None, str, Path], validation_error: ValidationError):
    prefix = termcolor.colored('Error:', color='red')

    if config_file:
        document = os.path.expandvars(config_file.read_text())
        yaml_doc = yaml.load(document, ruamel.yaml.RoundTripLoader)
        document_lines = document.split('\n')
    else:
        yaml_doc = {}
        document_lines = []

    other_errors = []

    for error in validation_error.errors():
        locations = error['loc']
        lines = []
        current = yaml_doc

        for key in locations:
            if key in current and hasattr(current[key], 'lc'):
                lines.append(current[key].lc.line)
                current = current[key]

        if len(locations) == 1 and locations[0] in yaml_doc:
            lines = [i for i, line in enumerate(document_lines) if line.startswith(f'{locations[-1]}')]

        if lines:
            offset = len(yaml_doc[locations[0]]) if isinstance(yaml_doc.get(locations[0]), (list, dict)) else 0
            first_line, last_line = lines[0] - 1, lines[0] + offset + 1
            logger.error(f'\n{prefix} {error["msg"]}')
            logger.error(f'  On file {config_file}, Line {lines[-1]}')
            _print_error_line(document_lines, first_line, last_line, locations)
        else:
            other_errors.append(error)

    for error in other_errors:
        logger.error(f'\n{prefix} {error["loc"][0]} {error["msg"]}')


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

                return model.model_validate(config)
            except ValidationError as e:
                _print_validation_error(config_file, e)
                exit(1)


def get_validation_model(config: dict) -> Type[JobConfig]:
    kind = config.get('kind')
    if kind == JobTypes.GROUP.value:
        return GroupConfig
    if kind == JobTypes.JOB.value:
        return JobConfig
    else:
        return ExperimentConfig

# TODO: Add support for remote job scheduling through Swarm or OpenFaas
# TODO: Add support for running group of jobs in parallel / Hyperparams
import os
from enum import Enum
from dotenv import find_dotenv, load_dotenv
from src.utils.cli import cli_decorator
from src.utils.config import parse_config
from src.utils.logging import logger, setup_logging
from src.utils.optuna.optuna import PRUNERS, SAMPLERS
import subprocess
import docker
from typing import Optional, List, Type, Union
from pydantic import BaseModel, validator, DirectoryPath, PositiveInt, root_validator


class JobTypes(Enum):
    JOB = "job"
    EXPERIMENT = "experiment"
    GROUP = "group"


class DockerConfig(BaseModel):
    dockerfile: Optional[str]
    image: Optional[str]
    context: Optional[DirectoryPath] = None
    args: dict = {}

    @root_validator()
    def check_card_number_omitted(cls, values):
        if values.get('image') and values.get('dockerfile'):
            raise ValueError('image and dockerfile fields cannot be used simultaneously. Use one of them.')
        return values


class JobConfig(BaseModel):
    name: str
    run: Union[str, List[str]]
    kind: JobTypes = JobTypes.EXPERIMENT
    docker_config: Optional[DockerConfig]


class GroupConfig(JobConfig):
    sampler: str
    pruner: str
    num_trials: PositiveInt
    concurrent_workers: PositiveInt
    # Improve by adding dict of classes
    param_space: dict

    @validator('sampler')
    def sampler_must_exists(cls, value):
        samplers = list(SAMPLERS.keys())
        if value not in samplers:
            raise ValueError(f'Sampler must be one of the following: {samplers}')
        return value

    @validator('pruner')
    def pruner_must_exists(cls, value):
        pruners = list(PRUNERS.keys())
        if value not in pruners:
            raise ValueError(f'Pruner must be one of the following: {pruners}')
        return value


class ExperimentConfig(JobConfig):
    # TODO: Improve by adding experiment signature
    params: dict = {}


def get_validation_model(config: dict) -> Type[JobConfig]:
    job = JobConfig(**config)
    kind = job.kind
    if kind == JobTypes.GROUP:
        return GroupConfig
    if kind == JobTypes.EXPERIMENT:
        return ExperimentConfig
    else:
        return JobConfig


def extract_string_from_docker_log(log):
    return log['stream'].splitlines() if 'stream' in log else []


def create_low_level_docker_client(**kwargs):
    params = docker.api.client.utils.kwargs_from_env(**kwargs)
    return docker.APIClient(**params)


def extract_docker_config_params(docker_config):
    dockerfile = docker_config.get('dockerfile', None)
    context = docker_config.get('context', None)
    image = docker_config.get('image', None)
    build_args = docker_config.get('args')
    return dockerfile, context, image, build_args


def build_image(client, context, dockerfile, build_args):
    if not context:
        head, tail = os.path.split(dockerfile)
        build_params = {'path': head, 'dockerfile': tail}
    else:
        dockerfile_file = open(dockerfile, 'rb')
        build_params = {'path': context, 'fileobj': dockerfile_file}
    logs = client.build(rm=True, buildargs=build_args, decode=True, **build_params)
    logs_str = []
    for log in logs:
        chunk = extract_string_from_docker_log(log)
        logs_str.extend(chunk)
        for line in chunk:
            logger.info(line)
    return logs_str[-1].strip().split(' ')[-1]


def run_docker_container(image, command):
    client = docker.from_env()
    container = client.containers.run(
        image,
        ['-c', command],
        auto_remove=True,
        entrypoint='sh',
        volumes={os.getcwd(): {'bind': '/mnt/', 'mode': 'rw'}},
        working_dir='/mnt/',
        detach=True,
    )
    logs = container.attach(stdout=True, stderr=True, stream=True, logs=True)
    for chunk in logs:
        logger.info(chunk.decode('utf-8'))
    logger.info('Finished job!')


def process_docker(config: DockerConfig, command: Union[List[str], str]):
    client = create_low_level_docker_client()
    commands = command if isinstance(command, list) else [command]
    command_single_expression = " && ".join(commands)
    image = config.image
    if config.dockerfile:
        logger.info('Building docker image...')
        image = build_image(client, config.context, config.dockerfile, config.args)
    if image:
        logger.info('Running job on docker container...')
        run_docker_container(image, command_single_expression)


def run_job(job: JobConfig):
    logger.info(f"\nRunning {job.kind}: {job.name}")

    if isinstance(job, ExperimentConfig):
        run_commands = job.run if isinstance(job.run, list) else [job.run]
        argv = ' '.join([f'--{k} {v}' for k, v in job.params.items()])
        bash_commands = [f'PYTHONPATH=. python3 {cmd} {argv}' for cmd in run_commands]
    else:
        bash_commands = job.run

    if job.docker_config:
        process_docker(job.docker_config, bash_commands)
    else:
        for commands in bash_commands:
            subprocess.run(commands, shell=True)


@cli_decorator
def main(config_file):
    load_dotenv(find_dotenv())
    config = parse_config(config_file, get_validation_model)
    setup_logging(experiment_name=config.name)
    run_job(config)


if __name__ == '__main__':
    main()

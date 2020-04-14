# TODO: Add support for remote job scheduling through Swarm or OpenFaas

import os
import subprocess
from pathlib import Path
from typing import List, Union
from dotenv import find_dotenv, load_dotenv
import docker
import typer

from ..config import parse_config, get_validation_model
from ..config.models import DockerConfig, JobConfig, ExperimentConfig, GroupConfig
from ..logging import logger, setup_logging


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


def run_job(job: JobConfig, config_file: str):
    if isinstance(job, ExperimentConfig) or isinstance(job, GroupConfig):
        run_commands = job.run if isinstance(job.run, list) else [job.run]
        bash_commands = [f'python3 {cmd} {config_file}' for cmd in run_commands]
    else:
        bash_commands = job.run

    if job.docker_config:
        process_docker(job.docker_config, bash_commands)
    else:
        for commands in bash_commands:
            subprocess.run(commands, shell=True)


app = typer.Typer()

ExistentFile = typer.Argument(
    ...,
    exists=True,
    file_okay=True,
    dir_okay=False,
    writable=False,
    readable=True,
    resolve_path=True,
)


@app.command()
def run(config_file: Path = ExistentFile):
    load_dotenv(find_dotenv())
    config = parse_config(config_file, get_validation_model)
    setup_logging(experiment_name=config.name)
    run_job(config, str(config_file))

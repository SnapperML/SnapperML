# TODO: Add support for remote job scheduling through Swarm or OpenFaas
# TODO: Add support for running group of jobs in parallel / Hyperparams
import os
import json
from enum import Enum
from dotenv import find_dotenv, load_dotenv
from src.utils.cli import cli_decorator
from src.utils.config import parse_config
from src.utils.logging import logger, setup_logging
from src.utils.input import SUPPORTED_EXTENSIONS
import subprocess
import docker
from schema import And, Or, Optional, Schema


class JobTypes(Enum):
    JOB = "job"
    EXPERIMENT = "experiment"
    GROUP = "group"


SCHEMA = {
    'name': Schema(str, error='Experiment/Job name must be a string'),

    Optional('build', 'Invalid build configuration, you must use a dictionary'): {
        Or("dockerfile", "image", 'Invalid dockerfile or image, you must only only one of them', only_one=True): str,
        Optional('context', error='Invalid context, you must use an existent directory', default=''): str,
        Optional('args', default={}): dict,
    },

    Optional('params', error='Invalid params, you must use a dictionary', default={}): dict,

    Optional('input', error='Invalid input, you must use a dictionary', default={}): {
        'file': And(Schema(str, error='You must specify an input file as string'),
                    Schema(os.path.exists, error='You must specify an existing input file'),
                    Schema(lambda f: os.path.splitext(f)[-1] in SUPPORTED_EXTENSIONS,
                           error=f'Unsupported input file extension. Must be one of the following: {SUPPORTED_EXTENSIONS}')),
        Optional('columns', default='*'): [str, dict, list],
        Optional('batch_size', default=None): int,
        Optional('tree', default=''): str,
    },

    'run': Schema([str], error='Run key must be a list of commands'),
}


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


def process_docker(docker_config, command):
    client = create_low_level_docker_client()
    commands = command if isinstance(command, list) else [command]
    command_single_expression = " && ".join(commands)
    dockerfile, context, image, build_args = extract_docker_config_params(docker_config)
    if dockerfile:
        logger.info('Building docker image...')
        image = build_image(client, context, dockerfile, build_args)
    if image:
        logger.info('Running job on docker container...')
        run_docker_container(image, command_single_expression)


def extract_info_base(config):
    experiment_name = config["name"]
    kind = config.get("kind", JobTypes.EXPERIMENT)
    run_command = config['run']
    input_config = config.get('input')
    docker_config = config.get('build')
    return experiment_name, kind, run_command, input_config, docker_config


def run_experiment(params, experiment_name, commands, docker_config, input_config, kind):
    logger.info(f"\nRunning experiment: {experiment_name}")
    run_commands = commands if isinstance(commands, list) else [commands]

    if input_config:
        input_json = json.dumps(input_config)
        run_commands = [f"{cmd} --input='{input_json}'" for cmd in commands]

    if kind == JobTypes.EXPERIMENT:
        argv = ' '.join([f'--{k} {v}' for k, v in params.items()])
        bash_commands = [f'PYTHONPATH=. python3 {cmd} {argv}' for cmd in run_commands]
    else:
        bash_commands = commands

    if docker_config:
        process_docker(docker_config, bash_commands)
    else:
        for commands in bash_commands:
            subprocess.run(commands, shell=True)


@cli_decorator
def main(config_file):
    load_dotenv(find_dotenv())
    config = parse_config(config_file, SCHEMA)
    experiment_name, kind, run_command, input_config, docker_config = extract_info_base(config)
    setup_logging(experiment_name=experiment_name)
    run_experiment(
        params=config.get('params', {}),
        experiment_name=experiment_name,
        commands=run_command,
        docker_config=docker_config,
        input_config=input_config,
        kind=kind)


if __name__ == '__main__':
    main()

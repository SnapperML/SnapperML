import os
from enum import Enum
from dotenv import find_dotenv, load_dotenv
from src.utils.cli import cli_decorator
from src.utils.config import parse_config
from src.utils.logging import logger, setup_logging
import subprocess
import docker


class ExperimentTypes(Enum):
    JOB = "job"
    EXPERIMENT = "experiment"
    GROUP = "group"


def extract_docker_config_params(docker_config):
    dockerfile = docker_config.get('dockerfile')
    context = docker_config.get('context', None)
    image = docker_config.get('image', None)
    build_args = docker_config.get('args', {})
    return dockerfile, context, image, build_args


def build_image(client, context, dockerfile, build_args):
    if not context:
        head, tail = os.path.split(dockerfile)
        build_params = {'path': head, 'dockerfile': tail}
    else:
        dockerfile_file = open(dockerfile, 'rb')
        build_params = {'path': context, 'fileobj': dockerfile_file}
    print(build_params)
    image, logs = client.images.build(rm=True, buildargs=build_args, **build_params)
    for log in logs:
        logger.debug(log.get('stream', ''))
    return image.id


def run_docker_container(client, image, command):
    logs = client.containers.run(
        image,
        ['-c', command],
        auto_remove=True,
        entrypoint='sh',
        volumes={os.getcwd(): {'bind': '/mnt/', 'mode': 'rw'}},
        working_dir='/mnt/'
    )
    logger.debug(logs)


def process_docker(docker_config, command):
    client = docker.from_env()
    commands = command if isinstance(command, list) else [command]
    command_single_expression = " && ".join(commands)
    dockerfile, context, image, build_args = extract_docker_config_params(docker_config)
    if dockerfile:
        image = build_image(client, context, dockerfile, build_args)
    if image:
        run_docker_container(client, image, command_single_expression)


def extract_docker_build_info(config):
    docker_config = config.get('build')
    if not docker_config:
        return None
    else:
        image = config.get('image')
        dockerfile = config.get('dockerfile')
        if image and dockerfile or (not image and not dockerfile):
            # TODO: Throw config parsing error
            pass
        return docker_config


def extract_info_base(config):
    experiment_name = config["name"]
    kind = config.get("type")
    run_command = config['run']
    return experiment_name, kind, run_command


def run_experiment(config_file, experiment_name, command, docker_config):
    logger.info(f"\nRunning experiment: {experiment_name}")
    run_commands = command if isinstance(command, list) else [command]
    bash_commands = [f'python3 {cmd} --config_file {config_file}' for cmd in run_commands]
    if docker_config:
        process_docker(docker_config, bash_commands)
    else:
        for command in bash_commands:
            subprocess.run(command, shell=True)


@cli_decorator
def main(config_file):
    load_dotenv(find_dotenv())
    config = parse_config(config_file)
    experiment_name, kind, run_command = extract_info_base(config)
    docker_config = extract_docker_build_info(config)
    setup_logging(experiment_name=experiment_name)
    run_experiment(config_file, experiment_name, run_command, docker_config)


if __name__ == '__main__':
    main()

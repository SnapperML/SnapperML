import os
import subprocess
from pathlib import Path
import tempfile
from typing import *
from dotenv import find_dotenv, load_dotenv
import docker
import typer
import click
from pydantic import ValidationError
import pystache

from snapper_ml.config import parse_config, get_validation_model, SUPPORTED_EXTENSIONS
from snapper_ml.config.models import DockerConfig, JobConfig, ExperimentConfig, \
    GroupConfig, JobTypes, PrunerEnum, SamplerEnum, OptimizationDirection, Metric, Run
from snapper_ml.logging import logger, setup_logging
from snapper_ml.utils import recursive_map


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


def build_image(client: docker.APIClient, context: Path, dockerfile: Path, build_args: dict):
    if not context:
        build_params = {'path': str(dockerfile.parent.absolute()), 'dockerfile': dockerfile.name}
    else:
        build_params = {'path': str(context.absolute()), 'fileobj': dockerfile.open('rb')}
    logs = client.build(rm=True, buildargs=build_args, decode=True, **build_params)
    logs_str = []
    for log in logs:
        chunk = extract_string_from_docker_log(log)
        logs_str.extend(chunk)
        for line in chunk:
            logger.info(line)
    return logs_str[-1].strip().split(' ')[-1]


def run_docker_container(image: str, command, env={}):
    client = docker.from_env()
    container = client.containers.run(
        image,
        ['-c', command],
        auto_remove=True,
        entrypoint='sh',
        volumes={os.getcwd(): {'bind': '/mnt/', 'mode': 'rw'}},
        working_dir='/mnt/',
        detach=True,
        environment=env
    )
    logs = container.attach(stdout=True, stderr=True, stream=True, logs=True)
    for chunk in logs:
        logger.info(chunk.decode('utf-8'))
    logger.info('Finished job!')


def process_docker(config: DockerConfig, command: Union[List[str], str], env={}):
    client = create_low_level_docker_client()
    commands = command if isinstance(command, list) else [command]
    command_single_expression = " && ".join(commands)
    image = config.image
    if config.dockerfile:
        logger.info('Building docker image...')
        image = build_image(client, config.context, config.dockerfile, config.args)
    if image:
        logger.info('Running job on docker container...')
        run_docker_container(image, command_single_expression, env)


def run_job(job: JobConfig, config_file: str, env: Dict):
    run_commands: List[Run] = job.run if isinstance(job.run, list) else [job.run]

    if isinstance(job, ExperimentConfig) or isinstance(job, GroupConfig):
        bash_commands = [f'python3 {cmd.command} {config_file}' for cmd in run_commands]
    else:
        bash_commands = [pystache.render(cmd.command, job.params) if cmd.template else cmd.command
                         for cmd in run_commands]

    if job.docker_config:
        process_docker(job.docker_config, bash_commands, env)
    else:
        for commands in bash_commands:
            subprocess.run(commands, shell=True, env={**os.environ, **env})


def validate_dict(value: str) -> dict:
    value = value.strip()
    if not value:
        return {}
    try:
        return dict(item.strip().split("=") for item in value.split(";"))
    except Exception:
        raise typer.BadParameter(
            'It should be semicolon-separated list of field=value pairs, e.g. "date=0; amount=1"')


def validate_file_or_dict(value: Union[dict, str]) -> dict:
    if isinstance(value, dict):
        return value
    try:
        if os.path.isfile(value):
            return parse_config(value)
        else:
            return validate_dict(value)
    except Exception:
        raise typer.BadParameter('It should be dictionary of the form "k1=v1; k2=v2" or an existent YAML or JSON file')


def validate_existent_file(value: Union[List[Path], Path], extensions: Union[str, List[str]] = '.py'):
    if not value:
        return value

    is_singleton = not isinstance(value, list)
    extensions = [extensions] if isinstance(extensions, str) else extensions

    if is_singleton:
        value = [value]

    current_dir = Path('.').absolute()
    for file in value:
        if extensions and file.suffix not in extensions:
            raise typer.BadParameter(f'File should have one of the following extensions: {",".join(extensions)}')
        if current_dir not in list(file.parents):
            raise typer.BadParameter('Running scripts from outside the working directory is not supported.')

    return value[0] if is_singleton else value


app = typer.Typer()

ExistentFile = lambda extension, *args, **kwargs: typer.Argument(
    *args,
    callback=lambda value: validate_existent_file(value, extension),
    exists=True,
    file_okay=True,
    dir_okay=False,
    writable=False,
    readable=True,
    resolve_path=True,
    **kwargs
)

ExistentFileOption = lambda extension, *args, **kwargs: typer.Option(
    *args,
    callback=lambda value: validate_existent_file(value, extension),
    exists=True,
    file_okay=True,
    dir_okay=False,
    writable=False,
    readable=True,
    resolve_path=True,
    **kwargs
)

ExistentDir = lambda *args, **kwargs: typer.Option(
    *args,
    **kwargs,
    exists=True,
    file_okay=False,
    dir_okay=True,
    readable=True,
    resolve_path=True,
)

FileOrDict = lambda *args, **kwargs: typer.Option(
    *args,
    callback=validate_file_or_dict,
    metavar="FILE | DICT",
    **kwargs
)

tracking_uri = None

CLI_HELP = """
ml-experiment CLI allows you to execute jobs from a configuration file.
It can also be used to run a job on-the-fly by specifying the arguments in-place.
And ultimately, it can be used to execute jobs combining input arguments with
a configuration file, so config files can used as templates.
""".replace('\n', ' ')

OVERRIDE_CONFIG = 'Overrides the config file field if specified.'
ONLY_GROUP = 'Only applies for groups of experiments.'
DICT_OVERLAP = 'In case of overlap, the values of this dictionary will take precedence over the rest'

NAME_HELP = f'Name of the job. {OVERRIDE_CONFIG}'
PARAMS_HELP = f'Job parameters. If config file is specified, these parameters {DICT_OVERLAP}'
KIND_HELP = f'Type of job. {OVERRIDE_CONFIG}'
PARAM_SPACE_HELP = f'Job parameter space. {ONLY_GROUP} {DICT_OVERLAP}'
NUM_TRIALS_HELP = f'Number of experiments to execute in parallel. {ONLY_GROUP} {OVERRIDE_CONFIG}'
TIMEOUT_HELP = 'Timeout per trial. In case of an experiment taking too long, it will be aborted.' \
               f'{ONLY_GROUP} {OVERRIDE_CONFIG}'
SAMPLER_HELP = f'Sampler name. {ONLY_GROUP} {OVERRIDE_CONFIG}'
PRUNER_HELP = f'Pruner name. {ONLY_GROUP} {OVERRIDE_CONFIG}'
METRIC_KEY_HELP = 'Name of the metric to optimize. It must be one of the keys of the metrics dictionary ' \
                  f'returned by the main function. {ONLY_GROUP} {OVERRIDE_CONFIG}'
METRIC_DIRECTION_HELP = 'Whether Hyperparameter Optimization Engine should minimize or maximize the given metric. ' \
                        f'{ONLY_GROUP} {OVERRIDE_CONFIG}'
DOCKER_IMAGE_HELP = 'If specified, the job will be run inside a docker contained based on the given image'
DOCKER_CONTEXT_HELP = 'A directory to use as a docker context.' \
                      f'Only applies when dockerfile is specified. {OVERRIDE_CONFIG}'
DOCKER_ARGS_HELP = 'A dictionary of build arguments. Only applies when the Dockerfile is specified.'
RAY_CONFIG_HELP = 'A dictionary of arguments to pass to Ray.init.' \
                  f'Here you can specify the cluster address, number of cpu, gpu, etc. {DICT_OVERLAP}'


# TODO: Add .py extension restriction when params/params_space is used.
@app.command(help=CLI_HELP)
def run(scripts: List[Path] = ExistentFile('.py', None),
        config_file: Path = ExistentFileOption(SUPPORTED_EXTENSIONS, None, '--config_file'),
        name: str = typer.Option(None, help=NAME_HELP),
        kind: JobTypes = typer.Option(None, help=KIND_HELP),
        env: str = FileOrDict({}),
        params: str = FileOrDict({}, help=PARAMS_HELP),
        param_space: str = FileOrDict({}, '--param_space', help=PARAM_SPACE_HELP),
        num_trials: int = typer.Option(None, '--num_trials', min=0, metavar='POSITIVE_INT', help=NUM_TRIALS_HELP),
        timeout_per_trial: float = typer.Option(None, '--timeout_per_trial', min=0,
                                                metavar='POSITIVE_FLOAT', help=TIMEOUT_HELP),
        sampler: SamplerEnum = typer.Option(None, help=SAMPLER_HELP),
        pruner: PrunerEnum = typer.Option(None, help=PRUNER_HELP),
        metric_key: str = typer.Option(None, '--metric_key', help=METRIC_KEY_HELP),
        metric_direction: OptimizationDirection = typer.Option(None, '--metric_direction', help=METRIC_DIRECTION_HELP),
        docker_image: str = typer.Option(None, '--docker_image', help=DOCKER_IMAGE_HELP),
        dockerfile: Path = ExistentFileOption(None, None),
        docker_context: Path = ExistentDir(None, '--docker_context', help=DOCKER_CONTEXT_HELP),
        docker_build_args: str = FileOrDict({}, '--docker_build_args', help=DOCKER_ARGS_HELP),
        ray_config: str = FileOrDict({}, '--ray_config', help=RAY_CONFIG_HELP)):
    load_dotenv(find_dotenv())

    if not scripts and not config_file:
        ctx = click.get_current_context()
        click.echo(ctx.get_help())
        ctx.exit()

    if config_file:
        # TODO: Fix parse when file does not exist
        config = parse_config(config_file, get_validation_model)
        kind = kind or config.kind
        name = name or config.name
        scripts = scripts or config.run
        params = {**config.params, **params}

        if config.ray_config:
            ray_config = {**config.ray_config.dict(), **ray_config}

        if config.docker_config:
            docker_image = docker_image or config.docker_config.dockerfile
            dockerfile = dockerfile or config.docker_config.dockerfile
            docker_context = docker_context or config.docker_config.context
            docker_build_args = {**docker_build_args, **config.docker_config.args}

        config = config.dict(exclude_defaults=True)
    else:
        config = {}

    metric = Metric(name=metric_key, metric_direction=metric_direction) if metric_key else None

    # Job type inference based on input parameters
    kind = JobTypes.GROUP if param_space else kind

    job_config = {
        'params': params,
        'name': name,
        'ray_config': ray_config,
        'run': scripts
    }

    job_config = {k: v for k, v in job_config.items() if v}

    if docker_image or dockerfile:
        job_config['docker_config'] = {
            'image': docker_image,
            'dockerfile': dockerfile,
            'context': docker_context,
            'args': docker_build_args
        }

    try:
        if kind == JobTypes.GROUP:
            group_config = dict(sampler=sampler,
                                pruner=pruner,
                                num_trials=num_trials,
                                timeout_per_trial=timeout_per_trial,
                                metric=metric,
                                param_space=param_space)
            group_config = {k: v for k, v in group_config.items() if v}
            group_config = {**job_config, **config, **group_config}
            result = GroupConfig.parse_obj(group_config)
        elif kind == JobTypes.EXPERIMENT:
            result = ExperimentConfig(**job_config)
        else:
            result = JobConfig(**job_config)
    except ValidationError as e:
        print(e)
        raise typer.Exit()

    setup_logging(experiment_name=result.name)

    # Avoid raising non-serializable errors
    if isinstance(result, GroupConfig):
        result.param_space = recursive_map(
            lambda x: str(x) if isinstance(x, Callable) else x, result.param_space)

    fp = tempfile.NamedTemporaryFile(mode='w+', suffix='.json')
    file_content = result.json(exclude_defaults=False)
    fp.write(file_content)
    fp.flush()
    os.fsync(fp.fileno())
    run_job(result, fp.name, env)
    fp.close()

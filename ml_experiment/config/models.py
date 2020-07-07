import os
from enum import Enum
from inspect import getfullargspec
from typing import *
from pydantic import BaseModel, PositiveFloat, DirectoryPath, \
    root_validator, PositiveInt, validator, FilePath, create_model, BaseConfig
from ..optuna import SAMPLERS, PRUNERS
from ..optuna.types import ParamDistributionBase, ParamDistribution


class JobTypes(Enum):
    JOB = "job"
    EXPERIMENT = "experiment"
    GROUP = "group"


class RayConfig(BaseModel):
    address: Optional[str]

    @validator('address', pre=True)
    def convert_localhost(cls, v: str):
        if v:
            v_striped = v.strip()
            return '' if v_striped == 'localhost' else v_striped
        return v

    class Config:
        extra = 'allow'


class OptimizationDirection(Enum):
    MINIMIZE = 'minimize'
    MAXIMIZE = 'maximize'


class Metric(BaseModel):
    name: str
    direction: OptimizationDirection = OptimizationDirection.MINIMIZE


class WorkerResourcesConfig(BaseModel):
    cpu: PositiveFloat = 1.0
    gpu: float = 0.0


class DockerConfig(BaseModel):
    dockerfile: Optional[FilePath]
    image: Optional[str]
    context: Optional[DirectoryPath] = None
    args: Dict = {}

    @root_validator()
    def check_dockerfile_and_image(cls, values):
        if values.get('image') and values.get('dockerfile'):
            raise ValueError('image and dockerfile fields cannot be used simultaneously. Use one of them.')
        return values


class Run(BaseModel):
    command: Union[FilePath, str]
    template: bool = False


class GoogleCloudConfig(BaseModel):
    credentials_keyfile: FilePath = None
    job_spec: dict
    project_id: str = os.getenv('GOOGLE_CLOUD_PROJECT_ID')


class JobConfig(BaseModel):
    name: str
    kind: JobTypes = JobTypes.JOB
    run: List[Run]
    docker_config: Optional[DockerConfig]
    params: dict = {}
    ray_config: Optional[RayConfig]

    @root_validator()
    def check_docker_and_ray(cls, values):
        if values.get('docker_config') and values.get('ray_config'):
            raise ValueError('Executing on Docker and Ray are incompatible. Please, select just one way.')
        return values

    """
    @root_validator()
    def check_run_commands(cls, values):
        for cmd in values['run']:
            command = cmd.command
            if values['kind'] in [JobTypes.GROUP, JobTypes.EXPERIMENT]:
                if isinstance(command, str) or not command.exists():
                    raise ValueError('Script does not exists')
                elif command.suffix() != '.py':
                    raise ValueError('Script should be a python file when running an experiment or a group')
        return values
    """

    @validator('run', pre=True)
    def convert_to_run(cls, value):
        if isinstance(value, str) or isinstance(value, FilePath):
            return [Run(command=value)]
        if isinstance(value, List):
            return [x for v in value for x in cls.convert_to_run(v)]
        elif isinstance(value, Run):
            return [value]
        elif isinstance(value, Dict):
            return [Run(**value)]
        else:
            raise ValueError()

    class Config:
        extra = 'forbid'


PrunerEnum = Enum('PrunerEnum', zip(PRUNERS.keys(), PRUNERS.keys()), module=__name__)
SamplerEnum = Enum('SamplerEnum', zip(SAMPLERS.keys(), SAMPLERS.keys()), module=__name__)


class GroupConfig(JobConfig):
    kind = JobTypes.GROUP
    sampler: Optional[SamplerEnum]
    pruner: Optional[PrunerEnum]
    num_trials: PositiveInt
    resources_per_worker: WorkerResourcesConfig = WorkerResourcesConfig()
    # TODO: Improve by adding dict of classes
    timeout_per_trial: Optional[PositiveFloat]
    param_space: Dict[str, Union[ParamDistribution, List[ParamDistribution]]]
    metric: Optional[Metric]


class ExperimentConfig(JobConfig):
    kind = JobTypes.EXPERIMENT


def create_model_from_signature(func: Callable,
                                model_name: str,
                                allow_factory_types: bool = False):
    args, _, varkw, defaults, kwonlyargs, kwonlydefaults, annotations = getfullargspec(func)
    defaults = defaults or []
    args = args or []

    non_default_args = len(args) - len(defaults)
    defaults = (...,) * non_default_args + defaults

    params = dict(zip(args, defaults))
    kwonlyparams = {param: kwonlydefaults.get(param, ...) for param in kwonlyargs}
    all_params = {**params, **kwonlyparams}
    model_params = {}

    for param, default in all_params.items():
        annotation = annotations.get(param, Any)

        if allow_factory_types:
            annotation_args = getattr(annotation, '__args__', None)
            # If annotation is a wrapper type
            if annotation_args and len(annotation_args) == 1:
                # Replace  T[X] -> T[ParamDistribution[X]]
                required_distribution = ParamDistributionBase[annotation_args[0]]
                wrapper_annotation = annotation.copy_with((required_distribution,))
                annotation = Union[annotation, wrapper_annotation]
            elif annotation in [list, tuple]:
                annotation = Union[annotation, List[ParamDistributionBase[Any]], ParamDistributionBase[List]]
            annotation = Union[annotation, ParamDistributionBase[annotation]]

        model_params[param] = (annotation, default)

    class Config(BaseConfig):
        # Allow extra params if there is a **kwargs parameter in the function signature
        extra = 'allow' if varkw else 'forbid'

    return create_model(model_name, **model_params, __config__=Config)


def replace_model_field(__new_model_name__: str = None, __base_model__: Type[BaseModel] = BaseModel, **kwargs):
    return create_model(__new_model_name__ or __base_model__.__name__, **kwargs, __base__=__base_model__)

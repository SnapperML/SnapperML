import os
from enum import Enum
from inspect import getfullargspec
from typing import *
from pydantic import BaseModel, PositiveFloat, DirectoryPath, \
    root_validator, PositiveInt, validator, FilePath, create_model
from ..optuna import SAMPLERS, PRUNERS
from ..optuna.types import ParamDistribution


class JobTypes(Enum):
    JOB = "job"
    EXPERIMENT = "experiment"
    GROUP = "group"


class RayConfig(BaseModel):
    address: Optional[str]

    @validator('address', pre=True)
    def convert_localhost(cls, v: str):
        v_striped = v.strip()
        return '' if v_striped == 'localhost' else v_striped

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
    gpu: PositiveFloat = 0.0


class DockerConfig(BaseModel):
    dockerfile: Optional[str]
    image: Optional[str]
    context: Optional[DirectoryPath] = None
    args: dict = {}

    @root_validator()
    def check_dockerfile_and_image(cls, values):
        if values.get('image') and values.get('dockerfile'):
            raise ValueError('image and dockerfile fields cannot be used simultaneously. Use one of them.')
        return values


class GoogleCloudConfig(BaseModel):
    credentials_keyfile: FilePath = None
    job_spec: dict
    project_id: str = os.getenv('GOOGLE_CLOUD_PROJECT_ID')


class JobConfig(BaseModel):
    # TODO: Improve by adding restrictions according signature
    kind: JobTypes = JobTypes.JOB
    name: str
    run: Union[str, List[str]]
    docker_config: Optional[DockerConfig]
    params: dict = {}
    ray_config: Optional[RayConfig] = RayConfig()

    # google_cloud_config: Optional[GoogleCloudConfig]

    @root_validator()
    def check_docker_and_ray(cls, values):
        if values.get('docker_config') and values.get('ray_config'):
            raise ValueError('Executing on Docker and Ray are incompatible. Please, select just one way.')
        return values

    class Config:
        extra = 'forbid'


class GroupConfig(JobConfig):
    kind = JobTypes.JOB
    sampler: Optional[str]
    pruner: Optional[str]
    num_trials: PositiveInt
    resources_per_worker: WorkerResourcesConfig = WorkerResourcesConfig()
    # TODO: Improve by adding dict of classes
    timeout_per_trial: Optional[PositiveFloat]
    param_space: Dict[str, Union[ParamDistribution, List[ParamDistribution]]]
    metric: Optional[Metric]

    @validator('sampler')
    def sampler_must_exist(cls, value):
        if value not in SAMPLERS:
            raise ValueError(f'Sampler must be one of the following: {list(SAMPLERS.keys())}')
        return value

    @validator('pruner')
    def pruner_must_exist(cls, value):
        if value not in PRUNERS:
            raise ValueError(f'Pruner must be one of the following: {list(PRUNERS.keys())}')
        return value


class ExperimentConfig(JobConfig):
    kind = JobTypes.EXPERIMENT


def create_model_from_signature(func: Callable,
                                model_name: str,
                                base_model: Type[BaseModel] = BaseModel):
    args, _, varkw, defaults, kwonlyargs, kwonlydefaults, annotations = getfullargspec(func)
    defaults = defaults or []
    args = args or []

    non_default_args = len(args) - len(defaults)
    defaults = (...,) * non_default_args + defaults

    keyword_only_params = {param: kwonlydefaults.get(param, Any) for param in kwonlyargs}
    params = {param: (annotations.get(param, Any), default) for param, default in zip(args, defaults)}

    class Config:
        extra = 'allow'

    # Allow extra params if there is a **kwargs parameter in the function signature
    config = Config if varkw else None

    return create_model(
        model_name,
        **params,
        **keyword_only_params,
        __base__=base_model,
        __config__=config,
    )


def replace_model_field(__new_model_name__: str = None, __base_model__: Type[BaseModel] = BaseModel, **kwargs):
    return create_model(__new_model_name__ or __base_model__.__name__, **kwargs, __base__=__base_model__)

import os
from enum import Enum
from typing import *
from pydantic import field_validator, model_validator, field_serializer, ConfigDict, BaseModel, PositiveFloat, DirectoryPath, \
    PositiveInt, FilePath, AnyUrl, FieldValidationInfo
from ..optuna import SAMPLERS, PRUNERS
from ..optuna.types import ParamDistribution
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MLFLOW_TRACKING_URI: str
    OPTUNA_STORAGE_URI: Optional[str]

class JobTypes(Enum):
    JOB = "job"
    EXPERIMENT = "experiment"
    GROUP = "group"


class RayConfig(BaseModel):
    address: Optional[str] = None
    num_cpus: Optional[PositiveInt] = None
    num_gpus: Optional[PositiveInt] = None

    @field_validator('address', mode="before")
    @classmethod
    def convert_localhost(cls, v: str):
        if v:
            v_striped = v.strip()
            return '' if v_striped == 'localhost' else v_striped
        return v
    model_config = SettingsConfigDict(extra='allow')


class OptimizationDirection(Enum):
    MINIMIZE = 'minimize'
    MAXIMIZE = 'maximize'


class Metric(BaseModel):
    name: str
    direction: OptimizationDirection = OptimizationDirection.MINIMIZE
    model_config = ConfigDict(extra='forbid')

class Data(BaseModel):
    folder: Optional[str] = ''
    files: List[str]

class WorkerResourcesConfig(BaseModel):
    cpu: PositiveFloat = 1.0
    gpu: float = 0.0
    model_config = ConfigDict(extra='forbid')


class DockerConfig(BaseModel):
    dockerfile: Optional[FilePath] = None
    image: Optional[str] = None
    context: Optional[DirectoryPath] = None
    args: Dict = {}

    @model_validator(mode='before')
    @classmethod
    def check_dockerfile_and_image(cls, values):
        if values.get('image') and values.get('dockerfile'):
            raise ValueError('image and dockerfile fields cannot be used simultaneously. Use one of them.')
        return values
    model_config = ConfigDict(extra='forbid')


class Run(BaseModel):
    command: Union[FilePath, str]
    template: bool = False
    model_config = ConfigDict(extra='forbid')


class GoogleCloudConfig(BaseModel):
    credentials_keyfile: FilePath = None
    job_spec: dict
    project_id: str = os.getenv('GOOGLE_CLOUD_PROJECT_ID')
    model_config = ConfigDict(extra='forbid')


class JobConfig(BaseModel):
    name: str
    kind: JobTypes = JobTypes.JOB
    run: List[Run]
    data: Data = None
    docker_config: Optional[DockerConfig] = None
    params: dict = {}
    ray_config: Optional[RayConfig] = None

    @model_validator(mode='before')
    @classmethod
    def check_docker_and_ray(cls, values):
        if values.get('docker_config') in values and values.get('ray_config'):
            raise ValueError('Executing on Docker and Ray are incompatible. Please, select just one way.')
        return values

    @model_validator(mode='before')
    @classmethod
    def check_ray_for_jobs(cls, values):
        if 'ray_config' in values and values['kind'] == JobTypes.JOB:
            raise ValueError('Ray as an execution environment is only supported for experiments and groups.')
        return values

    @field_validator('run', mode='before')
    def check_run_commands(cls, value: List[Run], info: FieldValidationInfo):
        kind = info.data.get('kind')

        for cmd in value:
            command = cmd.command

            if kind in [JobTypes.GROUP, JobTypes.EXPERIMENT]:
                if not isinstance(command, str) or not os.path.exists(command):
                    raise ValueError('Script does not exist')
            
            # Check for .py suffix if the kind is GROUP or EXPERIMENT
            if kind in [JobTypes.GROUP, JobTypes.EXPERIMENT] and not command.endswith('.py'):
                raise ValueError('Script should be a Python file when running an experiment or a group')

        return value

    @field_validator('run', mode="before")
    @classmethod
    def convert_to_run(cls, value):
        if isinstance(value, list):
            return [x for v in value for x in cls.convert_to_run(v)]
        elif isinstance(value, dict) and 'command' in value:
            return [Run(command=value['command'])]
        elif isinstance(value, (str, FilePath)):
            return [Run(command=value)]
        elif isinstance(value, Run):
            return [value]
        elif isinstance(value, dict):
            return [Run(**value)]
        else:
            raise ValueError()
    model_config = ConfigDict(extra='forbid')


PrunerEnum = Enum('PrunerEnum', zip(PRUNERS.keys(), PRUNERS.keys()), module=__name__)
SamplerEnum = Enum('SamplerEnum', zip(SAMPLERS.keys(), SAMPLERS.keys()), module=__name__)


class GroupConfig(JobConfig):
    kind: JobTypes = JobTypes.GROUP
    sampler: Optional[SamplerEnum] = None
    pruner: Optional[PrunerEnum] = None
    num_trials: PositiveInt
    resources_per_worker: WorkerResourcesConfig = WorkerResourcesConfig()
    timeout_per_trial: Optional[PositiveFloat] = None
    param_space: Dict[str, Union[ParamDistribution, List[ParamDistribution]]]
    metric: Optional[Metric] = None

    @field_serializer('param_space')
    def serialize(self, paramDistribution : str):
        return paramDistribution


class ExperimentConfig(JobConfig):
    kind: JobTypes = JobTypes.EXPERIMENT

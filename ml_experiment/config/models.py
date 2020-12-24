import os
from enum import Enum
from typing import *
from pydantic import BaseModel, PositiveFloat, DirectoryPath, \
    root_validator, PositiveInt, validator, FilePath, BaseSettings, AnyUrl
from ..optuna import SAMPLERS, PRUNERS
from ..optuna.types import ParamDistribution


class Settings(BaseSettings):
    MLFLOW_TRACKING_URI: AnyUrl
    OPTUNA_STORAGE_URI: Optional[str]


class JobTypes(Enum):
    JOB = "job"
    EXPERIMENT = "experiment"
    GROUP = "group"


class RayConfig(BaseModel):
    address: Optional[str]
    num_cpus: Optional[PositiveInt]
    num_gpus: Optional[PositiveInt]

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

    @root_validator()
    def check_ray_for_jobs(cls, values):
        if values.get('ray_config') and values['kind'] == JobTypes.JOB:
            raise ValueError('Ray as an execution environment is only supported for experiments and groups.')
        return values

    @root_validator()
    def check_run_commands(cls, values):
        for cmd in values['run']:
            command = cmd.command
            if values['kind'] in [JobTypes.GROUP, JobTypes.EXPERIMENT]:
                if isinstance(command, str) or not command.exists():
                    raise ValueError('Script does not exists')
                elif command.suffix != '.py':
                    raise ValueError('Script should be a python file when running an experiment or a group')
        return values

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
    timeout_per_trial: Optional[PositiveFloat]
    param_space: Dict[str, Union[ParamDistribution, List[ParamDistribution]]]
    metric: Optional[Metric]


class ExperimentConfig(JobConfig):
    kind = JobTypes.EXPERIMENT

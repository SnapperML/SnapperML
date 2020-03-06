from enum import Enum
from typing import Optional, Union, List, Dict
from pydantic import BaseModel, PositiveFloat, DirectoryPath, root_validator, PositiveInt, validator
from src.utils.optuna import SAMPLERS, PRUNERS
from src.utils.optuna.types import Choice, Range, RandomInt, Uniform, LogUniform


class JobTypes(Enum):
    JOB = "job"
    EXPERIMENT = "experiment"
    GROUP = "group"


class TrialResourcesConfig(BaseModel):
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
    resources_per_trial: TrialResourcesConfig = TrialResourcesConfig()
    # Improve by adding dict of classes
    timeout_per_trial: Optional[PositiveFloat]
    param_space: Dict[str, Union[Choice, Range, RandomInt, Uniform, LogUniform]]

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
    # TODO: Improve by adding experiment signature
    params: dict = {}

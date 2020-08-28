import os
import optuna
from typing import *
from .types import ParamDistribution

if TYPE_CHECKING:
    from ..config.models import GroupConfig

PRUNERS = {
    'hyperband': optuna.pruners.HyperbandPruner,
    'sha': optuna.pruners.SuccessiveHalvingPruner,
    'percentile': optuna.pruners.PercentilePruner,
    'median': optuna.pruners.MedianPruner,
}

SAMPLERS = {
    'random': optuna.samplers.RandomSampler,
    'tpe': optuna.samplers.TPESampler,
    'skopt': optuna.integration.SkoptSampler
}


def _get_storage_uri() -> str:
    # TODO: Make this generic for any relational DB
    user = os.getenv('POSTGRES_USER')
    password = os.getenv('POSTGRES_PASSWORD')
    db = os.getenv('POSTGRES_DB')
    port = os.getenv('POSTGRES_PORT', 5432)
    host = os.getenv('POSTGRES_HOST', 'localhost')
    return f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}'


def _delete_optuna_study(study_name):
    try:
        optuna.delete_study(study_name, _get_storage_uri())
    except Exception:
        pass


def optimize_optuna_study(study: optuna.Study,
                          objective: Callable[[optuna.Trial], float],
                          group_config: 'GroupConfig') -> optuna.Study:
    optuna.logging.enable_propagation()
    optuna.logging.disable_default_handler()
    study.optimize(objective,
                   n_trials=group_config.num_trials,
                   timeout=group_config.timeout_per_trial)
    return study


def create_optuna_study(group_config: 'GroupConfig') -> optuna.Study:
    optuna.logging.enable_propagation()
    optuna.logging.disable_default_handler()
    pruner = group_config.pruner and PRUNERS.get(group_config.pruner.value)()
    sampler = group_config.sampler and SAMPLERS.get(group_config.sampler.value)()
    _delete_optuna_study(study_name=group_config.name)
    study = optuna.create_study(study_name=group_config.name,
                                sampler=sampler,
                                storage=_get_storage_uri(),
                                direction=group_config.metric.direction.value,
                                load_if_exists=True,
                                pruner=pruner)
    return study


def sample_params_from_distributions(trial: optuna.Trial,
                                     distributions: Dict[str, Union[ParamDistribution, List[ParamDistribution]]]):
    params = {}

    for k, distribution in distributions.items():
        if isinstance(distribution, list):
            params[k] = [d(f'{k}_{i}', trial) for i, d in enumerate(distribution)]
        else:
            params[k] = distribution(k, trial)

    return params

import os
import mlflow
import optuna
from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from src.utils.config.models import Metric, GroupConfig

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


def create_mlflow_callback(metric):
    def callback(_, trial):
        trial_value = trial.value if trial.value is not None else float('nan')
        mlflow.log_params(trial.params)
        mlflow.log_metrics({metric: trial_value})
    return callback


def _get_storage_uri():
    user = os.getenv('POSTGRES_USER')
    password = os.getenv('POSTGRES_PASSWORD')
    db = os.getenv('POSTGRES_DB')
    port = os.getenv('POSTGRES_PORT', 5432)
    host = os.getenv('POSTGRES_HOST', 'localhost')
    return f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}'


def create_optuna_study(objective: Callable[[optuna.Trial], float],
                        group_config: 'GroupConfig',
                        metric: 'Metric',
                        add_mlflow_callback=True):
    optuna.logging.enable_propagation()
    optuna.logging.disable_default_handler()
    pruner = group_config.pruner and PRUNERS.get(group_config.pruner)()
    sampler = group_config.sampler and SAMPLERS.get(group_config.sampler)()
    study = optuna.create_study(study_name=group_config.name,
                                sampler=sampler,
                                storage=_get_storage_uri(),
                                direction=metric.direction.value,
                                load_if_exists=True,
                                pruner=pruner)
    callbacks = [create_mlflow_callback(metric.name)] if add_mlflow_callback else []
    study.optimize(objective,
                   n_trials=group_config.num_trials,
                   timeout=group_config.timeout_per_trial,
                   callbacks=callbacks)
    return {'Best value': study.best_value, **study.best_params}

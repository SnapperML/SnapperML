import mlflow
import optuna
from typing import Callable
from src.utils.config.models import GroupConfig

PRUNERS = {
    'hyperband': optuna.pruners.HyperbandPruner,
    'sha': optuna.pruners.SuccessiveHalvingPruner,
    'percentile': optuna.pruners.PercentilePruner,
    'median': optuna.pruners.MedianPruner,
}
SAMPLERS = {
    'random': optuna.samplers.RandomSampler,
    'tpe': optuna.samplers.TPESampler,
}


def mlflow_callback(_, trial):
    trial_value = trial.value if trial.value is not None else float('nan')
    mlflow.log_params(trial.params)
    mlflow.log_metrics({'Optuna trial value': trial_value})


def create_optuna_study(objective: Callable[[optuna.Trial], float], group_config: GroupConfig):
    study = optuna.create_study(study_name=group_config.name,
                                sampler=SAMPLERS.get(group_config.sampler)(),
                                pruner=PRUNERS.get(group_config.pruner)())
    study.optimize(objective, n_trials=group_config.num_trials, callbacks=[mlflow_callback])
    return {'Best value': study.best_value, **study.best_params}

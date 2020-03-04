import mlflow
import optuna


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


def create_optuna_study(experiment_name, objective, **kwargs):
    study = optuna.create_study(study_name=experiment_name, **kwargs)
    study.optimize(objective, n_trials=100, callbacks=[mlflow_callback])
    return {'Best value': study.best_value, **study.best_params}

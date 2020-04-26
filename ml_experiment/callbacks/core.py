from dataclasses import dataclass
from typing import Optional, Dict, Any, List
from ml_experiment.config import JobConfig
from optuna import Trial


class Callback:
    def on_job_start(self, config: JobConfig, **kwargs):
        pass

    def on_job_end(self, config: JobConfig, exception: Optional[Exception]):
        pass

    def on_trial_start(self, config: JobConfig, trial: Trial, sampled_params: dict):
        pass

    def on_trial_end(self, config: JobConfig,
                     trial: Trial,
                     metric: Optional[float],
                     exception: Optional[Exception]):
        pass

    def on_info_logged(self, config: JobConfig,
                       metrics: Dict[str, Any],
                       artifacts: Dict[Dict, Any],
                       **kwargs):
        pass


@dataclass
class CallbacksHandler:
    callbacks: List[Callback]
    config: JobConfig

    def on_job_start(self, *args, **kwargs):
        for callback in self.callbacks:
            kwargs['config'] = self.config
            callback.on_job_start(*args, **kwargs)

    def on_job_end(self, *args, **kwargs):
        for callback in self.callbacks:
            kwargs['config'] = self.config
            callback.on_job_end(*args, **kwargs)

    def on_trial_start(self, *args, **kwargs):
        for callback in self.callbacks:
            kwargs['config'] = self.config
            callback.on_trial_start(*args, **kwargs)

    def on_trial_end(self, *args, **kwargs):
        for callback in self.callbacks:
            kwargs['config'] = self.config
            callback.on_trial_end(*args, **kwargs)

    def on_info_logged(self, *args, **kwargs):
        for callback in self.callbacks:
            kwargs['config'] = self.config
            callback.on_info_logged(*args, **kwargs)

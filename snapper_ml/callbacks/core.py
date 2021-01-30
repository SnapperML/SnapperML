from dataclasses import dataclass
from typing import Optional, Dict, Any, List
from snapper_ml.config import JobConfig
from optuna import Trial


class Callback:
    """
    Base class for callbacks that want to react to fired events.

    To create a new type of callback, you'll need to inherit from this class,
    and implement one or more methods as required for your purposes.
    Arguably the easiest way to get started is to look at the source code for
    some of the pre-defined ones.
    """

    def on_job_start(self, config: JobConfig, **kwargs):
        """
        This method will be execute once the experiment has started
        :param config: The configuration object contains all the information regarding
        how the experiment is executed
        """
        pass

    def on_job_end(self, config: JobConfig, exception: Optional[Exception]):
        """
        This method will be execute once the experiment has ended
        :param config: The configuration object contains all the information regarding
        how the experiment is executed
        :param exception: If not none, it means that the experiment has finished due to
        an error. This param contains that error.
        """
        pass

    def on_trial_start(self, config: JobConfig, trial: Trial, sampled_params: dict):
        """
        Only for groups of experiments.

        This method will be execute once a trial has been started.
        :param config: The configuration object contains all the information regarding
        how the experiment is executed
        :param trial: The object of the class optuna.Trial that correspond to this trial
        :param sampled_params: The randomly selected parameters
        """
        pass

    def on_trial_end(self, config: JobConfig,
                     trial: Trial,
                     metric: Optional[float],
                     exception: Optional[Exception]):
        """
        Only for groups of experiments.

        This method will be execute once a trial has been finished.
        :param config: The configuration object contains all the information regarding
        how the experiment is executed
        :param trial: The object of the class optuna.Trial that correspond to this trial
        :param metric: If everything when fine, it will contain the value of the optimization metric
        :param exception: If not none, it means that the trial has finished due to
        an error. This param contains that error.
        """
        pass

    def on_info_logged(self, config: JobConfig,
                       metrics: Dict[str, Any],
                       artifacts: Dict[Dict, Any],
                       **kwargs):
        """
        This method will be execute every time the metrics and artifacts are logged.
        It will be called at least one time for every experiment.

        :param config: The configuration object contains all the information regarding
               how the experiment is executed
        :param metrics: The metrics dictionary returned by the main function
        :param artifacts: The artifacts dictionary returned by the main function
        """
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

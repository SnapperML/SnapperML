from dataclasses import dataclass
from abc import ABCMeta, abstractmethod
from typing import *
from snapper_ml.config import JobConfig, GroupConfig
from optuna import Trial, Study
from datetime import datetime, timedelta
import pprint
from .core import Callback
from pytictoc import TicToc
import socket
import traceback
from knockknock.slack_sender import send_slack_message
from knockknock.email_sender import send_email, create_yag_sender
from knockknock.desktop_sender import show_desktop_notification
import sys
import telegram

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
PRETTY_PRINTER = pprint.PrettyPrinter(indent=2, width=60)


def create_job_start_message(config: JobConfig, start_time: datetime, run_id: Optional[str]) -> str:
    host_name = socket.gethostname()
    run_id_line = f'\nRun id: {run_id}' if run_id else ''

    contents = f"""
        Starting job {config.name} in {sys.argv[0]} 🎬 {run_id_line}
        Machine name: {host_name}
        Starting date: {start_time.strftime(DATE_FORMAT)}
        Parameters: {PRETTY_PRINTER.pformat(config.params)} 
    """

    if isinstance(config, GroupConfig):
        contents += f'\nHyperparameter space: {PRETTY_PRINTER.pformat(config.param_space)}'

    return contents.strip()


def create_job_finish_message(config: JobConfig,
                              exception: Optional[Exception],
                              finish_date: datetime,
                              study: Optional[Study],
                              duration_seconds: float) -> str:
    host_name = socket.gethostname()
    delta = timedelta(seconds=duration_seconds)
    crash_title = f'Crashed job - {config.name} ❌'
    finish_title = f'Finished job  - {config.name} 🎉'

    contents = f"""
        {crash_title if exception else finish_title}
        Machine name: {host_name}
        Finish date: {finish_date.strftime(DATE_FORMAT)}
        Duration: {delta}
    """

    if study:
        contents += f"""
            Best Trial: {study.best_trial.number}
            Best Params: {study.best_params}
        """

    if exception:
        contents += f'\nTraceback: {traceback.format_exc()}'

    return contents.strip()


def create_trial_start_message(config: JobConfig,
                               sampled_params: dict,
                               trial: Trial,
                               start_time: datetime):
    run_id = trial.user_attrs.get('mlflow_run_id')
    contents = f"""
        Starting trial {trial.number} for {config.name} 🎬
        Run id: {run_id}
        Starting date: {start_time.strftime(DATE_FORMAT)}
        Fixed parameters: {PRETTY_PRINTER.pformat(config.params)} 
        Sampled parameters: {PRETTY_PRINTER.pformat(sampled_params)} 
    """
    return contents.strip()


def create_trial_finish_message(config: JobConfig,
                                exception: Optional[Exception],
                                finish_date: datetime,
                                trial: Trial,
                                metric: Optional[float],
                                sampled_params: dict,
                                duration_seconds: float):
    delta = timedelta(seconds=duration_seconds)
    crash_title = f'Crashed trial {trial.number} for {config.name} ❌'
    finish_title = f'Finished trial {trial.number} for {config.name} 🎉'
    run_id = trial.user_attrs.get('mlflow_run_id')

    contents = f"""
        {crash_title if exception else finish_title}
        Run id: {run_id}
        
        Finish date: {finish_date.strftime(DATE_FORMAT)}
        Duration: {delta}
        Fixed parameters: {PRETTY_PRINTER.pformat(config.params)} 
        Sampled parameters: {PRETTY_PRINTER.pformat(sampled_params)} 
    """

    if exception:
        contents += f'\nTraceback: {traceback.format_exc()}'
    elif metric:
        contents += f'\nMetric: {metric}'

    return contents.strip()


class NotifierBase(Callback, metaclass=ABCMeta):
    """
    Base class for notifiers

    To create a new type of notifier, you'll need to inherit from this class, and implement one
    or more methods as required for your purposes. Specifically, the send_message method should be override.
    Arguably the easiest way to get started is to look at the source code for some of the pre-defined ones.
    """

    def __post_init__(self):
        self.job_timer: Optional[TicToc] = None
        self.trial_timers: Dict[int, TicToc] = {}
        self.sampled_params_dict: Dict[int, Dict] = {}
        self.run_id_dict: Dict[int, str] = {}
        self.study: Optional[Study] = None

    def on_job_start(self, config, **kwargs):
        self.job_timer = TicToc()
        self.job_timer.tic()
        run_id = kwargs.get('run_id')
        message = create_job_start_message(config, datetime.now(), run_id)
        self.send_message(message)

    def on_job_end(self, config, exception):
        message = create_job_finish_message(
            config=config,
            exception=exception,
            finish_date=datetime.now(),
            duration_seconds=self.job_timer.tocvalue(),
            study=self.study)
        self.send_message(message)

    def on_trial_start(self, config, trial, sampled_params, **kwargs):
        if not self.study:
            self.study = trial.study
        timer = TicToc()
        timer.tic()
        self.trial_timers[trial.number] = timer
        self.sampled_params_dict[trial.number] = sampled_params
        message = create_trial_start_message(config, sampled_params, trial, datetime.now())
        self.send_message(message)

    def on_trial_end(self, config, trial, metric, exception):
        duration = self.trial_timers[trial.number].tocvalue()
        sampled_params = self.sampled_params_dict[trial.number]
        message = create_trial_finish_message(config,
                                              exception=exception,
                                              sampled_params=sampled_params,
                                              trial=trial,
                                              metric=metric,
                                              finish_date=datetime.now(),
                                              duration_seconds=duration)
        self.send_message(message)

    @abstractmethod
    def send_message(self, msg: str) -> None:
        """
        This method should be override by your custom logic

        :param msg: The preprocessed messaged generated from the experiment information
        """
        pass


@dataclass
class TelegramNotifier(NotifierBase):
    """
    Callback that sends a message through a Telegram Bot.

    It requires a token and chat_id which can be get following
    these instructions: https://core.telegram.org/bots

    :param token: Telegram Bot Token.
    :param chat_id: Telegram group id. More info on how to get
                    this id `here <https://stackoverflow.com/questions/32423837/telegram-bot-how-to-get-a-group-chat-id>`_.
    """

    token: str
    chat_id: int

    def __post_init__(self):
        super().__post_init__()
        self.bot = telegram.Bot(self.token)

    def send_message(self, message: str):
        self.bot.send_message(self.chat_id, message)


@dataclass
class DesktopNotifier(NotifierBase):
    """
    Callback that sends a desktop notification when an event happens.

    It works out-of-the-box for Linux and OS X. For Windows it is necessary to install
    the `win10toast <https://pypi.org/project/win10toast/>`_ package.
    """
    def send_message(self, msg: str):
        subject = msg.split('\n')[0]
        show_desktop_notification(subject, msg)


@dataclass
class SlackNotifier(NotifierBase):
    """
    Callback that sends a message to an specific Slack channel when an event happens.

    It requires a webhook URL, in order to generate that URL you should follow
    these `instructions <https://pypi.org/project/win10toast/>`_

    :param webhook_url: Theb webhook generated from Slack Apps
    :param channel: Slack channel name
    :param username: The username that will appear on the slack messages
    """
    webhook_url: str
    channel: str
    username: str

    def send_message(self, msg: str, **kwargs):
        icon_emoji = ':x:' if 'exception' in kwargs else ':tada:'
        send_slack_message(self.webhook_url, self.channel, msg, self.username, icon_emoji=icon_emoji)


@dataclass
class EmailNotifier(NotifierBase):
    """
    Callback that sends a email to a recipient or list of recipients when an event happens.

    This service relies on `Yagmail <https://github.com/kootenpv/yagmail)>`_,
    so you'll need to setup a Gmail account and follow the library instructions.
    """
    sender_email: str
    recipient_emails: List[str]

    def __post_init__(self):
        super().__post_init__()
        self._yag_sender = create_yag_sender(self.recipient_emails, self.sender_email)

    def send_message(self, msg: str):
        subject = msg.split('\n')[0]
        return send_email(self._yag_sender, self.recipient_emails, subject, msg)

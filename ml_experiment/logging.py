"""
This module is for logging utility functions.
"""
import logging
import os
import coloredlogs


logger = logging.getLogger(__name__)


def setup_logging(experiment_name):
    global logger
    logger = logging.getLogger(__name__)
    logs_folder = os.environ.get('LOGS_FOLDER', './logs')
    if not os.path.exists(logs_folder):
        os.mkdir(logs_folder)
    info_handler = logging.FileHandler(os.path.join('logs', f'{experiment_name}.info.log'))
    error_handler = logging.FileHandler(os.path.join('logs', f'{experiment_name}.error.log'))
    console = logging.StreamHandler()

    simple_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    descriptive_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    info_handler.setLevel(logging.INFO)
    error_handler.setLevel(logging.ERROR)
    console.setLevel(logging.DEBUG)

    info_handler.setFormatter(logging.Formatter(descriptive_format))
    error_handler.setFormatter(logging.Formatter(descriptive_format))
    console.setFormatter(logging.Formatter(simple_format))

    logger.addHandler(info_handler)
    logger.addHandler(error_handler)
    logger.addHandler(console)

    coloredlogs.install(fmt=simple_format, level='DEBUG', logger=logger)

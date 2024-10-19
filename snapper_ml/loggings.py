import logging
import os
import sys
import coloredlogs

# Initialize logger at the module level
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, stream=sys.stdout, format='%(message)s')

def setup_logging(experiment_name):
    # Avoid re-adding handlers if they are already present
    if not logger.hasHandlers():
        logs_folder = os.environ.get('LOGS_FOLDER', './logs')

        # Create logs folder if it doesn't exist
        if not os.path.exists(logs_folder):
            os.mkdir(logs_folder)

        # File handlers for info and error logs
        info_handler = logging.FileHandler(os.path.join(logs_folder, f'{experiment_name}.info.log'))
        error_handler = logging.FileHandler(os.path.join(logs_folder, f'{experiment_name}.error.log'))

        # Console handler (for stdout streaming)
        console = logging.StreamHandler(sys.stdout)

        # Define logging formats
        file_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        console_format = '%(asctime)s - %(levelname)s - %(message)s'

        # Set levels for handlers
        info_handler.setLevel(logging.INFO)
        error_handler.setLevel(logging.ERROR)
        console.setLevel(logging.DEBUG)

        # Set formatting for handlers
        info_handler.setFormatter(logging.Formatter(file_format))
        error_handler.setFormatter(logging.Formatter(file_format))
        console.setFormatter(logging.Formatter(console_format))

        # Add handlers to the logger
        logger.addHandler(info_handler)
        logger.addHandler(error_handler)
        logger.addHandler(console)

        # Install coloredlogs for better console readability
        coloredlogs.install(fmt=console_format, level='DEBUG', logger=logger)

        # Ensure the logger propagates to root (to prevent duplicate logs)
        logger.propagate = False
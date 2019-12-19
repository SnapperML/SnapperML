from dotenv import find_dotenv, load_dotenv
from src.utils.cli import cli_decorator
from src.utils.config import parse_config
from src.utils.logging import logger, setup_logging
import subprocess


@cli_decorator
def main(config_file):
    load_dotenv(find_dotenv())
    config = parse_config(config_file)
    experiment_name = config["name"]
    setup_logging(experiment_name=experiment_name)
    logger.info(f"\nRunning experiment: {experiment_name}")

    run_command = config['run']
    run_command = run_command if isinstance(run_command, list) else [run_command]
    for command in run_command:
        subprocess.run(['python3', command, '--config_file', config_file])


if __name__ == '__main__':
    main()

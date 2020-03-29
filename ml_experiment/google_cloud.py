from googleapiclient import discovery
from googleapiclient import errors
from .config.models import JobConfig
from .logging import logger


def create_job_spec(job_name, config_filepath):
    training_inputs = {'packageUris': ['gs://my/trainer/path/package-0.0.0.tar.gz'],
                       'pythonModule': 'trainer.task',
                       'args': ['--config_file', config_filepath],
                       'jobDir': 'gs://my/training/job/directory',
                       'master-image-uri': '$IMAGE_URI',
                       'runtimeVersion': '1.14',
                       'pythonVersion': '3.5'}
    return {'jobId': job_name, 'trainingInput': training_inputs}


def upload_job_to_google_cloud_ai_platform(config_filepath: str, job_config: JobConfig):
    ml = discovery.build('ml', 'v1')
    project_id = f'projects/{job_config.google_cloud_config.project_id}'
    job_spec = create_job_spec(job_config.name, config_filepath)
    request = ml.projects().jobs().create(body=job_spec, parent=project_id)

    try:
        response = request.execute()
        logger.info(response)
    except errors.HttpError as err:
        logger.error('There was an error creating the training job. Check the details:')
        logger.error(err._get_reason())

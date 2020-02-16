import os
from . import root_helper, csv_helper
from .exceptions import DataLoaderNotInitialized

dataLoader = None

SUPPORTED_EXTENSIONS = ['.csv', '.root']


class DataLoader(object):
    _instance = None

    def __init__(self, file, batch_size=None, **kwargs):
        self._batch_size = batch_size
        _, file_extension = os.path.splitext(file)
        if file_extension == '.root':
            self.generator = root_helper.get_dataframe(file, batch_size=batch_size, **kwargs)
        if file_extension == '.csv':
            self.generator = csv_helper.get_dataframe(file, batch_size=batch_size, **kwargs)

    @property
    def batch_size(self):
        return self._batch_size

    @classmethod
    def initialize_instance(cls, *args, **kwargs):
        cls._instance = cls(*args, **kwargs)

    @classmethod
    def get_instance(cls):
        if cls._instance:
            return cls._instance
        else:
            raise DataLoaderNotInitialized('Data loader not initialized.'
                                           'You need to run the experiment with an input configuration')

    def __next__(self):
        return next(self.generator)

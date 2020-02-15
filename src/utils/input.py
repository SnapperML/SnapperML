import os
import pandas as pd
from src.utils import root_helper
import glob

dataLoader = None


class UnsupportedColumnSelector(Exception):
    pass


class DataLoaderNotInitializer(Exception):
    pass


def get_csv_columns_selector(column_names):
    if isinstance(column_names, str):
        column_names = column_names.strip()
        if "*" in column_names or "?" in column_names or "[" in column_names:
            return lambda col: col == column_names or glob.fnmatch.fnmatchcase(col, column_names)
        else:
            return lambda col: col == column_names
    if isinstance(column_names, list):
        selectors = [get_csv_columns_selector(c) for c in column_names]
        return lambda col: any([selector(col) for selector in selectors])
    elif isinstance(column_names, dict):
        raise UnsupportedColumnSelector('Unsupported column selector. For csv files, '
                                        'only lists and glob-like strings are supported')


def csv_generator(filepath, columns=None, batch_size=None, **kwargs):
    if batch_size:
        kwargs['chunksize'] = batch_size
    if columns:
        kwargs['usecols'] = get_csv_columns_selector(columns)
    for chunk in pd.read_csv(filepath, **kwargs):
        yield chunk


class DataLoader(object):
    _instance = None

    def __init__(self, file, batch_size=None, **kwargs):
        self._batch_size = batch_size
        _, file_extension = os.path.splitext(file)
        if file_extension == '.root':
            self.generator = root_helper.get_dataframe(file, batch_size=batch_size, **kwargs)
        if file_extension == '.csv':
            self.generator = csv_generator(file, batch_size=batch_size, **kwargs)

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
            raise DataLoaderNotInitializer('Data loader not initialized.'
                                           'You need to run the experiment with an input configuration')

    def __next__(self):
        return next(self.generator)

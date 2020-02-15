import os
import pandas as pd
from src.utils.root_helper import get_dataframe
import glob


class UnsupportedColumnSelector(Exception):
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
    def __init__(self, filepath, batch_size=None, **kwargs):
        self._batch_size = batch_size
        _, file_extension = os.path.splitext(filepath)
        if file_extension == '.root':
            self.generator = get_dataframe(filepath, batch_size=batch_size, **kwargs)
        if file_extension == '.csv':
            self.generator = csv_generator(filepath, batch_size=batch_size, **kwargs)

    @property
    def batch_size(self):
        return self._batch_size

    def __next__(self):
        for df in self.generator:
            yield df

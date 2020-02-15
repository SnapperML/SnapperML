import glob
import pandas as pd
from .exceptions import UnsupportedColumnSelector


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


def get_dataframe(filepath, columns=None, batch_size=None, **kwargs):
    if batch_size:
        kwargs['chunksize'] = batch_size
    if columns:
        kwargs['usecols'] = get_csv_columns_selector(columns)
    for chunk in pd.read_csv(filepath, **kwargs):
        yield chunk

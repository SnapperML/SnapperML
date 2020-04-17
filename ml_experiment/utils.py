from typing import *
from docstring_parser import parse as parse_docstring


def monkey_patch_imported_function(original_func: Callable, new_function: Callable, target: any):
    """
    Monkey-patch functions imported as "from foo import baz".

    Replace an imported function in *target* scope by a new function

    :param original_func: Imported function to be replaced
    :param new_function: New function which replaces original_func
    :param target: Object or function whose scope will be changed
    :return: None
    """
    scope: dict = target.__globals__
    for key in scope.keys():
        if scope[key] == original_func:
            scope[key] = new_function


def recursive_map(func: Callable, seq: Union[Dict, Sequence]):
    if isinstance(seq, Sequence):
        return [recursive_map(func, item) for item in seq]
    elif isinstance(seq, Dict):
        return {k: recursive_map(func, v) for k, v in seq.items()}
    else:
        return func(seq)


def get_description_from_function(func):
    description = ''
    if func.__doc__:
        docstring = parse_docstring(func.__doc__)
        description = f'{docstring.short_description}\n\n{docstring.long_description or ""}'
    return description

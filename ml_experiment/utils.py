from typing import Callable


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

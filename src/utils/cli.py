from inspect import signature
import argparse
from functools import wraps


def cli_decorator(func, description=''):
    """Decorator to create a CLI around a callable.
    It takes automatically its positional and keyword arguments
    and generates the argument parser. """
    parser = argparse.ArgumentParser(description=description)
    sig = signature(func)

    for parameter in sig.parameters.values():
        name = parameter.name.replace('*', '')
        # Not supporting *args or **kwargs arguments for now.
        if parameter.kind != parameter.POSITIONAL_OR_KEYWORD:
            continue
        default = None if parameter.default == parameter.empty else parameter.default
        if default:
            parser.add_argument(f'--{name}', default=default)
        else:
            parser.add_argument(f'{name}')

    @wraps(func)
    def inner():
        args = parser.parse_args()
        return func(**vars(args))
    return inner

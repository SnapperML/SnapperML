from inspect import signature
import argparse
from functools import wraps, partial


def create_argument_parse_from_signature(func, description=""):
    parser = argparse.ArgumentParser(description=description)
    sig = signature(func)

    for parameter in sig.parameters.values():
        name = parameter.name.replace('*', '')
        # Not supporting *args or **kwargs arguments for now.
        if parameter.kind != parameter.POSITIONAL_OR_KEYWORD:
            continue
        if parameter.default == parameter.empty:
            parser.add_argument(f'{name}')
        else:
            parser.add_argument(f'--{name}', default=parameter.default)
    return parser


def cli_decorator(func=None, *, description=""):
    """Decorator to create a CLI around a callable.
    It takes automatically its positional and keyword arguments
    and generates the argument parser. """
    if func is None:
        return partial(cli_decorator, description=description)
    parser = create_argument_parse_from_signature(func, description)
    @wraps(func)
    def inner():
        args = parser.parse_args()
        return func(**vars(args))
    return inner

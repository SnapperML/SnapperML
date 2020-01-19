from docstring_parser import parse as parse_docstring
from inspect import signature
import argparse
from functools import wraps, partial


class CustomHelpFormatter(argparse.HelpFormatter):
    def _get_default_metavar_for_optional(self, action):
        return action.type.__name__ if action.type else 'any'

    def _get_default_metavar_for_positional(self, action):
        return self._get_default_metavar_for_optional(action)


def add_argument(parameter, argument_group, as_keyword):
    name = parameter.name.replace('*', '')
    params = {'type': parameter.annotation} if parameter.annotation != parameter.empty else {}
    if parameter.default == parameter.empty:
        if as_keyword:
            params['required'] = True
        else:
            params['help'] = name
        name = f'--{name}' if as_keyword else name
        argument_group.add_argument(name, **params)
    else:
        argument_group.add_argument(
            f'--{name}',
            default=parameter.default,
            help=f'Default: {parameter.default}',
            **params,
        )


def get_description_from_function(func):
    description = ''
    if func.__doc__:
        docstring = parse_docstring(func.__doc__)
        description = f'{docstring.short_description}\n\n{docstring.long_description or ""}'
    return description


def create_argument_parse_from_function(func, all_keywords=False, *args, **kwargs):
    func_signature = signature(func)
    parser = argparse.ArgumentParser(
        description=get_description_from_function(func),
        formatter_class=CustomHelpFormatter,
        *args,
        **kwargs
    )
    if all_keywords:
        optional = parser._action_groups.pop()
        required = parser.add_argument_group('required arguments')
        parser._action_groups.append(optional)
    else:
        optional = required = parser

    for parameter in func_signature.parameters.values():
        # Not supporting *args or **kwargs arguments for now.
        if parameter.kind != parameter.POSITIONAL_OR_KEYWORD:
            continue
        if parameter.default == parameter.empty:
            add_argument(parameter, required, all_keywords)
        else:
            add_argument(parameter, optional, all_keywords)

    return parser


def cli_decorator(func=None, *, description=""):
    """Decorator to create a CLI around a callable.
    It takes automatically its positional and keyword arguments
    and generates the argument parser. """
    if func is None:
        return partial(cli_decorator, description=description)
    parser = create_argument_parse_from_function(func, description)
    @wraps(func)
    def inner():
        args = parser.parse_args()
        return func(**vars(args))
    return inner


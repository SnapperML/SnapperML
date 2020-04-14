from docstring_parser import parse as parse_docstring
from inspect import signature
import argparse


class CustomHelpFormatter(argparse.HelpFormatter):
    @classmethod
    def get_type_hint(cls, action):
        if not action.type:
            return 'any'
        try:
            return action.type.__name__
        except AttributeError:
            return str(action.type)

    def _get_default_metavar_for_optional(self, action):
        return self.get_type_hint(action)

    def _get_default_metavar_for_positional(self, action):
        # return f'{action.dest}: {self.get_type_hint(action)}'
        return action.dest


def add_argument(parameter, argument_group, as_keyword, as_optional=False):
    # TODO: Handle lists and dicts
    name = parameter.name.replace('*', '')
    kwargs = {'type': parameter.annotation} if parameter.annotation != parameter.empty else {}
    has_default_value = parameter.default != parameter.empty

    if has_default_value:
        kwargs['default'] = parameter.default
        kwargs['help'] = f'Default: {parameter.default}'
        kwargs['required'] = False

    if as_optional:
        kwargs['default'] = argparse.SUPPRESS

    if not has_default_value and not as_optional:
        if as_keyword:
            kwargs['required'] = True
        else:
            kwargs['help'] = name
        name = f'--{name}' if as_keyword else name
        argument_group.add_argument(name, **kwargs)
    else:
        argument_group.add_argument(f'--{name}', **kwargs)


def get_description_from_function(func):
    description = ''
    if func.__doc__:
        docstring = parse_docstring(func.__doc__)
        description = f'{docstring.short_description}\n\n{docstring.long_description or ""}'
    return description


def create_argument_parse_from_function(func, all_keywords=False, all_optional=False, *args, **kwargs):
    func_signature = signature(func)
    kwargs = {
        'description': get_description_from_function(func),
        'formatter_class': CustomHelpFormatter,
        **kwargs,
    }
    parser = argparse.ArgumentParser(*args, **kwargs)

    if all_keywords and not all_optional:
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
            add_argument(parameter, required, all_keywords, as_optional=all_optional)
        else:
            add_argument(parameter, optional, all_keywords, as_optional=all_optional)

    return parser


def get_default_params_from_func(func):
    sig = signature(func)
    return {
        param.name: param.default for param in sig.parameters.values()
        if param.kind == param.POSITIONAL_OR_KEYWORD and param.default != param.empty
    }

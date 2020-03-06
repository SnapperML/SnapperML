import re
from typing import Callable, Any


def validate_numerical_method_str(method_name, value, num_arguments=2, output_type=float):
    if not isinstance(value, str):
        raise TypeError('Must be a string')
    try:
        argument_regex = r'\s*(([0-9]|\.)*)\s*'
        argument_regex = ','.join([argument_regex] * num_arguments)
        match = re.match(rf'{method_name}\({argument_regex}\)', value)
        groups = list(match.groups())
        return tuple([output_type(groups[i]) for i in range(0, len(groups), 2)])
    except Exception:
        params = ", ".join([f'param{i}' for i in range(1, num_arguments + 1)])
        raise TypeError(f'Value must be of the form {method_name}({params})')


class Choice(Callable):
    output_value = Any

    def __init__(self, choices):
        self.choices = choices

    @classmethod
    def validate(cls, value):
        if not isinstance(value, list):
            raise TypeError('List of choices is required')

        return cls(value)

    def __call__(self, trial):
        return trial.suggest_categorical(self.choices)


class Uniform(Callable):
    output_value = float

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    @classmethod
    def validate(cls, value):
        low, high = validate_numerical_method_str('uniform', value)
        return cls(low=low, high=high)

    def __call__(self, trial):
        return trial.suggest_uniform(**self.kwargs)


class LogUniform(Callable):
    output_value = float

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    @classmethod
    def validate(cls, value):
        low, high = validate_numerical_method_str('loguniform', value)
        return cls(low=low, high=high)

    def __call__(self, trial):
        return trial.suggest_loguniform(**self.kwargs)


class Range(Callable):
    output_value = int

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    @classmethod
    def validate(cls, value):
        try:
            start, stop, step = validate_numerical_method_str('range', value, num_arguments=3, output_type=int)
            return cls(start=start, stop=stop, step=step)
        except TypeError:
            start, stop = validate_numerical_method_str('range', value, num_arguments=2, output_type=int)
            return cls(start=start, stop=stop)

    def __call__(self, trial):
        return trial.suggest_categorical(list(range(**self.kwargs)))


class RandomInt(Callable):
    output_value = int

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    @classmethod
    def validate(cls, value):
        low, high = validate_numerical_method_str('randint', value, num_arguments=2, output_type=int)
        return cls(low=low, high=high)

    def __call__(self, trial):
        return trial.suggest_categorical(list(range(**self.kwargs)))

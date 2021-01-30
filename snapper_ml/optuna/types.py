import re
from typing import *
from pydantic import parse_obj_as, ValidationError
from optuna import Trial
import json

T = TypeVar('T')


def validate_numerical_method_str(method_name, value, num_arguments=2) -> Tuple[float, ...]:
    if not isinstance(value, str):
        raise TypeError('Must be a string')
    try:
        argument_regex = r'\s*(([0-9]|\.)*)\s*'
        argument_regex = ','.join([argument_regex] * num_arguments)
        match = re.match(rf'{method_name}\({argument_regex}\)', value)
        groups = list(match.groups())
        return tuple([float(groups[i]) for i in range(0, len(groups), 2)])
    except Exception:
        params = ", ".join([f'param{i}' for i in range(1, num_arguments + 1)])
        raise ValueError(f'Value must be of the form {method_name}({params})')


class Choice(Callable[[str, Trial], T]):
    output_value = Any

    def __init__(self, choices):
        self.choices = choices

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        if isinstance(value, cls):
            return value
        if not isinstance(value, str):
            raise TypeError('List of choices is required')
        try:
            value = value.strip()
            regex = r'choice\(\s*(\[.*\])\s*\)'
            match = re.findall(regex, value, re.IGNORECASE)
            content = json.loads(match[0].replace('\'', '"'))
            if not isinstance(content, list):
                raise Exception()
        except Exception as e:
            raise ValueError('Value must be of the form choice([value1, value2, ...])')
        try:
            result = parse_obj_as(List[Union[ParamDistribution, Any]], content)
        except ValidationError:
            result = content

        return cls(result)

    def __str__(self):
        return f'choice({self.choices})'.lower()

    def __call__(self, name, trial):
        return trial.suggest_categorical(name, self.choices)

    def __repr__(self):
        return self.__str__()


class Uniform(Callable[[str, Trial], float]):
    output_value = float

    def __init__(self, low, high):
        self.low = low
        self.high = high

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        if isinstance(value, cls):
            return value
        low, high = validate_numerical_method_str('uniform', value)
        return cls(low=low, high=high)

    def __call__(self, name, trial):
        return trial.suggest_uniform(name, self.low, self.high)

    def __str__(self):
        return f'uniform({self.low}, {self.high})'

    def __repr__(self):
        return self.__str__()


class LogUniform(Callable[[str, Trial], float]):
    output_value = float

    def __init__(self, low, high):
        self.low = low
        self.high = high

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        if isinstance(value, cls):
            return value
        low, high = validate_numerical_method_str('loguniform', value)
        return cls(low=low, high=high)

    def __call__(self, name, trial):
        return trial.suggest_loguniform(name, self.low, self.high)

    def __str__(self):
        return f'loguniform({self.low}, {self.high})'

    def __repr__(self):
        return self.__str__()


class Range(Callable[[str, Trial], int]):
    output_value = int

    def __init__(self, start: int, stop: int, step=1):
        self.start = start
        self.stop = stop
        self.step = step
        self.choices = list(range(start, stop, step))

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        if isinstance(value, cls):
            return value
        try:
            start, stop, step = validate_numerical_method_str('range', value, num_arguments=3)
            return cls(start=int(start), stop=int(stop), step=int(step))
        except ValueError:
            start, stop = validate_numerical_method_str('range', value, num_arguments=2)
            return cls(start=int(start), stop=int(stop))

    def __call__(self, name, trial):
        return trial.suggest_categorical(name, self.choices)

    def __str__(self):
        return f'range({self.start}, {self.stop}, {self.step})'

    def __repr__(self):
        return self.__str__()


class RandomInt(Callable[[str, Trial], int]):
    output_value = int

    def __init__(self, low, high):
        self.low = low
        self.high = high

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        if isinstance(value, cls):
            return value
        low, high = validate_numerical_method_str('randint', value, num_arguments=2)
        return cls(low=int(low), high=int(high))

    def __call__(self, name, trial):
        return trial.suggest_int(name, self.low, self.high)

    def __str__(self):
        return f'randint({self.low}, {self.high})'

    def __repr__(self):
        return self.__str__()


ParamDistribution = Union[Choice[Any], Range, RandomInt, Uniform, LogUniform]
ParamDistributionBase = Callable[[str, Trial], T]

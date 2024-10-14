from typing import Any, Dict, Tuple, TypeVar, Union, List, Callable
from pydantic import field_serializer
from pydantic_core import CoreSchema, core_schema

from optuna import Trial
import re
import json

T = TypeVar('T')


def validate_numerical_method_str(method_name, value, num_arguments=2) -> Tuple[float, ...]:
    if not isinstance(value, str):
        raise TypeError('Must be a string')
    try:
        argument_regex = r'\s*(([0-9]|\.)*)\s*'
        argument_regex = ','.join([argument_regex] * num_arguments)
        pattern = rf'{method_name}\({argument_regex}\)'

        match = re.match(pattern, value)

        groups = list(match.groups())
        return tuple([float(groups[i]) for i in range(0, len(groups), 2)])
    except Exception:
        params = ", ".join([f'param{i}' for i in range(1, num_arguments + 1)])
        raise ValueError(f'Value must be of the form {method_name}({params}) but {value} was got')


class Choice:
    output_value = Any

    def __init__(self, choices):
        self.choices = choices

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: Callable[[Any], CoreSchema]
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(cls.validate, handler(Any))


    @classmethod
    def validate(cls, value: Any) -> 'Choice':
        if isinstance(value, cls):
            return value
        
        if isinstance(value, ParamDistribution):
            raise ValueError(f'Value must be of the form choice([value1, value2, ...]) but "{value}" was received.')
        elif not isinstance(value, str):
            raise TypeError('A string representation of choices is required')

        value = value.strip()
        regex = r'choice\(\s*(\[.*?\])\s*\)'

        match = re.fullmatch(regex, value, re.IGNORECASE)
        
        if not match:
            raise ValueError(f'Value must be of the form choice([value1, value2, ...]) but "{value}" was received.')

        try:
            # Load the content from the matched string
            content = json.loads(match.group(1).replace("'", '"'))
            
            if not isinstance(content, list):
                raise ValueError('Value must be a list of choices.')

        except json.JSONDecodeError:
            raise ValueError(f'Failed to parse choices from value "{value}". Ensure it is in valid JSON format.')
        except Exception as e:
            raise ValueError(f'An error occurred while validating choices: {str(e)}')

        return cls(content)

    def __str__(self):
        return f'choice({self.choices})'.lower()
    
    def __repr__(self):
        return self.__str__()

    def __call__(self, name, trial: Any):
        return trial.suggest_categorical(name, self.choices) 
    

class Uniform:
    output_value = float

    def __init__(self, low, high):
        self.low = low
        self.high = high

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: Callable[[Any], CoreSchema]
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(cls.validate, handler(Any))


    @classmethod
    def validate(cls, value: Any) -> 'Uniform':
        if isinstance(value, cls):
            return value
        
        if isinstance(value, ParamDistribution):
            raise ValueError(f'Value must be of the form uniform([low, high]) but "{value}" was received.')
        elif not isinstance(value, str):
            raise TypeError('A string representation of uniform is required')

        low, high = validate_numerical_method_str('uniform', value)
        return cls(low=low, high=high)

    def __call__(self, name, trial: Trial):
        return trial.suggest_float(name, self.low, self.high)

    def __str__(self):
        return f'uniform({self.low}, {self.high})'

    def __repr__(self):
        return self.__str__()


class LogUniform:
    output_value = float

    def __init__(self, low, high):
        self.low = low
        self.high = high

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: Callable[[Any], CoreSchema]
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(cls.validate, handler(Any))


    @classmethod
    def validate(cls, value: Any) -> 'LogUniform':
        if isinstance(value, cls):
            return value
        
        if isinstance(value, ParamDistribution):
            raise ValueError(f'Value must be of the form loguniform([low, high]) but "{value}" was received.')
        elif not isinstance(value, str):
            raise TypeError('A string representation of loguniform is required')

        low, high = validate_numerical_method_str('loguniform', value)
        return cls(low=low, high=high)

    def __call__(self, name, trial: Trial):
        return trial.suggest_float(name, self.low, self.high, log=True)

    def __str__(self):
        return f'loguniform({self.low}, {self.high})'

    def __repr__(self):
        return self.__str__()


class Range:
    output_value = int

    def __init__(self, start: int, stop: int, step=1):
        self.start = start
        self.stop = stop
        self.step = step
        self.choices = list(range(start, stop, step))

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: Callable[[Any], CoreSchema]
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(cls.validate, handler(Any))

    @classmethod
    def validate(cls, value: Any) -> 'Range':
        if isinstance(value, cls):
            return value
        
        if isinstance(value, ParamDistribution):
            raise ValueError(f'Value must be of the form range([value1, value2, ...]) but "{value}" was received.')
        elif not isinstance(value, str):
            raise TypeError('A string representation of range is required')

        try:
            # Attempt to validate for three arguments (start, stop, step)
            start, stop, step = validate_numerical_method_str('range', value, num_arguments=3)
            return cls(start=int(start), stop=int(stop), step=int(step))
        except ValueError:
            # Fall back to validating for two arguments (start, stop)
            start, stop = validate_numerical_method_str('range', value, num_arguments=2)
            return cls(start=int(start), stop=int(stop))

    def __call__(self, name, trial: Trial):
        return trial.suggest_categorical(name, self.choices)

    def __str__(self):
        return f'range({self.start}, {self.stop}, {self.step})'

    def __repr__(self):
        return self.__str__()


class RandomInt:
    output_value = int

    def __init__(self, low, high):
        self.low = low
        self.high = high

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: Callable[[Any], CoreSchema]
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(cls.validate, handler(Any))

    @classmethod
    def validate(cls, value: Any) -> 'RandomInt':
        if isinstance(value, cls):
            return value
        
        if isinstance(value, ParamDistribution):
            raise ValueError(f'Value must be of the form randint([low, high]) but "{value}" was received.')
        elif not isinstance(value, str):
            raise TypeError('A string representation of randint is required')

        low, high = validate_numerical_method_str('randint', value, num_arguments=2)
        return cls(low=int(low), high=int(high))

    def __call__(self, name, trial: Trial):
        return trial.suggest_int(name, self.low, self.high)

    def __str__(self):
        return f'randint({self.low}, {self.high})'

    def __repr__(self):
        return self.__str__()


ParamDistribution = Union[Choice, Range, RandomInt, Uniform, LogUniform]

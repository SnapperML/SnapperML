# Experiment Specification


## Experiment Definition

```yaml
name: str
kind: experiment (optional)

params:
  param1: int | str | list | dict
  param2: ...
  ...
  paramN: ...

run:
  - path/to/script1
  ...
  - path/to/scriptN
```


## Group Definition

```yaml
name: str
kind: group (required)

param_space:
  param1: distribution(x1, x2, ..., xN)
  ...
  paramN: distribution(x1, x2, ..., xN)

params:
  otherParam1: int | str | list | dict
  ...
  otherParamN: ...

run:
  - path/to/script1
  ...
  - path/to/scriptN
```


## Parameter space distributions

```
range(min: int, max: int, step: int)
```

```
randint(min: int, max: int)
```

```
loguniform(min: int, max: int)
```

```
uniform(min: int, max: int)
```

```
choice([value1: any, value2: any, ..., valueN: int])
```

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

docker_config:
  image: str
  dockerfile: path/to/dockerfile
  context: path/to/context/directory
  args: dict

ray_config:
  address: localhost | master_node_address
  cpu: positive integer
  gpu: positive integer


run:
  - path/to/script1
  ...
  - path/to/scriptN
```


## Group Definition

```yaml
name: str
kind: group (required)
sampler:
pruner:
timeout_per_trial: positive float
resources_per_worker:
  cpu: positive float
  gpu: positive float


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


## Models Reference

``` eval_rst

.. autoclass:: ml_experiment.config.models.ExperimentConfig
   :show-inheritance:
   :undoc-members:
   :members:


.. autoclass:: ml_experiment.config.models.GroupConfig
   :show-inheritance:
   :undoc-members:
   :members:


.. autoclass:: ml_experiment.config.models.RayConfig
   :show-inheritance:
   :undoc-members:
   :members:


.. autoclass:: ml_experiment.config.models.JobTypes
   :show-inheritance:
   :undoc-members:
   :members:


.. autoclass:: ml_experiment.config.models.Metric
   :show-inheritance:
   :undoc-members:
   :members:


.. autoclass:: ml_experiment.config.models.DockerConfig
   :show-inheritance:
   :undoc-members:
   :members:


.. autoclass:: ml_experiment.config.models.WorkerResourcesConfig
   :show-inheritance:
   :undoc-members:
   :members:
```

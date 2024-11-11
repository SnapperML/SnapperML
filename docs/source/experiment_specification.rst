YAML/JSON Specification
===========================

Configuration files are validated and parsed into Python objects.
Therefore, config files have the same structure as the Python models. Feel free to check them in case of doubt.


Experiment Definition
----------------------

.. code-block:: yaml

    name: str # Required
    kind: experiment # Optional. This is the default value

    # Optional. Defaults to an empty dict
    params:
      param1: int | str | list | dict
      param2: ...
      ...
      paramN: ...

    # Optional. If not specified, the job will be run in the host environment (without Docker).
    docker_config:
      image: str
      dockerfile: path/to/dockerfile
      context: path/to/context/directory
      args: dict

    # Optional. If not specified, the job will be run in a local environment (without Ray).
    # In any case, only one process will be spawned.
    # Any other entry of this dictionary will be passed as it is to Ray.init,
    # so you can fully configure the job execution.
    # More information about the parameters you can use here:
    # https://docs.ray.io/en/master/package-ref.html#ray.init
    ray_config:
      address: localhost | master_node_address

    run: # Required
      - path/to/script1.py
      ...
      - path/to/scriptN.py


Group Definition
------------------
.. code-block:: yaml

    name: str   # Required.
    kind: group # Required. This line should be specified for snapper-ml CLI to know what type of job is this
    sampler: str # Optional.
    pruner: str  # Optional.
    timeout_per_trial: positive float # Optional
    resources_per_worker: # Optional
      cpu: positive float # Required (only if the parent is specified)
      gpu: positive float # Optional.


    # Optional. Defaults to an empty dict
    param_space:
      param1: distribution(x1, x2, ..., xN)
      ...
      paramN: distribution(x1, x2, ..., xN)

      # Distributions can also be used inside a list.
      # The behavior is to sample a random value for each position
      otherParam:
        - distribution(x1, ..., xN]
        ...
        - distribution(x1, ..., xN)

    # Optional. Defaults to an empty dict
    params:
      otherParam1: int | str | list | dict
      ...
      otherParamN: ...

    # Optional. If not specified, the job will be run in a local Ray cluster.
    # Any other entry of this dictionary will be passed as it is to Ray.init,
    # so you can fully configure the job execution.
    # More information about the parameters you can use here:
    ray_config:
      address: localhost | master_node_address

    run:
      - path/to/script1
      ...
      - path/to/scriptN



Parameter space distributions
-----------------------------------

Generates a random integer from min to max with an specific step.

.. code-block:: none

    range(min: int, max: int, step: int)


Generates a random integer from min to max (same as range with step = 1)

.. code-block:: none

    randint(min: int, max: int)


A uniform distribution in the log domain.

.. code-block:: none

    loguniform(min: int, max: int)


A uniform distribution in the linear domain.

.. code-block:: none

    uniform(min: int, max: int)


A categorical distribution based on the values provided. The sample parameter will be selected randomly
(with uniform probability) among the provided values.

.. code-block:: none

    choice([value1: any, value2: any, ..., valueN: int])



Models Reference
-------------------------

.. _models:


.. autoclass:: snapper_ml.config.models.ExperimentConfig
   :show-inheritance:
   :undoc-members:
   :members:


.. autoclass:: snapper_ml.config.models.GroupConfig
   :show-inheritance:
   :undoc-members:
   :members:


.. autoclass:: snapper_ml.config.models.RayConfig
   :show-inheritance:
   :undoc-members:
   :members:


.. autoclass:: snapper_ml.config.models.JobTypes
   :show-inheritance:
   :undoc-members:
   :members:


.. autoclass:: snapper_ml.config.models.Metric
   :show-inheritance:
   :undoc-members:
   :members:


.. autoclass:: snapper_ml.config.models.DockerConfig
   :show-inheritance:
   :undoc-members:
   :members:


.. autoclass:: snapper_ml.config.models.WorkerResourcesConfig
   :show-inheritance:
   :undoc-members:
   :members:


.. autoclass:: snapper_ml.config.models.PrunerEnum
   :undoc-members:
   :members:


.. autoclass:: snapper_ml.config.models.SamplerEnum
   :undoc-members:
   :members:

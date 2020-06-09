Package Reference
=========================================

Overview
-----------------

.. autosummary::

  ml_experiment
  ml_experiment.callbacks
  ml_experiment.callbacks.notifiers
  ml_experiment.integrations
  ml_experiment.config.models


ml_experiment
--------------

.. automodule:: ml_experiment


.. autodecorator:: ml_experiment.job


.. autoclass:: ml_experiment.DataLoader
   :undoc-members:
   :members:


.. autoclass:: ml_experiment.Trial
   :undoc-members:
   :members:


.. autoclass:: ml_experiment.AutologgingBackend
   :undoc-members:
   :members:


ml_experiment.callbacks
------------------------

.. automodule:: ml_experiment.callbacks


.. autoclass:: ml_experiment.callbacks.Callback
   :undoc-members:
   :members:


.. automodule:: ml_experiment.callbacks.notifiers


.. autoclass:: ml_experiment.callbacks.notifiers.NotifierBase
   :members:


.. autoclass:: ml_experiment.callbacks.notifiers.TelegramNotifier
.. autoclass:: ml_experiment.callbacks.notifiers.DesktopNotifier
.. autoclass:: ml_experiment.callbacks.notifiers.SlackNotifier
.. autoclass:: ml_experiment.callbacks.notifiers.EmailNotifier


ml_experiment.integrations
---------------------------

.. automodule:: ml_experiment.integrations

All these classes are imported from Optuna package. For more
information of how to use, please take a look at the official
documentation `here <https://optuna.readthedocs.io/en/latest/reference/integration.html>`_.

.. autoclass:: ml_experiment.integrations.KerasPruningCallback
.. autoclass:: ml_experiment.integrations.TensorFlowPruningHook
.. autoclass:: ml_experiment.integrations.TFKerasPruningCallback
.. autoclass:: ml_experiment.integrations.XGBoostPruningCallback
.. autoclass:: ml_experiment.integrations.LightGBMPruningCallback
.. autoclass:: ml_experiment.integrations.PyTorchIgnitePruningHandler
.. autoclass:: ml_experiment.integrations.PyTorchLightningPruningCallback
.. autoclass:: ml_experiment.integrations.FastAIPruningCallback
.. autoclass:: ml_experiment.integrations.MXNetPruningCallback
.. autoclass:: ml_experiment.integrations.ChainerPruningExtension


ml_experiment.config.models
----------------------------

.. automodule:: ml_experiment.config.models


.. autoclass:: ml_experiment.config.models.Metric
   :undoc-members:
   :members:

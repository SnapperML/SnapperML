# SnapperML

[![](https://readthedocs.org/projects/snapperml/badge/?style=for-the-badge&version=latest)](https://snapperml.readthedocs.io/en/latest/?badge=latest)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)
[![PyPI version](https://img.shields.io/pypi/v/snapper-ml.svg?style=for-the-badge)](https://pypi.org/project/snapper-ml/)

![SnapperML](https://raw.githubusercontent.com/SnapperML/SnapperML/refs/heads/master/docs/assets/banner.png)

SnapperML is a comprehensive framework for experiment tracking and machine learning operationalization (MLOps), built using well-supported technologies like [Mlflow](https://mlflow.org/), [Ray](https://github.com/ray-project/ray/), Docker, and more. It provides an opinionated workflow designed to facilitate both local and cloud-based experimentation.

## Key Features

- **Automatic Tracking**: Seamless integration with MLflow for parameter and metric tracking.
- **Distributed Training**: First-class support for distributed training and hyperparameter optimization using Optuna and Ray.
- **CLI-Based Execution**: Easily package and execute projects within containers using our intuitive Command Line Interface (CLI).
- **Web Interface**: A modern web interface developed with Vite, React, TypeScript, and Bootstrap for managing experiment configurations.

## Project Goals

SnapperML aims to:

1. **Enhance Maintainability**: By addressing technical debt and improving the codebase, making it cleaner and more efficient.
1. **Improve Scalability**: Ensure the system can handle large-scale experiments and concurrent requests smoothly.
1. **Provide a Robust Web UI**: A user-friendly interface that simplifies the setup and execution of ML experiments.
1. **Ensure Reproducibility**: Leverage MLOps principles to ensure experiments can be replicated easily.

## Architecture

### Overview

SnapperML integrates several components to streamline machine learning workflows:

- **CLI Framework**: Facilitates command-based interactions and logging for experiment execution.
- **Flask API**: Manages requests from the frontend and interfaces with backend processes.
- **Vite-Powered Web UI**: An accessible and intuitive web application that handles experiment configurations and tracks real-time logs.
- **Containerized Databases**: Securely stores experiment results using containerized MLflow and Optuna databases.
  > [!IMPORTANT]
  > Be sure to configure your databases and network settings carefully to ensure the security and integrity of your experiment data.

![Architecture Overview](https://raw.githubusercontent.com/SnapperML/SnapperML/refs/heads/master/docs/assets/snapperml_architecture.png)

## Installation

### Prerequisites

- docker
- python 3.12+
- node.js (for UI development)

### Install

The python package can be install using **pip**:

```
pip install snapper-ml
```

Or from this repo:

```
pip install .
```

> [!NOTE]
> Python 3.12 or later is required. Ensure that Docker is installed and running on your system for full functionality.

## Deploy

To run SnapperML, you first need to deploy MLflow and Optuna databases. Execute:

> [!TIP]
> To use the SnapperML web interface, deploy it with:

```
snapper-ml make docker
```

Once the deploy finished you can execute `snapper-ml` in the CLI. For an ilustrative example, check the [example section](#Example).

To use snapperML web interface you need to deploy it too.

```
snapper-ml make UI
```

Open [localhost:4000](http://localhost:4000/) and upload your firsts experiments!

![UI](https://raw.githubusercontent.com/SnapperML/SnapperML/refs/heads/master/docs/assets/UI.png)

To stop snapper UI just execute:

```
make stop_UI
```

And to stop mlflow and optuna databases execute:

```
make stop_docker
```

> [!CAUTION]
> Running make stop_UI also stops the Docker containers for the databases, so ensure you have saved all necessary data.

## Documentation

The documentation is available [here](https://snapperml.readthedocs.io/en/latest/)

> [!TIP]
> Visit the documentation for more examples and detailed instructions.

## Example

```python
# train_svm.py

from snapper_ml import job

@job
def main(C, kernel, gamma='scale'):
    np.random.seed(1234)
    X_train, X_val, y_train, y_val = load_data()
    model = SVC(C=C, gamma=gamma, kernel=kernel)
    model.fit(X_train, y_train)
    accuracy = model.score(X_val, y_val)
    return {'val_accuracy': accuracy}


if __name__ == '__main__':
    main()
```

```yaml
# train_svm.yaml

name: "SVM"
kind: "group"
num_trials: 12
sampler: TPE

param_space:
  C: loguniform(0.01, 1000)
  gamma: choice(['scale', 'auto'])

metric:
  name: val_accuracy
  direction: maximize

ray_config:
  num_cpus: 4

data:
  folder: data/
  files: ["*QGSJet.txt"]

run:
  - train_svm.py
```

```

snapper-ml run --config_file=train_svm.yaml
```

> [!WARNING]
> Make sure the configuration files are correctly set to avoid runtime errors. Misconfigured parameters could lead to unexpected behavior.

There are more examples in the [examples folder](https://github.com/yerasiito/SnapperML/tree/master/examples).

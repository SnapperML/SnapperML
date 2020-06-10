# Running your first experiment

## Quickstart

### 1. Instrumenting a python script

```python
from ml_experiment import job

import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris

SEED = 1234

@job # ADD THIS DECORATOR
def main(C = 1.0, kernel = 'rbf', degree = 3, gamma = 'scale'):
    np.random.seed(SEED)
    iris = load_iris()
    X_train, X_val, y_train, y_val = train_test_split(iris.data, iris.target, random_state=SEED)
    model = SVC(C=C, gamma=gamma, kernel=kernel, degree=degree)
    model.fit(X_train, y_train)
    accuracy = model.score(X_val, y_val)
    return {'val_accuracy': accuracy}


if __name__ == '__main__':
    main()
```

### 2. Defining a configuration file

Defining a configuration file is straightforward, we just need to create a YAML/JSON file and specify the name
of the experiment, its parameters, and the file to execute.

```yaml
name: "SVM #1"

params:
  C: 10
  kernel: poly
  gamma: auto
  degree: 3

run:
  - examples/scripts/train_svm.py
```

### 3. Executing the experiment 

Finally, once we have an instrumented Python script and a config file, we can execute the job as follows:

```bash
ml-experiment --config_file examples/experiments/svm.yaml
```


## Running jobs in a Docker container


```yaml
docker_config:
  image: image_name:tag
```


```yaml
docker_config:
  dockerfile: path/to/dockerfile
```


## Adding callbacks

Callbacks are an important aspect in almost any ML/DL framework.
Callbacks allow one to hook into the process and react to some event happening.

ml-experiment offers a simple callback system based on the class
[Callback][]. In order to implement a custom callback, all it takes is implementing that
abstract class.

Once we've implemented a custom callback class, we can add an instance of it
as *callbacks* argument of [job][]

The module [notifiers][] contains some predefined callbacks for notifications. It 


```python
from ml_experiment import job
from ml_experiment.callbacks.notifiers import DesktopNotifier

import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris

SEED = 1234

# ADD THIS
@job(callbacks=[DesktopNotifier()])
def main(C = 1.0, kernel = 'rbf', degree = 3, gamma = 'scale'):
    np.random.seed(SEED)
    iris = load_iris()
    X_train, X_val, y_train, y_val = train_test_split(iris.data, iris.target, random_state=SEED)
    model = SVC(C=C, gamma=gamma, kernel=kernel, degree=degree)
    model.fit(X_train, y_train)
    accuracy = model.score(X_val, y_val)
    return {'val_accuracy': accuracy}


if __name__ == '__main__':
    main()
```

[notifiers]: <package_reference.html#ml_experiment.callbacks.notifiers.NotifierBase>
[job]: <package_reference.html#ml_experiment.job>
[Callback]: <package_reference.html#ml_experiment.callbacks.Callback>

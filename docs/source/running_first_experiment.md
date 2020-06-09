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

@job
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

```bash
ml-experiment --config_file examples/experiments/svm.yaml
```


## Running jobs in a Docker container


```yaml
name: "SVM #2"

params:
  C: 10
  kernel: poly
  gamma: auto
  degree: 3

docker_config:
  image: image_name:tag

run:
  - examples/scripts/train_svm.py
```


```yaml
name: "SVM #2"

params:
  C: 10
  kernel: poly
  gamma: auto
  degree: 3

docker_config:
  dockerfile: path/to/dockerfile

run:
  - examples/scripts/train_svm.py
```


## Adding callbacks


```python
from ml_experiment import job
from ml_experiment.callbacks.notifiers import DesktopNotifier

import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris

SEED = 1234

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

# Hyperparameter Tuning


## From experiments to group of experiments

```yaml
name: "SVM"
kind: 'group'
num_trials: 10

param_space:
  C: loguniform(0.01, 1000)
  kernel: choice(['rbf', 'poly', 'linear'])
  gamma: choice(['scale', 'auto'])
  degree: range(2, 5)

params:
  C: 1.0

metric:
  name: val_accuracy
  direction: maximize

run:
  - examples/scripts/train_svm.py
```

### Configuring the Ray cluster

```yaml
resources_per_worker:
  cpu: 0.25
  gpu: 0.5

ray_config:
  num_cpus: 4
  num_gpus: 1
```

> NOTE: Docker integration and Ray integration are incompatible for the moment. So, Docker is not supported
for running groups of experiments.


### Pruning unpromising trails

```yaml
sampler: tpe
pruner: hyperband
```

## Sharing data across multiples processes

```python
from ml_experiment import job, DataLoader
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler


SEED = 1234 


class MyDataLoader(DataLoader):
    @classmethod
    def load_data(cls):
        iris = load_iris()
        X_train, X_val, y_train, y_val = train_test_split(iris.data, iris.target, random_state=SEED)
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_val = scaler.transform(X_val)
        return X_train, X_val, y_train, y_val


@job(data_loader=MyDataLoader)
def main(C = 1.0, kernel = 'rbf', degree = 3, gamma = 'scale'):
    X_train, X_val, y_train, y_val = MyDataLoader.load_data()
    model = SVC(C=C, gamma=gamma, kernel=kernel, degree=degree)
    model.fit(X_train, y_train)
    accuracy = model.score(X_val, y_val)
    return {'val_accuracy': accuracy}

```


## Accessing the Trial instance to model a complex parameter space

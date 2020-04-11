from typing import *
from modelling.utils.data import UnifiedDataLoader, SEED
import numpy as np
from ml_experiment import experiment
from sklearn.svm import SVC


@experiment(data_loader=UnifiedDataLoader)
def main(C: float = 1.0, kernel: str = 'rbf', degree: int = 3, gamma: Any = 'scale'):
    np.random.seed(SEED)
    X_train, X_val, y_train, y_val = UnifiedDataLoader.load_data()
    model = SVC(C=C, kernel=kernel, degree=degree, gamma=gamma)
    model.fit(X_train, X_val)
    accuracy = model.score(X_val, y_val)
    return {'val_accuracy': accuracy}


if __name__ == '__main__':
    main()

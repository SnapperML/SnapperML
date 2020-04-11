import glob
from typing import Tuple, List

import numpy as np
from ml_experiment import DataLoader
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler


Dataset = Tuple[np.ndarray, np.ndarray]
VALIDATION_SPLIT = 0.2
SEED = 1234


class SplitDataLoader(DataLoader):
    @classmethod
    def load_data(cls) -> Tuple[List[Dataset], List[Dataset]]:
        train_files = glob.glob('data/raw/QGSJet-*-train.txt')
        datasets = [np.genfromtxt(file, delimiter=',') for file in train_files]
        train_datasets, val_datasets, = [], []

        for i, dataset in enumerate(datasets):
            class_vector = np.full(dataset.shape[0], i)
            X_train, X_val, y_train, y_val = train_test_split(dataset, class_vector,
                                                              test_size=VALIDATION_SPLIT,
                                                              random_state=SEED)
            scaler = MinMaxScaler()
            X_train = scaler.fit_transform(X_train)
            X_val = scaler.transform(X_val)
            train_datasets.append((X_train, y_train))
            val_datasets.append((X_val, y_val))

        return train_datasets, val_datasets


class UnifiedDataLoader(DataLoader):
    @classmethod
    def load_data(cls) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        train_files = glob.glob('data/raw/QGSJet-*-train.txt')
        datasets = [np.genfromtxt(file, delimiter=',') for file in train_files]
        X, y = [], []

        for i, dataset in enumerate(datasets):
            X.append(dataset)
            y.append(np.full(dataset.shape[0], i))

        X = np.concatenate(X, axis=0)
        y = np.concatenate(y, axis=0)

        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=VALIDATION_SPLIT, random_state=SEED)
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_val = scaler.transform(X_val)
        return X_train, X_val, y_train, y_val

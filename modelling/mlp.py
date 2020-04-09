import glob
from typing import *
from keras.layers import Input, Dense, Dropout
from keras.models import Model
from keras.optimizers import Adam
from keras import regularizers
from keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from ml_experiment import experiment, AutologgingBackend, DataLoader

VALIDATION_SPLIT = 0.2
SEED = 1234


class MyDataLoader(DataLoader):
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
        scaler = MinMaxScaler()
        X_train = scaler.fit_transform(X_train)
        X_val = scaler.transform(X_val)
        return X_train, X_val, y_train, y_val


def create_model(input_size, layers, regularization, ps) -> Model:
    pass


@experiment(autologging_backends=AutologgingBackend.KERAS)
def main(layers: List[int], epochs: int, batch_size: int = 128, regularization: float = 0, ps: float = 0):
    """Simple autoencoder"""
    np.random.seed(SEED)
    X_train, X_val, y_train, y_val = MyDataLoader.load_data()

    early_stopping = EarlyStopping(patience=40, restore_best_weights=True)
    model = create_model(X_train.shape[1], layers, regularization, ps)
    history = model.fit(
        X_train,
        X_train,
        epochs=epochs,
        batch_size=batch_size,
        shuffle=True,
        validation_data=(X_val, X_val),
        callbacks=[early_stopping],
        verbose=0)

    accuracy = model.evaluate(X_val, y_val)
    return {'val_accuracy': accuracy}


if __name__ == '__main__':
    main()

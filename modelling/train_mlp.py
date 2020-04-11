import glob
from typing import *
from keras.layers import Dense, Dropout, Activation, BatchNormalization
from keras.models import Model, Sequential
from keras.optimizers import Adam, SGD
from keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import numpy as np
from ml_experiment import experiment, AutologgingBackend, DataLoader, Trial
from ml_experiment.integrations import KerasPruningCallback
from modelling.utils.one_cycle import OneCycleLR

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
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_val = scaler.transform(X_val)
        return X_train, X_val, y_train, y_val


def create_model(output_size, layers, ps, optimizer, activation, use_bn) -> Model:
    if not isinstance(ps, list):
        ps = [ps] * len(layers)

    model = Sequential()

    for i, (units, p) in enumerate(zip(layers, ps)):
        model.add(Dense(units))
        if use_bn:
            model.add(BatchNormalization())
        model.add(Activation(activation=activation))
        model.add(Dropout(rate=p))

    model.add(Dense(output_size, activation='sigmoid'))
    model.compile(optimizer, loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model


@experiment(autologging_backends=AutologgingBackend.KERAS, data_loader=MyDataLoader)
def main(layers: List[int],
         epochs: int,
         batch_size: int = 128,
         ps: Union[List[float], float] = 0,
         one_cycle: bool = True,
         activation='relu',
         use_bn=True,
         lr: float = 1e-3):
    """Simple autoencoder"""
    np.random.seed(SEED)
    X_train, X_val, y_train, y_val = MyDataLoader.load_data()
    num_classes = len(np.unique(y_train))

    callbacks = [
        EarlyStopping(patience=50, restore_best_weights=True, monitor='val_accuracy'),
        KerasPruningCallback(Trial.get_current(), monitor='val_accuracy')
    ]

    if one_cycle:
        optimizer = SGD(learning_rate=lr)
        callbacks.append(OneCycleLR(lr, verbose=False))
    else:
        optimizer = Adam(learning_rate=lr)

    model = create_model(
        output_size=num_classes,
        layers=layers,
        ps=ps,
        optimizer=optimizer,
        activation=activation,
        use_bn=use_bn)

    history = model.fit(
        X_train,
        y_train,
        epochs=epochs,
        batch_size=batch_size,
        shuffle=True,
        validation_data=(X_val, y_val),
        callbacks=callbacks,
        verbose=0)

    accuracy = np.max(history.history['val_accuracy'])
    return {'val_accuracy': accuracy}


if __name__ == '__main__':
    main()

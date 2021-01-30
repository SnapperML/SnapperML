from typing import *
from keras.layers import Dense, Dropout, Activation, BatchNormalization
from keras.models import Model, Sequential
from keras.optimizers import Adam, SGD
from keras.callbacks import EarlyStopping
from modelling.utils.data import UnifiedDataLoader
import numpy as np
from snapper_ml import job, AutologgingBackend, Trial
from snapper_ml.integrations import KerasPruningCallback
from modelling.utils.one_cycle import OneCycleLR

VALIDATION_SPLIT = 0.2
SEED = 1234


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


@job(autologging_backends=AutologgingBackend.KERAS, data_loader_func=UnifiedDataLoader)
def main(layers: List[int],
         epochs: int,
         batch_size: int = 128,
         ps: Union[List[float], float] = 0,
         one_cycle: bool = True,
         activation: str = 'relu',
         use_bn=True,
         lr: float = 1e-3):
    """Simple autoencoder"""
    np.random.seed(SEED)
    X_train, X_val, y_train, y_val = UnifiedDataLoader.load_data()
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

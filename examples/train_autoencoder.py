from typing import *
import numpy as np
from snapper_ml import job, AutologgingBackend

from keras.layers import Dense, Dropout, Input
from keras.models import Sequential, Model
from keras.optimizers import SGD
from keras import constraints
import keras.backend as K
import tensorflow as tf
from keras.callbacks import EarlyStopping
from modelling.utils.data import SplitDataLoader, SEED
from scipy.spatial.distance import euclidean
from tied_autoencoder_keras import DenseLayerAutoencoder
from modelling.utils.one_cycle import OneCycleLR


class WeightsOrthogonalityConstraint(constraints.Constraint):
    def __init__(self, encoding_dim, weightage=1.0, axis=0):
        self.encoding_dim = encoding_dim
        self.weightage = weightage
        self.axis = axis

    def weights_orthogonality(self, w):
        if self.axis == 1:
            w = K.transpose(w)
        if self.encoding_dim > 1:
            m = K.dot(K.transpose(w), w) - K.eye(self.encoding_dim)
            return self.weightage * K.sqrt(K.sum(K.square(m)))
        else:
            m = K.sum(w ** 2) - 1.
            return m

    def __call__(self, w):
        return self.weights_orthogonality(w)


class UncorrelatedFeaturesConstraint(constraints.Constraint):
    def __init__(self, encoding_dim, weightage=1.0):
        self.encoding_dim = encoding_dim
        self.weightage = weightage

    def get_covariance(self, x):
        x_centered = K.transpose(x - K.mean(x, axis=0, keepdims=True))
        covariance = K.dot(x_centered, K.transpose(x_centered)) / tf.cast(x_centered.get_shape()[0], tf.float32)
        return covariance

    # Constraint penalty
    def uncorrelated_feature(self, x):
        if self.encoding_dim <= 1:
            return 0.0
        else:
            output = self.covariance - tf.math.multiply(self.covariance, K.eye(self.encoding_dim))
            return K.sum(K.square(output))

    def __call__(self, x):
        self.covariance = self.get_covariance(x)
        return self.weightage * self.uncorrelated_feature(x)


def get_constraints(encoding_dim: int,
                    unit_norm_constraint: bool = False,
                    uncorrelated_features: bool = False,
                    weight_orthogonality: bool = False):
    kernel_constraint, kernel_regularizer, activity_regularizer = None, None, None
    if unit_norm_constraint:
        kernel_constraint = constraints.UnitNorm(axis=0)
    if uncorrelated_features:
        activity_regularizer = UncorrelatedFeaturesConstraint(encoding_dim, weightage=1.0)
    if weight_orthogonality:
        kernel_regularizer = WeightsOrthogonalityConstraint(encoding_dim, weightage=1.0, axis=0)
    return kernel_constraint, kernel_regularizer, activity_regularizer


def create_untied_model(
        input_size: int,
        encoding_dim: Union[List[int], int],
        ps: float,
        activation: str = 'relu',
        unit_norm_constraint: bool = False,
        uncorrelated_features: bool = False,
        weight_orthogonality: bool = False):
    np.random.seed(SEED)
    autoencoder = Sequential()
    autoencoder.add(Dropout(rate=ps))
    decoding_dim = [input_size] + encoding_dim[:-1]
    kernel_constraint, kernel_regularizer, activity_regularizer = get_constraints(encoding_dim[-1],
                                                                                  unit_norm_constraint,
                                                                                  weight_orthogonality,
                                                                                  uncorrelated_features)
    for i, units in enumerate(encoding_dim):
        kwargs = {'input_shape': (input_size,)} if i == 0 else {}
        kwargs['kernel_regularizer'] = kernel_regularizer
        kwargs['activity_regularizer'] = activity_regularizer if i == len(encoding_dim) - 1 else None
        encoder = Dense(units,
                        activation=activation,
                        use_bias=True,
                        kernel_constraint=kernel_constraint,
                        **kwargs)
        autoencoder.add(encoder)

    for i, units in enumerate(decoding_dim[::-1]):
        layer_activation = 'sigmoid' if i == len(encoding_dim) - 1 else activation
        decoder = Dense(units,
                        activation=layer_activation,
                        use_bias=True,
                        kernel_constraint=kernel_constraint,
                        kernel_regularizer=kernel_regularizer)
        autoencoder.add(decoder)

    return autoencoder


def create_model(input_size: int, encoding_dim: List[int], lr: float,
                 ps: float, activation: str, tied_weights: bool, **kwargs):
    """Single fully-connected neural layer as encoder and decoder"""
    if not isinstance(encoding_dim, list):
        encoding_dim = [encoding_dim]

    if tied_weights:
        inputs = Input(shape=(input_size,))
        x = DenseLayerAutoencoder(encoding_dim, dropout=ps)(inputs)
        autoencoder = Model(inputs=inputs, outputs=x)
    else:
        autoencoder = create_untied_model(input_size, encoding_dim, ps, activation, **kwargs)

    autoencoder.compile(SGD(learning_rate=lr), loss='mse')
    return autoencoder


@job(autologging_backends=AutologgingBackend.KERAS, data_loader_func=SplitDataLoader)
def main(encoding_dim: Union[int, List[int]],
         epochs: int,
         batch_size: int = 128,
         ps: float = 0,
         activation: str = 'relu',
         one_cycle: bool = True,
         lr: float = 1e-3,
         tied_weights: bool = False,
         unit_norm_constraint: bool = False,
         weight_orthogonality: bool = False):
    train_datasets, val_datasets = SplitDataLoader.load_data()
    autoencoders = []

    for train, val in zip(train_datasets, val_datasets):
        X_train, _ = train
        X_val, _ = val
        # callbacks = [EarlyStopping(patience=50, restore_best_weights=True)]
        callbacks = []
        if one_cycle:
            callbacks.append(OneCycleLR(lr, verbose=False))
        autoencoder = create_model(
            X_train.shape[1],
            encoding_dim=encoding_dim,
            ps=ps,
            tied_weights=tied_weights,
            unit_norm_constraint=unit_norm_constraint,
            weight_orthogonality=weight_orthogonality,
            activation=activation,
            lr=lr
        )
        autoencoder.fit(
            X_train,
            X_train,
            epochs=epochs,
            batch_size=batch_size,
            shuffle=True,
            validation_data=(X_val, X_val),
            callbacks=callbacks,
            verbose=0)
        autoencoders.append(autoencoder)

    X_val = [dataset[0] for dataset in val_datasets]
    y_val = [dataset[1] for dataset in val_datasets]
    X_val = np.concatenate(X_val, axis=0)
    y_val = np.concatenate(y_val, axis=0)

    predictions = [autoencoder.predict(X_val) for autoencoder in autoencoders]
    y_preds = []

    print(predictions)

    for i, x in enumerate(X_val):
        preds = [euclidean(x, X_pred[i]) for X_pred in predictions]
        y_preds.append(np.argmin(preds))

    y_preds = np.array(y_preds)
    accuracy = np.mean(y_preds == y_val)
    return {'val_accuracy': accuracy}


if __name__ == '__main__':
    main()

from typing import *
import numpy as np
from snapper_ml import job, AutologgingBackend

from keras.layers import Dense, Dropout, Input, Lambda
from keras.models import Sequential, Model
from keras.losses import mse
from keras.optimizers import SGD
import keras.backend as K
from keras.callbacks import EarlyStopping
from modelling.utils.data import SplitDataLoader, SEED
from scipy.spatial.distance import euclidean
from modelling.utils.one_cycle import OneCycleLR


def sampling(args):
    """Reparameterization trick by sampling from an isotropic unit Gaussian.

    # Arguments
        args (tensor): mean and log of variance of Q(z|X)

    # Returns
        z (tensor): sampled latent vector
    """
    z_mean, z_log_var = args
    batch = K.shape(z_mean)[0]
    dim = K.int_shape(z_mean)[1]
    # by default, random_normal has mean = 0 and std = 1.0
    epsilon = K.random_normal(shape=(batch, dim))
    return z_mean + K.exp(0.5 * z_log_var) * epsilon


def create_loss(input_dim, inputs, outputs, mu, sigma):
    # VAE loss = mse_loss or xent_loss + kl_loss
    reconstruction_loss = mse(inputs, outputs) * input_dim
    kl_loss = 1 + sigma - K.square(mu) - K.exp(sigma)
    kl_loss = K.sum(kl_loss, axis=-1)
    kl_loss *= -0.5
    return K.mean(reconstruction_loss + kl_loss)


def create_model(
        input_size: int,
        encoding_dim: Union[List[int], int],
        latent_dim: int,
        ps: float,
        lr: float,
        activation: str = 'relu'):
    np.random.seed(SEED)
    decoding_dim = [input_size] + encoding_dim[:-1]

    inputs = Input(shape=(input_size, ), name='encoder_input')
    encoder = Dropout(rate=ps)(inputs)

    for i, units in enumerate(encoding_dim):
        kwargs = {'input_shape': (input_size,)} if i == 0 else {}
        encoder = Dense(units, activation=activation, **kwargs)(encoder)

    mu = Dense(latent_dim, name='mu')(encoder)
    sigma = Dense(latent_dim, name='log_var')(encoder)
    z = Lambda(sampling, output_shape=(latent_dim,), name='z')([mu, sigma])
    encoder = Model(inputs, [mu, sigma, z], name='encoder')

    latent_inputs = Input(shape=(latent_dim,), name='z_sampling')
    decoder = latent_inputs

    for i, units in enumerate(decoding_dim[::-1]):
        layer_activation = 'sigmoid' if i == len(encoding_dim) - 1 else activation
        decoder = Dense(units, activation=layer_activation)(decoder)

    decoder = Model(latent_inputs, decoder, name='decoder')
    outputs = decoder(encoder(inputs)[2])
    autoencoder = Model(inputs, outputs, name='vae_mlp')
    loss = create_loss(input_size, inputs, outputs, mu, sigma)
    autoencoder.add_loss(loss)
    autoencoder.compile(SGD(learning_rate=lr), loss='mse')
    return autoencoder, encoder, decoder


@job(autologging_backends=AutologgingBackend.KERAS, data_loader_func=SplitDataLoader)
def main(encoding_dim: Union[int, List[int]],
         epochs: int,
         latent_dim: int,
         batch_size: int = 128,
         ps: float = 0,
         activation: str = 'relu',
         one_cycle: bool = True,
         lr: float = 1e-3):
    train_datasets, val_datasets = SplitDataLoader.load_data()
    autoencoders = []

    for train, val in zip(train_datasets, val_datasets):
        X_train, _ = train
        X_val, _ = val

        callbacks = [EarlyStopping(patience=50, restore_best_weights=True)]
        if one_cycle:
            callbacks.append(OneCycleLR(lr, verbose=False))

        autoencoder, _, _ = create_model(
            X_train.shape[1],
            encoding_dim=encoding_dim,
            ps=ps,
            activation=activation,
            latent_dim=latent_dim,
            lr=lr,
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

    for i, x in enumerate(X_val):
        preds = [euclidean(x, X_pred[i]) for X_pred in predictions]
        y_preds.append(np.argmin(preds))

    y_preds = np.array(y_preds)
    accuracy = np.mean(y_preds == y_val)
    return {'val_accuracy': accuracy}


if __name__ == '__main__':
    main()

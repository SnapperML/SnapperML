from keras.layers import Input, Dense
from keras.models import Model
from keras import regularizers
import pandas as pd
import src.utils.cli


def create_model(input_shape, encoding_dim, regularizer, optimizer):
    """Single fully-connected neural layer as encoder and decoder"""
    input = Input(shape=(input_shape, ))
    encoded = Dense(encoding_dim, activation='relu', activity_regularizer=regularizer)(input)
    decoded = Dense(input_shape, activation='sigmoid')(encoded)
    autoencoder = Model(input, decoded)
    encoder = Model(input, encoded)
    encoded_input = Input(shape=(encoding_dim,))
    decoder_layer = autoencoder.layers[-1]
    decoder = Model(encoded_input, decoder_layer(encoded_input))
    autoencoder.compile(optimizer, loss='binary_crossentropy')
    return autoencoder, encoder, decoder


def main(train_data, encoding_dim, optimizer, epochs, batch_size=256, l1_regularization=0):
    dataframe = pd.load_csv(train_data)
    regularizer = regularizers.l1(l1_regularization) if l1_regularization else None
    autoencoder, encoder, decoder = create_model(
        dataframe, encoding_dim, regularizer, optimizer)
    autoencoder.fit(
        dataframe,
        dataframe,
        epochs=epochs,
        batch_size=batch_size,
        shuffle=True,
        validation_data=(dataframe, dataframe),
        verbose=2)

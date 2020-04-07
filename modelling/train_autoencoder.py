import glob
from typing import *
from keras.layers import Input, Dense
from keras.models import Model
from keras import regularizers
from keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from ml_experiment import experiment, AutologgingBackend, DataLoader

VALIDATION_SPLIT = 0.2
SEED = 1234

np.random.seed(SEED)

Dataset = Tuple[np.ndarray, np.ndarray]


class MyDataLoader(DataLoader):
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


def create_model(input_size, encoding_dim, optimizer):
    """Single fully-connected neural layer as encoder and decoder"""
    input = Input(shape=(input_size,))
    encoded = Dense(encoding_dim, activation='relu')(input)
    decoded = Dense(input_size, activation='sigmoid')(encoded)
    autoencoder = Model(input, decoded)
    encoder = Model(input, encoded)
    encoded_input = Input(shape=(encoding_dim,))
    decoder_layer = autoencoder.layers[-1]
    decoder = Model(encoded_input, decoder_layer(encoded_input))
    autoencoder.compile(Adam(learning_rate=1e-2), loss='binary_crossentropy')
    return autoencoder, encoder, decoder


@experiment(autologging_backends=AutologgingBackend.KERAS)
def main(encoding_dim: int, optimizer: str, epochs: int, batch_size: int = 128, l1_regularization=None):
    """Simple autoencoder with Dropout"""
    train_datasets, val_datasets = MyDataLoader.load_data()
    # regularizer = regularizers.l1(l1_regularization) if l1_regularization else None
    autoencoders = []

    for train, val in zip(train_datasets, val_datasets):
        X_train, _ = train
        X_val, _ = val
        autoencoder, encoder, decoder = create_model(X_train.shape[1], encoding_dim, optimizer)
        autoencoder.fit(
            X_train,
            X_train,
            epochs=epochs,
            batch_size=batch_size,
            shuffle=True,
            validation_data=(X_val, X_val),
            verbose=1)
        autoencoders.append((autoencoder, encoder, decoder))


if __name__ == '__main__':
    main()

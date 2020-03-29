from ml_experiment.experiments import experiment, AutologgingBackend
from torch import manual_seed
import tensorflow as tf
from numpy.random import seed


@experiment(autologging_backends=[AutologgingBackend.TENSORFLOW, AutologgingBackend.KERAS, AutologgingBackend.FASTAI])
def main():
    seed(1)
    manual_seed(2)
    tf.random.set_seed(3)


if __name__ == '__main__':
    main()

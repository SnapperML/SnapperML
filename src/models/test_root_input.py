from src.utils.experiments import experiment


@experiment(optimization_metric='optimizer_test')
def main(optimizer, epochs: int):
    print(optimizer, epochs)
    yield {'optimizer_test': 10, 'epochs_test': epochs}, {}


if __name__ == '__main__':
    main()

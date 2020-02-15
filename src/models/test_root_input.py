from src.utils.experiments import experiment
from src.utils.input import DataLoader


@experiment()
def main(optimizer, epochs: int):
    yield {'optimizer_test': 10, 'epochs_test': epochs}, {}
    data_loader = DataLoader.get_instance()
    print(next(data_loader).columns)


if __name__ == '__main__':
    main()

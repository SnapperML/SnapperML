
class NoMetricSpecified(Exception):
    def __str__(self):
        return 'Optimization metric should be specified. Please, add it to the experiment decorator'


class ExperimentError(Exception):
    pass


class DataNotLoaded(Exception):
    def __str__(self):
        return 'Trying to access not loaded data. Please, add data_loader parameter to @experiment decorator'

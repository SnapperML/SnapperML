
class NoMetricSpecified(Exception):
    def __str__(self):
        return 'Optimization metric should be specified. Please, add it to the experiment decorator'


class ExperimentError(Exception):
    pass

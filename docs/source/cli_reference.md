# CLI Reference

snapper-ml CLI allows you to execute jobs from a configuration file. It can also be used to run a job without having to create a configuration file. And ultimately, it can be used to execute jobs combining input arguments with a configuration file, so those config files can work as a template. 

**Usage**:

```console
$ snapper-ml [OPTIONS] [SCRIPTS]...
```

**Options**:

* `--config_file FILE`
* `--name TEXT`: Name of the job. Overrides the config file field if specified.
* `--kind [job|experiment|group]`: Type of job. Overrides the config file field if specified.
* `--params FILE | DICT`: Job parameters. If config file is specified, these parameters In case of overlap, the values of this dictionary will take precedence over the rest
* `--param_space FILE | DICT`: Job parameter space. Only applies for groups of experiments. In case of overlap, the values of this dictionary will take precedence over the rest
* `--num_trials POSITIVE_INT`: Number of experiments to execute in parallel. Only applies for groups of experiments. Overrides the config file field if specified.
* `--timeout_per_trial POSITIVE_FLOAT`: Timeout per trial. In case of an experiment taking too long, it will be aborted.Only applies for groups of experiments. Overrides the config file field if specified.
* `--sampler [random|tpe|skopt]`: Sampler name. Only applies for groups of experiments. Overrides the config file field if specified.
* `--pruner [hyperband|sha|percentile|median]`: Pruner name. Only applies for groups of experiments. Overrides the config file field if specified.
* `--metric_key TEXT`: Name of the metric to optimize. It must be one of the keys of the metrics dictionary returned by the main function. Only applies for groups of experiments. Overrides the config file field if specified.
* `--metric_direction [minimize|maximize]`: Whether Hyperparameter Optimization Engine should minimize or maximize the given metric. Only applies for groups of experiments. Overrides the config file field if specified.
* `--docker_image TEXT`: If specified, the job will be run inside a docker contained based on the given image
* `--dockerfile FILE`
* `--docker_context DIRECTORY`: A directory to use as a docker context.Only applies when dockerfile is specified. Overrides the config file field if specified.
* `--docker_build_args FILE | DICT`: A dictionary of build arguments. Only applies when the Dockerfile is specified.
* `--ray_config FILE | DICT`: A dictionary of arguments to pass to Ray.init.Here you can specify the cluster address, number of cpu, gpu, etc. In case of overlap, the values of this dictionary will take precedence over the rest
* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

# CLI Reference

**Usage**:

```console
$ ml-experiment [OPTIONS] [SCRIPTS]...
```

**Options**:

* `--config_file FILE`
* `--name TEXT`
* `--kind [job|experiment|group]`
* `--params FILE | DICT`
* `--param_space FILE | DICT`
* `--sampler [random|tpe|skopt]`
* `--pruner [hyperband|sha|percentile|median]`
* `--num_trials POSITIVE_INT`
* `--timeout_per_trial POSITIVE_FLOAT`
* `--metric_key TEXT`
* `--metric_direction [minimize|maximize]`
* `--docker_image TEXT`
* `--docker_context DIRECTORY`
* `--docker_build_args FILE | DICT`
* `--dockerfile FILE`
* `--ray_config FILE | DICT`
* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

#!/usr/bin/env bash

file=source/cli_reference.md

typer ../ml_experiment/scripts/run_experiment.py utils docs \
  --output ${file} \
  --name="ml-experiment"

# Replace first line by the corresponding header
header="# CLI Reference"
content=$(tail -n +2 ${file})
echo "$header" > ${file}
echo "$content" >> ${file}

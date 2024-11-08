#!/usr/bin/env bash
mlflow server -h 0.0.0.0 -p ${MLFLOW_PORT:-'5000'} \
    --default-artifact-root=${MLFLOW_ARTIFACT_STORE:-'./mlruns'}

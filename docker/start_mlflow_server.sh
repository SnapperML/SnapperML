#!/usr/bin/env bash
mlflow server -h 0.0.0.0 -p ${MLFLOW_PORT:-'5000'} \
    --backend-store-uri="mysql+pymysql://${MYSQL_USER}:${MYSQL_PASSWORD}@mlflow_storage:${MYSQL_PORT:-3306}/${MYSQL_DATABASE}" \
    --default-artifact-root=${MLFLOW_ARTIFACT_STORE:-'./mlruns'}

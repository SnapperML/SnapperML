#!/usr/bin/env bash
bash -c "./docker/wait-for mlflow_storage:${MYSQL_PORT:-3306} -- ./docker/start_mlflow_server.sh && /bin/bash"
#!/usr/bin/env bash
bash -c "./wait-for mlflow_storage:${MYSQL_PORT:-3306} -- ./start_mlflow_server.sh && /bin/bash"

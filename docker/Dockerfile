FROM python:3.7

WORKDIR /app

COPY start_mlflow_server.sh .
COPY wait-for .

RUN  pip install mlflow

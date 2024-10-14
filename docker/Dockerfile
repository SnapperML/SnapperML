FROM python:3.12

WORKDIR /app

COPY start_mlflow_server.sh .
COPY wait-for .
COPY .envdocker .

RUN pip install mlflow pymysql mysqlclient cryptography
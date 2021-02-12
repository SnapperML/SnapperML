FROM python:3.7

WORKDIR /app

COPY myentrypoint.sh .
COPY start_mlflow_server.sh .
COPY wait-for .

RUN pip install pymysql
RUN  pip install mlflow

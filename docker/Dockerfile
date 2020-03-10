FROM continuumio/miniconda3
ADD requirements.txt /build/requirements.txt
WORKDIR /build/
RUN apt-get update && apt-get install -y libpq-dev && pip install -r requirements.txt
WORKDIR /mnt/

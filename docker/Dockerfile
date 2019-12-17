FROM continuumio/miniconda3
ADD requirements.txt /build/requirements.txt
WORKDIR /build/
RUN pip install -r requirements.txt
WORKDIR /mnt/

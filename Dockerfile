FROM ufoym/deepo:cpu

ADD docker/requirements.txt /build/requirements.txt
ADD ml_experiment /build/ml_experiment
ADD setup.py /build/setup.py
ADD README.md /build/README.md

WORKDIR /build/

RUN  pip install --upgrade pip && pip install -e .

WORKDIR /mnt/

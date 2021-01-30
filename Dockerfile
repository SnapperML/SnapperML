FROM ufoym/deepo:cpu

ADD docker/requirements.txt /build/requirements.txt
ADD snapper_ml /build/ml_experiment
ADD setup.py /build/setup.py
ADD README.md /build/README.md

WORKDIR /build/
RUN  /usr/bin/python3 -m pip install --upgrade pip
RUN  pip uninstall -y enum34
RUN  pip install -e .

WORKDIR /mnt/

FROM ufoym/deepo:cpu

ADD docker/requirements.txt /build/requirements.txt
ADD snapper_ml /build/ml_experiment
ADD setup.py /build/setup.py
ADD README.md /build/README.md

WORKDIR /build/
RUN apt update
RUN  apt install -y python3.9
RUN  /usr/bin/python3 -m pip install --upgrade pip
RUN  pip3 uninstall -y enum34
RUN  pip3 install -e .

WORKDIR /mnt/

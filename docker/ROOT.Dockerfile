# Intermediate image for private repository
# cloning without leaking the ssh private key
FROM alpine/git as intermediate

ARG LATTES_REPO_ACCESS_TOKEN
WORKDIR /
RUN mkdir /root/.ssh/  \
    && git config --global http.sslVerify false \
    && git clone https://oauth2:${LATTES_REPO_ACCESS_TOKEN}@git02.ncg.ingrid.pt/LATTES/LATTESsim.git


FROM rootproject/root

COPY --from=intermediate /LATTESsim /LATTESsim
RUN python3 -m pip install numpy pandas rootpy
WORKDIR /LATTESsim
RUN git checkout newconcept && make

ENTRYPOINT ["/bin/bash"]

# Intermediate image for private repository
# cloning without leaking the ssh private key
FROM alpine/git as intermediate

ARG SSH_PRIVATE_KEY
WORKDIR /
RUN mkdir /root/.ssh/  \
    && echo "${SSH_PRIVATE_KEY}" > /root/.ssh/id_rsa \
    && chmod 400 /root/.ssh/id_rsa \
    && ssh-keyscan git02.ncg.ingrid.pt >> /root/.ssh/known_hosts \
    && git clone git@git02.ncg.ingrid.pt:LATTES/LATTESsim.git


FROM rootproject/root

COPY --from=intermediate /LATTESsim /LATTESsim
RUN python3 -m pip install numpy pandas rootpy
WORKDIR /LATTESsim
RUN make

ENTRYPOINT ["/bin/bash"]

FROM python:3.9.6-alpine3.14

RUN apk update && \
    apk add ca-certificates && \
    apk add --no-cache build-base \
        openssl

COPY build/dist/*.whl /tmp/files/

RUN pip3 install /tmp/files/*.whl
    #rm -rf /tmp/files

ARG CONNECT_CERT_PATH_BUILD_ARG="./conf"

# install certificates
# copy certificates and keys
WORKDIR /usr/local/share/ca-certificates/
COPY $CONNECT_CERT_PATH_BUILD_ARG/*.pem ./
RUN chmod 644 *.pem
RUN update-ca-certificates

# configure a user
RUN addgroup -S lfh && adduser -S lfh -G lfh -h /home/lfh

WORKDIR /home/lfh/app
RUN mkdir config && \
    chown -R lfh:lfh /home/lfh/app

# copy config files
COPY --chown=lfh:lfh $CONNECT_CERT_PATH_BUILD_ARG/nats-server.nk ./conf/
COPY --chown=lfh:lfh $CONNECT_CERT_PATH_BUILD_ARG/*.pem ./conf/

CMD ["python3", "-m", "hl7_listener.main"]

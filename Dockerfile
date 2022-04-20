#docker build -t yankchina/logviewer_websocket .
FROM python:3.9.6-slim

LABEL maintainer="yankchina@gmail.com"
LABEL version="1.0"

ENTRYPOINT []

WORKDIR /home

# replace shell with bash so we can source files
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

COPY ./requirements.txt /home/
COPY ./server.py /home/
RUN pip3 install -r /home/requirements.txt

EXPOSE 8765
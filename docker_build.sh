#!/bin/bash -e
maintainer=yankchina
image_name=logviewer_websocket
tag=1.0
docker build -t $maintainer/$image_name:$tag .

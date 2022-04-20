#!/bin/bash -e
maintainer=yankchina
image_name=logviewer_websocket
tag=1.0
docker_image_name=$maintainer/$image_name:$tag
echo $1
docker stop $1 && docker rm $1
docker rmi $docker_image_name
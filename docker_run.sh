#/bin/bash -e
container_name=logviewer_websocket
docker_image_name=yankchina/wsmonitor:1.0
docker run -it --name $container_name -p 8765:8765 $docker_image_name  /bin/bash

# logviewer with Websocket

## Setup

```
$ python -m venv .virtualenv
$ ./ve pip install -r requirements.txt
```

Or Using Docker

```
## build docker image
bash ./docker_build.sh
## run container with the docker image 
bash ./docker_run.sh
```

## Demo

### Start WebSocket server

```
$ python server.py -h
usage: server.py [-h] [--host HOST] [--port PORT] --prefix PREFIX

optional arguments:
  -h, --help       show this help message and exit
  --host HOST
  --port PORT
  --prefix PREFIX  Allowed directories

$ python server.py --host 127.0.0.1 --port 8765 --prefix /tmp/ --prefix /tmp/dir1

## In Docker You will change up commandline with 

$ python server.py --host 0.0.0.0 --port 8765 --prefix /tmp/

```

### Start demo client

```
$ ./ve python -m http.server
```

Create `/tmp/demo.log` file and browse `http://localhost:8000/demo.html`, you will see the content of the log file. Append logs to this file and the content will be shown in browser immediately.

# -*- coding: utf-8 -*-

import os.path
import asyncio
import logging
import argparse
import websockets
from collections import deque
from urllib.parse import urlparse, parse_qs
from tailer import Tailer


# init
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)
allowed_prefixes = []

@asyncio.coroutine
def view_log(websocket, path):

    logging.info('Connected, remote={}, path={}'.format(websocket.remote_address, path))

    try:
        try:
            parse_result = urlparse(path)
        except Exception:
            raise ValueError('URL不正确')

        file_path = os.path.abspath(parse_result.path)
        allowed = False
        for prefix in allowed_prefixes:
            if file_path.startswith(prefix):
                allowed = True
                break
        if not allowed:
            raise ValueError('无权访问文件')

        if not os.path.isfile(file_path):
            raise ValueError('文件不存在')

        query = parse_qs(parse_result.query)
        tail = query and query['tail'] and is_true(query['tail'][0])

        with open(file_path) as f:

            lines = deque(f, 1000)
            yield from websocket.send(''.join(lines))
            del lines

            if tail:
                for line in Tailer(f).follow():
                    yield from websocket.send(line)
                    yield from asyncio.sleep(1)
            else:
                yield from websocket.close()

    except ValueError as e:
        try:
            yield from websocket.send(str(e))
            yield from websocket.close()
        except Exception:
            pass

        log_close(websocket, path, e)

    except Exception as e:
        log_close(websocket, path, e)

    else:
        log_close(websocket, path)

def log_close(websocket, path, exception=None):
    message = 'Closed, remote={}, path={}'.format(websocket.remote_address, path)
    if exception is not None:
        message += ', exception={}'.format(exception)
        logging.warn(message)
    else:
        logging.info(message)

def is_true(value):
    return isinstance(value, str) and value.lower() in ('true', '1', 'yes')

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=8765)
    parser.add_argument('--prefix', required=True, action='append', help='Allowed directories')
    args = parser.parse_args()

    allowed_prefixes.extend(args.prefix)
    start_server = websockets.serve(view_log, args.host, args.port)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    main()

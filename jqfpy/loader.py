import json
from json.decoder import WHITESPACE
from collections import deque


def load(stream, *, buffered=False):
    if buffered:
        return _load_buffered(stream)
    else:
        return _load_unbuffered(stream)


def _load_unbuffered(stream):
    buf = deque([], maxlen=100)
    first_err = None

    decoder = json.JSONDecoder()

    for line in stream:
        buf.append(line)
        try:
            body = "".join(buf)
            if len(body.strip()) > 0:
                idx = WHITESPACE.match(body).end()
                ob, end = decoder.raw_decode(body, idx)
                first_err = None
                yield ob
                buf.clear()
                buf.append(body[end:])
        except json.JSONDecodeError as e:
            if first_err is None:
                first_err = e

    if first_err is not None:
        raise first_err


def _load_buffered(stream):
    s = stream.read()
    size = len(s)
    decoder = json.JSONDecoder()

    end = 0
    while True:
        idx = WHITESPACE.match(s[end:]).end()
        i = end + idx
        if i >= size:
            break
        ob, end = decoder.raw_decode(s, i)
        yield ob

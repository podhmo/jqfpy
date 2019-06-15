import json
from json.decoder import WHITESPACE
from collections import deque, OrderedDict

try:
    from json import JSONDecodeError
except ImportError:
    JSONDecodeError = ValueError  # for 3.4
from .rec import consume_rec


def load(stream, *, buffered=False):
    if buffered:
        return _load_buffered(stream)
    else:
        return _load_unbuffered(stream)


def _load_unbuffered(stream):
    buf = deque([], maxlen=100)
    first_err = None

    decoder = json.JSONDecoder(object_pairs_hook=OrderedDict)

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
        except JSONDecodeError as e:
            if first_err is None:
                first_err = e

    if first_err is not None:
        raise first_err


def _load_buffered(stream):
    s = stream.read()
    size = len(s)
    decoder = json.JSONDecoder(object_pairs_hook=OrderedDict)

    end = 0
    while True:
        idx = WHITESPACE.match(s[end:]).end()
        i = end + idx
        if i >= size:
            break
        ob, end = decoder.raw_decode(s, i)
        yield ob


def dump(d, fp, *, ignore_none=False, squash_level=0, raw=False, extra_kwargs=None):
    opts = extra_kwargs or dict(sort_keys=False, ensure_ascii=False)

    def _dump(d):
        if ignore_none and d is None:
            return
        elif raw and isinstance(d, str):
            print(d, file=fp)
        else:
            json.dump(d, fp=fp, **opts)
            print(file=fp)

    consume_rec(d, _dump, n=squash_level)

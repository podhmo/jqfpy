import json
from json.decoder import WHITESPACE


def load(stream, *, slurp=False):
    return loads(stream.read(), slurp=slurp)


def loads(s, *, slurp=False):
    if slurp:
        return list(loads_slurp_iter(s))
    else:
        return json.loads(s)


def loads_slurp_iter(s):
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

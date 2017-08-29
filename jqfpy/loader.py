import json
from json.decoder import WHITESPACE
from collections import deque


def load(stream):
    buf = deque([], maxlen=100)
    for line in stream:
        buf.append(line)
        try:
            d = json.loads("\n".join(buf))
        except json.JSONDecodeError as e:
            pass
        else:
            yield d
            buf.clear()


# def loads(s, *, slurp=False):
#     if not slurp:
#         yield json.loads(s)
#     else:
#         size = len(s)
#         decoder = json.JSONDecoder()

#         end = 0
#         while True:
#             idx = WHITESPACE.match(s[end:]).end()
#             i = end + idx
#             if i >= size:
#                 break
#             ob, end = decoder.raw_decode(s, i)
#             yield ob

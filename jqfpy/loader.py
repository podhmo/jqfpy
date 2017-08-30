import json
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

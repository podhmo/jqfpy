import json
from collections import deque


def load(stream):
    buf = deque([], maxlen=100)
    first_err = None

    for line in stream:
        buf.append(line)
        try:
            d = json.loads("\n".join(buf))
        except json.JSONDecodeError as e:
            if first_err is None:
                first_err = e
        else:
            first_err = None
            yield d
            buf.clear()

    if first_err is not None:
        raise first_err

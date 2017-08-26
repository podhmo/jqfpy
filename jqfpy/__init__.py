import sys
import random
import json

missing = object()


class Getter:
    def __init__(self, d, sep="/"):
        self.d = d
        self.sep = sep

    def get(self, k=None, d=None, default=None):
        d = d or self.d
        if k is None:
            return d
        ks = k.split(self.sep)
        for k in ks:
            if k.isdecimal():
                k = int(k)
                try:
                    d = d[k]
                except IndexError:
                    return default
            else:
                d = d.get(k, missing)
                if d is missing:
                    return default
        return d


def transform(d, code):
    lines = [line.strip() for line in code.split(";")]
    rmarker = "r{}".format(str(random.random())[2:])
    lines[-1] = "{} = {}".format(rmarker, lines[-1])
    pycode = "\n".join(lines)

    env = {rmarker: {}, "get": Getter(d).get}
    exec(pycode, env)

    return env[rmarker]


def run(stream, code, *, squash=False):
    d = json.load(stream)
    r = transform(d, code)
    if squash:
        for line in r:
            json.dump(line, sys.stdout, indent=2, ensure_ascii=False)
            print()
    else:
        json.dump(r, sys.stdout, indent=2, ensure_ascii=False)
        print()

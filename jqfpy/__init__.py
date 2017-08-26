import random

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


def create_rvalname():
    return "r{}".format(str(random.random())[2:])


def create_pycode(code, rvalname):
    lines = [line.strip() for line in code.split(";")]
    lines[-1] = "{} = {}".format(rvalname, lines[-1])
    pycode = "\n".join(lines)
    return pycode


def exec_pycode(d, pycode, rvalname):
    env = {rvalname: {}, "get": Getter(d).get}
    exec(pycode, env)
    return env[rvalname]

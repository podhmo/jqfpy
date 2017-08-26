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


def create_pycode(fnname, code):
    lines = ["def {}(get):".format(fnname)]
    lines.extend([line.strip() for line in code.split(";")])
    lines[-1] = "return {}".format(lines[-1])
    pycode = "\n    ".join(lines)
    return pycode


def exec_pycode(fnname, pycode):
    env = {}
    exec(pycode, env)
    return env[fnname]


def transform(fn, d):
    return fn(Getter(d).get)

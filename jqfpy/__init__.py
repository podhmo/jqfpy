from jqfpy.helpermodule import HelperModule
from jqfpy.accessor import Accessor


class Getter:
    def __init__(self, d, accessor=Accessor()):
        self.d = d
        self.accessor = accessor

    def get(self, k=None, d=None, default=None):
        d = d or self.d
        if k is None:
            return d
        access_keys = self.accessor.split_key(k)
        return self.accessor.access(access_keys, d, default)

    __call__ = get


def create_pycode(fnname, code):
    lines = ["def {}(get, h=None):".format(fnname)]
    lines.extend([line.strip() for line in code.split(";")])
    lines[-1] = "return {}".format(lines[-1])
    pycode = "\n    ".join(lines)
    return pycode


def exec_pycode(fnname, pycode):
    env = {}
    exec(pycode, env)
    return env[fnname]


def transform(fn, d):
    getter = Getter(d)
    return fn(getter, h=HelperModule(getter))

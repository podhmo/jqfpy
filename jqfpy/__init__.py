from jqfpy.helpermodule import HelperModule, Context
from jqfpy.accessor import Accessor


class Getter:
    def __init__(self, d, *, accessor=Accessor()):
        self.d = d
        self.accessor = accessor

    def get(self, k=None, d=None, default=None):
        d = d or self.d
        if k is None:
            return d
        access_keys = self.accessor.split_key(k)
        if access_keys and access_keys[0] == "[]":
            rest_keys = access_keys[1:]
            return [self.accessor.access(rest_keys, x, default) for x in d]
        else:
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


def create_context(*, here=None, extra_kwargs=None) -> Context:
    return Context(here=here, dump_extra_kwargs=extra_kwargs)


def transform(ctx, fn, d, *, additionals=None):
    getter = Getter(d)
    h = HelperModule(ctx, getter, additionals=additionals)
    return fn(getter, h=h)

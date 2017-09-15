from jqfpy.helpermodule import HelperModule
from jqfpy.accessor import Accessor


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
    accessor = Accessor(d)
    return fn(accessor, h=HelperModule(accessor))

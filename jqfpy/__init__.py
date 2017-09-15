from jqfpy.helpermodule import HelperModule

missing = object()


class Accessor:
    def __init__(self, d):
        self.d = d

    def _split_key(self, k, *, sep="/"):
        return [normalize_json_pointer(x) for x in k.split(sep)]

    def _split_key_pair(self, k, *, sep="@"):
        if sep not in k:
            return self._split_key(k), []
        else:
            access_keys, build_keys = k.split(sep, 1)
            return self._split_key(access_keys), self._split_key(build_keys)

    def get(self, k=None, d=None, default=None):
        d = d or self.d
        if k is None:
            return d
        _, _, v = self.access(k, d, default)
        return v

    __call__ = get

    def access(self, k, d, default=None):
        access_keys, build_keys = self._split_key_pair(k)
        for k in access_keys:
            if k.isdecimal():
                k = int(k)
                try:
                    d = d[k]
                except IndexError:
                    return access_keys, build_keys, default
            else:
                d = d.get(k, missing)
                if d is missing:
                    return access_keys, build_keys, default
        return access_keys, build_keys, d


def normalize_json_pointer(ref):
    if "~" not in ref:
        return ref
    return ref.replace("~1", "/").replace("~0", "~")


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

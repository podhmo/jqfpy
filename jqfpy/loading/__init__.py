import os.path
import sys


class Repository:
    def __init__(self):
        self.mapping = {}
        self._cached = {}
        self.factories = {}

    def register(self, *exts):
        def _register(fn):
            self.factories[fn.__name__] = fn
            for ext in exts:
                self.mapping[ext] = fn.__name__
            return fn

        return _register

    def lookup(self, name):
        m = self._cached.get(name)
        if m is None:
            m = self._cached[name] = self.factories[name]()
        return m

    def lookup_by_extname(self, extname):
        return self.lookup(self.mapping[extname])


class Dispatcher:
    def __init__(self, repository):
        self.repository = repository

    def dispatch(self, stream, *, default_format="json"):
        return self._lookup(stream, default_format)

    def _lookup(self, stream, default):
        filename = get_filepath_from_stream(stream)
        ext = os.path.splitext(filename)[1]
        try:
            return self.repository.lookup_by_extname(ext)
        except KeyError:
            return self.repository.lookup(default)


_repo = Repository()


@_repo.register(".txt", ".raw")
def raw():
    from . import _raw as m

    m.SEPARATOR = None
    return m


@_repo.register(".json", ".js")
def json():
    from . import _json as m

    m.SEPARATOR = None
    return m


@_repo.register(".yaml", ".yml")
def yaml():
    try:
        from . import _yaml as m

        m.SEPARATOR = "---\n"
    except ImportError:
        fp = sys.stderr
        print(
            "\x1b[33m\x1b[1myaml module is not found. please install via \n  pip install 'jqfpy[yaml]'\x1b[0m",
            file=fp,
        )
        sys.exit(1)
    return m


@_repo.register(".ltsv")
def ltsv():
    from . import _ltsv as m

    m.SEPARATOR = None
    return m


register = _repo.register
get_module = Dispatcher(_repo).dispatch


def get_filepath_from_stream(stream):
    return getattr(stream, "name", "")

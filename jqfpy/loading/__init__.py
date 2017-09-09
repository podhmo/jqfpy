import os.path


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
        filename = getattr(stream, "name", "")
        ext = os.path.splitext(filename)[1]
        try:
            return self.repository.lookup_by_extname(ext)
        except KeyError:
            return self.repository.lookup(default)


_repo = Repository()


@_repo.register(".json", ".js")
def json():
    from . import _json as m
    m.SEPARATOR = None
    return m


@_repo.register(".yaml", ".yml")
def yaml():
    from . import _yaml as m
    m.SEPARATOR = "---\n"
    return m


register = _repo.register
get_module = Dispatcher(_repo).dispatch

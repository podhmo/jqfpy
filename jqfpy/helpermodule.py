from collections import OrderedDict


# todo: dynamic loading via option
class HelperModule:
    def __init__(self, getter, *, factory=OrderedDict):
        self.getter = getter
        self.factory = factory

    @property
    def d(self):
        return self.getter.d

    # todo: nested

    def pick(self, ks, *, d=None, default=None):
        d = d or self.d
        return self.factory((k, d.get(k, default)) for k in ks)

    def omit(self, ks, *, d=None):
        d = d or self.d
        return self.factory((k, d[k]) for k in list(d.keys()) if k not in ks)

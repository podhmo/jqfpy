from collections import OrderedDict


# todo: dynamic loading via option
class HelperModule:
    def __init__(self, getter, *, factory=OrderedDict):
        self.getter = getter
        self.factory = factory

    @property
    def d(self):
        return self.getter.d

    def _make_dict(self, items):
        items = list(items)
        d = self.factory()
        for raw_k, v in items:
            cursor = d
            ks = self.getter.split_keys(raw_k)
            for k in ks[:-1]:
                if k not in cursor:
                    cursor[k] = self.factory()
                cursor = cursor[k]
            cursor[ks[-1]] = v
        return d

    def pick(self, ks, *, d=None, default=None):
        d = d or self.d
        return self._make_dict((k, self.getter.get(k, d=d, default=default)) for k in ks)

    def omit(self, ks, *, d=None):
        d = d or self.d
        return self._make_dict((k, self.getter.get(k, d=d)) for k in list(d.keys()) if k not in ks)

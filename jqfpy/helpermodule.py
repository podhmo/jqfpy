from collections import OrderedDict


# todo: dynamic loading via option
class HelperModule:
    def __init__(self, accessor, *, factory=OrderedDict):
        self.accessor = accessor
        self.factory = factory

    @property
    def d(self):
        return self.accessor.d

    def _make_dict(self, triples):
        d = self.factory()
        for access_keys, build_keys, v in triples:
            cursor = d
            if not build_keys:
                build_keys = access_keys

            for k in build_keys[:-1]:
                if k not in cursor:
                    cursor[k] = self.factory()
                cursor = cursor[k]
            cursor[build_keys[-1]] = v
        return d

    def pick(self, ks, *, d=None, default=None):
        d = d or self.d
        return self._make_dict(self.accessor.access(k, d=d, default=default) for k in ks)

    def omit(self, ks, *, d=None):
        d = d or self.d
        return self._make_dict(self.accessor.access(k, d=d) for k in list(d.keys()) if k not in ks)

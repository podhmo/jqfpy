from collections import OrderedDict
from . import _tree as tree


# todo: dynamic loading via option
class HelperModule:
    def __init__(self, getter, *, factory=OrderedDict):
        self.getter = getter
        self.accessor = getter.accessor  # xxx
        self.factory = factory

    @property
    def d(self):
        return self.getter.d

    def _build_dict(self, triples):
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

    def pick(self, *ks, d=None, default=None):
        d = d or self.d
        return self._build_dict(self._pick_gen(ks, d, default))

    def _pick_gen(self, ks, d, default):
        d = d or self.d
        for k in ks:
            access_keys, build_keys = self.accessor.split_key_pair(k)
            yield access_keys, build_keys, self.accessor.access(access_keys, d, default=default)

    def omit(self, *ks, d=None):
        d = d or self.d
        t = tree.build_tree([self.accessor.split_key(k) for k in ks])
        return self._build_dict(self._omit_gen(d, t, []))

    def _omit_gen(self, d, t, hist):
        for k in d.keys():
            if k in t:
                hist.append(k)
                yield from self._omit_gen(d[k], t.children[k], hist=hist)
                hist.pop()
            elif k in t.leafs:
                continue
            else:
                hist.append(k)
                yield hist[:], [], d[k]
                hist.pop()

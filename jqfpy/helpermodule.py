from collections import OrderedDict
from . import _tree as tree


# todo: dynamic loading via option
class HelperModule:
    def __init__(self, accessor, *, factory=OrderedDict):
        self.accessor = accessor
        self.factory = factory

    @property
    def d(self):
        return self.accessor.d

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

    def pick(self, ks, *, d=None, default=None):
        d = d or self.d
        return self._build_dict(self.accessor.access(k, d=d, default=default) for k in ks)

    def omit(self, ks, *, d=None):
        d = d or self.d
        access_keys_list = []
        for k in ks:
            access_keys, _ = self.accessor.get_keys_pair(k)
            access_keys_list.append(access_keys)

        t = tree.build_tree(access_keys_list)
        return self._build_dict(self._omit_access(d, t, []))

    def _omit_access(self, d, t, hist):
        for k in d.keys():
            if k in t:
                hist.append(k)
                yield from self._omit_access(d[k], t.children[k], hist=hist)
                hist.pop()
            elif k in t.leafs:
                continue
            else:
                hist.append(k)
                yield hist[:], [], d[k]
                hist.pop()

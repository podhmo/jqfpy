import sys
import itertools
from collections import OrderedDict
from . import accessor
from . import _tree as tree


# todo: dynamic loading via option
class HelperModule:
    def __init__(self, getter, *, factory=OrderedDict, additionals=None, dump=None):
        self.getter = getter
        self.accessor = getter.accessor  # xxx
        self.factory = factory
        self.additionals = additionals
        self.dump = dump or self._dump_default

    def __getattr__(self, k):
        if self.additionals is None:
            raise AttributeError(k)
        return getattr(self.additionals, k)

    @property
    def d(self):
        return self.getter.d

    def dumpfile(self, filename, data):
        with open(filename, "w") as wf:
            self.dump(data, fp=wf)

    def _dump_default(self, data, fp=sys.stdout):
        print(data, file=fp)

    def pick(self, *ks, d=None, default=None):
        d = d or self.d
        return pick(
            d, ks, default=default, factory=self.factory, accessor=self.accessor
        )

    def omit(self, *ks, d=None):
        d = d or self.d
        return omit(d, ks, factory=self.factory, accessor=self.accessor)

    def flatten(self, L, *, n):
        for _ in range(n):
            L = flatten1(L)
        return L

    def flatten1(self, L):
        return flatten1(L)

    def chunk(self, L, *, n):
        return list(chunk(L, n=n))


def _build_dict(triples, *, factory):
    d = factory()
    for access_keys, build_keys, v in triples:
        cursor = d
        if not build_keys:
            build_keys = access_keys

        for k in build_keys[:-1]:
            if k not in cursor:
                cursor[k] = factory()
            cursor = cursor[k]
        cursor[build_keys[-1]] = v
    return d


def pick(d, ks, *, default=None, factory=OrderedDict, accessor=accessor.Accessor()):
    gen = _pick_gen(d, ks, default=default, accessor=accessor)
    return _build_dict(gen, factory=factory)


def _pick_gen(d, ks, *, default, accessor):
    for k in ks:
        access_keys, build_keys = accessor.split_key_pair(k)
        yield access_keys, build_keys, accessor.access(access_keys, d, default=default)


def omit(d, ks, *, factory=OrderedDict, accessor=accessor.Accessor()):
    t = tree.build_tree([accessor.split_key(k) for k in ks])
    gen = _omit_gen(d, t, [])
    return _build_dict(gen, factory=factory)


def _omit_gen(d, t, hist):
    for k in d.keys():
        if k in t:
            hist.append(k)
            yield from _omit_gen(d[k], t.children[k], hist=hist)
            hist.pop()
        elif k in t.leafs:
            continue
        else:
            hist.append(k)
            yield hist[:], [], d[k]
            hist.pop()


def flatten1(L):
    return list(itertools.chain.from_iterable(L))


def chunk(iterable, n):
    it = iter(iterable)
    while True:
        chunk_it = itertools.islice(it, n)
        try:
            first_el = next(chunk_it)
        except StopIteration:
            return
        yield tuple(itertools.chain((first_el,), chunk_it))

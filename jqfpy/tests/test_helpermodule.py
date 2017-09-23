import unittest


class HelperModuleTests(unittest.TestCase):
    def _getTarget(self):
        from jqfpy.helpermodule import HelperModule
        return HelperModule

    def _makeOne(self, d, *, factory):
        from jqfpy import Getter
        return self._getTarget()(Getter(d), factory=factory)

    def test_pick(self):
        d = {
            "a": 1,
            "b": 2,
            "c": 3,
            "d": 4,
            "e": 5,
            "x": {"y0": {"z00": 10, "z01": 11}, "y1": {"z10": 100, "z11": 101}}
        }

        candidates = [
            (["a"], {"a": 1}),
            (["a", "c", "e"], {"a": 1, "c": 3, "e": 5}),
            (["x"], {"x": {"y0": {"z00": 10, "z01": 11}, "y1": {"z10": 100, "z11": 101}}}),
            (["x/y0"], {"x": {"y0": {"z00": 10, "z01": 11}}}),
            (["x/y0/z00"], {"x": {"y0": {"z00": 10}}}),
            (["x/y0/z00", "x/y1/z10"], {"x": {"y0": {"z00": 10}, "y1": {"z10": 100}}}),
            (["x/y0/z00@z0", "x/y1/z11@z1"], {"z0": 10, "z1": 101}),
            (["x/y0@y0", "x/y1@y1"], {"y0": {"z00": 10, "z01": 11}, "y1": {"z10": 100, "z11": 101}}),
            (["x/y0/z00@y/z0", "x/y1/z11@y/z1"], {"y": {"z0": 10, "z1": 101}}),
        ]
        for keys, expected in candidates:
            with self.subTest(keys=keys):
                target = self._makeOne(d, factory=dict)
                got = target.pick(*keys)
                self.assertEqual(got, expected)

    def test_omit(self):
        d = {
            "a": 1,
            "b": 2,
            "c": 3,
            "d": 4,
            "e": 5,
            "x": {"y0": {"z00": 10, "z01": 11}, "y1": {"z10": 100, "z11": 101}}
        }

        candidates = [
            (["a", "x"], {"b": 2, "c": 3, "d": 4, "e": 5}),
            (["a", "c", "e", "x"], {"b": 2, "d": 4}),
            (["a", "b", "c", "d", "e"], {"x": d["x"]}),
            (["a", "b", "c", "d", "e", "x/y1"], {"x": {"y0": {"z00": 10, "z01": 11}}}),
            (["a", "b", "c", "d", "e", "x/y1", "x/y2"], {"x": {"y0": {"z00": 10, "z01": 11}}}),
            (["a", "b", "c", "d", "e", "x/y1", "x/y2", "x/y0/z01"], {"x": {"y0": {"z00": 10}}}),
        ]
        for keys, expected in candidates:
            with self.subTest(keys=keys):
                target = self._makeOne(d, factory=dict)
                got = target.omit(*keys)
                self.assertEqual(got, expected)

    def test_flatten(self):
        L = [[[[[1]]]], [[[[2]]]], [[[[3, 4], [5]], [[6]]]]]
        candidates = [
            (L, 1, [[[[1]]], [[[2]]], [[[3, 4], [5]], [[6]]]]),
            (L, 2, [[[1]], [[2]], [[3, 4], [5]], [[6]]]),
            (L, 3, [[1], [2], [3, 4], [5], [6]]),
            (L, 4, [1, 2, 3, 4, 5, 6]),
        ]
        for L, n, expected in candidates:
            with self.subTest(L=L, n=n):
                target = self._makeOne(None, factory=dict)
                got = target.flatten(L, n=n)
                self.assertEqual(got, expected)

    def test_chunk(self):
        L = [1, 2, 3, 4, 5]
        candidates = [
            (L, 1, [(1, ), (2, ), (3, ), (4, ), (5,)]),
            (L, 2, [(1, 2), (3, 4), (5, )]),
            (L, 3, [(1, 2, 3), (4, 5)]),
            (L, 4, [(1, 2, 3, 4), (5, )]),
            (L, 5, [(1, 2, 3, 4, 5)]),
            (L, 6, [(1, 2, 3, 4, 5)]),
        ]
        for L, n, expected in candidates:
            with self.subTest(L=L, n=n):
                target = self._makeOne(None, factory=dict)
                got = list(target.chunk(L, n=n))
                self.assertEqual(got, expected)

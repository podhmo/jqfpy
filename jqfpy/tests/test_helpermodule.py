import unittest


class HelperModuleTests(unittest.TestCase):
    def _getTarget(self):
        from jqfpy.helpermodule import HelperModule
        return HelperModule

    def _makeOne(self, d, *, factory):
        from jqfpy import Getter
        return self._getTarget()(Getter(d))

    def test_pick(self):
        d = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}

        candidates = [
            (["a"], {"a": 1}),
            (["a", "c", "e"], {"a": 1, "c": 3, "e": 5})
            # todo nested
        ]
        for keys, expected in candidates:
            with self.subTest(keys=keys):
                target = self._makeOne(d, factory=dict)
                got = target.pick(keys)
                self.assertEqual(got, expected)

    def test_omit(self):
        d = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}

        candidates = [
            (["a"], {"b": 2, "c": 3, "d": 4, "e": 5}),
            (["a", "c", "e"], {"b": 2, "d": 4})
            # todo nested
        ]
        for keys, expected in candidates:
            with self.subTest(keys=keys):
                target = self._makeOne(d, factory=dict)
                got = target.omit(keys)
                self.assertEqual(got, expected)

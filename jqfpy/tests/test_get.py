import unittest


class GetTests(unittest.TestCase):
    def _makeOne(self, d):
        from jqfpy import Accessor
        return Accessor(d)

    def test_rootdoc(self):
        d = {"person": {"name": "foo", "age": 20}}
        target = self._makeOne(d)

        candidates = [
            ("person", d["person"]),
            ("person/name", "foo"),
            ("person/age", 20),
            (":missing", None),
        ]
        for k, expected in candidates:
            with self.subTest(k=k):
                got = target.get(k)
                self.assertEqual(got, expected)

import unittest


class GetTests(unittest.TestCase):
    def _makeOne(self, d):
        from jqfpy import Getter
        return Getter(d)

    def test_simple_get(self):
        d = {
            "person": {
                "name": "foo",
                "age": 20,
                "skills": [{
                    "name": "x"
                }, {
                    "name": "y"
                }, {
                    "name": "z"
                }],
            },
        }
        target = self._makeOne(d)

        candidates = [
            ("person", d["person"]),
            ("person/name", "foo"),
            ("person/age", 20),
            (":missing", None),
            ("person/skills", d["person"]["skills"]),
            ("person/skills/1", {"name": "y"}),
            ("person/skills/1/name", "y"),
            ("person/skills[]/name", ["x", "y", "z"]),
            ("*/age", 20),
            ("person/*", d["person"]),
            ("person/*/name", None),
            ("person/*[]/name", ["x", "y", "z"]),
        ]
        for k, expected in candidates:
            with self.subTest(k=k):
                got = target.get(k)
                self.assertEqual(got, expected)

import unittest


class GetTests(unittest.TestCase):
    def _makeOne(self, d):
        from jqfpy import Getter

        return Getter(d)

    def test_get(self):
        d = {
            "person": {
                "name": "foo",
                "age": 20,
                "skills": [{"name": "x"}, {"name": "y"}, {"name": "z"}],
            }
        }
        target = self._makeOne(d)

        candidates = [
            ("/person", d["person"]),
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
        ]
        for k, expected in candidates:
            with self.subTest(k=k):
                got = target.get(k)
                self.assertEqual(got, expected)

    def test_get2(self):
        from collections import OrderedDict

        group = OrderedDict()
        group["x"] = {"name": "X"}
        group["y"] = {"name": "Y"}
        group["z"] = {"name": "Z"}

        d = {"group": group}
        target = self._makeOne(d)

        candidates = [("group/*[]/name", ["X", "Y", "Z"])]
        for k, expected in candidates:
            with self.subTest(k=k):
                got = target.get(k)
                self.assertEqual(got, expected)

    def test_get_list(self):
        d = [
            {"name": "foo", "skills": [{"name": "x"}, {"name": "y"}, {"name": "z"}]},
            {"name": "bar", "skills": [{"name": "x"}, {"name": "y"}]},
        ]
        target = self._makeOne(d)

        candidates = [
            ("[]/name", ["foo", "bar"]),
            ("[]/skills[]/name", [["x", "y", "z"], ["x", "y"]]),
        ]
        for k, expected in candidates:
            with self.subTest(k=k):
                got = target.get(k)
                self.assertEqual(got, expected)

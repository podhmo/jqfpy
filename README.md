# jqfpy

[![Build Status](https://travis-ci.org/podhmo/jqfpy.svg?branch=master)](https://travis-ci.org/podhmo/jqfpy)

## jq is too difficult

jq is too difficult, at least for me.

For example, extracting key-name when use is true only, from below JSON data.

```json
{
  "apps": {
    "foo": {
      "use": true
    },
    "bar": {
      "use": true
    },
    "boo": {
      "use": true
    },
    "bee": {
      "use": false
    }
  }
}
```

What is jq's answer? (taking over 30 minutes, my past challenges).

```console
$ cat data.json | jq '.apps | . as $$o | keys | map(select($$o[.].use))'
[
  "bar",
  "boo",
  "foo"
]
```

If you have python's knowledge, this is tiny oneliner, isn't it?

```console
$ cat data.json | jqfpy '[k for k, opts in get("apps").items() if opts["use"]]'
[
  "foo",
  "bar",
  "boo"
]
```

(`get()` is special function, like a `json.load(sys.stdin).get`.)

## install

```console
$ pip install jqfpy
```

## how to use

### describe syntax

todo.

### tutorial

this is jqfpy version of [jq's Tutorial](https://stedolan.github.io/jq/tutorial/)

```console
$ alias jsonDATA="curl 'https://api.github.com/repos/stedolan/jq/commits?per_page=5'"
# jq.
$ jsonDATA | jq '.'
# jqfpy.
$ jsonDATA | jqfpy 'get()'
```

```console
# jq.
$ jsonDATA | jq '.[0]'
# jqfpy.
$ jsonDATA | jqfpy 'get()[0]'
```

```console
# jq.
$ jsonDATA | jq '.[0] | {message: .commit.message, name: .commit.committer.name}'
# jqfpy.
$ jsonDATA | jqfpy 'd = get()[0]; {"message": get("commit/message", d), "name": get("commit/committer/name", d)}'
# or
$ jsonDATA | jqfpy '{"message": get("0/commit/message"), "name": get("0/commit/committer/name")}'
```

```console
# jq.
$ jsonDATA | jq '.[] | {message: .commit.message, name: .commit.committer.name}'
# jqfpy.
$ jsonDATA | jqfpy --squash 'L = get(); [{"message": get("commit/message", d), "name": get("commit/committer/name", d)} for d in L]'
```

```console
# jq.
$ jsonDATA | jq '[.[] | {message: .commit.message, name: .commit.committer.name, parents: [.parents[].html_url]}]'
# jqfpy.
$ jsonDATA | 'L = get(); [{"message": get("commit/message", d), "name": get("commit/committer/name", d), "parents": [p["html_url"] for p in d["parents"]]} for d in L]'
# or (using h.pick)
$ jsonDATA | 'L = get(); [h.pick("commit/message@message", "commit/committer/name@name", "parents[]/html_url@parents", d=d) for d in L]'
```

## additionals

### other formats support

jqfpy is supporting other formats(but this is experimental feature)

- yaml
- ltsv

if you want to use yaml supported version. install via below command.

```console
$ pip install jqfpy[yaml]
```

and calling jqfpy with `--input-format,-i` option and `--output-format,-o` option.

02data.yaml

```yaml
person:
  name: foo
  age: 20
  nickname: fool
```

```console
$ cat 02data.yaml | jqfpy -i yaml 'get("person")'
{
  "name": "foo",
  "age": 20,
  "nickname": "fool"
}

$ cat 02data.yaml | jqfpy -i yaml -o ltsv 'get("person")'
name:foo	age:20	nickname:fool
```

### helper functions

helper functions are included.

- pick()
- omit()
- flatten()
- chunk()
- loadfile()
- dumpfile()

pick()

```console
$ cat 02data.yaml | jqfpy -i yaml 'h.pick("person/name", "person/age")'
{
  "person": {
    "name": "foo",
    "age": 20
  }
}

$ cat 02data.yaml | jqfpy -i yaml 'h.pick("person/name@name", "person/age@age")'
{
  "name": "foo",
  "age": 20
}
```

omit()

```console
$ cat 02data.yaml | jqfpy -i yaml 'h.omit("person/nickname")'
{
  "person": {
    "name": "foo",
    "age": 20
  }
}
```

flatten()

```console
$ seq 1 5 | jqfpy --slurp -c 'L = get(); [L, L]'
[[1, 2, 3, 4, 5], [1, 2, 3, 4, 5]]
$ seq 1 5 | jqfpy --slurp -c 'L = get(); h.flatten([L, L], n=1)'
[1, 2, 3, 4, 5, 1, 2, 3, 4, 5]
```

chunk()

```console
$ seq 1 10 | jqfpy --slurp -c 'h.chunk(get(), n=3)'
[[1, 2, 3], [4, 5, 6], [7, 8, 9], [10]]
```

loadfile()

```console
$ ls *.json
a.json b.json
$ echo '["a", "b"]' | jqfpy '{name: h.loadfile(f"{name}.json") for name in get()}'
```

`--here` and `--relative-path` options.

```console
# see ./x.json
$ jqfpy 'h.loadfile("x.json")' a/b/main.json

# see ./a/b/x.json
$ jqfpy --here a/b/ 'h.loadfile("x.json")' a/b/main.json

# see ./a/b/x.json
$ jqfpy --relative-path 'h.loadfile("x.json")' a/b/main.json
```

dumpfile()

```
$ echo {"person0.json": {"name": "foo", "age": 20}, "person1.json": {"name": "bar}} | jqfpy '[h.dumpfile(v, fname) for fname, v in get().item()]' > /dev/null
```


### individual helper module with --additionals

match.py

```python
import re


def match(rx, text):
    if text is None:
        return False
    return re.search(rx, text)
```

```console
$ cat examples/additionals/00data.json | jqfpy --additionals=./match.py '[d for d in get("constraint") if h.match("^1\..+", d.get("version"))]'
[
  {
    "name": "github.com/Masterminds/vcs",
    "version": "1.11.0"
  },
  {
    "name": "github.com/boltdb/bolt",
    "version": "1.0.0"
  }
]
```

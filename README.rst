jqfpy
========================================

.. image:: https://travis-ci.org/podhmo/jqfpy.svg?branch=master
    :target: https://travis-ci.org/podhmo/jqfpy

jq is too difficult
----------------------------------------

jq is too difficult, at least for me.

For example, extracting key-name when use is true only, from below JSON data.

.. code-block:: json

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

What is jq's answer? (taking over 30 minutes, my past challenges).

.. code-block:: console

  $ cat data.json | jq '.apps | . as $$o | keys | map(select($$o[.].use))'
  [
    "bar",
    "boo",
    "foo"
  ]

If you have python's knowledge, this is tiny oneliner, isn't it?

.. code-block:: console

  $ cat data.json | jqfpy '[k for k, opts in get("apps").items() if opts["use"]]'
  [
    "foo",
    "bar",
    "boo"
  ]

(`get()` is special function, like a `json.load(sys.stdin).get`.)

install
----------------------------------------

.. code-block:: console

  pip install jqfpy


how to use
----------------------------------------

describe syntax
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

todo.

tutorial
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

this is jqfpy version of `jq's Tutorial <https://stedolan.github.io/jq/tutorial/>`_.

.. code-block:: console

   alias jsonDATA="curl 'https://api.github.com/repos/stedolan/jq/commits?per_page=5'"
   # jq.
   jsonDATA | jq '.'
   # jqfpy.
   jsonDATA | jqfpy 'get()'

.. code-block:: console

   # jq.
   jsonDATA | jq '.[0]'
   # jqfpy.
   jsonDATA | jqfpy 'get()[0]'

.. code-block:: console

   # jq.
   jsonDATA | jq '.[0] | {message: .commit.message, name: .commit.committer.name}'
   # jqfpy.
   jsonDATA | jqfpy 'd = get()[0]; {"message": get("commit/message", d), "name": get("commit/committer/name", d)}'
   # or
   jsonDATA | jqfpy '{"message": get("0/commit/message"), "name": get("0/commit/committer/name")}'

.. code-block:: console

   # jq.
   jsonDATA | jq '.[] | {message: .commit.message, name: .commit.committer.name}'
   # jqfpy.
   jsonDATA | jqfpy --squash 'L = get(); [{"message": get("commit/message", d), "name": get("commit/committer/name", d)} for d in L]'

.. code-block:: console

   # jq.
   jsonDATA | jq '[.[] | {message: .commit.message, name: .commit.committer.name, parents: [.parents[].html_url]}]'
   # jqfpy.
   jsonDATA | 'L = get(); [{"message": get("commit/message", d), "name": get("commit/committer/name", d), "parents": [p["html_url"] for p in d["parents"]]} for d in L]'
   # or (using h.pick)
   jsonDATA | 'L = get(); [h.pick("commit/message@message", "commit/committer/name@name", "parents[]/html_url@parents", d=d) for d in L]'

additionals
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

other formats support
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

jqfpy is supporting other formats(but this is experimental feature)

- yaml
- ltsv

if you want to use yaml supported version. install via below command.

```
$ pip install jqfpy[yaml]
```

and calling jqfpy with `--input-format,-i` option and `--output-format,-o` option.

02data.yaml

.. code-block:: yaml

   person:
     name: foo
     age: 20
     nickname: fool


.. code-block:: console

   $ cat 02data.yaml | jqfpy -i yaml 'get("person")'
   {
     "name": "foo",
     "age": 20,
     "nickname": "fool"
   }

   $ cat 02data.yaml | jqfpy -i yaml -o ltsv 'get("person")'
   name:foo	age:20	nickname:fool


helper functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

helper functions are included.

- pick()
- omit()

pick()

.. code-block:: console

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

omit()

.. code-block:: console

   $ cat 02data.yaml | jqfpy -i yaml 'h.omit("person/nickname")'
   {
     "person": {
       "name": "foo",
       "age": 20
     }
   }

jqfpy
========================================

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

  $ cat data.json | jq -r '.apps | . as $$o | keys | map(select($$o[.].use))'
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

tutorial
----------------------------------------

todo

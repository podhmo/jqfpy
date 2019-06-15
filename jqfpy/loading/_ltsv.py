from collections import OrderedDict
from .rec import consume_rec


def load(stream, *, buffered=False):
    for line in stream:
        yield OrderedDict(
            pair.split(":", 1) for pair in line.rstrip("\n\r").split("\t")
        )


def dump(d, fp, *, ignore_none=False, squash_level=0, raw=False, extra_kwargs=None):
    opts = extra_kwargs or dict(sort_keys=False, ensure_ascii=False)

    def _dump(d):
        if d is None:
            return
        elif raw and isinstance(d, str):
            print(d, file=fp)
        else:
            if opts.get("sort_keys", False):
                items = sorted(d.items(), key=lambda pair: pair[0])
            else:
                items = d.items()
            print("\t".join("{}:{}".format(k, v) for k, v in items), file=fp)

    consume_rec(d, _dump, n=squash_level)

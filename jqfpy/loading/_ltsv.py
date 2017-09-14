from collections import OrderedDict


def load(stream, *, buffered=False):
    for line in stream:
        yield OrderedDict(pair.split(":", 1) for pair in line.rstrip("\n\r").split("\t"))


def dump(d, fp, *, squash=False, raw=False, extra_kwargs=None):
    opts = extra_kwargs or dict(sort_keys=False, ensure_ascii=False)

    def _dump(d):
        if raw and isinstance(d, str):
            print(d, file=fp)
        else:
            if opts.get("sort_keys", False):
                items = sorted(d.items(), key=lambda pair: pair[0])
            else:
                items = d.items()
            print("\t".join("{}:{}".format(k, v) for k, v in items), file=fp)

    if squash:
        for line in d:
            _dump(line)
    else:
        _dump(d)

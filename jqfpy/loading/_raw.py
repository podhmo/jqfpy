from .rec import consume_rec


def load(stream, *, buffered=False):
    if buffered:
        return _load_buffered(stream)
    else:
        return _load_unbuffered(stream)


def _load_buffered(stream):
    return [s.rstrip() for s in stream]


def _load_unbuffered(stream):
    # unbuffered
    return (s.rstrip() for s in stream)


def dump(d, fp, *, squash_level=0, raw=False, extra_kwargs=None):
    def _dump(d):
        if raw:
            print(d, file=fp)
        else:
            print(repr(d), file=fp)

    consume_rec(d, _dump, n=squash_level)

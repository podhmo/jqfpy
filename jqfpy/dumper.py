import json


def dump(
    d,
    fp,
    *,
    squash=False,
    compact=False,
    raw=False,
    json_kwargs=None,
):
    opts = json_kwargs or dict(sort_keys=False, ensure_ascii=False)
    if not compact:
        opts["indent"] = 2

    def _dump(d):
        if raw and isinstance(d, str):
            print(d)
        else:
            json.dump(d, fp=fp, **opts)
            print(file=fp)

    if squash:
        for line in d:
            _dump(line)
    else:
        _dump(d)

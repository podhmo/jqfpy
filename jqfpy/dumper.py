import json


def dump(d, fp, *, squash=False, compact=False):
    opts = {"ensure_ascii": False}
    if not compact:
        opts["indent"] = 2

    if squash:
        for line in d:
            json.dump(line, fp=fp, **opts)
            print(file=fp)
    else:
        json.dump(d, fp=fp, **opts)
        print(file=fp)

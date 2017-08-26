import json


def dump(d, fp, *, squash=False, compact=False, sort_keys=False, ensure_ascii=False):
    opts = {"ensure_ascii": ensure_ascii, "sort_keys": sort_keys}
    if not compact:
        opts["indent"] = 2

    if squash:
        for line in d:
            json.dump(line, fp=fp, **opts)
            print(file=fp)
    else:
        json.dump(d, fp=fp, **opts)
        print(file=fp)

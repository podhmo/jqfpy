missing = object()


class Accessor:
    def split_key(self, k, *, sep="/"):
        return [normalize_json_pointer(x) for x in k.split(sep)]

    def split_key_pair(self, k, *, sep="@"):
        if sep not in k:
            return self.split_key(k), []
        else:
            access_keys, build_keys = k.split(sep, 1)
            return self.split_key(access_keys), self.split_key(build_keys)

    def access(self, access_keys, d, default=None):
        for k in access_keys:
            if k.isdecimal():
                k = int(k)
                try:
                    d = d[k]
                except IndexError:
                    return default
            else:
                d = d.get(k, missing)
                if d is missing:
                    return default
        return d


def normalize_json_pointer(ref):
    if "~" not in ref:
        return ref
    return ref.replace("~1", "/").replace("~0", "~")

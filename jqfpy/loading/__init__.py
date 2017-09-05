def get_module(fmt):
    if fmt == "yaml":
        from . import _yaml
        return _yaml
    else:
        from . import _json
        return _json

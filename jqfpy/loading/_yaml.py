import re
from collections import OrderedDict, defaultdict, ChainMap
import yaml
from .rec import consume_rec


class Dumper(yaml.Dumper):
    def ignore_aliases(self, data):
        return True


class Loader(yaml.Loader):
    pass


def _represent_odict(dumper, instance):
    return dumper.represent_mapping("tag:yaml.org,2002:map", instance.items())


def _construct_odict(loader, node):
    return OrderedDict(loader.construct_pairs(node))


def _represent_str(dumper, instance, _rx=re.compile("[#:]")):
    style = None
    if "\n" in instance:
        style = "|"
    else:
        m = _rx.search(instance)
        if m is not None:
            style = "'"
    return dumper.represent_scalar("tag:yaml.org,2002:str", instance, style=style)


def load(stream, *, buffered=False):
    return yaml.load_all(stream, Loader=Loader)


def dump(d, fp, *, ignore_none=False, squash_level=0, raw=False, extra_kwargs=None):
    extra_kwargs = extra_kwargs or {}
    default_flow_style = extra_kwargs.get("indent", None) is None
    allow_unicode = not extra_kwargs.get("ensure_ascii", False)

    def _dump(d):
        if ignore_none and d is None:
            return
        yaml.dump(
            d,
            fp,
            Dumper=Dumper,
            allow_unicode=allow_unicode,
            default_flow_style=default_flow_style,
        )

    consume_rec(d, _dump, n=squash_level)


Loader.add_constructor("tag:yaml.org,2002:map", _construct_odict)
for dict_class in [OrderedDict, defaultdict, ChainMap]:
    Dumper.add_representer(dict_class, _represent_odict)
Dumper.add_representer(str, _represent_str)

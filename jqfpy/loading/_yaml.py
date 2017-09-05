import yaml
from functools import partial
from collections import OrderedDict, defaultdict, ChainMap


class Dumper(yaml.Dumper):
    def ignore_aliases(self, data):
        return True


class Loader(yaml.Loader):
    pass


def _represent_odict(dumper, instance):
    return dumper.represent_mapping('tag:yaml.org,2002:map', instance.items())


def _construct_odict(loader, node):
    return OrderedDict(loader.construct_pairs(node))


def _represent_str(dumper, instance):
    if "\n" in instance:
        return dumper.represent_scalar('tag:yaml.org,2002:str', instance, style='|')
    else:
        return dumper.represent_scalar('tag:yaml.org,2002:str', instance)


Loader.add_constructor('tag:yaml.org,2002:map', _construct_odict)
for dict_class in [OrderedDict, defaultdict, ChainMap]:
    Dumper.add_representer(dict_class, _represent_odict)
Dumper.add_representer(str, _represent_str)


def load(stream, *, buffered=False):
    return [yaml.load(stream, Loader=Loader)]


def dump(d, fp, *, squash=False, raw=False, json_kwargs=None):
    if squash:
        for line in d:
            yaml.dump(line, fp, Dumper=Dumper)
    else:
        yaml.dump(d, fp, Dumper=Dumper)

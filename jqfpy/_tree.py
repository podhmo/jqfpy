from collections import OrderedDict


class Node:
    def __init__(self):
        self.children = OrderedDict()
        self.leafs = set()

    def __contains__(self, k):
        return k in self.children

    def subtree(self, k):
        if k not in self:
            self.children[k] = self.__class__()
        return self.children[k]

    def add_leaf(self, v):
        self.leafs.add(v)


def build_tree(L):
    t = Node()

    for ks in L:
        cursor = t
        for k in ks[:-1]:
            cursor = cursor.subtree(k)
        cursor.add_leaf(ks[-1])
    return t


def dump_tree(t, indent=""):
    for k, st in t.children.items():
        print("{}{}".format(indent, k))
        dump_tree(st, indent=indent + "  ")
    for v in t.leafs:
        print("{}{}".format(indent, v))

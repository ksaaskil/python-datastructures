"""Custom implementation of mutable dict supporting
minimum, maximum, predecessor, and successor operations.

Examples:

>>> tree = TreeDict()
>>> tree[1] = 'one'

# >>> tree[1]
# 'one'
# >>> del tree[1]
"""

from dataclasses import dataclass
import typing as t


@dataclass
class Node:
    key: int
    value: t.Any
    parent: t.Optional["Node"] = None
    left: t.Optional["Node"] = None
    right: t.Optional["Node"] = None


@dataclass
class Tree:
    root: t.Optional["Node"] = None

    def insert(self, key: int, value):
        insert_to(self, key, value)


def insert_to(tree: Tree, key, value):
    """Reference insertion algorithm from Introduction to Algorithms. Operates in-place.
    """
    y = None
    x = tree.root

    z = Node(key=key, value=value)

    while x is not None:
        y = x
        if z.key < x.key:
            x = x.left
        else:
            x = x.right

    z.parent = y
    if y is None:
        tree.root = z
    elif z.key < y.key:
        y.left = z
    else:
        y.right = z


class TreeDict:
    def __init__(self):
        self.dict = {}

    def __setitem__(self, key, item):
        self.dict[key] = item

    def __getitem__(self, key):
        return self.dict[key]

    def __delitem__(self, key):
        del self.dict[key]


__all__ = ["TreeDict"]

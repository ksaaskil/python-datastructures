"""Custom implementation of mutable dict supporting
minimum, maximum, predecessor, and successor operations.

Examples:

>>> tree = TreeDict()
>>> tree[1] = 'one'
>>> tree[1]
'one'

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


def _inorder_walk(node: t.Optional[Node], func):
    if node is None:
        return
    print("Calling on ", str(node))
    _inorder_walk(node.left, func)
    print("Done left")
    func(node)
    print("Done center")
    _inorder_walk(node.right, func)
    print("Done right")


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
        elif z.key > x.key:
            x = x.right
        else:
            x.value = value
            return

    z.parent = y
    if y is None:
        tree.root = z
    elif z.key < y.key:
        y.left = z
    else:
        y.right = z


def search(tree: Tree, key):
    if tree.root is None:
        raise KeyError("Empty dictionary, can't find key {}".format(key))

    x = tree.root

    while x is not None:
        if key < x.key:
            x = x.left
        elif key > x.key:
            x = x.right
        else:
            return x.value

    raise KeyError("Key {} not found".format(key))


def delete(tree: Tree, key):
    pass


class TreeDict:
    def __init__(self):
        self.tree = Tree()

    def __setitem__(self, key, item):
        insert_to(self.tree, key, item)

    def __getitem__(self, key):
        return search(self.tree, key)

    def __delitem__(self, key):
        return delete(self.tree, key)

    def __contains__(self, key):
        try:
            self[key]
            return True
        except KeyError:
            return False

    def inorder_walk(self, func):
        _inorder_walk(self.tree.root, func)


__all__ = ["TreeDict"]

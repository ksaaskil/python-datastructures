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


def inorder_walk(node: t.Optional[Node], func):
    if node is None:
        return

    inorder_walk(node.left, func)
    func(node)
    inorder_walk(node.right, func)


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


def search(tree: Tree, key):
    pass


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

    def inorder_walk(self, func):
        inorder_walk(self.tree.root, func)


__all__ = ["TreeDict"]

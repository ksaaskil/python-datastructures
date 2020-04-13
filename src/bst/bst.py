from dataclasses import dataclass, replace
from typing import Optional, Any, TypeVar, Generic, Callable
from typing_extensions import Protocol
from abc import abstractmethod

Key = TypeVar("Key", bound="Comparable")


class Comparable(Protocol):
    @abstractmethod
    def __eq__(self, other: Any) -> bool:
        pass

    @abstractmethod
    def __lt__(self: Key, other: Key) -> bool:
        pass

    def __gt__(self: Key, other: Key) -> bool:
        return (not self < other) and self != other

    def __le__(self: Key, other: Key) -> bool:
        return self < other or self == other

    def __ge__(self: Key, other: Key) -> bool:
        return not self < other


@dataclass
class Node(Generic[Key]):
    key: Key
    parent: Optional["Node[Key]"] = None
    left: Optional["Node[Key]"] = None
    right: Optional["Node[Key]"] = None


# Alias for convenience
@dataclass
class Tree_(Generic[Key]):
    root: Optional[Node[Key]]


Tree = Node


def insert_(tree: Tree_[Key], key: Key):
    """Reference insertion algorithm from Introduction to Algorithms. Operates in-place.
    """
    y = None
    x = tree.root

    z = Node(key=key)

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


def insert(node: Optional[Node[Key]], z: Node[Key]) -> Node[Key]:
    if node is None:
        return z

    # Update parent
    z = replace(z, parent=node)

    if z.key < node.key:
        # Replace current node's left child with a tree where z has been inserted
        return replace(node, left=insert(node.left, z))
    else:
        return replace(node, right=insert(node.right, z))


def transplant(tree: Optional[Node], u: Node, v: Optional[Node]):
    """Replace subtree as a child of its parent with another subtree.
    """

    assert tree is not None, "Expected to find u in tree to transplant v"

    if tree == u:
        # u is the root, replace whole tree
        return v

    # if v is not None:
    #    assert u.parent == v.parent

    if tree.left == u:
        if v is not None:
            v = replace(v, parent=tree)
        tree = replace(tree, left=v)
        return tree
    elif tree.right == u:
        if v is not None:
            v = replace(v, parent=tree)
        tree = replace(tree, right=v)
        return tree

    # Keep looking for u
    if u.key < tree.key:
        # u is on the left
        return replace(tree, left=transplant(tree.left, u, v))
    else:
        # u is on the right
        return replace(tree, right=transplant(tree.right, u, v))


def delete(node: Optional[Node[Key]], z: Node[Key]) -> Optional[Node[Key]]:
    if node is None:
        return None

    if node != z:
        if z.key < node.key:
            return replace(node, left=delete(node.left, z))
        else:
            return replace(node, right=delete(node.right, z))

    # node is z
    assert node == z

    return node


def inorder_walk(tree: Optional[Tree[Key]], visit: Callable[[Node[Key]], None]):
    """In-order tree walk."""

    if tree is None:
        return

    inorder_walk(tree.left, visit)
    visit(tree)
    inorder_walk(tree.right, visit)


Acc = TypeVar("Acc")


def inorder_reduce(
    tree: Optional[Tree[Key]],
    accumulator: Callable[[Acc, Node[Key]], Acc],
    initializer: Acc,
) -> Acc:
    """Accumulate values by walking the tree.

    Arguments:
        tree {Optional[Tree[Key]]} -- Tree to walk.
        accumulator {Callable[[V, Node[Key]], Acc]} -- Accumulator function.
        initializer {Acc} -- Initial value.

    Returns:
        Acc -- Accumulated value.
    """

    acc = initializer

    def call(node: Node[Key]):
        nonlocal acc
        acc = accumulator(acc, node)

    inorder_walk(tree, visit=call)

    return acc

from dataclasses import dataclass, replace
from typing import Optional, Any, TypeVar, Generic, Callable
from typing_extensions import Protocol
from abc import abstractmethod

C = TypeVar("C", bound="Comparable")


class Comparable(Protocol):
    @abstractmethod
    def __eq__(self, other: Any) -> bool:
        pass

    @abstractmethod
    def __lt__(self: C, other: C) -> bool:
        pass

    def __gt__(self: C, other: C) -> bool:
        return (not self < other) and self != other

    def __le__(self: C, other: C) -> bool:
        return self < other or self == other

    def __ge__(self: C, other: C) -> bool:
        return not self < other


@dataclass
class Node(Generic[C]):
    key: C
    parent: Optional["Node[C]"] = None
    left: Optional["Node[C]"] = None
    right: Optional["Node[C]"] = None


# Alias for convenience
@dataclass
class Tree_(Generic[C]):
    root: Optional[Node[C]]


Tree = Node


def insert_(tree: Tree_[C], key: C):
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


def insert(node: Optional[Node[C]], z: Node[C]) -> Node[C]:
    if node is None:
        return z

    # Update parent
    z = replace(z, parent=node)

    if z.key < node.key:
        # Replace current node's left child with a tree where z has been inserted
        return replace(node, left=insert(node.left, z))
    else:
        return replace(node, right=insert(node.right, z))


def walk(tree: Optional[Tree[C]], call: Callable[[Node[C]], None]):
    """In-order tree walk."""

    if tree is None:
        return

    walk(tree.left, call)
    call(tree)
    walk(tree.right, call)


V = TypeVar("V")


def reduce(
    tree: Optional[Tree[C]], accumulator: Callable[[V, Node[C]], V], initializer: V,
) -> V:
    """Accumulate values by walking the tree.

    Arguments:
        tree {Optional[Tree[C]]} -- Tree to walk.
        accumulator {Callable[[V, Node[C]], V]} -- Accumulator function.
        initializer {V} -- Initial value.

    Returns:
        V -- Accumulated value.
    """

    acc = initializer

    def call(node: Node[C]):
        nonlocal acc
        acc = accumulator(acc, node)

    walk(tree, call)

    return acc

from bst import Node, insert, Tree, reduce as accumulate
import hypothesis.strategies as some
from functools import reduce
from typing import Sequence, TypeVar, Sequence, Tuple, Optional
from hypothesis import given

Ex = TypeVar("Ex")


@some.composite
def tree(
    draw, key_gen: some.SearchStrategy[Ex] = some.integers()
) -> Tuple[Optional[Tree[Ex]], Sequence[Ex]]:
    """Strategy to produce a tree and the list of values used to create the tree."""
    keys = draw(some.lists(key_gen))  # type: Sequence[Ex]

    tree = None

    for value in keys:
        tree = insert(tree, Node(key=value))

    return (tree, keys)


@given(tree_and_inserted=tree())
def test_insertion(tree_and_inserted):
    """Test all values inserted into tree can be found from the tree."""
    tree, inserted = tree_and_inserted
    values_in_tree = accumulate(tree, lambda acc, v: [*acc, v.key], [])

    # Invariant
    assert set(values_in_tree) == set(inserted)

    # Sanity check: first value inserted is the root
    if len(inserted) > 0:
        assert tree.key == inserted[0]


def test_insert_right():
    n = Tree(key=2)
    new_tree = insert(n, Node(key=3))
    assert new_tree.key == 2
    assert new_tree.right.key == 3


def test_insert_left():
    n = Tree(key=2)
    new_tree = insert(n, Node(key=1))
    assert new_tree.key == 2
    assert new_tree.left.key == 1

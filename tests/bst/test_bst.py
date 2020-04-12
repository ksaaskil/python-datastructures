from bst import Node, insert, Tree, reduce as accumulate
import hypothesis.strategies as some
from functools import reduce
from typing import Sequence, TypeVar, Sequence, Tuple, Optional
from hypothesis import given, assume

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


@given(tree_and_inserted=tree())
def test_tree_property(tree_and_inserted):
    """
    Test binary search tree property. All values in the left subtree of each node
    is smaller than the node's key, and all values in the right subtree are larger than the node's key.
    """
    tree, inserted = tree_and_inserted
    assume(len(inserted) > 0)  # Only test non-empty trees

    assert tree is not None

    nodes_in_tree = accumulate(tree, lambda acc, v: [*acc, v], [])

    for node in nodes_in_tree:
        if node is None:
            pass

        left_values = accumulate(node.left, lambda acc, v: [*acc, v.key], [])
        right_values = accumulate(node.right, lambda acc, v: [*acc, v.key], [])

        for left in left_values:
            assert left < node.key

        for right in right_values:
            assert right > node.key

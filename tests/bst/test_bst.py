from bst import Node, insert, Tree, Key
from bst.bst import inorder_walk
import hypothesis.strategies as some
from functools import reduce
from typing import Sequence, TypeVar, Sequence, Tuple, Optional
from hypothesis import given, assume

Ex = TypeVar("Ex")


def collect(tree: Tree[Key]):
    """Helper function to collect all nodes from a tree.
    """
    acc = []

    def add(node: Node[Key]):
        acc.append(node)

    inorder_walk(tree, visit=add)

    return acc


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
    keys_in_tree = [node.key for node in collect(tree)]

    # Invariant
    assert sorted(keys_in_tree) == sorted(inserted)

    # Sanity check: first value inserted is the root
    if len(inserted) > 0:
        assert tree.key == inserted[0]


def assert_tree_property_holds(node: Node[Key]):
    if node.left is not None:
        assert node.key >= node.left.key
        assert_tree_property_holds(node.left)

    if node.right is not None:
        assert node.key <= node.right.key
        assert_tree_property_holds(node.right)


@given(tree_and_inserted=tree())
def test_tree_property(tree_and_inserted):
    """
    Test binary search tree property. All values in the left subtree of each node
    is smaller than the node's key, and all values in the right subtree are larger than the node's key.
    """
    tree, inserted = tree_and_inserted
    assume(len(inserted) > 0)  # Only test non-empty trees

    assert tree is not None

    assert_tree_property_holds(tree)

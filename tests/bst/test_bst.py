from bst import Node, insert, Tree, Key, delete, transplant
from bst.bst import inorder_walk
import hypothesis.strategies as some
from functools import reduce
from typing import Sequence, TypeVar, Sequence, Tuple, Optional
from hypothesis import given, assume

Ex = TypeVar("Ex")


def collect(tree: Optional[Tree[Key]]):
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


@some.composite
def nodes_to_delete(draw, tree: Optional[Tree]):
    nodes = collect(tree)
    to_delete_ids = draw(some.slices(len(nodes)))
    return nodes[to_delete_ids]


@given(tree_and_inserted=tree(), data=some.data())
def test_deletion(tree_and_inserted, data):
    tree, inserted_keys = tree_and_inserted
    assume(len(inserted_keys) > 0)

    # Pick something to delete
    to_delete = data.draw(nodes_to_delete(tree), label="Nodes to delete")
    keys_to_delete = [node.key for node in to_delete]

    for node in to_delete:
        tree = delete(tree, node)

    assert_bst_property_holds(tree)
    keys_after_delete = [node.key for node in collect(tree)]

    # assert len(inserted_keys) - len(keys_after_delete) == len(keys_to_delete)

    kept_keys = set(inserted_keys) - set(keys_to_delete)

    for kept_key in kept_keys:
        assert kept_key in keys_after_delete

    for deleted_key in keys_to_delete:
        # assert deleted_key not in keys_after_delete
        pass
        #
        # pass


@given(tree_and_inserted=tree(), data=some.data())
def test_transplant(tree_and_inserted, data):
    tree_to_transplant, inserted = tree_and_inserted

    assume(len(inserted) > 0)

    # Pick something to transplant
    nodes = collect(tree_to_transplant)
    node_to_replace = data.draw(some.sampled_from(nodes), label="Node to replace")

    another_tree, another_inserted = data.draw(
        tree(), label="Node to add with transplant"
    )

    new_tree = transplant(tree_to_transplant, node_to_replace, another_tree)

    new_nodes = collect(new_tree)

    assert node_to_replace not in new_nodes

    new_keys = [node.key for node in new_nodes]

    for another in another_inserted:
        assert another in new_keys


def assert_bst_property_holds(node: Optional[Node[Key]]):
    if node is None:
        return

    if node.left is not None:
        keys_left = [node.key for node in collect(node.left)]
        for key in keys_left:
            assert key <= node.key
        assert_bst_property_holds(node.left)

    if node.right is not None:
        keys_right = [node.key for node in collect(node.right)]
        for key in keys_right:
            assert key >= node.key
        assert_bst_property_holds(node.right)


@given(tree_and_inserted=tree())
def test_tree_property(tree_and_inserted):
    """
    Test binary search tree property. All values in the left subtree of each node
    is smaller than the node's key, and all values in the right subtree are larger than the node's key.
    """
    tree, inserted = tree_and_inserted
    assert_bst_property_holds(tree)

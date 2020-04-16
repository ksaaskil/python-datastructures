from dict_tree import TreeDict
from hypothesis import given, assume
from hypothesis.stateful import (
    RuleBasedStateMachine,
    precondition,
    rule,
    Bundle,
    consumes,
)
import hypothesis.strategies as some
import itertools
import pytest


def keys_and_values():
    return some.lists(some.tuples(some.integers(), some.binary()))


def dedupe(key_value_pairs):
    """Remove duplicate keys by always picking the last. Also sorts the array by key.
    
>>> dedupe([(0, 0), (0, 1), (1, 2), (0, 2)])
[(0, 2), (1, 2)]
    
    """
    as_sorted = sorted(key_value_pairs, key=lambda pair: pair[0])
    grouped = itertools.groupby(as_sorted, lambda pair: pair[0])

    deduped = []
    for _, same_key in grouped:
        last = None
        for key_val in same_key:
            last = key_val
        deduped.append(last)
    return deduped


@some.composite
def dict_and_values(draw):
    keys_and_vals = draw(keys_and_values())

    tree = TreeDict()
    for key, val in keys_and_vals:
        tree[key] = val

    return tree, keys_and_vals


def collect(tree: TreeDict):
    collected = []

    tree.inorder_walk(lambda x: collected.append(x))
    return collected


@given(dict_and_values=dict_and_values())
def test_insert_and_search(dict_and_values):
    dict_tree, inserted = dict_and_values
    deduped = dedupe(inserted)
    assert len(deduped) <= len(inserted)

    for key, value in deduped:
        in_dict = dict_tree[key]
        assert in_dict == value, "Expected {} for key {}, got {}".format(
            value, key, in_dict
        )


@given(dict_and_values=dict_and_values(), data=some.data())
def test_search_nonexisting(dict_and_values, data):
    """Test drawing a key not in dictionary."""
    dict_tree, inserted = dict_and_values
    inserted_keys = [key for key, _ in inserted]
    new_key = data.draw(some.integers())
    assume(new_key not in inserted_keys)

    with pytest.raises(KeyError):
        dict_tree[new_key]


def test_search_delete():
    dict_tree = TreeDict()
    key_vals = [(0, 0), (1, 1)]
    for key, val in key_vals:
        dict_tree[key] = val

    del dict_tree[1]
    assert 1 not in dict_tree
    assert 0 in dict_tree
    del dict_tree[0]
    assert 0 not in dict_tree


@given(
    dict_and_values=dict_and_values().filter(lambda keyval: len(keyval[1]) > 0),
    data=some.data(),
)
def test_search_after_delete(dict_and_values, data):
    """Test drawing a key not in dictionary."""
    dict_tree, inserted = dict_and_values
    inserted_keys = [key for key, _ in inserted]
    key_to_delete = data.draw(some.sampled_from(inserted_keys), label="Key to delete")
    keys_before = [node.key for node in collect(dict_tree)]
    print("Keys before delete:", keys_before)
    del dict_tree[key_to_delete]
    print("Keys after delete:", [node.key for node in collect(dict_tree)])
    with pytest.raises(KeyError):
        dict_tree[key_to_delete]


class StatefulDictStateMachine(RuleBasedStateMachine):
    def __init__(self):
        super().__init__()
        self.tree = TreeDict()
        self.in_dict = {}

    inserted_keys = Bundle("inserted")
    deleted_keys = Bundle("deleted_keys")

    @rule(target=inserted_keys, key=some.integers(), v=some.text())
    def insert(self, key, v):
        self.tree[key] = v
        self.in_dict[key] = v
        return key

    @rule(key=inserted_keys)
    def search(self, key):
        assert self.tree[key] == self.in_dict[key]

    @rule(key=consumes(inserted_keys))
    def delete(self, key):
        assume(key not in self.in_dict)
        del self.tree[key]
        del self.in_dict[key]

    @rule(key=some.integers())
    def search_non_existing(self, key):
        assume(key not in self.in_dict)
        assert key not in self.in_dict
        with pytest.raises(KeyError):
            self.tree[key]


TestStatefulDict = StatefulDictStateMachine.TestCase

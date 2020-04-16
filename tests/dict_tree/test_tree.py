from dict_tree import TreeDict
from hypothesis import given, assume
from hypothesis.stateful import RuleBasedStateMachine, rule
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


@given(
    dict_and_values=dict_and_values().filter(lambda keyval: len(keyval[1]) > 0),
    data=some.data(),
)
def test_search_after_delete(dict_and_values, data):
    """Test drawing a key not in dictionary."""
    dict_tree, inserted = dict_and_values
    inserted_keys = [key for key, _ in inserted]
    new_key = data.draw(some.sampled_from(inserted_keys))

    del dict_tree[new_key]

    with pytest.raises(KeyError):
        dict_tree[new_key]
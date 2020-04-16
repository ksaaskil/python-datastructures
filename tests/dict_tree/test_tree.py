from dict_tree import TreeDict
from hypothesis import given
import hypothesis.strategies as some
import itertools


def keys_and_values():
    return some.lists(some.tuples(some.integers(), some.text()))


def dedupe(key_value_pairs):
    """Remove duplicate keys by always picking the last."""
    grouped = itertools.groupby(key_value_pairs, lambda pair: pair[0])

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
def test_insert_and_walk(dict_and_values):
    dict_tree, inserted = dict_and_values
    deduped = dedupe(inserted)

    # collected = collect(dict_tree)
    # print(collected)
    # print(inserted)
    # print(collected)
    # assert len(collected) == len(deduped)

from dict_tree import TreeDict
from hypothesis import given
import hypothesis.strategies as some


def keys_and_values():
    return some.lists(some.tuples(some.integers(), some.text()))


@some.composite
def dict_and_values(draw):
    keys_and_vals = draw(keys_and_values())
    tree = TreeDict()
    for key, val in keys_and_vals:
        tree[key] = val

    return tree, keys_and_vals


@given(dict_and_values=dict_and_values())
def test_dict(dict_and_values):
    dict_tree, inserted = dict_and_values
    print(dict_tree)
    assert dict_and_values is not None

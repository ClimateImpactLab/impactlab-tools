import pytest

from impactlab_tools.utils.configdict import ConfigDict, gather_configtree


@pytest.fixture
def simple_nested_tree():
    return {'a': 1, 'b': {'a': 2}, 'c': 3, 'd-4': 4, 'e_5': 5, 'F': 6}


def test_configdict_climbs_tree(simple_nested_tree):
    conf = ConfigDict(simple_nested_tree)
    assert conf['c'] == 3


def test_configdict_prefer_child(simple_nested_tree):
    conf = gather_configtree(simple_nested_tree)['b']
    assert conf['a'] == 2


def test_configdict_selfreference(simple_nested_tree):
    conf = gather_configtree(simple_nested_tree)
    conf['b'] = conf
    assert conf['b'] == conf


def test_configdict_caseinsensitive_keys(simple_nested_tree):
    conf = gather_configtree(simple_nested_tree)
    assert conf['A'] == 1
    assert conf['f'] == 6

    conf['Z'] = 'foobar'
    assert conf['z'] == 'foobar'


def test_configdict_normalize(simple_nested_tree):
    """Normalize underscores and hyphens in keys
    """
    conf = ConfigDict(simple_nested_tree)
    assert conf['d_4'] == 4
    assert conf['e-5'] == 5

    conf['y-7'] = 'foobar'
    assert conf['y_7'] == 'foobar'

    conf['z-9'] = 'foobar'
    assert conf['z_9'] == 'foobar'


def test_configdict_throws_keyerror(simple_nested_tree):
    conf = ConfigDict(simple_nested_tree)
    with pytest.raises(KeyError):
        conf['foobar']


def test_configdict_merge(simple_nested_tree):
    conf1 = ConfigDict(simple_nested_tree)
    conf2 = ConfigDict({'foo': 0})

    internal_goal = simple_nested_tree.copy()
    internal_goal['foo'] = 0

    conf_merge = conf1.merge(conf2)

    assert conf_merge['foo'] == 0
    for k, v in simple_nested_tree.items():
        assert conf_merge[k] == v
    assert conf_merge.parent == conf1.parent


def test_configdict_merge_parentswap(simple_nested_tree):
    conf1 = gather_configtree(simple_nested_tree)['b']

    nested_tree_mod = simple_nested_tree.copy()
    nested_tree_mod['a'] = 9
    conf2 = gather_configtree(nested_tree_mod)['b']

    conf_merge = conf1.merge(conf2, xparent=True)

    assert conf_merge.data == conf2.data
    assert conf_merge.parent == conf2.parent


def test_configdict_key_access_stack(simple_nested_tree):
    """Test ConfigDict adds values to ``self.key_access_stack`` on query
    """
    conf = ConfigDict(simple_nested_tree)
    assert conf.key_access_stack == {}
    conf['a']
    assert 'a' in list(conf.key_access_stack.keys())


def test_configdict_key_access_stack_nested(simple_nested_tree):
    """Test ConfigDict.key_access_stack sores keys in appropriate configdict
    """
    conf = gather_configtree(simple_nested_tree)
    nested = conf['b']
    nested['a']
    nested['f']

    assert list(nested.key_access_stack.keys()) == ['a']

    top_keys = list(nested.parent.key_access_stack.keys())
    top_keys.sort()
    assert top_keys == ['b', 'f']


def test_configdict_used_all_keys_falseparent(simple_nested_tree):
    conf = gather_configtree(simple_nested_tree)
    nested = conf['b']

    nested['a']
    nested['f']

    assert nested.accessed_all_keys() is False


def test_configdict_accessed_all_keys(simple_nested_tree):
    conf = gather_configtree(simple_nested_tree)
    nested = conf['b']

    conf['a']
    conf['c']
    conf['d-4']
    conf['e-5']
    conf['f']

    assert conf.accessed_all_keys() is True
    assert nested.accessed_all_keys() is False

    nested['a']

    assert nested.accessed_all_keys() is True

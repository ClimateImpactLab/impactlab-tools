
def test_top_level_imports():
    import impactlab_tools

    assert type(impactlab_tools) == 'module'


def test_acp_imports():
    from impactlab_tools.acp import dist, aggregate
    from impactlab_tools.utils import cache, weighting

    assert type(dist) == 'module'
    assert type(aggregate) == 'module'
    assert type(cache) == 'module'
    assert type(weighting) == 'module'

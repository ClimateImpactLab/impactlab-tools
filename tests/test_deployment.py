
import pytest


def test_top_level_imports():
    import impactlab_tools

    assert isinstance(impactlab_tools, type(pytest))


def test_acp_imports():
    from impactlab_tools.acp import dist, aggregate
    from impactlab_tools.utils import cache, weighting

    assert isinstance(dist, type(pytest))
    assert isinstance(aggregate, type(pytest))
    assert isinstance(cache, type(pytest))
    assert isinstance(weighting, type(pytest))


from __future__ import absolute_import

import pytest


def test_top_level_imports():
    import impactlab_tools

    if not isinstance(impactlab_tools, type(pytest)):
        raise TypeError


def test_acp_imports():
    from impactlab_tools.acp import dist, aggregate
    from impactlab_tools.utils import weighting

    if not isinstance(dist, type(pytest)):
        raise TypeError

    if not isinstance(aggregate, type(pytest)):
        raise TypeError

    if not isinstance(weighting, type(pytest)):
        raise TypeError

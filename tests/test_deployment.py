
from __future__ import absolute_import

import pytest


def test_top_level_imports():
    from src import impactlab_tools

    if not isinstance(impactlab_tools, type(pytest)):
        raise TypeError


def test_acp_imports():
    from src.impactlab_tools.acp import dist
    from src.impactlab_tools.acp import aggregate
    from src.impactlab_tools.utils import weighting

    if not isinstance(dist, type(pytest)):
        raise TypeError

    if not isinstance(aggregate, type(pytest)):
        raise TypeError

    if not isinstance(weighting, type(pytest)):
        raise TypeError

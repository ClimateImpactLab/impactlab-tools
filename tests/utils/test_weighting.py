
from __future__ import absolute_import

import pytest

import xarray as xr
import numpy as np
import pandas as pd

from impactlab_tools.utils import weighting


@pytest.yield_fixture
def increasing_array():

    yield xr.DataArray(
        np.sum(np.mgrid[0:5, 0:5, 0:5], axis=0),
        dims=('x', 'y', 'z'),
        coords={c: [c+str(i) for i in range(5)] for c in ['x', 'y', 'z']})


@pytest.yield_fixture
def random_array():

    yield xr.DataArray(
        np.random.random((5, 5, 5)),
        dims=('x', 'y', 'z'),
        coords={c: [c+str(i) for i in range(5)] for c in ['x', 'y', 'z']})


def test_unweighted_median(random_array):
    '''
    Asserts weighted_quantile_xr correctly returns the median
    '''

    for dim in random_array.dims:
        weighted = weighting.weighted_quantile_xr(
            random_array, [0.5], np.ones((5)), dim=dim)

        median = random_array.median(dim=dim)

        if not (weighted == median).all():
            raise ValueError()


def test_first_value(random_array):
    '''
    Asserts weighted_quantile_xr correctly returns the first value
    '''

    for dim in random_array.dims:
        weighted = weighting.weighted_quantile_xr(
            random_array, [0.5], [1, 0, 0, 0, 0], dim=dim)

        first = random_array.isel(**{dim: 0})

        if not (weighted == first).all():
            raise ValueError()


def test_manual_weighting(increasing_array):
    '''
    Asserts weighted_quantile_xr matches a manually weighted mean
    '''

    for dim in increasing_array.dims:
        weighted = weighting.weighted_quantile_xr(
            increasing_array, [0.5], [0.25, 0.5, 0, 0, 0.25], dim=dim)

        manual = increasing_array.isel(**{dim: [0, 1, 1, 4]}).median(dim=dim)

        if not (weighted == manual).all():
            raise ValueError()


def test_unsorted_weights_index(increasing_array):
    '''
    Asserts weighted_quantile_xr weights correctly with unsorted weights
    '''

    for dim in increasing_array.dims:

        index = pd.Series(
            [0.25, 0.5, 0.25, 0, 0],
            index=pd.Index([dim+str(i) for i in [2, 4, 1, 3, 0]]))

        weighted = weighting.weighted_quantile_xr(
            increasing_array, [0.125, 0.5], index, dim=dim)

        try:
            manual = increasing_array.isel_points(
                dim = pd.Index([0.125, 0.5], name='quantile'),
                **{dim: [1, 3]})
        except AttributeError:  # Triggered for xarray >= v0.13
            manual = increasing_array.isel(
                **{dim: xr.DataArray([1, 3],
                                 dims='quantile',
                                 coords={'quantile': [0.125, 0.5]})}
            )

        assert (weighted == manual).all()

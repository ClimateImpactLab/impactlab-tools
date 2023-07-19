
from __future__ import absolute_import

import numpy as np
import pandas as pd
import xarray as xr

import toolz
import os

import impactlab_tools.assets


# file readers for default weights files in assets directory

@toolz.memoize
def _get_weights(project='acp', rcp='rcp85'):

    da = (
        pd.read_csv(
            os.path.join(
                os.path.dirname(impactlab_tools.assets.__file__),
                'weights_{}.csv'.format(project)),
            index_col=[0, 1])['weight']
        .xs(rcp, level='rcp')
        .to_xarray())

    return da


# Computation helpers

def weighted_quantile_xr(
        data,
        quantiles,
        sample_weight,
        dim,
        values_sorted=False):
    """
    Compute quantiles of a weighted distribution

    similar to :py:func:`weighted_quantile` operates on a named dimension of an
    :py:class:`xarray.DataArray`.

    .. NOTE ::

        quantiles should be in [0, 1]!

    Parameters
    ----------

    data : DataArray or Dataset

        :py:class:`xarray.DataArray` or :py:class`xarray.Dataset` with data
        indexed by ``dim``

    quantiles : array-like

        quantiles of distribution to return

    sample_weight : numpy.array

        weights array-like of the same length as `array`

    values_sorted : bool

        if True, then will avoid sorting of initial array

    dim : str

        Dimension along which to weight the data

    Returns
    -------

    xarray.DataArray

        computed quantiles from weighted distribution

    """
    if hasattr(data, 'data_vars'):
        res = xr.Dataset()
        for var in data.data_vars.keys():
            if dim in data[var].dims:
                res[var] = _weighted_quantile_xr_da(
                    data[var], quantiles, sample_weight, dim, values_sorted)
            else:
                res[var] = data[var]

        return res

    else:
        return _weighted_quantile_xr_da(
            data, quantiles, sample_weight, dim, values_sorted)


def _weighted_quantile_xr_da(
        data,
        quantiles,
        sample_weight,
        dim,
        values_sorted=False):

    axis = data.get_axis_num(dim)
    dims = list(data.dims[:axis]) + ['quantile'] + list(data.dims[axis+1:])
    coords = {
        coord: data.coords[coord] for coord in data.dims if coord in dims}
    coords.update({'quantile': quantiles})

    if isinstance(sample_weight, (pd.Series, xr.DataArray)):
        weights = sample_weight.loc[data.coords[dim].values].values
    else:
        weights = sample_weight

    data_dist = weighted_quantile(
        data.values,
        quantiles,
        weights,
        values_sorted=values_sorted,
        axis=axis)

    data_dist = xr.DataArray(data_dist, dims=dims, coords=coords)

    return data_dist


def weighted_quantile(
        values,
        quantiles,
        sample_weight=None,
        values_sorted=False,
        old_style=False,
        axis=None):
    """
    Compute quantiles of a weighted distribution

    similar to :py:func:`weighted_quantile_1d` but supports weighting along any
    (numbered) dimension

    .. NOTE ::

        quantiles should be in [0, 1]!

    Parameters
    ----------

    values : numpy.array

        numpy.array with data

    quantiles : array-like

        quantiles of distribution to return

    sample_weight : numpy.array

        weights array-like of the same length as `array`

    values_sorted : bool

        if True, then will avoid sorting of initial array

    old_style : bool

        if True, will correct output to be consistent with numpy.percentile.

    Returns
    -------

    numpy.array

        computed quantiles from weighted distribution

    """
    if len(values.shape) > 1 and axis is not None:

        return np.apply_along_axis(
            weighted_quantile_1d,
            axis,
            values,
            quantiles,
            sample_weight,
            values_sorted,
            old_style)

    else:

        return weighted_quantile_1d(
            values,
            quantiles,
            sample_weight,
            values_sorted,
            old_style)


def weighted_quantile_1d(
        values,
        quantiles,
        sample_weight=None,
        values_sorted=False,
        old_style=False):
    """
    Very close to numpy.percentile, but supports weights

    Thanks to Alleo!
    http://stackoverflow.com/questions/21844024/weighted-percentile-using-numpy/29677616#29677616

    .. NOTE ::

        quantiles should be in [0, 1]!

    Parameters
    ----------

    values : numpy.array

        numpy.array with data

    quantiles : array-like

        quantiles of distribution to return

    sample_weight : numpy.array

        weights array-like of the same length as `array`

    values_sorted : bool

        if True, then will avoid sorting of initial array

    old_style : bool

        if True, will correct output to be consistent with numpy.percentile.

    Returns
    -------

    numpy.array

        computed quantiles from weighted distribution

    """
    values = np.array(values)
    quantiles = np.array(quantiles)

    if sample_weight is None:
        return np.percentile(values, quantiles)

    sample_weight = np.array(sample_weight)

    if not np.all(quantiles >= 0) and np.all(quantiles <= 1):
        raise ValueError('quantiles should be in [0, 1]')

    if not values_sorted:

        sorter = np.argsort(values)
        values = values[sorter]
        sample_weight = sample_weight[sorter]

    # Find the cumsum, and locate the center of each weight's mass
    # e.g. [0.25, 0.25, 0.5, 0] --> [0.125, 0.375, 0.75, 1]
    weighted_quantiles = np.cumsum(sample_weight) - 0.5 * sample_weight

    if old_style:

        # To be convenient with np.percentile
        # e.g. [0, 0.25, 0.25, 0.5, 0] --> [ 0, 0.2857, 0.7143, 1]
        weighted_quantiles -= weighted_quantiles[0]
        weighted_quantiles /= weighted_quantiles[-1]

    else:

        weighted_quantiles /= np.sum(sample_weight)

    result = np.interp(quantiles, weighted_quantiles, values)

    return result

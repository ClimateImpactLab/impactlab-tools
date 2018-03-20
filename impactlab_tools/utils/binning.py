
from __future__ import absolute_import

import xarray as xr
import numpy as np
import scipy.stats

from pandas import CategoricalIndex


def binned_statistic_1d(da, dim, bins=10, statistic='count', value_range=None):
    '''
    Bin a data array by values and summarize along a dimension

    Parameters
    ----------

    da : xr.DataArray
        DataArray to be binned

    dim : str
        Dimension along which to summarize the binned values

    statistic : string or callable, optional
        The statistic to compute (default is 'count'). The following statistics
        are available:

        * 'mean' : compute the mean of values for points within each bin. Empty
            bins will be represented by NaN.

        * 'median' : compute the median of values for points within each bin.
            Empty bins will be represented by NaN.

        * 'count' : compute the count of points within each bin. This is
            identical to an unweighted histogram. values array is not
            referenced.

        * 'sum' : compute the sum of values for points within each bin. This is
            identical to a weighted histogram.

        * 'min' : compute the minimum of values for points within each bin.
            Empty bins will be represented by NaN.

        * 'max' : compute the maximum of values for point within each bin.
            Empty bins will be represented by NaN.

        * function : a user-defined function which takes a 1D array of values,
            and outputs a single numerical statistic. This function will be
            called on the values in each bin. Empty bins will be represented by
            function([]), or NaN if this returns an error.

    bins : int or sequence of scalars, optional
        If bins is an int, it defines the number of equal-width bins in the
        given range (10 by default). If bins is a sequence, it defines the bin
        edges, including the rightmost edge, allowing for non-uniform bin
        widths. Values in x that are smaller than lowest bin edge are assigned
        to bin number 0, values beyond the highest bin are assigned to
        bins[-1]. If the bin edges are specified, the number of bins will be,
        (nx = len(bins)-1).


    value_range : (float, float) or [(float, float)], optional
        The lower and upper range of the bins. If not provided, value_range is
        simply (x.min(), x.max()). Values outside the range are ignored.

    Returns
    -------

    binned : xr.DataArray
        A data array with bins along the summary dimension

    Examples
    --------

    .. code-block:: python

        >>> da = xr.DataArray(
        ...     np.arange(16).reshape(4,4),
        ...     dims=('a', 'b'),
        ...     coords={'a': list('abcd'), 'b': list('wxyz')})
        ...
        >>> da # doctest: +SKIP
        <xarray.DataArray (a: 4, b: 4)>
        array([[  0,  1,  2,  3],
               [  4,  5,  6,  7],
               [  8,  9, 10, 11],
               [ 12, 13, 14, 15]])
        Coordinates:
          * a        (a) <U1 'a' 'b' 'c' 'd'
          * b        (b) <U1 'w' 'x' 'y' 'z'

        >>> binned_statistic_1d(
        ...     da, 'b', [0, 2, 5, 20])
        ...     # doctest: +SKIP
        <xarray.DataArray (a: 4, goh realroups: 3)>
        array([[ 2., 2., 0.],
               [ 0., 1., 3.],
               [ 0., 0., 4.],
               [ 0., 0., 4.]])
        Coordinates:
          * a        (a) <U1 'a' 'b' 'c' 'd'
          * groups   (groups) object '(0, 2]' '(2, 5]' '(5, 20]'

        >>> binned_statistic_1d(da, 'a', statistic='sum') # doctest: +SKIP
        <xarray.DataArray (groups: 10, b: 4)>
        array([[  0.,  1.,  2.,  3.],
               [  0.,  0.,  0.,  0.],
               [  0.,  0.,  0.,  0.],
               [  4.,  5.,  6.,  7.],
               [  0.,  0.,  0.,  0.],
               [  0.,  0.,  0.,  0.],
               [  8.,  9., 10., 11.],
               [  0.,  0.,  0.,  0.],
               [  0.,  0.,  0.,  0.],
               [ 12., 13., 14., 15.]])
        Coordinates:
          * groups   (groups) object '(0.0, 1.5]' '(1.5, 3.0]' '(3.0, 4.5]' ...
          * b        (b) <U1 'w' 'x' 'y' 'z'
    '''

    # apply binned_statistic along dim
    bnd = np.apply_along_axis(
        lambda x, **kwds: scipy.stats.binned_statistic(x, x, **kwds)[0],
        da.get_axis_num(dim),
        da.values,
        bins=bins,
        statistic=statistic,
        range=value_range)

    if isinstance(bins, int):
        if value_range is None:
            value_range = float(da.min()), float(da.max())
        bins = np.linspace(value_range[0], value_range[1], bins+1)

    # build index for new array
    bindex = CategoricalIndex(
        ['({}, {}]'.format(bins[i-1], bins[i]) for i in range(1, len(bins))],
        ordered=True)

    da = xr.DataArray(
        bnd,
        dims=tuple([
            d if d != dim else 'groups' for d in da.dims]),
        coords={
            d if d != dim else 'groups': da.coords[d] if d != dim else bindex
            for d in da.dims})
    return da

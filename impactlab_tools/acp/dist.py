
from __future__ import absolute_import

from impactlab_tools.utils.weighting import weighted_quantile_xr
from impactlab_tools.utils.cache import DataCache


def acp_quantiles(
        data,
        rcp,
        quantiles=[0.05, 0.167, 0.5, 0.833, 0.95],
        values_sorted=False,
        dim='model',
        api=None):
    """
    Compute quantiles of an xarray distribution using ACP weights

    .. NOTE ::

        quantiles should be in [0, 1]!

    Parameters
    ----------

    data : DataArray

        xarray.DataArray with data

    rcp : str

        RCP weights/models to use ('rcp26', 'rcp45', 'rcp60', 'rcp85')

    quantiles : array-like

        quantiles of distribution to return

    values_sorted : bool

        if True, then will avoid sorting of initial array

    dim : str

        dimension along which to retrieve quantiles. The indices of this
        dimension should be valid ACP climate models.

    api : object

        DataFS API object to use in data retrieval (optional, uses default
        profile if not provided)


    Returns
    -------

    xarray.DataArray

        computed quantiles from weighted distribution

    See also
    --------

    * :py:func:`.utils.weighting.weighted_quantile_xr`
    * :py:func:`.utils.weighting.weighted_quantile`
    * :py:func:`.utils.weighting.weighted_quantile_1d`
    * :py:func:`numpy.percentile`
    * :py:meth:`pandas.DataFrame.quantile`
    * :py:meth:`pandas.Series.quantile`

    """

    mw = DataCache.retrieve('ACP_climate_gcm-modelweights.csv').xs(
        rcp, level='rcp')['weight_corrected']

    return weighted_quantile_xr(
        data=data,
        quantiles=quantiles,
        sample_weight=mw,
        values_sorted=False,
        dim=dim)

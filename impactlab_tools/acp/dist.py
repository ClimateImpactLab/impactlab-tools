
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

        This function does not control for the number of samples of each model.
        If they are not constant across models provide a correctly weighted
        weights array to :py:func:`utils.weighting.weighted_quantile_xr`.
        We would like to fix this. If you have a good fix we'd love a PR :)

    Parameters
    ----------

    data : DataArray
        :py:class:`xarray.DataArray` or :py:class:`xarray.Dataset` with data
        indexed by ACP model along the dimension ``dim``. If a Dataset is
        passed, ``acp_quantiles`` computes the weighted quantile for each
        variable in the ``Dataset`` that is indexed by ``dim``.

    rcp : str
        RCP weights/models to use ('rcp26', 'rcp45', 'rcp60', 'rcp85')

    quantiles : array-like
        quantiles of distribution to return. quantiles should be in [0, 1].

    values_sorted : bool
        if True, then will avoid sorting of initial array

    dim : str
        dimension along which to retrieve quantiles. The indices of this
        dimension should be valid ACP climate models. Default: `'model'`.

    api : object
        DataFS API object to use in data retrieval (optional, uses default
        profile if not provided)


    Returns
    -------

    DataArray or Dataset
        returns a new :py:class:`~xarray.DataArray` or
        :py:class:`~xarray.Dataset` with quantiles computed from weighted
        distribution along a new dimension ``quantile`` and dimension ``dim``
        dropped.

    See also
    --------

    * :py:func:`.gcp.dist.gcp_quantiles`
    * :py:func:`.utils.weighting.weighted_quantile_xr`
    * :py:func:`.utils.weighting.weighted_quantile`
    * :py:func:`.utils.weighting.weighted_quantile_1d`
    * :py:func:`numpy.percentile`
    * :py:meth:`xarray.Dataset.quantile`
    * :py:meth:`xarray.DataArray.quantile`
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

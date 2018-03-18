
from __future__ import absolute_import

import numpy as np

from impactlab_tools.utils.weighting import weighted_quantile_xr, _get_weights


def acp_quantiles(
        data,
        rcp,
        quantiles=[0.05, 0.17, 0.5, 0.83, 0.95],
        values_sorted=False,
        dim='model'):
    """
    Compute quantiles of an xarray distribution using ACP weights

    .. NOTE ::

        This function does not control for the number of samples of each model.
        If they are not constant across models provide a correctly weighted
        weights array to :py:func:`utils.weighting.weighted_quantile_xr`.
        We would like to fix this. If you have a good fix we'd love a PR :)

    Parameters
    ----------

    data : DataArray or Dataset
        :py:class:`xarray.DataArray` or :py:class:`xarray.Dataset` with data
        indexed by ACP model along the dimension ``dim``. If a Dataset is
        passed, ``acp_quantiles`` computes the weighted quantile for each
        variable in the ``Dataset`` that is indexed by ``dim``.

    rcp : str
        RCP weights/models to use ('rcp45', 'rcp85')

    quantiles : list-like, optional
        quantiles of distribution to return. quantiles should be in [0, 1].
        Default [0.05, 0.17, 0.5, 0.83, 0.95].

    values_sorted : bool, optional
        if True, then will avoid sorting of initial array. default False.

    dim : str, optional
        dimension along which to retrieve quantiles. The indices of this
        dimension should be valid (case insensitive) ACP climate models.
        Default: `'model'`.

    Returns
    -------

    DataArray or Dataset
        returns a new :py:class:`~xarray.DataArray` or
        :py:class:`~xarray.Dataset` with quantiles computed from weighted
        distribution along a new dimension ``quantile`` and dimension ``dim``
        dropped.

    See also
    --------

    * :py:func:`.gcp.dist.acp_quantiles`
    * :py:func:`.utils.weighting.weighted_quantile_xr`
    * :py:func:`.utils.weighting.weighted_quantile`
    * :py:func:`.utils.weighting.weighted_quantile_1d`
    * :py:func:`numpy.percentile`
    * :py:meth:`xarray.Dataset.quantile`
    * :py:meth:`xarray.DataArray.quantile`
    * :py:meth:`pandas.DataFrame.quantile`
    * :py:meth:`pandas.Series.quantile`

    """

    # prep weight
    sample_weight = _get_weights(project='acp', rcp=rcp)
    sample_weight = sample_weight.rename({'model': dim})

    # prepare arrays of models to align along `dim` (case insensitive)
    models_in_data = data.coords[dim].values
    models_in_data_aligned = np.array([m.lower() for m in models_in_data])

    # align weights to match ordering of models (using lowercase models)
    sample_weight = sample_weight.sel(**{dim: models_in_data_aligned})

    # swap weights coordinate to use model names from data
    sample_weight.coords[dim] = models_in_data

    return weighted_quantile_xr(
        data, quantiles, sample_weight=sample_weight, dim=dim)

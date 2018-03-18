
from __future__ import absolute_import

import xarray as xr
import os

import impactlab_tools.assets


def population_weighted_mean(
        ds,
        level='state',
        dim='fips',
        year=2012,
        pop=None):
    '''
    Find the population-weighted mean of a county-level xarray DataArray

    Parameters
    ----------
    ds : array
        :py:class:`~xarray.DataArray` to be aggregated. May contain any number
        of dimensions >= 1.

    level : str (optional)
        Level of resolution to aggregate to. May be one of ``'fips'``,
        ``'state'``, ``'state_names'``, ``'state_abbrevs'``, ``'census'``,
        or ``'national'`` (default ``'state'``)

    dim : str (optional)
        dimension to aggregate along (default ``'fips'``)

    year : int (optional)
        population year (or column in the ``pop`` dataset) to use for the
        weights. If not provided, 2012 population is used.

    pop : array (optional)
        :py:class:`~xarray.DataArray` to use for weights. If not provided,
        US Census Bureau 2014 vintage CO-EST2014-alldata.csv estimates from
        the ACP are used

    Returns
    -------
    mean : array
        weighted average aggregated :py:class:`~xarray.DataArray`

    '''

    if pop is None:
        with xr.open_dataset(
            os.path.join(
                os.path.dirname(impactlab_tools.assets.__file__),
                'ACP_county_census_pop.nc')) as pop:

            return pop.load()

        if dim != 'fips':
            pop = pop.rename({'fips': dim})

    return (
        ((ds * pop[str(year)]).groupby(level).sum(dim=dim)) /
        ((pop[str(year)]).groupby(level).sum(dim=dim)))

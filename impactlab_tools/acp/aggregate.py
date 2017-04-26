
import datafs
from impactlab_tools.utils.cache import DataCache


def population_weighted_mean(
        ds,
        level='state',
        dim='fips',
        year=2012,
        api=None,
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

    api : DataAPI (optional)
        :py:class:`datafs.DataAPI` object to use. If not provided, creates a
        new ``DataAPI`` object

    pop : array (optional)
        :py:class:`~xarray.DataArray` to use for weights. If not provided,
        US Census Bureau 2014 vintage CO-EST2014-alldata.csv estimates from
        the ACP are used

    Returns
    -------
    mean : array
        weighted average aggregated :py:class:`~xarray.DataArray`

    '''

    if pop is None and api is None:
        api = datafs.get_api()

    if pop is None:
        pop = _prep_pop_data(api)

        if dim != 'fips':
            pop = pop.rename({'fips': dim})

    return (
        ((ds * pop[str(year)]).groupby(level).sum(dim=dim)) /
        ((pop[str(year)]).groupby(level).sum(dim=dim)))


def _prep_pop_data(api):

    pop_arch = (
        'ACP/integration/socioeconomics/population/' +
        'census/county_census_pop.nc')

    return DataCache.retrieve(pop_arch, api=api)

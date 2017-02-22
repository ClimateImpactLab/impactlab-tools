
import datafs
import xarray as xr
import pandas as pd
import metacsv


def population_weighted_mean(ds, level='state', dim='fips', year=2012, api=None, pop=None):
    if pop is None and api is None:
        api = datafs.get_api()

    if pop is None:
        pop = _prep_pop_data(api)

    if dim != 'fips':
        pop = pop.rename({'fips': dim})

    return (((ds * pop[str(year)]).groupby(level).sum(dim=dim)) /
            ((pop[str(year)]).groupby(level).sum(dim=dim)))


def _prep_pop_data(api):

    pop_arch = api.get_archive('ACP/integration/socioeconomics/' +
        'population/census/county_census_pop.nc')

    try:
        with pop_arch.get_local_path(version='1.0') as f:
            with xr.open_dataset(f) as pop:
                pop.load()

        return pop

    except (KeyError, ValueError):
        pass

    csv_arch = api.get_archive('ACP/integration/socioeconomics/' +
        'population/census/county_census_pop.csv')

    with csv_arch.open('rb', version='0.0.1') as f:
        pop_data = pd.read_csv(f, index_col=range(7))

    pop_data['fips'] = ((lambda x: x['STATE']*1000 + x['COUNTY'])(
        pop_data.reset_index(['STATE', 'COUNTY'], drop=False))).values

    pop_data['state'] = pop_data.reset_index(
        'STATE', drop=False)['STATE'].values

    pop_data['census'] = pop_data.reset_index(
        'DIVISION', drop=False)['DIVISION'].values

    pop_data['national'] = 1

    pop_data = pop_data.set_index(
            ['national', 'census', 'state', 'fips'],
        append=True).reset_index(
            pop_data.index.names, drop=True)

    years = range(2010, 2015)

    pop_data = metacsv.DataFrame(
        pop_data[list(map('POPESTIMATE{}'.format, years))])
    
    pop_data.columns = list(map(str, years))

    pop_data.coords = {
        'fips': None,
        'state': 'fips',
        'census': 'fips',
        'national': 'fips'}

    pop = pop_data.to_xarray()

    with pop_arch.get_local_path(
        bumpversion='major',
        message='2014 vintage CO-EST2014-alldata.csv used in the ACP, ' +
            'prepared for use with xarray Datasets',
        dependencies={'ACP/integration/socioeconomics/' +
            'population/census/county_census_pop.csv': '0.0.1'}) as f:

        pop.to_netcdf(f)

    return pop
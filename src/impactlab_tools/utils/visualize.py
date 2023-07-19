import numpy as np

import matplotlib
import matplotlib.pyplot as plt
import geopandas as gpd

import toolz


def get_shape_path():

    return 'assets/hierid_regions'


@toolz.memoize
def prep_polygons(
        shapepath=None,
        projection='cyl',
        **kwargs):

    if shapepath is None:
        shapepath = get_shape_path()

    gdf  = gpd.read_file(shapepath)
    gdf = gdf.set_index('hierid').geometry

    return gdf

def plot_by_hierid(da, ax=None, legend=True, **kwargs):

    if ax is None:
        ax = plt.subplot(111)

    gdf = prep_polygons().loc[da.hierid]
    gdf['value'] = da.to_series()
    gdf[gdf.value.notnull()].plot('value', legend=legend, **kwargs)

    ax.set_ylabel('Longitude')
    ax.set_xlabel('Latitude')

    return ax

import numpy as np

import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

import toolz


def get_shape():
    
    return '../assets/hierid_regions'
    

@toolz.memoize
def prep_polygons(
        shapepath=None,
        projection='cyl',
        **kwargs):
    
    if shapepath is None:
        shapepath = get_shape()

    m = Basemap(projection=projection, llcrnrlat=-90, urcrnrlat=90,\
            llcrnrlon=-180, urcrnrlon=180, resolution=None, **kwargs)
    m.readshapefile(shapepath, 'shapes', drawbounds=False)
    
    poly = []

    for ii in range(len(m.shapes)):
        poly.append(Polygon(m.shapes[ii], closed=False))
        
    return m, poly

def plot_by_hierid(da, ax=None, clim=None, cmap='jet', **kwargs):

    if ax is None:
        ax = plt.subplot(111)
        
    if clim is None:
        clim = [da.min(), da.max()]
        
    m, poly = prep_polygons()

    hierids = np.array([m.shapes_info[i]['hierid'] for i in range(len(m.shapes))])
    hierids = hierids[np.in1d(hierids, da.hierid)]

    color = da.sel(hierid=hierids).values

    c = PatchCollection(poly, array=color, cmap=cmap, **kwargs)
    c.set_clim(clim)     # set the range of colorbar here
    ax.add_collection(c)
    ax.set_xlim(-180, 180)
    ax.set_ylim(-90,90)
    ax.set_xticks(np.linspace(-180, 180, 7))
    ax.set_yticks(np.linspace(-90, 90, 7))
    ax.set_ylabel('Longitude')
    ax.set_xlabel('Latitude')
    plt.colorbar(c, ax=ax)

    return ax

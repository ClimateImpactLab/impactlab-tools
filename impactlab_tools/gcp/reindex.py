
from __future__ import absolute_import

import os

import numpy as np
import toolz
import xarray as xr

import impactlab_tools.assets

try:
    unicode
except NameError:
    unicode = str


@toolz.memoize
def _get_impactregion_mapping():
    with xr.open_dataset(
            os.path.join(
                os.path.dirname(impactlab_tools.assets.__file__),
                'GCP_impact_regions.nc')
            ) as mapping:

        mapping.load()

    return mapping


def shapenum_to_hierid(data, dim='SHAPENUM', new_dim='hierid', inplace=False):
    '''
    Re-indexes a DataArray or Dataset from SHAPENUM to hierid
    using agglomerated-world-new region definitions

    Parameters
    ----------

    data : Dataset or DataArray
        :py:class:`xarray.Dataset` or :py:class:`xarray.DataArray`
        indexed by a SHAPENUM positional index

    dim : str, optional
        Dimension along which to reindex (default `'SHAPENUM'`)

    new_dim : str, optional
        New name for reindexed dimension (default `'hierid'`)

    inplace : bool, optional
        Modify the Dataset or DataArray in place rather than
        returning a copy (default False)

    Returns
    -------

    reshaped : Dataset or DataArray
        Copy of dataset reindexed by hierid along dimension `dim`


    Example
    -------

    .. code-block:: python

        >>> import numpy as np, xarray as xr
        >>> np.random.seed(1)
        >>> ds = xr.Dataset({'var1': xr.DataArray(
        ...     np.random.random((24378,)),
        ...     dims=('SHAPENUM',),
        ...     coords={'SHAPENUM': np.arange(1,24379)})})
        ...
        >>> reshaped = shapenum_to_hierid(ds)
        >>> reshaped # doctest: +ELLIPSIS
        <xarray.Dataset>
        Dimensions:  (hierid: 24378)
        Coordinates:
          * hierid   (hierid) ...
        Data variables:
            var1     (hierid) float64 0.417 0.7203 0.0001144 ...

        >>> (reshaped.var1.values == ds.var1.values).all()
        True

    '''
    mapping = _get_impactregion_mapping()

    if inplace:
        res = data
    else:
        res = data.copy()

    if not np.in1d(res.coords[dim].values, mapping.SHAPENUM.values).all():
        raise IndexError(
            'Not all values in "{}" found in SHAPENUM'.format(dim))

    res.coords[dim] = (
        mapping
        .set_coords('SHAPENUM')
        .swap_dims({'hierid': 'SHAPENUM'})
        .sel(SHAPENUM=res.coords[dim].astype('float64'))
        .hierid.values)

    res = res.rename({dim: new_dim})
    return res


def hierid_to_shapenum(data, dim='hierid', new_dim='SHAPENUM', inplace=False):
    '''
    Re-indexes a DataArray or Dataset from hierid to SHAPENUM
    using agglomerated-world-new region definitions

    Parameters
    ----------

    data : Dataset or DataArray
        :py:class:`xarray.Dataset` or :py:class:`xarray.DataArray`
        indexed by a hierid impact region name (str) index

    dim : str, optional
        Dimension along which to reindex (default `'hierid'`)

    new_dim : str, optional
        New name for reindexed dimension (default `'SHAPENUM'`)

    inplace : bool, optional
        Modify the Dataset or DataArray in place rather than
        returning a copy (default False)

    Returns
    -------

    reshaped : Dataset or DataArray
        Copy of dataset reindexed by SHAPENUM along dimension `dim`


    Example
    -------

    .. code-block:: python

        >>> import numpy as np, xarray as xr
        >>> np.random.seed(1)
        >>> ds = xr.Dataset({'var2': xr.DataArray(
        ...     np.random.random((10,)),
        ...     dims=('hierid',),
        ...     coords={'hierid':
        ...         ['ABW', 'AFG.1.12', 'AFG.1.R8abddb145b8788ee',
        ...          'AFG.1.R91a8634efe8e02a7', 'AFG.1.Ra6a2bba0a271cb4a',
        ...          'AFG.1.Rcf29900a4c191e96', 'AFG.1.Rd0d6327d56611fba',
        ...          'AFG.10.103', 'AFG.10.106', 'AFG.10.109']})})
        ...
        ...
        >>> reshaped = hierid_to_shapenum(ds)
        >>> reshaped
        <xarray.Dataset>
        Dimensions:   (SHAPENUM: 10)
        Coordinates:
          * SHAPENUM  (SHAPENUM) float64 1.369e+03 5.747e+03 ...
        Data variables:
            var2      (SHAPENUM) float64 0.417 0.7203 0.0001144 ...

        >>> (reshaped.var2.values == ds.var2.values).all()
        True

    '''
    mapping = _get_impactregion_mapping()
    mapping.hierid.values = mapping.hierid.values.astype(unicode)

    if inplace:
        res = data
    else:
        res = data.copy()

    if not np.in1d(res.coords[dim].values, mapping.hierid.values).all():
        raise IndexError(
            'Not all values in "{}" found in "hierid"'.format(dim))

    # Insert SHAPENUM values where "dim" values match with mapping['hierid'].
    # Needed rewrite because `where()` and prev. approach did not work in
    # xarray v0.14.0.
    res.coords[dim] = mapping.isel(
        hierid=mapping['hierid'].isin(res[dim].astype(unicode))
    )['SHAPENUM'].values

    res = res.rename({dim: new_dim})
    return res

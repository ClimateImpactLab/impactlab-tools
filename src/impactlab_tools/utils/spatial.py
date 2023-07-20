import numpy as np
from scipy.spatial import cKDTree

def spatial_fillna_nearest_neighbor(
        da,
        x_dim='longitude',
        y_dim='latitude',
        distance_upper_bound=np.inf,
        inplace=False):
    """
    Fill NaNs in N-D data using nearest-neighbor along x/y dimensions

    Parameters
    ----------
    da : xr.DataArray
        DataArray fo fill NaNs
    x_dim : str, optional
        x dimension in da to use in finding nearest neighbors, default
        `'longitude'`
    y_dim : str, optional
        y dimension in da to use in finding nearest neighbors, default
        `'latitude'`
    distance_upper_bound : float, optional
        Maximum interpolation distance (in units of x and y), default
        np.inf allows interpolation to full grid. If set, returns NaN
        when outside upper bound.
    inplace : bool, optional
        If True, fill data inplace; otherwise return a copy. Default
        False.

    Returns
    -------
    filled : xr.DataArray
        DataArray with filled values returned if inplace is False.
        Otherwise, returns `None`.
    """

    xy_dims = [x_dim, y_dim]
    not_xy_dims = [d for d in da.dims if d not in xy_dims]

    not_all_nans = da.notnull().any(dim=not_xy_dims)

    # get vectors of isnull, notnull flags
    stacked_isnull_flag = (~not_all_nans).stack(obs=xy_dims)
    notnull_flag = (~stacked_isnull_flag.values)
    isnull_flag = stacked_isnull_flag.values

    # get full set of xy points
    xy_full = np.vstack([stacked_isnull_flag[x_dim], stacked_isnull_flag[y_dim]]).T

    # get set of isnull, notnull xy points
    xy_isnull = xy_full[isnull_flag]
    xy_notnull = xy_full[notnull_flag]

    # build kdtree from valid points
    tree = cKDTree(xy_notnull)
    _, null_nn_notnull_indices = tree.query(
        xy_isnull, k=1, distance_upper_bound=distance_upper_bound)

    nearest_neighbor_valid = (null_nn_notnull_indices != len(xy_notnull))

    # build a mask for null values that have been successfully mapped to
    # nearest neighbors
    isnull_and_filled_flag = isnull_flag.copy()
    isnull_and_filled_flag[isnull_flag] = nearest_neighbor_valid

    # build an indexing array with filled values pointing to their nearest neighbors
    isnull_nn_indices = np.arange(xy_full.shape[0])
    isnull_nn_indices[isnull_and_filled_flag] = (
        isnull_nn_indices[notnull_flag][null_nn_notnull_indices[nearest_neighbor_valid]])

    if not inplace:
        da = da.copy()

    all_dims = (not_xy_dims + xy_dims)
    dim_inds = [da.dims.index(d) for d in all_dims]
    res_shapes = [da.shape[i] for i in dim_inds]
    dim_sorter = [all_dims.index(d) for d in da.dims]

    da.values = (
        da
        .stack(obs=xy_dims)
        .transpose(*tuple(list(not_xy_dims) + ['obs']))
        .values[..., isnull_nn_indices]
        .reshape(res_shapes)
        .transpose(*dim_sorter))

    if not inplace:
        return da


from __future__ import absolute_import

import impactlab_tools.gcp.dist
import xarray as xr
import numpy as np

import pytest


@pytest.fixture
def rcp85_models():
    return [
        'surrogate_MRI-CGCM3_01',
        'surrogate_GFDL-ESM2G_01',
        'surrogate_MRI-CGCM3_06',
        'surrogate_GFDL-ESM2G_06',
        'surrogate_MRI-CGCM3_11',
        'surrogate_GFDL-ESM2G_11',
        'ACCESS1-0',
        'CanESM2',
        'CNRM-CM5',
        'GFDL-ESM2G',
        'IPSL-CM5A-LR',
        'MIROC-ESM',
        'MPI-ESM-MR',
        'bcc-csm1-1',
        'CCSM4',
        'CSIRO-Mk3-6-0',
        'GFDL-ESM2M',
        'IPSL-CM5A-MR',
        'MIROC-ESM-CHEM',
        'MRI-CGCM3',
        'BNU-ESM',
        'CESM1-BGC',
        'GFDL-CM3',
        'inmcm4',
        'MIROC5',
        'MPI-ESM-LR',
        'NorESM1-M',
        'surrogate_GFDL-CM3_89',
        'surrogate_CanESM2_89',
        'surrogate_GFDL-CM3_94',
        'surrogate_CanESM2_94',
        'surrogate_GFDL-CM3_99',
        'surrogate_CanESM2_99']


def test_gcp_quantiles_full(rcp85_models):

    test_da = xr.DataArray(
        np.ones(len(rcp85_models), ),
        dims=['model'],
        coords=[rcp85_models])

    impactlab_tools.gcp.dist.gcp_quantiles(
        test_da, rcp='rcp85', dim='model')


def test_gcp_quantiles():
    da = impactlab_tools.gcp.dist.gcp_quantiles(
        xr.DataArray(
            [1, 1, 1],
            dims=['model'],
            coords=[['GFDL-ESM2G', 'MIROC-ESM-CHEM', 'surrogate_CanESM2_99']]),
        rcp='rcp85',
        quantiles=[0.1, 0.4, 0.7, 0.99])

    if len(da.dims) != 1:
        raise ValueError

    if da.shape[0] != 4:
        raise ValueError

    if da.mean(dim='quantile') != 1:
        raise ValueError

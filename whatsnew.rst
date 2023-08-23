What's New
==========

These are new features and improvements of note in each release.

v0.5.0 (August 23, 2023)
------------------------

 - Drop Python 2 support. Requires Python >= v3.7.

 - General documentation build update. Update to readthedocs v2 configuration.

 - Update package dependencies. Require previously unlisted dependencies: ``h5netcdf``, ``geopandas``, ``matplotlib``, ``numpy``, ``pandas``, ``scipy``, ``xarray``.

 - Fix error from bad coordinate assignment in ``impactlab_tools.gcp.reindex.hierid_to_shapenum()``.

 - Remove dependence on ``toolz`` package.

 - Quick and dirty code style cleanup.

 - Replace ``flake8`` with ``ruff`` for code quality checks.

 - Consolidate requirements files into requirements.txt, purely used for Github Actions CI.

 - Update and refactor into ``src/`` layout with ``pyproject.toml``. Radically simplify the 'meta' of building and maintaining the package.

 - Drop ``tox``.

 - Add LICENSE file to repo. 

 - Remove Travis-CI configurations. Use Github Actions for CI (:issue:`468`)

v0.4.0 (November 14, 2019)
--------------------------

 - add new :py:class:`impactlab_tools.utils.configdict.ConfigDict` class and convenience function :py:func:`impactlab_tools.utils.configdict.gather_configtree` (:issue:`434`)

 - :py:func:`impactlab_tools.utils.files.sharedpath` can now pull the path to "shareddir" path from the ``IMPERICS_SHAREDDIR`` shell variable (:issue:`456`). Previously, this was the only entry in "../server.yml", which is still a valid way of specifying "shareddir".

 - fix bug causing assets to be missing from installed package (:issue:`187`)

 - resolve warning message from upstream ``pyyaml`` deprecation (:issue:`447`)

 - work around bug from :py:func:`impactlab_tools.gcp.reindex.hierid_to_shapenum` throwing ``KeyError`` when using ``xarray`` v0.14.0 (:issue:`455`)

 - minor fixes to documentation

v0.3.1 (March 19, 2018)
-----------------------

 - "stability and performance improvements"

v0.3.0 (March 17, 2018)
-----------------------

 - drop DataFS dependency and move all data dependencies to ``impactlab_tools/assets`` (:issue:`147`)
 - add python 3+ support (:issue:`82`)

v0.2.0 (December 12, 2017)
--------------------------

 - add paralog
 - add mapping utilities in :py:mod:`impactlab_tools.utils.visualize`

v0.1.0 (September 8, 2017)
--------------------------

  - fix bug causing docs to fail when importing conda packages (:issue:`67`)
  - add missing documentation for utils.binning module (finalizes :issue:`59`)
  - add :py:func:`impactlab_tools.gcp.dist.gcp_quantiles` function (:issue:`16`)
  - allow :py:func:`~impactlab_tools.utils.weighting.weighted_quantiles_xr` to broadcast across variables in a dataset (:issue:`78`)
  - add reindexing functions :py:func:`impactlab_tools.gcp.reindex.shapenum_to_hierid` and :py:func:`impactlab_tools.gcp.reindex.hierid_to_shapenum` (:issue:`80`)

v0.0.6 (August 16, 2017)
------------------------

  - add bin-by-value function (see :py:func:`impactlab_tools.utils.binning.binned_statistic_1d`) (:issue:`59`)

v0.0.5 (February 23, 2017)
----------------------------

  - add tests, doctests, docs build tests, codacy, codecov (:issue:`3`)
  - docs now build, whatsnew added (:issue:`4`)
  - add version tracking code in :py:mod:`impactlab_tools.utils.versions` (:pull:`1`)
  - ``versions.py`` moved from ``os`` to ``utils`` submodule (:issue:`13`)
  - docs badge updated to point correctly to readthedocs.io (:issue:`12`)
  - package dependencies pinned, pyup setup (:pull:`8`)
  - restructure docs and add sphinx-autoapi documentation (:issue:`15`)
  - minor formatting and bug fixes
  - pypi version pinned in travis.yml


See the issue tracker on GitHub for a complete list.


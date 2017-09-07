What's New
==========

These are new features and improvements of note in each release.

v0.0.7 (Current version)
------------------------

  - fix bug causing docs to fail when importing conda packages (:issue:`67`)
  - add missing documentation for utils.binning module (finalizes :issue:`59`)
  - add :py:func:`impactlab_tools.gcp.dist.gcp_quantiles` function (:issue:`16`)
  - allow :py:func:`~impactlab_tools.utils.weighting.weighted_quantiles_xr` to broadcast across variables in a dataset (:issue:`78`)

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


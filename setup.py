#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements_install = [
    ]

requirements_test = [
    'Sphinx>=1.4.1',
    'sphinx_rtd_theme>=0.1.0',
    'pip>=8.0',
    'wheel>=0.27',
    'flake8>=2.0',
    'tox>=2.3.0',
    'coverage>=4.0',
    'pytest>=3.0',
    'pytest_cov>=2.0',
    'pytest-runner>=2.5',
    'coveralls>=1.0'
    ]

requirements_conda = [
    'numpy>=1.7',
    'pandas>=0.15',
    'netCDF4>=1.1',
    'xarray>=0.8'
]

extras = {
    'test': requirements_test,
    'conda': requirements_conda
}


setup(
    name='impactlab-tools',
    version='0.4.0',
    description="Python tools for Climate Impact Lab developers",
    long_description=readme,
    author="Climate Impact Lab",
    author_email="mdelgado@rhg.com",
    url='https://pypi.python.org/pypi',
    packages=find_packages(
        exclude=['*.tests', '*.tests.*', 'tests.*', 'tests']),
    package_dir={'impactlab_tools':
                 'impactlab_tools'},
    package_data={'impactlab-tools': ['assets/*']},
    include_package_data=True,
    install_requires=requirements_install,
    license="MIT license",
    zip_safe=False,
    keywords='impactlab-tools',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6"
    ],
    test_suite='tests',
    setup_requires=['pytest-runner'],
    tests_require=requirements_test,
    extras_require=extras
)

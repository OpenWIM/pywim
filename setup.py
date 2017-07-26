#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'numpy',
    'scipy',
    'matplotlib',
    'pandas',
    'ipython',
    'sqlalchemy',
    'statsmodels',
    'llvmlite',
    'scikit-learn',
    'jupyter',
    'numba',
    'h5py',
    'peakutils'
]

test_requirements = [
    # TODO: put package test requirements here
]


def get_version():
    """Obtain the version number"""
    import imp
    import os
    mod = imp.load_source(
        'version', os.path.join('pywim', '__init__.py')
    )
    return mod.__version__


setup(
    name='pywim',
    version=get_version(),
    description="Open algorithms to use in WIM research",
    long_description=readme + '\n\n' + history,
    author="Ivan Ogasawara",
    author_email='ivan.ogasawara@gmail.com',
    url='https://github.com/OpenWIM/pywim',
    packages=[
        'pywim',
    ],
    package_dir={'pywim':
                 'pywim'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='pywim',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)

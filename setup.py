# -*- coding: utf-8 -*-
#
import codecs
import os

from setuptools import find_packages, setup

# https://packaging.python.org/single_source_version/
base_dir = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(base_dir, 'complex_colormap', '__about__.py'),
          'rb') as f:
    exec(f.read(), about)


def read(fname):
    try:
        content = codecs.open(
            os.path.join(os.path.dirname(__file__), fname),
            encoding='utf-8'
        ).read()
    except Exception:
        content = ''
    return content


setup(
    name='complex_colormap',
    version=about['__version__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    packages=find_packages(),
    description='Color maps for complex-valued functions',
    long_description=read('README.rst'),
    url=about['__website__'],
    download_url='https://github.com/endolith/complex_colormap/releases',
    license=about['__license__'],
    platforms='any',
    install_requires=[
        'colorspacious',
        'matplotlib',
        'numpy',
        'scipy',
    ],
    classifiers=[
        about['__status__'],
        about['__license__'],
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Physics',
    ]
)

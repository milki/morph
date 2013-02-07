#!/usr/bin/python
# Setup file for morph

try:
    from setuptools import setup
    has_setuptools = True
except ImportError:
    from distutils.core import setup
    has_setuptools = False
from distutils.core import Distribution

morph_version_string = '0.0.1'

include_dirs = []
setup_kwargs = {}

if has_setuptools:
    setup_kwargs['test_suite'] = 'morph.tests.test_suite'

setup(name='morph',
      description='Python Batch Renamer',
      keywords='git',
      version=morph_version_string,
      url='http://github.com/milki/morph',
      download_url='http://github.com/milki/morph/tags/morph-%s.tar.gz' %
                   morph_version_string,
      license='GPLv2 or later',
      author='milki',
      author_email='milki@rescomp.berkeley.edu',
      long_description="""
      Batch File Renamer
      """,
      packages=['morph', 'morph.tests'],
      scripts=[],
      ext_modules = [],
      **setup_kwargs
      )

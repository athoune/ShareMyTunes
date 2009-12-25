#!/usr/bin/env python
# -*- coding: utf8 -*-

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup

setup(name='shareMyTunes',
      version='0.1',
      license='GPL-3',
      description='iTunes db share',
      author='Mathieu Lecarme',
      author_email='mathieu@garambrogne.net',
      url='http://github.com/athoune/ShareMyTunes',
      packages=['shareMyTunes'],
      package_dir={'': 'src/'},
      #scripts=['src/toto'],
      install_requires=["genshi", "whoosh"]
     )

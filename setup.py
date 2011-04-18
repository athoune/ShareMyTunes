#!/usr/bin/env python
# -*- coding: utf8 -*-

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup

setup(name='shareMyTunes',
	version='0.2.1',
	license='GPL-3',
	description='iTunes db share',
	author='Mathieu Lecarme',
	author_email='mathieu@garambrogne.net',
	url='http://github.com/athoune/ShareMyTunes',
	packages=[
		'shareMyTunes',
		'shareMyTunes.index',
		'shareMyTunes.reader',
		'shareMyTunes.web'
	],
	package_dir={'': 'src/'},
	package_data={'shareMyTunes.web' : ['data/*.*']},
	scripts=['bin/shareMyTunesd', 'bin/shareMyTunes-index'],
	install_requires=[
		"genshi",
		"whoosh",
		"mutagen",
		"pybonjour",
		"bottle",
		"opensearch"],
	app=['src/shareMyTunes/server.py']
)

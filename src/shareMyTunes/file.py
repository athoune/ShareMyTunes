#!/usr/bin/env python

import os.path

from mutagen.id3 import ID3, ID3NoHeaderError

from filter import Filter

__author__ = "mlecarme"

"""
[TODO] multiple artworks
[TODO] old artwork format

http://code.google.com/p/mutagen/wiki/Tutorial
"""
class Dummy:
	"""
	A fake id3 object
	"""
	def get(self, key):
		return None

class File:
	"""File with id3
	"""
	def __init__(self, path):
		self.path = path
		self._id3 = None
	def id3(self):
		if self._id3 == None:
			try:
				self._id3 = ID3(self.path)
			except ID3NoHeaderError:
				self._id3 = Dummy()
		return self._id3
	def artwork(self):
		"artwork (png or jpg)"
		return self.id3().get('APIC:')
	def cddb(self):
		"cddb id tag"
		return self.id3().get(u"COMM:iTunes_CDDB_IDs:'eng'")

class ID3Filter(Filter):
	def filter(self, item):
		if item.has_key('path'):
			f = File(item['path'])
			item['artwork'] = f.artwork() != None
			_, ext = os.path.splitext(item['path'])
			item['extension'] = ext[1:]
		else:
			item['artwork'] = False
		return item

if __name__ == '__main__':
	import sys
	f = File(sys.argv[1])
	print "cddb:   ", f.cddb()
	art = f.artwork()
	if art != None:
		print "artwork:", art.mime

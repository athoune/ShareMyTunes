#!/usr/bin/env python

from mutagen.id3 import ID3

__author__ = "mlecarme"
__version__ = "0.1"

"""
[TODO] multiple artworks
[TODO] old artwork format

http://code.google.com/p/mutagen/wiki/Tutorial
"""

class File:
	"""File with id3
	"""
	def __init__(self, path):
		self.path = path
		self._id3 = None
	def id3(self):
		if self._id3 == None:
			self._id3 = ID3(self.path)
		return self._id3
	def artwork(self):
		"artwork (png or jpg)"
		return self.id3().get('APIC:')
	def cddb(self):
		"cddb id tag"
		return self.id3().get(u"COMM:iTunes_CDDB_IDs:'eng'")

if __name__ == '__main__':
	import sys
	f = File(sys.argv[1])
	print "cddb:   ", f.cddb()
	art = f.artwork()
	if art != None:
		print "artwork:", art.mime

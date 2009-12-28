#!/usr/bin/env python

import urllib
from urlparse import urlparse
import os.path

from whoosh.support.charset import charset_table_to_dict, default_charset
from genshi.input import XMLParser, START, TEXT, END

__author__ = "mlecarme"
__version__ = "0.1"

no_accent = charset_table_to_dict(default_charset)

"""
[TODO] indexing artworks
"""
class ItunesParser:
	"""
	Event based iTunes XML parser
	"""
	def __init__(self, path):
		self.stream = XMLParser(open(path,'r'))
	def __iter__(self):
		ouvrant = None
		indentation = 0
		tracks = False
		valeur = False
		piste = {}
		albums = set()
		artists = set()
		for kind, data, pos in self.stream:
			if kind == START:
				ouvrant = data[0].localname
				indentation += 1
			if kind == END:
				indentation -= 1
			if ouvrant == 'key' and kind == TEXT:
				key = data.strip()
				if not tracks and key == 'Tracks':
					tracks = True
					mini = indentation
				if tracks:
					if indentation < mini -1:
						break
				valeur = True
				#print indentation, data
			if kind == START and indentation == 4:
				if piste != {} and 'Persistent ID' in piste and piste['Name'] != None:
					piste['Name'] = piste['Name'].strip(" \n\t\r")
					if piste['Name'] != '':
						track = {
							'trackId'            : piste['Track ID'],
							'name'               : piste['Name'],
							'artist'             : piste.get('Artist', None),
							'album'              : piste.get('Album', None),
							'genre'              : piste.get('Genre', None),
							'kind'               : piste.get('Kind', None),
							'size'               : piste.get('Size', None),
							'totalTime'          : piste.get('Total Time', None),
							'trackNumber'        : piste.get('Track Number', None),
							'dateModified'       : piste.get('Date Modified', None),
							'dateAdded'          : piste.get('Date Added', None),
							'bitRate'            : piste.get('Bit Rate', None),
							'sampleRate'         : piste.get('Sample Rate', None),
							'persistentID'       : piste['Persistent ID'],
							'trackType'          : piste.get('Track Type', None),
							'location'           : piste.get('Location', None),
							'fileFolderCount'    : piste.get('File Folder Count', None),
							'libraryFolderCount' : piste.get('Library Folder Count', None)
						}
						'''
						track['cleanPath'] = "%s/%s/%s" % (
							track['artist'].translate(no_accent), 
							track['album'].translate(no_accent),
							track['name'].translate(no_accent))
						'''
						if track['location'] != None:
							url = urlparse(track['location'])
							path = urllib.unquote(url.path)
							if url.scheme == 'file' and os.path.isfile(path) :
								track['path'] = path
						yield track
				piste = {}
			if ouvrant != 'key' and kind == TEXT and valeur and indentation == 5:
				#print "	 ", key, ":(", ouvrant, ")", unicode(data).encode('latin1', 'ignore')
				piste[key] = data
				valeur = False

if __name__ == '__main__':
	parser = ItunesParser(os.path.expanduser('~/Music/iTunes/iTunes Music Library.xml'))
	for a in parser:
		print a
	#parser.parse()
	

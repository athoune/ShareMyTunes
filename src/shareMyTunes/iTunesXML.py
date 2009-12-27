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
	def piste(self, trackId, name, artist, album, genre, kind, size, total_time,
			track_number, date_modified, date_added, bit_rate, sample_rate,
			persistant_id, track_type, location, file_folder_count,
			library_folder_count):
		try:
			print 'piste :', name
		except UnicodeEncodeError :
			pass
	def album(self, album):
		try:
			print 'album   :', album
		except UnicodeEncodeError :
			pass
	def artiste(self, artiste):
		try:
			print 'artiste :', artiste
		except UnicodeEncodeError :
			pass
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
				if tracks == False and key == 'Tracks':
					tracks = True
					min = indentation
				if tracks:
					if indentation < min -1:
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
						"""
						self.piste(
							piste['Track ID'],
							piste['Name'],
							piste.get('Artist', None),
							piste.get('Album', None),
							piste.get('Genre', None),
							piste.get('Kind', None),
							piste.get('Size', None),
							piste.get('Total Time', None),
							piste.get('Track Number', None),
							piste.get('Date Modified', None),
							piste.get('Date Added', None),
							piste.get('Bit Rate', None),
							piste.get('Sample Rate', None),
							piste['Persistent ID'],
							piste.get('Track Type', None),
							piste.get('Location', None),
							piste.get('File Folder Count', None),
							piste.get('Library Folder Count', None)
							)
						if 'Artist' in piste and piste['Artist'] not in artists:
							artists.add(piste['Artist'])
							self.artiste(piste['Artist'])
						if 'Album' in piste and piste['Album'] not in albums:
							albums.add(piste['Album'])
							self.album(piste['Album'])
						"""
				piste = {}
			if ouvrant != 'key' and kind == TEXT and valeur and indentation == 5:
				#print "	 ", key, ":(", ouvrant, ")", unicode(data).encode('latin1', 'ignore')
				piste[key] = data
				valeur = False

if __name__ == '__main__':
	import os.path
	parser = ItunesParser(os.path.expanduser('~/Music/iTunes/iTunes Music Library.xml'))
	for a in parser:
		print a
	#parser.parse()
	

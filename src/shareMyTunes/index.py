#!/usr/bin/env python

from iTunesXML import ItunesParser
from whoosh.fields import Schema, STORED, ID, KEYWORD, TEXT
import os.path
from whoosh.filedb.filestore import FileStorage
from whoosh.qparser import QueryParser

__author__ = "mlecarme"
__version__ = "0.1"

class Index:
	def __init__(self, path, index='index'):
		self.path = path
		self.schema = Schema(
			trackId = ID(stored=True),
			name=TEXT(stored=True),
			artist=TEXT(stored=True),
			album=TEXT(stored=True),
			genre=KEYWORD)
		if not os.path.exists(index):
			self.empty = True
			os.mkdir(index)
			self.ix = FileStorage(index).create_index(self.schema)
		else:
			self.empty = False
			self.ix = FileStorage(index).open_index()
		self.parser = QueryParser("name", schema = self.schema)
		self.searcher = self.ix.searcher()
		self.reader = self.ix.reader()
	def index(self):
		if self.empty:
			self.writer = self.ix.writer()
			xml_parser = ItunesParser(self.path)
			xml_parser.piste = self.handle_piste
			xml_parser.parse()
		else :
			print "already indexed"
	def handle_piste(self, trackId, name, artist, album, genre, kind, size, total_time,
		track_number, date_modified, date_added, bit_rate, sample_rate,
		persistant_id, track_type, location, file_folder_count, 
		library_folder_count):
			self.writer.add_document(trackId = trackId, name=name,
				artist=artist, album=album, genre=genre)
			self.writer.commit()
	def query(self, query):
		q = self.parser.parse(query)
		print q
		return self.searcher.search(q)
if __name__ == '__main__':
	import os.path
	index = Index(os.path.expanduser('~/Music/iTunes/iTunes Music Library.xml'))
	index.index()
	q = index.query(u'tokyo*')
	print q
	for response in q:
		print "\t", response
	#print dir(index.searcher)
	print "Genres:", list(index.reader.lexicon('genre'))
	#print list(index.reader.most_frequent_terms("name", 5))


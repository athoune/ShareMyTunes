#!/usr/bin/env python

from iTunesXML import ItunesParser
from whoosh.fields import Schema, STORED, ID, KEYWORD, TEXT
import os.path
from whoosh.filedb.filestore import FileStorage

class Index:
	def __init__(self, path, index='index'):
		self.parser = ItunesParser(path)
		self.schema = Schema(
			trackId = ID(stored=True),
			name=TEXT(stored=True),
			artist=TEXT(stored=True),
			album=TEXT(stored=True),
			genre=KEYWORD)
		if not os.path.exists(index):
			os.mkdir(index)
		self.storage = FileStorage(index)
		self.ix = self.storage.create_index(self.schema)
	def index(self):
		self.writer = self.ix.writer()
		self.parser.piste = self.piste
		self.parser.parse()
	def piste(self, trackId, name, artist, album, genre, kind, size, total_time,
		track_number, date_modified, date_added, bit_rate, sample_rate,
		persistant_id, track_type, location, file_folder_count, 
		library_folder_count):
			self.writer.add_document(trackId = trackId, name=name,
				artist=artist, album=album, genre=genre)
			self.writer.commit()
if __name__ == '__main__':
	import os.path
	index = Index(os.path.expanduser('~/Music/iTunes/iTunes Music Library.xml'))
	index.index()


#!/usr/bin/env python

import os.path
import sys

from whoosh.fields import Schema, STORED, ID, KEYWORD, TEXT
from whoosh.filedb.filestore import FileStorage
from whoosh.qparser import MultifieldParser

from iTunesXML import ItunesParser
from file import ID3Filter

__author__ = "mlecarme"
__version__ = "0.1"

def boolean(bool):
	if bool:
		return u"1"
	return u"0"
class Index:
	def __init__(self, path, folder=os.path.expanduser('~/Library/Application Support/Share my tunes')):
		self.path = path
		self.schema = Schema(
			trackId = ID(stored=True),
			name=TEXT(stored=True),
			artist=TEXT(stored=True),
			album=TEXT(stored=True),
			genre=KEYWORD(stored=True),
			location=STORED,
			trackNumber=STORED,
			bitRate=ID(stored=True),
			artwork=KEYWORD(stored=True)
			)
		if not os.path.exists(folder):
			os.makedirs(folder)
		index = "%s/index" % folder
		if not os.path.exists(index):
			self.empty = True
			os.makedirs(index)
			self.ix = FileStorage(index).create_index(self.schema)
		else:
			self.empty = False
			self.ix = FileStorage(index).open_index()
		self.parser = MultifieldParser(["name", "album", "artist"], schema = self.schema)
		self.searcher = self.ix.searcher()
		self.reader = self.ix.reader()
	def index(self):
		if self.empty:
			self.writer = self.ix.writer()
			pipe = ID3Filter()
			#[TODO] using itunes info for artwork?
			cpt = 0
			for track in pipe(ItunesParser(self.path)):
				if track['album'] != None : 
					album = track['album'].encode('ascii', 'ignore')
				else:
					album = ""
				#print track['artwork'], "[%s]" % album, track['name'].encode('ascii', 'ignore')
				if cpt % 20 == 0:
					sys.stdout.write("\n%i " %cpt)
				sys.stdout.write('#')
				self.writer.add_document(
					trackId = track['trackId'], name=track['name'],
					artist=track['artist'], album=track['album'],
					genre=track['genre'], location=track['location'],
					artwork=boolean(track['artwork']),
					trackNumber=track['trackNumber'], bitRate=track['bitRate']
				)
				if cpt % 100 == 0:
					self.writer.commit()
				cpt += 1
			print "\n\n%i tracks indexed" % cpt
			self.writer.commit()
		else :
			print "already indexed"
		self.ix.optimize()
	def query(self, query):
		q = self.parser.parse(query)
		return self.searcher.search(q, sortedby=("album", "name"))
if __name__ == '__main__':
	import os.path
	index = Index(os.path.expanduser('~/Music/iTunes/iTunes Music Library.xml'))
	index.index()
	q = index.query(u'tokyo*')
	print "q:", dir(q)
	for response in q:
		print "\t", response
	#print dir(index.searcher)
	print "Genres:", list(index.reader.lexicon('genre'))
	#print list(index.reader.most_frequent_terms("name", 5))


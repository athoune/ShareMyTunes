#!/usr/bin/env python

import os.path
import sys

from whoosh.fields import Schema, STORED, ID, KEYWORD, TEXT
from whoosh.filedb.filestore import FileStorage
import whoosh.index
from whoosh.qparser import MultifieldParser

from shareMyTunes.reader.iTunesXML import ItunesParser
import shareMyTunes.reader.file

__author__ = "mlecarme"

def boolean(bool):
	if bool:
		return u"1"
	return u"0"

class Index:
	def __init__(self, path='~/Music/iTunes/iTunes Music Library.xml', folder='~/Library/Application Support/Share my tunes'):
		self.path = os.path.expanduser(path)
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
		self.parser = MultifieldParser(["name", "album", "artist"], schema = self.schema)
		self.folder = "%s/index" % os.path.expanduser(folder)
		self.empty = not whoosh.index.exists_in(self.folder)
		self.ix = None
	def index(self):
		if self.empty:
			if not os.path.exists(self.folder):
				os.makedirs(self.folder)
			st = FileStorage(self.folder)
			ix = st.create_index(self.schema)
			w = ix.writer()
			w.add_document(name = u"beuha")
			pipe = file.ID3Filter()
			#[TODO] using itunes info for artwork?
			cpt = 0
			for track in pipe(ItunesParser(self.path)):
				if track['album'] != None : 
					album = track['album'].encode('ascii', 'ignore')
				else:
					album = ""
				#print track['artwork'], "[%s]" % album, track['name'].encode('ascii', 'ignore')
				if cpt % 20 == 0:
					print "\n%i " %cpt,
				print '#',
				#print track['album'], track['name']
				w.add_document(
					trackId = track['trackId'], name=track['name']
					,artist=track['artist'], album=track['album'],
					genre=track['genre'], location=track['location'],
					artwork=boolean(track['artwork']),
					trackNumber=track['trackNumber'], bitRate=track['bitRate']
				)
				#if cpt % 100 == 1:
				#	w.commit()
				cpt += 1
			print "\n\n%i tracks indexed" % cpt
			w.commit()
			ix.optimize()
			ix.close()
		else :
			print "already indexed"
	def query(self, query):
		if self.ix == None:
			self.ix = FileStorage(self.folder).open_index()
		q = self.parser.parse(query)
		return self.ix.searcher().search(q, sortedby=("album", "name"), limit=None)
if __name__ == '__main__':
	import os.path
	index = Index()
	index.index()
	q = index.query(u'tokyo*')
	print "q:", dir(q)
	for response in q:
		print "\t", response
	print list(index.query(u'genre:"films" OR genre:soundtrack'))
	#print dir(index.searcher)
	#print "Genres:", list(index.reader.lexicon('genre'))
	#print list(index.reader.most_frequent_terms("name", 5))


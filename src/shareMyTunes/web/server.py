#!/usr/bin/env python

from wsgiref.simple_server import make_server
from wsgiref.util import request_uri, FileWrapper
from urlparse import urlparse, parse_qs
import json
import os.path
import urllib
from cStringIO import StringIO

from whoosh.support.charset import charset_table_to_dict, default_charset

from shareMyTunes.reader.file import File

import bonjour
from shareMyTunes.index import Index

__author__ = "mlecarme"

"""
[TODO] opensearch XML format
[TODO] woosh spell checking
"""

OK = '200 OK'
NOT_FOUND = '404 NOT FOUND'
PLAIN = 'text/plain'
HTML = 'text/html'

MIME = {
	'css' :'text/css',
	'js'  :'application/x-javascript',
	'html':'text/html',
	'ico' :'image/x-icon',
	'png' :'image/png',
	'jpg' :'image/jpg',
	'gif' :'image/gif',
	'swf' :'application/x-shockwave-flash',
	'mp3' :'audio/mpeg',
	'm4a' :'audio/mpeg',
	'zip' :'application/zip'
}

no_accent = charset_table_to_dict(default_charset)
for letter in iter(" /\\:"):
	no_accent[ord(letter)] = u'_'

class JsonList:
	def __init__(self, list):
		self.list = list
		self.length = len(list)
	def __iter__(self):
		yield '['
		i = self.length
		for elem in self.list:
			yield json.dumps(elem, separators=(',', ':'))
			if i > 1:
				yield ","
			i -= 1
		yield ']'

class JsonResponse:
	def __init__(self, response):
		self.response = response
		self.length = len(response)
	def __iter__(self):
		yield '['
		cpt = 0
		for r in self.response:
			rr = {}
			for key in r:
				rr[key] = r[key]
			# print r['name']
			if r['album'] == None:
				continue
			cpt += 1
			rr['docNum'] = self.response.docnum(cpt-1)
			rr['clean_path'] = "%s/%s/%s" % (
				r['artist'].translate(no_accent), 
				r['album'].translate(no_accent),
				r['name'].translate(no_accent))
			del rr['location']
			print rr
			yield json.dumps(rr, separators=(',', ':'))
			print cpt, self.length
			if cpt < self.length:
				yield ","
		yield ']'

class ShareMyTunes_app:
	def __init__(self, db=os.path.expanduser('~/Music/iTunes/iTunes Music Library.xml')):
		self.index = Index(db)
		self.index.index()
		self.root = os.path.dirname(__file__)
	def __call__(self, environ, start_response):
		#print environ
		print start_response
		uri = urlparse(request_uri(environ))
		print uri
		q = parse_qs(uri.query)
		if uri.path == '/query':
			return self.query(start_response, q)
		if uri.path == '/':
			start_response(OK, [('Content-type', HTML)])
			return FileWrapper(open(self.root + '/data/index.html', 'r'))
		uris = uri.path.split('/')[1:]
		print uris
		if uris[0] == 'data' and len(uris) == 2:
			f = self.root + '/data/' + uris[1]
			if not os.path.isfile(f):
				start_response(NOT_FOUND, PLAIN)
				return [uris[1] + " doesn't exist"]
			r, ext = os.path.splitext(f)
			start_response(OK, [('Content-type', MIME[ext[1:]])])
			return FileWrapper(open(f, 'r'))
		if uris[0] == 'track':
			return self.track(start_response, uris[1], uris[2])
		# The returned object is going to be printed
		start_response(OK, [('Content-type', PLAIN)])
		return ["Hello iTunes"]
	def query(self, start_response, query, header = None):
		start_response(OK, [('Content-type', PLAIN)])
		response = self.index.query(unicode(query['q'][0]))
		return JsonResponse(response)
	def track(self, start_response, track, type = 'data'):
		t = self.index.reader.stored_fields(int(track))
		u = urlparse(t['location'])
		print u.scheme
		f = urllib.unquote(u.path)
		if not os.path.isfile(f):
			start_response(NOT_FOUND, [('Content-type', PLAIN)])
			print "NOT FOUND : %s" % f
			return ["%s not found" % track]
		if type == 'music':
			_, ext = os.path.splitext(f)
			start_response(OK, [('Content-type', MIME[ext[1:]])])
			print "serving %s as %s" % (f, ext)
			return FileWrapper(open(f, 'r'))
		if type == 'data':
			start_response(OK, [('Content-type', PLAIN)])
			return json.dumps(t)
		if type == 'artwork':
			ff = File(f)
			artwork = ff.artwork()
			if artwork == None:
				start_response(NOT_FOUND, [('Content-type', PLAIN)])
				return ["No artwork for %s" % track]
			print artwork.mime
			start_response(OK, [('Content-type', str(artwork.mime))])
			return FileWrapper(StringIO(artwork.data))

def local():
	bonjour.broadcast()
	httpd = make_server('', 8000, ShareMyTunes_app())
	print "Serving on port 8000..."
	# Serve until process is killed
	httpd.serve_forever()

if __name__ == '__main__':
	local()

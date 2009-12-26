#!/usr/bin/env python

from wsgiref.simple_server import make_server
from wsgiref.util import request_uri, FileWrapper
from urlparse import urlparse, parse_qs
import json
import os.path

from index import Index

__author__ = "mlecarme"
__version__ = "0.1"

OK = '200 OK'
NOT_FOUND = '404 NOT FOUND'
PLAIN = 'text/plain'
HTML = 'text/html'

MIME = {
	'css' :'text/css',
	'js'  :'application/x-javascript',
	'html':'text/html',
	'ico' :'image/x-icon',
	'png' :'image/png'
}

class ShareMyTunes_app:
	def __init__(self, db='~/Music/iTunes/iTunes Music Library.xml'):
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
			return self.root(q)
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

		# The returned object is going to be printed
		start_response(OK, [('Content-type', PLAIN)])
		return ["Hello iTunes"]
	def query(self, query, header = None):
		start_response(OK, [('Content-type', PLAIN)])
		response = self.index.query(unicode(query['q'][0]))
		tas = []
		for r in response:
			print r
			tas.append(r)
		print tas
		return json.dumps(tas)

if __name__ == '__main__':
	print __file__
	httpd = make_server('', 8000, ShareMyTunes_app())
	print "Serving on port 8000..."

	# Serve until process is killed
	httpd.serve_forever()
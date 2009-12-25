#!/usr/bin/env python

from wsgiref.simple_server import make_server
from wsgiref.util import request_uri
from urlparse import urlparse, parse_qs
import json

from index import Index

__author__ = "mlecarme"
__version__ = "0.1"

class ShareMyTunes_app:
	def __init__(self, db='~/Music/iTunes/iTunes Music Library.xml'):
		self.index = Index(db)
		self.index.index()
	def __call__(self, environ, start_response):
		#print environ
		print start_response
		uri = urlparse(request_uri(environ))
		print uri
		q = parse_qs(uri.query)
		status = '200 OK' # HTTP Status
		headers = [('Content-type', 'text/plain')] # HTTP Headers
		start_response(status, headers)
		if uri.path == '/':
			return self.root(q)

		# The returned object is going to be printed
		return ["Hello iTunes"]
	def root(self, query, header = None):
		response = self.index.query(unicode(query['q'][0]))
		tas = []
		for r in response:
			print r
			tas.append(r)
		print tas
		return json.dumps(tas)

if __name__ == '__main__':
	httpd = make_server('', 8000, ShareMyTunes_app())
	print "Serving on port 8000..."

	# Serve until process is killed
	httpd.serve_forever()
#!/usr/bin/env python

from wsgiref.simple_server import make_server
from wsgiref.util import request_uri, FileWrapper
from urlparse import urlparse, parse_qs
import json
import os.path
import select
import urllib

from file import File

import pybonjour

from index import Index

__author__ = "mlecarme"
__version__ = "0.1"

"""
[TODO] opensearch XML format
[TODO] woosh spell checking
[TODO] artwork display
[TODO] 
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
	'swf' :'application/x-shockwave-flash',
	'mp3' :'audio/mpeg',
	'm4a' :'audio/mpeg'
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
		tas = []
		cpt = 0
		for r in response:
			print r
			r['docNum'] = response.docnum(cpt)
			tas.append(r)
			cpt += 1
		print tas
		return json.dumps(tas)
	def track(self, start_response, track, type = 'data'):
		t = self.index.reader.stored_fields(int(track))
		u = urlparse(t['location'])
		print u.scheme
		f = urllib.unquote(u.path)
		if type == 'music':
			_, ext = os.path.splitext(f)
			start_response(OK, [('Content-type', MIME[ext[1:]])])
			print "serving %s as %s" % (f, ext)
			return FileWrapper(open(f, 'r'))
		if type == 'data':
			start_response(OK, [('Content-type', PLAIN)])
			return json.dumps(t)
		if type == 'artworks':
			ff = File(f)
			artwork = ff.artwork()
			if artwork == None:
				start_response(NOT_FOUND, [('Content-type', PLAIN)])
				return
			print artwork.mime
			start_response(OK, [('Content-type', str(artwork.mime))])
			return artwork.data

def register_callback(sdRef, flags, errorCode, name, regtype, domain):
	if errorCode == pybonjour.kDNSServiceErr_NoError:
		print 'Registered service:'
		print '  name    =', name
		print '  regtype =', regtype
		print '  domain  =', domain

if __name__ == '__main__':
	sdRef = pybonjour.DNSServiceRegister(name = 'Share my tunes',
			                                     regtype = '_http._tcp',
			                                     port = 8000,
			                                     callBack = register_callback)
	ready = select.select([sdRef], [], [])
	if sdRef in ready[0]:
		pybonjour.DNSServiceProcessResult(sdRef)
	sdRef = pybonjour.DNSServiceRegister(name = 'Share my tunes',
		                                     	regtype = '_share_my_tunes._tcp',
												port = 8000,
												callBack = register_callback)
	ready = select.select([sdRef], [], [])
	if sdRef in ready[0]:
		pybonjour.DNSServiceProcessResult(sdRef)
	httpd = make_server('', 8000, ShareMyTunes_app())
	print "Serving on port 8000..."

	# Serve until process is killed
	httpd.serve_forever()
	
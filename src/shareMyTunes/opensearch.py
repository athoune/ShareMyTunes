#!/usr/bin/env python

__author__ = "mlecarme"

from wsgiref.simple_server import make_server
from wsgiref.validate import validator
from wsgiref.util import request_uri
from urlparse import urlparse, parse_qs

from index import Index

class OpenSearchWrapper(object):
	def __init__(self, query, search):
		self.search = search
		self.query = query
	def __iter__(self):
		yield """
			<?xml version="1.0" encoding="UTF-8"?>
			 <rss version="2.0" 
			      xmlns:opensearch="http://a9.com/-/spec/opensearch/1.1/"
			      xmlns:atom="http://www.w3.org/2005/Atom">
			   <channel>
			     <title>Example.com Search: {query}</title>
			     <link>{link}</link>
			     <description>Search results for "{query}"</description>
			     <opensearch:totalResults>{total}</opensearch:totalResults>
			     <opensearch:startIndex>{startIndex}</opensearch:startIndex>
			     <opensearch:itemsPerPage>{itemsPerPage}</opensearch:itemsPerPage>
			     <atom:link rel="search" type="application/opensearchdescription+xml" href="http://example.com/opensearchdescription.xml"/>
			     <opensearch:Query role="request" searchTerms="{query}" startPage="{startPage}" />""".format(
					link='',
					startIndex=0,
					itemsPerPage=0,
					startPage=0,
					query=self.query,
					total=len(self.search)
			)
		for s in self.search:
			yield """
			     <item>
			       <title>{title}</title>
			       <link>{link}</link>
			       <description>
			       </description>
			     </item>
		""".format(title = s['name'], link=s['location']).encode('utf8')
		yield "</channel></rss>"
		

class Opensearchd(object):
	def __init__(self):
		self.index = Index()
	def notFound(self, start_response):
		status = '404 NOT FOUND' # HTTP Status
		headers = [('Content-type', 'text/plain')]#application/rss+xml
		start_response(status, headers)
		return [' ']
	def search(self, start_response, query):
		search = self.index.query(unicode(query))
		status = '200 OK' # HTTP Status
		headers = [('Content-type', 'text/plain')]#application/rss+xml
		start_response(status, headers)
		return OpenSearchWrapper(query, search)

	def __call__(self,environ, start_response):
		uri = urlparse(request_uri(environ))
		if uri.path != "/":
			return self.notFound(start_response)
		else:
			q = parse_qs(uri.query)
			if 'q' not in q:
				return self.notFound(start_response)
			else :
				return self.search(start_response, q['q'][0])

if __name__ == '__main__':
	osd = Opensearchd()
	httpd = make_server('', 8001, osd)
	print "Serving on port 8001..."

	# Serve until process is killed
	httpd.serve_forever()
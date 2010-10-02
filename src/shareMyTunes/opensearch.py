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
		yield u"""
<feed xmlns="http://www.w3.org/2005/Atom" 
	xmlns:opensearch="http://a9.com/-/spec/opensearch/1.1/">
	<title>Example.com Search: {query}</title> 
	<link href="{link}"/>
	<updated>2003-12-13T18:30:02Z</updated>
	<author> 
		<name>Share my tunes</name>
	</author> 
	<id>urn:uuid:60a76c80-d399-11d9-b93C-0003939e0af6</id>
	<opensearch:totalResults>{total}</opensearch:totalResults>
	<opensearch:startIndex>{startIndex}</opensearch:startIndex>
	<opensearch:itemsPerPage>{itemsPerPage}</opensearch:itemsPerPage>
	<opensearch:Query role="request" searchTerms="{query}" startPage="{startPage}" />
	<!--
	<link rel="alternate" href="http://example.com/New+York+History?pw=3" type="text/html"/>
	<link rel="self" href="http://example.com/New+York+History?pw=3&amp;format=atom" type="application/atom+xml"/>
	<link rel="first" href="http://example.com/New+York+History?pw=1&amp;format=atom" type="application/atom+xml"/>
	<link rel="previous" href="http://example.com/New+York+History?pw=2&amp;format=atom" type="application/atom+xml"/>
	<link rel="next" href="http://example.com/New+York+History?pw=4&amp;format=atom" type="application/atom+xml"/>
	<link rel="last" href="http://example.com/New+York+History?pw=42299&amp;format=atom" type="application/atom+xml"/>
	<link rel="search" type="application/opensearchdescription+xml" href="http://example.com/opensearchdescription.xml"/>
	-->""".format(
		link='',
		startIndex=0,
		itemsPerPage=0,
		startPage=0,
		query=self.query,
		total=len(self.search)
).encode('utf8')
		for s in self.search:
			yield u"""
	<entry xmlns="http://www.w3.org/2005/Atom" xmlns:media="http://search.yahoo.com/mrss/">
		<title>{title}</title>
		<link href="{link}"/>
		<author>
			<name>{author}</name>
		</author>
		<id>{id}</id>
		<updated>2003-12-13T18:30:02Z</updated>
		<content type="text">
		</content>
		<media:content
			url="{link}"
			bitrate="{bitrate}"
		>
			<media:title>{title}</media:title>
			<media:category>{category}</media:category>
		</media:content>
	</entry>
""".format(
			title = s['name'],
			link=s['location'],
			id=s['trackId'],
			author=s['artist'],
			category=s.get('genre', ''),
			bitrate=s.get('bitrate', 0)
			).encode('utf8')
		yield "</feed>"
		

class Opensearchd(object):
	def __init__(self):
		self.index = Index()
	def notFound(self, start_response):
		status = '404 NOT FOUND' # HTTP Status
		headers = [('Content-type', 'text/plain')]
		start_response(status, headers)
		return [' ']
	def search(self, start_response, query):
		search = self.index.query(unicode(query))
		status = '200 OK' # HTTP Status
		headers = [('Content-type', 'text/plain')]#application/atom+xml
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
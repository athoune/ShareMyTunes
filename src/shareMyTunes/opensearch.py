#!/usr/bin/env python

__author__ = "mlecarme"

from bottle import route, request, response

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
		

index = Index()
HOST = 'localhost'
PORT = 8001


@route('/opensearch')
def search():
	query = request.GET.get('q')
	search = index.query(unicode(query))
	response.content_type = 'text/plain'#application/atom+xml
	return OpenSearchWrapper(query, search)

@route('/opensearch-description')
def description():
	response.content_type = 'text/plain'#application/atom+xml
	return """<?xml version="1.0" encoding="UTF-8"?>
	 <OpenSearchDescription xmlns="http://a9.com/-/spec/opensearch/1.1/">
	   <ShortName>Share My Tunes</ShortName>
	   <Description>Sharing your iTunes music</Description>
	   <Tags>iTunes mp3</Tags>
	   <Contact>admin@example.com</Contact>
	   <Url type="application/atom+xml" 
	        template="http://%s:%i/opensearch?q={searchTerms}&amp;pw={startPage?}"/>
	 </OpenSearchDescription>""" % (HOST, PORT)

if __name__ == '__main__':
	from bottle import run
	run(host=HOST, port=PORT)

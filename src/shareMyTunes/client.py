#!/usr/bin/env python

__author__ = "mlecarme"

import sys
here = sys.path[0]
sys.path.remove(here)
from opensearch import Client
sys.path.insert(0, here)

HOST = 'localhost'
PORT = 8001

c = Client('http://%s:%i/opensearch-description' % (HOST, PORT))
resp = c.search(sys.argv[1])
for r in resp:
	print r
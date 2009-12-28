#!/usr/bin/env python

__author__ = "mlecarme"
__version__ = "0.1"

class Filter(object):
	"""
	Object that filter iterable and can be piped
	"""
	def __init__(self):
		self.filters = [self]
	def __call__(self, iter):
		self.iter = iter
		return self
	def filter(self, item):
		return item
	def __iter__(self):
		for a in self.iter:
			for f in self.filters:
				a = f.filter(a)
			yield a
	def __or__(self, other):
		self.filters.append(other)
		return self

class AutoFilter(Filter):
	"""
	Filter built with a function
	"""
	def __init__(self, filter):
		Filter.__init__(self)
		self._filter = filter
	def filter(self, item):
		return self._filter(item)

if __name__ == '__main__':
	def f(str):
		return str.lower()
	class StarFilter(Filter):
		def filter(self, item):
			return "* %s" % item
	class DotFilter(Filter):
		def filter(self, item):
			return "- %s" % item
	test = ["Pim", "Pam", "Poum"]
	a = AutoFilter(f) | StarFilter() | DotFilter()
	for i in a(iter(test)):
		print i
	a = AutoFilter(f) | DotFilter() | StarFilter()
	for i in a(iter(test)):
		print i

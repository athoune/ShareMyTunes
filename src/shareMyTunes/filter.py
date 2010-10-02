#!/usr/bin/env python

__author__ = "mlecarme"

class Filter(object):
	"""
	Object that filter iterable and can be piped
	"""
	def __init__(self):
		self.filters = [self]
	def __call__(self, it):
		self.iter = it
		return self
	def filter(self, item):
		"overide me"
		return item
	def __iter__(self):
		for it in self.iter:
			for filt in self.filters:
				it = filt.filter(it)
			yield it
	def __or__(self, other):
		self.filters.append(other)
		return self

class AutoFilter(Filter):
	"""
	Filter built with a function
	"""
	def __init__(self, filt):
		Filter.__init__(self)
		self._filter = filt
	def filter(self, item):
		return self._filter(item)

if __name__ == '__main__':
	def f(string):
		return string.lower()
	class StarFilter(Filter):
		def filter(self, item):
			return "* %s" % item
	class DotFilter(Filter):
		def filter(self, item):
			return "- %s" % item
	test = ["Pim", "Pam", "Poum"]
	filtr = AutoFilter(f) | StarFilter() | DotFilter()
	for i in filtr(iter(test)):
		print i
	filtr = AutoFilter(f) | DotFilter() | StarFilter()
	for i in filtr(iter(test)):
		print i

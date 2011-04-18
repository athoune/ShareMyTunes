#!/usr/bin/env python
import select

import pybonjour

def register_callback(sdRef, flags, errorCode, name, regtype, domain):
	if errorCode == pybonjour.kDNSServiceErr_NoError:
		print 'Registered service:'
		print '  name    =', name
		print '  regtype =', regtype
		print '  domain  =', domain

def broadcast(name = 'Share my tunes', port = 8000):
	sdRef = pybonjour.DNSServiceRegister(
		name = name,
		regtype = '_http._tcp',
		port = port,
		callBack = register_callback)
	ready = select.select([sdRef], [], [])
	if sdRef in ready[0]:
		pybonjour.DNSServiceProcessResult(sdRef)
	sdRef = pybonjour.DNSServiceRegister(name = name,
		regtype = '_share_my_tunes._tcp',
		port = port,
		callBack = register_callback)
	ready = select.select([sdRef], [], [])
	if sdRef in ready[0]:
		pybonjour.DNSServiceProcessResult(sdRef)

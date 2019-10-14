#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Util
"""

import os
import sys
import time


class Util(object):
	""" Util """

	def __init__(self, config):

		self.__config = config


	def setPriority(self, priority=4):
		""" set priority """

		self.debug('__setPriority: priority=%s', (priority,))

		if not priority:
			return 1

		priority = abs(int(priority))

		# priority
		if priority not in range(1, 5+1):
			priority = 5

		return priority


	# maxlen
	def logMaxLen(self, msg):
		""" max length """

		# maxlen
		msgLen = len(msg)
		if msgLen < self.__config['maxLen']:
			return msg

		msg = msg[:self.__config['maxLen']] + ' ...'
		self.debug('log: msgLen=%s > global maxLen=%s -> because msg short',\
			(msgLen, self.__config['maxLen']))

		return msg


	def debug(self, msg, val=()):
		""" debug mode log """

		if not self.__config['debugMode']:
			return 1

		tf = time.strftime(self.__config['timeFormat'], time.localtime())
		getpid = os.getpid()
		msgVal = msg % val

		if val:
			msgVal = msg % val
			sys.stderr.write('%s [%s] DEBUG: %s\n' % (tf, getpid, msgVal))
			return 0

		sys.stderr.write('%s [%s] DEBUG: %s\n' % (tf, getpid, msg))
		return 0

if __name__ == '__main__':

	MAX_LEN = 10000
	TIME_FORMAT = '%Y/%m/%d %H:%M:%S'

	U = Util({'maxLen':MAX_LEN, 'timeFormat':TIME_FORMAT, 'debugMode':True})

	U.setPriority(0)
	U.setPriority(1)

	U.logMaxLen('message')

	U.debug('ccc\n')

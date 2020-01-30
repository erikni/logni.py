#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Console Stream
"""

import sys


__all__ = ['ConsoleStream']


class ConsoleStream(object):
	""" Console Stream """

	def __init__(self, config):
		""" Init

		@param config
		"""

		self.__config = config


	def console(self, console=False):
		""" Console / stderr

		@param console
		"""

		self.__config['console'] = console


	def log(self, logMessage):
		""" Log to console / stderr

		@param logMessage
		"""

		# stderr / console
		if not self.__config['console']:
			return 0

		sys.stderr.write('%s\n' % logMessage)

		if self.__config['flush']:
			sys.stderr.flush()

		return 0


if __name__ == '__main__':

	C = ConsoleStream({'flush':False, 'console':True})
	C.log('bbb\n')

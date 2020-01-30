#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File Stream
"""

import logni


__all__ = ['FileStream']


class FileStream(object):
	""" file stream """

	def __init__(self, config):
		""" Init

		@param config
		"""

		self.__fd = None
		self.__util = logni.Util(config)
		self.__config = config
		self.file(config.get('logFile'))


	def file(self, logFile):
		""" File

		@param logFile

		@return exitcode
		"""

		if not logFile:
			self.__util.debug('file: logFile not input')
			return 0

		self.__util.debug('file=%s', logFile)

		# err: read file
		try:
			self.__fd = open(logFile, 'a')
		except BaseException as emsg:
			self.__util.debug('file="%s": err="%s"', (logFile, emsg))
			return 1

		return 0


	def log(self, logMessage):
		""" Log to file

		@param logMessage

		@return exitcode
		"""

		# file descriptor
		if not self.__fd:
			return 0

		self.__fd.write('%s\n' % logMessage)

		if self.__config['flush']:
			self.__fd.flush()

		return 0


if __name__ == '__main__':

	TIME_FORMAT = '%Y/%m/%d %H:%M:%S'

	F = FileStream({'logFile': '/tmp/file.log',\
		'flush':True,\
		'debugMode':True,\
		'timeFormat':TIME_FORMAT})
	F.log('aaa')
	F.log('bbb')

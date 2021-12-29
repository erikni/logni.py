#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File Stream
"""

# pylint: disable=cyclic-import
import logni


__all__ = ['FileStream']


class FileStream():
	""" file stream """

	def __init__(self, config):
		""" Init

		@param config
		"""

		self.__fd = None
		self.__util = logni.Util(config)
		self.__config = config
		self.file(config.get('log_file'))


	def file(self, log_file):
		""" File

		@param log_file

		@return exitcode
		"""

		if not log_file:
			self.__util.debug('file: log_file not input')
			return True

		self.__util.debug('file=%s', log_file)

		# err: read file
		try:
			self.__fd = open(log_file, 'a')
		except BaseException as emsg:
			self.__util.debug('file="%s": err="%s"', (log_file, emsg))
			return 1

		return True


	def log(self, log_message):
		""" Log to file

		@param log_message

		@return exitcode
		"""

		# file descriptor
		if not self.__fd:
			return True

		self.__fd.write('%s\n' % log_message)

		if self.__config['flush']:
			self.__fd.flush()

		return True


if __name__ == '__main__':

	TIME_FORMAT = '%Y/%m/%d %H:%M:%S'

	F = FileStream({'log_file': '/tmp/file.log',\
		'flush':True,\
		'debugMode':True,\
		'timeFormat':TIME_FORMAT})
	F.log('aaa')
	F.log('bbb')

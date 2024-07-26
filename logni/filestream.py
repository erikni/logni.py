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


	def file(self, log_file:str) -> bool:
		""" File

		@param log_file

		@return exitcode
		"""
		# pylint: disable=consider-using-with

		if not log_file:
			self.__util.debug('file: log_file not input')
			return True

		self.__util.debug('file=%s', log_file)

		# err: read file
		try:
			self.__fd = open(log_file, 'a', encoding='utf-8')
		except PermissionError as pemsg:
			self.__util.debug('file="%s": err="%s"', (log_file, pemsg))
			return False

		return True


	def log(self, log_message:str) -> bool:
		""" Log to file

		@param log_message

		@return exitcode
		"""

		# file descriptor
		if not self.__fd:
			return True

		self.__fd.write(f'{log_message}\n')

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

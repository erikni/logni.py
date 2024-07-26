#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Util
"""

import os
import sys
import time


__all__ = ['Util']


class Util():
	""" Util """

	def __init__(self, config):
		""" Init

		@param config
		"""

		self.__config = config
		self.__name = config.get('name', '').upper()


	def set_priority(self, priority:int=4) -> int:
		""" Set priority

		@param priority

		@return priority
		"""

		self.debug('__set_priority: priority=%s', (priority,))

		if not priority:
			return 1

		priority = abs(int(priority))

		# priority
		if priority not in range(1, 5+1):
			priority = 5

		return priority


	# maxlen
	def log_max_len(self, msg:str) -> str:
		""" Max length

		@param msg

		@return msg
		"""

		# maxlen
		msg_len = len(msg)
		if msg_len < self.__config['maxLen']:
			return msg

		msg = msg[:self.__config['maxLen']] + ' ...'
		self.debug('log: msg_len=%s > global maxLen=%s -> because msg short',\
			(msg_len, self.__config['maxLen']))

		return msg


	def debug(self, msg:str, params:tuple=()) -> bool:
		""" Debug mode log

		@param msg
		@param params

		@return exitcode
		"""

		if not self.__config['debugMode']:
			return False

		time_format = time.strftime(self.__config['timeFormat'], time.localtime())
		getpid = os.getpid()
		msg_val = msg % params

		if params:
			msg_val = msg % params
			sys.stderr.write(f'{time_format} [{getpid}] {self.__name} D0: {msg_val}\n')
			return True

		sys.stderr.write(f'{time_format} [{getpid}] {self.__name} D0: {msg}\n')
		return True


if __name__ == '__main__':

	MAX_LEN = 10000
	TIME_FORMAT = '%Y/%m/%d %H:%M:%S'

	U = Util({'maxLen':MAX_LEN, 'timeFormat':TIME_FORMAT, 'debugMode':True, 'name':'TEST'})

	U.set_priority(0)
	U.set_priority(1)

	U.log_max_len('message')

	U.debug('ccc\n')

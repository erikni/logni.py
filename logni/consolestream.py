#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Console Stream
"""

import sys
import colorama
import logni


__all__ = ['ConsoleStream']


class ConsoleStream():
	""" Console Stream """

	def __init__(self, config):
		""" Init

		@param config
		"""

		self.__config = config
		self.cfg = logni.Cfgni()


	def console(self, console:bool=False):
		""" Console / stderr

		@param console
		"""

		self.__config['console'] = console


	def log(self, log_message:str, severity:str) -> bool:
		""" Log to console / stderr

		@param log_message
		"""

		# console off
		if not self.__config['console']:
			return False

		# color
		color = colorama.Fore.BLACK + colorama.Back.WHITE
		if severity == self.cfg.SEVERITY_CRITICAL:
			color = colorama.Back.MAGENTA

		elif severity == self.cfg.SEVERITY_ERROR:
			color = colorama.Back.RED

		elif severity == self.cfg.SEVERITY_WARN:
			color = colorama.Back.YELLOW

		elif severity == self.cfg.SEVERITY_INFO:
			color = colorama.Back.GREEN

		# console on
		sys.stderr.write(f'{color}{log_message}\n')
		sys.stderr.write(colorama.Back.RESET)
		sys.stderr.write(colorama.Fore.RESET)

		if self.__config['flush']:
			sys.stderr.flush()

		return True


if __name__ == '__main__':

	C = ConsoleStream({'flush':False, 'console':True})
	C.log('info message\n', 'info')

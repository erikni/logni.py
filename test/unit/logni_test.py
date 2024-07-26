#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Unit test
"""

import unittest
import logni


MAX_LEN = 10000
CHARSET = 'utf8'
TIME_FORMAT = '%Y/%m/%d %H:%M:%S'


class TestStringMethods(unittest.TestCase):
	""" Unit test """

	def __check_config_struct(self, config):
		"""
		Method tests basic structure for config
		"""

		self.assertTrue('debugMode' in config, msg='debugMode must be input')
		self.assertTrue('charset' in config, msg='charset must be input')
		self.assertTrue('color' in config, msg='color must be input')
		self.assertTrue('console' in config, msg='console must be input')
		self.assertTrue('logFile' in config, msg='logFile must be input')
		self.assertTrue('env' in config, msg='env must be input')
		self.assertTrue('flush' in config, msg='flush must be input')
		self.assertTrue('mask' in config, msg='mask must be input')
		self.assertTrue('name' in config, msg='name must be input')
		self.assertTrue('maxLen' in config, msg='maxLen must be input')
		self.assertTrue('strip' in config, msg='strip must be input')
		self.assertTrue('stackOffset' in config, msg='stackOffset must be input')
		self.assertTrue('stackDepth' in config, msg='stackDepth must be input')
		self.assertTrue('timeFormat' in config, msg='timeFormat must be input')

		self.assertTrue(isinstance(config['debugMode'], bool), msg='debugMode must be boolean')
		self.assertTrue(isinstance(config['color'], bool), msg='color must be boolean')
		self.assertTrue(isinstance(config['console'], bool), msg='console must be boolean')
		self.assertTrue(isinstance(config['flush'], bool), msg='flush must be boolean')
		self.assertTrue(isinstance(config['strip'], bool), msg='strip must be boolean')

		self.assertTrue(isinstance(config['maxLen'], int), msg='maxLen must be integer')
		self.assertTrue(isinstance(config['stackOffset'], int), msg='stackOffset must be integer')
		self.assertTrue(isinstance(config['stackDepth'], int), msg='stackDepth must be integer')


	def __check_log_struct(self, ret_log):
		"""
		Method tests basic structure for OK return call
		"""

		self.assertTrue('msg' in ret_log, msg='key msg: must be in ouput structure')
		self.assertTrue('severity' in ret_log, msg='key severity: must be in ouput structure')
		self.assertTrue('priority' in ret_log, msg='key priority: must be in ouput structure')
		self.assertTrue('use' in ret_log, msg='key use: must be in ouput structure')

		self.assertTrue(isinstance(ret_log['priority'], int), msg='key priority: must be integer')
		self.assertTrue(isinstance(ret_log['use'], int), msg='key use: must be integer')


	def __config(self):
		"""
		Config
		"""
		# pylint: disable=no-self-use

		# config
		config = {\
			'debugMode': True,
			'charset': CHARSET,
			'color': True,
			'console': True,
			'logFile': None,
			'env': '',
			'flush': True,
			'mask': 'ALL',
			'name': 'logname',
			'maxLen': MAX_LEN,
			'strip': True,
			'stackOffset': 0,
			'stackDepth': 1,
			'timeFormat': TIME_FORMAT,
			'revision': ''}

		return config


	def test10_ok(self):
		"""
		Test OK
		"""

		config = self.__config()
		self.__check_config_struct(config)

		log = logni.Logni(config)

		return log


	def test11_ok_info(self):
		""" info OK """

		log = self.test10_ok()
		for priority_no in range(1, 4):
			ret = log.info('info message', priority=priority_no)
			self.__check_log_struct(ret)

		return ret

	def test12_ok_warn(self):
		""" warning OK """

		log = self.test10_ok()
		for priority_no in range(1, 4):
			ret = log.warn('warn message', priority=priority_no)
			self.__check_log_struct(ret)

		return ret

	def test12_ok_error(self):
		""" error OK """

		log = self.test10_ok()
		for priority_no in range(1, 4):
			ret = log.error('error message', priority=priority_no)
			self.__check_log_struct(ret)

		return ret

	def test12_ok_critical(self):
		""" critical OK """

		log = self.test10_ok()
		for priority_no in range(1, 4):
			ret = log.critical('critical message', priority=priority_no)
			self.__check_log_struct(ret)

		return ret

	def test12_ok_debug(self):
		""" debug OK """

		log = self.test10_ok()
		for priority_no in range(1, 4):
			ret = log.debug('debug message', priority=priority_no)
			self.__check_log_struct(ret)

		return ret


	def test21_err_mask(self):
		"""
		No used mask
		"""

		# init
		config = self.__config()
		config['mask'] = 'I4'
		log = logni.Logni(config)

		ret_info = log.info('info message', priority=1)

		self.assertTrue('use' in ret_info)
		self.assertFalse(ret_info['use'])


	def test22_err_method(self):
		"""
		Test tests incorrect method call raises Attribute error
		"""
		# pylint: disable=no-member

		# init
		config = self.__config()
		log = logni.Logni(config)

		with self.assertRaises(AttributeError):
			log.non_exist_method()


	def test23_err_param(self):
		"""
		Test tests incorrect method call raises type error - non existent parameter
		"""
		# pylint: disable=unexpected-keyword-arg

		# init
		config = self.__config()
		log = logni.Logni(config)

		with self.assertRaises(TypeError):
			log.info('info message', non_exist_param=2)


if __name__ == '__main__':
	unittest.main()

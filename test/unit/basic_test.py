#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Unit test
"""

import unittest
import sys

sys.path.append('../../src')
sys.path.append('src')

import logni


MAX_LEN = 10000
CHARSET = 'utf8'
TIME_FORMAT = '%Y/%m/%d %H:%M:%S'


class TestStringMethods(unittest.TestCase):
	""" Unit test """

	def __checkConfigStructure(self, config):
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


	def __checkLogStructure(self, retLog):
		"""
		Method tests basic structure for OK return call
		"""

		self.assertTrue('msg' in retLog, msg='key msg: must be in ouput structure')
		self.assertTrue('severity' in retLog, msg='key severity: must be in ouput structure')
		self.assertTrue('priority' in retLog, msg='key priority: must be in ouput structure')
		self.assertTrue('use' in retLog, msg='key use: must be in ouput structure')

		self.assertTrue(isinstance(retLog['priority'], int), msg='key priority: must be integer')
		self.assertTrue(isinstance(retLog['use'], int), msg='key use: must be integer')


	def __config(self):
		""" 
		Config 
		"""

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


	def testOK(self):
		"""
		Test OK
		"""

		config = self.__config()
		self.__checkConfigStructure(config)

		log = logni.Logni(config)

		ret = log.info('info message', priority=1)
		self.__checkLogStructure(ret)

		ret = log.warn('warn message', priority=1)
		self.__checkLogStructure(ret)

		ret = log.error('error message', priority=1)
		self.__checkLogStructure(ret)

		ret = log.critical('critical message', priority=1)
		self.__checkLogStructure(ret)

		ret = log.debug('debug message', priority=1)
		self.__checkLogStructure(ret)


	def testNoUsedMask(self):
		"""
		No used mask 
		"""

		# init
		config = self.__config()
		config['mask'] = 'I4'
		log = logni.Logni(config)

		retInfo = log.info('info message', priority=1)

		self.assertTrue('use' in retInfo)
		self.assertFalse(retInfo['use'])
		

	def testNonExistMethod(self):
		"""
		Test tests incorrect method call raises Attribute error
		"""

		# init
		config = self.__config()
		log = logni.Logni(config)

		with self.assertRaises(AttributeError):
			log.nonExistMethod()


	def testNonExistParameter(self):
		"""
		Test tests incorrect method call raises type error - non existent parameter
		"""

		# init
		config = self.__config()
		log = logni.Logni(config)

		with self.assertRaises(TypeError):
			log.info('info message', nonExistentParameter=2)


if __name__ == '__main__':
	unittest.main()

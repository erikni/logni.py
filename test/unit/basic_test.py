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

		self.assertTrue('debugMode' in config)
		self.assertTrue('charset' in config)
		self.assertTrue('color' in config)
		self.assertTrue('console' in config)
		self.assertTrue('logFile' in config)
		self.assertTrue('env' in config)
		self.assertTrue('flush' in config)
		self.assertTrue('mask' in config)
		self.assertTrue('maxLen' in config)
		self.assertTrue('strip' in config)
		self.assertTrue('stackOffset' in config)
		self.assertTrue('stackDepth' in config)
		self.assertTrue('timeFormat' in config)

		self.assertTrue(isinstance(config['debugMode'], bool))
		self.assertTrue(isinstance(config['color'], bool))
		self.assertTrue(isinstance(config['console'], bool))
		self.assertTrue(isinstance(config['flush'], bool))
		self.assertTrue(isinstance(config['strip'], bool))

		self.assertTrue(isinstance(config['maxLen'], int))
		self.assertTrue(isinstance(config['stackOffset'], int))
		self.assertTrue(isinstance(config['stackDepth'], int))


	def __checkLogStructure(self, retLog):
		"""
		Method tests basic structure for OK return call
		"""

		self.assertTrue('msg' in retLog)
		self.assertTrue('severity' in retLog)
		self.assertTrue('priority' in retLog)
		self.assertTrue('use' in retLog)

		self.assertTrue(isinstance(retLog['priority'], int))
		self.assertTrue(retLog['use'])


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

#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
 GNU General Public License v3.0

 Permissions of this strong copyleft license are conditioned on making
 available complete source code of licensed works and modifications,
 which include larger works using a licensed work, under the same license.
 Copyright and license notices must be preserved. Contributors provide
 an express grant of patent rights.

 see all: https://github.com/erikni/logni.py/blob/master/LICENSE

 ---

 logni is python library for event logging and application states

 Example:

 log = logni.Logni({'debugMode':True, 'mask':'ALL', 'console':True})

 log.info('informational message with priority=4')
 log.info('informational message with priority=3', priority=3)

 log.debug('debug message [ts=%s] with priority=2', time.time(), priority=2)
 log.error('error message with priority=1', priority=1)
 log.warn('warning message with priority=1', priority=1)
"""

import time
import random
import traceback
import os
import os.path
import functools
import utilni
import filestream
import consolestream

MAX_LEN = 10000
CHARSET = 'utf8'
TIME_FORMAT = '%Y/%m/%d %H:%M:%S'

class Logni(object):
	""" logni object """

	def __init__(self, config=None):
		""" Init

		@param config """

		# global
		self.__config = {\
			'debugMode': False,
			'charset': CHARSET,
			'color': False,
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

		if not config:
			config = {}

		for cfgName in config:
			self.__config[cfgName] = config[cfgName]

		self.__util = utilni.Util(self.__config)
		self.__file = filestream.FileStream(self.__config)
		self.__console = consolestream.ConsoleStream(self.__config)

		# severity
		self.__logniMaskSeverity = {}
		self.__logniMaskSeverityFull = ['DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL']

		# severity (sortname)
		self.__logniMaskSeverityShort = []
		for severityName in self.__logniMaskSeverityFull:
			_short = severityName[:1]

			self.__logniMaskSeverityShort.append(_short)
			self.__logniMaskSeverity[_short] = self.__util.setPriority(5)

		# default
		self.mask('ALL')
		self.console(True)

		if config.get('mask'):
			self.mask(config['mask'])


	def file(self, logFile):
		""" File

		@param logFile

		@return exitcode """

		self.__config['logFile'] = logFile
		return self.__file.file(logFile)


	def console(self, console=False):
		""" Console (stderr)

		@param console

		@return exitcode """

		self.__config['console'] = console
		self.__util.debug('console=%s', console)
		return self.__console.console(console)

	stderr = console


	def __setMask(self, mask='ALL'):
		""" Set ALL | OFF mask

		@param mask

		@return exitcode """

		maskPriority = {'ALL': 1, 'OFF': 5}
		priority = maskPriority.get(mask)
		if not priority:
			return 1

		for severityShort in self.__logniMaskSeverityShort:
			self.__logniMaskSeverity[severityShort] = self.__util.setPriority(priority)

		self.__util.debug('__setMask: self.__logniMaskSeverityShort=%s', self.__logniMaskSeverityShort)
		self.__util.debug('__setMask: self.__logniMaskSeverity=%s', self.__logniMaskSeverity)

		return 0


	def mask(self, mask='ALL'):
		""" Set mask

		@param mask

		@return exitcode """

		self.__util.debug('mask=%s', mask)

		# default mask=ALL
		if not mask:
			mask = 'ALL'
			self.__util.debug('mask=ALL')


		# log mask = ALL | OFF
		if self.__setMask(mask) == 0:
			return 0

		# len is wrong
		lenMask = len(mask)
		if lenMask not in (2, 4, 6, 8, 10):
			self.__util.debug('mask=%s: error len=%s', (mask, lenMask))
			return 1

		# set default MASK=0FF
		self.__setMask('OFF')

		# set severity
		for no in range(0, lenMask, 2):

			_len = mask[no]
			_priority = self.__util.setPriority(mask[no+1])

			self.__logniMaskSeverity[_len] = _priority
			self.__util.debug('mask: len=%s, priority=%s', (_len, _priority))

			del _len, _priority

		self.__util.debug('mask: self.__logniMaskSeverity=%s', self.__logniMaskSeverity)
		self.__config['mask'] = mask

		return 0


	# log use?
	def __logUse(self, severity='', priority=1):
		""" Use log?

		@param severity
		@param priority

		@return exitcode """

		self.__util.debug('log.__logUse: severity=%s, priority=%s', (severity, priority))

		priority = self.__util.setPriority(priority)

		# if mask=ALL
		if self.__config['mask'] == 'ALL':
			self.__util.debug('log.__logUse: severity=%s, msg priority=%s ' + \
				'>= mask=ALL -> msg log is VISIBLE',\
				(severity, priority))
			return 0

		if severity[0] not in self.__logniMaskSeverity:
			self.__util.debug('log.__logUse: severity=%s not exist', severity)
			return 1

		# message hidden
		_priority = self.__logniMaskSeverity[severity[0]]
		if priority < _priority:
			self.__util.debug('log.__logUse: severity=%s, msg priority=%s < ' + \
				'mask priority=%s -> msg log is HIDDEN',\
				(severity, priority, _priority))
			return 1

		# message visible
		self.__util.debug('log.__logUse: severity=%s, msg priority=%s >= ' + \
			'mask priority=%s -> msg log is VISIBLE',\
			(severity, priority, _priority))

		return 0


	def __log(self, msg, params=(), severity='DEBUG', priority=1):
		""" Log message

		@param msg
		@param params
		@param severity
		@param priority

		@return struct """

		# priority
		priority = self.__util.setPriority(priority)

		# log use?
		if self.__logUse(severity, priority) == 1:
			return {'msg':msg, 'severity':severity, 'priority':priority, 'use':False}

		try:
			msg = msg % params
		except BaseException as emsg:
			msg = '!! %s %s <%s>' % (msg, params, emsg)

		# todo: unicode test
		# if isinstance(msg, types.UnicodeType):
		# msg = msg.encode(self.__config['charset'], 'ignore')

		# strip message
		if self.__config['strip']:
			msg = msg.replace('\n', ' ').strip()

		# max len
		msg = self.__util.logMaxLen(msg)

		# stack
		stackList = []
		offset = self.__config['stackOffset'] + 1
		limit = self.__config['stackDepth'] + offset
		for tes in traceback.extract_stack(limit=limit)[:-offset]:
			stackList.append('%s:%s():%s' % (tes[0].split('/')[-1], tes[2], tes[1]))

		# log message
		xrand = '%x' % random.SystemRandom().randint(1, 4294967295)
		logMessage = "%s [%s] %s: %s [%s] {%s}" % \
			(time.strftime(self.__config['timeFormat'], time.localtime()),\
			os.getpid(),\
			'%s%s' % (severity[0], priority),\
			msg, xrand,\
			','.join(stackList))

		# log to file / console
		self.__file.log(logMessage)
		self.__console.log(logMessage)

		return {'msg':msg, 'severity':severity, 'priority':priority, 'use':True, 'hash':xrand}


	# ---

	def critical(self, msg, params=(), priority=1):
		""" Critical: critical / fatal message

		@param msg
		@param params
		@param priority

		@return struct """

		return self.__log(msg, params, 'CRITICAL', priority)

	fatal = critical


	def error(self, msg, params=(), priority=1):
		""" Error: error message

		@param msg
		@param params
		@param priority

		@return struct """

		return self.__log(msg, params, 'ERR', priority)

	err = error


	def warn(self, msg, params=(), priority=1):
		""" Warn: warning message

		@param msg
		@param params
		@param priority

		@return struct """

		return self.__log(msg, params, 'WARN', priority)

	warning = warn


	def info(self, msg, params=(), priority=1):
		""" Info: informational messages

		@param msg
		@param params
		@param priority

		@return struct """

		return self.__log(msg, params, 'INFO', priority)

	informational = info


	def debug(self, msg, params=(), priority=1):
		""" Debug: debug-level messages

		Alias: dbg()

		@param msg
		@param params
		@param priority

		@return struct """

		return self.__log(msg, params, 'DEBUG', priority)

	dbg = debug


	def emergency(self, msg, params=()):
		""" Emergency: system is unusable

		Alias: critical(priority=4)

		@param msg
		@param params

		@return struct """
		return self.critical(msg, params, priority=4)


	def alert(self, msg, params=()):
		""" Alert: action must be taken immediately

		Alias: error(priority=3)

		@param msg
		@param params

		@return struct """

		return self.error(msg, params, priority=3)


	def notice(self, msg, params=()):
		""" Notice: normal but significant condition

		Alias: info(priority=1)

		@param msg
		@param params

		@return struct """

		return self.info(msg, params, priority=1)


	def timer(self, func):
		""" Timer: print the runtime of the decorated function """

		@functools.wraps(func)
		def logWrapperTimer(*args, **kwargs):
			""" log wrapper timer """

			startTime = time.time()
			ret = func(*args, **kwargs)
			runTime = time.time() - startTime

			self.info('func %s() in %s secs', (func.__name__, runTime), priority=1)

			return ret

		return logWrapperTimer


# run: python test/example/example.py

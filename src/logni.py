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
"""

import time
import random
import types
import traceback
import os
import os.path
import sys

MAX_LEN = 10000


class Logni(object):
	""" logni object """

	def __init__(self, config=None):
		""" init """

		# global
		self.__config = {\
			'debugMode': False,
			'charset': 'utf8',
			'color': 0,
			'console': 0,
			'env': '',
			'flush': 1,
			'mask': 'ALL',
			'maxLen': MAX_LEN,
			'strip': 0,
			'stackOffset': 0,
			'stackDepth': 1,
			'timeFormat': '%Y/%m/%d %H:%M:%S',
			'revision': ''}

		self.__file = None

		if not config:
			config = {}

		for cfgName in config:
			self.__config[cfgName] = config[cfgName]

		# colors: https://getbootstrap.com/docs/4.1/components/alerts/
		# self.__logniColors = {\
		#	'primary':"#004085", # blue light
		#	'secondary':"#383d41", # seda
		#	'success':"#155724", # green light
		#	'danger':"#721c24", # ping light
		#	'warning':"#856404", # yellow light
		#	'info':"#0c5460", # blue-green light
		#	'light':"#818182", # svetle seda
		#	'dark':"#1b1e21"} # tmave seda

		# severity
		self.__logniMaskSeverity = {}
		self.__logniSeverityColors = { \
			'DEBUG': "light",
			'INFO': "primary",
			'WARN': "warning",
			'ERROR': "danger",
			'CRITICAL': "danger"}

		self.__logniMaskSeverityFull = ["DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"]

		# severity (sortname)
		self.__logniMaskSeverityShort = []
		for severityName in self.__logniMaskSeverityFull:
			_short = severityName[:1]

			self.__logniMaskSeverityShort.append(_short)
			self.__logniMaskSeverity[_short] = self.__setPriority(5)

		# default
		self.mask('ALL')
		self.console(True)

		if config.get('mask'):
			self.mask(config['mask'])


	def file(self, logFile):
		""" file """

		self.__debug('file=%s', logFile)

		# err: file not found
		if not os.path.isfile(logFile):
			self.__debug('file="%s": not found"', logFile)
			return 1

		# err: read file
		try:
			self.__file = open(logFile, 'ab')
		except BaseException, emsg:
			self.__debug('file="%s": err="%s"', (logFile, emsg))
			return 1

		return 0


	def mask(self, mask='ALL'):
		""" mask """

		self.__debug('mask=%s', mask)

		# default mask=ALL
		if not mask:
			mask = 'ALL'
			self.__debug('mask=ALL')

		# log mask = ALL | OFF
		if self.__setMask(mask) == 0:
			return 0

		# len is wrong
		lenMask = len(mask)
		if lenMask not in (2, 4, 6, 8, 10):
			self.__debug('mask=%s: error len=%s', (mask, lenMask))
			return 1

		# set default MASK=0FF
		self.__setMask('OFF')

		# set severity
		for no in range(0, lenMask, 2):

			_len = mask[no]
			_priority = self.__setPriority(mask[no+1])

			self.__logniMaskSeverity[_len] = _priority
			self.__debug('mask: len=%s, priority=%s', (_len, _priority))

			del _len, _priority

		self.__debug('mask: self.__logniMaskSeverity=%s', self.__logniMaskSeverity)
		self.__config['mask'] = mask

		return 0


	def __setMask(self, mask='ALL'):
		""" set mask """

		if not mask:
			mask = 'ALL'

		maskPriority = {'ALL': 1, 'OFF': 5}
		priority = maskPriority.get(mask)
		if not priority:
			return 1

		for severityShort in self.__logniMaskSeverityShort:
			self.__logniMaskSeverity[severityShort] = self.__setPriority(priority)

		self.__debug('__setMask: self.__logniMaskSeverityShort=%s', self.__logniMaskSeverityShort)
		self.__debug('__setMask: self.__logniMaskSeverity=%s', self.__logniMaskSeverity)

		return 0



	def console(self, console=0):
		""" stderr / console """

		self.__config['console'] = console
		self.__debug('console=%s', console)

	stderr = console


	def maxLen(self, maxLen=MAX_LEN):
		""" stderr / console """

		self.__config['maxLen'] = maxLen
		self.__debug('maxLen=%s', maxLen)


	def __setPriority(self, priority=4):
		""" set priority """

		self.__debug('__setPriority: priority=%s', priority)

		if not priority:
			return 1

		priority = abs(int(priority))

		# priority
		if priority not in range(1, 5+1):
			priority = 5

		return priority


	def __logUse(self, severity='', priority=1):
		""" use log ? """

		self.__debug('__logUse: severity=%s, priority=%s', (severity, priority))

		priority = self.__setPriority(priority)

		# if mask=ALL
		if self.__config['mask'] == 'ALL':
			self.__debug('__logUse: severity=%s, msg priority=%s >= mask=ALL -> msg log is VISIBLE',\
				(severity, priority))
			return 0

		if severity[0] not in self.__logniMaskSeverity:
			self.__debug('__logUse: severity=%s not exist', severity)
			return 1

		# message hidden
		_priority = self.__logniMaskSeverity[severity[0]]
		if priority < _priority:
			self.__debug('__logUse: severity=%s, msg priority=%s < mask priority=%s -> msg log is HIDDEN',\
				(severity, priority, _priority))
			return 1

		# message visible
		self.__debug('__logUse: severity=%s, msg priority=%s >= mask priority=%s -> msg log is VISIBLE',\
			(severity, priority, _priority))

		return 0


	def __logMaxLen(self, msg):
		""" max length """

		# maxlen
		msgLen = len(msg)
		if msgLen < self.__config['maxLen']:
			return msg

		msg = msg[:self.__config['maxLen']] + ' ...'
		self.__debug('log: msgLen=%s > global maxLen=%s -> because msg short',\
			(msgLen, self.__config['maxLen']))

		return msg


	def log(self, msg, params=(), **kw):
		""" log message """

		severity, priority = kw.iteritems().next()
		self.__debug('log: severity=%s, priority=%s', (severity, priority))

		# priority
		priority = self.__setPriority(priority)

		# log use?
		if self.__logUse(severity, priority) == 1:
			return {'msg':msg, 'severity':severity, 'priority':priority, 'use':0}

		try:
			msg = msg % params
		except BaseException, emsg:
			msg = '!! %s %s <%s>' % (msg, params, emsg)

		# unicode test
		if isinstance(msg, types.UnicodeType):
			msg = msg.encode(self.__config['charset'], 'ignore')

		# strip text
		if self.__config['strip']:
			msg = msg.replace('\n', ' ').strip()

		# maxlen
		msg = self.__logMaxLen(msg)

		# stack
		stackList = []
		offset = self.__config['stackOffset'] + 1
		limit = self.__config['stackDepth'] + offset
		for tes in traceback.extract_stack(limit=limit)[:-offset]:
			stackList.append('%s:%s():%s' % (tes[0].split('/')[-1], tes[2], tes[1]))

		# log message
		xrand = '%x' % random.randint(1, 4294967295)
		logMessage = "%s [%s] %s: %s [%s] {%s}\n" % \
			(time.strftime(self.__config['timeFormat'], time.localtime()),\
			os.getpid(),\
			'%s%s' % (severity[0], priority),\
			msg, xrand,\
			','.join(stackList))

		# log to file / console
		self.__log2File(logMessage)
		self.__log2Console(logMessage)

		return {'msg':msg, 'severity':severity, 'priority':priority, 'use':1}


	def __log2File(self, logMessage):
		""" log to file """

		# file descriptor
		if not self.__file:
			return 0

		self.__file.write(logMessage)

		if self.__config['flush']:
			self.__file.flush()

		return 0


	def __log2Console(self, logMessage):
		""" log to console """

		# stderr / console
		if not self.__config['console']:
			return 0

		sys.stderr.write(logMessage)

		if self.__config['flush']:
			sys.stderr.flush()

		return 0

	# ---

	def critical(self, msg, params=(), priority=4):
		""" critical / fatal message """

		return self.log(msg=msg, params=params, CRITICAL=priority)

	fatal = critical


	def error(self, msg, params=(), priority=4):
		""" err / error message """

		return self.log(msg=msg, params=params, ERR=priority)

	err = error


	def warn(self, msg, params=(), priority=4):
		""" warn / warning message """

		return self.log(msg=msg, params=params, WARN=priority)

	warning = warn


	def info(self, msg, params=(), priority=4):
		""" info / informational message """

		return self.log(msg=msg, params=params, INFO=priority)

	informational = info


	def debug(self, msg, params=(), priority=4):
		""" dbg / debug message """

		return self.log(msg=msg, params=params, DEBUG=priority)

	dbg = debug


	def __debug(self, msg, val=()):
		""" debug mode log """

		if not self.__config['debugMode']:
			return 1

		tf = time.strftime(self.__config['timeFormat'], time.localtime())
		getpid = os.getpid()

		if val:
			print '%s [%s] DEBUG:' % (tf, getpid), msg % val
			return 0

		print '%s [%s] DEBUG: %s' % (tf, getpid, msg)
		return 0


# run: python test/example/example.py

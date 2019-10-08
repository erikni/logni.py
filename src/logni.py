#!usr/bin/python
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
import sys
#import logging


class Logni(object):
	""" logni object """

	def __init__(self):
		""" init """

		self.debugMode = 0

		self.__mask = 'ALL'
		self.__stderr = 0
		self.__flush = 1
		self.__maxLen = 1000
		self.__strip = 0
		self.__stackOffset = 0
		self.__stackDepth = 1
		self.__timeFormat = '%Y/%m/%d %H:%M:%S'

		self.__fd = None
		self.__charset = 'utf8'

		self.__env = ''
		self.__revision = ''

		#self.__logEntries = 0
		#self.__logRollbar = 0
		#self.__rollbar = None
		#self.__loge = None

		# colors: https://getbootstrap.com/docs/4.1/components/alerts/
		self.__logniColors = {\
			'primary':"#004085", # blue light
			'secondary':"#383d41", # seda
			'success':"#155724", # green light
			'danger':"#721c24", # ping light
			'warning':"#856404", # yellow light
			'info':"#0c5460", # blue-green light
			'light':"#818182", # svetle seda
			'dark':"#1b1e21"} # tmave seda

		# severity
		self.__logniMaskSeverity = {}
		self.__logniSeverityColors = { \
			'DEBUG':"light",
			'INFO':"primary",
			'WARN':"warning",
			'ERROR':"danger",
			'CRITICAL':"danger"}

		self.__logniMaskSeverityFull = ["DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"]

		# severity (sortname)
		self.__logniMaskSeverityShort = []
		for severityName in self.__logniMaskSeverityFull:
			_short = severityName[:1]

			self.__logniMaskSeverityShort.append(_short)
			self.__logniMaskSeverity[_short] = self.__setPriority(5)

			del _short

		# default
		self.mask('ALL')
		self.stderr(True)
		self.color(True)


	# def logentries(self, apiKey):
	#	""" logentries """
	#
	#	if not apiKey:
	#		self.ni('logentries: apikey must be input', ERR=4)
	#		return 1
	#
	#	# logentries
	#	try:
	#		from logentries import LogentriesHandler
	#	except BaseException, emsg:
	#		self.ni('logentries import error="%s"', emsg, ERR=4)
	#		return 1
	#
	#	self.__loge = logging.getLogger('logentries')
	#	self.__loge.setLevel(logging.INFO)
	#	# Note if you have set up the logentries handler in Django, the following line is not necessary
	#	self.__loge.addHandler(LogentriesHandler(apiKey))
	#
	#	self.__logEntries = 1
	#
	#	return 0


	# def rollbar(self, apiKey):
	#	""" rollbar """
	#
	#	if not apiKey:
	#		self.ni('rollbar: apikey must be input', ERR=4)
	#		return 1
	#
	#	try:
	#		import rollbar
	#	except BaseException, emsg:
	#		self.ni('rollbar import error="%s"', emsg, ERR=4)
	#		return 1
	#
	#	self.__rollbar = rollbar.init(apiKey, self.__env)
	#
	#	self.__logRollbar = 1
	#
	#	return 0


	def color(self, color=True):
		""" color """

		# todo: code
		self.__debug('color=%s', color)


	def environment(self, env=''):
		""" environment """

		self.__env = env
		self.__debug('environment=%s', env)

	env = environment


	def revision(self, revision=''):
		""" revision """

		self.__revision = revision
		self.__debug('revision=%s', revision)


	def file(self, logFile):
		""" file """

		# err: read file
		try:
			self.__fd = open(logFile, 'ab')
		except BaseException, emsg:
			self.__debug('file="%s", err="%s"', (logFile, emsg))
			return 1

		self.__debug('file=%s', logFile)

		return 0


	def mask(self, mask='ALL'):
		""" mask """

		self.__debug('mask=%s', mask)

		if not mask:
			self.__debug('mask=ALL')
			mask = 'ALL'

		# log mask = ALL | OFF
		retMask = self.__setMask(mask)
		if retMask == 0:
			return 0

		# len is wrong
		lenMask = len(mask)
		if lenMask < 2 or lenMask > 10:
			self.__debug('mask=%s: error len=%s', (mask, lenMask))
			return 1

		# err: incorrect mask
		if lenMask % 2 != 0:
			raise ValueError('logni: incorrect mask="%s"' % (mask,))

		# set default LEVEL=0
		self.__setMask('OFF')

		# set severity
		for no in range(0, lenMask, 2):

			_len = mask[no]
			_priority = self.__setPriority(mask[no+1])

			self.__logniMaskSeverity[_len] = _priority
			self.__debug('mask: len=%s, priority=%s', (_len, _priority))

			del _len, _priority

		self.__debug('mask: self.__logniMaskSeverity=%s', self.__logniMaskSeverity)
		self.__mask = mask

		return 0


	def __setMask(self, mask='ALL'):
		""" set mask """

		if not mask:
			mask = 'ALL'

		if mask == 'ALL':
			priority = 1
		elif mask == 'OFF':
			priority = 5
		else:
			return 1

		for severityShort in self.__logniMaskSeverityShort:
			self.__logniMaskSeverity[severityShort] = self.__setPriority(priority)

		self.__debug('__setMask: self.__logniMaskSeverityShort=%s', self.__logniMaskSeverityShort)
		self.__debug('__setMask: self.__logniMaskSeverity=%s', self.__logniMaskSeverity)

		return 0



	def stderr(self, stderr=0):
		""" stderr """

		self.__stderr = stderr
		self.__debug('stderr=%s', stderr)

	console = stderr


	def flush(self, flush=0):
		""" flush """

		self.__flush = flush
		self.__debug('flush=%s', flush)


	def strip(self, strip=0):
		""" strip """

		self.__strip = strip
		self.__debug('strip=%s', strip)


	def maxLen(self, maxLen=0):
		""" maxLen """

		self.__maxLen = maxLen
		self.__debug('maxLen=%s', maxLen)


	# def __le(self, msg, mask):
	#	""" logentries """
	#
	#	if mask == 'INFO':
	#		return self.__loge.info(msg)
	#
	#	elif mask == 'WARN':
	#		return self.__loge.warning(msg)
	#
	#	elif mask in ('ERR', 'ERROR'):
	#		return self.__loge.error(msg)
	#
	#	elif mask in ('CRITICAL', 'FATAL'):
	#		return self.__loge.critical(msg)
	#
	#	elif mask in ('DEBUG', 'DBG'):
	#		return self.__loge.debug(msg)


	def __logUse(self, severity='', priority=1):
		""" use log ? """

		priority = self.__setPriority(priority)

		# mask=ALL
		if self.__mask == 'ALL':
			self.__debug('uselog: severity=%s, msg priority=%s >= mask=ALL -> msg log is VISIBLE',\
				(severity, priority))

			return 0

		if severity[0] not in self.__logniMaskSeverity:
			self.__debug('uselog: severity=%s not exist', severity)
			return 1

		# message hidden
		_priority = self.__logniMaskSeverity[severity[0]]
		if priority < _priority:
			self.__debug('uselog: severity=%s, msg priority=%s < mask priority=%s -> msg log is HIDDEN',\
				(severity, priority, _priority))
			return 1

		# message visible
		self.__debug('uselog: severity=%s, msg priority=%s >= mask priority=%s -> msg log is VISIBLE',\
			(severity, priority, _priority))

		return 0


	def __setPriority(self, priority=4):
		""" set priority """

		if not priority:
			priority = 1

		priority = int(priority)

		# priority
		if priority < 1:
			priority = 1
		elif priority > 5:
			priority = 5

		return priority


	def log(self, msg, params=(), config=None, **kw):
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
			#color = 'red'
			msg = '!! %s %s <%s>' % (msg, params, emsg)

		# unicode test
		if isinstance(msg, types.UnicodeType):
			msg = msg.encode(self.__charset, 'ignore')

		# strip text
		if self.__strip:
			msg = msg.replace('\n', ' ').strip()

		# config
		if not config:
			config = {'maxLen':0, 'depth':0, 'offset':0}

		maxLen = config.get('maxLen', 0)
		offset = config.get('offset', 0)

		# maxlen
		msgLen = len(msg)
		if self.__maxLen > 0 and msgLen > self.__maxLen:
			msg = msg[:self.__maxLen] + ' ...'
			self.__debug('ni: msgLen=%s > global maxLen=%s -> because msg short', (msgLen, self.__maxLen))

		if maxLen > 0 and msgLen > maxLen:
			msg = msg[:maxLen] + ' ...'
			self.__debug('ni: msgLen=%s > local maxLen=%s -> because msg short', (msgLen, maxLen))

		# color
		# todo ...

		# stack
		stackList = []
		offset = (offset or self.__stackOffset or 0) + 1
		limit = (config.get('depth', 0) or self.__stackDepth) + offset
		for tes in traceback.extract_stack(limit=limit)[:-offset]:
			stackList.append('%s:%s():%s' % (tes[0].split('/')[-1], tes[2], tes[1]))
		# del stackList

		# log message
		logMessage = "%s [%s] %s: %s [%s] {%s}\n" % \
			(time.strftime(self.__timeFormat, time.localtime()),\
			os.getpid(),\
			'%s%s' % (severity[0], priority),\
			msg,\
			'%x' % random.randint(1, 4294967295),\
			','.join(stackList))

		# file descriptor
		if self.__fd:
			self.__fd.write(logMessage)
			if self.__flush:
				self.__fd.flush()

		# stderr
		if self.__stderr:
			sys.stderr.write(logMessage)
			if self.__flush:
				sys.stderr.flush()

		# logentries
		# if self.__logEntries:
		#	retLE = self.__le(msg=msg, mask=severity)
		#	if retLE:
		#		ret['logentries'] = retLE
		#	del retLE

		# rollbar
		# if self.__logRollbar:
		#	self.__rollbar.report_message(message=logMessage, level=severity.lower(), request=None,\
		#		extra_data=None, payload_data=None)

		return {'msg':msg, 'severity':severity, 'priority':priority, 'use':1}

	# ---

	def fatal(self, msg, params=(), priority=4):
		""" fatal """

		return self.log(msg=msg, params=params, CRITICAL=priority)

	critical = fatal


	def error(self, msg, params=(), priority=4):
		""" error """

		return self.log(msg=msg, params=params, ERR=priority)

	err = error


	def warn(self, msg, params=(), priority=4):
		""" warn """

		return self.log(msg=msg, params=params, WARN=priority)

	warning = warn


	def info(self, msg, params=(), priority=4):
		""" info """

		return self.log(msg=msg, params=params, INFO=priority)

	informational = info


	def debug(self, msg, params=(), priority=4):
		""" debug """

		return self.log(msg=msg, params=params, DEBUG=priority)

	dbg = debug


	def __debug(self, msg, val=()):
		""" debugmode log """

		if self.debugMode:
			if val:
				print 'DEBUG:', msg % val
			else:
				print 'DEBUG:', msg

		return



if __name__ == '__main__':

	LOG = Logni()

	print

	print "set debug mode"
	LOG.debugMode = 1
	print


	# init
	LOG.mask('I3E1C1W2')
	LOG.stderr(1)
	print


	# https://logentries.com
	# print "logni.logentries( '<YOUR_API_KEY>')"
	# LOG.logentries('<YOUR_LOGENTRIES_KEY>')
	# print


	# logging
	print "# logni.log('tests %s %s', (11, 22), INFO=3)"
	LOG.log('tests %s %s', (11, 22), INFO=3)
	print


	# alias method for log.ni()
	print "# logni.critical('critical message')"
	LOG.critical('critical message', ())
	print


	print "# logni.error('error message #%s', time.time(), priority=4)"
	LOG.error('error message #%s', time.time(), priority=4)
	print


	print "# logni.warning('warning message #%s', time.time(), priority=3)"
	LOG.warning('warning message #%s', time.time(), priority=3)
	print


	print "# logni.info('info message #%s', time.time(), priority=2)"
	LOG.info('info message #%s', time.time(), priority=2)
	print


	print "# logni.debug('debug message #%s', time.time(), priority=1)"
	LOG.debug('debug message #%s', time.time(), priority=1)
	print

	print "# logni.maxLen(5) "
	LOG.maxLen(5)

	print "# logni.info('very loooong meeeesage', time.time(), priority=4)"
	print LOG.info('very loooong meeeesage #%s', time.time(), priority=4)
	print
	print LOG.info('info message without params', priority=4)
	print

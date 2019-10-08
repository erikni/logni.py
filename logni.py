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


class LogNI(object):
	""" logni is python library for event logging and application states """

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

		self.__filed = None
		self.__charset = 'utf8'

		self.__env = ''
		self.__revision = ''

		#self.__logEntries = 0
		#self.__logRollbar = 0
		#self.__rollbar = None
		#self.__loge = None

		# colors: https://getbootstrap.com/docs/4.1/components/alerts/
		self.__logniColors = {\
			'primary' : "#004085", # blue light
			'secondary' : "#383d41", # seda
			'success' : "#155724", # green light
			'danger' : "#721c24", # ping light
			'warning' : "#856404", # yellow light
			'info' : "#0c5460", # blue-green light
			'light' : "#818182", # svetle seda
			'dark' : "#1b1e21"} # tmave seda

		# severity
		self.__logniMaskSeverity = {}
		self.__logniSeverityColors = { \
			'DEBUG' : "light",
			'INFO' : "primary",
			'WARN' : "warning",
			'ERROR' : "danger",
			'CRITICAL' : "danger"}

		self.__logniMaskSeverityFull = ["DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"]

		# severity (sortname)
		self.__logniMaskSeverityShort = []
		for severityName in self.__logniMaskSeverityFull:
			_short = severityName[:1]

			self.__logniMaskSeverityShort.append(_short)
			self.__logniMaskSeverity[_short] = 5

			del _short

		# default
		self.mask('ALL')
		self.stderr(True)
		self.color(True)


	#def logentries(self, apiKey):
	#	""" logentries """
	#
	#	if not apiKey:
	#		self.ni('logentries: apikey must be input', ERR=4)
	#		return 1
	#
	#	# logentries
	#	try:
	#		from logentries import LogentriesHandler
	#	except Exception, emsg:
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


	#def rollbar(self, apiKey):
	#	""" rollbar """
	#
	#	if not apiKey:
	#		self.ni('rollbar: apikey must be input', ERR=4)
	#		return 1
	#
	#	try:
	#		import rollbar
	#	except Exception, emsg:
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

		pass


	def environment(self, env=''):
		""" environment """

		self.__env = env

	env = environment


	def revision(self, revision=''):
		""" revision """

		self.__revision = revision


	def file(self, logFile):
		""" file """

		# err: read file
		try:
			self.__filed = open(logFile, 'ab')
		except Exception, emsg:
			sys.stderr.write('logni: file="%s", open err="%s"', (logFile, emsg))
			return 1

		return 0


	def mask(self, mask='ALL'):
		""" mask """

		if not mask:
			mask = 'ALL'

		# log mask = ALL | OFF
		retMask = self.__setMask(mask)
		if retMask == 0:
			return 0

		# len is wrong
		lenMask = len(mask)
		if lenMask < 2 or lenMask > 10:
			return 1

		# err: incorrect mask
		if lenMask % 2 != 0:
			raise ValueError('logni: incorrect mask="%s"' % (mask,))

		# set default LEVEL=0
		self.__setMask('OFF')

		# set severity
		for no in range(0, lenMask, 2):

			_len = mask[no]
			_no = mask[no+1]

			if not _no.isdigit():
				raise ValueError('logni: logLevel="%s" must be integer' % (_no,))

			self.__logniMaskSeverity[_len] = int(_no)
			self.__debug('mask: len=%s, no=%s', (_len, _no))

			del _len, _no

		self.__debug('mask: self.__logniMaskSeverity=%s', self.__logniMaskSeverity)
		self.__mask = mask

		return 0


	def __setMask(self, mask='ALL'):

		if not mask:
			mask = 'ALL'

		if mask == 'ALL':
			priority = 1
		elif mask == 'OFF':
			priority = 5
		else:
			return 1

		for severityShort in self.__logniMaskSeverityShort:
			self.__logniMaskSeverity[severityShort] = priority

		self.__debug('__setMask: self.__logniMaskSeverityShort=%s', self.__logniMaskSeverityShort)
		self.__debug('__setMask: self.__logniMaskSeverity=%s', self.__logniMaskSeverity)

		return 0



	def stderr(self, stderr=0):
		""" stderr """

		self.__stderr = stderr

	console = stderr


	def flush(self, flush=0):
		""" flush """
		self.__flush = flush

	def strip(self, strip=0):
		""" strip """
		self.__strip = strip

	def maxLen(self, maxLen=0):
		""" maxLen """
		self.__maxLen = maxLen


	#def __le(self, msg, mask):
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

		if not priority:
			priority = 1

		# mask=ALL
		if self.__mask == 'ALL':
			self.__debug('uselog: severity=%s, msg priority=%s >= mask=ALL -> msg log is VISIBLE',\
				(severity, priority))

			return 0

		if severity[0] not in self.__logniMaskSeverity:
			self.__debug('uselog: severity=%s not exist', severity)
			return 1

		# message hidden
		_no = self.__logniMaskSeverity[severity[0]]
		if priority < _no:
			self.__debug('uselog: severity=%s, msg priority=%s < mask priority=%s -> msg log is HIDDEN',\
				(severity, priority, _no))
			return 1


		# message visible
		self.__debug('uselog: severity=%s, msg priority=%s >= mask priority=%s -> msg log is VISIBLE',\
			(severity, priority, _no))

		return 0


	def ni(self, msg, params={}, offset=0, depth=0, maxLen=0, **kw):
		""" message """

		severity, priority = kw.iteritems().next()
		logInfo = '%s%s' % (severity[0], priority)
		self.__debug('ni: severity=%s, priority=%s', (severity, priority))

		# priority
		if priority < 1:
			priority = 1
		elif priority > 4:
			priority = 4

		# log use?
		retUse = self.__logUse(severity, priority)
		if retUse == 1:
			return 1

		try:
			msg = msg % params
		except Exception, emsg:
			logInfo	= '!!'
			#color = 'red'
			msg = '%s %s <%s>' % (msg, params, emsg)

		# unicode test
		#if type(msg) == types.UnicodeType:
		if isinstance(msg, types.UnicodeType):
			msg = msg.encode(self.__charset, 'ignore')

		# strip text
		if self.__strip:
			msg = msg.replace('\n', ' ').strip()

		# maxlen
		msgLen = len(msg)
		if self.__maxLen > 0:
			if msgLen > self.__maxLen:
				msg = msg[:self.__maxLen] + ' ...'
				self.__debug('ni: msgLen=%s > global maxLen=%s -> because msg short', (msgLen, self.__maxLen))

		if maxLen > 0:
			if msgLen > maxLen:
				msg = msg[:maxLen] + ' ...'
				self.__debug('ni: msgLen=%s > local maxLen=%s -> because msg short', (msgLen, maxLen))

		# color
		# todo ...

		# stack
		stackList = []
		offset = (offset or self.__stackOffset or 0) + 1
		limit = (depth or self.__stackDepth) + offset
		lineNo = 0
		filename = 'unknown'
		for (filename, lineNo, func, text) in traceback.extract_stack(limit=limit)[:-offset]:
			filename = filename.split('/')[-1]
			lineInfo = "%s:%s():%s" % (filename, func, lineNo)
			stackList.append(lineInfo)
			text = None
		stackInfo = ",".join(stackList)

		# message format
		timeString = time.strftime(self.__timeFormat, time.localtime())
		hashStr = '%x' % random.randint(1, 4294967295)

		logMessage = "%s [%s] %s: %s [%s] {%s}\n" % \
			(timeString, os.getpid(), logInfo, msg, hashStr, stackInfo)

		# file descriptor
		if self.__filed:
			self.__filed.write(logMessage)
			if self.__flush:
				self.__filed.flush()

		# stderr
		if self.__stderr:
			sys.stderr.write(logMessage)
			if self.__flush:
				sys.stderr.flush()


		ret = {'hash':hashStr}

		# logentries
		#if self.__logEntries:
		#	retLE = self.__le(msg=msg, mask=severity)
		#	if retLE:
		#		ret['logentries'] = retLE
		#	del retLE

		# rollbar
		#if self.__logRollbar:
		#	self.__rollbar.report_message(message=logMessage, level=severity.lower(), request=None,\
		#		extra_data=None, payload_data=None)

		return ret

	# ---

	def fatal(self, msg, params, priority=4):
		""" fatal """

		return self.ni(msg=msg, params=params, CRITICAL=priority)

	critical = fatal


	def error(self, msg, params, priority=4):
		""" error """

		return self.ni(msg=msg, params=params, ERR=priority)

	err = error


	def warn(self, msg, params, priority=4):
		""" warn """
		return self.ni(msg=msg, params=params, WARN=priority)

	warning = warn


	def info(self, msg, params, priority=4):
		""" info """

		return self.ni(msg=msg, params=params, INFO=priority)

	informational = info


	def debug(self, msg, params, priority=4):
		""" debug """

		return self.ni(msg=msg, params=params, DEBUG=priority)

	dbg = debug


	def __debug(self, msg, val):

		if self.debugMode:
			if val:
				print 'DEBUG:', msg % val
			else:
				print 'DEBUG:', msg

		return



if __name__ == '__main__':

	logni = LogNI()

	print

	print "set debug mode"
	logni.debugMode = 1
	print


	# init
	logni.mask('I3E1C1W2')
	logni.stderr(1)
	print


	# https://logentries.com
	#print "logni.logentries( '<YOUR_API_KEY>')"
	#logni.logentries('<YOUR_LOGENTRIES_KEY>')
	#print


	# logging
	print "# log.ni('tests %s %s', (11, 22), INFO=3)"
	logni.ni('tests %s %s', (11, 22), INFO=3)
	print


	# alias method for log.ni()
	print "# log.critical('critical message')"
	logni.critical('critical message', ())
	print


	print "# log.error('error message #%s', time.time(), priority=4)"
	logni.error('error message #%s', time.time(), priority=4)
	print


	print "# log.warning('warning message #%s', time.time(), priority=3)"
	logni.warning('warning message #%s', time.time(), priority=3)
	print


	print "# log.info('info message #%s', time.time(), priority=2)"
	logni.info('info message #%s', time.time(), priority=2)
	print


	print "# log.debug('debug message #%s', time.time(), priority=1)"
	logni.debug('debug message #%s', time.time(), priority=1)
	print

	print "# log.maxLen(5) "
	logni.maxLen(5)

	print "# log.info('very loooong meeeesage', time.time(), priority=4)"
	print logni.info('very loooong meeeesage #%s', time.time(), priority=4)
	print

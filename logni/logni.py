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

# pylint: disable=cyclic-import
import sys
import time
import random
import traceback
import os
import os.path
import functools
import logni

MAX_LEN = 10000
CHARSET = 'utf-8'
TIME_FORMAT = '%Y/%m/%d %H:%M:%S'

class Logni():
	""" Logni object """

	# global
	__config = {\
		'debugMode': False,
		'charset': CHARSET,
		'color': False,
		'console': True,
		'log_file': None,
		'env': '',
		'flush': True,
		'name': 'LOG',
		'mask': 'ALL',
		'maxLen': MAX_LEN,
		'strip': True,
		'stackOffset': 1,
		'stackDepth': 2,
		'timeFormat': TIME_FORMAT,
		'revision': ''}


	def __init__(self, config=None):
		""" Init

		@param config """

		self.cfg = logni.Cfgni()
		if not config:
			config = {}

		# environment variable values
		for env_name in ('mask', 'console', 'name', 'file'):
			if os.environ.get(f'LOGNI_{env_name.upper()}'):
				config[env_name] = os.environ[f'LOGNI_{env_name.upper()}']

		# config
		for cfg_name in config:
			self.__config[cfg_name] = config[cfg_name]

		# init
		self.__name = self.__config.get('name', 'LOG').upper()
		self.__util = logni.Util(self.__config)
		self.__file = logni.FileStream(self.__config)
		self.__console = logni.ConsoleStream(self.__config)

		# severity
		self.__logni_mask_severity = {}
		self.__logni_mask_severity_full = [\
			self.cfg.SEVERITY_DEBUG,\
			self.cfg.SEVERITY_INFO,\
			self.cfg.SEVERITY_WARN,\
			self.cfg.SEVERITY_ERROR,\
			self.cfg.SEVERITY_CRITICAL]

		# severity (shortname)
		self.__logni_mask_severity_short = []
		for severity_name in self.__logni_mask_severity_full:
			_short = severity_name[:1]

			self.__logni_mask_severity_short.append(_short)
			self.__logni_mask_severity[_short] = self.__util.set_priority(5)

		# default
		self.mask(self.__config.get('mask', 'ALL'))
		self.console(self.__config.get('console', True))


	def file(self, log_file:str):
		""" File output

		@param log_file

		@return exitcode """

		self.__config['log_file'] = log_file

		return self.__file.file(log_file)


	def console(self, console:bool=False):
		""" Console (stderr) output

		@param console

		@return exitcode """

		self.__config['console'] = console
		self.__util.debug('console=%s', console)

		return self.__console.console(console)

	stderr = console


	def name(self, name:str):
		""" Set name """

		if not name:
			return False

		self.__config['name'] = name
		self.__util.debug('name=%s', name)
		self.__name = name.upper()

		return True


	def __set_mask(self, mask='ALL'):
		""" Set ALL | OFF / NOTSET mask

		@param mask

		@return exitcode """

		mask_priority = {'ALL': 1, 'OFF': 5, 'NOTSET': 5}
		priority = mask_priority.get(mask)
		if not priority:
			return False

		for severity_short in self.__logni_mask_severity_short:
			self.__logni_mask_severity[severity_short] = self.__util.set_priority(priority)

		self.__util.debug('__set_mask: self.__logni_mask_severity_short=%s',\
			self.__logni_mask_severity_short)
		self.__util.debug('__set_mask: self.__logni_mask_severity=%s',\
			self.__logni_mask_severity)

		return True


	def mask(self, mask:str='ALL'):
		""" Set mask

		@param mask

		@return exitcode """

		self.__util.debug('mask=%s', mask)

		# default mask=ALL
		if not mask:
			mask = 'ALL'
			self.__util.debug('mask=ALL')


		# log mask = ALL | OFF
		if self.__set_mask(mask):
			return True

		# len is wrong
		len_mask = len(mask)
		if len_mask not in (2, 4, 6, 8, 10):
			self.__util.debug('mask=%s: error len=%s', (mask, len_mask))
			return False

		# set default MASK=0FF
		self.__set_mask('OFF')

		# set severity
		for pos_no in range(0, len_mask, 2):

			_len = mask[pos_no]
			_priority = self.__util.set_priority(mask[pos_no+1])

			self.__logni_mask_severity[_len] = _priority
			self.__util.debug('mask: len=%s, priority=%s', (_len, _priority))

			del _len, _priority

		self.__util.debug('mask: self.__logni_mask_severity=%s', self.__logni_mask_severity)
		self.__config['mask'] = mask

		return True


	# log use?
	def __log_use(self, severity:str, priority:int=1):
		""" Use log?

		@param severity
		@param priority

		@return exitcode """

		self.__util.debug('__log_use: severity=%s, priority=%s', (severity, priority))

		priority = self.__util.set_priority(priority)

		# if mask=ALL
		if self.__config['mask'] == 'ALL':
			self.__util.debug('__log_use: severity=%s, msg priority=%s ' + \
				'>= mask=ALL -> msg log is VISIBLE',\
				(severity, priority))
			return True

		if severity[0] not in self.__logni_mask_severity:
			self.__util.debug('__log_use: severity=%s not exist', severity)
			return False

		# message hidden
		_priority = self.__logni_mask_severity[severity[0]]
		if priority < _priority:
			self.__util.debug('__log_use: severity=%s, msg priority=%s < ' + \
				'mask priority=%s -> msg log is HIDDEN',\
				(severity, priority, _priority))
			return False

		# message visible
		self.__util.debug('__log_use: severity=%s, msg priority=%s >= ' + \
			'mask priority=%s -> msg log is VISIBLE',\
			(severity, priority, _priority))

		return True


	def __log_message(self, severity:str, msg:str, priority:int):
		""" message """

		# stack
		stack_list = []
		offset = self.__config['stackOffset'] + 1
		limit = self.__config['stackDepth'] + offset
		for tes in traceback.extract_stack(limit=limit)[:-offset]:
			stack_list.append(f'{tes[0].split("/")[-1]}:{tes[2]}():{tes[1]}')
		slist = ','.join(stack_list)

		xrand = random.SystemRandom().randint(1, 4294967295)
		time_format = time.strftime(self.__config['timeFormat'], time.localtime())
		spriority = f'{severity[0]}{priority}'

		log_message = f"{time_format} [{os.getpid()}] {self.__name} {spriority}: {msg} [{xrand}] {slist}"

		return log_message, xrand


	def log(self, severity:str, msg:str, params:tuple=(), priority:int=1):
		""" Log message

		@param msg
		@param params
		@param severity
		@param priority

		@return struct """
		# pylint: disable=broad-exception-caught

		# priority
		priority = self.__util.set_priority(priority)

		# log use?
		if not self.__log_use(severity, priority):
			return {'msg':msg, 'severity':severity, 'priority':priority, 'use':False}

		try:
			msg = msg % params
		except TypeError as temsg:
			msg = f'!! {msg} {params} <{temsg}>'
		except BaseException as bemsg:
			msg = f'!! {msg} {params} <{bemsg}>'

		# unicode test
		# if isinstance(msg, types.UnicodeType):
		# msg = msg.encode(self.__config['charset'], 'ignore')

		# strip message
		if self.__config['strip']:
			msg = msg.replace('\n', ' ').strip()

		# max len
		msg = self.__util.log_max_len(msg)

		# log message
		log_message, xrand = self.__log_message(severity, msg, priority)

		# log to file / console
		self.__file.log(log_message)
		self.__console.log(log_message, severity)

		return {'msg':msg, 'severity':severity, 'priority':priority, 'use':True, 'hash':xrand}

	# ---

	def traceback(self, exc, priority:int=1):
		""" Traceback exception """
		# pylint: disable=broad-exception-caught

		try:
			exc_type = exc.__class__
			exc_tb = exc.__traceback__
			exc_value = exc
		except BaseException as base_err:
			exc_type, exc_value, exc_tb = sys.exc_info()
			del base_err

		tbt = traceback.TracebackException(exc_type, exc_value, exc_tb)
		msg = '\\n'.join(tbt.format())

		return self.log(self.cfg.SEVERITY_CRITICAL, msg, (), priority)


	def critical(self, msg:str, params:tuple=(), priority:int=1):
		""" Critical: critical / fatal message

		@param msg
		@param params
		@param priority

		@return struct """

		return self.log(self.cfg.SEVERITY_CRITICAL, msg, params, priority)

	fatal = critical


	def error(self, msg:str, params:tuple=(), priority:int=1):
		""" Error: error message

		@param msg
		@param params
		@param priority

		@return struct """

		return self.log(self.cfg.SEVERITY_ERROR, msg, params, priority)

	err = error


	def warn(self, msg:str, params:tuple=(), priority:int=1):
		""" Warn: warning message

		@param msg
		@param params
		@param priority

		@return struct """

		return self.log(self.cfg.SEVERITY_WARN, msg, params, priority)

	warning = warn


	def info(self, msg:str, params:tuple=(), priority:int=1):
		""" Info: informational messages

		@param msg
		@param params
		@param priority

		@return struct """

		return self.log(self.cfg.SEVERITY_INFO, msg, params, priority)

	informational = info


	def debug(self, msg:str, params:tuple=(), priority:int=1):
		""" Debug: debug-level messages

		@param msg
		@param params
		@param priority

		@return struct """

		return self.log(self.cfg.SEVERITY_DEBUG, msg, params, priority)

	dbg = debug


	def emergency(self, msg:str, params:tuple=()):
		""" Emergency: system is unusable

		critical(msg, priority=4) """

		return self.critical(msg, params, priority=4)


	def alert(self, msg:str, params:tuple=()):
		""" Alert: action must be taken immediately

		error(msg, priority=3) """

		return self.error(msg, params, priority=3)


	def notice(self, msg:str, params:tuple=()):
		""" Notice: normal but significant condition

		info(msg, priority=1) """

		return self.info(msg, params, priority=1)


	def timer(self, func):
		""" Timer: print the runtime of the decorated function """

		@functools.wraps(func)
		def log_wrapper_timer(*args, **kwargs):
			""" log wrapper timer """

			start_time = time.time()
			ret = func(*args, **kwargs)
			run_time = int((time.time() - start_time) * 1000)

			self.info('func %s() in %sms', (func.__name__, run_time), priority=1)

			return ret

		return log_wrapper_timer

# run: python test/example/basic_example.py

#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Basic example
"""

import time
import logni
from logni import log

LOGNI_MASK = 'I3E1C1W2'
LOGNI_CONSOLE = True
LOGNI_FILENAME = f'/tmp/basic-{time.time()}.log'
LOGNI_DEBUG = True

LOG = logni.Logni({'mask':LOGNI_MASK, 'debugMode':LOGNI_DEBUG, 'name':'BASICTEST',\
	'logFile':LOGNI_FILENAME})
LOG.console(LOGNI_CONSOLE)
LOG.mask(LOGNI_MASK)
print()

# alias method for log.ni()
print('$ logni.critical(\'critical message\')')
LOG.critical('critical message', ())
print('---')
print()

print("$ logni.error('error message #%s', time.time(), priority=4)")
LOG.error('error message #%s', time.time(), priority=4)
print('---')
print()

print("$ logni.warn('warn message #%s', time.time(), priority=3)")
LOG.warning('warn message #%s', time.time(), priority=3)
print('---')
print()

print("$ logni.info('info message #%s', time.time(), priority=2)")
LOG.info('info message #%s', time.time(), priority=2)
print('---')
print()

print("$ logni.debug('debug message #%s', time.time(), priority=1)")
LOG.debug('debug message #%s', time.time(), priority=1)
print('---')
print()

print('$ logni.traceback()')
try:
	3/0
except ZeroDivisionError as zerr:
	LOG.traceback(zerr)
print('---')
print()

LOG.info('info message without params', priority=4)

# ---

print('info:')
log.info('info test')
print()

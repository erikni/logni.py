#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Basic example
"""

import time
import logni

FILENAME = '/tmp/basic-%s.log' % time.time()
LOG = logni.Logni({'mask':'I3E1C1W2', 'debugMode':True, 'name':'logname', 'logFile':FILENAME})


# console
LOG.console(True)

# alias method for log.ni()
print('# logni.critical(\'critical message\')')
LOG.critical('critical message', ())
print('---')

print("# logni.error('error message #%s', time.time(), priority=4)")
LOG.error('error message #%s', time.time(), priority=4)
print('---')

print("# logni.warning('warning message #%s', time.time(), priority=3)")
LOG.warning('warning message #%s', time.time(), priority=3)
print('---')

print("# logni.info('info message #%s', time.time(), priority=2)")
LOG.info('info message #%s', time.time(), priority=2)
print('---')

print("# logni.debug('debug message #%s', time.time(), priority=1)")
LOG.debug('debug message #%s', time.time(), priority=1)
print('---')

LOG.info('info message without params', priority=4)

#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import time

sys.path.append('../../src')
sys.path.append('src')

import logni


LOG = logni.Logni({'mask':'I3E1C1W2', 'debugMode':True})


# console
LOG.console(True)


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

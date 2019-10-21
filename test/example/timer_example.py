
#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Timer example
"""

import sys
import sys

sys.path.append('../../src')
sys.path.append('src')

import logni

LOG = logni.Logni({'mask':'ALL', 'debugMode':True})

@LOG.timer
def wasteSomeTime(no):
	""" waste some time """

	for _ in range(no):
		sum([i**2 for i in range(10000)])


wasteSomeTime(1)
wasteSomeTime(999)

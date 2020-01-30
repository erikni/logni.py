
#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Timer example
"""

import logni

LOG = logni.Logni({'mask':'ALL', 'debugMode':True})

@LOG.timer
def wasteSomeTime(no):
	""" waste some time """

	for _ in range(no):
		sum([i**2 for i in range(10000)])


@LOG.timer
def wasteSomeTime2(no, rangeNo):
	""" waste some time """

	for _ in range(no):
		sum([i**2 for i in range(rangeNo)])


wasteSomeTime(1)
wasteSomeTime(999)

print('---')

wasteSomeTime2(1, 10)
wasteSomeTime2(999, 1000)

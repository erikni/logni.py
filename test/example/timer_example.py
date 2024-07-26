
#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Timer example
"""

import logni

LOG = logni.Logni({'mask':'ALL', 'debugMode':True})

@LOG.timer
def waste_some_time(xno):
	""" waste some time """

	for _ in range(xno):
		sum(y**2 for y in list(range(10000)))


@LOG.timer
def waste_some_time2(xno, range_no):
	""" waste some time """

	for _ in range(xno):
		sum(i**2 for i in list(range(range_no)))


waste_some_time(1)
waste_some_time(999)

print('---')

waste_some_time2(1, 10)
waste_some_time2(999, 1000)

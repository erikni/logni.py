 [ ![Download](https://api.bintray.com/packages/logni/deb/python-logni/images/download.svg) ](https://bintray.com/logni/deb/python-logni/_latestVersion)

# logni
Logging facility for Python

---

Example:

`# python`

`>>> from logni import log`

`>>> log.mask('ALL')` 

`>>> log.stderr(1)`

`# log.ni( 'tests %s %s', (11, 22), INFO=3 )`

2016/04/01 22:08:18 [15489] I3: tests 11 22 [17ed5aec] {logni.py:<module>():196}

`# log.critical( 'critical message' )`

2016/04/01 22:08:18 [15489] F4: critical message [7e995d1a] {logni.py:fatal():161}

`# log.error( 'error message   #%s', time.time(), level=4 )`

2016/04/01 22:08:18 [15489] E4: error message   #1459541298.29 [58138001] {logni.py:error():164}

`# log.warning( 'warning message #%s', time.time(), level=3 )`

2016/04/01 22:08:18 [15489] W3: warning message #1459541298.29 [91b483ab] {logni.py:warn():167}

`# log.info( 'info message    #%s', time.time(), level=2 )`

2016/04/01 22:08:18 [15489] I2: info message    #1459541298.29 [eaf58c15] {logni.py:info():170}

`# log.debug( 'debug message   #%s', time.time(), level=1 )`

2016/04/01 22:08:18 [15489] D1: debug message   #1459541298.29 [37e911b8] {logni.py:debug():173}

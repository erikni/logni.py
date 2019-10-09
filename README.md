[![Codacy Badge](https://api.codacy.com/project/badge/Grade/441b9bb67c0f4956b5d4bcfbe76e00c6)](https://www.codacy.com/manual/erikni/logni.py?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=erikni/logni.py&amp;utm_campaign=Badge_Grade)
[![Github Releases](https://img.shields.io/github/downloads/atom/atom/latest/total.svg)](https://github.com/erikni/logni.py/releases)
[![Build Status](https://api.travis-ci.org/erikni/logni.py.svg?branch=develop)](http://travis-ci.org/erikni/logni.py)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENCE)

# logni.py
logni is a python library for event logging and application states

## How to install?
- git (github)
- pip (python packages -> todo)


Install from Github
```
$ git clone https://github.com/erikni/logni.py.git
$ cd logni.py
$ pip install -r requirements.txt
$ python src/logni.py
```

## Example

```
$ python

>>> import logni
>>> log = logni.Logni()

>>> log.mask('ALL')
>>> log.stderr(1)

$ log.log('tests %s %s', (11, 22), INFO=3)
2016/04/01 22:08:18 [15489] I3: tests 11 22 [17ed5aec] {logni.py:<module>():196}

$ log.critical('critical message')
2016/04/01 22:08:18 [15489] F4: critical message [7e995d1a] {logni.py:fatal():161}

$ log.error('error message #%s', time.time(), priority=4)
2016/04/01 22:08:18 [15489] E4: error message #1459541298.29 [58138001] {logni.py:error():164}

$ log.warn('warning message #%s', time.time(), priority=3)
2016/04/01 22:08:18 [15489] W3: warning message #1459541298.29 [91b483ab] {logni.py:warn():167}

$ log.info('info message #%s', time.time(), priority=2)
2016/04/01 22:08:18 [15489] I2: info message #1459541298.29 [eaf58c15] {logni.py:info():170}

$ log.debug('debug message #%s', time.time(), priority=1)
2016/04/01 22:08:18 [15489] D1: debug message #1459541298.29 [37e911b8] {logni.py:debug():173}
```

## Test

[test/unit](https://github.com/erikni/logni.py/tree/develop/test/unit)

## Contribution

[Pull Requests](https://github.com/erikni/logni.py/pulls) are very welcome.

# Licence

[GNU General Public License v3.0](LICENSE)

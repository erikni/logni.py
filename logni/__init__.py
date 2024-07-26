#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
logni init
"""

from logni.utilni import Util
from logni.filestream import FileStream
from logni.consolestream import ConsoleStream
from logni.logni import Logni
from logni.cfgni import Cfgni

#pylint: disable=invalid-name
log = Logni()

__all__ = ['Util', 'FileStream', 'ConsoleStream', 'Logni', 'log', 'Cfgni']

#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
logni init
"""

from .utilni import Util
from .filestream import FileStream
from .consolestream import ConsoleStream
from .logni import Logni

#pylint: disable=invalid-name
log = Logni()

__all__ = ['Util', 'FileStream', 'ConsoleStream', 'Logni', 'log']

#!/usr/bin/python
# -*- coding: utf-8 -*-

import pytest


def testFuncFast():
    pass


@pytest.mark.slow
def testFuncSlow():
    pass

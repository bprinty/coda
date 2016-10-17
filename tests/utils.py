#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# testing utilities
# 
# @author <bprinty@gmail.com>
# ------------------------------------------------


# import
# ------
import os
from functools import wraps
import unittest


# decorators
# ----------
def remote(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        test = os.getenv('GENOVA_TEST_REMOTE', None)
        if test:
            return func(*args, **kwargs)
        return
    return decorator


# classes
# -------
class ModelTest(unittest.TestCase):
    """
    Abstract factory class for common model testing functionality. 
    """
    pass
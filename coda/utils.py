# -*- coding: utf-8 -*-
#
# Commonly used utilities for development.
# 
# @author <bprinty@gmail.com>
# ------------------------------------------------


# imports
# -------
import inspect
from functools import wraps
from gems import composite


# metaclasses
# -----------
class DocRequire(type):
    """
    Metaclass forcing requirement of docstrings on all public
    class methods.
    """

    def __init__(self, name, bases, attrs):
        for key, value in attrs.items():
            if key.startswith("__") or key.startswith("_"):
                continue
            if not hasattr(value, "__call__"):
                continue
            if not getattr(value, '__doc__'):
                raise TypeError("%s must have a docstring" % key)
        type.__init__(self, name, bases, attrs)


# decorators
# ----------
def keywords(func):
    """
    Accumulate all arguments as keyword argument dictionary.

    Examples:
        >>> @allkw
        >>> def test(*args, **kwargs):
        >>>     return kwargs
        >>>
        >>> print test({'one': 1}, two=2)
        {'one': 1, 'two': 2}
    """
    @wraps(func)
    def _(*args, **kwargs):
        idx = 0 if inspect.ismethod(func) else 1
        if len(args) > idx:
            if isinstance(args[idx], (dict, composite)):
                for key in args[idx]:
                    kwargs[key] = args[idx][key]
                args = args[:idx]
        return func(*args, **kwargs)
    return _

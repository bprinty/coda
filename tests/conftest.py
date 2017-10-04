# -*- coding: utf-8 -*-
#
# pytest plugins
# 
# @author <bprinty@asuragen.com>
# ------------------------------------------------


# imports
# -------
import os
import pytest
import logging
import coda
from . import tearDown, cl


# config
# ------
logging.basicConfig(level=logging.ERROR)


# plugins
# -------
def pytest_addoption(parser):
    parser.addoption("-E", action="store", metavar="NAME",
        help="only run tests matching the environment NAME.")
    return


def pytest_configure(config):
    # register an additional marker
    config.addinivalue_line("markers",
        "env(name): mark test to run only on named environment")
    return


def pytest_runtest_setup(item):
    envmarker = item.get_marker("env")
    if envmarker is not None:
        envname = envmarker.args[0]
        if envname != item.config.getoption("-E"):
            pytest.skip("test requires env %r" % envname)
    return


@pytest.fixture(autouse=True)
def bootstrap():
    global __user_config__
    cwd = os.path.dirname(os.path.realpath(__file__))
    coda.db.__user_config__ = os.path.join(cwd, 'resources', '.coda')
    coda.db.options()
    coda.db.session.db.files.drop()
    coda.add(cl)
    yield
    coda.delete(cl)
    return

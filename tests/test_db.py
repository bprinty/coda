#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# testing for coda
# 
# @author <bprinty@gmail.com>
# ------------------------------------------------


# imporobj
# -------
import unittest
import os
import json
import subprocess
from nose_parameterized import parameterized

import coda


# session
# -------
class TestSession(unittest.TestCase):

    def test_properties(self):
        coda.options()
        self.assertEqual(coda.db.session.host, 'localhost')
        self.assertEqual(coda.db.session.port, 27017)
        self.assertEqual(coda.db.session.write, True)
        self.assertEqual(coda.db.session.dbname, 'coda-testing')
        self.assertEqual(coda.db.session.db.__class__.__name__, 'Database')
        return

    def test_options(self):
        coda.options(host='newhost')
        self.assertEqual(coda.db.session.host, 'newhost')
        return


# searching
# ---------
class TestFind(unittest.TestCase):
    """
    Test search functionality for coda.
    """

    @parameterized.expand([
        ({'type': 'text'}, 4),
        ({'type': 'source'}, 3),
    ])
    def test_find(self, query, count):
        ret = coda.find(query)
        self.assertTrue(isinstance(ret, coda.Collection))
        self.assertEqual(len(ret), count)
        return

    @parameterized.expand([
        ({'type': 'text'}, 'one.txt'),
        ({'type': 'source'}, 'db.py'),
    ])
    def test_find_one(self, query, name):
        ret = coda.find_one(query)
        self.assertTrue(isinstance(ret, coda.File))
        self.assertEqual(ret.name, name)
        return


class TestDeletes(unittest.TestCase):
    """
    Test search functionality for coda.
    """

    @parameterized.expand([
        (os.path.realpath(__file__)),
    ])
    def test_add_delete(self, path):
        # add
        fi = coda.File(path=path, metadata={
            'cohort': 'testing',
            'ext': 'py',
            'type': 'source'
        })
        coda.add(fi)
        cl = coda.find({'cohort': 'testing'})
        self.assertEqual(len(cl), 1)
        self.assertEqual(cl[0].type, 'source')
        # update
        fi.metadata.type = 'newtype'
        fi.metadata.keep = True
        coda.add(fi)
        cl = coda.find({'cohort': 'testing'})
        self.assertEqual(cl[0].type, 'newtype')
        self.assertEqual(cl[0].keep, True)
        # delete
        coda.delete(fi)
        cl = coda.find({'cohort': 'testing'})
        self.assertEqual(cl, None)
        return



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
import subprocess

import coda


# session
# -------
class TestEntryPoints(unittest.TestCase):

    def call(self, subcommand, *args):
        wd = os.path.realpath(os.path.join(coda.db.__base__, '..'))
        return subprocess.check_output('PYTHONPATH={} python {}/coda/__main__.py -c {} {} {}'.format(
            wd, wd, coda.db.__user_config__, subcommand, ' '.join(args)
        ), stderr=subprocess.STDOUT, shell=True)

    def test_status(self):
        res = self.call('status')
        self.assertTrue('good to go!' in res)
        return

    def test_find(self):
        path = os.path.realpath(__file__)
        fi = coda.File(path=path, metadata={
            'cohort': 'testing',
            'ext': 'py',
            'type': 'source'
        })
        coda.add(fi)
        res = self.call('find', 'cohort', 'testing')
        self.assertTrue('tests/test_coda.py' in res)
        coda.delete(fi)
        return

    def test_show(self):
        path = os.path.realpath(__file__)
        fi = coda.File(path=path, metadata={
            'cohort': 'testing',
            'ext': 'py',
            'type': 'source'
        })
        coda.add(fi)
        res = self.call('show', path)
        self.assertTrue('"cohort": "testing"' in res)
        self.assertTrue('"ext": "py"' in res)
        self.assertTrue('"type": "source"' in res)
        coda.delete(fi)
        return

    def test_add(self):
        path = os.path.realpath(__file__)
        self.call('add', path)
        fi = coda.find_one({'path': path})
        self.assertEqual(fi.name, 'test_coda.py')
        coda.delete(fi)
        return

    def test_delete(self):
        path = os.path.realpath(__file__)
        fi = coda.File(path)
        coda.add(fi)
        self.call('delete', path)
        fi = coda.find_one({'path': path})
        self.assertEqual(fi, None)
        return

    def test_tag(self):
        path = os.path.realpath(__file__)
        self.call('tag', path, 'cohort', 'testing')
        fi = coda.find_one({'cohort': 'testing'})
        self.assertEqual(fi.name, 'test_coda.py')
        coda.delete(fi)
        return


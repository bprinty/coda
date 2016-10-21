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

from . import __resources__
import coda


# file
# ----
class TestFile(unittest.TestCase):

    @parameterized.expand([
        ('one', os.path.join(__resources__, 'simple', 'one.txt'), {'one': 1}),
        ('two', os.path.join(__resources__, 'simple', 'two', 'two.txt'), {'one': 1, 'two': 2})
    ])
    def test_properties(self, name, filepath, metadata):
        fi = coda.File(filepath, metadata=metadata)
        self.assertEqual(fi.path, filepath)
        self.assertEqual(fi.location, os.path.dirname(filepath))
        self.assertEqual(fi.name, os.path.basename(filepath))
        self.assertEqual(fi.extension, '.' + filepath.split('.')[-1])
        for key in metadata:
            self.assertEqual(fi.metadata[key], metadata[key])
            self.assertEqual(getattr(fi, key), metadata[key])
            self.assertEqual(fi[key], metadata[key])
        return

    def test_metadata(self):
        # test metadata setting
        one = os.path.join(__resources__, 'simple', 'one.txt')
        fi = coda.File(one, metadata={'one': 1})
        self.assertEqual(fi.one, 1)
        fi.two = 2
        self.assertEqual(fi.metadata.two, 2)

        # test implicit querying for files already in the database
        coda.add(fi)
        fi2 = coda.File(one)
        self.assertEqual(fi.one, 1)
        self.assertEqual(fi.metadata.one, 1)
        coda.delete(fi)
        return

    def test_operators(self):
        one = os.path.join(__resources__, 'simple', 'one.txt')
        two = os.path.join(__resources__, 'simple', 'two', 'two.txt')
        three = os.path.join(__resources__, 'simple', 'three', 'three.txt')
        f1 = coda.File(one, metadata={'filetype': 'text', 'content': 'data'})
        f2 = coda.File(two, metadata={'filetype': 'text', 'content': 'nothing'})
        f3 = coda.File(three, metadata={'filetype': 'text', 'content': 'something'})

        # contains
        self.assertTrue('one' in one)
        self.assertFalse('two' in one)

        # addition
        cl1 = f1 + f2
        self.assertTrue(isinstance(cl1, coda.Collection))
        self.assertTrue(f1 in cl1)
        self.assertTrue(f2 in cl1)
        cl2 = f3 + cl1
        self.assertTrue(isinstance(cl2, coda.Collection))
        self.assertTrue(f1 in cl2)
        self.assertTrue(f2 in cl2)
        self.assertTrue(f3 in cl2)

        # equality
        self.assertEqual(f1, coda.File(one))
        return

    def test_exceptions(self):
        with self.assertRaises(TypeError):
            one = os.path.join(__resources__, 'simple', 'one.txt')
            f1 = coda.File(one, metadata={'filetype': 'text', 'content': 'data'})
            c1 = f1 + 1
            c1 = f1 + 'str'
        return


# collection
# ----------
class TestCollection(unittest.TestCase):

    def test_properties(self):
        one = os.path.join(__resources__, 'simple', 'one.txt')
        two = os.path.join(__resources__, 'simple', 'two', 'two.txt')
        three = os.path.join(__resources__, 'simple', 'three', 'four', 'four.txt')
        f1 = coda.File(one, metadata={'filetype': 'text', 'content': 'data'})
        f2 = coda.File(two, metadata={'filetype': 'text', 'content': 'nothing'})
        f3 = coda.File(three, metadata={'filetype': 'text', 'content': {'some': 'data'}})
        cl = f1 + f2 + f3
        self.assertEqual(len(cl.files), 3)
        self.assertEqual(cl.files[0].path, one)
        self.assertEqual(cl.files[1].path, two)
        self.assertEqual(cl.files[2].path, three)
        self.assertEqual(cl.metadata.filetype, 'text')
        self.assertEqual(cl.filetype, 'text')
        self.assertEqual(cl.filelist, [one, two, three])
        with self.assertRaises(AttributeError):
            self.assertEqual(cl.metadata.content, None)
        return

    def test_properties_filetree(self):
        cl = coda.Collection(os.path.join(__resources__, 'simple'))
        self.assertEqual(
            map(lambda x: x.name, cl.files),
            ['one.txt', 'four.txt', 'three.txt', 'two.txt']
        )
        return

    def test_filter(self):
        cl = coda.Collection(os.path.join(__resources__, 'simple'))
        cl2 = cl.filter(lambda x: 'o' in x.name)
        self.assertEqual(
            map(lambda x: x.name, cl2.files),
            ['one.txt', 'four.txt', 'two.txt']
        )
        return

    def test_operators(self):
        one = os.path.join(__resources__, 'simple', 'one.txt')
        two = os.path.join(__resources__, 'simple', 'two', 'two.txt')
        three = os.path.join(__resources__, 'simple', 'three', 'four', 'four.txt')
        f1 = coda.File(one, metadata={'filetype': 'text', 'content': 'data'})
        f2 = coda.File(two, metadata={'filetype': 'text', 'content': 'nothing'})
        f3 = coda.File(three, metadata={'filetype': 'text', 'content': {'some': 'data'}})
        # addition
        cl = f1 + f2
        self.assertTrue(isinstance(cl, coda.Collection))
        self.assertEqual(cl.files, [f1, f2])
        cl2 = cl + f3
        self.assertTrue(isinstance(cl2, coda.Collection))
        self.assertEqual(cl2.files, [f1, f2, f3])
        cl3 = f3 + cl
        self.assertTrue(isinstance(cl3, coda.Collection))
        self.assertEqual(cl3.files, [f3, f1, f2])
        self.assertEqual(cl + cl2, cl3)
        # subtraction
        self.assertEqual(cl, cl2 - f3)
        self.assertEqual(cl2 - cl, coda.Collection(files=[f3]))
        # equality
        self.assertNotEqual(f1, f2)
        self.assertEqual(f1, cl[0])
        # contains
        self.assertTrue(f1 in cl)
        self.assertFalse(f3 in cl)
        # iteration
        self.assertEqual([i for i in cl], [i for i in cl.files])
        return

    def test_add_metadata(self):
        one = os.path.join(__resources__, 'simple', 'one.txt')
        two = os.path.join(__resources__, 'simple', 'two', 'two.txt')
        three = os.path.join(__resources__, 'simple', 'three', 'four', 'four.txt')
        f1 = coda.File(one, metadata={'filetype': 'text', 'content': 'data'})
        f2 = coda.File(two, metadata={'filetype': 'text', 'content': 'nothing'})
        f3 = coda.File(three, metadata={'filetype': 'text', 'content': {'some': 'data'}})
        cl = f1 + f2 + f3
        # adding via keyword arguments
        cl.add_metadata(newproperty='value')
        self.assertEqual(cl.metadata.newproperty, 'value')
        self.assertEqual(cl.newproperty, 'value')
        self.assertEqual(map(lambda x: x.newproperty, cl), ['value']*len(cl))
        # adding via dictionary
        cl.add_metadata({'newerproperty': 'newervalue'})
        self.assertEqual(cl.metadata.newerproperty, 'newervalue')
        self.assertEqual(cl.newerproperty, 'newervalue')
        self.assertEqual(map(lambda x: x.newerproperty, cl), ['newervalue']*len(cl))
        # adding via setattr on class
        cl.newestproperty = 'newestvalue'
        self.assertEqual(cl.metadata.newestproperty, 'newestvalue')
        self.assertEqual(cl.newestproperty, 'newestvalue')
        self.assertEqual(map(lambda x: x.newestproperty, cl), ['newestvalue']*len(cl))
        return

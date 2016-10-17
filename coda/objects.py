# -*- coding: utf-8 -*-
#
# All ensembl-based object models
# 
# @author <bprinty@gmail.com>
# ------------------------------------------------


# imports
# -------
import os
from gems import composite, filetree

from coda.utils import DocRequire, keywords


# files
# -----
class File(object):
    """
    Abstract class for file object.

    Args:
        path (list): List of file object to manage.
        metadata (dict): Dictionary with common metadata for collection,
            specified a priori.
    """
    __metaclass__ = DocRequire

    def __init__(self, path, metadata={}):
        assert os.path.exists(path), 'Specified file path does not exist!'
        assert not os.path.isdir(path), 'Specified file is not a file! Use the Collection object for a directory.'
        self.path = path
        self._metadata = composite(metadata)
        return

    @property
    def name(self):
        """
        Return basename for file.
        """
        return os.path.basename(self.path)

    @property
    def location(self):
        """
        Return dirname for file.
        """
        return os.path.dirname(self.path)

    @property
    def extension(self):
        """
        Return extension for file.
        """
        return '.' + self.name.split('.')[-1]

    @property
    def metadata(self):
        """
        Proxy for returning metadata about specified file.
        """
        return self._metadata

    def __cmp__(self, other):
        if not isinstance(other, File):
            TypeError('unsupported comparison type(s) \'{}\' and \'{}\''.format(type(self), type(other)))
        return cmp(self.path, other.path)

    def __str__(self):
        return self.path

    def __eq__(self, other):
        if isinstance(other, File):
            return self.path == other.path
        else:
            return False

    def __add__(self, other):
        if isinstance(other, File):
            if self == other:
                return Collection(files=[self])
            else:
                return Collection(files=[self, other])
        elif isinstance(other, Collection):
            if self in other:
                return other
            else:
                return Collection(files=[self] + other.files)
        else:
            raise TypeError('unsupported operand type(s) for +: \'{}\' and \'{}\''.format(type(self), type(other)))
        return

    def __getattr__(self, name):
        return self.metadata[name]

    def __getitem__(self, name):
        return self.metadata[name]

    def __setattr__(self, name, value):
        if name not in ['_metadata', 'path']:
            self.metadata[name] = value
        else:
            super(File, self).__setattr__(name, value)
        return


class Collection(object):
    """
    Abstract class for collection of file objects.

    Args:
        files (list): List of file objects to manage, or path to directory
            to generate collection from.
        metadata (dict): Dictionary with common metadata for collection,
            specified a priori.
    """
    __metaclass__ = DocRequire

    def __init__(self, files, metadata={}):
        if isinstance(files, basestring):
            assert os.path.exists(files), 'Specified path does not exist!'
            assert os.path.isdir(files), 'Specified path is not a directory! Use the File object for a file.'
            ft = filetree(files)
            self.files = map(lambda x: File(x), ft.filelist())
        else:
            self.files = files
        self._metadata = composite(metadata)
        return

    @property
    def metadata(self):
        """
        If no metadata is initially specified for a file, query the database
        for metadata about the specified file.
        """
        if len(self._metadata) == 0:
            res = self.files[0].metadata
            for idx in range(1, len(self.files)):
                res = res.intersection(self.files[idx].metadata)
            self._metadata = res
        return self._metadata

    @keywords
    def add_metadata(self, *args, **kwargs):
        """
        Add metadata for all objects in the collection. 
        """
        for idx in range(0, len(self.files)):
            for key in kwargs:
                self.files[idx].metadata[key] = kwargs[key]
        for key in kwargs:
            self.metadata[key] = kwargs[key]
        return

    def filter(self, func=lambda x: True):
        """
        Filter collection using specified function.

        Args:
            func (function): Function to filter with.
        """
        return Collection(filter(func, self.files))

    def __str__(self):
        return '\n'.join(map(str, self.files))

    def __cmp__(self, other):
        return cmp(len(self.files), len(other.files))

    def __iter__(self):
        for obj in self.files:
            yield obj

    def __len__(self):
        return len(self.files)

    def __contains__(self, item):
        return item in self.files

    def __add__(self, other):
        if isinstance(other, File):
            res = map(lambda x: x, self.files)
            if other not in self:
                res += [other]
            return Collection(files=res, metadata=self._metadata)
        elif isinstance(other, Collection):
            res = map(lambda x: x, self.files)
            for item in other.files:
                if item not in self:
                    res += [item]
            return Collection(files=res, metadata=self._metadata)
        else:
            raise TypeError('unsupported operand type(s) for +: \'{}\' and \'{}\''.format(type(self), type(other)))
        return

    def __sub__(self, other):
        if isinstance(other, File):
            return Collection(files=filter(lambda x: x != other, self.files))
        elif isinstance(other, Collection):
            return Collection(files=filter(lambda x: x not in other, self.files))
        else:
            raise TypeError('unsupported operand type(s) for +: \'{}\' and \'{}\''.format(type(self), type(other)))
        return

    def __getattr__(self, name):
        return self.metadata[name]

    def __getitem__(self, idx):
        return self.files[idx]

    def __setattr__(self, name, value):
        if name not in ['_metadata', 'files']:
            self.add_metadata({name: value})
        else:
            super(Collection, self).__setattr__(name, value)
        return

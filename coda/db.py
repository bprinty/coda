# -*- coding: utf-8 -*-
#
# All ensembl-based object models
# 
# @author <bprinty@gmail.com>
# ------------------------------------------------


# imports
# -------
import os
from cached_property import cached_property
import pymongo
from gems import composite
from multipledispatch import dispatch

from coda.objects import File, Collection
from coda.utils import DocRequire, keywords


# config
# ------
__base__ = os.path.dirname(os.path.realpath(__file__))
__default_config__ = os.path.join(__base__, '.coda')
__user_config__ = os.path.join(os.getenv("HOME"), '.coda')


# database config
# ---------------
class Session(object):
    """
    Object for managing connection to internal database.

    Args:
        host (str): Host with database to connect to.
        port (int): Port to connect to database with.
        write (bool): Whether or not to allow writing to the database.
        dbname (str): Name of database to use.
    """

    def __init__(self, host='localhost', port=27017, write=True, dbname='coda'):
        self.host = host
        self.port = port
        self.write = write
        self.dbname = dbname
        self._db = None
        return

    @property
    def db(self):
        """
        Internal property for managing connection to mongodb database.
        """
        if self._db is None:
            try:
                client = pymongo.MongoClient(self.host, self.port)
                self._db = client[self.dbname]
            except pymongo.errors.ServerSelectionTimeoutError:
                self._db = None
                raise AssertionError('Could not connect to database! Try using `mongod` to start mongo server.')
        return self._db


@keywords
def options(*args, **kwargs):
    """
    Set options for the current session.

    Args:
        kwargs (dict): List of arbitrary config items to set.
    """
    global session, __default_config__, __user_config__
    with open(__default_config__, 'r') as cfig:
        config = composite(cfig)
    if os.path.exists(__user_config__):
        with open(__user_config__, 'r') as cfig:
            config = config + composite(cfig)
    if len(kwargs) != 0:
        config = config + composite(kwargs)
    try:
        session = Session(**config._dict)
    except TypeError:
        raise AssertionError('Something is wrong with your coda configuration'
                             ' -- check your config file for valid parameters.')
    return config


session = Session()
options()


# searching
# ---------
def find(query):
    """
    Search database for files with specified metadata.
    """
    files = []
    for item in session.db.files.find(query):
        path = item.get('path')
        if path is None:
            raise AssertionError('Path information for file not available -- '
                                 'your database is in a weird state. Please '
                                 'ensure that each record in the database has '
                                 'an associated path.')
        item.pop('path', None)
        files.append(File(path=path, metadata=item))
    if len(files) == 0:
        return None
    return Collection(files=files)


def find_one(query):
    """
    Search database for one files with specified metadata.
    """
    item = session.db.files.find_one(query)
    if item is None:
        return None
    path = item.get('path')
    if path is None:
        raise AssertionError('Path information for file not available -- '
                             'your database is in a weird state. Please '
                             'ensure that each record in the database has '
                             'an associated path.')
    item.pop('path', None)
    return File(path=path, metadata=item)


# database update methods
# -----------------------
def add(obj):
    """
    Add file object or collection object to database.

    Args:
        obj (File, Collection): File or collection of files to delete.
    """
    global session
    if isinstance(obj, (Collection, list, tuple)):
        return map(add, obj)
    if not isinstance(obj, File):
        raise TypeError('unsupported type for add {}'.format(type(obj)))
    ret = session.db.files.find_one({'path': obj.path})
    dat = obj.metadata.json()
    dat['path'] = obj.path
    if ret is None:
        return session.db.files.insert_one(dat)
    else:
        return session.db.files.update({'path': dat['path']}, dat)


def delete(obj):
    """
    Delete file or collection of files from database.

    Args:
        obj (File, Collection): File or collection of files to delete.
    """
    global session
    if isinstance(obj, (Collection, list, tuple)):
        return map(delete, obj)
    if not isinstance(obj, File):
        raise TypeError('unsupported type for delete {}'.format(type(obj)))
    return session.db.files.delete_many({'path': obj.path})


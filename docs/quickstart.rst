Quickstart
==========

Overview
--------

Coda is a file system organizer, originally designed for data scientists who frequently deal with large amounts of heterogeneous data. In this age where data are king, being able to efficiently search and label those data is paramount to maintaining productivity. Coda provides tools for tagging, aggregating, and searching an existing file structure ... BLAH ADD MORE.

As a quick example of how to use coda to organize an arbitrary dataset, see the following example:

.. code-block:: python

    >>> import coda
    >>>
    >>> # index a filesystem for querying
    >>> coda.add('/path/to/folder')
    >>> collection = coda.find(extension='.csv')
    >>>
    >>> # print the number of csv files in that collection
    >>> print len(collection)
    5
    >>> # for each csv file that has 'testing' in the name
    >>> # add metadata about the file for searching later
    >>> files = collection.filter(search='testing.*')
    >>> print len(files)
    2
    >>> files.cohort = 'testing'
    >>> coda.add(files)
    >>>
    >>> # now search again for only those files
    >>> collection = coda.find({'cohort': 'testing'})
    >>> print len(collection)
    2
    >>> print collection
    '/path/to/folder/today/testing123.csv'
    '/path/to/folder/yesterday/testing456.csv'


The sections below give a semi-in-depth overview of the full spectrum of capabilities provided by `coda <http://github.com/bprinty/coda.git>`_. For any other inquiries on how you might be able to use this tool, or if any part of it is left un- or under-documented, contact the developers on `GitHub <http://github.com/bprinty/coda.git>`_.


Installation
------------

See the `Installation <./installation.html>`_ section for details on how to install the project. There are several components to getting coda up and running, so don't just ``pip`` your way through the installation, please actually read the `Installation <./installation.html>`_ section.


Objects
-------

Individual Files
~~~~~~~~~~~~~~~~

:class:`coda.File` objects are used throughout ``coda`` for managing properties about
files, and serve as proxies for querying operations that take place. Generally a new
:class:`coda.File` object is instantiated and tagged with metadata whenever a file
needs to be added for tracking to the coda database. To instantiate a new file, use:

.. code-block:: python
    
    >>> fi = coda.File('/path/to/my/file.txt', metadata={
        'group': 'dev',
        'sample': 'A001'
    })
    >>> print fi.metadata
    {'group': 'dev', 'sample': 'A001'}


You can also get and set metadata properties directly on the class:

.. code-block:: python

    >>> fi = coda.File('/path/to/my/file.txt')
    >>> fi.group = 'dev'
    >>> fi.sample = 'A001'
    >>> print fi.metadata
    {'group': 'dev', 'sample': 'A001'}


If a file already exists in the database, the metadata property will automatically be
populated with the content from the database:

.. code-block:: python

    >>> fi = coda.File('/path/to/my/file.txt', metadata={
        'group': 'dev',
        'sample': 'A001'
    })
    >>> coda.add(fi)
    >>>
    >>> fi2 = coda.File('/path/to/my/file.txt')
    >>> print fi2.metadata
    {'group': 'dev', 'sample': 'A001'}


Additionally, you can query the database for a single :class:`coda.File` object matching parameters
if you use the :func:`coda.find_one` query method:

.. code-block:: python

    >>> fi = coda.find_one({'group': 'dev'})
    >>> print fi
    '/path/to/my/file.txt'


Collections of Files
~~~~~~~~~~~~~~~~~~~~


Database Operations
-------------------


Adding Files to Tracking
~~~~~~~~~~~~~~~~~~~~~~~~

For adding files to the database, the :func:`coda.add` method is used. The argument to 


Updating Files with Metadata
~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Searching for Files with Metadata
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once files have been added to the database and tagged with metadata, the :func:`coda.find`
and :func:`coda.find_one`, can be used to query for files matching specific metadata criteria.
These two methods take a dictionary of query parameters as an argument and return either
a :class:`coda.File` (:func:`coda.find_one`) or :class:`coda.Collection` object (:func:`coda.find`)
containing the query results. As an example, to query files with a particular metadata tag:

.. code-block:: python

    >>> cl = coda.find({'group': 'dev'})
    >>> print cl
    '/path/to/dev/file/one.txt'
    '/path/to/dev/file/two.txt'


You can also use `MongoDB query parameters <https://docs.mongodb.com/v3.2/reference/method/db.collection.find/>`_ to do more advanced queryies on data:



Deleting Files from the Database
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Example Use Case
----------------




Notes on Performance
--------------------

.. Talk about not polluting metadata with heavy data ... heavy data should be stored
.. in files and referenced in metadata. Set-based operations for gathering metadata on
.. Collections assumes that the metadata is relatively minimal (no extremely deep data structures).







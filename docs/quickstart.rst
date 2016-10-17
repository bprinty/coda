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
    >>> for obj in files:
    >>>     obj.metadata.cohort = testing
    >>>     coda.update(obj)
    >>>
    >>> # now search again for only those files
    >>> collection = coda.search(cohort='testing')
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


Collections of Files
~~~~~~~~~~~~~~~~~~~~


Database Operations
-------------------


Adding Files to Tracking
~~~~~~~~~~~~~~~~~~~~~~~~


Updating Files with Metadata
~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Notes on Performance
--------------------

.. Talk about not polluting metadata with heavy data ... heavy data should be stored
.. in files and referenced in metadata. Set-based operations for gathering metadata on
.. Collections assumes that the metadata is relatively minimal (no extremely deep data structures).







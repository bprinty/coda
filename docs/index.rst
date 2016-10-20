.. coda documentation master file


Welcome to coda's documentation!
======================================


Introduction:
=============

Coda is a file system organizer, designed for data scientists who frequently deal
with large amounts of heterogeneous data. In this age where data rules all, being able to
efficiently search and label those data is paramount to maintaining productivity. Coda
allows you to tag files with arbitrary metadata, so that you can stay organized when
managing/analyzing large datasets over time. 

As a quick example of how coda might be useful for organizing an arbitrary dataset,
see the following example (see the `Quickstart <./quickstart.html>`_ section for more
in-depth documentation):

.. talk about the principles of coda:
..    - files are associated with metadata
..    - files are tracked
..    - coda uses mongo for the tracking
..    - you can search for files associated with metadata
..    - great for data scientists

.. separate the examples below into more readable chunks

.. code-block:: python

    >>> import coda
    >>>
    >>> # generate a collection of files from a directory
    >>> cl = coda.Collection('/path/to/test/data')
    >>>
    >>> # show all of the files in the structure
    >>> print cl
    /path/to/test/data/type1.txt
    /path/to/test/data/type1.csv
    /path/to/test/data/type2.txt
    /path/to/test/data/type2.csv
    >>>
    >>> # print the number files in that collection
    >>> print len(collection)
    4
    >>>
    >>> # set properties about the collection
    >>> cl.group = 'test'
    >>> cl.cohort = 'My Cohort'
    >>>
    >>> # add the files in the collection to the database
    >>> # for tracking and retrieval later
    >>> coda.add(cl)
    >>>
    >>> # do the same with a training dataset
    >>> cl = coda.Collection('/path/to/train/data', metadata={'group': 'train'})
    >>> coda.add(cl)
    >>>
    >>> # wait ... add one more file in a different location to
    >>> # the training set
    >>> fi = coda.File('/my/special/training/file.csv')
    >>> fi.group = 'train'
    >>> coda.add(fi)
    >>>
    >>> # ... later in time ...
    >>>
    >>> # query all of our training files
    >>> cl = coda.find({'group': 'train'})
    >>> print cl
    /path/to/train/data/type1.txt
    /path/to/train/data/type1.csv
    /path/to/train/data/type2.txt
    /path/to/train/data/type2.csv
    /my/special/training/file.csv
    >>>
    >>> # filter those by csv files
    >>> print cl.filter(lambda x: '.csv' in x.name)
    /path/to/train/data/type1.csv
    /path/to/train/data/type2.csv
    /my/special/training/file.csv
    >>>
    >>> # tag the special file with new metadata
    >>> cl.files[-1].special = True
    >>> coda.add(cl.files[-1])
    >>>
    >>> # query it back (for the example)
    >>> fi = coda.find_one({'special': True})
    >>> print fi.metadata
    {'group': 'train', 'special': True}


The topics covered in the `Quickstart <./quickstart.html>`_ section give a semi-in-depth overview of the spectrum of capabilities provided by `coda <http://github.com/bprinty/coda.git>`_. For any other inquiries on how you might be able to use this tool, or if any part of it is left un- or under-documented, contact the developers on `GitHub <http://github.com/bprinty/coda.git>`_.


Contents:
=========

.. toctree::
   :maxdepth: 2

   installation
   quickstart
   api


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


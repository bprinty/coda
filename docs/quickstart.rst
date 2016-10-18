Quickstart
==========


Installation
------------

See the `Installation <./installation.html>`_ section for details on how to install the project. There are several components to getting coda up and running (coda requires a `MongoDB <https://docs.mongodb.com/>`_ instance), so don't just ``pip`` your way through the installation, please actually read the `Installation <./installation.html>`_ section.


Files
-----

:class:`coda.File` objects are used throughout ``coda`` for managing properties about
files, and serve as proxies for querying operations that take place. Generally, a new
:class:`coda.File` object is instantiated and tagged with metadata whenever a file
needs to be added for tracking to the coda database. To instantiate a new file, use:

.. code-block:: python
    
    >>> fi = coda.File('/path/to/my/file.txt', metadata={
    >>>     'group': 'dev',
    >>>     'sample': 'A001'
    >>> })
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
    >>>     'group': 'dev',
    >>>     'sample': 'A001'
    >>> })
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
--------------------

:class:`coda.Collection` objects are used throughout ``coda`` for managing properties about
collections of files, and serve as proxies for querying operations that take place. Generally,
a new :class:`coda.Collection` object is instantiated to group sets of files together, in order
to add/update metadata shared by all :class:`coda.File` objects in the collection, or to
perform bulk database updates with all associated files. To instantiate a new collection, you can 
do it several ways:

    1. Instantiating the collection object with a list of :class:`coda.File` objects.
    2. Adding :class:`coda.File` or :class:`coda.Collection` objects together.
    3. Instantiating the collection object with the path to a directory, where all files
       in that directory are instantiated as :class:`coda.File` objects within that
       collection. Or, by
    4. Querying the database for a collection of files.


Each of these methods can be used in different contexts, depending on the application. Below are
a set of examples that detail each of the ways a :class:`coda.Collection` object can be created:

.. code-block:: python

    >>> # with file objects
    >>> one = coda.File('/path/to/file/one.txt', metadata={
    >>>     'group': 'dev',
    >>>     'sample': 'A001'
    >>> })
    >>> two = coda.File('/path/to/file/two.txt', metadata={
    >>>     'group': 'dev',
    >>>     'sample': 'A002'
    >>> })
    >>> collection = Collection([one, two])
    >>>
    >>> # adding file objects together
    >>> collection = one + two
    >>>
    >>> # instantiating with a path
    >>> collection = coda.Collection('/path/to/file', metadata={'group': 'dev'})
    >>>
    >>> # once items are in the database, by querying
    >>> coda.add(collection)
    >>> same_collection = coda.find({'group': 'dev'})


Metadata for a collection will only show the metadata shared by all items in a collection. So,
using the example above, the ``metadata`` property on the object would look like:

.. code-block:: python

    >>> print collection.metadata
    {'group': 'dev'}
    >>>
    >>> # but, you can still access metadata about each of
    >>> # the files individually
    >>> print collection.files[0].metadata
    {'group': 'A001'}


Similarly to :class:`coda.File` objects, you can get and set metadata properties for the entire
cohort of files directly on the class. Using the ``collection`` variable above:

.. code-block:: python

    >>> collection.group = 'test'
    >>> print collection.metadata
    {'group': 'test'}


For files in the collection that already have entries in the database, metadata will automatically
be populated with the content from the database. So, using the same example:

.. code-block:: python

    >>> print collection[0].metadata
    {'group': 'test', 'sample': 'A001'}
    >>> coda.add(collection)
    >>>
    >>> cl2 = coda.Collection('/path/to/file')
    >>> print cl2
    /path/to/file/one.txt
    /path/to/file/two.txt
    >>>
    >>> print cl2.metadata
    {'group': 'test'}
    >>>

Using the same example, you can query for a :class:`coda.Collection` object matching specific metadata
criteria, by using the :func:`coda.find` query method:

.. code-block:: python

    >>> cl = coda.find({'group': 'test'})
    >>> print cl
    /path/to/file/one.txt
    /path/to/file/two.txt


As an addendum to the functionality provided by MongoDB for querying, you can also filter collections
returned by queryies using arbitrary functions:

.. code-block:: python

    >>> cl = coda.find({'group': 'test'})
    >>> print cl.filter(lambda x: x.sample == 'A001')
    /path/to/file/one.txt



Tracking Files
--------------

To add files to the ``coda`` database for tracking, the :func:`coda.add` method is used. The :func:`coda.add`
takes a :class:`coda.File` with metadata or a :class:`coda.Collection` object, and stores information about that
file (i.e. the path and associated metadata) in the database:

.. code-block:: python

    >>> # instantiate file objects with metadata
    >>> one = coda.File('/path/to/file/one.txt', metadata={
    >>>     'group': 'dev',
    >>>     'sample': 'A001'
    >>> })
    >>> two = coda.File('/path/to/file/two.txt', metadata={
    >>>     'group': 'dev',
    >>>     'sample': 'A002'
    >>> })
    >>> collection = Collection([one, two])
    >>>
    >>> # add a single file for tracking
    >>> coda.add(one)
    >>>
    >>> # hold up, we want the whole collection added
    >>> coda.add(collection)
    >>> 
    >>> # ... later in time ...
    >>> 
    >>> # query all files in the 'dev' group
    >>> cl = coda.find({'group': 'dev'})
    >>> print cl == collection
    True
    >>>
    >>> # add a new tag for the 'two' file and add it to the database
    >>> two.type = 'datatype'
    >>> coda.add(two)


Untracking Files
----------------

To untrack files and delete them from the ``coda`` database, the :func:`coda.delete` method is used. The
:func:`coda.delete` takes a :class:`coda.File` with metadata or a :class:`coda.Collection` object, and
deletes all instances of associated files in the database.

.. code-block:: python



Updating Metadata
-----------------



Querying
--------

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



Notes on Performance
--------------------

.. Talk about not polluting metadata with heavy data ... heavy data should be stored
.. in files and referenced in metadata. Set-based operations for gathering metadata on
.. Collections assumes that the metadata is relatively minimal (no extremely deep data structures).







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
deletes all instances of associated files in the database. For example:

.. code-block:: python

    >>> # query for a file object
    >>> fi = coda.find_one({'group': 'dev', 'old': True})
    >>> coda.delete(fi)
    >>>
    >>> # delete a tracked file from the filesystem
    >>> fi = coda.File('/path/to/file/one.txt')
    >>>
    >>> # Delete the file -- if it is already in the database,
    >>> # it will be removed. Otherwise, nothing happens. It's also
    >>> # worth nothing that this method does not delete the actual file.
    >>> coda.delete(fi)
    >>>
    >>> # delete the 'dev' collection from before
    >>> cl = coda.find({'group': 'dev'})
    >>> coda.delete(cl)


Updating Metadata
-----------------

To update metadata about a :class:`coda.File` or :class:`coda.Collection`, simply re-add the file
(using :func:`coda.add`) with the updated meatadata. For example:

.. code-block:: python

    >>> # query a file object
    >>> fi = coda.find_one({'group': 'dev', 'special': True})
    >>> print fi
    /path/to/file/three.txt
    >>> 
    >>> # add new metadata on that object and update the database
    >>> fi.special = False
    >>> fi.key = 'value'
    >>> coda.add(fi)
    >>>
    >>> # show the new metadata -- as shown before, you can just
    >>> # instantiate a file object directly, and the metadata will
    >>> # flow implicitly from the database
    >>> fi = coda.File('/path/to/file/three.txt')
    >>> print fi.metadta
    {'group': 'dev', 'special': True, 'special': False, 'key': 'value'}
    >>>
    >>> # you can similarly update a collection -- for the examples
    >>> # below, all files have already been added to the database
    >>> cl = coda.Collection('/path/to/file')
    >>> print cl.metadata
    {'group': 'dev'}
    >>> cl.key = 'newvalue'
    >>> coda.add(cl)


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
    /path/to/dev/file/one.txt
    /path/to/dev/file/two.txt


Since you can filter collection objects by arbitrary functions, doing more advanced queryies
about file contents is easy:

.. code-block:: python

    >>> # define more advanced filtering function --
    >>> # this example just makes sure the number of lines is
    >>> # greater than 50
    >>> def my_filter(name):
    >>>     with open(name, 'r') as fi:
    >>>         length = len(fi.readlines())
    >>>     return length > 50 
    >>> 
    >>> # query and filter the collection
    >>> cl = coda.find({'group': 'dev'}).filter(my_filter)
    >>> print cl
    /path/to/dev/file/two.txt


Querying for single files is similarly as easy:

.. code-block:: python

    >>> fi = coda.find_one({'group': 'dev'})
    >>> print fi
    /path/to/dev/file/one.txt


As alluded to above, ``coda`` also provides functionality for implicitly doing the querying. If
you already have a file object that you want to know metadata about, instead of using :func:`coda.find_one`
with the ``path`` parameter, you can just instantiate a :class:`coda.File` object and query the
metadata directly. The information is pulled implicitly from the database. For example:

.. code-block:: python

    >>> fi = coda.File('/path/to/dev/file/one.txt')
    >>> print fi.metadata
    {'group': 'dev', 'sample': 'A001'}


You can also use this method of querying for collections:

.. code-block:: python

    >>> cl = coda.Collection('/path/to/dev/files')
    >>> print cl.metadata
    {'group': 'dev'}


Finally, since ``coda`` is using MongoDB for storing the metadata, when performing queries with
:func:`coda.find` and :func:`coda.find_one`, you can use
`MongoDB query parameters <https://docs.mongodb.com/v3.0/reference/operator/query/>`_
to do more advanced querying on data:

.. code-block:: python

    >>> cl = coda.find({'$or': [{'group': 'dev'}, {'group': 'test'}]})



Command-Line Use
----------------

High-level components of the functionality described above is also accessible
via the ``coda`` command-line entry point. Using the entry point, you can
add, delete, and tag files or collections of files. Below are examples of
the API:

.. code-block:: bash

    ~$ # add a file for tracking to the database
    ~$ coda add /path/to/file.txt
    ~$
    ~$ # add a collection of files for tracking
    ~$ coda add /path/to/directory/


To tag a file or collection with specific metadata, use the ``tag`` subcommand:

.. code-block:: bash

    ~$ # format: coda tag <file> <key> <value>
    ~$ coda tag /path/to/file.txt extension txt


To list all of the tracked files in the current directory, use the ``list`` subcommand:

.. code-block:: bash

    ~$ # format: coda list [<path>]
    ~$ coda list
    /path/to/file.txt


To remove a file from tracking, use the ``delete`` subcommand:

.. code-block:: bash

    ~$ coda delete /path/to/file.txt


To show all metadata about a file, use the ``show`` subcommand:

.. code-block:: bash

    ~$ coda show /path/to/file.txt
    /path/to/file.txt
    {
        "extension": "txt"
    }


To find files matching metadata search criteria, use the ``find`` command:

.. code-block:: bash
    
    ~$ # format: coda find <key> <value>
    ~$ coda find extension txt
    /path/to/file.txt


For more information, check out the command-line help information:

.. code-block:: bash

    ~$ coda -h



.. Notes on Performance
.. --------------------

.. Some datasets have lots of features that are hard to nav``coda`` is not meant to

.. .. Talk about not polluting metadata with heavy data ... heavy data should be stored
.. .. in files and referenced in metadata. Set-based operations for gathering metadata on
.. .. Collections assumes that the metadata is relatively minimal (no extremely deep data structures).







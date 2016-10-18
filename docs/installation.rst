Installation
============


Through pip
-----------

To install the latest stable release via pip, run::

    $ pip install coda


Via GitHub
----------

To install the bleeding-edge version of the project::

    $ git clone http://github.com/bprinty/coda.git
    $ cd coda
    $ python setup.py install


Setting up MongoDB
------------------

This application uses a `MongoDB <https://docs.mongodb.com/>`_ backend to store all the file annotation information. In order to use this module, you must have MongoDB installed and running on a port that is tied to the current session (a detailed description of the session can be found in the `API <./api.html>`_ section). To install MongoDB, visit `their website <https://docs.mongodb.com/manual/installation>`_, and follow the instructions.

After installing MongoDB, start the daemon using:

.. code-block:: bash

    $ mongod

If this fails to start, it's usually because the data directory used by mongo currently does not exist. Typically, this can be fixed by the following:

.. code-block:: bash

    $ sudo mkdir -p /data/db
    $ sudo chown $USER:$USER -R /data/db

If it still fails to start, you're on your own (a.k.a. hit up stack overflow) ...


Questions/Feedback
------------------

For questions/feedback about any of this, file an issue in the `Github Issue Tracker <http://github.com/bprinty/coda/issues>`_ for this project.
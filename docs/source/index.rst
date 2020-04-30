.. Couchbase Python Client Library documentation master file, created by
   sphinx-quickstart on Fri Apr  5 17:46:04 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Couchbase Python Client Library Documentation
=============================================

Prerequisites
=============
- Couchbase Server (http://couchbase.com/download)
- Python development files
- A C compiler (except on Windows)

Contents:

.. toctree::
   :maxdepth: 2

   api/couchbase
   api/subdoc
   api/datastructures
   api/views
   api/analytics
   api/n1ql
   api/search
   api/results
   api/exceptions
   api/transcoder
   api/threads
   api/convertfuncs
   api/items
   api/logging

Asynchronous APIs
=================

.. toctree::
   :maxdepth: 2

   api/txcouchbase
   api/acouchbase

Internal APIs
=============

These are internal APIs whose interfaces are subject to change. They may
nevertheless be helpful for debugging or extending existing functionality.

.. toctree::
   :maxdepth: 2

   api/async


Management APIs
===================

These APIs allow simple manipulation of buckets themselves. They require
administrative privileges. Currently these APIs are only available for
the synchronous `couchbase` interface.

.. toctree::
   :maxdepth: 2

   api/management


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

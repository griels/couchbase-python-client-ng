=================
Bucket object
=================

.. module:: couchbase.bucket
.. class:: Bucket

    .. automethod:: __init__


.. _argtypes:

    .. automethod:: scope
    .. automethod:: default_collection



=================
Scope object
=================

.. module:: couchbase.collection
.. class:: Scope

    .. automethod:: __init__

Used internally by the SDK.
This constructor is not intended for external use.


    .. automethod:: default_collection
    .. automethod:: open_collection


=================
Collection object
=================

.. module:: couchbase.collection
.. class:: Collection

    .. automethod:: __init__


Used internally by the SDK.
This constructor is not intended for external use.


Passing Arguments
=================

.. currentmodule:: couchbase.collection

All keyword arguments passed to methods should be specified as keyword
arguments, and the user should not rely on their position within the keyword
specification - as this is subject to change.

Thus, if a function is prototyped as::

    def foo(self, key, foo=None, bar=1, baz=False)

then arguments passed to ``foo()`` should *always* be in the form of ::

    obj.foo(key, foo=fooval, bar=barval, baz=bazval)

and never like ::

    obj.foo(key, fooval, barval, bazval)



Key and Value Format
====================

.. currentmodule:: couchbase

By default, keys are encoded as UTF-8, while values are encoded as JSON;
which was selected to be the default for compatibility and ease-of-use
with views.


Format Options
--------------

The following constants may be used as values to the `format` option
in methods where this is supported. This is also the value returned in the
:attr:`~couchbase_core.result.ValueResult.flags` attribute of the
:class:`~couchbase_core.result.ValueResult` object from a
:meth:`~couchbase.collection.Collection.get` operation.

Each format specifier has specific rules about what data types it accepts.

.. data:: FMT_JSON

    Indicates the value is to be converted to JSON. This accepts any plain
    Python object and internally calls :meth:`json.dumps(value)`. See
    the Python `json` documentation for more information.
    It is recommended you use this format if you intend to examine the value
    in a MapReduce view function

.. data:: FMT_PICKLE

    Convert the value to Pickle. This is the most flexible format as it accepts
    just about any Python object. This should not be used if operating in
    environments where other Couchbase clients in other languages might be
    operating (as Pickle is a Python-specific format)

.. data:: FMT_BYTES

    Pass the value as a byte string. No conversion is performed, but the value
    must already be of a `bytes` type. In Python 2.x `bytes` is a synonym
    for `str`. In Python 3.x, `bytes` and `str` are distinct types. Use this
    option to store "binary" data.
    An exception will be thrown if a `unicode` object is passed, as `unicode`
    objects do not have any specific encoding. You must first encode the object
    to your preferred encoding and pass it along as the value.

    Note that values with `FMT_BYTES` are retrieved as `byte` objects.

    `FMT_BYTES` is the quickest conversion method.

.. data:: FMT_UTF8

    Pass the value as a UTF-8 encoded string. This accepts `unicode` objects.
    It may also accept `str` objects if their content is encodable as UTF-8
    (otherwise a :exc:`~couchbase.exceptions.ValueFormatError` is
    thrown).

    Values with `FMT_UTF8` are retrieved as `unicode` objects (for Python 3
    `unicode` objects are plain `str` objects).

.. data:: FMT_AUTO

    Automatically determine the format of the input type. The value of this
    constant is an opaque object.

    The rules are as follows:

    If the value is a ``str``, :const:`FMT_UTF8` is used. If it is a ``bytes``
    object then :const:`FMT_BYTES` is used. If it is a ``list``, ``tuple``
    or ``dict``, ``bool``, or ``None`` then :const:`FMT_JSON` is used.
    For anything else :const:`FMT_PICKLE` is used.


Key Format
----------

The above format options are only valid for *values* being passed to one
of the storage methods (see :meth:`couchbase.collection.Collection.upsert`).

For *keys*, the acceptable inputs are those for :const:`FMT_UTF8`

Single-Key Data Methods
=======================

These methods all return a :class:`~couchbase_core.result.Result` object containing
information about the operation (such as status and value).

.. currentmodule:: couchbase.collection


Storing Data
------------

.. currentmodule:: couchbase.collection
.. class:: Collection

    These methods set the contents of a key in Couchbase. If successful,
    they replace the existing contents (if any) of the key.

    .. automethod:: upsert

    .. automethod:: insert

    .. automethod:: replace


Retrieving Data
---------------

.. currentmodule:: couchbase.collection
.. class:: Collection

    .. automethod:: get

Modifying Data
--------------

These methods modify existing values in Couchbase

.. currentmodule:: couchbase.collection
.. class:: Collection


    .. automethod:: append

    .. automethod:: prepend

Entry Operations
----------------

These methods affect an entry in Couchbase. They do not
directly modify the value, but may affect the entry's accessibility
or duration.


.. currentmodule:: couchbase.collection
.. class:: Collection

    .. automethod:: remove

    .. automethod:: lock

    .. automethod:: unlock

    .. automethod:: touch


Sub-Document Operations
-----------------------

These methods provide entry points to modify *parts* of a document in
Couchbase.

.. note::

    Sub-Document API methods are available in Couchbase Server 4.5
    (currently in Developer Preview).

    The server and SDK implementations and APIs are subject to change


.. currentmodule:: couchbase.collection
.. class:: Collection

    .. automethod:: lookup_in
    .. automethod:: mutate_in

Counter Operations
------------------

These are atomic counter operations for Couchbase. They increment
or decrement a counter. A counter is a key whose value can be parsed
as an integer. Counter values may be retrieved (without modification)
using the :meth:`couchbase.collection.Collection.get` method

.. currentmodule:: couchbase.options
.. class:: SignedInt64

    .. automethod:: __init__


.. currentmodule:: couchbase.collection
.. class:: DeltaValue

    .. automethod:: __init__

.. class:: Collection

    .. automethod:: increment
    .. automethod:: decrement


MapReduce/View Methods
======================

.. currentmodule:: couchbase.cluster
.. class:: Cluster

    .. automethod:: query

N1QL Query Methods
==================

.. currentmodule:: couchbase.cluster
.. class:: Cluster

    .. automethod:: query


Full-Text Search Methods
========================

.. currentmodule:: couchbase.cluster
.. class:: Cluster

    .. automethod:: search_query

Using Custom Ports
-------------------

If you require to connect to an alternate port for bootstrapping the client
(either because your administrator has configured the cluster to listen on
alternate ports, or because you are using the built-in ``cluster_run``
script provided with the server source code), you may do so in the host list
itself.

Simply provide the host in the format of ``host:port``.

Note that the port is dependent on the *scheme* used. In this case, the scheme
dictates what specific service the port points to.


=============== ========
Scheme          Protocol
=============== ========
``couchbase``   memcached port (default is ``11210``)
``couchbases``  SSL-encrypted memcached port (default is ``11207``)
``http``        REST API/Administrative port (default is ``8091``)
=============== ========


Options in Connection String
----------------------------

Additional client options may be specified within the connection
string itself. These options are derived from the underlying
*libcouchbase* library and thus will accept any input accepted
by the library itself. The following are some influential options:


- ``config_total_timeout``. Number of seconds to wait for the client
  bootstrap to complete.

- ``config_node_timeout``. Maximum number of time to wait (in seconds)
  to attempt to bootstrap from the current node. If the bootstrap times
  out (and the ``config_total_timeout`` setting is not reached), the
  bootstrap is then attempted from the next node (or an exception is
  raised if no more nodes remain).

- ``config_cache``. If set, this will refer to a file on the
  filesystem where cached "bootstrap" information may be stored. This
  path may be shared among multiple instance of the Couchbase client.
  Using this option may reduce overhead when using many short-lived
  instances of the client.

  If the file does not exist, it will be created.

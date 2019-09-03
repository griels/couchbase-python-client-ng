#
# Copyright 2013, Couchbase, Inc.
# All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import couchbase_core._bootstrap
import couchbase_core._libcouchbase as _LCB
from couchbase_core._libcouchbase import Collection as _Base

import couchbase_v2
from couchbase_core.client import Client as CoreClient, _depr
from couchbase_core import _depr
from couchbase_core.result import *
from couchbase_core.bucketmanager import BucketManager

import json
from typing import *


class Pipeline(object):
    def __init__(self, parent):
        """
        .. versionadded:: 1.2.0

        Creates a new pipeline context. See :meth:`~Bucket.pipeline`
        for more details
        """
        self._parent = parent
        self._results = None

    def __enter__(self):
        self._parent._pipeline_begin()

    def __exit__(self, *args):
        self._results = self._parent._pipeline_end()
        return False

    @property
    def results(self):
        """
        Contains a list of results for each pipelined operation
        executed within the context. The list remains until this
        context is reused.

        The elements in the list are either :class:`.Result`
        objects (for single operations) or :class:`.MultiResult`
        objects (for multi operations)
        """
        return self._results


class DurabilityContext(object):
    def __init__(self, parent, persist_to=-1, replicate_to=-1, timeout=0.0):
        self._parent = parent
        self._new = {
            '_dur_persist_to': persist_to,
            '_dur_replicate_to': replicate_to,
            '_dur_timeout': int(timeout * 1000000)
        }
        self._old = {}

    def __enter__(self):
        for k, v in self._new.items():
            self._old[k] = getattr(self._parent, k)
            setattr(self._parent, k, v)

    def __exit__(self, *args):
        for k, v in self._old.items():
            setattr(self._parent, k, v)
        return False


class Bucket(CoreClient):
    _MEMCACHED_OPERATIONS = CoreClient._MEMCACHED_OPERATIONS+('endure',
                                                   'observe', 'rget', 'set', 'add', 'delete')

    def pipeline(self):
        """
        Returns a new :class:`Pipeline` context manager. When the
        context manager is active, operations performed will return
        ``None``, and will be sent on the network when the context
        leaves (in its ``__exit__`` method). To get the results of the
        pipelined operations, inspect the :attr:`Pipeline.results`
        property.

        Operational errors (i.e. negative replies from the server, or
        network errors) are delivered when the pipeline exits, but
        argument errors are thrown immediately.

        :return: a :class:`Pipeline` object
        :raise: :exc:`.PipelineError` if a pipeline is already created
        :raise: Other operation-specific errors.

        Scheduling multiple operations, without checking results::

          with cb.pipeline():
            cb.upsert("key1", "value1")
            cb.counter("counter")
            cb.upsert_multi({
              "new_key1" : "new_value_1",
              "new_key2" : "new_value_2"
            })

        Retrieve the results for several operations::

          pipeline = cb.pipeline()
          with pipeline:
            cb.upsert("foo", "bar")
            cb.replace("something", "value")

          for result in pipeline.results:
            print("Pipeline result: CAS {0}".format(result.cas))

        .. note::

          When in pipeline mode, you cannot execute view queries.
          Additionally, pipeline mode is not supported on async handles

        .. warning::

          Pipeline mode should not be used if you are using the same
          object concurrently from multiple threads. This only refers
          to the internal lock within the object itself. It is safe
          to use if you employ your own locking mechanism (for example
          a connection pool)

        .. versionadded:: 1.2.0

        """
        return Pipeline(self)

    # We have these wrappers so that IDEs can do param tooltips and the
    # like. we might move this directly into C some day

    def upsert(self, key, value, *args, **kwargs):
        return _Base.upsert(self, key, value, *args, **kwargs)

    def insert(self, key, value, *args, **kwargs):
        return _Base.insert(self, key, value, *args, **kwargs)

    def replace(self, key, value, *args, **kwargs):
        return _Base.replace(self, key, value, *args, **kwargs)

    def append(self, key, value, *args, **kwargs):
        return _Base.append(self, key, value, *args, **kwargs)

    def prepend(self, key, value, *args, **kwargs):
        return _Base.prepend(self, key, value, *args, **kwargs)

    def lookup_in(self, key, *specs, **kwargs):
        """Atomically retrieve one or more paths from a document.

        :param key: The key of the document to lookup
        :param spec: A list of specs (see :mod:`.couchbase_core.subdocument`)
        :return: A :class:`.couchbase_core.result.SubdocResult` object.
            This object contains the results and any errors of the
            operation.

        Example::

            import couchbase_core.subdocument as SD
            rv = cb.lookup_in('user',
                              SD.get('email'),
                              SD.get('name'),
                              SD.exists('friends.therock'))

            email = rv[0]
            name = rv[1]
            friend_exists = rv.exists(2)

        .. seealso:: :meth:`retrieve_in` which acts as a convenience wrapper
        """
        return super(Bucket, self).lookup_in(key,specs,**kwargs)

    def mutate_in(self, key, *specs, **kwargs):
        """Perform multiple atomic modifications within a document.

        :param key: The key of the document to modify
        :param specs: A list of specs (See :mod:`.couchbase_core.subdocument`)
        :param bool create_doc:
            Whether the document should be create if it doesn't exist
        :param bool insert_doc: If the document should be created anew, and the
            operations performed *only* if it does not exist.
        :param bool upsert_doc: If the document should be created anew if it
            does not exist. If it does exist the commands are still executed.
        :param kwargs: CAS, etc.
        :return: A :class:`~.couchbase_core.result.SubdocResult` object.

        Here's an example of adding a new tag to a "user" document
        and incrementing a modification counter::

            import couchbase_core.subdocument as SD
            # ....
            cb.mutate_in('user',
                         SD.array_addunique('tags', 'dog'),
                         SD.counter('updates', 1))

        .. note::

            The `insert_doc` and `upsert_doc` options are mutually exclusive.
            Use `insert_doc` when you wish to create a new document with
            extended attributes (xattrs).

        .. seealso:: :mod:`.couchbase_core.subdocument`
        """
        return super(Bucket, self).mutate_in(key, specs, **kwargs)

    def durability(self, persist_to=-1, replicate_to=-1, timeout=0.0):
        """Returns a context manager which will apply the given
        persistence/replication settings to all mutation operations when
        active

        :param int persist_to:
        :param int replicate_to:

        See :meth:`endure` for the meaning of these two values

        Thus, something like::

          with cb.durability(persist_to=3):
            cb.upsert("foo", "foo_value")
            cb.upsert("bar", "bar_value")
            cb.upsert("baz", "baz_value")

        is equivalent to::

            cb.upsert("foo", "foo_value", persist_to=3)
            cb.upsert("bar", "bar_value", persist_to=3)
            cb.upsert("baz", "baz_value", persist_to=3)


        .. versionadded:: 1.2.0

        .. seealso:: :meth:`endure`
        """
        return DurabilityContext(self, persist_to, replicate_to, timeout)

    def bucket_manager(self):
        """
        Returns a :class:`~.BucketManager` object which may be used to
        perform management operations on the current bucket. These
        operations may create/modify design documents and flush the
        bucket
        """
        return BucketManager(self)

    n1ql_query = CoreClient.query
    query = CoreClient.view_query

    def _analytics_query(self, query, _, *args, **kwargs):
        # we used to take the CBAS host as the second parameter, but
        # LCB now retrieves the hostname from the cluster
        return super(Bucket,self).analytics_query(query, *args, **kwargs)

    analytics_query = _analytics_query

    # "items" interface

    _OLDOPS = { 'set': 'upsert', 'add': 'insert', 'delete': 'remove'}
    for o, n in _OLDOPS.items():
        for variant in ('', '_multi'):
            oldname = o + variant
            newname = n + variant

            try:
                dst = locals()[n + variant]
            except KeyError:
                dst = getattr(_Base, n + variant)

            def mkmeth(oldname, newname, _dst):
                def _tmpmeth(self, *args, **kwargs):
                    _depr(oldname, newname)
                    return _dst(self, *args, **kwargs)
                return _tmpmeth

            locals().update({oldname: mkmeth(oldname, newname, dst)})

    """
    Lists the names of all the memcached operations. This is useful
    for classes which want to wrap all the methods
    """

    def design_get(self, *args, **kwargs):
        _depr('design_get', 'bucket_manager().design_get')
        return self.bucket_manager().design_get(*args, **kwargs)

    def design_create(self, *args, **kwargs):
        _depr('design_create', 'bucket_manager().design_create')
        return self.bucket_manager().design_create(*args, **kwargs)

    def design_publish(self, *args, **kwargs):
        _depr('design_publish', 'bucket_manager().design_publish')
        return self.bucket_manager().design_publish(*args, **kwargs)

    def design_delete(self, *args, **kwargs):
        _depr('design_delete', 'bucket_manager().design_delete')
        return self.bucket_manager().design_delete(*args, **kwargs)

    def add_bucket_creds(self, bucket, password):
        if not bucket or not password:
            raise ValueError('Bucket and password must be nonempty')
        return _Base._add_creds(self, bucket, password)

    def get_attribute(self, key, attrname):
        pass

    def set_attribute(self, key, attrname):
        pass

    if _LCB.PYCBC_CRYPTO_VERSION<1:
        pass
    else:
        pass

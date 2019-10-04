from couchbase import OptionBlock
from typing import *
from couchbase.management.generic import GenericManager


class QueryIndexManager(GenericManager):
    def __init__(self, parent_cluster):
        """
        Query Index Manager
        The Query Index Manager interface contains the means for managing indexes used for queries.
        :param parent_cluster:
        """
        super(QueryIndexManager,self).__init__(parent_cluster)

    def get_all_indexes(self,  # type: QueryIndexManager
                        bucket_name,  # type: str
                        options  # type: GetAllQueryIndexOptions
                        ):
        # type: (...)-> Iterable[IQueryIndex]
        """
        GetAllIndexes
        Fetches all indexes from the server.
        Signature
        Iterable<IQueryIndex> GetAllIndexes(string bucket_name, [options])
        Parameters
        Required:
        bucket_name: string - the name of the bucket.
        Optional:
        Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.
        N1QL
        SELECT idx.* FROM system:indexes AS idx
        WHERE keyspace_id = "bucket_name"
        ORDER BY is_primary DESC, name ASC
        Returns
        An array of IQueryIndex.
        Throws
        InvalidArgumentsException
        Any exceptions raised by the underlying platform
        """

    def create_index(self,  # type: QueryIndexManager
                     bucket_name,  # type: str
                     index_name,  # type: str
                     fields,  # type: str
                     options  # type: CreateQueryIndexOptions
                     ):
        """
        CreateIndex
        Creates a new index.
        Signature
        void CreateIndex(string bucket_name, string index_name, []string fields,  [options])
        Parameters
        Required:
        bucket_name: string - the name of the bucket.
        index_name: string - the name of the index.
        fields: []string - the fields to create the index over.
        Optional:
        IgnoreIfExists (bool) - Don't error/throw if the index already exists.
        NumReplicas (int) - The number of replicas that this index should have. Uses the WITH keyword and num_replica.
        CREATE INDEX index_name ON bucket_name WITH { "num_replica": 2 }
        https://docs.couchbase.com/server/current/n1ql/n1ql-language-reference/createindex.html
        Deferred (bool) - Whether the index should be created as a deferred index.
        Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.
        Returns
        Throws
        IndexAlreadyExistsException
        InvalidArgumentsException
        Any exceptions raised by the underlying platform"""

    def create_primary_index(self,  # type: QueryIndexManager
                             bucket_name,  # type: str
                             options  # type: CreatePrimaryQueryIndexOptions
                             ):
        """
        CreatePrimaryIndex
        Creates a new primary index.
        Signature
        void CreatePrimaryIndex(string bucket_name, [options])
        Parameters
        Required:
        bucket_name: string - name of the bucket.
        Optional:
        index_name: string - name of the index.
        IgnoreIfExists (bool) - Don't error/throw if the index already exists.
        NumReplicas (int) - The number of replicas that this index should have. Uses the WITH keyword and num_replica.
        CREATE INDEX index_name ON bucket_name WITH { "num_replica": 2 }
        https://docs.couchbase.com/server/current/n1ql/n1ql-language-reference/createindex.html
        Deferred (bool) - Whether the index should be created as a deferred index.
        Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.
        Returns
        Throws
        QueryIndexAlreadyExistsException
        InvalidArgumentsException
        Any exceptions raised by the underlying platform
        """

    def drop_index(self,  # type: QueryIndexManager
                   bucket_name,  # type: str
                   index_name,  # type: str
                   options  # type: DropQueryIndexOptions
                   ):
        """
        DropIndex
        Drops an index.
        Signature
        void DropIndex(string bucket_name, string index_name, [options])
        Parameters
        Required:
        bucket_name: string - name of the bucket.
        index_name: string - name of the index.
        Optional:
        IgnoreIfNotExists (bool) - Don't error/throw if the index does not exist.
        Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.
        Returns
        Throws
        QueryIndexNotFoundException
        InvalidArgumentsException
        Any exceptions raised by the underlying platform"""

    def drop_primary_index(self,  # type: QueryIndexManager
                           bucket_name,  # type: str
                           options  # type: DropPrimaryQueryIndexOptions
                           ):
        """
        DropPrimaryIndex
        Drops a primary index.
        Signature
        void DropPrimaryIndex(string bucket_name, [options])
        Parameters
        Required:
        bucket_name: string - name of the bucket.
        Optional:
        index_name: string - name of the index.
        IgnoreIfNotExists (bool) - Don't error/throw if the index does not exist.
        Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.
        Returns
        Throws
        QueryIndexNotFoundException
        InvalidArgumentsException
        Any exceptions raised by the underlying platform
        """

    def watch_indexes(self,  # type: QueryIndexManager
                      bucket_name,  # type: str
                      index_names,  # type: str
                      duration,  # type: Duration
                      options  # type: WatchQueryIndexOptions
                      ):
        """WatchIndexes
        Watch polls indexes until they are online.
        Signature
        void WatchIndexes(string bucket_name, []string index_names, timeout duration, [options])
        Parameters
        Required:
        bucket_name: string - name of the bucket.
        index_name: []string - name(s) of the index(es).
        Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.
        Optional:
        WatchPrimary (bool) - whether or not to watch the primary index.
        Returns
        Throws
        QueryIndexNotFoundException
        InvalidArgumentsException
        Any exceptions raised by the underlying platform
        """

    def build_deferred_indexes(self,  # type: QueryIndexManager
                               bucket_name,  # type: str
                               options  # type: BuildQueryIndexOptions
                               ):
        """BuildDeferredIndexes
        Build Deferred builds all indexes which are currently in deferred state.
        Signature
        void BuildDeferredIndexes(string bucket_name, [options])
        Parameters
        Required:
        bucket_name: string - name of the bucket.
        Optional:
        Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.
        Returns
        Throws
        Any exceptions raised by the underlying platform
        InvalidArgumentsException

        """



class IQueryIndex(object):
    def __init__(self):
        """The IQueryIndex interface provides a means of mapping a query index into an object."""

    @property
    def name(self):
        # type: (...)->str
        pass

    @property
    def IsPrimary(self):
        # type: (...)->bool
        pass

    @property
    def type(self):
        # type: (...)->IndexType
        pass

    @property
    def state(self):
        # type: (...)->str
        pass

    @property
    def keyspace(self):
        # type: (...)->str
        pass

    @property
    def IndexKey(self):
        # type: (...)->Iterable[str]
        pass

    @property
    def condition(self):
        # type: (...)->str
        pass


class IndexType(object):
    pass


class GetAllQueryIndexOptions(OptionBlock):
    pass


class CreateQueryIndexOptions(OptionBlock):
    pass


class CreatePrimaryQueryIndexOptions(OptionBlock):
    pass


class DropQueryIndexOptions(OptionBlock):
    pass


class DropPrimaryQueryIndexOptions(OptionBlock):
    pass


class WatchQueryIndexOptions(OptionBlock):
    pass


class BuildQueryIndexOptions(OptionBlock):
    pass

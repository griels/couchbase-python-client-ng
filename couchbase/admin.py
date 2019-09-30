from couchbase.options import OptionBlock, Duration
from couchbase_core.admin import Admin
from typing import *


class InsertCollectionOptions(OptionBlock):
    pass


class InsertScopeOptions(OptionBlock):
    pass


class CollectionManager(object):
    def __init__(self,
                 admin_bucket,  # type: Admin
                 bucket_name  # type: str
                 ):
        self.admin_bucket = admin_bucket
        self.bucket_name = bucket_name

    def insert_collection(self,
                          collection_name,  # type: str
                          scope_name,  # type: str
                          *options  # type: InsertCollectionOptions
                          ):
        """
        Upsert a collection into the parent bucket

        :param collection_name: Collection name
        :param scope_name: Scope name
        :param options:
        :return:
        """

        path = "pools/default/buckets/default/collections/{}".format(scope_name)

        params = {
            'name': collection_name
        }

        form = self.admin_bucket._mk_formstr(params)
        return self.admin_bucket.http_request(path=path,
                                 method='POST',
                                 content_type='application/x-www-form-urlencoded',
                                 content=form)

    def insert_scope(self,
                     scope_name,  # type: str
                     *options  # type: InsertScopeOptions
                     ):
        """
        Upsert a collection into the parent bucket

        :param scope_name: Scope name
        :param options:
        :return:
        """

        path = "pools/default/buckets/default/collections"

        params = {
            'name': scope_name
        }

        form = self.admin_bucket._mk_formstr(params)
        return self.admin_bucket.http_request(path=path,
                                 method='POST',
                                 content_type='application/x-www-form-urlencoded',
                                 content=form)


class ViewIndexManager(object):
    def get_design_document(self,  # type: ViewIndexManager
                            design_doc_name,  # type: str
                            namespace,  # type: DesignDocumentNamespace
                            **options):
        # type: (...)->DesignDocument
        """Fetches a design document from the server if it exists.
        Parameters
        Required:
        designDocName: string - the name of the design document.
        namespace: enum - PRODUCTION if the user is requesting a document from the production namespace, or DEVELOPMENT if from the development namespace.
        Optional:
        Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.
        Returns
        An instance of DesignDocument.
        Throws
        DesignDocumentNotFoundException (http 404)
        Any exceptions raised by the underlying platform
        Uri
        GET http://localhost:8092/<bucketname>/_design/<ddocname>
        Example response from server
        {
            "views":{
                "test":{
                    "map":"function (doc, meta) {\n\t\t\t\t\t\t  emit(meta.id, null);\n\t\t\t\t\t\t}",
                    "reduce":"_count"
                }
            }
        }
        """

    def get_all_design_documents(self,  # type: ViewIndexManager
                                 namespace,  # type: DesignDocumentNamespace
                                 *options,
                                 **kwargs):
        # type: (...)->Iterable[DesignDocument]
        """
        GetAllDesignDocuments
        Fetches all design documents from the server.
        ]
        When processing the server response, the client must strip the “_design/” prefix from the document ID (as well as the “_dev” prefix if present). For example, a doc.meta.id value of “_design/foo” must be parsed as “foo”, and “_design/dev_bar” must be parsed as “bar”.
        Signature
        Parameters
        Required:
        namespace (enum) - indicates whether the user wants to get production documents (PRODUCTION) or development documents (DEVELOPMENT).
        Optional:
        Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.
        Returns
        An iterable of DesignDocument.
        Throws
        Any exceptions raised by the underlying platform
        Uri
        GET http://localhost:8091/pools/default/buckets/<bucket-name>/ddocs

        Example response from server
        {
        "rows":[
            {
                "doc":{
                    "meta":{
                        "id":"_design/dev_test",
                        "rev":"1-ae5e21ec"
                    },
                    "json":{
                        "views":{
                            "test":{
                                "map":"function (doc, meta) {\n\t\t\t\t\t\t  emit(meta.id, null);\n\t\t\t\t\t\t}",
                                "reduce":"_count"
                            }
                        }
                    }
                },
                "controllers":{
                    "compact":"/pools/default/buckets/default/ddocs/_design%2Fdev_test/controller/compactView",
                    "setUpdateMinChanges":"/pools/default/buckets/default/ddocs/_design%2Fdev_test/controller/setUpdateMinChanges"
                }
            }
        ]
        }
        """

    def upsert_design_document(self,  # type: ViewIndexManager
                               designDocData,  # type: DesignDocument
                               namespace,  # type: DesignDocumentNamespace
                               *options,
                               **kwargs):
        # type: (...)->None
        """
        UpsertDesignDocument
        Updates, or inserts, a design document.
        Signature
        Parameters
        Required:
        designDocData: DesignDocument - the data to use to create the design document
        namespace (enum) - indicates whether the user wants to upsert the document to the production namespace (PRODUCTION) or development namespace (DEVELOPMENT).
        Optional:


        Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.
        Returns
        Throws
        Any exceptions raised by the underlying platform
        Uri
        PUT http://localhost:8092/<bucketname>/_design/<ddocname>
                                               DropDesignDocument
        """

    def drop_design_document(self,  # type: ViewIndexManager
                             designDocName,  # type: str
                             namespace,  # type: DesignDocumentNamespace
                             *options,
                             **kwargs):
        # type: (...)->None
        """
        Removes a design document.
        Parameters
        Required:
        designDocName: string - the name of the design document.
        namespace: enum - indicates whether the name refers to a production document (PRODUCTION) or a development document (DEVELOPMENT).
        Optional:
        Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.
        Returns
        Throws
        DesignDocumentNotFoundException (http 404)
        InvalidArgumentsException
        Any exceptions raised by the underlying platform
        Uri
        DELETE http://localhost:8092/<bucketname>/_design/<ddocname>
                                                  PublishDesignDocument
        Publishes a design document. This method is equivalent to getting a document from the development namespace and upserting it to the production namespace.
            Signature
        void PublishDesignDocument(string designDocName, [options])
        Parameters
        Required:
        designDocName: string - the name of the development design document.
        Optional:
        Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.
        Returns
        Throws
        DesignDocumentNotFoundException (http 404)
        InvalidArgumentsException
        Any exceptions raised by the underlying platform
        """


class IQueryIndex(OptionBlock):
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


class QueryIndexManager(object):
    def __init__(self):
        """
        Query Index Manager
        The Query Index Manager interface contains the means for managing indexes used for queries.
        """

    def get_all_indexes(self,  # type: QueryIndexManager
                        bucketName: str, options: GetAllQueryIndexOptions) -> Iterable[IQueryIndex]:
        """
        GetAllIndexes
        Fetches all indexes from the server.
        Signature
        Iterable<IQueryIndex> GetAllIndexes(string bucketName, [options])
        Parameters
        Required:
        BucketName: string - the name of the bucket.
        Optional:
        Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.
        N1QL
        SELECT idx.* FROM system:indexes AS idx
        WHERE keyspace_id = "bucketName"
        ORDER BY is_primary DESC, name ASC
        Returns
        An array of IQueryIndex.
        Throws
        InvalidArgumentsException
        Any exceptions raised by the underlying platform
        """

    def create_index(self,  # type: QueryIndexManager
                     bucketName: str, indexName: str, fields: str, options: CreateQueryIndexOptions):
        """
        CreateIndex
        Creates a new index.
        Signature
        void CreateIndex(string bucketName, string indexName, []string fields,  [options])
        Parameters
        Required:
        BucketName: string - the name of the bucket.
        IndexName: string - the name of the index.
        fields: []string - the fields to create the index over.
        Optional:
        IgnoreIfExists (bool) - Don’t error/throw if the index already exists.
        NumReplicas (int) - The number of replicas that this index should have. Uses the WITH keyword and num_replica.
        CREATE INDEX indexName ON bucketName WITH { "num_replica": 2 }
        https://docs.couchbase.com/server/current/n1ql/n1ql-language-reference/createindex.html
        Deferred (bool) - Whether the index should be created as a deferred index.
        Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.
        Returns
        Throws
        IndexAlreadyExistsException
        InvalidArgumentsException
        Any exceptions raised by the underlying platform"""

    def create_primary_index(self,  # type: QueryIndexManager
                             bucketName: str, options: CreatePrimaryQueryIndexOptions):
        """
        CreatePrimaryIndex
        Creates a new primary index.
        Signature
        void CreatePrimaryIndex(string bucketName, [options])
        Parameters
        Required:
        BucketName: string - name of the bucket.
        Optional:
        IndexName: string - name of the index.
        IgnoreIfExists (bool) - Don’t error/throw if the index already exists.
        NumReplicas (int) - The number of replicas that this index should have. Uses the WITH keyword and num_replica.
        CREATE INDEX indexName ON bucketName WITH { "num_replica": 2 }
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
                   bucketName: str, indexName: str, options: DropQueryIndexOptions):
        """
        DropIndex
        Drops an index.
        Signature
        void DropIndex(string bucketName, string indexName, [options])
        Parameters
        Required:
        BucketName: string - name of the bucket.
        IndexName: string - name of the index.
        Optional:
        IgnoreIfNotExists (bool) - Don’t error/throw if the index does not exist.
        Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.
        Returns
        Throws
        QueryIndexNotFoundException
        InvalidArgumentsException
        Any exceptions raised by the underlying platform"""

    def drop_primary_index(self,  # type: QueryIndexManager
                           bucketName: str, options: DropPrimaryQueryIndexOptions):
        """
        DropPrimaryIndex
        Drops a primary index.
        Signature
        void DropPrimaryIndex(string bucketName, [options])
        Parameters
        Required:
        BucketName: string - name of the bucket.
        Optional:
        IndexName: string - name of the index.
        IgnoreIfNotExists (bool) - Don’t error/throw if the index does not exist.
        Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.
        Returns
        Throws
        QueryIndexNotFoundException
        InvalidArgumentsException
        Any exceptions raised by the underlying platform
        """

    def watch_indexes(self,  # type: QueryIndexManager
                      bucketName: str, indexNames: str, duration: Duration, options: WatchQueryIndexOptions):
        """WatchIndexes
        Watch polls indexes until they are online.
        Signature
        void WatchIndexes(string bucketName, []string indexNames, timeout duration, [options])
        Parameters
        Required:
        BucketName: string - name of the bucket.
        IndexName: []string - name(s) of the index(es).
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
                               bucketName: str, options: BuildQueryIndexOptions):
        """BuildDeferredIndexes
        Build Deferred builds all indexes which are currently in deferred state.
        Signature
        void BuildDeferredIndexes(string bucketName, [options])
        Parameters
        Required:
        BucketName: string - name of the bucket.
        Optional:
        Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.
        Returns
        Throws
        Any exceptions raised by the underlying platform
        InvalidArgumentsException

        """

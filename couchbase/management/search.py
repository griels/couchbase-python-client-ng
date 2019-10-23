from typing import *
from couchbase.management.generic import GenericManager


class SearchIndexManager(GenericManager):
    def __init__(self, parent_cluster):
        """Search Index Manager
        The Search Index Manager interface contains the means for managing indexes used for search. Search index definitions are purposefully left very dynamic as the index definitions on the server are complex. As such it is left to each SDK to implement its own dynamic type for this, JSONObject is used here to signify that. Stability level is uncommited?
        :param parent_cluster:
        """
        super(SearchIndexManager,self).__init__(parent_cluster)

    def get_index(self,  # type: SearchIndexManager
                  index_name,  # type: str
                  options  # type: GetSearchIndexOptions
                  ):
        # type: (...)-> ISearchIndex
        """GetIndex
        Fetches an index from the server if it exists.
        Signature
        ISearchIndex GetIndex(str index_name, [options])
        Parameters
        Required:
        index_name: string - name of the index.
        Optional:
        Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.
        Returns
        An instance of ISearchIndex.
        Throws
        SearchIndexNotFoundException
        InvalidArgumentsException
        Any exceptions raised by the underlying platform
        Uri
        GET http://localhost:8094/api/index/<name>"""

    def get_all_indexes(self,  # type: SearchIndexManager
                        options  # type: GetAllSearchIndexesOptions
                        ):
        # type: (...)->Iterable[ISearchIndex]
        """
        GetAllIndexes
        Fetches all indexes from the server.
        Signature
        Iterable<ISearchIndex> GetAllIndexes([options])
        Parameters
        Required:
        Optional:
        Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.
        Returns
        An array of ISearchIndex.
        Throws
        Any exceptions raised by the underlying platform
        Uri
        GET http://localhost:8094/api/index"""

    def upsert_index(self,  # type: SearchIndexManager
                     index_definition,  # type: ISearchIndex
                     options  # type: UpsertSearchIndexOptions
                     ):
        pass
        """
        UpsertIndex
        Creates, or updates, an index. .
        Signature
        void UpsertIndex(ISearchIndex indexDefinition, [options])
        Parameters
        Required:
        indexDefinition: SearchIndex - the index definition
        Optional:
        Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.
        Returns
        Throws
        InvalidArgumentsException
        If any of the following are empty:
        Name
        Type
        SourceType
        Any exceptions raised by the underlying platform
        Uri
        PUT http://localhost:8094/api/index/<index_name>
        Should be sent with request header "cache-control" set to "no-cache"."""

    def drop_index(self,  # type: SearchIndexManager
                   index_name,  # type: str
                   options  # type: DropSearchIndexOptions
                   ):
        """
        DropIndex
        Drops an index.
        Signature
        void DropIndexstring index_name, [options])
        Parameters
        Required:
        index_name: string - name of the index.
        Optional:
        Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.
        Returns
        Throws
        SearchIndexNotFoundException
        InvalidArgumentsException
        Any exceptions raised by the underlying platform
        Uri
        DELETE http://localhost:8094/api/index/<index_name>
        """

    def get_indexed_documents_count(self,  # type: SearchIndexManager
                                    index_name,  # type: str
                                    options  # type: GetIndexedSearchIndexOptions
                                    ):
        # type: (...)->int
        """GetIndexedDocumentsCount
        Retrieves the number of documents that have been indexed for an index.
        Signature
        void GetIndexedDocumentsCount(string index_name, [options])
        Parameters
        Required:
        index_name: string - name of the index.
        Optional:
        Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.
        Returns
        Throws
        SearchIndexNotFoundException
        InvalidArgumentsException
        Any exceptions raised by the underlying platform
        Uri
        GET http://localhost:8094/api/index/<index_name>/count
        """

    def pause_ingest(self,  # type: SearchIndexManager
                     index_name  # type: str
                     ):
        """PauseIngest
        Pauses updates and maintenance for an index.
        Signature
        void PauseIngest(string index_name, [options])
        Parameters
        Required:
        index_name: string - name of the index.
        Optional:
        Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.
        Returns
        Throws
        SearchIndexNotFoundException
        InvalidArgumentsException
        Any exceptions raised by the underlying platform
        Uri
        POST /api/index/{index_name}/ingestControl/pause
        """

    def resume_ingest(self,  # type: SearchIndexManager
                      index_name  # type: str
                      ):
        """ResumeIngest
        Resumes updates and maintenance for an index.
        Signature
        void ResumeIngest(string index_name, [options])
        Parameters
        Required:
        index_name: string - name of the index.
        Optional:
        Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.
        Returns
        Throws
        SearchIndexNotFoundException
        InvalidArgumentsException
        Any exceptions raised by the underlying platform
        Uri
        POST /api/index/{index_name}/ingestControl/resume
        """

    def allow_querying(self,  # type: SearchIndexManager
                       index_name  # type: str
                       ):
        """AllowQuerying
        Allows querying against an index.
        Signature
        void AllowQuerying(string index_name, [options])
        Parameters
        Required:
        index_name: string - name of the index.
        Optional:
        Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.
        Returns
        Throws
        SearchIndexNotFoundException
        InvalidArgumentsException
        Any exceptions raised by the underlying platform
        Uri
        POST /api/index/{index_name}/queryControl/allow
        """

    def disallow_querying(self,  # type: SearchIndexManager
                          index_name  # type: str
                          ):
        """DisallowQuerying
        Disallows querying against an index.
        Signature
        void DisallowQuerying(string index_name, [options])
        Parameters
        Required:
        index_name: string - name of the index.
        Optional:
        Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.
        Returns
        Throws
        SearchIndexNotFoundException
        InvalidArgumentsException
        Any exceptions raised by the underlying platform
        Uri
        POST /api/index/{index_name}/queryControl/disallow
        """

    def freeze_plan(self,  # type: SearchIndexManager
                    index_name  # type: str
                    ):
        """FreezePlan
        Freeze the assignment of index partitions to nodes.
        Signature
        void FreezePlan(string index_name, [options])
        Parameters
        Required:
        index_name: string - name of the index.
        Optional:
        Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.
        Returns
        Throws
        SearchIndexNotFoundException
        InvalidArgumentsException
        Any exceptions raised by the underlying platform
        Uri
        POST /api/index/{index_name}/planFreezeControl/freeze"""

    def unfreeze_plan(self,  # type: SearchIndexManager
                      index_name  # type: str
                      ):
        """
        UnfreezePlan
        Unfreeze the assignment of index partitions to nodes.
        Signature
        void UnfreezePlan(string index_name, [options])
        Parameters
        Required:
        index_name: string - name of the index.
        Optional:
        Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.
        Returns
        Throws
        SearchIndexNotFoundException
        InvalidArgumentsException
        Any exceptions raised by the underlying platform
        Uri
        POST /api/index/{index_name}/planFreezeControl/unfreeze"""

    def analyze_document(self,  # type: SearchIndexManager
                         index_name,  # type: str
                         document,  # type: JSONDocument
                         options  # type: AnalyzeDocOptions
                         ):
        # type: (...)->Iterable[JSONDocument]
        """

        AnalyzeDocument
        Allows users to see how a document is analyzed against a specific index.
        Signature
        Iterable<JSONObject> AnalyzeDocument(string index_name, JSONObject document, [options])
        Parameters
        Required:
        index_name: string - name of the index.
        Document: JSONObject - the document to be analyzed.
        Optional:
        Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.
        Returns
        An iterable of JSONObject. The response from the server returns an object containing two top level keys: status and analyzed. The SDK must return the value containing within the analyze key.
        Throws
        SearchIndexNotFoundException
        InvalidArgumentsException
        Any exceptions raised by the underlying platform
        Uri
        POST /api/index/{index_name}/analyzeDoc
        As of build mad hatter 3839
        Analytics Index Manager
        Stability level is not volatile."""


class SearchIndex(object):
    def __init__(self):
        """SearchIndex provides a means to map search indexes into object. The Params, SourceParams, and PlanParams fields are left to the SDK to decide what is idiomatic (e.g. JSONObject), the definitions of these fields is purposefully vague."""

    @property
    def UUID(self):
        # type: (...)->str
        """string `json:"uuid"`"""
        """UUID is required for updates. It provides a means of ensuring consistency, the UUID must match the UUID value
        for the index on the server."""

    @property
    def name(self):
        # type: (...)->str
        """`json:"name"`"""

    @property
    def source_name(self):
        # type: (...)->str
        """source_name is the name of the source of the data for the index e.g. bucket name.
        source_name string `json:"sourceName,omitempty"`"""

    @property
    def type(self):
        # type: (...)->int
        """// Type is the type of index, e.g. fulltext-index or fulltext-alias.
        Type string `json:"type"`"""

    @property
    def params(self):
        # type: (...)->Mapping[str,object]
        """// IndexParams are index properties such as store type and mappings.
        Params map[string]interface{} `json:"params"`"""

    @property
    def SourceUUID(self):
        # type: (...)->int
        """the UUID of the data source, this can be used to more tightly tie the index to a source.
        SourceUUID string `json:"sourceUUID,omitempty"`"""

    @property
    def SourceParams(self):
        # type: (...)->Mapping[str,object]
        """extra parameters to be defined. These are usually things like advanced connection and tuning parameters.
        SourceParams map[string]interface{} `json:"sourceParams,omitempty"`"""

    @property
    def SourceType(self):
        # type: (...)->str
        """the type of the data source, e.g. couchbase or nil depending on the Type field.
        SourceType string `json:"sourceType"`"""

    @property
    def PlanParams(self):
        # type: (...)->Mapping[str,object]
        """plan properties such as number of replicas and number of partitions.
        PlanParams map[string]interface{} `json:"planParams,omitempty"`"""


class GetSearchIndexOptions(object):
    pass


class ISearchIndex(object):
    pass


class GetAllSearchIndexesOptions(object):
    pass


class UpsertSearchIndexOptions(object):
    pass


class DropSearchIndexOptions(object):
    pass


class GetIndexedSearchIndexOptions(object):
    pass


class AnalyzeDocOptions(object):
    pass


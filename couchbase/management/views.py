from couchbase.management.generic import GenericManager
from typing import *


class ViewIndexManager(GenericManager):
    def __init__(self, parent_cluster):
        super(ViewIndexManager, self).__init__(parent_cluster)

    def get_design_document(self,  # type: ViewIndexManager
                            design_doc_name,  # type: str
                            namespace,  # type: DesignDocumentNamespace
                            **options):
        # type: (...)->DesignDocument
        """Fetches a design document from the server if it exists.
        Parameters
        Required:
        design_doc_name: string - the name of the design document.
        namespace,  # type: enum - PRODUCTION if the user is requesting a document from the production namespace
        or DEVELOPMENT if from the development namespace.
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
        When processing the server response, the client must strip the "_design/" prefix from the document ID (as well as the "_dev" prefix if present). For example, a doc.meta.id value of "_design/foo" must be parsed as "foo", and "_design/dev_bar" must be parsed as "bar".
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
                               design_doc_data,  # type: DesignDocument
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
                             design_doc_name,  # type: str
                             namespace,  # type: DesignDocumentNamespace
                             *options,
                             **kwargs):
        # type: (...)->None
        """
        Removes a design document.
        Parameters
        Required:
        design_doc_name: string - the name of the design document.
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
        void PublishDesignDocument(string design_doc_name, [options])
        Parameters
        Required:
        design_doc_name: string - the name of the development design document.
        Optional:
        Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.
        Returns
        Throws
        DesignDocumentNotFoundException (http 404)
        InvalidArgumentsException
        Any exceptions raised by the underlying platform
        """


class DesignDocument(object):
    def __init__(self):
        """DesignDocument provides a means of mapping a design document into an object. It contains within it a map of View."""

    @property
    def name(self):
        # type: (...)->str
        pass

    @property
    def views(self):
        # type: (...)->Mapping[str,View]
        pass


class View(object):

    @property
    def map(self):
        # type: (...)->str
        pass

    @property
    def reduce(self):
        # type: (...)->str
        pass
from enum import Enum

from couchbase import Duration
from couchbase.management.generic import GenericManager
from typing import *

from couchbase_core import JSONMapping, JSON
from couchbase_core.bucketmanager import BucketManager
from couchbase_core.client import Client
from mypy_extensions import TypedDict


from attr import ib as attrib, s as attrs
from attr.validators import instance_of as io, deep_mapping as dm

from couchbase_core.exceptions import HTTPError, HttpErrorHandler
import couchbase_core._libcouchbase as _LCB


class DesignDocumentNamespace(Enum):
    PRODUCTION = False
    DEVELOPMENT = True

    def prefix(self, ddocname):
        return Client._mk_devmode(ddocname, self.value)


class DesignDocumentNotFoundException(HTTPError):
    pass


class ViewErrorHandler(HttpErrorHandler):
    @staticmethod
    def mapping():
        # type (...)->Mapping[str, CBErrorType]
        return {'Unknown design': DesignDocumentNotFoundException}


@ViewErrorHandler.wrap
class ViewIndexManager(GenericManager):
    def __init__(self, parent_cluster, bucketname):
        super(ViewIndexManager, self).__init__(parent_cluster)
        self._bucketname = bucketname

    def get_design_document(self,  # type: ViewIndexManager
                            design_doc_name,  # type: str
                            namespace,  # type: DesignDocumentNamespace
                            timeout = None,  # type: Duration
                            **options):
        # type: (...)->DesignDocument
        """
        Fetches a design document from the server if it exists.

        :param str design_doc_name: the name of the design document.
        :param DesignDocumentNamespace namespace: PRODUCTION if the user is requesting a document from the production namespace
        or DEVELOPMENT if from the development namespace.
        :param options:
        :param Duration timeout: the time allowed for the operation to be terminated. This is controlled by the client.
        :return: An instance of DesignDocument.

        :raises: DesignDocumentNotFoundException
        """
        # Uri
        # GET http://localhost:8092/<bucketname>/_design/<ddocname>
        # Example response from server
        # {
        #     "views":{
        #         "test":{
        #             "map":"function (doc, meta) {\n\t\t\t\t\t\t  emit(meta.id, null);\n\t\t\t\t\t\t}",
        #             "reduce":"_count"
        #         }
        #     }
        # }
        path = "{bucketname}/_design/{design_doc_name}".format(bucketname=self._bucketname,
                                                               design_doc_name=namespace.prefix(design_doc_name))

        response = self._admin_bucket._http_request(type=_LCB.LCB_HTTP_TYPE_VIEW,
                                                    path=path,
                                                    method=_LCB.LCB_HTTP_METHOD_GET,
                                                    content_type="application/json")

        return self._json_to_ddoc(response)

    @staticmethod
    def _json_to_ddoc(
            response  # type: JSON
    ):
        # type: (...)->DesignDocument
        return DesignDocument(response[0], {k: View(**v) for k, v in response['views'].items()})

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
        path = "{bucketname}/ddocs".format(bucketname=self._bucketname)

        response = self._admin_bucket._http_request(type=_LCB.LCB_HTTP_TYPE_VIEW,
                                                    path=path,
                                                    method=_LCB.LCB_HTTP_METHOD_GET,
                                                    content_type="application/json")

        return list(map(lambda x: self._json_to_ddoc(x['doc']['json']), response))

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


@attrs
class View(object):
    name = attrib(validator=io(str))  # type: str
    reduce = attrib(validator=io(str))  # type: str


@attrs
class DesignDocument(object):
    name = attrib(validator=io(str))  # type: str
    views = attrib(validator=dm(io(str), io(View),None))  # type: Mapping[str,View]



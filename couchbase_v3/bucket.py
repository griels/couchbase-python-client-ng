from couchbase_v2.bucket import Bucket as SDK2Bucket
from .collection import CBCollection as SDK3Collection, CollectionOptions, CBCollection
from .options import OptionBlock, forward_args
from .result import *
class BucketOptions(OptionBlock):
    pass


class IViewResult(IResult):
    def __init__(self, sdk2_result # type: couchbase_v2.ViewResult
                ):
        pass


class Bucket(object):
    _bucket=None  # type: SDK2Bucket

    @overload
    def __init__(self,
                 connection_string,  # type: str
                 name=None,
                 *options  # type: BucketOptions
                 ):
        # type: (...)->None
        pass

    def __init__(self,
                 connection_string,  # type: str
                 name=None,
                 *options,
                 **kwargs
                ):
        # type: (...)->None
        self._name=name
        self._bucket=SDK2Bucket(connection_string,**forward_args(kwargs,*options))

    @property
    def name(self):
        # type: (...)->str
        return self._name
    from .collection import Scope

    def scope(self,
              scope_name  # type: str
              ):
        # type: (...)->Scope
        from couchbase_v3 import Scope

        return Scope(self, scope_name)

    def default_collection(self,
                           options=None  # type: CollectionOptions
                           ):
        # type: (...)->CBCollection
        return CBCollection(self)

    def collection(self,
                   collection_name,  # type: str
                   options=None  # type: CollectionOptions
                   ):
        # type: (...)->CBCollection
        return CBCollection(self, collection_name)

    def view_query(self,
                   design_doc,  # type: str
                   view_name,  # type: str
                   *view_options # type: ViewOptions
                   ):
        # type: (...)->IViewResult
        cb=self._bucket # type: SDK2Bucket
        res=cb.query(design_doc, view_name, **forward_args(None,*view_options))
        return IViewResult(res)

    def spatial_view_query(self,
                           design_doc,  # type: str
                           view_name,  # type: str
                           options=None  # type: ViewOptions
                           ):
        # type: (...)->ISpatialViewResult
        pass

    def views(self):
        # type: (...)->IViewManager
        pass

    def ping(self,
             options=None  # type: PingOptions
             ):
        # type: (...)->IPingResult
        pass
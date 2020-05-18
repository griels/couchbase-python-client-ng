from asyncio import AbstractEventLoop

from couchbase.asynchronous import wrap_async_decorator, wrap_async

try:
    import asyncio
except ImportError:
    import trollius as asyncio

from acouchbase.asyncio_iops import IOPS
from acouchbase.iterator import AQueryResult, ASearchResult, AAnalyticsResult, AViewResult
from couchbase_core.experimental import enable; enable()
from couchbase_core.experimental import enabled_or_raise; enabled_or_raise()
from couchbase.collection import AsyncCBCollection as BaseAsyncCBCollection
from couchbase_core.client import Client as CoreClient
from couchbase.bucket import AsyncBucket as V3AsyncBucket
from typing import *
from couchbase.cluster import AsyncCluster as V3AsyncCluster

T = TypeVar('T', bound=CoreClient)


class AIOClientMixin(object):
    def __new__(cls, *args, **kwargs):
        # type: (...) -> Type[T]
        if not hasattr(cls, "AIO_wrapped"):
            for k, method in cls._gen_memd_wrappers(AIOClientMixin._meth_factory).items():
                setattr(cls, k, method)
            cls.AIO_wrapped = True
        return super(AIOClientMixin, cls).__new__(cls, *args, **kwargs)

    @staticmethod
    def _meth_factory(meth, _):
        #import functools
        #@functools.wraps(meth)
        def ret(self, *args, **kwargs):
            rv = meth(self, *args, **kwargs)
            ft = asyncio.Future()

            def on_ok(res):
                ft.set_result(res)
                rv.clear_callbacks()

            def on_err(_, excls, excval, __):
                err = excls(excval)
                ft.set_exception(err)
                rv.clear_callbacks()

            rv.set_callbacks(on_ok, on_err)
            return ft

        #ret.__annotations__['return']="asyncio.futures.Future[{}]".format()
        return wrap_async_decorator(meth)(ret)

    def __init__(self, connstr=None, *args, **kwargs):
        loop = asyncio.get_event_loop()
        if connstr and 'connstr' not in kwargs:
            kwargs['connstr'] = connstr
        super(AIOClientMixin, self).__init__(IOPS(loop), *args, **kwargs)
        self._loop = loop

        cft = asyncio.Future(loop=loop)

        def ftresult(err):
            if err:
                cft.set_exception(err)
            else:
                cft.set_result(True)

        self._cft = cft
        self._conncb = ftresult

    def on_connect(self):
        if not self.connected:
            self._connect()
            return self._cft

    connected = CoreClient.connected


class Collection(AIOClientMixin, BaseAsyncCBCollection):
    def __init__(self,
                 *args,
                 **kwargs
                 ):
        super(AsyncCBCollection, self).__init__(*args, **kwargs)

    @wrap_async_decorator(BaseAsyncCBCollection.upsert)
    def upsert(self, *args, **kwargs):
        super(Collection, self).upsert(*args, **kwargs)


AsyncCBCollection = Collection


class ABucket(AIOClientMixin, V3AsyncBucket):
    def __init__(self, *args, **kwargs):
        super(ABucket,self).__init__(collection_factory=AsyncCBCollection, *args, **kwargs)

    view_query = wrap_async(V3AsyncBucket.view_query, AViewResult)


Bucket = ABucket


class ACluster(AIOClientMixin, V3AsyncCluster):
    def __init__(self, connection_string, *options, **kwargs):
        super(ACluster, self).__init__(connection_string=connection_string, *options, bucket_factory=Bucket, **kwargs)

    @wrap_async_decorator(V3AsyncCluster.query, AQueryResult)
    def query(self, *args, **kwargs):
        return super(ACluster, self).query(*args, **kwargs)

    @wrap_async_decorator(V3AsyncCluster.search_query, ASearchResult)
    def search_query(self, *args, **kwargs):
        return super(ACluster, self).search_query(*args, **kwargs)

    @wrap_async_decorator(V3AsyncCluster.analytics_query, AAnalyticsResult)
    def analytics_query(self, *args, **kwargs):
        return super(ACluster, self).analytics_query(*args, **kwargs)
#    analytics_query = AIOClientMixin.wrap_async(V3AsyncCluster.analytics_query, AAnalyticsResult)


Cluster = ACluster


def get_event_loop(evloop=None  # type: AbstractEventLoop
                   ):
    """
    Get an event loop compatible with acouchbase.
    Some Event loops, such as ProactorEventLoop (the default asyncio event
    loop for Python 3.8 on Windows) are not compatible with acouchbase as
    they don't implement all members in the abstract base class.

    :param evloop: preferred event loop
    :return: The preferred event loop, if compatible, otherwise, a compatible
    alternative event loop.
    """
    return IOPS.get_event_loop(evloop)

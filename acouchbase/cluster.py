from asyncio import AbstractEventLoop

from couchbase_core.asynchronous.client import AsyncConnectorMixin

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

class AIOConnectorMixin(object):
    def __init__(self, connstr=None, *args, **kwargs):
        loop = asyncio.get_event_loop()
        if connstr and 'connstr' not in kwargs:
            kwargs['connstr'] = connstr
        super(AIOConnectorMixin, self).__init__(IOPS(loop), *args, **kwargs)
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

    def wait_until_ready(self):
        on_connect=self.on_connect()
        if on_connect:
            get_event_loop().run_until_complete(on_connect)
            assert(self.connected)

    connected = CoreClient.connected


class AIOClientMixin(AIOConnectorMixin):
    def __new__(cls, *args,**kwargs):
        # type: (...) -> Type[T]
        if not hasattr(cls, "AIO_wrapped"):
            for k, method in cls._gen_memd_wrappers(AIOClientMixin._meth_factory).items():
                setattr(cls, k, method)
            cls.AIO_wrapped = True
        return super(AIOClientMixin, cls).__new__(cls, *args, **kwargs)

    @staticmethod
    def _meth_factory(meth, _):
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

        return ret

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

    def respond_to_value(self,  # type: AIOClientMixin
                         holder,  # type: asyncio.Future
                         responder):
        async def waiter(ft_result):
            result=await ft_result
            return responder(result)
        holder.add_done_callback(waiter)
        return holder

class AsyncCBCollection(AIOClientMixin, BaseAsyncCBCollection):
    def __init__(self,
                 *args,
                 **kwargs
                 ):
        super(AsyncCBCollection, self).__init__(*args, **kwargs)


Collection = AsyncCBCollection


class ABucket(AIOClientMixin, V3AsyncBucket):
    def __init__(self, *args, **kwargs):
        super(ABucket,self).__init__(collection_factory=AsyncCBCollection, *args, **kwargs)

    def view_query(self, *args, **kwargs):
        if "itercls" not in kwargs:
            kwargs["itercls"] = AViewResult
        return super(ABucket, self).view_query(*args, **kwargs)


Bucket = ABucket

from couchbase.cluster import AsyncConnectingCluster
class DefaultCluster(AIOConnectorMixin, AsyncConnectingCluster):
    def __init__(self, connection_string, *options, **kwargs):
        super(DefaultCluster, self).__init__(connection_string=connection_string, *options, bucket_factory=Bucket, **kwargs)


    def _operate_on_an_open_bucket(self,
                                   verb,
                                   failtype,
                                   *args,
                                   **kwargs):
        return super(DefaultCluster, self)._operate_on_an_open_bucket(verb, failtype, *args, **kwargs)

    def _operate_on_cluster(self,
                            verb,
                            failtype,  # type: Type[CouchbaseException]
                            *args,
                            **kwargs):

        return super(DefaultCluster, self)._operate_on_cluster(verb, failtype, *args, **kwargs)

    # for now this just calls functions.  We can return stuff if we need it, later.
    def _sync_operate_on_entire_cluster(self,
                                        verb,
                                        *args,
                                        **kwargs):
        return super(DefaultCluster, self)._sync_operate_on_entire_cluster(verb, *args, **kwargs)


class ACluster(AIOClientMixin, V3AsyncCluster):
    def __init__(self, connection_string, *options, **kwargs):
        super(ACluster, self).__init__(connection_string=connection_string, *options, bucket_factory=Bucket, **kwargs)

    def query(self, *args, **kwargs):
        if "itercls" not in kwargs:
            kwargs["itercls"] = AQueryResult
        return super(ACluster, self).query(*args, **kwargs)

    def search_query(self, *args, **kwargs):
        if "itercls" not in kwargs:
            kwargs["itercls"] = ASearchResult
        return super(ACluster, self).search_query(*args, **kwargs)

    def analytics_query(self, *args, **kwargs):
        return super(ACluster, self).analytics_query(*args, itercls=kwargs.pop('itercls', AAnalyticsResult),
                                                           **kwargs)


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

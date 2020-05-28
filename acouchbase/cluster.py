from asyncio import AbstractEventLoop

from couchbase_core.supportability import internal

from couchbase.asynchronous import async_kv_operation, wrap_async, async_iterable
from couchbase.result import ResultDeriv, Result
from couchbase.result import AsyncResult

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
from couchbase_core.asynchronous.client import AsyncClientMixin

T = TypeVar('T', bound=AsyncClientMixin)


class AIOClientMixinBase(object):
    """
    AIOClientMixinBase
    """
    @internal
    def __init__(self,  # type: AIOClientMixinBase
                 connstr=None,  # type: str
                 *args,  # type: Any
                 **kwargs  # type: Any
                 ):
        # type: (...) -> None
        """
        AIOClientMixinBase

        :param connstr: Connection string
        :param args: to be passed through to superconstructor
        :param kwargs: to be passed through to superconstructor
        """
        loop = asyncio.get_event_loop()
        if connstr and 'connstr' not in kwargs:
            kwargs['connstr'] = connstr
        super(AIOClientMixinBase, self).__init__(IOPS(loop), *args, **kwargs)
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


class AIOClientMixinType(type(AIOClientMixinBase)):
    @classmethod
    def gen_client(cls,  # type: Type[AIOClientMixinType]
                   base  # type: Type[T]
                   ):
        # type: (...) -> Type[T]
        class Result(AIOClientMixinBase, base):
            def __init__(self, *args, **kwargs):
                super(Result, self).__init__(*args, **kwargs)
            locals().update(base._gen_memd_wrappers(AIOClientMixinType._meth_factory))

        return Result

    @staticmethod
    def _meth_factory(meth, _):
        import functools

        @functools.wraps(meth)
        def ret(self,  # type: AsyncCBCollection
                *args,  # type: Any
                **kwargs  # type: Any
                ):
            # type: (...) -> asyncio.Future[AsyncResult]
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

        from couchbase.asynchronous import get_return_type
        # noinspection PyProtectedMember
        try:
            sync_rtype = get_return_type(meth)
            rtype=sync_rtype._async()
        except Exception as e:
            rtype = AsyncResult

        ret.__annotations__['return'] = 'asyncio.Future[{}]'.format(rtype.__name__)
        return async_kv_operation(meth)(ret)


class Collection(AIOClientMixinType.gen_client(BaseAsyncCBCollection)):
    def __copy__(self):
        pass

    def __deepcopy__(self, memo):
        pass


AsyncCBCollection = Collection


class ABucket(AIOClientMixinType.gen_client(V3AsyncBucket)):
    def __init__(self, *args, **kwargs):
        super(ABucket,self).__init__(collection_factory=AsyncCBCollection, *args, **kwargs)

    view_query = wrap_async(V3AsyncBucket.view_query, AViewResult)


Bucket = ABucket


class ACluster(AIOClientMixinType.gen_client(V3AsyncCluster)):
    def __init__(self, connection_string, *options, **kwargs):
        super(ACluster, self).__init__(connection_string=connection_string, *options, bucket_factory=Bucket, **kwargs)

    @async_iterable(V3AsyncCluster.query, AQueryResult)
    def query(self, *args, **kwargs):
        return super(ACluster, self).query(*args, **kwargs)

    @async_iterable(V3AsyncCluster.search_query, ASearchResult)
    def search_query(self, *args, **kwargs):
        return super(ACluster, self).search_query(*args, **kwargs)

    @async_iterable(V3AsyncCluster.analytics_query, AAnalyticsResult)
    def analytics_query(self, *args, **kwargs):
        return super(ACluster, self).analytics_query(*args, **kwargs)


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

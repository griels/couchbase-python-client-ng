from asyncio import AbstractEventLoop

from couchbase_core import IterableClass

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
import boltons.funcutils

T = TypeVar('T', bound=CoreClient)
iterable_producer = TypeVar('iterable_producer', bound=Callable)


def wrap_async(method,   # type: iterable_producer
               default_iterator  # type: Type[IterableClass]
               ):
    # type: (...) -> iterable_producer
    import functools

    def wrap(func):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            return func(self, *args, **kwargs)
        wrapper.__annotations__=method.__annotations__
        wrapper.__annotations__['itercls'] = Type[default_iterator]
        wrapper.__annotations__['return'] = default_iterator
        return wrapper
    return boltons.funcutils.partial(wrap)


class AIOClientMixin(object):
    def __new__(cls, *args, **kwargs):
        # type: (...) -> Type[T]
        if not hasattr(cls, "AIO_wrapped"):
            for k, method in cls._gen_memd_wrappers(AIOClientMixin._meth_factory).items():
                setattr(cls, k, method)
            cls.AIO_wrapped = True
        return super(AIOClientMixin, cls).__new__(cls, *args, **kwargs)

    @classmethod
    def wrap_async(cls,  # type: Type[AIOClientMixin]
                   method,  # type: iterable_producer
                   default_iterator  # type: Type[IterableClass]
                   ):
        # type: (...) -> iterable_producer
        import functools

        #@boltons.funcutils.wraps(method)
        @functools.wraps(method)
        def wrapper_raw(self,
                        *args,
                        **kwargs
                        ):
            return method(self, *args, itercls=kwargs.pop('itercls',default_iterator),**kwargs)

        fresh = boltons.funcutils.FunctionBuilder.from_func(method)
        try:
            fresh.remove_arg('itercls')
        except ValueError:
            pass
        fresh.add_arg('itercls', default_iterator, kwonly=True)
        method_with_itercls = fresh.get_func()
        method_with_itercls.__annotations__['itercls'] = Type[default_iterator]
        method_with_itercls.__annotations__['return'] = default_iterator
        wrapper = boltons.funcutils.update_wrapper(wrapper_raw, method_with_itercls)
        wrapper.__annotations__ = method.__annotations__
        wrapper.__doc__ += """
        :param itercls: type of the iterable class to be returned, :class:`{}` by default""".format(
            default_iterator.__name__)
        return wrapper

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

    view_query = AIOClientMixin.wrap_async(V3AsyncBucket.view_query, AViewResult)


Bucket = ABucket


class ACluster(AIOClientMixin, V3AsyncCluster):
    def __init__(self, connection_string, *options, **kwargs):
        super(ACluster, self).__init__(connection_string=connection_string, *options, bucket_factory=Bucket, **kwargs)

    import functools
    @wrap_async(V3AsyncCluster.query, AQueryResult)
    #@functools.wraps(V3AsyncCluster.query)
    def query(self, *args, itercls=AQueryResult, **kwargs):
        return super(ACluster, self).query(*args, itercls=itercls, **kwargs)
    search_query = AIOClientMixin.wrap_async(V3AsyncCluster.search_query, ASearchResult)
    analytics_query = AIOClientMixin.wrap_async(V3AsyncCluster.analytics_query, AAnalyticsResult)


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

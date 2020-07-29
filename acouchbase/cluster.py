from asyncio import AbstractEventLoop

from couchbase_core.supportability import internal

from couchbase.asynchronous import wrap_async, async_iterable, async_kv_operation
import logging
import traceback
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
from six import with_metaclass

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


Bases = TypeVar('Bases', bound=Tuple[Type,...])


class AIOClientMixinType(type(AIOClientMixinBase)):
    def __new__(cls,  # type: Type[AIOClientMixinType]
                name,  # type: str
                bases,  # type: Bases
                namespace  # type: Dict[str, Any]
                ):
        # type: (...) -> Type[AsyncCBCollection]
        namespace=dict(**namespace)
        namespace.update(bases[0]._gen_memd_wrappers(AIOClientMixinType._meth_factory))
        Final=super(AIOClientMixinType, cls).__new__(cls, name, (AIOClientMixinBase,)+bases, namespace)
        return Final

    @staticmethod
    def _meth_factory(meth, _):
        import functools
        import boltons.funcutils
        @functools.wraps(meth)
        def wrapped_raw(self,  # type: AsyncCBCollection
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

        meth_annotations = get_type_hints(meth)
        try:
            fresh_ann=wrapped_raw.__annotations__
        except:
            fresh_ann=dict()

        fresh_ann.update(meth_annotations)
        from couchbase.asynchronous import get_return_type
        # noinspection PyProtectedMember
        ret=wrapped_raw
        #ret=functools.wraps(meth,assigned=tuple(set(functools.WRAPPER_ASSIGNMENTS)-{'__annotations__'}))(wrapped_raw)

        try:
            sync_rtype = get_return_type(meth)
            rtype=sync_rtype._async()
        except Exception as e:
            rtype = AsyncResult
        try:
            fresh_ann=getattr(meth,'__annotations',{})
            fresh_ann['return']='asyncio.Future[{}]'.format(rtype.__name__)
            ret.__qualname__='AsyncCBCollection.{}'.format(ret.__name__)
            setattr(ret,'__annotations__',fresh_ann)
        except Exception as e:
            logging.error("Prolbmes {}".format(traceback.format_exc()))
        logging.error("Wrapped {} as {}".format(meth, ret))
        return ret# async_kv_operation(meth,rtype)(ret)


class Collection(with_metaclass(AIOClientMixinType, BaseAsyncCBCollection)):
    def __copy__(self):
        pass

    def __deepcopy__(self, memo):
        pass

AsyncCBCollection = Collection


class ABucket(with_metaclass(AIOClientMixinType, V3AsyncBucket)):
    def __init__(self, *args, **kwargs):
        super(ABucket,self).__init__(collection_factory=AsyncCBCollection, *args, **kwargs)

    view_query = wrap_async(V3AsyncBucket.view_query, AViewResult)


Bucket = ABucket


class ACluster(with_metaclass(AIOClientMixinType, V3AsyncCluster)):
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

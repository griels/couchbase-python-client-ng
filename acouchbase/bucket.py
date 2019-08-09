try:
    import asyncio
except ImportError:
    import trollius as asyncio

from acouchbase.asyncio_iops import IOPS
from acouchbase.iterator import AView, AN1QLRequest
from couchbase_v2.asynchronous.bucket import AsyncBucket as V2AsyncBucket
from couchbase_core.experimental import enabled_or_raise; enabled_or_raise()
from couchbase_core._pyport import with_metaclass
from couchbase_core.bucket import Bucket as CoreSyncBucket


class AIOBucket(CoreSyncBucket):
    def __init__(self, *args, **kwargs):
        loop = asyncio.get_event_loop()
        self.asyncbucketbase.__init__(self, IOPS(loop), *args, **kwargs)
        self._loop = loop

        cft = asyncio.Future(loop=loop)
        def ftresult(err):
            if err:
                cft.set_exception(err)
            else:
                cft.set_result(True)

        self._cft = cft
        self._conncb = ftresult

    def query(self, *args, **kwargs):
        if "itercls" not in kwargs:
            kwargs["itercls"] = AView
        return self.asyncbucketbase.query(self, *args, **kwargs)

    def n1ql_query(self, *args, **kwargs):
        if "itercls" not in kwargs:
            kwargs["itercls"] = AN1QLRequest
        return self.asyncbucketbase.n1ql_query(self, *args, **kwargs)

    def connect(self):
        if not self.connected:
            self._connect()
            return self._cft

class AsyncAdapter(type):
    def __new__(cls, name, bases, attr):
        asyncbucketbase=bases[0]
        bases=(AIOBucket,)+bases
        attr.update(asyncbucketbase.syncbucket._gen_memd_wrappers(AsyncAdapter._meth_factory))
        attr['asyncbucketbase']=asyncbucketbase
        return super(AsyncAdapter,cls).__new__(cls, name, bases, attr)

    def _meth_factory(meth, name):
        def ret(self, *args, **kwargs):
            rv = meth(self, *args, **kwargs)
            ft = asyncio.Future()
            def on_ok(res):
                ft.set_result(res)
                rv.clear_callbacks()

            def on_err(res, excls, excval, exctb):
                err = excls(excval)
                ft.set_exception(err)
                rv.clear_callbacks()

            rv.set_callbacks(on_ok, on_err)
            return ft

        return ret

class V2Bucket(with_metaclass(AsyncAdapter,V2AsyncBucket)):
    def __init__(self, *args, **kwargs):
        super(V2Bucket,self).__init__(*args, **kwargs)

Bucket=V2Bucket

from couchbase_core.asynchronous.bucket import V3AsyncCoreBucket
# class V3AIOCoreBucket(with_metaclass(AsyncAdapter,V3AsyncCoreBucket)):
#     def __init__(self, *args, **kwargs):
#         super(V3AIOCoreBucket,self).__init__(*args, **kwargs)
#
# from couchbase.bucket import Bucket as V3SyncBucket
#
# class V3Bucket(V3SyncBucket):
#     def __init__(self, *args, **kwargs):
#         kwargs['corebucket_class']=V3AIOCoreBucket
#         super(V3Bucket,self).__init__(*args,**kwargs)

#from couchbase.bucket import Bucket
#
#
# class CoreAsyncBucket(with_metaclass(AsyncAdapter,CoreAsyncBucket)):
#     def __init__(self, *args, **kwargs):
#         super(CoreAsyncBucket,self).__init__(*args,**kwargs)
#
# class V3Bucket(Bucket):
#     def __init__(self, *args, **kwargs):
#         kwargs['corebucket_class']=CoreAsyncBucket
#         super(V3Bucket,self).__init__(*args, **kwargs)


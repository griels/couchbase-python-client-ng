try:
    import asyncio
except ImportError:
    import trollius as asyncio

from acouchbase.asyncio_iops import IOPS
from acouchbase.iterator import AView, AN1QLRequest
from couchbase_core.experimental import enabled_or_raise; enabled_or_raise()
from couchbase_core._pyport import with_metaclass
from couchbase_core.bucket import Bucket as CoreBucket
from couchbase_core.asynchronous.bucket import AsyncBucket as CoreAsyncBucket

class AsyncBucketFactory(type):
    def __new__(cls, name, bases, attrs):
        asyncbase=bases[0]
        n1ql_query=getattr(asyncbase,'n1ql_query',getattr(asyncbase,'query'))
        view_query=getattr(asyncbase,'view_query',getattr(asyncbase,'query'))
        class Bucket(*bases):
            def __init__(self, *args, **kwargs):
                loop = asyncio.get_event_loop()
                super(Bucket, self).__init__(IOPS(loop), *args, **kwargs)
                self._loop = loop

                cft = asyncio.Future(loop=loop)
                def ftresult(err):
                    if err:
                        cft.set_exception(err)
                    else:
                        cft.set_result(True)

                self._cft = cft
                self._conncb = ftresult

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

            def view_query(self, *args, **kwargs):
                if "itercls" not in kwargs:
                    kwargs["itercls"] = AView
                return view_query(self, *args, **kwargs)

            def query(self, *args, **kwargs):
                if "itercls" not in kwargs:
                    kwargs["itercls"] = AN1QLRequest
                return n1ql_query(self,*args, **kwargs)

            locals().update(CoreBucket._gen_memd_wrappers(_meth_factory))

            def connect(self):
                if not self.connected:
                    self._connect()
                    return self._cft

        return super(AsyncBucketFactory,cls).__new__(cls, name, (Bucket,)+bases[1:], attrs)

from couchbase_v2.asynchronous.bucket import AsyncBucket as V2AsyncBucket
class Bucket(with_metaclass(AsyncBucketFactory,V2AsyncBucket)):
    def __init__(self, *args, **kwargs):
        super(Bucket,self).__init__(*args,**kwargs)


from couchbase.bucket import Bucket as V3SyncBucket

class V3CoreBucket(with_metaclass(AsyncBucketFactory,CoreAsyncBucket)):
    def __init__(self, *args, **kwargs):
        super(V3CoreBucket,self).__init__(*args,**kwargs)

class V3Bucket(V3SyncBucket):
    def __init__(self, *args, **kwargs):
        kwargs['corebucket_class']=V3CoreBucket
        super(V3Bucket,self).__init__(*args,**kwargs)
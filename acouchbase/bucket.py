try:
    import asyncio
except ImportError:
    import trollius as asyncio

from acouchbase.asyncio_iops import IOPS
from acouchbase.iterator import AView, AN1QLRequest
from couchbase_v2.asynchronous.bucket import AsyncBucket as V2AsyncBucket
from couchbase_core.experimental import enabled_or_raise; enabled_or_raise()
from couchbase_core._pyport import with_metaclass
from couchbase_core.asynchronous import AsyncBucketFactory as CoreAsyncBucketFactory

class AsyncBucketFactory(type):
    def __new__(cls, name, bases, attrs):
        asyncbase=bases[0]
        class Bucket(asyncbase):
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

            def query(self, *args, **kwargs):
                if "itercls" not in kwargs:
                    kwargs["itercls"] = AView
                return super().query(*args, **kwargs)

            def n1ql_query(self, *args, **kwargs):
                if "itercls" not in kwargs:
                    kwargs["itercls"] = AN1QLRequest
                return super().n1ql_query(*args, **kwargs)

            locals().update(V2AsyncBucket._gen_memd_wrappers(_meth_factory))

            def connect(self):
                if not self.connected:
                    self._connect()
                    return self._cft

        return super(AsyncBucketFactory,cls).__new__(cls, name, (Bucket,)+bases[1:], attrs)

class Bucket(with_metaclass(AsyncBucketFactory,V2AsyncBucket)):
    pass


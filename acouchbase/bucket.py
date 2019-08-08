try:
    import asyncio
except ImportError:
    import trollius as asyncio

from acouchbase.asyncio_iops import IOPS
from acouchbase.iterator import AView, AN1QLRequest
from couchbase_v2.asynchronous.bucket import AsyncBucket as V2AsyncBucket
from couchbase_core.experimental import enabled_or_raise; enabled_or_raise()
from couchbase_core._pyport import with_metaclass


class AsyncAdapter(type):
    def __new__(cls, name, bases, attr):
        syncbucket=bases[0]
        attr.update(syncbucket._gen_memd_wrappers(AsyncAdapter._meth_factory))
        attr.syncbucket=syncbucket
        return super(AsyncAdapter,cls).__new__(cls, name, bases, attr)

    def __init__(self, *args, **kwargs):
        loop = asyncio.get_event_loop()
        self.syncbucket.__init__(self, IOPS(loop), *args, **kwargs)
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
        return self.syncbucket.query(self, *args, **kwargs)

    def n1ql_query(self, *args, **kwargs):
        if "itercls" not in kwargs:
            kwargs["itercls"] = AN1QLRequest
        return self.syncbucket.n1ql_query(self, *args, **kwargs)



    def connect(self):
        if not self.connected:
            self._connect()
            return self._cft

class V2Bucket(with_metaclass(AsyncAdapter,V2AsyncBucket)):
    def __init__(self, *args, **kwargs):
        super(V2Bucket,self).__init__(self, *args, **kwargs)

Bucket=V2Bucket
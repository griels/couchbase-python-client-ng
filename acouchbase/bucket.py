try:
    import asyncio
except ImportError:
    import trollius as asyncio

from acouchbase.asyncio_iops import IOPS
from acouchbase.iterator import AView, AN1QLRequest
from couchbase_v2.asynchronous.bucket import AsyncBucket as V2AsyncBucket
from couchbase_core.experimental import enabled_or_raise; enabled_or_raise()


class AsyncAdapter(object):
    _super=V2AsyncBucket
    def __init__(self, *args, **kwargs):
        loop = asyncio.get_event_loop()
        self._super.__init__(self, IOPS(loop), *args, **kwargs)
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
        return self._super.query(self, *args, **kwargs)

    def n1ql_query(self, *args, **kwargs):
        if "itercls" not in kwargs:
            kwargs["itercls"] = AN1QLRequest
        return self._super.n1ql_query(self, *args, **kwargs)

    locals().update(V2AsyncBucket._gen_memd_wrappers(_meth_factory))

    def connect(self):
        if not self.connected:
            self._connect()
            return self._cft

class V2Bucket(AsyncAdapter, V2AsyncBucket):
    def __init__(self, *args, **kwargs):
        AsyncAdapter.__init__(self, *args, **kwargs)

Bucket=V2Bucket
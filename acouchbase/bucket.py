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
from couchbase.bucket import Bucket as V3SyncBucket


class AsyncAdapter(type):
    def __new__(cls, name, bases, attr):
        asyncbucketbase=bases[0]

        class AIOBucket(asyncbucketbase):
            def __init__(self, *args, **kwargs):
                loop = asyncio.get_event_loop()
                super(AIOBucket,self).__init__(IOPS(loop), *args, **kwargs)
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
                return super(AIOBucket,self).query(*args, **kwargs)

            def n1ql_query(self, *args, **kwargs):
                if "itercls" not in kwargs:
                    kwargs["itercls"] = AN1QLRequest
                return super(AIOBucket,self).n1ql_query(*args, **kwargs)

            def connect(self):
                if not self.connected:
                    self._connect()
                    return self._cft

        attr.update(asyncbucketbase.syncbucket._gen_memd_wrappers(AsyncAdapter._meth_factory))
        attr['asyncbucketbase']=asyncbucketbase
        return super(AsyncAdapter,cls).__new__(cls, name, tuple([AIOBucket])+bases[1:], attr)

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


class V2AIOBucket(with_metaclass(AsyncAdapter, V2AsyncBucket)):
    def __init__(self, *args, **kwargs):
        super(V2AIOBucket, self).__init__(*args, **kwargs)


Bucket = V2AIOBucket


#class V3AIOCoreBucket(with_metaclass(AsyncAdapter, V3SyncBucket)):
#    def __init__(self, *args, **kwargs):
#        super(V3AIOCoreBucket, self).__init__(*args, **kwargs)


class V3AIOBucket(V3SyncBucket):
    def __init__(self, *args, **kwargs):
        kwargs['corebucket_class'] = None#V3AIOCoreBucket
        super(V3AIOBucket, self).__init__(*args, **kwargs)

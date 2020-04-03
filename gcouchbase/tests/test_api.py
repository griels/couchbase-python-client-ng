from couchbase_tests.base import ApiImplementationMixin, SkipTest
try:
    import gevent
except ImportError as e:
    raise SkipTest(e)

from gcouchbase.cluster import Bucket, GView
from couchbase_tests.importer import get_configured_classes
import os


class GEventImplMixin(ApiImplementationMixin):
    factory = Bucket
    viewfactory = GView
    should_check_refcount = True
    def _implDtorHook(self):
        import gc
        if not getattr(self.cb,'closed',True):
            waiter = getattr(self.cb,'_get_close_future',None)
            cb_desc=str(self.cb)
            del self.cb
            gc.collect()
            if not waiter:
                raise SkipTest("no _get_close_future for {}".format(cb_desc))
            if os.getenv("PYCBC_GEVENT_WAIT") and not waiter().wait(10):
                raise SkipTest("Not properly cleaned up!")


skiplist = ('IopsTest', 'LockmodeTest', 'PipelineTest')

configured_classes = get_configured_classes(GEventImplMixin,
                                            skiplist=skiplist)

globals().update(configured_classes)

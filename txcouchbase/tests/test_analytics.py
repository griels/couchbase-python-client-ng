from twisted.internet import reactor, defer
from twisted.internet.task import deferLater
from twisted.trial._synctest import SkipTest

import couchbase.tests_v3.cases.analytics_t
from couchbase import Cluster as SyncCluster
from txcouchbase.bucket import TxCluster, BatchedAnalyticsResult
from txcouchbase.tests.base import gen_base
import os


class TxAnalyticsTest(gen_base(couchbase.tests_v3.cases.analytics_t.AnalyticsTestCase,timeout=20)):
    def setUp(self):
        if not os.getenv("PYCBC_ASYNC_ANALYTICS"):
            raise SkipTest("TODO: Fix async analytics testing")
        self._factory = SyncCluster
        super(TxAnalyticsTest, self).setUp()
        self._factory = self.gen_cluster
        self.cluster = self.make_connection()

    @staticmethod
    def sleep(secs):
        def slept(*args, **kwargs):
            pass

        return deferLater(reactor, secs, slept)

    def _passthru(self, result, *args, **kwargs):
        return result

    def try_n_times(self, num_times, seconds_between, func,  *args, on_success=_passthru, **kwargs):
        if not isinstance(self.cluster, TxCluster):
            return super(TxAnalyticsTest, self).try_n_times(num_times, seconds_between, func, on_success=on_success, *args,
                                                            **kwargs)

        class ResultHandler(object):
            def __init__(self, parent):
                self.remaining = num_times
                self._parent = parent

            def start(self, *exargs, **exkwargs):
                ret = func(*args, **kwargs)

                def kicker(result):
                    return self.success(result, args, kwargs, *exargs, **exkwargs)
                try:
                    result = ret.addCallback(kicker)
                    ret.addErrback(self.on_fail)
                except:
                    result = ret
                return result

            def success(self, result, *exargs, **kwargs):
                return on_success(result, *exargs, **kwargs)

            def on_fail(self, deferred_exception):
                deferred_exception.printDetailedTraceback()
                if self.remaining:
                    self.remaining -= 1
                    deferred = TxAnalyticsTest.sleep(seconds_between)
                    deferred.addErrback(self._parent.fail)
                    return deferred.addCallback(self.start)
                else:
                    return self._parent.fail(
                        "unsuccessful {} after {} times, waiting {} seconds between calls".format(func, num_times,
                                                                                                  seconds_between))

        return ResultHandler(self).start()

    def checkResult(self, result, callback):
        # d = defer.Deferred()
        def check(answer, *args, **kwargs):
            import logging
            final_answer = getattr(answer, 'result', answer)
            try:

                logging.error(
                    "Calling verifier {} with final_answer {}, (answer {}), {}, {}".format(callback, final_answer, answer, args, kwargs))
                result = callback(final_answer, *args, **kwargs)
                logging.error(
                    "Called verifier {} with final_answer {}, (answer {}), {}, {} and got {}".format(callback,
                                                                                                     final_answer,
                                                                                                     answer, args,
                                                                                                     kwargs, result))

                return self._success(result)
            except Exception as e:
                import traceback
                logging.exception("Called verifier {} with final_answer {}, (answer {}), {}, {} and got exception:".format(callback,final_answer, answer, args, kwargs))
                return self._fail(traceback.format_exc())

        result.addErrback(defer.fail)
        return result.addCallback(check)

    def _fail(self, message):
        import logging
        logging.error(message)
        return defer.fail

    def _success(self, *args, **kwargs):
        import twisted.internet.defer
        return None#twisted.internet.defer.Deferred()

    def _verify(self, d  # type: Base
                ):
        import logging
        def verify(o):
            logging.error("in callback with {}".format(o))
            self.assertIsInstance(o, BatchedAnalyticsResult)
            rows = [r for r in o]
            logging.error("End of callback")

        result = d.addCallback(verify)
        d.addErrback(self.mock_fallback)
        logging.error("ready to return")
        return result

    def assertQueryReturnsRows(self, query, *options, **kwargs):
        d = self.cluster.analytics_query(query, *options, **kwargs)

        def query_callback(result):
            self.assertIsInstance(result, BatchedAnalyticsResult)

            rows = result.rows()
            if len(rows) > 0:
                return rows
            return self._success("no rows in result")

        d.addErrback(self.fail)
        return d.addCallback(query_callback)

    locals().update()

    @property
    def factory(self):
        return self._factory

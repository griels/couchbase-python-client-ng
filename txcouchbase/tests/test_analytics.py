from twisted.internet import reactor
from twisted.internet.task import deferLater
from twisted.trial._synctest import SkipTest

import couchbase.tests_v3
from couchbase import Cluster as SyncCluster
from txcouchbase.bucket import TxCluster, BatchedAnalyticsResult
from txcouchbase.tests.base import gen_base


class TxAnalyticsTest(gen_base(couchbase.tests_v3.cases.analytics_t.AnalyticsTestCase)):
    def setUp(self):
        raise SkipTest()
        self._factory=SyncCluster
        super(TxAnalyticsTest, self).setUp()
        # if self.is_mock:
        #     raise SkipTest("analytics not mocked")
        # if int(self.get_cluster_version().split('.')[0]) < 6:
        #     raise SkipTest("no analytics in {}".format(self.get_cluster_version()))
        # self.mgr = self.cluster.analytics_indexes()
        # self.dataset_name = 'test_beer_dataset'
        # # create a dataset to query
        # self.mgr.create_dataset(self.dataset_name, 'beer-sample', CreateDatasetOptions(ignore_if_exists=True))
        # def has_dataset(name):
        #     datasets = self.mgr.get_all_datasets()
        #     return [d for d in datasets if d.dataset_name == name][0]
        # self.try_n_times(10, 3, has_dataset, self.dataset_name)
        # # connect it...
        #
        # self.mgr.connect_link()
        self._factory=self.gen_cluster
        self.cluster=self.make_connection()


    def sleep(self, secs):
        return deferLater(reactor, secs, lambda: None)

    def try_n_times(self, num_times, seconds_between, func, *args, **kwargs):
        if not isinstance(self.cluster, TxCluster):
            return super(TxAnalyticsTest, self).try_n_times(num_times, seconds_between, func, *args, **kwargs)
        class ResultHandler(object):
            def __init__(self, parent):
                self.remaining=num_times
                self._parent=parent
            def start(self):
                ret = func(*args, **kwargs)
                result = ret.addCallback(self.success)
                ret.addErrback(self.on_fail)
                return result
            def success(self, result):
                return result
            def on_fail(self, deferred_exception):
                #deferred_exception.catch(Exception)
                #return None
                if self.remaining:
                    self.remaining-=1
                    return self.sleep(seconds_between).addCallback(self.start)
                else:
                    self._parent.fail("unsuccessful {} after {} times, waiting {} seconds between calls".format(func, num_times, seconds_between))
        return ResultHandler(self).start()

    def checkResult(self, result, callback):
        return result#result.addCallback(callback)

    def _verify(self, d  # type: Base
                    ):
        import logging
        def verify(o):
            logging.error("in callback with {}".format(o))
            self.assertIsInstance(o, BatchedAnalyticsResult)
            rows = [r for r in o]
            logging.error("End of callback")

        result= d.addCallback(verify)
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
            raise Exception("no rows in result")
        return d.addCallback(query_callback)

    locals().update()
    @property
    def factory(self):
        return self._factory
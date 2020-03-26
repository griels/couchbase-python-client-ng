# Copyright 2013, Couchbase, Inc.
# All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from couchbase.exceptions import UnknownHostError
from twisted.internet import defer

from couchbase.management.analytics import CreateDatasetOptions
from couchbase_core.exceptions import (
    BucketNotFoundError,
    ObjectDestroyedError)

from couchbase_tests.base import ConnectionTestCase
from couchbase_core.connstr import ConnectionString
from txcouchbase.tests.base import gen_base
from txcouchbase.bucket import TxBucket, TxCluster, BatchedAnalyticsResult
from nose.tools import timed
import sys
from unittest import SkipTest
from couchbase.cluster import Cluster as SyncCluster

Base = gen_base(ConnectionTestCase)

# TODO: once TxCluster is fully async, retarget to TxCluster and rename to BasicClusterTest


class BasicClusterTest(Base):
    def __init__(self, *args, **kwargs):
        super(BasicClusterTest, self).__init__(*args, **kwargs)

    @property
    def factory(self):
        return self.gen_cluster

    def testConnectionSuccess(self):
        cb = self.make_connection()
        d = cb.on_connect()
        d.addCallback(lambda x: self.assertTrue(cb.connected))
        return d

    def testConnectionFailure(self  # type: Base
                              ):
        cb = self.make_connection(host="qweqwe")
        d = cb.on_connect()
        d.addCallback(lambda x: x, cb)
        return self.assertFailure(d, UnknownHostError)

    @timed(10)
    def testBadEvent(self):
        if sys.version_info>=(3,7):
            raise SkipTest("Deadlocks on Python 3.x")
        cb = self.make_connection()
        self.assertRaises(ValueError, cb.registerDeferred,
                          'blah',
                          defer.Deferred())

        d = defer.Deferred()
        cb.registerDeferred('connect', d)
        d.addBoth(lambda x: None)
        return d

    def testMultiHost(self):
        info = self.cluster_info
        cs = ConnectionString.parse(self.make_connargs()['connection_string'])
        cs.hosts = [ info.host + ':' + '10', info.host + ':' + str(info.port) ]
        cb = self.make_connection(connection_string=cs.encode())
        d = cb.on_connect()
        d.addCallback(lambda x: self.assertTrue(cb.connected))
        return d

    def testConnstrFirstArg(self):
        info = self.cluster_info
        s = self.make_connargs()['connection_string']
        cb = TxBucket(connection_string=s,password=self.cluster_info.bucket_password)
        d = cb.on_connect().addCallback(lambda x: self.assertTrue(cb.connected))
        self.register_cleanup(cb)
        return d

    def testConnectionDestroyed(self):
        cb = self.make_connection()
        d = cb.on_connect()
        self.assertFailure(d, ObjectDestroyedError)
        return d



import couchbase.tests_v3.cases.cluster_t
import couchbase.tests_v3.cases.analytics_t
from couchbase_v2.bucket import Bucket as V2Bucket

import asyncio

class RewrappedCluster(TxCluster):
    def __init__(self, *args, **kwargs):
        async def wrapper():
            return super(RewrappedCluster, self).__init__(*args,**kwargs)
        self.evloop = asyncio.get_event_loop()
        self.evloop.run_until_complete(wrapper())
    async def wrapper(self, meth, *args, **kwargs):
        result=meth(super(RewrappedCluster,self), *args, **kwargs)
        return await result
    def _wrap(self,  # type: TxDeferredClient
              meth, *args, **kwargs):
        """
        Wraps a Twisted Cluster back into a synchronous cluster,
        for testing purposes
        """
        #if not self.connected:
        #    return self._connectSchedule(self._wrap, meth, *args, **kwargs)


        result=self.evloop.run_until_complete(self.wrapper(meth, *args, **kwargs))
        return result

    ### Generate the methods
    def _meth_factory(meth, name):
        def ret(self, *args, **kwargs):
            return self._wrap(meth, *args, **kwargs)
        return ret

    locals().update(TxCluster._gen_memd_wrappers(_meth_factory))
    for x in TxCluster._MEMCACHED_OPERATIONS:
        if locals().get(x+'_multi', None):
            locals().update({x+"Multi": locals()[x+"_multi"]})

import os
if False or os.getenv("PYCBC_TXCLUSTER_TESTS"):
    class TxClusterTests(couchbase.tests_v3.cases.analytics_t.AnalyticsTestCase):
        #@property
        #def factory(self):
        #    return self._factory
        @property
        def cluster_factory(self):
            return RewrappedCluster
        def realSetUp(self):
            #self._factory=V2Bucket
            super(couchbase.tests_v3.cases.analytics_t.AnalyticsTestCase, self).setUp()
            #self._factory=Base.gen_cluster
            #self.cluster=self.make_connection()
from twisted.internet.task import deferLater
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
if True:
    class TxAnalyticsTest(gen_base(couchbase.tests_v3.cases.analytics_t.AnalyticsTestCase)):
        def setUp(self):
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
                    deferred_exception.catch(Exception)
                    return None
                    #if self.remaining:
                    #    self.remaining-=1
                    #    self.sleep(seconds_between).addCallback()
                    #else:
                    #self._parent.fail("unsuccessful {} after {} times, waiting {} seconds between calls".format(func, num_times, seconds_between))
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

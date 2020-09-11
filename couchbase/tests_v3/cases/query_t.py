# -*- coding:utf-8 -*-
#
# Copyright 2020, Couchbase, Inc.
# All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import datetime
from unittest import SkipTest

from couchbase.n1ql import UnsignedInt64
from couchbase.cluster import QueryOptions, QueryProfile, QueryResult
from couchbase.n1ql import QueryMetaData, QueryStatus, QueryWarning
from couchbase_tests.base import CollectionTestCase, BASEDIR


class QueryTests(CollectionTestCase):
    def setUp(self):
        super(QueryTests, self).setUp()

        if not self.is_realserver:
            raise SkipTest('mock does not mock queries')
        # since we know that the CollectionTestCase loads beers, lets
        # use beer-sample bucket for our query tests.  NOTE: it isn't
        # clear to me that this is a great idea long-term, but we seem
        # to require this, and that bucket has a primary index, lets
        # use it.  Later when the querymgr works, and it can wait for the
        # index to exist, we can make this more isolated
        self.query_bucket = 'beer-sample'

    def assertRows(self,
                   result,  # type: QueryResult
                   expected_count):
        count = 0
        self.assertIsNotNone(result)
        for row in result.rows():
            self.assertIsNotNone(row)
            count += 1
        print(result.errors)
        self.assertEqual(count, expected_count)

    def test_simple_query(self):
        result = self.cluster.query("SELECT * FROM `beer-sample` LIMIT 2")
        self.assertRows(result, 2)
        self.assertIsNone(result.metadata().profile())
        self.assertTrue(result._params._adhoc)

    def test_simple_query_prepared(self):
        result = self.cluster.query("SELECT * FROM `beer-sample` LIMIT 2", QueryOptions(adhoc=False, metrics=True))  # type: QueryResult
        self.assertRows(result, 2)
        self.assertIsNone(result.metadata().profile())
        self.assertFalse(result._params._adhoc)

    def test_simple_query_with_positional_params(self):
        result = self.cluster.query("SELECT * FROM `beer-sample` WHERE brewery_id LIKE $1 LIMIT 1", '21st_amendment%')
        self.assertRows(result, 1)

    def test_simple_query_with_named_params(self):
        result = self.cluster.query("SELECT * FROM `beer-sample` WHERE brewery_id LIKE $brewery LIMIT 1",
                                    brewery='21st_amendment%')
        self.assertRows(result, 1)

    def test_simple_query_with_positional_params_in_options(self):
        result = self.cluster.query("SELECT * FROM `beer-sample` WHERE brewery_id LIKE $1 LIMIT 1",
                                    QueryOptions(positional_parameters=['21st_amendment%']))
        self.assertRows(result, 1)

    def test_simple_query_with_named_params_in_options(self):
        result = self.cluster.query("SELECT * FROM `beer-sample` WHERE brewery_id LIKE $brewery LIMIT 1",
                                    QueryOptions(named_parameters={'brewery':'21st_amendment%'}))
        self.assertRows(result, 1)

    # NOTE: Ideally I'd notice a set of positional parameters in the query call, and assume they were the positional
    # parameters for the query (once popping off the options if it is in there).  But this seems a bit tricky so for
    # now, kwargs override the corresponding value in the options, only.
    def test_simple_query_without_options_with_kwargs_positional_params(self):
        result = self.cluster.query("SELECT * FROM `beer-sample` WHERE brewery_id LIKE $1 LIMIT 1",
                                    positional_parameters=['21st_amendment%'])
        self.assertRows(result, 1)

    # NOTE: Ideally I'd notice that a named parameter wasn't an option parameter name, and just _assume_ that it is a
    # named parameter for the query.  However I worry about overlap being confusing, etc...
    def test_simple_query_without_options_with_kwargs_named_params(self):
        result = self.cluster.query("SELECT * FROM `beer-sample` WHERE brewery_id LIKE $brewery LIMIT 1",
                                    named_parameters={'brewery':'21st_amendment%'})
        self.assertRows(result, 1)

    def test_query_with_profile(self):
        result = self.cluster.query("SELECT * FROM `beer-sample` LIMIT 1", QueryOptions(profile=QueryProfile.TIMINGS))
        self.assertRows(result, 1)
        self.assertIsNotNone(result.metadata().profile())

    def test_query_with_metrics(self):
        initial = datetime.datetime.now()
        result = self.cluster.query("SELECT * FROM `beer-sample` LIMIT 1", QueryOptions(metrics=True))
        self.assertRows(result, 1)
        taken = datetime.datetime.now() - initial
        metadata = result.metadata()  # type: QueryMetaData
        metrics = metadata.metrics()
        self.assertIsInstance(metrics.elapsed_time(), datetime.timedelta)
        self.assertLess(metrics.elapsed_time(), taken)
        self.assertGreater(metrics.elapsed_time(), datetime.timedelta(milliseconds=0))
        self.assertLess(metrics.elapsed_time(), taken)
        self.assertGreater(metrics.execution_time(), datetime.timedelta(milliseconds=0))

        expected_counts = {metrics.mutation_count: 0,
                           metrics.result_count: 1,
                           metrics.sort_count: 0,
                           metrics.warning_count: 0}
        for method, expected in expected_counts.items():
            count_result = method()
            fail_msg = "{} failed".format(method)
            self.assertIsInstance(count_result, UnsignedInt64, msg=fail_msg)
            self.assertEqual(UnsignedInt64(expected), count_result, msg=fail_msg)
        self.assertGreater(metrics.result_size(), UnsignedInt64(500))

        self.assertEqual(UnsignedInt64(0), metrics.error_count())
        self.assertIsNone(metadata.profile())

    def test_query_metadata(self):
        result = self.cluster.query("SELECT * FROM `beer-sample` LIMIT 2")
        self.assertRows(result, 2)
        metadata = result.metadata()  # type: QueryMetaData
        for id_meth in (metadata.client_context_id,metadata.request_id):
            id_res = id_meth()
            fail_msg = "{} failed".format(id_meth)
            self.assertIsInstance(id_res, str, msg=fail_msg)
        self.assertEqual(QueryStatus.SUCCESS, metadata.status())
        self.assertIsInstance(metadata.signature(), (str, dict))
        self.assertIsInstance(metadata.warnings(), (list))
        for warning in metadata.warnings():
            self.assertIsInstance(warning, QueryWarning)
            self.assertIsInstance(warning.message, str)
            self.assertIsInstance(warning.code, int)

    def test_mixed_positional_parameters(self):
        # we assume that positional overrides one in the Options
        result = self.cluster.query("SELECT * FROM `beer-sample` WHERE brewery_id LIKE $1 LIMIT 1",
                                    QueryOptions(positional_parameters=['xgfflq']), '21st_am%')
        self.assertRows(result, 1)

    def test_mixed_named_parameters(self):
        result = self.cluster.query("SELECT * FROM `beer-sample` WHERE brewery_id LIKE $brewery LIMIT 1",
                                    QueryOptions(named_parameters={'brewery':'xxffqqlx'}), brewery='21st_am%')
        self.assertRows(result, 1)

    #import memory_profiler

    #@memory_profiler.profile()
    def test_no_leak(self):
        #raise SkipTest()
        import objgraph

        import tracemalloc
        tracemalloc.start()
        from couchbase.cluster import Cluster, ClusterOptions, QueryOptions, ClusterTimeoutOptions, QueryScanConsistency
        # timeout = 10
        # timeout_options = ClusterTimeoutOptions(kv_timeout=timeout,
        #                                         query_timeout=timeout)
        # options = ClusterOptions(authenticator=self.m)
        # cluster = Cluster(connection_string='couchbase://172.23.96.142', options=options)
        # bucket = cluster.bucket('bucket-1')
        # collection = bucket.scope('scope-1').collection('collection-1')
        import gc
        #gc.set_debug(gc.DEBUG_LEAK | gc.DEBUG_STATS)
        import objgraph
        doc = {'field1': "value1"}
        for i in range(100):
            key = str(i)
            self.bucket.upsert(key, doc, persist_to=0, replicate_to=0, ttl=0)

        statement = "SELECT * FROM default:`default` USE KEYS[$1];".format(self.cluster_info.bucket_name,self.coll._self_scope.name, self.coll._self_name)
        for j in range(10):
            for i in range(5):
                args = [str(i)]
                print("PRE : iteration {} key: {}".format(j, i))
                objgraph.show_growth(shortnames=False, limit=10)
                #query_opts = QueryOptions(adhoc=False, scan_consistency=QueryScanConsistency.NOT_BOUNDED, positional_parameters=args)
                result=self.cluster.query(statement, *args)#, query_opts)
                import weakref
                #res_weak=weakref.ref(result)
                #del query_opts
                class weaklist(list):
                    __slots__ = ('__weakref__',)
                stuff=weaklist(result)
                metadata=result.meta#.metadata()
                #del metadata
                #del result
                #result.raw.rows.append('fish')
                raw=weakref.ref(result)#.raw.rows[:1])#weaklist(result.raw.rows))

                result.raw.rows.clear()
                del result
                del metadata
                #del stuff
                gc.collect()
                print("POST: iteration {} key: {}".format(j, i))
                objgraph.show_growth(shortnames=False)
                value=raw()#res_weak()
                if value:
                    leaks=objgraph.get_leaking_objects(value)
                    count = 0
                    for entry in leaks:
                        if isinstance(entry, list):# and len(entry) and isinstance(entry[0],dict):
                            objgraph.show_chain(
                                objgraph.find_backref_chain(entry, objgraph.is_proper_module),
                                filename=str(BASEDIR.joinpath('ref_graphs','iter_{j}_{i}_leak_{count}_chain.png'.format(i=i, j=j,count=count))))
                            count+=1
                            if count>=10:
                                break
                #referents=gc.get_referents(value)
                #referers=gc.get_referrers(value)

                #print("""{} referents = {}
                #{} referrers = {} """.format(value, referents, value, referers))
                #try:
                #    leaking=objgraph.get_leaking_objects(value)
                #    print(len(leaking))
                #except Exception as e:
                #    raise
            snapshot=tracemalloc.take_snapshot()
            #tracemalloc.get_traced_memory()
            for x, stat in enumerate(snapshot.statistics('filename')[:5], 1):
                import logging
                print("top_current {x}: {stat}".format(x = x, stat = str(stat)))
            print("End of iteration {}\n".format(j))
            gc.collect()
        self.gen_obj_graph(self.cluster,'self.cluster','ref_graphs')
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
#
from couchbase_tests.base import CollectionTestCase, SkipTest
from couchbase.management.analytics import CreateDatasetOptions, DropDatasetOptions
from couchbase.analytics import AnalyticsOptions


class AnalyticsTestCase(CollectionTestCase):

    def setUp(self):
        self.realSetUp()
        if self.is_mock:
            raise SkipTest("analytics not mocked")
        if int(self.get_cluster_version().split('.')[0]) < 6:
            raise SkipTest("no analytics in {}".format(self.get_cluster_version()))
        self.mgr = self.cluster.analytics_indexes()
        self.dataset_name = 'test_beer_dataset'
        # create a dataset to query
        self.mgr.create_dataset(self.dataset_name, 'beer-sample', CreateDatasetOptions(ignore_if_exists=True))
        def has_dataset(name):
            datasets = self.mgr.get_all_datasets()
            return [d for d in datasets if d.dataset_name == name][0]
        def on_dataset(*args, **kwargs):
            return self.mgr.connect_link()

        self.try_n_times(10, 3, has_dataset, self.dataset_name, on_success=on_dataset)
        # connect it...


    def realSetUp(self):
        super(AnalyticsTestCase, self).setUp()

    def tearDown(self):
        self.try_n_times(10, 3, self.mgr.disconnect_link)
        self.mgr.drop_dataset(self.dataset_name, DropDatasetOptions(ignore_if_not_exists=True))

    def assertQueryReturnsRows(self, query, *options, **kwargs):
        result = self.cluster.analytics_query(query, *options, **kwargs)
        def verify_rows(actual_result):
            rows = actual_result.rows()
            if len(rows) > 0:
                return rows
            raise Exception("no rows in result")
        return self.checkResult(result, verify_rows)

    def assertRows(self, response):
        for r in response:
            if r:
                return
        self.fail("No rows in result!")

    def checkResult(self, result, callback):
        return callback(result)

    def test_simple_query(self):
        return self.try_n_times(10, 3, self.assertQueryReturnsRows, "SELECT * FROM `{}` LIMIT 1".format(self.dataset_name))

    def test_query_positional_params(self):
        rows = self.try_n_times(10, 3, self.assertQueryReturnsRows,
                                'SELECT * FROM `{}` WHERE `type` = $1 LIMIT 1'.format(self.dataset_name),
                                AnalyticsOptions(positional_parameters=["brewery"]))
        print(rows)
        return self.checkResult(rows, lambda result:  self.assertEqual("brewery", result[0][self.dataset_name]['type']))


    def test_query_positional_params_no_option(self):
        rows = self.try_n_times(10, 3, self.assertQueryReturnsRows,
                                'SELECT * FROM `{}` WHERE `type` = $1 LIMIT 1'.format(self.dataset_name),
                                "brewery")
        return self.checkResult(rows, lambda result: self.assertEqual("brewery", result[0][self.dataset_name]['type']))

    def test_query_positional_params_override(self):
        rows = self.try_n_times(10, 3, self.assertQueryReturnsRows,
                                'SELECT * FROM `{}` WHERE `type` = $1 LIMIT 1'.format(self.dataset_name),
                                AnalyticsOptions(positional_parameters=["jfjfjfjfjfj"]),
                                "brewery")
        return self.checkResult(rows, lambda result: self.assertEqual("brewery", result[0][self.dataset_name]['type']))

    @staticmethod
    def _on_success(result, *args, **kwargs):
        return result
    def _fail(self, message):
        self.fail(message)
    def _success(self):
        return True
    def test_query_named_parameters(self):
        def verify(result, *args, **kwargs):
            try:
                self.assertEqual("brewery", result[0][self.dataset_name]['type'])
                return self._success()
            except Exception as e:
                return self._fail(str(e))
        rows = self.try_n_times(10, 3, self.assertQueryReturnsRows,
                                "SELECT * FROM `{}` WHERE `type` = $btype LIMIT 1".format(self.dataset_name),
                                AnalyticsOptions(named_parameters={"btype": "brewery"}))
        return self.checkResult(rows, verify)

    def test_query_named_parameters_no_options(self):
        rows = self.try_n_times(10, 3, self.assertQueryReturnsRows,
                                "SELECT * FROM `{}` WHERE `type` = $btype LIMIT 1".format(self.dataset_name),
                                btype="brewery")
        return self.checkResult(rows, lambda result: self.assertEqual("brewery", rows[0][self.dataset_name]['type']))

    def test_query_named_parameters_override(self):
        rows = self.try_n_times(10, 3, self.assertQueryReturnsRows,
                                "SELECT * FROM `{}` WHERE `type` = $btype LIMIT 1".format(self.dataset_name),
                                AnalyticsOptions(named_parameters={"btype": "jfjfjfjf"}),
                                btype="brewery")
        return self.checkResult(rows, lambda result: self.assertEqual("brewery", result[0][self.dataset_name]['type']))




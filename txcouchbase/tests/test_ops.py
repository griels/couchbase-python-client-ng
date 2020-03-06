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
from unittest import SkipTest

from couchbase_tests.base import ConnectionTestCase

from txcouchbase.tests.base import gen_base
from couchbase_core.exceptions import NotFoundError
from couchbase_core.result import (
    OperationResult, ValueResult)

Base=gen_base(ConnectionTestCase)



class OperationTestCase(Base):
    def testSimpleSet(self):
        cb = self.make_connection()
        key = self.gen_key("test_simple_set")
        d = cb.upsert(key, "simple_Value")
        def t(ret):
            self.assertIsInstance(ret, OperationResult)
            self.assertEqual(ret.key, key)
            del ret

        d.addCallback(t)
        del cb
        return d

    def testSimpleGet(self):
        raise SkipTest("fix async wrapper")
        cb = self.make_connection()
        key = self.gen_key("test_simple_get")
        value = "simple_value"

        cb.upsert(key, value)
        d_get = cb.get(key)
        def t(ret):
            self.assertIsInstance(ret, ValueResult)
            self.assertEqual(ret.key, key)
            self.assertEqual(ret.value, value)

        d_get.addCallback(t)
        return d_get

    def testMultiSet(self):
        raise SkipTest("Fix multi async results")
        cb = self.make_connection()
        kvs = self.gen_kv_dict(prefix="test_multi_set")
        d_set = cb.upsertMulti(kvs)

        def t(ret):
            self.assertEqual(len(ret), len(kvs))
            self.assertEqual(ret.keys(), kvs.keys())
            self.assertTrue(ret.all_ok)
            for k in kvs:
                self.assertEqual(ret[k].key, k)
                self.assertTrue(ret[k].success)

            del ret

        d_set.addCallback(t)
        return d_set

    def testSingleError(self):
        raise SkipTest("fix async result")
        cb = self.make_connection()
        key = self.gen_key("test_single_error")

        d_del = cb.remove(key, quiet=True)

        d = cb.get(key, quiet=False)
        def t(err):
            self.assertIsInstance(err.value, NotFoundError)
            return True

        d.addCallback(lambda x: self.assertTrue(False))
        d.addErrback(t)
        return d

    def testMultiErrors(self  # type: Base
                        ):
        raise SkipTest("Fix async multiresults")
        cb = self.make_connection()
        kv = self.gen_kv_dict(prefix = "test_multi_errors")
        cb.upsertMulti(kv)

        rmkey = list(kv.keys())[0]
        cb.remove(rmkey)

        d = cb.getMulti(kv.keys())

        def t(err):
            self.assertIsInstance(err.value, NotFoundError)
            all_results = err.value.all_results
            for k, v in kv.items():
                self.assertTrue(k in all_results)
                res = all_results[k]
                self.assertEqual(res.key, k)
                if k != rmkey:
                    self.assertTrue(res.success)
                    self.assertEqual(res.value, v)

            res_fail = err.value.result
            self.assertFalse(res_fail.success)
            self.assertTrue(NotFoundError._can_derive(res_fail.rc))

        d.addErrback(t)
        return d

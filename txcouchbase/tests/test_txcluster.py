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
import sys
from unittest import SkipTest

from nose.tools import timed
from twisted.internet import defer

from couchbase.exceptions import (
    ObjectDestroyedException)
from couchbase.exceptions import UnknownHostException
from couchbase_core.connstr import ConnectionString
from couchbase_tests.base import AsyncClusterTestCase
from txcouchbase.cluster import TxBucket, TxCluster
from txcouchbase.tests.base import gen_base

Base = gen_base(AsyncClusterTestCase)


class BasicClusterTest(Base):
    def __init__(self, *args, **kwargs):
        super(BasicClusterTest, self).__init__(*args, **kwargs)

    @property
    def factory(self):
        return self.gen_cluster

    def testConnectionSuccess(self):
        raise SkipTest("To be fixed")
        cb = self.make_connection()
        d = cb.on_connect()
        d.addCallback(lambda x: self.assertTrue(cb.connected))
        return d

    def testConnectionFailure(self  # type: Base
                              ):
        cb = self.make_connection(host="qweqwe")
        d = cb.on_connect()
        d.addCallback(lambda x: x, cb)
        return self.assertFailure(d, UnknownHostException)

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
        raise SkipTest("To be fixed")
        info = self.cluster_info
        cs = ConnectionString.parse(self.make_connargs()['connection_string'])
        cs.hosts = [ info.host + ':' + '10', info.host + ':' + str(info.port) ]
        cb = self.make_connection(connection_string=cs.encode())
        d = cb.on_connect()
        d.addCallback(lambda x: self.assertTrue(cb.connected))
        return d

    def testConnstrFirstArg(self  # type: BasicClusterTest
                            ):
        raise SkipTest("To be reenabled if still relevant")
        info = self.cluster_info
        s = self.make_connargs()['connection_string']
        mock_options=self.cluster_info.mock_hack_options(self.is_mock)
        s=ConnectionString(s)
        s.bucket=None
        cb = TxCluster(connection_string=s,authenticator=mock_options.auth(self.cluster_info.admin_username, self.cluster_info.admin_password), **mock_options.kwargs)
        d = cb.on_connect().addCallback(lambda x: self.assertTrue(cb.connected))
        self.register_cleanup(cb)
        return d

    def testConnectionDestroyed(self):
        raise SkipTest("TODO: fix")
        cb = self.make_connection()
        d = cb.on_connect()
        self.assertFailure(d, ObjectDestroyedException)
        return d

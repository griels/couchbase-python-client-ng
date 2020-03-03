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
from twisted.internet import defer
from couchbase_core.exceptions import (
    BucketNotFoundError,
    ObjectDestroyedError)

from couchbase_tests.base import ConnectionTestCase
from couchbase_core.connstr import ConnectionString
from txcouchbase.tests.base import gen_base
from txcouchbase.bucket import TxBucket
from nose.tools import timed
import sys
from unittest import SkipTest


Base = gen_base(ConnectionTestCase)  # type: ConnectionTestCase


class BasicConnectionTest(Base):
    def __init__(self, *args, **kwargs):
        super(BasicConnectionTest,self).__init__(*args,**kwargs)

    def testConnectionSuccess(self):
        cb = self.make_connection()
        d = cb.connect()
        d.addCallback(lambda x: self.assertTrue(cb.connected))
        return d

    def testConnectionFailure(self  # type: Base
                              ):
        cb = self.make_connection(bucket='blahblah')
        d = cb.connect()
        d.addCallback(lambda x: x, cb)
        return self.assertFailure(d, BucketNotFoundError)

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
        d = cb.connect()
        d.addCallback(lambda x: self.assertTrue(cb.connected))
        return d

    def testConnstrFirstArg(self):
        info = self.cluster_info
        s = self.make_connargs()['connection_string']
        cb = TxBucket(s)
        d = cb.connect().addCallback(lambda x: self.assertTrue(cb.connected))
        self.register_cleanup(cb)
        return d

    def testConnectionDestroyed(self):
        cb = self.make_connection()
        d = cb.connect()
        self.assertFailure(d, ObjectDestroyedError)
        return d

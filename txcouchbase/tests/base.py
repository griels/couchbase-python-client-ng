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
from twisted.trial.unittest import TestCase

from txcouchbase.bucket import V2Bucket
from couchbase_tests.base import ConnectionTestCase
from twisted.protocols import policies

import twisted.internet.base

twisted.internet.base.DelayedCall.debug = True
import sys


def gen_base(basecls, timeout=10):
    class _TxTestCase(basecls, TestCase):
        def register_cleanup(self, obj):
            d = defer.Deferred()
            obj.registerDeferred('_dtor', d)
            self.addCleanup(lambda x: d, None)

            # Add another callback (invoked _outside_ of C) to ensure
            # the instance's destroy function is properly triggered
            if hasattr(obj, '_async_shutdown'):
                self.addCleanup(obj._async_shutdown)

        def make_connection(self, **kwargs):
            ret = super(_TxTestCase, self).make_connection(**kwargs)
            self.register_cleanup(ret)
            return ret

        def checkCbRefcount(self):
            pass

        @property
        def factory(self):
            return V2Bucket

        def setUp(self):
            super(_TxTestCase, self).setUp()
            self.cb = None

        def tearDown(self):
            super(_TxTestCase, self).tearDown()

    if timeout and sys.version_info < (3, 7):
        class _TxTimeOut(_TxTestCase, policies.TimeoutMixin):
            def __init__(self, *args, **kwargs):
                super(_TxTestCase, self).__init__(*args, **kwargs)
                self.setTimeout(timeout)

            def timeoutConnection(self):
                """
                Called when the connection times out.

                Override to define behavior other than dropping the connection.
                """
                raise TimeoutError("Timed out")
        return _TxTimeOut

    return _TxTestCase

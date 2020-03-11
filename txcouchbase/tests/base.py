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

from couchbase_tests.base import CouchbaseTestCase
from couchbase_core.client import Client
import twisted.internet.base
twisted.internet.base.DelayedCall.debug = True
from typing import *
T = TypeVar('T', bound=CouchbaseTestCase)
Factory = Callable[[Any],Client]

from txcouchbase.bucket import TxBucket


def gen_collection(*args, **kwargs):
    try:
        if args:
            connstr=args[0]
        else:
            connstr=kwargs.pop('connection_string')
        base_bucket = TxBucket(*args, connection_string = connstr, **kwargs)

        return base_bucket.default_collection()
    except Exception as e:
        raise


def gen_base(basecls,  # type: Type[T]
             timeout=5,
             factory=gen_collection  # type: Factory
             ):
    # type: (...) -> Type[Union[T,CouchbaseTestCase]]
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
            # type: (...) -> Factory
            ret = super(_TxTestCase, self).make_connection(**kwargs)
            self.register_cleanup(ret)
            return ret

        def checkCbRefcount(self):
            pass

        @property
        def factory(self):
            return factory

        def setUp(self):
            super(_TxTestCase, self).setUp()
            self.cb = None

        def tearDown(self):
            super(_TxTestCase, self).tearDown()

        @classmethod
        def setUpClass(cls) -> None:
            import inspect
            if timeout:
                for name, method in inspect.getmembers(cls,inspect.isfunction):
                    try:
                        print("Setting {} timeout to 10 secs".format(name))
                        getattr(cls,name).timeout=timeout
                    except Exception as e:
                        print(e)

    return _TxTestCase

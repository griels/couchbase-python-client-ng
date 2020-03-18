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
import twisted.internet.base
from twisted.internet import defer
from twisted.trial.unittest import TestCase

from couchbase_core.client import Client
from couchbase_tests.base import ConnectionTestCase

twisted.internet.base.DelayedCall.debug = True
from typing import *

from txcouchbase.bucket import TxCluster
from couchbase_core.cluster import ClassicAuthenticator
from couchbase_core.connstr import ConnectionString

T = TypeVar('T', bound=ConnectionTestCase)
Factory = Callable[[Any],Client]


class _TxTestCase(TestCase):
    def register_cleanup(self, obj):
        d = defer.Deferred()
        obj.registerDeferred('_dtor', d)
        self.addCleanup(lambda x: d, None)

        # Add another callback (invoked _outside_ of C) to ensure
        # the instance's destroy function is properly triggered
        if hasattr(obj, '_async_shutdown'):
            self.addCleanup(obj._async_shutdown)

    def make_connection(self,  # type: _TxTestCase
                        **kwargs):
        # type: (...) -> Factory
        ret = super(_TxTestCase, self).make_connection(**kwargs)
        self.register_cleanup(ret)
        return ret

    def checkCbRefcount(self):
        pass

    def gen_cluster(self,  # type: _TxTestCase
                    *args,
                    **kwargs):
        # type: (...) -> TxCluster
        args=list(args)
        connstr_nobucket, bucket = self._get_connstr_and_bucket_name(args, kwargs)
        return self.gen_cluster_raw(connstr_nobucket, **kwargs)

    def gen_cluster_raw(self, connstr_nobucket, **kwargs):
        return TxCluster(connection_string=str(connstr_nobucket),
                         authenticator=ClassicAuthenticator(self.cluster_info.admin_username,
                                                            self.cluster_info.admin_password), **kwargs)

    def _get_connstr_and_bucket_name(self,
                                     args,  # type: List[Any]
                                     kwargs):
        connstr = args.pop(0) if args else kwargs.pop('connection_string')
        connstr_nobucket = ConnectionString.parse(connstr)
        bucket=connstr_nobucket.bucket
        connstr_nobucket.bucket = None
        return connstr_nobucket, bucket

    def gen_collection(self,
                       *args, **kwargs):
        bucket_result = self.gen_bucket(args, kwargs)
        return bucket_result.default_collection()

    def gen_bucket(self, args, kwargs):
        args = list(args)
        connstr_nobucket, bucket = self._get_connstr_and_bucket_name(args, kwargs)
        return self.gen_cluster_raw(connstr_nobucket, **kwargs).bucket(bucket)

    @property
    def factory(self):
        return type(self)._factory() or self.gen_collection

    def setUp(self):
        super(_TxTestCase, self).setUp()
        self.cb = None

    def tearDown(self):
        super(_TxTestCase, self).tearDown()

    @classmethod
    def setUpClass(cls) -> None:
        import inspect
        if cls.timeout:
            for name, method in inspect.getmembers(cls,inspect.isfunction):
                try:
                    print("Setting {} timeout to 10 secs".format(name))
                    getattr(cls,name).timeout=cls.timeout
                except Exception as e:
                    print(e)


def gen_base(basecls,  # type: Type[T]
             timeout_specific=5,
             factory=None  # type: Factory
             ):
    # type: (...) -> Union[Type[_TxTestCase],Type[T]]
    class _TxTestCaseSpecific(_TxTestCase, basecls):
        @classmethod
        def timeout(cls):
            return timeout_specific

        @classmethod
        def _factory(cls):
            return factory
    return _TxTestCaseSpecific

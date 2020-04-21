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
import os
import sys
from typing import *

import twisted.internet.base
import twisted.python.util
from twisted.internet import defer
from twisted.trial.unittest import TestCase

from couchbase_core.client import Client
from couchbase_tests.base import ClusterTestCase
from txcouchbase.cluster import TxCluster

T = TypeVar('T', bound=ClusterTestCase)
Factory = Callable[[Any], Client]
twisted.internet.base.DelayedCall.debug = True

import logging
import re



def logged_spewer(frame, s, ignored):
    """
    A trace function for sys.settrace that prints every function or method call.
    """
    from twisted.python import reflect
    try:
        if 'self' in frame.f_locals:
            se = frame.f_locals['self']
            if hasattr(se, '__class__'):
                k = reflect.qual(se.__class__)
            else:
                k = reflect.qual(type(se))
            logging.info('method %s of %s at %s' % (
                frame.f_code.co_name, k, id(se)))
        else:
            logging.info('function %s in %s, line %s' % (
                frame.f_code.co_name,
                frame.f_code.co_filename,
                frame.f_lineno))
    except:
        pass

candidate_pattern=re.compile(r'.*(twisted|tx|couchbase).*')
def validate_frame(frame, s):
    co_name = frame.f_code.co_name
    co_filename = frame.f_code.co_filename
    return candidate_pattern.match(co_filename)

def magicmethod(clazz, method):
    if method not in clazz.__dict__:  # Not defined in clazz : inherited
        return 'inherited'
    elif hasattr(super(clazz), method):  # Present in parent : overloaded
        return 'overloaded'
    else:  # Not present in parent : newly defined
        return 'newly defined'

def logged_spewer(frame, s, ignored):
    """
    A trace function for sys.settrace that prints every function or method call.
    """
    from twisted.python import reflect
    try:
        co_name = frame.f_code.co_name
        co_filename = frame.f_code.co_filename

        if not validate_frame(frame, s):
            return
        if 'self' in frame.f_locals:
            se = frame.f_locals['self']
            if hasattr(se, '__class__'):
                clazz = se.__class__
            else:
                clazz = type(se)
            k = reflect.qual(clazz)
            #logging.info("Getting qualified name of {}".format(clazz))
            qualname=str(clazz)#getattr(clazz, '__qualname__', None)
            #logging.info("Got qualified name of {}, {}".format(clazz, qualname))
            if qualname and not candidate_pattern.match(qualname):
                return
            if magicmethod(clazz,co_name) in ('inherited',):
                return
            logging.info('method %s.%s at %s' % (
                k, co_name, id(se)))
        else:
            logging.info('function %s in %s, line %s' % (
                co_name,
                co_filename,
                frame.f_lineno))
    except:
        pass


def gen_base(basecls,  # type: Type[T]
             timeout=5,
             factory=None  # type: Factory
             ):
    # type: (...) -> Union[Type[_TxTestCase],Type[T]]
    class _TxTestCase(basecls, TestCase):
        def make_connection(self,  # type: _TxTestCase
                            **kwargs):
            # type: (...) -> Factory
            ret = super(_TxTestCase, self).make_connection(**kwargs)
            self.register_cleanup(ret)
            return ret

        def register_cleanup(self, obj):
            d = defer.Deferred()
            try:
                obj.registerDeferred('_dtor', d)
            except Exception as e:
                raise
            def cleanup(*args, **kwargs):
                return d, None
            self.addCleanup(cleanup)

            # Add another callback (invoked _outside_ of C) to ensure
            # the instance's destroy function is properly triggered
            if hasattr(obj, '_async_shutdown'):
                self.addCleanup(obj._async_shutdown)

        def checkCbRefcount(self):
            pass

        @property
        def cluster_class(self):
            return TxCluster

        @property
        def factory(self):
            return factory or self.gen_collection

        def setUp(self):
            if os.getenv("PYCBC_DEBUG_SPEWER"):
                # enable very detailed call logging
                self._oldtrace=sys.gettrace()
                sys.settrace(logged_spewer)
            if os.getenv("PYCBC_DEBUG_SPEWER"):
                # enable very detailed call logging
                self._oldtrace=sys.gettrace()
                sys.settrace(logged_spewer)

            super(_TxTestCase, self).setUp()
            self.cb = None

        def tearDown(self):
            super(_TxTestCase, self).tearDown()
            oldtrace = getattr(self, '_oldtrace', None)
            if oldtrace:
                sys.settrace(oldtrace)
            oldtrace=getattr(self, '_oldtrace', None)
            if oldtrace:
                sys.settrace(oldtrace)

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

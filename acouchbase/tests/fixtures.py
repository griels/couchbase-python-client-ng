import unittest

from couchbase_tests.base import ConnectionConfiguration, MockResourceManager, MockTestCase
from functools import wraps
from parameterized import parameterized_class
import os
from couchbase_core import abstractmethod
from collections import namedtuple

Details=namedtuple('Details',['factory','get_value'])

try:
    from acouchbase.bucket import V3Bucket
    from acouchbase.bucket import Bucket, V3CoreBucket
    from acouchbase.bucket import asyncio


    def asynct(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            future = f(*args, **kwargs)
            loop = asyncio.get_event_loop()
            loop.run_until_complete(future)

        return wrapper

    def gen_collection(*args, **kwargs):
        try:
            base_bucket=V3Bucket(*args, **kwargs)
            return base_bucket.default_collection()
        except Exception as e:
            raise


    target_dict = {'Bucket': Details(Bucket,lambda x: x.value), 'V3CoreBucket': Details(V3CoreBucket, lambda x:x.value)}
    collections = os.getenv("PYCBC_TEST_COLLECTIONS_ASYNC") or True
    if collections:
        target_dict.update({'Collection': Details(gen_collection,lambda x:x.content)})

    targets = list(map(lambda x: (x,), target_dict.keys()))
except (ImportError, SyntaxError):
    target_dict = {}


def parameterize_asyncio(cls):
    return parameterized_class(('factory_name',), targets)(cls)


class AioTestCase(MockTestCase):
    factory_name = None  # type: str

    def __init__(self, *args, **kwargs):
        self.details = target_dict[self.factory_name]
        super(AioTestCase, self).__init__(*args, **kwargs)

    @property
    def factory(self):
        return self.details.factory
    should_check_refcount = False
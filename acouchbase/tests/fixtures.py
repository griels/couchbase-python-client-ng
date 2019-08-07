import unittest

from couchbase_tests.base import ConnectionConfiguration, MockResourceManager, MockTestCase
from functools import wraps
from parameterized import parameterized_class
import os




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
        return V3Bucket(*args, **kwargs).default_collection()


    target_dict = {'Bucket': Bucket, 'V3CoreBucket': V3CoreBucket}
    collections = os.getenv("PYCBC_TEST_COLLECTIONS_ASYNC") or False
    if collections:
        target_dict.update({'Collection': gen_collection})

    targets = list(map(lambda x: (x,), target_dict.keys()))
except (ImportError, SyntaxError):
    target_dict = {}


def parameterize_asyncio(cls):
    return parameterized_class(('factory_name',), targets)(cls)


class AioTestCase(MockTestCase):
    factory_name = None  # type: str

    def __init__(self, *args, **kwargs):
        self.factory = target_dict[self.factory_name]
        super(AioTestCase, self).__init__(*args, **kwargs)

    should_check_refcount = False
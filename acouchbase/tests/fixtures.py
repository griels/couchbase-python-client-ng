import asyncio
import unittest

from couchbase_tests.base import ConnectionConfiguration, MockResourceManager, MockTestCase
from acouchbase.bucket import Bucket, V3AIOBucket

from functools import wraps


def asynct(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        future = f(*args, **kwargs)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(future)

    return wrapper

class AioTestCase(MockTestCase):
    @staticmethod
    def gen_collection(*args,**kwargs):
        return V3AIOBucket(*args,**kwargs).default_collection()
    factory = Bucket
    should_check_refcount = False

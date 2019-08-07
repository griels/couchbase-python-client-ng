import asyncio
import unittest

from couchbase_tests.base import ConnectionConfiguration, MockResourceManager, MockTestCase
from acouchbase.bucket import Bucket

from functools import wraps
from acouchbase.bucket import V3Bucket

def asynct(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        future = f(*args, **kwargs)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(future)

    return wrapper

class AioTestCase(MockTestCase):
    @staticmethod
    def gen_collection(*args, **kwargs):
        return V3Bucket(*args,**kwargs).default_collection()
    factory = gen_collection if False else Bucket
    should_check_refcount = False

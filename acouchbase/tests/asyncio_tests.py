# SyntaxError will trigger if yield or async is not supported
# ImportError will fail for python 3.3 because asyncio does not exist

import logging, traceback
from .fixtures import parameterize_asyncio

try:
    import acouchbase.tests.py34only
    @parameterize_asyncio
    class CouchbaseBeerCollectionTestSpecific(acouchbase.tests.py34only.CouchbaseBeerCollectionTest):
        pass
    @parameterize_asyncio
    class CouchbaseBeerBucketTestSpecific(acouchbase.tests.py34only.CouchbaseBeerBucketTest):
        pass

    @parameterize_asyncio
    class CouchbaseDefaultTestSpecific(acouchbase.tests.py34only.CouchbaseDefaultTest):
        pass
except (ImportError, SyntaxError) as e:
    logging.error("Got exception {}".format(traceback.format_exc()))

try:
    import acouchbase.tests.py35only
    @parameterize_asyncio
    class CouchbasePy35TestSpecific(acouchbase.tests.py35only.CouchbasePy35Test):
        pass
except (ImportError, SyntaxError) as e:
    logging.error("Got exception {}".format(traceback.format_exc()))

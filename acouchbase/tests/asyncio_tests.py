# SyntaxError will trigger if yield or async is not supported
# ImportError will fail for python 3.3 because asyncio does not exist

import logging, traceback
try:
    from acouchbase.tests.py34only import CouchbaseBeerTest, CouchbaseDefaultTest
except (ImportError, SyntaxError) as e:
    logging.error("Got exception {}".format(traceback.format_exc()))

try:
    from acouchbase.tests.py35only import CouchbasePy35Test
except (ImportError, SyntaxError) as e:
    logging.error("Got exception {}".format(traceback.format_exc()))

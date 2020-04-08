# SyntaxError will trigger if yield or async is not supported
# ImportError will fail for python 3.3 because asyncio does not exist

import logging, traceback


import acouchbase.tests.py34only
class CouchbaseBeerKVTestSpecific(acouchbase.tests.py34only.CouchbaseBeerKVTest):
    pass

class CouchbaseDefaultTestSpecificN1QL(acouchbase.tests.py34only.CouchbaseDefaultTestN1QL):
    pass


logging.error("Got exception {}".format(traceback.format_exc()))

try:
    import acouchbase.tests.py35only
    class CouchbasePy35TestSpecific(acouchbase.tests.py35only.CouchbasePy35Test):
        pass
except (ImportError, SyntaxError) as e:
    logging.error("Got exception {}".format(traceback.format_exc()))

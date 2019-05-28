import couchbase_v2.tests.cases
import couchbase_v3.tests.cases
import sys
sys.modules['couchbase_tests.cases.v2']=couchbase_v2.tests.cases
sys.modules['couchbase_tests.cases.v3']=couchbase_v3.tests.cases

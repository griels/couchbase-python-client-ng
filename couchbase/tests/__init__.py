from couchbase_tests import caseslist

import couchbase.tests_v3.cases as latest_cases
import acouchbase as acouchbase_tests
import txcouchbase.tests as txcouchbase_tests
import couchbase_v2.tests as v2_tests

caseslist += [latest_cases, acouchbase_tests, txcouchbase_tests, v2_tests]
import couchbase_tests.test_sync as test_sync

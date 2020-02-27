from couchbase_tests import caseslist

import couchbase_v2.tests.cases

caseslist += [couchbase_v2.tests.cases]

import couchbase.tests_v3.cases as latest_cases
import acouchbase as acouchbase_tests
import txcouchbase.tests as txcouchbase_tests
import gcouchbase.tests as gcouchbase_test

caseslist += [latest_cases, acouchbase_tests, txcouchbase_tests, gcouchbase_test]
import couchbase_tests.test_sync as test_sync

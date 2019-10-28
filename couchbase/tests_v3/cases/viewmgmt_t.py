from couchbase.management.queries import QueryIndex
from couchbase.management.views import DesignDocumentNamespace, DesignDocument
from typing import *

0#
# Copyright 2013, Couchbase, Inc.
# All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from nose.plugins.attrib import attr

from couchbase_tests.base import DDocTestCase, ClusterTestCase
from couchbase.exceptions import HTTPError

DNAME = "tmp"
VNAME = "a_view"

DESIGN_JSON = {
    'language' : 'javascript',
    'views' : {
        VNAME : {
            'map' : "function(doc) { emit(null,null); }"
        }
    }
}

DOCUMENT_FROM_JSON = DesignDocument.from_json(name=DNAME, **DESIGN_JSON)


@attr('slow')
class DesignDocManagementTest(ClusterTestCase):
    def setUp(self):
        super(DesignDocManagementTest, self).setUp()
        self.skipIfMock()
        self.mgr = self.bucket.views()

        try:
            self.mgr.drop_design_document(DNAME, DesignDocumentNamespace.PRODUCTION, syncwait=5)
        except HTTPError:
            pass

        try:
            self.mgr.drop_design_document(DNAME, DesignDocumentNamespace.DEVELOPMENT, syncwait=5)
        except HTTPError:
            pass
        self.cb = self.bucket

    def tearDown(self):
        del self.mgr
        super(DesignDocManagementTest, self).tearDown()

    def test_design_management(self):
        self.mgr.upsert_design_document(DOCUMENT_FROM_JSON, DesignDocumentNamespace.DEVELOPMENT, syncwait=5)

        rv = self.bucket.view_query(DNAME, VNAME, use_devmode=True,
                           limit=10)
        print(list(rv))
        self.assertTrue(rv.success)
        self.mgr.drop_design_document(DNAME, DesignDocumentNamespace.DEVELOPMENT)
        import time
        time.sleep(1)
        self.mgr.upsert_design_document(DOCUMENT_FROM_JSON, DesignDocumentNamespace.PRODUCTION, syncwait=5)

        rv = self.bucket.view_query(DNAME, VNAME,
                           limit=10)
        print(list(rv))
        self.assertTrue(rv.success)

        self.assertRaises(HTTPError,
                          self.cb.view_query,
                          DNAME, VNAME,
                          use_devmode=True)

        rv = self.mgr.design_delete(DNAME, use_devmode=False, syncwait=5)
        self.assertTrue(rv.success)

        self.assertRaises(HTTPError,
                          self.cb._view,
                          DNAME, VNAME,
                          use_devmode=False)

    def test_design_headers(self):
        rv = self.mgr.upsert_design_document(DOCUMENT_FROM_JSON, DesignDocumentNamespace.DEVELOPMENT,
                                   syncwait=5)

        rv = self.mgr.get_design_document(DNAME, DesignDocumentNamespace.DEVELOPMENT)
        self.assertTrue(rv.language)
        print(rv.language)
        #self.assertTrue('X-Couchbase-Meta' in rv.headers)

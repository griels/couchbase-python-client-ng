from couchbase_tests.base import ClusterTestCase


class SearchManagementTest(ClusterTestCase):
    def setUp(self, **kwargs):
        super(SearchManagementTest,self).setUp(**kwargs)
        self.sm=self.cluster.
    def test_get_index(self):
        assert False

    def test_get_all_indexes(self):
        assert False

    def test_upsert_index(self):
        assert False

    def test_drop_index(self):
        assert False

    def test_get_indexed_documents_count(self):
        assert False

    def test_pause_ingest(self):
        assert False

    def test_resume_ingest(self):
        assert False

    def test_allow_querying(self):
        assert False

    def test_disallow_querying(self):
        assert False

    def test_freeze_plan(self):
        assert False

    def test_unfreeze_plan(self):
        assert False

    def test_analyze_document(self):
        assert False

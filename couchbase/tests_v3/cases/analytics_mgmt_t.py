from unittest import SkipTest

from couchbase_tests.base import ClusterTestCase


class AnalyticsIndexTest(ClusterTestCase):
    def setUp(self, **kwargs):
        super(AnalyticsIndexTest,self).setUp(**kwargs)
        self.mgr=self.cluster.analytics_indexes()
        self.dataverse_name=self.gen_key()
        self.mgr.create_dataverse(self.dataverse_name)

    def tearDown(self):
        try:
            self.mgr.drop_dataverse(self.dataverse_name)
        except:
            pass

    def test_create_dataverse(self):
        extraverse=self.dataverse_name+"_extra"
        self.mgr.create_dataverse(extraverse)
        self.mgr.create_dataverse(extraverse)
        #self.assertRaises(Exception,self.mgr.create_dataverse,extraverse)

    def test_drop_dataverse(self):
        raise SkipTest("to be implemented")

    def test_create_dataset(self):
        raise SkipTest("to be implemented")

    def test_drop_dataset(self):
        raise SkipTest("to be implemented")

    def test_get_all_datasets(self):
        raise SkipTest("to be implemented")

    def test_create_index(self):
        raise SkipTest("to be implemented")

    def test_drop_index(self):
        raise SkipTest("to be implemented")

    def test_get_all_indexes(self):
        raise SkipTest("to be implemented")

    def test_connect_link(self):
        raise SkipTest("to be implemented")

    def test_disconnect_link(self):
        raise SkipTest("to be implemented")

    def test_get_pending_mutations(self):
        raise SkipTest("to be implemented")

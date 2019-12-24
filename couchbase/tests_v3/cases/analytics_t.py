from hypothesis_auto import auto_test, auto_pytest_magic
from hypothesis_auto import auto_pytest_magic, auto_pytest

from couchbase_tests.base import ClusterTestCase

from couchbase.management.analytics import AnalyticsIndexManager
from hypothesis_auto import Scenario, auto_pytest

class AnalyticsTest(ClusterTestCase):
    def setUp(self, **kwargs):
        super(AnalyticsTest,self).setUp(**kwargs)
        self.ai=self.cluster.analytics_indexes()
    @staticmethod
    def my_custom_verifier(scenario, *args, **kwargs):
        pass

def genTestCase():
    # type: (...)->AnalyticsTest
    x=AnalyticsTest()
    x.setUp()
    return x

@auto_pytest(genTestCase().ai.create_dataverse)
def test_stuff(test_case, *args, **kwargs):
    pass
    #
    #
    # def test_create_dataverse(self):
    #     assert False
    #
    # def test_drop_dataverse(self):
    #     assert False
    #
    # def test_create_dataset(self):
    #     assert False
    #
    # def test_drop_dataset(self):
    #     assert False
    #
    # def test_get_all_datasets(self):
    #     assert False
    #
    # def test_create_index(self):
    #     assert False
    #
    # def test_drop_index(self):
    #     assert False
    #
    # def test_get_all_indexes(self):
    #     assert False
    #
    # def test_connect_link(self):
    #     assert False
    #
    # def test_disconnect_link(self):
    #     assert False
    #
    # def test_get_pending_mutations(self):
    #     assert False

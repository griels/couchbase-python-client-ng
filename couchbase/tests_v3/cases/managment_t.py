from couchbase.management.buckets import CreateBucketSettings
from couchbase_tests.base import CollectionTestCase
from collections import namedtuple


class BucketManagementTests(CollectionTestCase):
    def setUp(self, *args, **kwargs):
        super(BucketManagementTests,self).setUp(*args, **kwargs)
        self.bm=self.cluster.buckets()

    def test_bucket_create(self):
        self.bm.create_bucket(CreateBucketSettings(name="fred",bucket_type="couchbase"))

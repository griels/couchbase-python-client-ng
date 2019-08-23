from gcouchbase.bucket import Bucket
from couchbase_core.client import _depr
from couchbase_core.connstr import convert_1x_args

class GConnection(Bucket):
    def __init__(self, bucket, **kwargs):
        _depr('gcouchbase.connection.GConnection',
              'gcouchbase.bucket.Bucket')

        kwargs = convert_1x_args(bucket, **kwargs)
        super(GConnection, self).__init__(**kwargs)

from couchbase_v2.bucket import Bucket, _depr
from couchbase_v2.user_constants import *
from couchbase_v2.connstr import convert_1x_args

_depr('couchbase_v2.connection', 'couchbase_v2.bucket')

class Connection(Bucket):
    def __init__(self, bucket='default', **kwargs):
        kwargs = convert_1x_args(bucket, **kwargs)
        super(Connection, self).__init__(**kwargs)

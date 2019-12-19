from typing import *

class GenericManager(object):
    def __init__(self,
                 parent  # type: 'couchbase.cluster.Cluster'
                 ):
        self._admin_bucket = parent._clusterclient
        self._parent=parent

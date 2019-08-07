#
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

from couchbase_core.asynchronous.view import AsyncViewBase
from couchbase_v2.bucket import Bucket
from couchbase_core.exceptions import ArgumentError
from couchbase_core.asynchronous.bucket import AsyncBucketFactory as CoreAsyncBucketFactory
from couchbase_core.asynchronous.bucket import AsyncBucket as CoreAsyncBucket
from couchbase_core.bucket import Bucket as CoreBucket
from couchbase_core._pyport import with_metaclass


class AsyncBucket(Bucket):
    syncbucket=Bucket
    def __init__(self, iops=None, *args, **kwargs):
        """
        Create a new Async Bucket. An async Bucket is an object
        which functions like a normal synchronous bucket connection,
        except that it returns future objects
        (i.e. :class:`~couchbase_v2.result.AsyncResult`
        objects) instead of :class:`~couchbase_v2.result.Result`.
        These objects are actually :class:`~couchbase_v2.result.MultiResult`
        objects which are empty upon retun. As operations complete, this
        object becomes populated with the relevant data.

        Note that the AsyncResult object must currently have valid
        :attr:`~couchbase_v2.result.AsyncResult.callback` and
        :attr:`~couchbase_v2.result.AsyncResult.errback` fields initialized
        *after* they are returned from
        the API methods. If this is not the case then an exception will be
        raised when the callbacks are about to arrive. This behavior is the
        primary reason why this interface isn't public, too :)

        :param iops: An :class:`~couchbase_v2.iops.base.IOPS`-interface
          conforming object. This object must not be used between two
          instances, and is owned by the connection object.

        :param kwargs: Additional arguments to pass to
          the :class:`~couchbase_v2.bucket.Bucket` constructor
        """

        CoreAsyncBucket.__init__(iops=iops, *args, **kwargs)

    query = CoreAsyncBucket.view_query
    n1ql_query = CoreAsyncBucket.query
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

from couchbase_v2.bucket import Bucket
from couchbase_core.asynchronous.bucket import AsyncBucketFactory as CoreAsyncBucketFactory
from couchbase_core._pyport import with_metaclass

class AsyncBucketFactory(type):
    def __new__(cls, name, bases, attrs):
        original=bases[0]
        class AsyncBucketBase(with_metaclass(CoreAsyncBucketFactory,original)):
            pass
        attrs['query']=AsyncBucketBase.view_query
        attrs['n1ql_query']=AsyncBucketBase.query
        return super(AsyncBucketFactory,cls).__new__(cls, name, tuple([AsyncBucketBase])+bases[1:], attrs)

class AsyncBucket(with_metaclass(CoreAsyncBucketFactory,Bucket)):
    def __init__(self, *args, **kwargs):
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

        super(AsyncBucket,self).__init__(*args, **kwargs)

AsyncBucket.query=AsyncBucket.view_query
AsyncBucket.n1ql_query=AsyncBucket.query

#
# Copyright 2019, Couchbase, Inc.
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
from couchbase.options import UnsignedInt64

try:
    from abc import abstractmethod
except:
    import abstractmethod


from couchbase_core.n1ql import N1QLRequest
from couchbase_core import iterable_wrapper, JSON, parse_time
from typing import *
from datetime import timedelta
import enum
import attr


class QueryStatus(enum.Enum):
    RUNNING = ()
    SUCCESS = ()
    ERRORS = ()
    COMPLETED = ()
    STOPPED = ()
    TIMEOUT = ()
    CLOSED = ()
    FATAL = ()
    ABORTED = ()
    UNKNOWN = ()


class QueryWarning(object):
    def __init__(self, raw_warning):
        self._raw_warning = raw_warning

    def code(self):
        # type: (...) -> int
        pass

    def message(self):
        # type: (...) -> str
        pass


class QueryMetrics(object):
    def __init__(self, raw_metrics):
        self._raw_metrics = raw_metrics

    def elapsed_time(self):
        # type: (...) -> timedelta
        return parse_time(self._raw_metrics.get('elapsedTime'))

    def execution_time(self):
        # type: (...) -> timedelta
        pass

    def sort_count(self):
        # type: (...) -> UnsignedInt64
        pass

    def result_count(self):
        # type: (...) -> UnsignedInt64
        pass

    def result_size(self):
        # type: (...) -> UnsignedInt64
        pass

    def mutation_count(self):
        # type: (...) -> UnsignedInt64
        pass

    def error_count(self):
        # type: (...) -> UnsignedInt64
        return UnsignedInt64(self._raw_metrics.get('errorCount', 0))

    def warning_count(self):
        # type: (...) -> UnsignedInt64
        pass


class QueryMetaData(object):
    def __init__(self,
                 parent  # type: QueryResult
                 ):
        self._parent = parent

    def request_id(self):
        # type: (...) -> str
        return self._parent.meta.get('requestID')

    def client_context_id(self):
        # type: (...) -> str
        return self._parent.meta.get('clientContextID')

    def signature(self):
        # type: (...) -> JSON
        return self._parent.meta.get('signature')

    def status(self):
        # type: (...) -> QueryStatus
        raise QueryStatus(self._parent.meta.get('status').upper())

    def warnings(self):
        # type: (...) -> List[QueryWarning]
        raise NotImplementedError()

    def metrics(self):
        # type: (...) -> Optional[QueryMetrics]
        return QueryMetrics(self._parent.metrics)

    def profile(self):
        # type: (...) -> Optional[JSON]
        return self._parent.profile


class QueryResult(iterable_wrapper(N1QLRequest)):
    def __init__(self,
                 *args, **kwargs
                 ):
        # type (...)->None
        super(QueryResult,self).__init__(*args, **kwargs)

    def metadata(self  # type: QueryResult
                 ):
        # type: (...) -> QueryMetaData
        return QueryMetaData(self)




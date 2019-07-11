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
from couchbase_core import IterableWrapper

from .options import OptionBlock

try:
    from abc import abstractmethod
except:
    import abstractmethod


from couchbase_core.n1ql import N1QLRequest
from typing import *


class IQueryResult(object):

    @abstractmethod
    def request_id(self):
        # type: (...) ->UUID
        pass

    @abstractmethod
    def client_context_id(self):
        # type: (...)->str
        pass

    @abstractmethod
    def signature(self):
        # type: (...)->Any
        pass

    @abstractmethod
    def rows(self):
        # type: (...)->List[T]
        pass

    @abstractmethod
    def warnings(self):
        # type: (...)->List[Warning]
        pass

    @abstractmethod
    def metrics(self):
        # type: (...)->QueryMetrics
        pass


class QueryOptions(OptionBlock, IQueryResult):
    @property
    @abstractmethod
    def is_live(self):
        return False

    def __init__(self, statement=None, parameters=None, timeout=None):

        """
        Executes a N1QL query against the remote cluster returning a IQueryResult with the results of the query.
        :param statement: N1QL query
        :param options: the optional parameters that the Query service takes. See The N1QL Query API for details or a SDK 2.0 implementation for detail.
        :return: An IQueryResult object with the results of the query or error message if the query failed on the server.
        :except Any exceptions raised by the underlying platform - HTTP_TIMEOUT for example.
        :except ServiceNotFoundException - service does not exist or cannot be located.

        """
        super(QueryOptions, self).__init__(statement=statement, parameters=parameters, timeout=timeout)


class QueryMetrics(object):
    pass


class QueryResult(IterableWrapper):
    def __init__(self,
                 parent  # type: N1QLRequest
                 ):
        # type (...)->None
        super(QueryResult,self).__init__(parent)

    def rows(self):
        return list(x for x in self)

    def metrics(self):  # type: (...)->QueryMetrics
        return self.parent.metrics

    def request_id(self):
        raise NotImplementedError("To be implemented")

    def client_context_id(self):
        raise NotImplementedError("To be implemented")

    def signature(self):
        raise NotImplementedError("To be implemented")

    def warnings(self):
        raise NotImplementedError("To be implemented")



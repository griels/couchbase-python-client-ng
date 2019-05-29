import abc
from abc import abstractproperty

from uuid import UUID

from typing import *

from couchbase_v3 import OptionBlock, Bucket, forward_args, OptionBlockDeriv, SearchException, SDK2Bucket
from .bucket import BucketOptions
from couchbase_v2.cluster import Cluster as SDK2Cluster, Authenticator as SDK2Authenticator
import couchbase_v3.options


T=TypeVar('T')


class QueryMetrics(object):
    pass


class IQueryResult:
    def request_id(self):
        # type: (...) ->UUID
        pass

    def client_context_id(self):
        # type: (...)->str
        pass

    def signature(self):
        # type: (...)->Any
        pass

    def rows(self):
        # type: (...)->List[T]
        pass

    def warnings(self):
        # type: (...)->List[Warning]
        pass

    def metrics(self):
        # type: (...)->QueryMetrics
        pass


CallableOnOptionBlock = Callable[[OptionBlockDeriv, Any], Any]


def options_to_func(orig,  # type: U
                    verb  # type: CallableOnOptionBlock
                    ):
    class invocation:
        # type: (...)->Callable[[T,Tuple[OptionBlockDeriv,...],Any],Any]
        def __init__(self,  # type: T
                       *options,  # type: OptionBlockDeriv
                       **kwargs  # type: Any
                       ):
            # type: (...)->None
            self.orig=orig
            self.options=options
            self.kwargs=kwargs

        def __call__(self, *args, **kwargs):
            # type: (...)->Callable[[T,Tuple[OptionBlockDeriv,...],Any],Any]
            def invocator(self, *options, **kwargs):
                return verb(self, forward_args(kwargs, *options))
            return invocator

    return invocation(orig)


class QueryOptions(OptionBlock, IQueryResult):
    @property
    @abc.abstractmethod
    def is_live(self):
        return False

    def __init__(self, statement = None, parameters=None, timeout = None):

        """
        Executes a N1QL query against the remote cluster returning a IQueryResult with the results of the query.
        :param statement: N1QL query
        :param options: the optional parameters that the Query service takes. See The N1QL Query API for details or a SDK 2.0 implementation for detail.
        :return: An IQueryResult object with the results of the query or error message if the query failed on the server.
        :except Any exceptions raised by the underlying platform - HTTP_TIMEOUT for example.
        :except ServiceNotFoundException - service does not exist or cannot be located.

        """
        super(Cluster.QueryOptions, self).__init__(statement=statement, parameters=parameters, timeout=timeout)


class Cluster:
    class ClusterOptions(OptionBlock):
        pass

    def __init__(self,
                 connection_string=None,  # type: str
                 *options  # type: ClusterOptions
                 ):
        self._cluster = SDK2Cluster(connection_string, bucket_class = Bucket, **couchbase_v3.forward_args(None, *options))
        self.outerself = self  # type: Cluster

    def authenticate(self,
                     authenticator=None,  # type: SDK2Authenticator
                     username=None,  # type: str
                     password=None  # type: str
                     ):
        self._cluster.authenticate(authenticator, username, password)

    def bucket(self,
               name,  # type: str,
               *options,  # type: BucketOptions
               **kwargs
               ):
        # type: (...)->Bucket
        return self._cluster.open_bucket(name, **forward_args(kwargs,*options))

    class QueryParameters(OptionBlock):
        def __init__(self, *args, **kwargs):
            super(Cluster.QueryParameters, self).__init__(*args, **kwargs)

    @overload
    def query(self,
              statement,
              parameters=None,
              timeout=None):
        pass

    @overload
    def query(self,
              statement,  # type: str,
              *options  # type: QueryOptions
              ):
        # type: (...)->IQueryResult
        pass

    def query_real(self,
                   statement,
                   *options, **kwargs):
        # type: (str, Any, Any) -> IQueryResult
        result = self._cluster.n1ql_query(statement, forward_args(kwargs, *options))
        return result

    @options_to_func(QueryOptions, query_real)
    class query:
        __doc__ = QueryOptions.__doc__

    def _operate_on_first_bucket(self, verb, failtype, *args, **kwargs):
        first_bucket = next(iter(self._cluster._buckets), None)  # type: Optional[couchbase_v3.SDK2Bucket]
        if not first_bucket:
            raise failtype("Need at least one bucket active to perform search")
        return verb(first_bucket, *args, **kwargs)

    def analytics_query(self,
                        statement,  # type: str,
                        *options,  # type: AnalyticsOptions
                        **kwargs
                        ):
        # type: (...)->IAnalyticsResult
        """
        Executes an Analytics query against the remote cluster and returns a IAnalyticsResult with the results of the query.
        :param statement: the analytics statement to execute
        :param options: the optional parameters that the Analytics service takes based on the Analytics RFC.
        :return: An IAnalyticsResult object with the results of the query or error message if the query failed on the server.
        Throws Any exceptions raised by the underlying platform - HTTP_TIMEOUT for example.
        :except ServiceNotFoundException - service does not exist or cannot be located.
        """
        return self.query(statement, *options, **kwargs)

    def search_query(self,
                     index,  # type: str
                     query,  # type: str
                     *options,  # type: SearchOptions
                     **kwargs
                     ):
        # type: (...)->ISearchResult
        """
        Executes a Search or FTS query against the remote cluster and returns a ISearchResult implementation with the results of the query.

        :param query: the fluent search API to construct a query for FTS
        :param options: the options to pass to the cluster with the query based off the FTS/Search RFC
        :return: An ISearchResult object with the results of the query or error message if the query failed on the server.
        Any exceptions raised by the underlying platform - HTTP_TIMEOUT for example.
        :except    ServiceNotFoundException - service does not exist or cannot be located.

        """
        return self._operate_on_first_bucket(SDK2Bucket.search, SearchException, index, query, **forward_args(kwargs, *options))


    def diagnostics(self,
                    reportId=None  # type: str
                    ):
        # type: (...)->IDiagnosticsResult
        """
        Creates a diagnostics report that can be used to determine the healthfulness of the Cluster.
        :param reportId - an optional string name for the generated report.
        :return:A IDiagnosticsResult object with the results of the query or error message if the query failed on the server.

        """
        return self._operate_on_first_bucket(SDK2Bucket.diagnostics, couchbase_v3.DiagnosticsException)

    def users(self):
        # type: (...)->IUserManager
        pass

    def indexes(self):
        # type: (...)->IIndexManager
        pass

    def nodes(self):
        # type: (...)->INodeManager
        pass

    def buckets(self):
        # type: (...)->IBucketManager
        pass

    def disconnect(self,
                   options=None  # type: DisconnectOptions
                   ):
        # type: (...)->None
        """
        Closes and cleans up any resources used by the Cluster and any objects it owns. Note the name is platform idiomatic.

        :param options - TBD
        :return: None
        :except Any exceptions raised by the underlying platform

        """
        pass

    def manager(self):
        # type: (...)->ClusterManager
        """

        Manager
        Returns a ClusterManager object for managing resources at the Cluster level.

        Caveats and notes:
        It is acceptable for a Cluster object to have a static Connect method which takes a Configuration for ease of use.
        To facilitate testing/mocking, it's acceptable for this structure to derive from an interface at the implementers discretion.
        The "Get" and "Set" prefixes are considered platform idiomatic and can be adjusted to various platform idioms.
        The Configuration is passed in via the ctor; overloads for connection strings and various other platform specific configuration are also passed this way.
        If a language does not support ctor overloading, then an equivalent method can be used on the object.

        :return:
        """
        pass


QueryParameters = Cluster.QueryParameters
ClusterOptions = Cluster.ClusterOptions
from typing import *

from couchbase.management.queries import QueryIndexManager
from couchbase.management.search import SearchIndexManager
from couchbase_core.exceptions import CouchbaseError
from .management.users import UserManager
from .management.buckets import BucketManager
from couchbase.management.admin import Admin
from couchbase.diagnostics import DiagnosticsResult, EndPointDiagnostics
from couchbase.fulltext import SearchResult, SearchOptions
from couchbase_core.fulltext import Query, Facet
from .analytics import AnalyticsResult
from .n1ql import QueryResult
from couchbase_core.n1ql import N1QLQuery
from .options import OptionBlock, OptionBlockTimeOut, forward_args, OptionBlockDeriv
from .bucket import BucketOptions, Bucket, CoreClient
from couchbase_core.cluster import Cluster as CoreCluster, Authenticator as CoreAuthenticator
from .exceptions import InvalidArgumentsException, SearchException, DiagnosticsException, QueryException, ArgumentError, AnalyticsException
from couchbase_core import abstractmethod
import multiprocessing
from multiprocessing.pool import ThreadPool
import couchbase.exceptions
import couchbase_core._libcouchbase as _LCB
from couchbase_core._pyport import raise_from
from couchbase.options import OptionBlockTimeOut


T = TypeVar('T')


class QueryMetrics(object):
    pass


CallableOnOptionBlock = Callable[[OptionBlockDeriv, Any], Any]


def options_to_func(orig,  # type: U
                    verb  # type: CallableOnOptionBlock
                    ):
    class invocation:
        # type: (...) -> Callable[[T,Tuple[OptionBlockDeriv,...],Any],Any]
        def __init__(self,  # type: T
                       *options,  # type: OptionBlockDeriv
                       **kwargs  # type: Any
                       ):
            # type: (...) -> None
            self.orig=orig
            self.options=options
            self.kwargs=kwargs

        def __call__(self, *args, **kwargs):
            # type: (...) -> Callable[[T,Tuple[OptionBlockDeriv,...],Any],Any]
            def invocator(self, *options, **kwargs):
                return verb(self, forward_args(kwargs, *options))
            return invocator

    return invocation(orig)


class AnalyticsOptions(OptionBlock):
    pass

class QueryScanConsistency(object):
  REQUEST_PLUS="request_plus"
  NOT_BOUNDED="not_bounded"

  def __init__(self, val):
    if val == self.REQUEST_PLUS or val == self.NOT_BOUNDED:
      self._value = val
    else:
      raise InvalidArgumentsException("QueryScanConsistency can only be {} or {}".format(self.REQUEST_PLUS, self.NOT_BOUNDED))

  @classmethod
  def request_plus(cls):
    return cls(cls.REQUEST_PLUS)

  @classmethod
  def not_bounded(cls):
    return cls(cls.NOT_BOUNDED)

  def as_string(self):
    return getattr(self, '_value', self.NOT_BOUNDED)

class QueryProfile(object):
  OFF='off'
  PHASES='phases'
  TIMINGS='timings'

  @classmethod
  def off(cls):
    return cls(cls.OFF)

  @classmethod
  def phases(cls):
    return cls(cls.PHASES)

  @classmethod
  def timings(cls):
    return cls(cls.TIMINGS)

  def __init__(self, val):
    if val == self.OFF or val == self.PHASES or val==self.TIMINGS:
      self._value = val
    else:
      raise InvalidArgumentsException("QueryProfile can only be {}, {}, {}".format(self.OFF, self.TIMINGS, self.PHASES))

  def as_string(self):
    return getattr(self, '_value', self.OFF)

class QueryOptions(OptionBlockTimeOut):
  VALID_OPTS=['timeout', 'read_only', 'scan_consistency','adhoc', 'client_context_id', 'consistent_with',
              'max_parallelism', 'positional_parameters', 'named_parameters', 'pipeline_batch', 'pipeline_cap',
              'profile', 'raw', 'scan_wait', 'scan_cap', 'metrics']
  @overload
  def __init__(self,
               timeout,                # type: timedelta
               read_only,              # type: bool
               scan_consistency,       # type: QueryScanConsistency
               adhoc,                  # type: bool
               client_context_id,      # type: str
               consistent_with,        # type: MutationState
               max_parallelism,        # type: int
               positional_parameters,  # type: Iterable[str]
               named_parameters,       # type: dict[str, str]
               pipeline_batch,         # type: int
               pipeline_cap,           # type: int
               profile,                # type: QueryProfile
               raw,                    # type: dict[str,Any]
               scan_wait,              # type: timedelta
               scan_cap,               # type: int
               metrics=False           # type: bool
               ):

    pass

  def __init__(self,
               **kwargs
               ):
    super(QueryOptions, self).__init__(**kwargs)

  def to_n1ql_query(self, statement, *options, **kwargs):
    # lets make a copy of the options, and update with kwargs...
    args = self.copy()
    args.update(kwargs)

    # now lets get positional parameters.  Actual positional
    # params OVERRIDE positional_parameters
    positional_parameters = args.pop('positional_parameters', [])
    if options and len(options) > 0:
      positional_parameters = options

    # now the named parameters.  NOTE: all the kwargs that are
    # not VALID_OPTS must be named parameters, and the kwargs
    # OVERRIDE the list of named_parameters
    new_keys = list(filter(lambda x: x not in self.VALID_OPTS, args.keys()))
    named_parameters = args.pop('named_parameters',{})
    for k in new_keys:
      named_parameters[k] = args[k]

    query = N1QLQuery(statement, *positional_parameters, **named_parameters)
    # now lets try to setup the options.  TODO: rework this after beta.3
    # but for now we will use the existing N1QLQuery.  Could be we can
    # add to it, etc...

    # default to false on metrics
    query.metrics = args.get('metrics', False)

    # TODO: there is surely a cleaner way...
    for k in self.VALID_OPTS:
      v = args.get(k, None)
      if (v):
        if k == 'scan_consistency':
          query.consistency = v.as_string()
        if k == 'consistent_with':
          query.consistent_with = v
        if k == 'adhoc':
          query.adhoc = v
        if k == 'timeout':
          query.timeout = v
        if k == 'scan_cap':
          query.scan_cap = v
        if k == 'pipeline_batch':
          query.pipeline_batch = v
        if k == 'pipeline_cap':
          query.pipeline_cap = v
        if k == 'read_only':
          query.readonly = v
        if k == 'profile':
          query.profile = v.as_string()
    return query

  # this will change the options for export.
  # NOT USED CURRENTLY
  def as_dict(self):
    for key, val in self.items():
      if key == 'positional_parameters':
        self.pop(key, None)
        self['args'] = val
      if key == 'named_parameters':
        self.pop(key, None)
        for k, v in val.items():
          self["${}".format(k)]=v
      if key == 'scan_consistency':
        self[key] = value.as_string()
      if key == 'consistent_with':
        self[key] = value.encode()
      if key == 'profile':
        self[key] = val.as_string()
      if key == 'scan_wait':
        # scan_wait should be in ms
        self[key] = val.total_seconds() * 1000
    if self.get('consistent_with', None):
      self['scan_consistency'] = 'at_plus'
    return self

class Cluster(object):
    clusterbucket = None  # type: CoreClient

    class ClusterOptions(OptionBlock):
        def __init__(self,
                     authenticator,  # type: CoreAuthenticator
                     **kwargs
                     ):
            super(ClusterOptions, self).__init__()
            self['authenticator'] = authenticator

    @overload
    def __init__(self,
                 connection_string,  # type: str
                 options  # type: ClusterOptions
                 ):
        pass

    def __init__(self,
                 connection_string,  # type: str
                 *options,  # type: ClusterOptions
                 **kwargs
                 ):
        """
        Create a Cluster object.
        An Authenticator must be provided either as the first argument or within the options argument.
        :param connection_string: the connection string for the cluster
        :param options: options for the cluster
        :type Cluster.ClusterOptions
        """
        self.connstr=connection_string
        cluster_opts=forward_args(kwargs, *options)
        authenticator=cluster_opts.pop('authenticator',None)
        if not authenticator:
            raise ArgumentError("Authenticator is mandatory")
        cluster_opts.update(bucket_class=lambda connstr, bname=None, **kwargs: Bucket(connstr,name=bname,admin=self.admin,**kwargs))
        self._cluster = CoreCluster(connection_string, **cluster_opts)  # type: CoreCluster
        self._authenticate(authenticator)

    @staticmethod
    def connect(connection_string,  # type: str
                *options,  # type: ClusterOptions
                **kwargs
                ):
        return Cluster(connection_string, *options, **kwargs)

    def _authenticate(self,
                      authenticator=None,  # type: CoreAuthenticator
                      username=None,  # type: str
                      password=None  # type: str
                      ):
        self._cluster.authenticate(authenticator, username, password)
        credentials = authenticator.get_credentials()
        self._clusteropts = credentials.get('options', {})
        self._clusteropts['bucket'] = "default"
        self._clusterclient=None
        auth=credentials.get('options')
        self.admin = Admin(auth.get('username'), auth.get('password'), connstr=str(self.connstr))

    def bucket(self,
               name,  # type: str,
               *options,  # type: BucketOptions
               **kwargs
               ):
        # type: (...) -> Bucket
        args=forward_args(kwargs,*options)
        args.update(bname=name)
        return self._cluster.open_bucket(name, **args)

    def query(self,
              statement,            # type: str
              *options,             # type: Any
              **kwargs              # type: Any
              ):
        # type: (...) -> QueryResult
        """
        Perform a N1QL query.

        :param str statement: the N1QL query statement to execute
        :param QueryOptions options: the optional parameters that the Query service takes.
        :param Any options: if present, assumed to be the positional parameters in the query.
        :param Any kwargs: Override the corresponding value in the Options.  If they don't match
          any value in the options, assumed to be named parameters for the query.

        :return: An :class:`QueryResult` object with the results of the query or error message
            if the query failed on the server.

        """
        # we could have multiple positional parameters passed in, one of which may or may not be
        # a QueryOptions.  Note if multiple QueryOptions are passed in for some strange reason,
        # all but the last are ignored.
        opt = QueryOptions()
        opts = list(options)
        for o in opts:
          if isinstance(o, QueryOptions):
            opt = o
            opts.remove(o)

        return QueryResult(self._operate_on_cluster(CoreClient.query, QueryException, opt.to_n1ql_query(statement, *opts, **kwargs)))

    def _operate_on_cluster(self,
                            verb,
                            failtype,  # type: Type[CouchbaseError]
                            *args,
                            **kwargs):
        if not self._clusterclient:
            self._clusterclient = CoreClient(str(self.connstr), _conntype=_LCB.LCB_TYPE_CLUSTER, **self._clusteropts)
        try:
            return verb(self._clusterclient, *args, **kwargs)
        except Exception as e:
            raise_from(failtype(params=CouchbaseError.ParamType(message="Cluster operation failed", inner_cause=e)), e)

    def analytics_query(self,  # type: Cluster
                        statement,  # type: str,
                        *options,  # type: AnalyticsOptions
                        **kwargs
                        ):
        # type: (...) -> AnalyticsResult
        """
        Executes an Analytics query against the remote cluster and returns a AnalyticsResult with the results of the query.
        :param statement: the analytics statement to execute
        :param options: the optional parameters that the Analytics service takes based on the Analytics RFC.
        :return: An AnalyticsResult object with the results of the query or error message if the query failed on the server.
        Throws Any exceptions raised by the underlying platform - HTTP_TIMEOUT for example.
        :except ServiceNotFoundException - service does not exist or cannot be located.
        """

        return AnalyticsResult(self._operate_on_cluster(CoreClient.analytics_query, AnalyticsException, statement, **forward_args(kwargs,*options)))

    @overload
    def search_query(self,
                     index,  # type: str
                     query,  # type: Union[str, Query]
                     facets=None  # type: Mapping[str,Facet]
                     ):
        pass

    @overload
    def search_query(self,
                     index,  # type: str
                     query,  # type: Union[str, Query]
                     options,  # type: SearchOptions
                     ):
        pass

    def search_query(self,
                     index,  # type: str
                     query,  # type: Union[str, Query]
                     *options,  # type: SearchOptions
                     **kwargs
                     ):
        # type: (...) -> SearchResult
        """
        Executes a Search or F.T.S. query against the remote cluster and returns a SearchResult implementation with the results of the query.

        :param query: the fluent search API to construct a query for F.T.S.
        :param options: the options to pass to the cluster with the query based off the F.T.S./Search RFC
        :return: An SearchResult object with the results of the query or error message if the query failed on the server.
        Any exceptions raised by the underlying platform - HTTP_TIMEOUT for example.
        :except    ServiceNotFoundException - service does not exist or cannot be located.

        """
        return SearchResult(self._operate_on_cluster(CoreClient.search, SearchException, index, query, **forward_args(kwargs, *options)))

    _root_diag_data = {'id', 'version', 'sdk'}

    def diagnostics(self,
                    reportId=None,  # type: str
                    timeout=None
                    ):
        # type: (...) -> DiagnosticsResult
        """
        Creates a diagnostics report that can be used to determine the healthfulness of the Cluster.
        :param reportId - an optional string name for the generated report.
        :return:A DiagnosticsResult object with the results of the query or error message if the query failed on the server.

        """

        pool = ThreadPool(processes=1)
        diag_results_async_result = pool.apply_async(self._operate_on_cluster,
                                                     (CoreClient.diagnostics, DiagnosticsException))
        try:
            diag_results = diag_results_async_result.get(timeout)
        except multiprocessing.TimeoutError as e:
            raise couchbase.exceptions.TimeoutError(params=dict(inner_cause=e))

        final_results = {'services': {}}

        for k, v in diag_results.items():
            if k in Cluster._root_diag_data:
                final_results[k] = v
            else:
                for item in v:
                    final_results['services'][k] = EndPointDiagnostics(k, item)
        return DiagnosticsResult(final_results)

    def users(self):
        # type: (...) -> UserManager
        return UserManager(self.admin)

    def query_indexes(self):
        # type: (...) -> QueryIndexManager
        return QueryIndexManager(self.admin)

    def search_indexes(self):
      # type: (...) -> SearchIndexManager
      return SearchIndexManager(self.admin)

    def buckets(self):
        # type: (...) -> BucketManager
        return BucketManager(self.admin)

    def disconnect(self,
                   options=None  # type: DisconnectOptions
                   ):
        # type: (...) -> None
        """
        Closes and cleans up any resources used by the Cluster and any objects it owns. Note the name is platform idiomatic.

        :param options - TBD
        :return: None
        :except Any exceptions raised by the underlying platform

        """
        raise NotImplementedError("To be implemented in full SDK3 release")

    def manager(self):
        # type: (...) -> ClusterManager
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
        return self._cluster.cluster_manager()


ClusterOptions = Cluster.ClusterOptions

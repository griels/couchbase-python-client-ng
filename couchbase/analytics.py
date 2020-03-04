from __future__ import annotations
from .n1ql import *
from couchbase_core.n1ql import N1QLRequest
from couchbase.options import OptionBlockTimeOut
from enum import Enum
from couchbase_core.analytics import AnalyticsQuery


class AnalyticsIndex(dict):
    def __init__(self, **kwargs):
        print("creating index from {}".format(kwargs))
        super(AnalyticsIndex, self).__init__(**kwargs['Index'])

    @property
    def name(self):
        return self.get("IndexName", None)

    @property
    def dataset_name(self):
        return self.get("DatasetName", None)

    @property
    def dataverse_name(self):
        return self.get("DataverseName", None)

    @property
    def is_primary(self):
        return self.get("IsPrimary", None)


class AnalyticsDataType(Enum):
    STRING='string'
    INT64='int64'
    DOUBLE='double'


class AnalyticsDataset(dict):
    def __init__(self, **kwargs):
        super(AnalyticsDataset, self).__init__(**kwargs)

    @property
    def dataset_name(self):
        return self.get("DatasetName", None)

    @property
    def dataverse_name(self):
        return self.get('DataverseName', None)

    @property
    def link_name(self):
        return self.get('LinkName', None)

    @property
    def bucket_name(self):
        return self.get('BucketName', None)


class AnalyticsResult(QueryResult):
    def client_context_id(self):
        return super(AnalyticsResult, self).client_context_id()

    def signature(self):
        return super(AnalyticsResult, self).signature()

    def warnings(self):
        return super(AnalyticsResult, self).warnings()

    def request_id(self):
        return super(AnalyticsResult, self).request_id()

    def __init__(self,
                 parent  # type: N1QLRequest
                 ):
        super(AnalyticsResult, self).__init__(parent)
        self._params=parent._params


from couchbase.cluster import QueryScanConsistency, QueryProfile


class AnalyticsOptions(OptionBlockTimeOut):
    VALID_OPTS = {'timeout', 'read_only', 'scan_consistency', 'client_context_id', 'positional_parameters',
                  'named_parameters', 'raw'}
    @overload
    def __init__(self,
                 timeout=None,  # type: timedelta
                 read_only=None,  # type: bool
                 scan_consistency=None,  # type: 'couchbase.cluster.QueryScanConsistency'
                 client_context_id=None,  # type: str
                 priority=None,  # type: bool
                 positional_parameters=None,  # type: Iterable[str]
                 named_parameters=None,  # type: Dict[str, str]
                 raw=None,  # type: Dict[str,Any]
                 ):

        pass

    def __init__(self,
                 **kwargs
                 ):
        super(AnalyticsOptions, self).__init__(**kwargs)

    # TODO: the priority is not making it into the queries yet -- see PYCBC-827
    def to_analytics_query(self, statement, *options, **kwargs):
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
        new_keys = args.keys()-self.VALID_OPTS
        named_parameters = args.pop('named_parameters', {})
        named_parameters.update({k: args[k] for k in new_keys})

        query = AnalyticsQuery(statement, *positional_parameters, **named_parameters)

        # TODO: there is surely a cleaner way...
        identity=lambda x:x
        for k, v in [(k, args.get(k)) for k in
                     (self.VALID_OPTS & args.keys())]:  # self.VALIDOPTS would need to be a set

            (prop, conversion) = {'scan_consistency': (AnalyticsQuery.consistency, QueryScanConsistency.as_string),
                                  'profile':          (AnalyticsQuery.profile, QueryProfile.as_string),
                                  'read_only': (AnalyticsQuery.readonly, identity),
                                  'timeout': (AnalyticsQuery.timeout, identity)}.get(k)
            prop.setter(query, conversion(v))

        return query




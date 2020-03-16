from typing import *

from fulltext import _SingleQuery, _genprop_str, _with_fields, _genprop, NoChildrenError, Query, _assign_kwargs, \
    _location_conv, _RangeQuery, _CompoundQuery, _convert_gt0, _bprop_wrap
from .options import OptionBlockTimeOut, timedelta, AcceptableUnsignedInt32, UnsignedInt32, UnsignedInt64
from couchbase_core import abstractmethod, IterableWrapper, JSON
from enum import Enum
from couchbase_core.fulltext import SearchRequest
from datetime import timedelta
from couchbase_core._pyport import Protocol
import couchbase_core
import attr


SearchQueryRow = JSON

# there is a v2 Params class that does what we want here -
# so for now the SearchOptions can just use it under the
# hood.  Later when we eliminate the v2 stuff, we can move
# that logic over into SearchOptions itself


class SearchRow(Protocol):
    """A single entry of search results. The server calls them "hits", and represents as a JSON object. The following interface describes the contents of the result row."""
    def index(self):
        # type: (...) -> str
        pass

    def id(self):
        # type: (...) -> str
        pass

    def score(self):
        # type: (...) -> float
        pass

    def explanation(self):
        # type: (...) -> JSONDocument
        pass

    def locations(self):
        # type: (...) -> Optional[SearchRowLocations]
        pass

    def fragments(self):
        # type: (...) -> Optional[Mapping[str,str]]
        pass

    def fields(self):
        # type: (...) -> Optional[T]
        pass


class SearchRowLocation(NamedTuple):
    field: str
    term: str
    position: UnsignedInt32
    start: UnsignedInt32
    end: UnsignedInt32
    array_positions: List[UnsignedInt32] = []


class SearchFacetResult(NamedTuple):
    """ An individual facet result has both metadata and details,
    as each facet can define ranges into which results are categorized."""
    name: str
    field: str
    total: UnsignedInt64
    missing: UnsignedInt64
    other: UnsignedInt64


"""Sample request/response payloads: https://github.com/couchbaselabs/sdk-testcases/tree/master/search"""

""" If top-level "error" property exists, then SDK should build and throw CouchbaseException with its content."""


@attr.attrs
class SearchMetrics(NamedTuple):
    took: timedelta
    total_rows: UnsignedInt64
    max_score: float
    success_partition_count: UnsignedInt64
    error_partition_count: UnsignedInt64

    @property
    def total_partition_count(self  # type: SearchMetrics
                              ):
        # type: (...) -> UnsignedInt64
        return self.success_partition_count + self.error_partition_count


class SearchRowLocations(Protocol):
    def get_all(self):
        # type: (...) -> List[SearchRowLocation]
        """list all locations (any field, any term)"""
        pass

    # list all locations for a given field (any term)
    @overload
    def get(self,
            field  # type: str
            ):
        # type: (...) -> List[SearchRowLocation]
        pass

    def get(self,
            field,  # type: str
            term  # type: str
            ):

        # type: (...) -> List[SearchRowLocation]
        """List all locations for a given field and term"""
        pass

    def fields(self):
        # type: (...) -> List[str]
        """
        :return: the fields in this location
        """
        pass

    def terms(self):
        # type: (...) -> Set[str]
        """
        List all terms in this locations,
        considering all fields (so a set):
        """
        pass

    def terms_for(self,
                  field  # type:str
                  ):

        # type: (...) -> list[str]
        """ list the terms for a given field """
        pass


class HighlightStyle(Enum):
    Ansi = 'ansi'
    Html = 'html'


class SearchOptions(OptionBlockTimeOut):
    @overload
    def __init__(self,
                 timeout=None,           # type: timedelta
                 limit=None,             # type: int
                 skip=None,              # type: int
                 explain=None,           # type: bool
                 fields=None,            # type: List[str]
                 highlight_style=None,   # type: HighlightStyle
                 highlight_fields=None,  # type: List[str]
                 scan_consistency=None,  # type: cluster.QueryScanConsistency
                 consistent_with=None,   # type: couchbase_core.MutationState
                 facets=None,            # type: Dict[str, couchbase_core.fulltext.Facet]
                 raw=None                # type: JSON
                 ):
        pass

    def __init__(self,
                 **kwargs   # type: Any
                 ):
        # convert highlight_style to str if it is present...
        style = kwargs.get('highlight_style', None)
        if(style) :
            kwargs['highlight_style'] = style.value

        super(SearchOptions, self).__init__(**kwargs)


class SearchMetaData(NamedTuple):
    """Represents the meta-data returned along with a search query result."""
    metrics: SearchMetrics
    errors: Mapping[str, Exception]


class SearchResultProtocol(Protocol):
    Facet = object
    @abstractmethod
    def rows(self):
        # type: (...) -> List[SearchRow]
        pass

    @abstractmethod
    def facets(self):
        # type: (...) -> Mapping[str, Facet]
        pass

    @abstractmethod
    def metadata(self):
        # type: (...) -> MetaDataProtocol
        pass


class MetaDataProtocol(Protocol):
    @abstractmethod
    def success_count(self):
        # type: (...) -> int
        pass

    @abstractmethod
    def error_count(self):
        # type: (...) -> int
        pass

    @abstractmethod
    def took(self):
        # type: (...) -> timedelta
        pass

    @abstractmethod
    def total_hits(self):
        # type: (...) -> int
        pass

    @abstractmethod
    def max_score(self):
        # type: (...) -> float
        pass


class MetaData(object):
    def __init__(self,
                 raw_data  # type: JSON
                 ):
        self._raw_data = raw_data

    @property
    def _status(self):
        # type: (...) -> Dict[str,int]
        return self._raw_data.get('status',{})

    def success_count(self):
        # type: (...) -> int
        return self._status.get('successful')

    def error_count(self):
        # type: (...) -> int
        return self._status.get('failed')

    def took(self):
        # type: (...) -> timedelta
        return timedelta(microseconds=self._raw_data.get('took'))

    def total_hits(self):
        # type: (...) -> int
        return self._raw_data.get('total_hits')

    def max_score(self):
        # type: (...) -> float
        return self._raw_data.get('max_score')


class SearchResult(SearchResultProtocol, IterableWrapper):
    def __init__(self,
                 raw_result  # type: SearchRequest
                 ):
        IterableWrapper.__init__(self, raw_result)

    def hits(self):
        # type: (...) -> Iterable[JSON]
        return list(x for x in self)

    def facets(self):
        # type: (...) -> Dict[str,SearchResult.Facet]
        return self.parent.facets

    def metadata(self):  # type: (...) -> MetaDataProtocol
        return MetaData(IterableWrapper.metadata(self))

from couchbase_core.fulltext import *
"""
SearchQuery implementations
MatchQuery
A match query analyzes the input text and uses that analyzed text to query the index.
MatchPhraseQuery
The input text is analyzed and a phrase query is built with the terms resulting from the analysis.
RegexpQuery
Finds documents containing terms that match the specified regular expression.
QueryStringQuery
The query string query allows humans to describe complex queries using a simple syntax.
WildcardQuery
Interprets * and ? wildcards as found in a lot of applications, for an easy implementation of such a search feature.
DocIdQuery
Allows to restrict matches to a set of specific documents.
BooleanFieldQuery
Allow to match `true`/`false` in a field mapped as boolean.
DateRangeQuery
The date range query finds documents containing a date value in the specified field within the specified range.
NumericRangeQuery
The numeric range query finds documents containing a numeric value in the specified field within the specified range.
TermRangeQuery
The term range query finds documents containing a string value in the specified field within the specified range.
GeoDistanceQuery
Finds `geopoint` indexed matches around a point with the given distance.
GeoBoundingBoxQuery
Finds `geopoint` indexed matches in a given bounding box.
ConjunctionQuery
Result documents must satisfy all of the child queries.
DisjunctionQuery
Result documents must satisfy a configurable min number of child queries.
BooleanQuery
The boolean query is a useful combination of conjunction and disjunction queries.
TermQuery
A query that looks for **exact** matches of the term in the index (no analyzer, no stemming). Useful to check what the actual content of the index is. It can also apply fuzziness on the term. Usual better alternative is `MatchQuery`.
PrefixQuery
The prefix query finds documents containing terms that start with the provided prefix. Usual better alternative is `MatchQuery`.
PhraseQuery
A query that looks for **exact** match of several terms (in the exact order) in the index. Usual better alternative is `MatchPhraseQuery`.
MatchAllQuery
A query that matches all indexed documents.
MatchNoneQuery
A query that matches nothing.

Return Types
SearchResult
The SearchResult interface provides a means of mapping the results of a Search query into an object. The description and details on the fields can be found in the Couchbase Full Text Search Index Query (FTS) RFC (which will be merged into this RFC during markdown conversion).

"""


class QueryStringQuery(_SingleQuery):
    """
    Query which allows users to describe a query in a query language.
    The server will then execute the appropriate query based on the contents
    of the query string:

    .. seealso::

        `Query Language <http://www.blevesearch.com/docs/Query-String-Query/>`_

    Example::

        QueryStringQuery('description:water and stuff')
    """

    _TERMPROP = 'query'
    query = _genprop_str('query')

    """
    Actual query string
    """


@_with_fields('field')
class WildcardQuery(_SingleQuery):
    """
    Query in which the characters `*` and `?` have special meaning, where
    `?` matches 1 occurrence and `*` will match 0 or more occurrences of the
    previous character
    """
    _TERMPROP = 'wildcard'
    wildcard = _genprop_str(_TERMPROP, doc='Wildcard pattern to use')


class DocIdQuery(_SingleQuery):
    """
    Matches document IDs. This is must useful in a compound query
    (for example, :class:`BooleanQuery`). When used as a criteria, only
    documents with the specified IDs will be searched.
    """
    _TERMPROP = 'ids'
    ids = _genprop(list, 'ids', doc="""
    List of document IDs to use
    """)

    def validate(self):
        super(DocIdQuery, self).validate()
        if not self.ids:
            raise NoChildrenError('`ids` must contain at least one ID')


@_with_fields('prefix_length', 'fuzziness', 'field', 'analyzer')
class MatchQuery(_SingleQuery):
    """
    Query which checks one or more fields for a match
    """
    _TERMPROP = 'match'
    match = _genprop_str(
        'match', doc="""
        String to search for
        """)


@_with_fields('fuzziness', 'prefix_length', 'field')
class TermQuery(_SingleQuery):
    """
    Searches for a given term in documents. Unlike :class:`MatchQuery`,
    the term is not analyzed.

    Example::

        TermQuery('lcb_cntl_string')
    """
    _TERMPROP = 'term'
    term = _genprop_str('term', doc='Exact term to search for')


@_with_fields('field', 'analyzer')
class MatchPhraseQuery(_SingleQuery):
    """
    Search documents which match a given phrase. The phrase is composed
    of one or more terms.

    Example::

        MatchPhraseQuery("Hello world!")
    """
    _TERMPROP = 'match_phrase'
    match_phrase = _genprop_str(_TERMPROP, doc="Phrase to search for")


@_with_fields('field')
class PhraseQuery(_SingleQuery):
    _TERMPROP = 'terms'
    terms = _genprop(list, 'terms', doc='List of terms to search for')

    def __init__(self, *phrases, **kwargs):
        super(PhraseQuery, self).__init__(phrases, **kwargs)

    def validate(self):
        super(PhraseQuery, self).validate()
        if not self.terms:
            raise NoChildrenError('Missing terms')


@_with_fields('field')
class PrefixQuery(_SingleQuery):
    """
    Search documents for fields beginning with a certain prefix. This is
    most useful for type-ahead or lookup queries.
    """
    _TERMPROP = 'prefix'
    prefix = _genprop_str('prefix', doc='The prefix to match')


@_with_fields('field')
class RegexQuery(_SingleQuery):
    """
    Search documents for fields matching a given regular expression
    """
    _TERMPROP = 'regex'
    regex = _genprop_str('regexp', doc="Regular expression to use")


@_with_fields('field')
class GeoDistanceQuery(Query):
    def __init__(self, distance, location, **kwargs):
        """
        Search for items within a given radius
        :param distance: The distance string specifying the radius
        :param location: A tuple of `(lon, lat)` indicating point of origin
        """
        super(GeoDistanceQuery, self).__init__()
        kwargs['distance'] = distance
        kwargs['location'] = location
        _assign_kwargs(self, kwargs)

    location = _genprop(_location_conv, 'location', doc='Location')
    distance = _genprop_str('distance')


@_with_fields('field')
class GeoBoundingBoxQuery(Query):
    def __init__(self, top_left, bottom_right, **kwargs):
        super(GeoBoundingBoxQuery, self).__init__()
        kwargs['top_left'] = top_left
        kwargs['bottom_right'] = bottom_right
        _assign_kwargs(self, kwargs)

    top_left = _genprop(
        _location_conv, 'top_left',
        doc='Tuple of `(lat, lon)` for the top left corner of bounding box')
    bottom_right = _genprop(
        _location_conv, 'bottom_right',
        doc='Tuple of `(lat, lon`) for the bottom right corner of bounding box')


@_with_fields('field')
class NumericRangeQuery(_RangeQuery):
    """
    Search documents for fields containing a value within a given numerical
    range.

    At least one of `min` or `max` must be specified.
    """
    def __init__(self, min=None, max=None, **kwargs):
        """
        :param float min: See :attr:`min`
        :param float max: See :attr:`max`
        """
        super(NumericRangeQuery, self).__init__(min, max, **kwargs)

    min = _genprop(
        float, 'min', doc='Lower bound of range. See :attr:`min_inclusive`')

    min_inclusive = _genprop(
        bool, 'inclusive_min',
        doc='Whether matches are inclusive of lower bound')

    max = _genprop(
        float, 'max',
        doc='Upper bound of range. See :attr:`max_inclusive`')

    max_inclusive = _genprop(
        bool, 'inclusive_max',
        doc='Whether matches are inclusive of upper bound')

    _MINMAX = 'min', 'max'


@_with_fields('field')
class DateRangeQuery(_RangeQuery):
    """
    Search documents for fields containing a value within a given date
    range.

    The date ranges are parsed according to a given :attr:`datetime_parser`.
    If no parser is specified, the RFC 3339 parser is used. See
    `Generating an RFC 3339 Timestamp <http://goo.gl/LIkV7G>_`.

    The :attr:`start` and :attr:`end` parameters should be specified in the
    constructor. Note that either `start` or `end` (but not both!) may be
    omitted.

    .. code-block:: python

        DateRangeQuery(start='2014-12-25', end='2016-01-01')
    """
    def __init__(self, start=None, end=None, **kwargs):
        """
        :param str start: Start of date range
        :param str end: End of date range
        :param kwargs: Additional options: :attr:`field`, :attr:`boost`
        """
        super(DateRangeQuery, self).__init__(start, end, **kwargs)

    start = _genprop_str('start', doc='Lower bound datetime')
    end = _genprop_str('end', doc='Upper bound datetime')

    start_inclusive = _genprop(
        bool, 'inclusive_start', doc='If :attr:`start` is inclusive')

    end_inclusive = _genprop(
        bool, 'inclusive_end', doc='If :attr:`end` is inclusive')

    datetime_parser = _genprop_str(
        'datetime_parser',
        doc="""
        Parser to use when analyzing the :attr:`start` and :attr:`end` fields
        on the server.

        If not specified, the RFC 3339 parser is used.
        Ensure to specify :attr:`start` and :attr:`end` in a format suitable
        for the given parser.
        """)

    _MINMAX = 'start', 'end'


@_with_fields('field')
class TermRangeQuery(_RangeQuery):
    """
    Search documents for fields containing a value within a given
    lexical range.
    """
    def __init__(self, start=None, end=None, **kwargs):
        super(TermRangeQuery, self).__init__(start=start, end=end, **kwargs)

    start = _genprop_str('start', doc='Lower range of term')

    end = _genprop_str('end', doc='Upper range of term')

    start_inclusive = _genprop(
        bool, 'inclusive_start', doc='If :attr:`start` is inclusive')

    end_inclusive = _genprop(
        bool, 'inclusive_end', doc='If :attr:`end` is inclusive')

    _MINMAX = 'start', 'end'


class ConjunctionQuery(_CompoundQuery):
    """
    Compound query in which all sub-queries passed must be satisfied
    """
    _COMPOUND_FIELDS = ('conjuncts', 'conjuncts'),

    def __init__(self, *queries):
        super(ConjunctionQuery, self).__init__()
        self.conjuncts = list(queries)

    def validate(self):
        super(ConjunctionQuery, self).validate()
        if not self.conjuncts:
            raise NoChildrenError('No sub-queries')


class DisjunctionQuery(_CompoundQuery):
    """
    Compound query in which at least :attr:`min` or more queries must be
    satisfied
    """
    _COMPOUND_FIELDS = ('disjuncts', 'disjuncts'),

    def __init__(self, *queries, **kwargs):
        super(DisjunctionQuery, self).__init__()
        _assign_kwargs(self, kwargs)
        self.disjuncts = list(queries)
        if 'min' not in self._json_:
            self.min = 1

    min = _genprop(
        _convert_gt0, 'min', doc='Number of queries which must be satisfied')

    def validate(self):
        super(DisjunctionQuery, self).validate()
        if not self.disjuncts or len(self.disjuncts) < self.min:
            raise NoChildrenError('No children specified, or min is too big')


class BooleanQuery(Query):
    def __init__(self, must=None, should=None, must_not=None):
        super(BooleanQuery, self).__init__()
        self._subqueries = {}
        self.must = must
        self.should = should
        self.must_not = must_not

    must = _bprop_wrap(
        'must', ConjunctionQuery,
        """
        Queries which must be satisfied. When setting this attribute, the
        SDK will convert value to a :class:`ConjunctionQuery` if the value
        is a list of queries.
        """)

    must_not = _bprop_wrap(
        'must_not', DisjunctionQuery,
        """
        Queries which must not be satisfied. Documents found which satisfy
        the queries in this clause are not returned in the match.

        When setting this attribute in the SDK, it will be converted to a
        :class:`DisjunctionQuery` if the value is a list of queries.
        """)

    should = _bprop_wrap(
        'should', DisjunctionQuery,
        """
        Specify additional queries which should be satisfied. As opposed to
        :attr:`must`, you can specify the number of queries in this field
        which must be satisfied.

        The type of this attribute is :class:`DisjunctionQuery`, and you can
        set the minimum number of queries to satisfy using::

            boolquery.should.min = 1
        """)

    @property
    def encodable(self):
        # Overrides the default `encodable` implementation in order to
        # serialize any sub-queries
        for src, tgt in ((self.must, 'must'),
                         (self.must_not, 'must_not'),
                         (self.should, 'should')):
            if src:
                self._json_[tgt] = src.encodable
        return super(BooleanQuery, self).encodable

    def validate(self):
        super(BooleanQuery, self).validate()
        if not self.must and not self.must_not and not self.should:
            raise ValueError('No sub-queries specified', self)


class MatchAllQuery(Query):
    """
    Special query which matches all documents
    """
    def __init__(self, **kwargs):
        super(MatchAllQuery, self).__init__()
        self._json_['match_all'] = None
        _assign_kwargs(self, kwargs)


class MatchNoneQuery(Query):
    """
    Special query which matches no documents
    """
    def __init__(self, **kwargs):
        super(MatchNoneQuery, self).__init__()
        self._json_['match_none'] = None
        _assign_kwargs(self, kwargs)


@_with_fields('field')
class BooleanFieldQuery(_SingleQuery):
    _TERMPROP = 'bool'
    bool = _genprop(bool, 'bool', doc='Boolean value to search for')


def make_search_body(index, query, params=None):
    """
    Generates a dictionary suitable for encoding as the search body
    :param index: The index name to query
    :param query: The query itself
    :param params: Modifiers for the query
    :type params: :class:`couchbase_core.fulltext.Params`
    :return: A dictionary suitable for serialization
    """
    dd = {}

    if not isinstance(query, Query):
        query = QueryStringQuery(query)

    dd['query'] = query.encodable
    if params:
        dd.update(params.as_encodable(index))
    dd['indexName'] = index
    return dd


RegexpQuery = RegexQuery
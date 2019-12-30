from typing import *

from couchbase.JSONdocument import JSONDocument
from .options import OptionBlock, timedelta
from couchbase_core import abstractmethod, IterableWrapper, JSON

from couchbase_core.fulltext import SearchRequest
from datetime import timedelta
from couchbase_core._pyport import Protocol


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


class SearchRowLocations(Protocol):
    def get_all(self):
         # type: (...) -> List[SearchRowLocation]
         # list all locations (any field, any term)
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
        """List all terms in this locations,
        considering all fields (so a set):"""
        pass

    def terms_for(self,
                  field  # type:str
                  ):

        # type: (...) -> list[str]
        """ list the terms for a given field """
        pass

"""SearchRowLocation
interface SearchRowLocation {
    String Field();
String Term();
uint32 Pos;
uint32 Start;
uint32 End;
Optional<uint32[]> ArrayPositions();
}
SearchFacetResult
An individual facet result has both metadata and details, as each facet can define ranges into which results are categorized.
interface SearchFacetResult {
    String Name();
String Field();
uint64 Total();
uint64 Missing();
uint64 Other();
}
Sample request/response payloads: https://github.com/couchbaselabs/sdk-testcases/tree/master/search

If top-level "error" property exists, then SDK should build and throw CouchbaseException with its content.
SearchMetrics
interface SearchMetrics {
    Duration Took();
uint64 TotalRows();
double MaxScore();
uint64 TotalPartitionCount(); // SuccessPartitionCount + ErrorPartitionCount
uint64 SuccessPartitionCount();
uint64 ErrorPartitionCount();
}"""


class SearchOptions(OptionBlock):
    pass


class SearchMetaData(Protocol):
    """Represents the meta-data returned along with a search query result."""
    def metrics(self):
        # type: (...) -> SearchMetrics
        pass

    def errors(self):
        # type: (...) -> Mapping[str,Exception]
        pass


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


class MetaData(MetaDataProtocol):
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
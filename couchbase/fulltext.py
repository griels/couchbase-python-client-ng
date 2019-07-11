from typing import *
from couchbase import OptionBlock
from couchbase_core import abstractmethod, IterableWrapper, JSON

from couchbase_core.fulltext import Facet, SearchRequest

SearchQueryRow = JSON

MetaData = JSON


class SearchOptions(OptionBlock):
    pass


class ISearchResult(object):
    @abstractmethod
    def hits(self):
        # type: (...)->List[SearchQueryRow]
        pass

    @abstractmethod
    def facets(self):
        # type: (...)->Mapping[str, Facet]
        pass

    @abstractmethod
    def metadata(self):
        # type: (...)->MetaData
        pass


class SearchResult(ISearchResult, IterableWrapper):
    def __init__(self,
                 raw_result  # type: SearchRequest
                 ):
        IterableWrapper.__init__(self, raw_result)

    def hits(self):
        # type: (...)->Iterable[JSON]
        return list(x for x in self)

    def facets(self):
        # type: (...)->Mapping[str,Facet]
        return self.parent.facets

    def metadata(self):  # type: (...)->MetaData
        return IterableWrapper.metadata(self)

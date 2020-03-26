from couchbase import ViewResult, QueryResult, AnalyticsResult, SearchResult
from couchbase_core.asynchronous.analytics import AsyncAnalyticsRequest
from couchbase_core.asynchronous.n1ql import AsyncN1QLRequest
from couchbase_core.asynchronous.view import AsyncViewBase
from couchbase_core.asynchronous.fulltext import AsyncSearchRequest


class AsyncViewResultBase(AsyncViewBase, ViewResult):
    def __init__(self, *args, **kwargs):
        """
        Initialize a new AsyncViewBase object. This is intended to be
        subclassed in order to implement the require methods to be
        invoked on error, data, and row events.

        Usage of this class is not as a standalone, but rather as
        an ``itercls`` parameter to the
        :meth:`~couchbase_core.connection.Connection.query` method of the
        connection object.
        """
        ViewResult.__init__(self, *args, **kwargs)


class AsyncQueryResultBase(AsyncN1QLRequest, QueryResult):
    def __init__(self, *args, **kwargs):
        """
        Initialize a new AsyncViewBase object. This is intended to be
        subclassed in order to implement the require methods to be
        invoked on error, data, and row events.

        Usage of this class is not as a standalone, but rather as
        an ``itercls`` parameter to the
        :meth:`~couchbase_core.connection.Connection.query` method of the
        connection object.
        """
        QueryResult.__init__(self, *args, **kwargs)


class AsyncAnalyticsResultBase(AsyncAnalyticsRequest, AnalyticsResult):
    def __init__(self, *args, **kwargs):
        """
        Initialize a new AsyncViewBase object. This is intended to be
        subclassed in order to implement the require methods to be
        invoked on error, data, and row events.

        Usage of this class is not as a standalone, but rather as
        an ``itercls`` parameter to the
        :meth:`~couchbase_core.connection.Connection.query` method of the
        connection object.
        """
        AnalyticsResult.__init__(self, *args, **kwargs)


class AsyncSearchResult(AsyncSearchRequest, SearchResult):
    def __init__(self, *args, **kwargs):
        """
        Initialize a new AsyncViewBase object. This is intended to be
        subclassed in order to implement the require methods to be
        invoked on error, data, and row events.

        Usage of this class is not as a standalone, but rather as
        an ``itercls`` parameter to the
        :meth:`~couchbase_core.connection.Connection.query` method of the
        connection object.
        """
        SearchResult.__init__(self, *args, **kwargs)
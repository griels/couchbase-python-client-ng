from typing import TypeVar, Callable, Type

from couchbase.result import ViewResult
from couchbase.n1ql import QueryResult
from couchbase.analytics import AnalyticsResult
from couchbase.search import SearchResult
from couchbase_core import IterableClass
from couchbase_core.asynchronous.view import AsyncViewBase
from couchbase.asynchronous.search import AsyncSearchRequest
from couchbase_core.asynchronous.rowsbase import AsyncRowsBase

import functools
import boltons.funcutils
iterable_producer = TypeVar('iterable_producer', bound=Callable)
import logging

def wrap_async_decorator(method,   # type: iterable_producer
                         default_iterator=None  # type: Type[IterableClass]
                         ):
    # type: (...) -> iterable_producer

    def wrap(func):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            return func(self, *args, itercls=kwargs.pop('itercls',default_iterator), **kwargs)
        wrapper.__annotations__=method.__annotations__
        if 'itercls' in wrapper.__annotations__ and iterable_producer:
            wrapper.__annotations__['itercls'] = Type[default_iterator]
            wrapper.__annotations__['return'] = default_iterator
        else:
            rtype = method.__annotations__.get('return', object)
            try:
                rtype_name=getattr(rtype,'__qualname__', str(rtype))
                logging.error("wrapping rtype {} for {} - got {}".format(rtype, method, rtype_name))
                wrapper.__annotations__['return'] = 'asyncio.futures.Future[{}]'.format(rtype_name)
            except Exception as e:
                raise
        wrapper.__doc__ = """{} version of `{}`.\n{}""".format('asyncio', method.__module__+"."+method.__qualname__, method.__doc__)
        return wrapper
    return boltons.funcutils.partial(wrap)


def wrap_async(method,  # type: iterable_producer
               default_iterator  # type: Type[IterableClass]
               ):
    # type: (...) -> iterable_producer

    @functools.wraps(method)
    def wrapper_raw(self,
                    *args,
                    **kwargs
                    ):
        return method(self, *args, itercls=kwargs.pop('itercls',default_iterator),**kwargs)

    fresh = boltons.funcutils.FunctionBuilder.from_func(method)
    try:
        fresh.remove_arg('itercls')
    except ValueError:
        pass
    fresh.add_arg('itercls', default_iterator, kwonly=True)
    method_with_itercls = fresh.get_func()
    method_with_itercls.__annotations__['itercls'] = Type[default_iterator]
    method_with_itercls.__annotations__['return'] = default_iterator
    wrapper = boltons.funcutils.update_wrapper(wrapper_raw, method_with_itercls)
    wrapper.__annotations__ = method.__annotations__
    wrapper.__doc__ += """
    :param itercls: type of the iterable class to be returned, :class:`{}` by default""".format(
        default_iterator.__name__)
    return wrapper


class AsyncViewResult(AsyncViewBase, ViewResult):
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


class AsyncQueryResult(AsyncRowsBase, QueryResult):
    def __init__(self, *args, **kwargs):
        QueryResult.__init__(self, *args, **kwargs)


class AsyncQueryResultBase(AsyncQueryResult, QueryResult):
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


class AsyncAnalyticsResult(AsyncRowsBase, AnalyticsResult):
    def __init__(self, *args, **kwargs):
        AnalyticsResult.__init__(self, *args, **kwargs)


class AsyncAnalyticsResultBase(AsyncAnalyticsResult, AnalyticsResult):
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
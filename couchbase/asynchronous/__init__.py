from abc import ABC

import inspect
import sys
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
import typing
import logging
import textwrap
import re

iterable_producer = TypeVar('iterable_producer', bound=Callable)

_type_pattern = re.compile(r'.*\(\.\.\.\)\s\-\>\s*(.*?)$')


def get_return_type(method):
    try:
        hints = typing.get_type_hints(method)
    except Exception as e:
        return "object"
    rtype = hints.get('return', None)
    if rtype:
        return str(rtype)
    type_comment = "object"
    parse_kwargs = {}
    if sys.version_info < (3, 8):
        try:
            import typed_ast.ast3 as ast
        except ImportError:
            return 'object'
    else:
        import ast
        parse_kwargs = {'type_comments': True}
    try:
        obj_ast = ast.parse(textwrap.dedent(inspect.getsource(method)), **parse_kwargs)
    except (OSError, TypeError):
        return "object"

    def _one_child(module):
        children = module.body  # use the body to ignore type comments

        if len(children) != 1:
            logging.warning(
                'Did not get exactly one node from AST for "%s", got %s', str(method), len(children))
            return

        return children[0]

    obj_ast = _one_child(obj_ast)
    if obj_ast is None:
        pass

    try:
        matches = _type_pattern.search(obj_ast.type_comment).groups('object')
        type_comment = matches[0]
    except Exception as e:
        pass
    return type_comment


class AsyncDecorator(functools.partial):
    @staticmethod
    def __new__(cls, method, *args, **kwargs):
        return super(AsyncDecorator, cls).__new__(cls, method, *args, **kwargs)


# noinspection PyPep8Naming
class async_iterable(AsyncDecorator):
    @staticmethod
    def __new__(cls, method,  # type: iterable_producer
                 default_iterator  # type: Type[IterableClass]
                 ):
        result=super(async_iterable, cls).__new__(cls, method)
        result._default_iterator=default_iterator
        return result

    def __call__(self,  # type: async_iterable
                 func, *args, **kwargs):
        # type: (...) -> iterable_producer
        def_iterator=self._default_iterator
        @functools.wraps(self.func)
        def wrapper(self, *args, **kwargs):
            return func(self, *args, itercls=kwargs.pop('itercls', def_iterator), **kwargs)
        wrapper.__annotations__['itercls'] = Type[self._default_iterator]
        wrapper.__annotations__['return'] = self._default_iterator
        return wrapper


# noinspection PyPep8Naming
class async_kv_operation(AsyncDecorator):
    @staticmethod
    def __new__(cls, method):
        return super(async_kv_operation, cls).__new__(cls, method)

    def __call__(self,  # type: async_iterable
                 func, *args, **kwargs):
        @functools.wraps(self.func)
        def wrapper(self, *args, **kwargs):
            return func(self, *args, **kwargs)
        rtype_name = get_return_type(self.func)

        try:
            logging.error("wrapping rtype for {} - got {}".format(self.func, rtype_name))
            wrapper.__annotations__['return'] = 'asyncio.futures.Future[{}]'.format(rtype_name)
        except Exception as e:
            raise
        return wrapper

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


class AsyncViewResult(AsyncViewBase, ViewResult, ABC):
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


class AsyncQueryResult(AsyncRowsBase, QueryResult, ABC):
    def __init__(self, *args, **kwargs):
        QueryResult.__init__(self, *args, **kwargs)


class AsyncQueryResultBase(AsyncQueryResult, QueryResult, ABC):
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


class AsyncAnalyticsResult(AsyncRowsBase, AnalyticsResult, ABC):
    def __init__(self, *args, **kwargs):
        AnalyticsResult.__init__(self, *args, **kwargs)


class AsyncAnalyticsResultBase(AsyncAnalyticsResult, AnalyticsResult, ABC):
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


class AsyncSearchResult(AsyncSearchRequest, SearchResult, ABC):
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
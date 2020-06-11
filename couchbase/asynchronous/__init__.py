from abc import ABC

import inspect
import sys
from typing import TypeVar, Callable

from couchbase.n1ql import QueryResult
from couchbase.analytics import AnalyticsResult
from couchbase.search import SearchResult
from couchbase_core import IterableClass
from couchbase_core.asynchronous.view import AsyncViewBase
from couchbase.asynchronous.search import AsyncSearchRequest
from couchbase_core.asynchronous.rowsbase import AsyncRowsBase

import functools
import boltons.funcutils
import logging
import textwrap
import re
import os
import sys
iterable_producer = TypeVar('iterable_producer', bound=Callable)

_type_pattern = re.compile(r'.*\(\.\.\.\)\s\-\>\s*(.*?)$')


def get_type_hints_comments(method):
    parse_kwargs = {}
    if sys.version_info < (3, 8):
        try:
            import typed_ast.ast3 as ast
        except ImportError:
            return None
    else:
        import ast
        parse_kwargs = {'type_comments': True}
    try:
        return ast.parse(textwrap.dedent(inspect.getsource(method)), **parse_kwargs)
    except (OSError, TypeError):
        return None


def get_return_type_str(method):

    obj_ast = get_type_hints_comments(method)
    if not obj_ast:
        return "object"

    def _one_child(module):
        children = module.body  # use the body to ignore type comments

        if len(children) != 1:
            logging.warning(
                'Did not get exactly one node from AST for "%s", got %s', str(method), len(children))
            return

        return children[0]

    obj_ast = _one_child(obj_ast)

    try:
        matches = _type_pattern.search(obj_ast.type_comment).groups('object')
        return matches[0]
    except Exception as e:
        return None


from couchbase.result import *


def get_return_type(func):
    rtype_str = get_return_type_str(func)
    co_obj = compile("{}".format(rtype_str), '<string>', 'eval')
    result = eval(co_obj, globals(), locals())
    return result


class AsyncDecorator(object):
    @staticmethod
    def __new__(cls, method, rtype, *args, **kwargs):
        result = super(AsyncDecorator, cls).__new__(cls, *args, **kwargs)
        result.func = method
        result.rtype = rtype
        return result

    def update_wrapper(self, wrapper, **kwargs):
        type_annotations = getattr(self.func,'__annotations__', getattr(wrapper, '__annotations__', {}))
        if type_annotations:
            type_annotations=dict(**type_annotations)
        else:
            try:
                type_annotations = get_type_hints(self.func)
            except:
                pass
        wrapper.__annotations__ =type_annotations
        wrapper.__annotations__['return'] = self.rtype
        wrapper.__annotations__.update(**kwargs)
        return wrapper


# noinspection PyPep8Naming
class async_iterable(AsyncDecorator):
    @staticmethod
    def __new__(cls, method,  # type: iterable_producer
                default_iterator  # type: Type[IterableClass]
                ):
        result = super(async_iterable, cls).__new__(cls, method, default_iterator)
        return result

    def __call__(self,  # type: async_iterable
                 func,  # type: iterable_producer
                 *args, **kwargs):
        # type: (...) -> iterable_producer
        def_iterator = self.rtype

        @functools.wraps(self.func)
        def wrapper(self, *args, **kwargs):
            return func(self, *args, itercls=kwargs.pop('itercls', def_iterator), **kwargs)

        return self.update_wrapper(wrapper, itercls=Type[self.rtype])


# noinspection PyPep8Naming
class async_kv_operation(AsyncDecorator):
    @staticmethod
    def __new__(cls, method, rtype):
        return super(async_kv_operation, cls).__new__(cls, method, rtype)

    def __call__(self,  # type: async_iterable
                 func, *args, **kwargs):
        @functools.wraps(self.func)
        def wrapper(self, *args, **kwargs):
            return func(self, *args, **kwargs)

        return self.update_wrapper(wrapper)


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
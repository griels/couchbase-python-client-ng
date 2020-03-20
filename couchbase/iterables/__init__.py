from typing import Union, Iterable, Any

from couchbase_core import StopAsyncIteration
from typing import *
IterableQuery = Iterable[Any]

#from couchbase.search import SearchRequest
#from couchbase_core.n1ql import N1QLRequest
#from couchbase_core.views.iterator import View

#IterableQuery = Union[SearchRequest, N1QLRequest, View]

WrappedIterable = TypeVar('T', bound=IterableQuery)

def iterable_wrapper(basecls  # type: Type[WrappedIterable]
                     ):
    # type: (...) -> Type['IterableWrapper']
    class IterableWrapper(basecls):
        def __init__(self,
                     *args, **kwargs  # type: IterableQuery
                     ):
            super(IterableWrapper, self).__init__(*args, **kwargs)
            self.done = False
            self.buffered_rows = []

        def metadata(self):
            # type: (...) -> JSON
            return self.meta

        def __iter__(self):
            for row in self.buffered_rows:
                yield row
            parent_iter = super(IterableWrapper, self).__iter__()
            while not self.done:
                try:
                    next_item = next(parent_iter)
                    self.buffered_rows.append(next_item)
                    yield next_item
                except (StopAsyncIteration, StopIteration) as e:
                    self.done = True
                    break
    return IterableWrapper
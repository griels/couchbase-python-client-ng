from abc import abstractmethod
from typing import *

import attr
import datetime

from functools import wraps
from couchbase_core._libcouchbase import Result as CoreResult

from couchbase.diagnostics import EndpointPingReport, ServiceType
from couchbase_core import iterable_wrapper, JSON
from couchbase_core.result import AsyncResult as CoreAsyncResult
from couchbase_core.result import MultiResult, SubdocResult
from couchbase_core.subdocument import Spec
from couchbase_core.supportability import internal
from couchbase_core.transcodable import Transcodable
from couchbase_core.views.iterator import View as CoreView
from .options import forward_args, UnsignedInt64
from collections import defaultdict

Proxy_T = TypeVar('Proxy_T')


# full means we are doing a subdoc lookup_in, and want to only
# get the results of the get_full().  Special case for a get where
# with_expiry=True.  Also this is a hack.
def canonical_sdresult(content, full=False):
    sdresult = content  # type: SubdocResult
    result = {}
    if full:
        return content.get_full
    cursor = iter(sdresult)
    for index in range(0, sdresult.result_count):
        spec = sdresult._specs[index]  # type: Spec
        result[spec[1]] = next(cursor)
    return result


# full means we are doing a subdoc lookup_in, and want to only
# get the results of the get_full().  Special case for a get where
# with_expiry=True.  Also this is a hack.
def extract_value(content, decode_canonical, full=False):
    if isinstance(content, MultiResult):
        return {k: decode_canonical(content[k].value) for k, v, in content}
    elif isinstance(content, SubdocResult):
        return decode_canonical(canonical_sdresult(content, full))
    return decode_canonical(content.value)


def get_decoder(item  # type: Type[Union[Transcodable,Any]]
                ):
    return getattr(item, 'decode_canonical', None) if issubclass(item, Transcodable) else item


class ContentProxy(object):
    """
    Used to provide access to Result content via Result.content_as[type]
    """

    @internal
    def __init__(self, content, full=False):
        self.content = content
        self.full = full

    def __getitem__(self,
                    item       # type: Type[Proxy_T]
                    ):
        # type: (...) -> Union[Proxy_T, Mapping[str,Proxy_T]]
        """

        :param item: the type to attempt to cast the result to
        :return: the content cast to the given type, if possible
        """
        return extract_value(self.content, get_decoder(item), self.full)


class ContentProxySubdoc(object):
    """
    Used to provide access to Result content via Result.content_as[type]
    """

    @internal
    def __init__(self, content):
        self.content = content

    def index_proxy(self, item, index):
        return get_decoder(item)(self.content[index])

    def __getitem__(self,
                    item  # type: Type[Proxy_T]
                    ):
        # type: (...) -> Callable[[int],Union[Proxy_T,Mapping[str,Proxy_T]]]
        """
        Returns a proxy for an array of subdoc results cast to the given type

        :param item: type to cast the array elements to
        :return: the proxy, which is callable with an index to extract from the array and cast
        """
        return lambda index: self.index_proxy(item, index)


class Result(object):
    @internal
    def __init__(self,
                 original  # type: CoreResult
                 ):
        # type: (...) -> None
        """
        This is the base implementation for SDK3 results

        :param int cas: CAS value
        :param Optional[int] error: error code if applicable
        """
        self._original = original

    @property
    def cas(self):
        # type: () -> int
        """
        The CAS value

        :return: the CAS value
        """
        return self._original.cas

    @property
    def error(self):
        # type: () -> int
        return self._original.rc

    @property
    def success(self):
        # type: () -> bool
        return not self.error

    TracingOutput = Dict[str, Any]

    @property
    def _tracing_output(self):
        # type: () -> TracingOutput
        return self._original.tracing_output

    __async_map = {}

    @classmethod
    def _async(cls):
        return Result._async_retarget(cls)

    @staticmethod
    def _async_retarget(cls):
        result = Result.__async_map.get(cls, None)
        if not result:
            result = AsyncWrapper.gen_wrapper(cls)
            Result.__async_map[cls] = result
        return result

    @classmethod
    def _from_raw(cls, orig_value):
        return Result._from_raw_retarget(cls, orig_value)

    @staticmethod
    def _from_raw_retarget(cls, orig_value):
        return (cls._async() if _is_async(orig_value) else cls)(orig_value)


class LookupInResult(Result):
    @internal
    def __init__(self,
                 original,  # type: CoreResult
                 **kwargs  # type: Any
                 ):
        # type: (...) -> None
        """
        LookupInResult is the return type for lookup_in operations.
        """
        super(LookupInResult, self).__init__(original)
        self.dict = kwargs

    @property
    def content_as(self):
        # type: (...) -> ContentProxySubdoc
        """
        Return a proxy that allows extracting the content as a provided type.

        Get first value as a string::

            value = cb.get('key').content_as[str](0)

        :return: returns as ContentProxySubdoc
        """
        return ContentProxySubdoc(self._original)

    def exists(self,
               index  # type: int
               ):
        return len(canonical_sdresult(self._original)) > index

    @property
    def expiry(self):
        return self._original.expiry

    def __len__(self):
        return len(canonical_sdresult(self._original))


class MutationResult(Result):
    def __init__(self,
                 original  # type: CoreResult
                 ):
        super(MutationResult, self).__init__(original)
        mutinfo = getattr(original, '_mutinfo', None)
        muttoken = MutationToken(mutinfo) if mutinfo else None
        self.mutationToken = muttoken

    def mutation_token(self):
        # type: () -> MutationToken
        return self.mutationToken


class MutateInResult(MutationResult):
    @internal
    def __init__(self,
                 content,  # type: CoreResult
                 **options  # type: Any
                 ):
        # type: (...) -> None
        """
        MutateInResult is the return type for mutate_in operations.
        """
        super(MutateInResult, self).__init__(content)
        self._content = content  # type: CoreResult
        self.dict = options

    @property
    def content_as(self):
        # type: (...) -> ContentProxySubdoc
        """
        Return a proxy that allows extracting the content as a provided type.

        Get first result as a string::

            cb.mutate_in('user',
                          SD.array_addunique('tags', 'dog'),
                          SD.counter('updates', 1)).content_as[str](0)

        :return: returns a :class:`~.ContentProxySubdoc`
        """
        return ContentProxySubdoc(self._content)

    @property
    def key(self):
        # type: (...) -> str
        """ Original key of the operation """
        return self._content.key


class PingResult(object):
    @internal
    def __init__(self,
                 original  # type: Mapping[str, Any]
                 ):
        self._id = original.get("id", None)
        self._sdk = original.get("sdk", None)
        self._version = original.get("version", None)
        self._endpoints = dict()
        for k, v in original['services'].items():
            # construct an EndpointPingReport for each
            k = ServiceType(k)
            self._endpoints[k] = list()
            for value in v:
                if value:
                    self._endpoints[k].append(EndpointPingReport(k, value))

    @property
    def endpoints(self):
        return self._endpoints

    @property
    def id(self):
        # the actual format is "0xdeaddeadbeef/<the string you passed in the options>"
        return self._id

    @property
    def sdk(self):
        return self._sdk

    @property
    def version(self):
        return self._version

    @classmethod
    def _async(cls):
        return Result._async_retarget(cls)

    @classmethod
    def _from_raw(cls, orig_value):
        return Result._from_raw_retarget(cls, orig_value)


class ExistsResult(Result):
    @internal
    def __init__(self,
                 original  # type: CoreResult
                 ):
        super(ExistsResult, self).__init__(original)

    @property
    def exists(self):
        return self._original.cas != 0


class GetResult(Result):
    @internal
    def __init__(self,
                 original
                 ):
        """
        GetResult is the return type for full read operations.
        """
        super(GetResult, self).__init__(original)
        self._id = original.key
        self._original = original
        self._full = False
        self._expiry = None
        if isinstance(original, SubdocResult):
            self._expiry = original.expiry
            self._full = bool(original.get_full)

    @property
    def id(self  # type: GetResult
           ):
        # type: (...) -> str
        return self._id

    @property
    def expiry(self  # type: GetResult
               ):
        # type: (...) -> datetime.datetime
        return self._expiry

    @property
    def content_as(self  # type: GetResult
                   ):
        # type: (...) -> ContentProxy
        return ContentProxy(self._original, self._full)

    @property
    def content(self  # type: GetResult
                ):
        # type: (...) -> Any
        return extract_value(self._original, lambda x: x, self._full)


class GetReplicaResult(GetResult):
    @property
    def is_replica(self):
        raise NotImplementedError("To be implemented in final sdk3 release")


class MultiResultBase(dict):
    single_result_type = None  # type: Type[ResultDeriv]

    @property
    def all_ok(self):
        return self._raw_result.all_ok

    def __init__(self, raw_result):
        self._raw_result = raw_result
        super(MultiResultBase, self).__init__({k: self.single_result_type._from_raw(v) for k, v in raw_result.items()})

    @classmethod
    def _async(cls):
        return Result._async_retarget(cls)

    @classmethod
    def _from_raw(cls, orig_value):
        return Result._from_raw_retarget(cls, orig_value)

    @classmethod
    def _gen_result_class(cls,  # type: Type[MultiResultBase]
                          item  # type: Type[ResultDeriv]
                          ):
        # type: (...) -> Type[MultiResultBase]
        class Result(MultiResultBase):
            single_result_type = item
        return Result


ResultDeriv = TypeVar('ResultDeriv', bound=Union[Result, MultiResultBase, PingResult])
R = TypeVar('R', bound=ResultDeriv)


class SyncOperation(Protocol[R]):
    def __call__(self,
                 target,  # type: CoreClient
                 *args,  # type: Any
                 **kwargs  # type: Any
                 ):
        # type: (...) -> R
        pass


class AsyncResult(object):
    def __init__(self,
                 core_result,
                 **kwargs):
        self._original = core_result
        self._kwargs = kwargs

    @property
    @abstractmethod
    def orig_class(self):
        # type: (...) -> Type[ResultDeriv]
        pass

    def set_callbacks(self, on_ok_orig, on_err_orig):
        def on_ok(res):
            on_ok_orig(self.orig_class(res, **self._kwargs))

        def on_err(res, excls, excval, exctb):
            on_err_orig(res, excls, excval, exctb)

        self._original.set_callbacks(on_ok, on_err)

    def clear_callbacks(self, *args):
        self._original.clear_callbacks(*args)


class AsyncWrapper(object):
    @staticmethod
    def gen_wrapper(base  # type: Type[ResultDeriv]
                    ):
        # type: (...) -> Type[Union[ResultDeriv, AsyncResult]]
        class Wrapped(AsyncResult, base):
            @property
            def orig_class(self):
                # type: (...) -> Type[ResultDeriv]
                return base
        return Wrapped


# TODO: eliminate the options shortly.  They serve no purpose
ResultPrecursor = NamedTuple('ResultPrecursor', [('orig_result', CoreResult), ('orig_options', Mapping[str, Any])])


def _is_async(orig_result  # type: CoreResult
              ):
    return _is_async_type(type(orig_result))


def _is_async_type(res_type):
    return issubclass(res_type, CoreAsyncResult)


def get_result_wrapper(func  # type: Callable[[Any], ResultPrecursor]
                       ):
    # type: (...) -> Callable[[Any], GetResult]
    @wraps(func)
    def wrapped(*args, **kwargs):
        return GetResult._from_raw(next(iter(func(*args, **kwargs))))

    return wrapped


def get_replica_result_wrapper(func  # type: Callable[[Any], ResultPrecursor]
                               ):
    # type: (...) -> Callable[[Any], GetReplicaResult]

    @wraps(func)
    def wrapped(*args, **kwargs):
        x = list(map(GetReplicaResult._from_raw, func(*args, **kwargs)))
        if len(x) > 1:
            return x
        return x[0]

    return wrapped


class MutationToken(object):
    def __init__(self, token):
        token = token or (None, None, None)
        (self.vbucketId, self.vbucketUUID, self.sequenceNumber) = token

    def partition_id(self):
        # type: (...) -> int
        return self.vbucketId

    def partition_uuid(self):
        # type: (...) -> int
        return self.vbucketUUID

    def sequence_number(self):
        # type: (...) -> int
        return self.sequenceNumber

    def bucket_name(self):
        # type: (...) -> str
        raise NotImplementedError()


class MultiGetResult(MultiResultBase._gen_result_class(GetResult)):
    pass


class MultiMutationResult(MultiResultBase._gen_result_class(MutationResult)):
    pass


class MultiResultWrapper(object):
    def __init__(self,  # type: MultiResultWrapper
                 orig_result_type  # type: Type[MultiResultBase]
                 ):
        # type: (...) -> None
        self.orig_result_type = orig_result_type

    def __call__(self, target, wrapped, keys, *options, **kwargs):
        # type: (...) -> Type[MultiResultBase]
        raw_result = wrapped(target, keys, **forward_args(kwargs, *options))
        return self.orig_result_type._from_raw(getattr(raw_result, 'orig_result', raw_result))


get_multi_mutation_result = MultiResultWrapper(MultiMutationResult)
get_multi_get_result = MultiResultWrapper(MultiGetResult)


def _wrap_in_mutation_result(func  # type: Callable[[Any,...],CoreResult]
                             ):
    # type: (...) -> Callable[[Any,...],MutationResult]
    @wraps(func)
    def mutated(*args, **kwargs):
        result = func(*args, **kwargs)
        return MutationResult._from_raw(getattr(result, 'orig_result', result))

    return mutated


@attr.s
class ViewRow(object):
    key = attr.ib()
    value = attr.ib(default=object)
    id = attr.ib(default=str)
    document = attr.ib(default=object)


class ViewMetaData(object):
    def __init__(self,
                 parent  # type: CoreView
                 ):
        self._parent = parent

    def total_rows(self  # type: ViewMetaData
                   ):
        # type: (...) -> UnsignedInt64
        return self._parent.rows_returned

    def debug(self  # type: ViewMetaData
              ):
        # type: (...) -> JSON
        return self._parent.debug


class ViewResult(iterable_wrapper(CoreView)):
    def __init__(self, *args, row_factory=ViewRow, **kwargs  # type: CoreView
                 ):
        super(ViewResult, self).__init__(*args, row_factory=row_factory, **kwargs)

    def metadata(self  # type: ViewResult
                 ):
        # type: (...) -> ViewMetaData
        return ViewMetaData(self)


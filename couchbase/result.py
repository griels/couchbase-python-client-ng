from couchbase_core.subdocument import Spec
from .options import Seconds, FiniteDuration, forward_args
from couchbase_core.transcodable import Transcodable
from couchbase_core._libcouchbase import Result as SDK2Result
from couchbase_core.result import MultiResult, SubdocResult
from typing import *
from boltons.funcutils import wraps
from couchbase_core import abstractmethod
from couchbase_core.result import AsyncResult
try:
    from asyncio.futures import Future
except:
    Future=object


Proxy_T = TypeVar('Proxy_T')


def canonical_sdresult(content):
    sdresult = content  # type: SubdocResult
    result = {}
    cursor = iter(sdresult)
    for index in range(0, sdresult.result_count):
        spec = sdresult._specs[index]  # type: Spec
        result[spec[1]] = next(cursor)
    return result


def extract_value(content, decode_canonical):
    if isinstance(content, MultiResult):
        return {k: decode_canonical(content[k].value) for k, v, in content}
    elif isinstance(content, SubdocResult):
        return decode_canonical(canonical_sdresult(content))
    return decode_canonical(content.value)


def get_decoder(item  # type: Type[Union[Transcodable,Any]]
                ):
    return getattr(item, 'decode_canonical', None) if issubclass(item, Transcodable) else item


class ContentProxy(object):
    def __init__(self, content):
        self.content = content

    def __getitem__(self,
                    item  # type: Type[Proxy_T]
                    ):
        # type: (...)->Union[Proxy_T,Mapping[str,Proxy_T]]
        return extract_value(self.content, get_decoder(item))


class ContentProxySubdoc(object):
    def __init__(self, content):
        self.content=content

    def index_proxy(self, item, index):
        return get_decoder(item)(self.content[index])

    def __getitem__(self,
                    item  # type: Type[Proxy_T]
                    ):
        # type: (...)->Callable[[int],Union[Proxy_T,Mapping[str,Proxy_T]]]
        return lambda index: self.index_proxy(item, index)


class IResult(object):
    @property
    @abstractmethod
    def cas(self):
        # type: ()->int
        raise NotImplementedError()

    @property
    @abstractmethod
    def error(self):
        # type: ()->int
        raise NotImplementedError()

    @property
    @abstractmethod
    def success(self):
        # type: ()->bool
        raise NotImplementedError()


class Result(IResult):
    def __init__(self,
                 cas,  # type: int
                 error=None  # type: Optional[int]
                 ):
        self._cas = cas
        self._error = error

    @property
    def cas(self):
        # type: ()->int
        return self._cas

    @property
    def error(self):
        # type: ()->int
        return self._error

    def success(self):
        # type: ()->bool
        return not self._error


class IGetResult(IResult):
    @property
    @abstractmethod
    def id(self):
        # type: ()->str
        pass

    @property
    @abstractmethod
    def expiry(self):
        # type: ()->FiniteDuration
        pass

    @property
    @abstractmethod
    def content_as(self):
        # type: (...)->ContentProxy
        raise NotImplementedError()

    @property
    @abstractmethod
    def content(self):
        # type: () -> Any
        raise NotImplementedError()


class LookupInResult(Result):
    def __init__(self,
                 content,  # type: SDK2Result
                 *args,  # type: Any
                 **kwargs  # type: Any
                 ):
        # type: (...) ->None
        """
        LookupInResult is the return type for lookup_in operations.
        Constructed internally by the API.
        """
        super(LookupInResult, self).__init__(content.cas, content.rc)
        self._content = content  # type: SDK2Result
        self.dict = kwargs

    @property
    def content_as(self):
        # type: (...)->ContentProxySubdoc
        return ContentProxySubdoc(self._content)

    def exists(self,
               index  # type: int
               ):
        return len(canonical_sdresult(self._content))>index


class MutationResult(Result):
    def __init__(self,
                 cas,  # type: int
                 mutation_token=None  # type: MutationToken
                 ):
        super(MutationResult, self).__init__(cas)
        self.mutationToken = mutation_token

    def mutation_token(self):
        # type: () -> MutationToken
        return self.mutationToken


class MutateInResult(MutationResult):
    def __init__(self,
                 content,  # type: SDK2Result
                 **options  # type: Any
                 ):
        # type: (...) ->None
        """
        MutateInResult is the return type for mutate_in operations.
        Constructed internally by the API.
        """
        self._content = content  # type: SDK2Result
        self.dict = options

    def content_as(self):
        # type: (...)->ContentProxy
        return ContentProxy(self._content)


class GetResult(Result, IGetResult):
    def __init__(self,
                 id,  # type: str
                 cas,  # type: int
                 rc,  # type: int
                 expiry,  # type: Seconds
                 *args,  # type: Any
                 **kwargs  # type: Any
                 ):
        # type: (...) ->None
        """
        GetResult is the return type for full read operations.
        Constructed internally by the API.
        """
        super(GetResult, self).__init__(cas, rc)
        self._id = id
        self._expiry = expiry
        self.dict = kwargs

    def content_as_array(self):
        # type: (...) ->List
        return list(self.content)

    @property
    def id(self):
        # type: () -> str
        return self._id

    @property
    def expiry(self):
        # type: () -> Seconds
        return self._expiry


class ValueWrapper(object):
    def __init__(self,value):
        self.value=value


class SDK2ResultWrapped(GetResult, Future):
    def __init__(self,
                 sdk2_result,  # type: SDK2Result
                 expiry=None,  # type: Seconds
                 **kwargs):
        key, value=next(iter(sdk2_result.items()),(None,None)) if isinstance(sdk2_result,AsyncResult) else (sdk2_result.key, sdk2_result)
        super(SDK2ResultWrapped, self).__init__(key, value.cas, value.rc, expiry, **kwargs)
        try:
            Future.__init__(self)
            self.set_result(ValueWrapper(sdk2_result))
        except:
            pass
        self._original = sdk2_result

    @property
    def content_as(self):
        # type: (...)->ContentProxy
        return ContentProxy(self._original)

    @property
    def content(self):
        # type: () -> Any
        return extract_value(self._original, lambda x: x)


ResultPrecursor = NamedTuple('ResultPrecursor', [('orig_result', SDK2Result), ('orig_options', Mapping[str, Any])])


def get_result_wrapper(func  # type: Callable[[Any], ResultPrecursor]
                       ):
    # type: (...)->Callable[[Any], GetResult]
    @wraps(func)
    def wrapped(*args, **kwargs):
        x, options = func(*args, **kwargs)
        return SDK2ResultWrapped(x, **(options or {}))

    wrapped.__name__ = func.__name__
    wrapped.__doc__ = func.__name__
    return wrapped


class MutationToken(object):
    def __init__(self, sequenceNumber,  # type: int
                 vbucketId,  # type: int
                 vbucketUUID  # type: int
                 ):
        self.sequenceNumber = sequenceNumber
        self.vbucketId = vbucketId
        self.vbucketUUID = vbucketUUID

    def partition_id(self):
        # type: (...)->int
        pass

    def partition_uuid(self):
        # type: (...)->int
        pass

    def sequence_number(self):
        # type: (...)->int
        pass

    def bucket_name(self):
        # type: (...)->str
        pass


class SDK2MutationToken(MutationToken):
    def __init__(self, orig_result):
        token=getattr(orig_result, '_mutinfo',(None,None,None))
        super(SDK2MutationToken,self).__init__(token[2],token[0],token[1])

class AsyncMutationResult(MutationResult, Future):
    def __init__(self,
                 result  # type: ResultPrecursor
                 ):
        orig_result=next(iter(result.orig_result.values()))
        MutationResult.__init__(self, orig_result.cas, SDK2MutationToken(orig_result))
        Future.__init__(self)
        try:
            self.set_result(orig_result)
        except:
            pass

def get_mutation_result(result  # type: ResultPrecursor
                        ):
    # type (...)->MutationResult
    if isinstance(result.orig_result, AsyncResult):
        return AsyncMutationResult(result)
    else:
        orig_result=result.orig_result
        return MutationResult(orig_result.cas, SDK2MutationToken(orig_result))


def get_multi_mutation_result(target, wrapped, keys, *options, **kwargs):
    final_options = forward_args(kwargs, *options)
    raw_result = wrapped(target, keys, **final_options)
    return {k: get_mutation_result(ResultPrecursor(v, final_options)) for k, v in raw_result.items()}

def _wrap_in_mutation_result(func  # type: Callable[[Any,...],SDK2Result]
                             ):
    # type: (...)->Callable[[Any,...],MutationResult]
    @wraps(func)
    def mutated(*args, **kwargs):
        result = func(*args, **kwargs)
        return get_mutation_result(result)

    mutated.__name__=func.__name__
    mutated.__doc__=func.__doc__
    return mutated


class IViewResult(IResult):
    @property
    def error(self):
        raise NotImplementedError()

    @property
    def success(self):
        raise NotImplementedError()

    @property
    def cas(self):
        raise NotImplementedError()


class ViewResult(Result):
    def __init__(self, sdk2_result # type: SDK2Result
                ):
        super(ViewResult, self).__init__(sdk2_result)
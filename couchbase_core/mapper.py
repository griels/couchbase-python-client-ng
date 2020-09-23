from typing import *
import enum
import datetime
import warnings

from couchbase.exceptions import InvalidArgumentException

Src = TypeVar('Src')
Dest = TypeVar('Dest')


def identity(input: Src) -> Src:
    return input


Functor = TypeVar('Functor', bound=Callable[[Src],Dest])
SrcToDest = TypeVar('SrcToDest', bound=Callable[[Src], Dest])
DestToSrc = TypeVar('DestToSrc', bound=Callable[[Dest], Src])


class Bijection(Generic[Src, Dest, SrcToDest, DestToSrc]):
    def __init__(
            self,
            src_to_dest,  # type:  SrcToDest
            dest_to_src = None,  # type: DestToSrc
            parent = None  # type: Bijection[Dest,Src]
    ):
        # type: (...) -> None
        self._src_to_dest=src_to_dest
        if parent:
            self._inverse = parent
        else:
            self._inverse = Bijection(dest_to_src, parent=self)

    def __neg__(self):
        # type: (...) -> Bijection[Dest,Src]
        return self._inverse

    def __call__(self,
                 src  # type: Src
                 ):
        # type: (...) -> Dest
        try:
            return self._src_to_dest(src)
        except Exception as e:
            raise


class Identity(Bijection[Src,Src, identity, identity]):
    def __init__(self, type: Type[Src]):
        super(Identity, self).__init__(self, self)

    def __call__(self, x: Src) -> Src:
        return x


Enum_Type = TypeVar('Enum_Type', bound=enum.Enum)


class EnumToStr(Generic[Enum_Type]):
    def __init__(self, type: Type[Enum_Type], enforce=True):
        self._type=type
        self._enforce=enforce

    def __call__(self, src: Enum_Type) -> str:
        if not self._enforce and isinstance(src, str) and src in map(lambda x: x.value, self._type):
            warnings.warn("Using deprecated string parameter {}".format(src))
            return src
        if not isinstance(src, self._type):
            raise InvalidArgumentException("Argument must be of type {} but got {}".format(self._type, src))
        return src.value


class StrToEnum(Generic[Enum_Type]):
    def __init__(self, type: Enum_Type):
        self._type=type
    def __call__(self, dest: str
               ) -> Enum_Type:
        return self._type(dest)


class StringEnum(Bijection[Enum_Type, str, EnumToStr[Enum_Type], StrToEnum[Enum_Type]]):
    def __init__(self):
        super(StringEnum, self).__init__(EnumToStr[Enum_Type],StrToEnum[Enum_Type])


def str_enum(type: Type[Enum_Type]) -> Bijection[Enum_Type, str, EnumToStr[Enum_Type], StrToEnum[Enum_Type]]:
    return Bijection(EnumToStr(type), StrToEnum(type))


def str_enum_loose(type: Type[Enum_Type]) -> Bijection[Union[str,Enum_Type], str, EnumToStr[Enum_Type], StrToEnum[Enum_Type]]:
    return Bijection(EnumToStr(type, False), StrToEnum(type))


def seconds_to_timedelta(seconds: float) -> datetime.timedelta:
    return datetime.timedelta(seconds=seconds)


def timedelta_to_seconds(td: datetime.timedelta) -> float:
    return td.total_seconds()


class Timedelta(Bijection[datetime.timedelta, float, timedelta_to_seconds, seconds_to_timedelta]):
    def __init__(self):
        super(Timedelta, self).__init__(timedelta_to_seconds, seconds_to_timedelta)


class Division(Bijection[float, float, float.__mul__, float.__mul__]):
    def __init__(self, divisor):
        super(Division, self).__init__((1/divisor).__mul__, divisor.__mul__)


Orig_Mapping = TypeVar('OrigMapping', bound=Mapping[str, Any])


class BijectiveMapping(object):
    def __init__(self,
                 fwd_mapping: Orig_Mapping
                 ):
        self.mapping=dict()
        self.reverse_mapping=dict()
        for src_key, transform_dict in fwd_mapping.items():
            self.mapping[src_key]={}
            for dest_key, transform in transform_dict.items():
                self.mapping[src_key][dest_key] = transform
                self.reverse_mapping[dest_key] = {src_key: -transform}

    @staticmethod
    def convert(mapping, raw_info):
        converted = {}
        for k, v in raw_info.items():
            entry = mapping.get(k, {k:Identity(object)})
            for dest, transform in entry.items():
                try:
                    converted[dest] = transform(v)
                except InvalidArgumentException as e:
                    raise InvalidArgumentException("Problem processing argument {}: {}".format(k, e.message))
        return converted

    def sanitize_src(self, src_data):
        return src_data

    def to_dest(self, src_data):
        return self.convert(self.mapping, src_data)

    def to_src(self, dest_data):
        return self.convert(self.reverse_mapping, dest_data)

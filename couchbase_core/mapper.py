from typing import *
import enum
import datetime

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
        return self._src_to_dest(src)


class Identity(Bijection[Src,Src, identity, identity]):
    def __init__(self):
        super(Identity, self).__init__(self, self)

    def __call__(self, x: Src) -> Src:
        return x


Enum_Type = TypeVar('Enum_Type', bound=enum.Enum)


class EnumToStr(Generic[Enum_Type]):
    def __call__(self, src: Enum_Type) -> str:
        return src.value

class StrToEnum(Generic[Enum_Type]):
    def __call__(self, dest: str
               ) -> Enum_Type:
        return Enum_Type._type[dest]


class StringEnum(Bijection[Enum_Type, str, EnumToStr[Enum_Type], StrToEnum[Enum_Type]]):
    def __init__(self):
        super(StringEnum, self).__init__(EnumToStr[Enum_Type],StrToEnum[Enum_Type])


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
        import copy
        self.mapping=copy.deepcopy(fwd_mapping)
        self.reverse_mapping=dict()
        for src_key, transform_dict in fwd_mapping.items():
            for dest_key, transform in transform_dict.items():
                try:
                    cooked_transform=transform()
                    self.mapping[src_key][dest_key]=cooked_transform
                    self.reverse_mapping[dest_key] = {src_key: -cooked_transform}
                except Exception as e:
                    pass

    @staticmethod
    def convert(mapping, raw_info):
        converted = {}
        for k, v in raw_info.items():
            entry = mapping.get(k, {k:Identity})
            for dest, transform in entry.items():
                converted[dest] = transform(v)
        return converted

    def to_dest(self, src_data):
        return self.convert(self.mapping, src_data)

    def to_src(self, dest_data):
        return self.convert(self.reverse_mapping, dest_data)

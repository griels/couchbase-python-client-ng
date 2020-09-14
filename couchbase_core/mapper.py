from typing import *
import enum
import datetime

Src = TypeVar('Src')
Dest = TypeVar('Dest')


def identity(input):
    return input


class Functor(Protocol[Src,Dest]):
    def __call__(self,
                 src  # type: Src
                 ):
        # type: (...) -> Dest
        pass


class Bijection(Generic[Src, Dest]):
    def __init__(
            self,
            src_to_dest,  # type:  Functor[Src,Dest],
            dest_to_src = None,  # type: Functor[Dest,Src]
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


class Identity(Bijection):
    def __init__(self):
        super(Identity, self).__init__(identity, identity)


identity_bijection = Identity()


Enum_Type = TypeVar('Enum_Type', bound=Type[enum.Enum])


class StringEnum(Generic[Enum_Type], Bijection[Enum_Type, str]):
    def __init__(self,
                 type: Enum_Type):
        self._type=type
        super(StringEnum, self).__init__(self.to_dest, self.to_src)

    def to_dest(self, src):
        return src.value

    def to_src(self,
               dest  # type: str
               ):
        return self._type[dest]


def seconds_to_timedelta(seconds: float) -> datetime.timedelta:
    return datetime.timedelta(seconds=seconds)


def timedelta_to_seconds(td: datetime.timedelta) -> float:
    return td.total_seconds()


class Timedelta(Bijection):
    def __init__(self):
        super(Timedelta, self).__init__(timedelta_to_seconds, seconds_to_timedelta)


timedelta_bijection = Timedelta()


class Division(Bijection[float, float]):
    def __init__(self, divisor):
        super(Division, self).__init__(lambda x: x / divisor, lambda x: x * divisor)


Orig_Mapping = TypeVar('OrigMapping', bound=Mapping[str, Any])


class BijectiveMapping(object):
    def __init__(self,
                 fwd_mapping: Orig_Mapping
                 ):
        self.mapping=fwd_mapping
        self.reverse_mapping=dict()
        for src_key, transform_dict in fwd_mapping.items():
            for dest_key, transform in transform_dict.items():
                self.reverse_mapping[dest_key] = {src_key: -transform}

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

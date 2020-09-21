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


id_bijection = Identity()


class NamedBijection(Generic[Src, Dest]):
    def __init__(self,
                 reversible_functor,  # type: Bijection[Src,Dest]
                 dest_name,  # type: str
                 src_name=None,  # type: str
                 parent=None  # type: NamedBijection
                 ):
        # type: (...) -> None
        self._dest_name = dest_name
        self._functor = reversible_functor
        if parent:
            self._inverse = parent
        else:
            self._inverse = NamedBijection(-reversible_functor, dest_name, src_name, self)

    def dest_name(self):
        return self._dest_name

    def src_name(self):
        return self._inverse.dest_name()

    def __call__(self, X: Src) -> Dest:
        return self._functor(X)

    def __neg__(self):
        return self._inverse

    def inverse(self, new_dest_name):
        return NamedBijection(-self._functor, new_dest_name, self._dest_name)


class NamedIdentity(NamedBijection):
    def __init__(self, dest_name):
        super(NamedIdentity, self).__init__(id_bijection, dest_name)
    def __call__(self, X: Src) -> Src:
        return id_bijection(X)

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


class NamedStringEnum(Generic[Enum_Type], NamedBijection[Enum_Type, str]):
    def __init__(self,
                 type: Enum_Type,
                 src_name, dest_name=None):
        super(NamedStringEnum, self).__init__(StringEnum(type), src_name=src_name, dest_name=dest_name)


def named_string_enum_bijection(enum_type,  # type: Enum_Type
                                src_name, dest_name):
    return NamedStringEnum(enum_type, src_name=src_name, dest_name=dest_name)


def seconds_to_timedelta(seconds: float) -> datetime.timedelta:
    return datetime.timedelta(seconds=seconds)


def timedelta_to_seconds(td: datetime.timedelta) -> float:
    return td.total_seconds()


class Timedelta(Bijection):
    def __init__(self):
        super(Timedelta, self).__init__(timedelta_to_seconds, seconds_to_timedelta)


td_bijection = Timedelta()


class NamedTimedeltaBijection(NamedBijection[datetime.timedelta,int]):
    def __init__(self, src_name, dest_name=None):
        super(NamedTimedeltaBijection, self).__init__(td_bijection, dest_name, src_name=src_name)


class Division(Bijection[float, float]):
    def __init__(self, divisor):
        super(Division, self).__init__(lambda x: x / divisor, lambda x: x * divisor)


class NamedDivision(NamedBijection):
    def __init__(self, dest_name, divisor):
        super(NamedDivision, self).__init__(Division(divisor), dest_name)


Orig_Mapping = TypeVar('OrigMapping', bound=Mapping[str, Any])


class BijectiveMapping(object):
    def __init__(self,
                 fwd_mapping: Orig_Mapping
                 ):
        self.mapping=fwd_mapping
        self.reverse_mapping = {v.dest_name():v.inverse(k) for k,v in fwd_mapping.items()}

    @staticmethod
    def convert(mapping, raw_info):
        converted = {}
        for k, v in raw_info.items():
            entry = mapping.get(k, NamedIdentity(k))
            converted[entry.dest_name()] = entry(v)
        return converted

    def to_dest(self, src_data):
        return self.convert(self.mapping, src_data)

    def to_src(self, dest_data):
        return self.convert(self.reverse_mapping, dest_data)

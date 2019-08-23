from typing import *
import couchbase.options
from .options import Cardinal, OptionBlock
from couchbase_core.durability import Durability


class ReplicateTo(Cardinal):
    Value = couchbase.options.Value


class PersistTo(Cardinal):
    Value = couchbase.options.Value


T = TypeVar('T', bound=OptionBlock)


class ClientDurableOption(object):
    def dur_client(self,  # type: T
                   replicate_to,  # type: couchbase.options.Value
                   persist_to,  # type: couchbase.options.Value
                   ):
        # type: (...)->T.ClientDurable
        self['replicate_to'] = replicate_to
        self['persist_to'] = persist_to
        return self


class ServerDurableOption(object):
    def dur_server(self,  # type: T
                   level,  # type: Durability
                   ):
        # type: (...)->T.ServerDurable
        self['durability_level'] = level
        return self

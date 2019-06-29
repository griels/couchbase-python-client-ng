from enum import IntEnum

from couchbase_core import CompatibilityEnum
from .exceptions_base import InternalSDKError


class CouchbaseDurabilityError(InternalSDKError):
    pass


class DurabilityInvalidLevelException(CouchbaseDurabilityError):
    """Given durability level is invalid"""


class DurabilityImpossibleException(CouchbaseDurabilityError):
    """Given durability requirements are impossible to achieve"""


class DurabilitySyncWriteInProgressException(CouchbaseDurabilityError):
    """Returned if an attempt is made to mutate a key which already has a
    SyncWrite pending. Client would typically retry (possibly with backoff).
    Similar to ELOCKED"""


class DurabilitySyncWriteAmbiguousException(CouchbaseDurabilityError):
    """There is a synchronous mutation pending for given key
    The SyncWrite request has not completed in the specified time and has ambiguous
    result - it may Succeed or Fail; but the final value is not yet known"""


class DurabilityErrorCode(CompatibilityEnum):
    @classmethod
    def prefix(cls):
        return "LCB_DURABILITY_"
    INVALID_LEVEL = DurabilityInvalidLevelException
    IMPOSSIBLE = DurabilityImpossibleException
    SYNC_WRITE_IN_PROGRESS = DurabilitySyncWriteInProgressException
    SYNC_WRITE_AMBIGUOUS = DurabilitySyncWriteAmbiguousException


_LCB_SYNCREP_MAP = {item.value:item.orig_value for item in DurabilityErrorCode}

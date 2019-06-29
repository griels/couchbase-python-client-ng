from .exceptions_base import *
import couchbase_core._libcouchbase as C
#from collections import defaultdict
#from string import Template
#import json

_PYCBC_CRYPTO_ERR_MAP ={
    C.PYCBC_CRYPTO_PROVIDER_NOT_FOUND: CryptoProviderNotFoundException,
    C.PYCBC_CRYPTO_PROVIDER_ALIAS_NULL: CryptoProviderAliasNullException,
    C.PYCBC_CRYPTO_PROVIDER_MISSING_PUBLIC_KEY: CryptoProviderMissingPublicKeyException,
    C.PYCBC_CRYPTO_PROVIDER_MISSING_SIGNING_KEY: CryptoProviderMissingSigningKeyException,
    C.PYCBC_CRYPTO_PROVIDER_MISSING_PRIVATE_KEY: CryptoProviderMissingPrivateKeyException,
    C.PYCBC_CRYPTO_PROVIDER_SIGNING_FAILED: CryptoProviderSigningFailedException,
    C.PYCBC_CRYPTO_PROVIDER_ENCRYPT_FAILED: CryptoProviderEncryptFailedException,
    C.PYCBC_CRYPTO_PROVIDER_DECRYPT_FAILED: CryptoProviderDecryptFailedException,
    C.PYCBC_CRYPTO_CONFIG_ERROR: CryptoConfigError,
    C.PYCBC_CRYPTO_EXECUTION_ERROR: CryptoExecutionError,
    C.PYCBC_CRYPTO_ERROR: CryptoError,
    C.PYCBC_CRYPTO_PROVIDER_KEY_SIZE_EXCEPTION: CryptoProviderKeySizeException
}

LCB_ERRTYPE_DURABILITY = getattr(C,'LCB_ERRTYPE_DURABILITY', None)
_LCB_ERRCAT_MAP_NODURABILITY ={
    C.LCB_ERRTYPE_NETWORK: CouchbaseNetworkError,
    C.LCB_ERRTYPE_INPUT: CouchbaseInputError,
    C.LCB_ERRTYPE_TRANSIENT: CouchbaseTransientError,
    C.LCB_ERRTYPE_FATAL: CouchbaseFatalError,
    C.LCB_ERRTYPE_DATAOP: CouchbaseDataError,
    C.LCB_ERRTYPE_INTERNAL: CouchbaseInternalError,
}

_LCB_ERRCAT_DURABILITY_ENTRIES = {LCB_ERRTYPE_DURABILITY: CouchbaseDurabilityError}
_LCB_ERRCAT_MAP = dict(list(_LCB_ERRCAT_MAP_NODURABILITY.items()) +
                       (list(_LCB_ERRCAT_DURABILITY_ENTRIES.items()) if LCB_ERRTYPE_DURABILITY else []))



if LCB_ERRTYPE_DURABILITY:
    from  couchbase_core.durability_exceptions import _LCB_SYNCREP_MAP
else:
    _LCB_SYNCREP_MAP = {}

_LCB_ERRNO_MAP = dict(list({
                               C.LCB_AUTH_ERROR:       AuthError,
                               C.LCB_DELTA_BADVAL:     DeltaBadvalError,
                               C.LCB_E2BIG:            TooBigError,
                               C.LCB_EBUSY:            BusyError,
                               C.LCB_ENOMEM:           NoMemoryError,
                               C.LCB_ETMPFAIL:         TemporaryFailError,
                               C.LCB_KEY_EEXISTS:      KeyExistsError,
                               C.LCB_KEY_ENOENT:       NotFoundError,
                               C.LCB_DLOPEN_FAILED:    DlopenFailedError,
                               C.LCB_DLSYM_FAILED:     DlsymFailedError,
                               C.LCB_NETWORK_ERROR:    NetworkError,
                               C.LCB_NOT_MY_VBUCKET:   NotMyVbucketError,
                               C.LCB_NOT_STORED:       NotStoredError,
                               C.LCB_NOT_SUPPORTED:    NotSupportedError,
                               C.LCB_UNKNOWN_HOST:     UnknownHostError,
                               C.LCB_PROTOCOL_ERROR:   ProtocolError,
                               C.LCB_ETIMEDOUT:        TimeoutError,
                               C.LCB_CONNECT_ERROR:    ConnectError,
                               C.LCB_BUCKET_ENOENT:    BucketNotFoundError,
                               C.LCB_EBADHANDLE:       BadHandleError,
                               C.LCB_INVALID_HOST_FORMAT: InvalidError,
                               C.LCB_INVALID_CHAR:     InvalidError,
                               C.LCB_EINVAL:           InvalidError,
                               C.LCB_DURABILITY_ETOOMANY: ArgumentError,
                               C.LCB_DUPLICATE_COMMANDS: ArgumentError,
                               C.LCB_CLIENT_ETMPFAIL:  ClientTemporaryFailError,
                               C.LCB_HTTP_ERROR:       HTTPError,
                               C.LCB_SUBDOC_PATH_ENOENT: SubdocPathNotFoundError,
                               C.LCB_SUBDOC_PATH_EEXISTS: SubdocPathExistsError,
                               C.LCB_SUBDOC_PATH_EINVAL: SubdocPathInvalidError,
                               C.LCB_SUBDOC_DOC_E2DEEP: DocumentTooDeepError,
                               C.LCB_SUBDOC_DOC_NOTJSON: DocumentNotJsonError,
                               C.LCB_SUBDOC_VALUE_E2DEEP: SubdocValueTooDeepError,
                               C.LCB_SUBDOC_PATH_MISMATCH: SubdocPathMismatchError,
                               C.LCB_SUBDOC_VALUE_CANTINSERT: SubdocCantInsertValueError,
                               C.LCB_SUBDOC_BAD_DELTA: SubdocBadDeltaError,
                               C.LCB_SUBDOC_NUM_ERANGE: SubdocNumberTooBigError,
                               C.LCB_EMPTY_PATH: SubdocEmptyPathError,
                           }.items()) + list(_PYCBC_CRYPTO_ERR_MAP.items()) + list(_LCB_SYNCREP_MAP.items()))


def _set_default_codes():
    for k, v in _LCB_ERRNO_MAP.items():
        v.CODE = k

    ArgumentError.CODE = 0

_set_default_codes()


def _mk_lcberr(rc, name=None, default=CouchbaseError, docstr="", extrabase=[]):
    """
    Create a new error class derived from the appropriate exceptions.
    :param int rc: libcouchbase error code to map
    :param str name: The name of the new exception
    :param class default: Default exception to return if no categories are found
    :return: a new exception derived from the appropriate categories, or the
             value supplied for `default`
    """
    categories = C._get_errtype(rc)
    if not categories:
        return default

    bases = extrabase[::]

    for cat, base in _LCB_ERRCAT_MAP.items():
        if cat & categories:
            bases.append(base)

    if name is None:
        name = "LCB_0x{0:0X} (generated, catch: {1})".format(
            rc, ", ".join(x.__name__ for x in bases))

    d = { '__doc__' : docstr }

    if not bases:
        bases = [CouchbaseError]

    return type(name, tuple(bases), d)

def reparent():
    # Reinitialize the exception classes again.
    for rc, oldcls in _LCB_ERRNO_MAP.items():
        # Determine the new reparented error category for this
        newname = "_{0}_0x{1:0X} (generated, catch {0})".format(oldcls.__name__, rc)
        newcls = _mk_lcberr(rc, name=newname, default=None, docstr=oldcls.__doc__,
                            extrabase=[oldcls])
        if not newcls:
            # No categories for this type, fall back to existing one
            continue

        _LCB_ERRNO_MAP[rc] = newcls

        del newcls
        del oldcls

reparent()

_EXCTYPE_MAP = {
    C.PYCBC_EXC_ARGUMENTS:  ArgumentError,
    C.PYCBC_EXC_ENCODING:   ValueFormatError,
    C.PYCBC_EXC_INTERNAL:   InternalSDKError,
    C.PYCBC_EXC_HTTP:       HTTPError,
    C.PYCBC_EXC_THREADING:  ObjectThreadError,
    C.PYCBC_EXC_DESTROYED:  ObjectDestroyedError,
    C.PYCBC_EXC_PIPELINE:   PipelineError
}


def exc_from_rc(rc, msg=None, obj=None):
    """
    .. warning:: INTERNAL

    For those rare cases when an exception needs to be thrown from
    Python using a libcouchbase error code.

    :param rc: The error code
    :param msg: Message (description)
    :param obj: Context
    :return: a raisable exception
    """
    newcls = CouchbaseError.rc_to_exctype(rc)
    return newcls(params={'rc': rc, 'objextra': obj, 'message': msg})


class QueueEmpty(Exception):
    """
    Thrown if a datastructure queue is empty
    """

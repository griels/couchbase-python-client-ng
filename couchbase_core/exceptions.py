#
# Copyright 2019, Couchbase, Inc.
# All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import couchbase_core._libcouchbase as C
from collections import defaultdict
from string import Template
import json

from couchbase_core import CompatibilityEnum

from typing import *
import inspect
import re
from boltons.funcutils import wraps
try:
    from typing import TypedDict
except:
    from typing_extensions import TypedDict


class CouchbaseError(Exception):
    """Base exception for Couchbase errors

    This is the base class for all exceptions thrown by Couchbase

    **Exception Attributes**

      .. py:attribute:: rc

      The return code which caused the error

        A :class:`~couchbase_core.result.MultiResult` object, if this
        exception was thrown as part of a multi-operation. This contains
        all the operations (including ones which may not have failed)

      .. py:attribute:: inner_cause

        If this exception was triggered by another exception, it is
        present here.

      .. py:attribute:: key

        If applicable, this is the key which failed.

      .. py:attribute:: csrc_info

        A tuple of (`file`, `line`) pointing to a location in the C
        source code where the exception was thrown (if applicable)

      .. py:attribute:: categories

        An integer representing a set of bits representing various error
        categories for the specific error as returned by libcouchbase.

      .. py:attribute:: is_data

        True if this error is a negative reply from the server
        (see :exc:`CouchbaseDataError`)

      .. py:attribute:: is_transient

        True if this error was likely caused by a transient condition
        (see :exc:`CouchbaseTransientError`)

      .. py:attribute:: is_fatal

        True if this error indicates a likely fatal condition for the client.
        See :exc:`CouchbaseFatalError`

      .. py:attribute:: is_network

        True if errors were received during TCP transport.
        See :exc:`CouchbaseNetworkError`

      .. py:attribute:: CODE

        This is a _class_ level attribute which contains the equivalent
        libcouchbase error code which is mapped to this exception class.

        This is usually the :attr:`rc` value for an exception instance. Unlike
        :attr:`rc` however, it may be used without an instantiated object,
        possibly helping performance.

    """

    CODE = 0

    @classmethod
    def rc_to_exctype(cls, rc):
        """
        Map an error code to an exception

        :param int rc: The error code received for an operation

        :return: a subclass of :class:`CouchbaseError`
        """
        try:
            return _LCB_ERRNO_MAP[rc]
        except KeyError:
            newcls = _mk_lcberr(rc)
            _LCB_ERRNO_MAP[rc] = newcls
            return newcls

    @classmethod
    def _can_derive(cls, rc):
        """
        Determines if the given error code is logically derived from this class
        :param int rc: the error code to check
        :return: a boolean indicating if the code is derived from this exception
        """
        return issubclass(cls.rc_to_exctype(rc), cls)

    ParamType = TypedDict('ParamType',
                          {'rc': int,
                           'all_results': Mapping,
                           'result': Any,
                           'inner_cause': Exception,
                           'csrc_info': Any,
                           'key': str,
                           'objextra': Any,
                           'message': str,
                           'context': Any,
                           'ref': Any})

    def __init__(self,  # type: CouchbaseError
                 params=None  # type: Union[CouchbaseError.ParamType,str]
                 ):
        if isinstance(params, str):
            params = {'message': params}
        elif isinstance(params, CouchbaseError):
            self.__dict__.update(params.__dict__)
            return

        self.rc = params.get('rc', self.CODE)
        self.all_results = params.get('all_results', {})
        self.result = params.get('result', None)
        self.inner_cause = params.get('inner_cause', None)
        self.csrc_info = params.get('csrc_info', ())
        self.key = params.get('key', None)
        self.objextra = params.get('objextra', None)
        self.message = params.get('message', None)
        self.context = params.get('context',None)
        self.ref = params.get('ref',None)

    @classmethod
    def pyexc(cls, message=None, obj=None, inner=None):
        return cls({'message': message,
                    'objextra': obj,
                    'inner_cause': inner})

    @property
    def categories(self):
        """
        Gets the exception categories (as a set of bits)
        """
        return C._get_errtype(self.rc)

    @property
    def is_base(self):
      return self.categories & C.LCB_ERROR_TYPE_BASE

    @property
    def is_shared(self):
      return self.categories & C.LCB_ERROR_TYPE_SHARED

    @property
    def is_keyvalue(self):
      return self.categories & C.LCB_ERROR_TYPE_KEYVALUE

    @property
    def is_query(self):
      return self.categories & C.LCB_ERROR_TYPE_QUERY

    @property
    def is_analytics(self):
      return self.categories & C.LCB_ERROR_TYPE_ANALYTICS

    @property
    def is_search(self):
      return self.categories & C.LCB_ERROR_TYPE_SEARCH

    @property
    def is_view(self):
      return self.categories & C.LCB_ERROR_TYPE_VIEW

    @property
    def is_sdk(self):
      return self.categories & C.LCB_ERROR_TYPE_SDK


    def split_results(self):
        """
        Convenience method to separate failed and successful results.

        .. versionadded:: 2.0.0

        This function will split the results of the failed operation
        (see :attr:`.all_results`) into "good" and "bad" dictionaries.

        The intent is for the application to handle any successful
        results in a success code path, and handle any failed results
        in a "retry" code path. For example

        .. code-block:: python

            try:
                cb.add_multi(docs)
            except CouchbaseTransientError as e:
                # Temporary failure or server OOM
                _, fail = e.split_results()

                # Sleep for a bit to reduce the load on the server
                time.sleep(0.5)

                # Try to add only the failed results again
                cb.add_multi(fail)

        Of course, in the example above, the second retry may fail as
        well, and a more robust implementation is left as an exercise
        to the reader.

        :return: A tuple of ( `ok`, `bad` ) dictionaries.
        """

        ret_ok, ret_fail = {}, {}
        count = 0
        nokey_prefix = ([""] + sorted(filter(bool, self.all_results.keys())))[-1]
        for key, v in self.all_results.items():
            if not key:
                key = nokey_prefix + ":nokey:" + str(count)
                count += 1
            success = getattr(v,'success', True)
            if success:
                ret_ok[key] = v
            else:
                ret_fail[key] = v

        return ret_ok, ret_fail

    def __str__(self):
        details = []

        if self.key:
            details.append("Key={0}".format(repr(self.key)))

        if self.rc:
            details.append("RC=0x{0:X}[{1}]".format(
                self.rc, C._strerror(self.rc)))
        if self.message:
            details.append(self.message)
        if self.all_results:
            details.append("Results={0}".format(len(self.all_results)))

        if self.inner_cause:
            details.append("inner_cause={0}".format(self.inner_cause))

        if self.csrc_info:
            details.append("C Source=({0},{1})".format(*self.csrc_info))

        if self.objextra:
            details.append("OBJ={0}".format(repr(self.objextra)))

        if self.context:
            details.append("Context={0}".format(self.context))

        if self.ref:
            details.append("Ref={0}".format(self.ref))

        success, fail = self.split_results()
        if len(fail)>0:
            summary = {key: value.tracing_output for key, value in fail.items() if hasattr(value,"tracing_output")}
            details.append("Tracing Output={}".format(json.dumps(summary)))

        s = "<{0}>".format(", ".join(details))
        return s


"""
Service Exceptions
A Service level exception is any error or exception thrown or handled by one of the specific Couchbase Services: Query/N1QL, F.T.S., Analytics, View and Key/Value (Memcached). The exception or error names for each service are:

QueryException
SearchException
ViewException
KeyValueException
AnalyticsException
SDKException
BaseException

All Service exceptions derived from the base CouchbaseException and have an internal exception which can be either a system error/exception raised by the platform or a generic or shared error/exception across all services.

"""
class QueryException(CouchbaseError):
    """
    A server error occurred while executing a N1QL query. Assumes that that the service has returned a response.
    Message
    The error message returned by the Query service
    Properties
    The error(s) returned by response from the server by the Query/N1QL service
    Any additional information returned by the server, the node it executed on, payload, HTTP status
    """
    pass

class SearchException(CouchbaseError):
    pass

    """Message
    The error message returned by the Search service
    Properties
    The error(s) returned by response from the server by the F.T.S. Service
    Any additional information returned by the server, the node it executed on, payload, HTTP status
    """

"""Derived Exceptions
TBD? May be nothing to extend...
"""
class AnalyticsException(CouchbaseError):
    pass
    """A server error occurred while executing an Analytics query. Assumes that that the service has returned a response
    Message
    The error message returned by the Analytics service
    Properties
    The error(s) returned by response from the server, contextId, any additional information returned by the server, the node it executed on, payload, HTTP status.
    """
"""
Derived Exceptions
TBD? May be nothing to extend...
"""
class ViewException(CouchbaseError):
    """A server error occurred while executing a View query.  Assumes that that the service has returned a response.
    Message
    The error message returned by the View service
    Properties
    The error(s) returned by response from the server, contextId, any additional information returned by the server, the node it executed on, payload, HTTP status.
    """
    pass

class KeyValueException(CouchbaseError):
    """
    A server error occurred while executing a K/V operation. Assumes that the service has returned a response.
    Message
    The XError message returned by the memcached server
    Properties
    The memcached response status
    XError and Enhanced error message information
    The document id
    The opaque used in the request"""
    pass

class SDKException(CouchbaseError):
  """
  An error occured within the SDK, while executing a command.
  Message
  The error message returned from the SDK itself
  Properties
  """
  pass

class SharedException(CouchbaseError):
  """
  A server error occured, and it is of a sort that several services would all raise.
  Message
  The error message returned by the server
  Properties
  """

class BaseException(CouchbaseError):
  """
  An error occured which doesn't  fit into any of the other categories
  Message
  The error message describing the error
  Properties
  """

#BEGIN V2 exception types.  These need to go as we move to V3 types, eventually
class CouchbaseNetworkError(CouchbaseError):
    """
    Base class for network-related errors. These indicate issues in the low
    level connectivity
    """

class CouchbaseInputError(CouchbaseError):
    """
    Base class for errors possibly caused by malformed input
    """

class CouchbaseTransientError(CouchbaseError):
    """
    Base class for errors which are likely to go away with time
    """

class CouchbaseFatalError(CouchbaseError):
    """
    Base class for errors which are likely fatal and require reinitialization
    of the instance
    """

class CouchbaseDataError(CouchbaseError):
    """
    Base class for negative replies received from the server. These errors
    indicate that the server could not satisfy the request because of certain
    data constraints (such as an item not being present, or a CAS mismatch)
    """
# END V2 exception types -- needs to go eventually

class InternalSDKError(CouchbaseError):
    """
    This means the SDK has done something wrong. Get support.
    (this doesn't mean *you* didn't do anything wrong, it does mean you should
    not be seeing this message)
    """

class CouchbaseInternalError(InternalSDKError):
    pass

class CouchbaseDurabilityError(InternalSDKError):
    pass

class ArgumentError(CouchbaseError):
    """Invalid argument

    A given argument is invalid or must be set
    """


class ValueFormatError(CouchbaseError):
    """Failed to decode or encode value"""


# The following exceptions are derived from libcouchbase
class AuthError(CouchbaseError):
    """Authentication failed

    You provided an invalid username/password combination.
    """


class DeltaBadvalError(CouchbaseError):
    """The given value is not a number

    The server detected that operation cannot be executed with
    requested arguments. For example, when incrementing not a number.
    """


class TooBigError(CouchbaseError):
    """Object too big

    The server reported that this object is too big
    """


class BusyError(CouchbaseError):
    """The cluster is too busy

    The server is too busy to handle your request right now.
    please back off and try again at a later time.
    """


class InternalError(CouchbaseError):
    """Internal Error

    Internal error inside the library. You would have
    to destroy the instance and create a new one to recover.
    """


class InvalidError(CouchbaseError):
    """Invalid arguments specified"""


class NoMemoryError(CouchbaseError):
    """The server ran out of memory"""


class RangeError(CouchbaseError):
    """An invalid range specified"""


class LibcouchbaseError(CouchbaseError):
    """A generic error"""


class TemporaryFailError(CouchbaseError):
    """Temporary failure (on server)

    The server tried to perform the requested operation, but failed
    due to a temporary constraint. Retrying the operation may work.

    This error may also be delivered if the key being accessed was
    locked.

    .. seealso::

        :meth:`couchbase_core.client.Client.lock`
        :meth:`couchbase_core.client.Client.unlock`
    """


class KeyExistsError(CouchbaseError):
    """The key already exists (with another CAS value)

    This exception may be thrown during an ``add()`` operation
    (if the key already exists), or when a CAS is supplied
    and the server-side CAS differs.
    """


class NotFoundError(CouchbaseError):
    """The key does not exist"""


class DlopenFailedError(CouchbaseError):
    """Failed to open shared object"""


class DlsymFailedError(CouchbaseError):
    """Failed to locate the requested symbol in the shared object"""


class NetworkError(CouchbaseNetworkError):
    """Network error

    A network related problem occured (name lookup,
    read/write/connect etc)
    """


class NotMyVbucketError(CouchbaseError):
    """The vbucket is not located on this server

    The server who received the request is not responsible for the
    object anymore. (This happens during changes in the cluster
    topology)
    """


class NotStoredError(CouchbaseError):
    """The object was not stored on the server"""


class NotSupportedError(CouchbaseError):
    """Not supported

    The server doesn't support the requested command. This error
    differs from :exc:`couchbase_core.exceptions.UnknownCommandError` by
    that the server knows about the command, but for some reason
    decided to not support it.
    """


class UnknownCommandError(CouchbaseError):
    """The server doesn't know what that command is"""


class UnknownHostError(CouchbaseNetworkError):
    """The server failed to resolve the requested hostname"""


class ProtocolError(CouchbaseNetworkError):
    """Protocol error

    There is something wrong with the datastream received from
    the server
    """


class TimeoutError(CouchbaseError):
    """The operation timed out"""


class ConnectError(CouchbaseNetworkError):
    """Failed to connect to the requested server"""


class BucketNotFoundError(CouchbaseError):
    """The requested bucket does not exist"""


class QueryIndexNotFoundError(CouchbaseError):
    """The requested index does not exist"""


class QueryIndexAlreadyExistsError(CouchbaseError):
    """The requested index already exists"""


class ClientNoMemoryError(CouchbaseError):
    """The client ran out of memory"""


class ClientTemporaryFailError(CouchbaseError):
    """Temporary failure (on client)

    The client encountered a temporary error (retry might resolve
    the problem)
    """


class BadHandleError(CouchbaseError):
    """Invalid handle type

    The requested operation isn't allowed for given type.
    """


class HTTPError(CouchbaseError):
    """HTTP error"""


class ObjectThreadError(CouchbaseError):
    """Thrown when access from multiple threads is detected"""


class ViewEngineError(CouchbaseError):
    """Thrown for inline errors during view queries"""

class ObjectDestroyedError(CouchbaseError):
    """Object has been destroyed. Pending events are invalidated"""


class PipelineError(CouchbaseError):
    """Illegal operation within pipeline state"""


class SubdocPathNotFoundError(CouchbaseError):
    """Subdocument path does not exist"""


class SubdocPathExistsError(CouchbaseError):
    """Subdocument path already exists (and shouldn't)"""


class SubdocPathInvalidError(CouchbaseError):
    """Subdocument path is invalid"""


class DocumentNotJsonError(CouchbaseError):
    """Document is not JSON and cannot be used for subdoc operations"""

class SubdocPathMismatchError(CouchbaseError):
    """Subdocument path conflicts with actual document structure"""


class DocumentTooDeepError(CouchbaseError):
    """Document is too deep to be used for subdocument operations"""


class SubdocNumberTooBigError(CouchbaseError):
    """Existing number is too big to be used for subdocument operations"""


class SubdocValueTooDeepError(CouchbaseError):
    """Value is too deep to insert into document, or would cause the document
    to be too deep"""


class SubdocCantInsertValueError(CouchbaseError):
    """Cannot insert value for given operation"""


class SubdocBadDeltaError(CouchbaseError):
    """Bad delta supplied for counter command"""


class SubdocEmptyPathError(CouchbaseError):
    """Empty path passed as subdoc spec"""


class CryptoError(CouchbaseError):
    def __init__(self, params=None, message="Generic Cryptography Error for alias:$alias", **kwargs):
        params = params or {}
        param_dict = params.get('objextra') or defaultdict(lambda: "unknown")
        params['message'] = Template(message).safe_substitute(**param_dict)
        super(CryptoError, self).__init__(params=params)


class CryptoConfigError(CryptoError):
    """Generic Crypto Config Error"""

    def __init__(self, params=None, message="Generic Cryptography Configuration Error for alias:$alias", **kwargs):
        super(CryptoConfigError, self).__init__(params=params, message=message, **kwargs)


class CryptoExecutionError(CryptoError):
    """Generic Crypto Execution Error"""

    def __init__(self, params=None, message="Generic Cryptography Execution Error for alias:$alias", **kwargs):
        super(CryptoExecutionError, self).__init__(params=params, message=message, **kwargs)


class CryptoProviderNotFoundException(CryptoConfigError):
    """No crypto provider can be found for a given alias."""

    def __init__(self, params=None):
        super(CryptoProviderNotFoundException, self).__init__(params=params,
                                                              message="The cryptographic provider could not be found for the alias:$alias")


class CryptoProviderAliasNullException(CryptoConfigError):
    """The annotation has no associated alias or is null or and empty string."""

    def __init__(self, params=None):
        super(CryptoProviderAliasNullException, self).__init__(params=params,
                                                               message="Cryptographic providers require a non-null, empty alias be configured.")


class CryptoProviderMissingPublicKeyException(CryptoConfigError):
    """The PublicKeyName field has not been set in the crypto provider configuration or is null or and empty string"""
    def __init__(self, params = None):
        super(CryptoProviderMissingPublicKeyException,self).__init__(params=params, message="Cryptographic providers require a non-null, empty public and key identifier (kid) be configured for the alias:$alias")



class CryptoProviderMissingSigningKeyException(CryptoConfigError):
    """The SigningKeyName field has not been set in the crypto provider configuration or is null or and empty string. Required for symmetric algos."""
    def __init__(self, params = None):
        super(CryptoProviderMissingSigningKeyException,self).__init__(params=params, message="Symmetric key cryptographic providers require a non-null, empty signing key be configured for the alias:$alias")



class CryptoProviderMissingPrivateKeyException(CryptoConfigError):
    """The PrivateKeyName field has not been set in the crypto provider configuration or is null or and empty string. Required for asymmetric algos."""
    def __init__(self, params = None):
        super(CryptoProviderMissingPrivateKeyException,self).__init__(params=params, message="Asymmetric key cryptographic providers require a non-null, empty private key be configured for the alias:$alias")



class CryptoProviderSigningFailedException(CryptoExecutionError):
    """Thrown if the authentication check fails on the decryption side."""
    def __init__(self, params = None):
        super(CryptoProviderSigningFailedException,self).__init__(params=params, message="The authentication failed while checking the signature of the message payload for the alias:$alias")



class CryptoProviderEncryptFailedException(CryptoExecutionError):
    """Thrown if an error occurs during encryption."""
    def __init__(self, params = None):
        super(CryptoProviderEncryptFailedException,self).__init__(params=params, message="The encryption of the field failed for the alias:$alias")



class CryptoProviderDecryptFailedException(CryptoExecutionError):
    """Thrown if an error occurs during decryption."""
    def __init__(self, params = None):
        super(CryptoProviderDecryptFailedException,self).__init__(params=params, message="The decryption of the field failed for the alias:$alias")


class CryptoProviderKeySizeException(CryptoError):
    def __init__(self, params = None):
        super(CryptoProviderKeySizeException,self).__init__(params=params, message=
        "The key found does not match the size of the key that the algorithm expects for the alias: $alias. Expected key size was $expected_keysize and configured key size is $configured_keysize")


class NotImplementedInV3(CouchbaseError):
    """Not available on PYCBC>=3.0.0-alpha1"""
    pass


class DataverseAlreadyExistsException(AnalyticsException):
    """Raised when attempting to create dataverse when it already exists"""
    pass


class DataverseNotFoundException(AnalyticsException):
    """Raised when attempting to drop a dataverse which does not exist"""
    pass


class DatasetNotFoundException(AnalyticsException):
    """Raised when attempting to drop a dataset which does not exist."""
    pass


class DatasetAlreadyExistsException(AnalyticsException):
    """Raised when attempting to create a dataset which already exists"""

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

_LCB_ERRCAT_MAP = {
    C.LCB_ERROR_TYPE_BASE: BaseException,
    C.LCB_ERROR_TYPE_SHARED: SharedException,
    C.LCB_ERROR_TYPE_KEYVALUE: KeyValueException,
    C.LCB_ERROR_TYPE_QUERY: QueryException,
    C.LCB_ERROR_TYPE_ANALYTICS: AnalyticsException,
    C.LCB_ERROR_TYPE_SEARCH: SearchException,
    C.LCB_ERROR_TYPE_VIEW: ViewException,
    C.LCB_ERROR_TYPE_SDK: SDKException
}

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


_LCB_ERRNO_MAP = dict(list({
    C.LCB_ERR_AUTHENTICATION_FAILURE:       AuthError,
    C.LCB_ERR_INVALID_DELTA:     DeltaBadvalError,
    C.LCB_ERR_VALUE_TOO_LARGE:            TooBigError,
    C.LCB_ERR_NO_MEMORY:           NoMemoryError,
    C.LCB_ERR_TEMPORARY_FAILURE:         TemporaryFailError,
    C.LCB_ERR_DOCUMENT_EXISTS:      KeyExistsError,
    C.LCB_ERR_DOCUMENT_NOT_FOUND:       NotFoundError,
    C.LCB_ERR_DLOPEN_FAILED:    DlopenFailedError,
    C.LCB_ERR_DLSYM_FAILED:     DlsymFailedError,
    C.LCB_ERR_NETWORK:    NetworkError,
    C.LCB_ERR_NOT_MY_VBUCKET:   NotMyVbucketError,
    C.LCB_ERR_NOT_STORED:       NotStoredError,
    C.LCB_ERR_UNSUPPORTED_OPERATION:    NotSupportedError,
    C.LCB_ERR_UNKNOWN_HOST:     UnknownHostError,
    C.LCB_ERR_PROTOCOL_ERROR:   ProtocolError,
    C.LCB_ERR_TIMEOUT:        TimeoutError,
    C.LCB_ERR_CONNECT_ERROR:    ConnectError,
    C.LCB_ERR_BUCKET_NOT_FOUND:    BucketNotFoundError,
    C.LCB_ERR_QUERY: QueryException,
    C.LCB_ERR_INDEX_NOT_FOUND: QueryIndexNotFoundError,
    #C.LCB_EBADHANDLE:       BadHandleError,
    C.LCB_ERR_INVALID_HOST_FORMAT: InvalidError,
    C.LCB_ERR_INVALID_CHAR:     InvalidError,
    C.LCB_ERR_INVALID_ARGUMENT:           InvalidError,
    C.LCB_ERR_DURABILITY_TOO_MANY: ArgumentError,
    C.LCB_ERR_DUPLICATE_COMMANDS: ArgumentError,
    C.LCB_ERR_NO_CONFIGURATION:  ClientTemporaryFailError,
    C.LCB_ERR_HTTP:       HTTPError,
    C.LCB_ERR_SUBDOC_PATH_NOT_FOUND: SubdocPathNotFoundError,
    C.LCB_ERR_SUBDOC_PATH_EXISTS: SubdocPathExistsError,
    C.LCB_ERR_SUBDOC_PATH_INVALID: SubdocPathInvalidError,
    C.LCB_ERR_SUBDOC_PATH_TOO_DEEP: DocumentTooDeepError,
    C.LCB_ERR_SUBDOC_DOCUMENT_NOT_JSON: DocumentNotJsonError,
    C.LCB_ERR_SUBDOC_VALUE_TOO_DEEP: SubdocValueTooDeepError,
    C.LCB_ERR_SUBDOC_PATH_MISMATCH: SubdocPathMismatchError,
    C.LCB_ERR_SUBDOC_VALUE_INVALID: SubdocCantInsertValueError,
    C.LCB_ERR_SUBDOC_DELTA_INVALID: SubdocBadDeltaError,
    C.LCB_ERR_SUBDOC_NUMBER_TOO_BIG: SubdocNumberTooBigError,
    C.LCB_ERR_INDEX_EXISTS: QueryIndexAlreadyExistsError,
    C.LCB_ERR_DATAVERSE_EXISTS: DataverseAlreadyExistsException,
    C.LCB_ERR_DATAVERSE_NOT_FOUND: DataverseNotFoundException,
    C.LCB_ERR_DATASET_NOT_FOUND: DatasetNotFoundException,
    C.LCB_ERR_DATASET_EXISTS: DatasetAlreadyExistsException
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


CBErrorType = TypeVar('CBErrorType', bound=CouchbaseError)


class AnyPattern(object):
    def match(self, *args, **kwargs):
        return True

    def __hash__(self):
        return hash(True)

    def __eq__(self, other):
        return isinstance(other, AnyPattern)

class NotSupportedWrapper(object):
    @classmethod
    def a_404_means_not_supported(cls, func):
        def wrapped(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except HTTPError as e:
                extra = getattr(e, 'objextra', None)
                status = getattr(extra, 'http_status', None)
                if status == 404:
                    raise NotSupportedError('Server does not support this api call')
                raise
        return wrapped

    @classmethod
    def a_400_or_404_means_not_supported(cls, func):
        # some functions 404 if < 6.5, but 400 if 6.5 with
        # developer preview off.  <Sigh>
        def wrapped(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except HTTPError as e:
                extra = getattr(e, 'objextra', None)
                status = getattr(extra, 'http_status', None)
                if status == 404 or status == 400:
                    raise NotSupportedError('Server does not support this api call')
                raise

        return wrapped


class DictMatcher(object):
    def __init__(self, **kwargs):
        self._pattern=tuple(kwargs.items())

    def match(self, dict):
        for k, v in self._pattern:
            if not k in dict or not v.match(dict[k]):
                return False
        return True

    def __hash__(self):
        return hash(self._pattern)

    def __eq__(self, other):
        return isinstance(other, DictMatcher) and other._pattern == self._pattern


class ErrorMapper(object):
    @classmethod
    def mgmt_exc_wrap(cls, func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except CouchbaseError as e:
                for orig_exc, text_to_final_exc in cls._compiled_mapping().items():
                    if isinstance(e, orig_exc):
                        extra = getattr(e, 'objextra', None)
                        # TODO: this parsing is fragile, lets ponder a better approach, if any
                        if extra:
                            value = getattr(extra, 'value', "")
                            # this value could be a string or a json-encoded string...
                            if isinstance(value, dict):
                              # there should be a key with the error
                              # can be error or errors :(
                              if 'error' in value:
                                value = value.get('error', None)
                              elif 'errors' in value:
                                value = value.get('errors', None)
                              if value and isinstance(value, dict):
                                # sometimes it is still a dict, so use the name field
                                value = value.get('name', None)
                            if isinstance(value, bytearray) or isinstance(value, bytes):
                                value = value.decode("utf-8")
                            for pattern, exc in text_to_final_exc.items():
                                matches=False
                                try:
                                    matches=pattern.match(value)
                                except Exception as f:
                                    pass
                                if matches:
                                    raise exc.pyexc(e.message, extra, e)

                raise

        return wrapped

    @classmethod
    def _compiled_mapping(cls):
        if not getattr(cls, '_cm', None):
            cls._cm = {
                orig_exc: {{str: re.compile}.get(type(k), lambda x: x)(k): v for k, v in mapping.items()} for
                orig_exc, mapping in cls.mapping().items()
            }
        return cls._cm

    @staticmethod
    def mapping():
        # type (...)->Mapping[CBErrorType, Mapping[str, CBErrorType]]
        return None

    @classmethod
    def wrap(cls, dest):
        for name, method in inspect.getmembers(dest, inspect.isfunction):
            if not name.startswith('_'):
                setattr(dest, name, cls.mgmt_exc_wrap(method))
        return dest

from couchbase_core.supportability import uncommitted, volatile
from couchbase_core import abstractmethod, JSON

from boltons.funcutils import wraps
from mypy_extensions import VarArg, KwArg, Arg

from .subdocument import LookupInSpec, MutateInSpec, MutateInOptions, \
    gen_projection_spec
from .result import GetResult, GetReplicaResult, ExistsResult, get_result_wrapper, CoreResult, ResultPrecursor, LookupInResult, MutateInResult, \
    MutationResult, _wrap_in_mutation_result, AsyncGetResult, get_replica_result_wrapper, get_mutation_result, get_multi_mutation_result
from .options import forward_args, timedelta, OptionBlockTimeOut, OptionBlockDeriv, ConstrainedInt, SignedInt64, \
    AcceptableInts
from .options import OptionBlock, AcceptableInts, OptionBlockBase
from .durability import ReplicateTo, PersistTo, ClientDurability, ServerDurability, DurabilityType, \
    ServerDurableOptionBlock, DurabilityOptionBlock
from couchbase_core._libcouchbase import Bucket as _Base
import couchbase.exceptions
from couchbase_core.client import Client as CoreClient
import copy

from typing import *
from couchbase.durability import Durability, DurabilityType, ServerDurability, ClientDurability, ServerDurableOptionBlock, ClientDurableOptionBlock, DurabilityOptionBlock
from couchbase_core.asynchronous.bucket import AsyncClientFactory
from datetime import timedelta

try:
    from typing import TypedDict
except:
    from typing_extensions import TypedDict


class DeltaValue(ConstrainedInt):
    def __init__(self,
                 value  # type: AcceptableInts
                 ):
        # type: (...) -> None
        """
        A non-negative integer between 0 and +0x7FFFFFFFFFFFFFFF inclusive.
        Used as an argument for :meth:`Collection.increment` and :meth:`Collection.decrement`

        :param couchbase.options.AcceptableInts value: the value to initialise this with.

        :raise: :exc:`~couchbase.exceptions.ArgumentError` if not in range
        """
        super(DeltaValue,self).__init__(value)

    @classmethod
    def max(cls):
        return 0x7FFFFFFFFFFFFFFF

    @classmethod
    def min(cls):
        return 0


class ReplaceOptions(DurabilityOptionBlock):
    @overload
    def __init__(self,
                 timeout,       # type: timedelta
                 durability,    # type: DurabilityType
                 cas            # type: int
                 ):
        pass

    def __init__(self,
                 **kwargs
                ):
        if 'cas' not in kwargs:
            kwargs['cas'] = 0
        super(ReplaceOptions, self).__init__(**kwargs)


class AppendOptions(OptionBlockTimeOut):
    pass

class RemoveOptions(DurabilityOptionBlock):
    @overload
    def __init__(self,
                 durability,    # type: DurabilityType
                 cas,           # type: int
                 **kwargs):
        """
        Remove Options

        :param DurabilityType durability: durability type

        :param int cas: The CAS to use for the removal operation.
        If specified, the key will only be removed from the server
        if it has the same CAS as specified. This is useful to
        remove a key only if its value has not been changed from the
        version currently visible to the client. If the CAS on the
        server does not match the one specified, an exception is
        thrown.
        """
        pass
    def __init__(self,
                 **kwargs
                ):
        if 'cas' not in kwargs:
            kwargs['cas'] = 0
        super(RemoveOptions,self).__init__(**kwargs)


class PrependOptions(OptionBlockTimeOut):
    pass

class UnlockOptions(OptionBlockTimeOut):
    pass

class CounterOptions(ServerDurableOptionBlock):
    pass

class CollectionOptions(OptionBlock):
    pass

class ExistsOptions(OptionBlockTimeOut):
    pass

class GetOptions(OptionBlockTimeOut):
    @overload
    def __init__(self,
                 timeout=None,  # type: timedelta
                 with_expiry=None,  # type: bool
                 project=None  # type: Iterable[str]
                 ):
        pass

    def __init__(self,
                 **kwargs
                 ):
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        super(GetOptions, self).__init__(**kwargs)

    @property
    def with_expiry(self):
      # type: (...) -> bool
      return self.get('with_expiry', False)

    @property
    def project(self):
        # type: (...) -> Iterable[str]
        return self.get('project', [])

class GetAndTouchOptions(GetOptions):
    pass

class GetAndLockOptions(GetOptions):
    pass

class GetAnyReplicaOptions(GetOptions):
  pass

class GetAllReplicasOptions(GetOptions):
  pass

class InsertOptions(DurabilityOptionBlock):
    pass

class UpsertOptions(DurabilityOptionBlock):
    pass

T = TypeVar('T', bound='CBCollection')
R = TypeVar("R")

RawCollectionMethodDefault = Callable[
    [Arg('CBCollection', 'self'), Arg(str, 'key'), VarArg(OptionBlockDeriv), KwArg(Any)], R]
RawCollectionMethodInt = Callable[
    [Arg('CBCollection', 'self'), Arg(str, 'key'), int, VarArg(OptionBlockDeriv), KwArg(Any)], R]
RawCollectionMethod = Union[RawCollectionMethodDefault, RawCollectionMethodInt]
RawCollectionMethodSpecial = TypeVar('RawCollectionMethodSpecial', bound=RawCollectionMethod)


def _get_result_and_inject(func  # type: RawCollectionMethod
                           ):
    # type: (...) ->RawCollectionMethod
    result = _inject_scope_and_collection(get_result_wrapper(func))
    result.__doc__ = func.__doc__
    result.__name__ = func.__name__
    return result


def _mutate_result_and_inject(func  # type: RawCollectionMethod
                              ):
    # type: (...) ->RawCollectionMethod
    result = _inject_scope_and_collection(_wrap_in_mutation_result(func))
    result.__doc__ = func.__doc__
    result.__name__ = func.__name__
    return result


def _inject_scope_and_collection(func  # type: RawCollectionMethodSpecial
                                 ):
    # type: (...) -> RawCollectionMethod
    @wraps(func)
    def wrapped(self,  # type: CBCollection
                *args,  # type: Any
                **kwargs  # type:  Any
                ):
        # type: (...)->Any
        if self.true_collections:
            if self._self_name and not self._self_scope:
                raise couchbase.exceptions.CollectionMissingException
            if self._self_scope and self._self_name:
                kwargs['scope'] = self._self_scope.name
                kwargs['collection'] = self._self_name

        return func(self, *args, **kwargs)

    return wrapped


CoreBucketOpRead = TypeVar("CoreBucketOpRead", Callable[[Any], CoreResult], Callable[[Any], GetResult])


def _wrap_get_result(func  # type: CoreBucketOpRead
                     ):
    # type: (...) -> CoreBucketOpRead
    @wraps(func)
    def wrapped(self,  # type: CBCollection
                *args,  # type: Any
                **kwargs  # type:  Any
                ):
        # type: (...)->Any
        return _inject_scope_and_collection(get_result_wrapper(func))(self,*args,**kwargs)

    return wrapped

class BinaryCollection(object):
    pass

class TouchOptions(OptionBlockTimeOut):
    pass

class LookupInOptions(OptionBlockTimeOut):
    pass


CoreBucketOp = TypeVar("CoreBucketOp", Callable[[Any], CoreResult], Callable[[Any], MutationResult])


def _wrap_multi_mutation_result(wrapped  # type: CoreBucketOp
                               ):
    # type: (...) -> CoreBucketOp
    @wraps(wrapped)
    def wrapper(target, keys, *options, **kwargs
                ):
        return get_multi_mutation_result(target, wrapped, keys, *options, **kwargs)
    return _inject_scope_and_collection(wrapper)


class CBCollection(CoreClient):
    def __init__(self,
                 *args,
                 **kwargs
                 ):
        # type: (...) -> None
        """
        Couchbase collection. Should only be invoked by internal API, e.g.
        by :meth:`couchbase.collection.scope.Scope.collection` or
        :meth:`couchbase.bucket.Bucket.default_collection`.

        Args as for CoreClient, plus:

        :param couchbase.collections.Scope parent: parent scope
        :param str name: name of collection
        :param CollectionOptions options: miscellaneous options
        """
        name = kwargs.pop('name', None)
        parent = kwargs.pop('parent', None)
        args = list(args)
        connstr = kwargs.pop('connection_string', kwargs.pop('connstr', None))
        connstr = connstr or args.pop(0)
        final_args = [connstr] + args
        super(CBCollection, self).__init__(*final_args, **kwargs)
        self._init(name, parent)

    def _init(self,
              name,  # type: Optional[str]
              scope  # type: Scope
              ):
        self._self_scope = scope  # type: Scope
        self._self_name = name  # type: Optional[str]
        self._self_true_collections = name and scope

    @property
    def true_collections(self):
        return self._self_true_collections
    def _wrap_dsop(self, sdres, has_value=False, **kwargs):
        return getattr(super(CBCollection, self)._wrap_dsop(sdres, has_value), 'value')

    @classmethod
    def cast(cls,
             parent,  # type: Scope
             name,  # type Optional[str]
             *options  # type: CollectionOptions
             ):
        # type: (...) -> CBCollection
        coll_args = copy.deepcopy(parent.bucket._bucket_args)
        coll_args.update(name=name, parent=parent)
        result = parent.bucket._corebucket_class(parent.bucket._connstr, **parent.bucket._bucket_args)
        return result

    @property
    def bucket(self):
        # type: (...) -> CoreClient
        return super(CBCollection,self)

    MAX_GET_OPS = 16

    def _get_generic(self, key, kwargs, options):
        opts = forward_args(kwargs, *options)
        opts.pop('key', None)
        spec = opts.pop('spec', [])
        project = opts.pop('project', None)
        with_expiry = opts.pop('with_expiry', False)
        if project:
            if len(project) <= CBCollection.MAX_GET_OPS:
                spec = gen_projection_spec(project)
            else:
                raise couchbase.exceptions.ArgumentError(
                    "Project only accepts {} operations or less".format(CBCollection.MAX_GET_OPS))
        if not project and not opts.get('with_expiry', False):
            x = super(CBCollection,self).get(key, **opts)
        else:
            # if you want the expiry, or a projection, need to do a subdoc lookup
            # NOTE: this currently doesn't work for with_expiry.  We need to add that
            x = super(CBCollection,self).lookup_in(key, spec, **opts)

        # NOTE: there is no reason for the options in the ResultPrecursor below.  Once
        # we get expiry done correctly, lets eliminate that as well.  Previously the
        # expiry you passed in was just duplicated into the result, which of course made
        # no sense since expiry should have been with_expiry (a bool) in the options.
        return ResultPrecursor(x, options)

    @_get_result_and_inject
    def get(self,
            key,        # type: str
            *options,   # type: GetOptions
            **kwargs    # type: Any
            ):
        # type: (...) -> GetResult
        """Obtain an object stored in Couchbase by given key.

        :param string key: The key to fetch. The type of key is the same
            as mentioned in :meth:`upsert`
        :param: GetOptions options: The options to use for this get request.
        :param: Any kwargs: Override corresponding value in options.

        :raise: :exc:`.NotFoundError` if the key does not exist
        :return: A :class:`couchbase.result.GetResult` object

        Simple get::

            value = cb.get('key').content_as[str]

        Inspect CAS value::

            rv = cb.get("key")
            value, cas = rv.content_as[str], rv.cas

        Request the expiry::
            rv = cb.get("key", GetOptions(with_expiry=True))
            value, expiry = rv.content_as[str], rv.expiry
        """
        return self._get_generic(key, kwargs, options)

    @_get_result_and_inject
    def get_and_touch(self,
                      id,       # type: str
                      expiry,   # type: int
                      *options, # type: GetAndTouchOptions
                      **kwargs
                      ):
        # type: (...) -> GetResult
        kwargs_final = forward_args(kwargs, *options)
        if 'durability' in set(kwargs.keys()).union(options[0][0].keys()):
            raise couchbase.exceptions.ReplicaNotAvailableException()

        return self._get_generic(id, kwargs, options)

    @_get_result_and_inject
    def get_and_lock(self,
                     id,        # type: str
                     expiry,    # type: int
                     *options,  # type: GetAndLockOptions
                     **kwargs
                     ):
        # type: (...) -> GetResult
        final_options=forward_args(kwargs, *options)
        x = _Base.get(self, id, expiry, **final_options)
        _Base.lock(self, id, options)
        return ResultPrecursor(x, options)

    @_inject_scope_and_collection
    @get_replica_result_wrapper
    def get_any_replica(self,
                         id,        # type: str
                         *options,  # type: GetFromReplicaOptions
                         **kwargs   # type: Any
                         ):
        # type: (...) -> GetReplicaResult
        """Obtain an object stored in Couchbase by given key, from a replica.

        :param string key: The key to fetch. The type of key is the same
            as mentioned in :meth:`upsert`
        :param: GetFromReplicaOptions options: The options to use for this get request.
        :param: Any kwargs: Override corresponding value in options.

        :raise: :exc:`.NotFoundError` if the key does not exist
                :exc:`.DocumentUnretrievableError` if no replicas exist
        :return: A :class:`couchbase.result.GetReplicaResult` object

        """
        final_options = forward_args(kwargs, *options)
        return super(CBCollection, self).rget(id, **final_options)

    @_inject_scope_and_collection
    @get_replica_result_wrapper
    def get_all_replicas(self,
                         id,         # type: str
                         *options,   # type: GetAllReplicasOptions
                         **kwargs    # type: Any
                         ):
      # type: (...) -> Iterable[GetReplicaResult]
      """Obtain an object stored in Couchbase by given key, from every replica.

      :param string key: The key to fetch. The type of key is the same
          as mentioned in :meth:`upsert`
      :param: GetFromReplicaOptions options: The options to use for this get request.
      :param: Any kwargs: Override corresponding value in options.

      :raise: :exc:`.NotFoundError` if the key does not exist
              :exc:`.DocumentUnretrievableError` if no replicas exist
      :return: A list(:class:`couchbase.result.GetReplicaResult`) object
      """
      return super(CBCollection, self).rgetall(id, **forward_args(kwargs, *options))

    @_inject_scope_and_collection
    def get_multi(self,  # type: CBCollection
                  keys,  # type: Iterable[str]
                  *options,  # type: GetOptions
                  **kwargs
                  ):
        # type: (...) -> Dict[str,GetResult]
        """
        Get multiple keys from the collection

        :param keys: list of keys to get
        :type Iterable[str]
        :return: a dictionary of :class:`~.GetResult` objects by key
        :rtype: dict
        """
        raw_result = super(CBCollection,self).get_multi(keys, **forward_args(kwargs, *options))
        return {k: AsyncGetResult(v) for k, v in raw_result.items()}

    @overload
    def upsert_multi(self,  # type: CBCollection
                     keys,  # type: Mapping[str,Any]
                     ttl=0,  # type: int
                     format=None,  # type: int
                     durability=None  # type: DurabilityType
                     ):
        pass

    @_inject_scope_and_collection
    def upsert_multi(self,  # type: CBCollection
                     keys,  # type: Dict[str,JSON]
                     *options,  # type: GetOptions
                     **kwargs
                     ):
        # type: (...) -> Dict[str,MutationResult]
        """
        Write multiple items to the cluster. Multi version of :meth:`upsert`

        :param dict keys: A dictionary of keys to set. The keys are the
            keys as they should be on the server, and the values are the
            values for the keys to be stored.

            `keys` may also be a :class:`~.ItemCollection`. If using a
            dictionary variant for item collections, an additional
            `ignore_cas` parameter may be supplied with a boolean value.
            If not specified, the operation will fail if the CAS value
            on the server does not match the one specified in the
            `Item`'s `cas` field.
        :param int ttl: If specified, sets the expiry value
            for all keys
        :param int format: If specified, this is the conversion format
            which will be used for _all_ the keys.
        :param int persist_to: Durability constraint for persistence.
            Note that it is more efficient to use :meth:`endure_multi`
            on the returned :class:`~couchbase_v2.result.MultiResult` than
            using these parameters for a high volume of keys. Using
            these parameters however does save on latency as the
            constraint checking for each item is performed as soon as it
            is successfully stored.
        :param int replicate_to: Durability constraints for replication.
            See notes on the `persist_to` parameter for usage.
        :param Durability durability_level: Sync replication durability level.
            You should either use this or the old-style durability params above,
            but not both.

        :return: A :class:`~.MultiResult` object, which is a
            `dict`-like object

        The multi methods are more than just a convenience, they also
        save on network performance by batch-scheduling operations,
        reducing latencies. This is especially noticeable on smaller
        value sizes.

        .. seealso:: :meth:`upsert`
        """
        return get_multi_mutation_result(self, CoreClient.upsert_multi, keys, *options, **kwargs)

    @_inject_scope_and_collection
    def insert_multi(self,  # type: CBCollection
                     keys,  # type: Dict[str,JSON]
                     *options,  # type: GetOptions
                     **kwargs
                     ):
        # type: (...) -> Dict[str, MutationResult]
        """
        Insert multiple items into the collection.

        :param dict keys: dictionary of items to insert, by key
        :return: a dictionary of :class:`~.MutationResult` objects by key
        :rtype: dict

        .. seealso:: :meth:`upsert_multi` - for other optional arguments
        """
        return get_multi_mutation_result(self, CoreClient.insert_multi, keys, *options, **kwargs)

    @_inject_scope_and_collection
    def remove_multi(self,  # type: CBCollection
                     keys,  # type: Iterable[str]
                     *options,  # type: GetOptions
                     **kwargs
                     ):
        # type: (...) -> Dict[str, MutationResult]
        """
        Remove multiple items from the collection.

        :param list keys: list of items to remove, by key
        :return: a dictionary of :class:`~.MutationResult` objects by key
        :rtype: dict

        .. seealso:: :meth:`upsert_multi` - for other optional arguments
        """
        return get_multi_mutation_result(self, CoreClient.remove_multi, keys, *options, **kwargs)

    replace_multi = _wrap_multi_mutation_result(CoreClient.replace_multi)
    touch_multi = _wrap_multi_mutation_result(CoreClient.touch_multi)
    lock_multi = _wrap_multi_mutation_result(CoreClient.lock_multi)
    unlock_multi = _wrap_multi_mutation_result(CoreClient.unlock_multi)
    append_multi = _wrap_multi_mutation_result(CoreClient.unlock_multi)
    prepend_multi = _wrap_multi_mutation_result(CoreClient.prepend_multi)
    counter_multi = _wrap_multi_mutation_result(CoreClient.counter_multi)

    def touch(self,
              id,  # type: str
              *options,  # type: TouchOptions
              **kwargs):
        # type: (...) -> MutationResult
        """Update a key's expiry time

        :param string key: The key whose expiry time should be
            modified
        :param int timeout: The new expiry time. If the expiry time
            is `0` then the key never expires (and any existing
            expiry is removed)
        :param Durability durability_level: Sync replication durability level.

        :return: :class:`.MutationResult`

        Update the expiry time of a key ::

            cb.upsert("key", expiry=timedelta(seconds=100))
            # expires in 100 seconds
            cb.touch("key", expiry=timedelta(seconds=0))
            # key should never expire now

        :raise: The same things that :meth:`get` does

        .. seealso:: :meth:`get` - which can be used to get *and* update the
            expiry
        """
        return _Base.touch(self, id, **forward_args(kwargs, *options))

    @_wrap_in_mutation_result
    def unlock(self,
               id,  # type: str
               *options  # type: UnlockOptions
               ):
        # type: (...) -> MutationResult
        """Unlock a Locked Key in Couchbase.

        This unlocks an item previously locked by :meth:`lock`

        :param key: The key to unlock
        :param cas: The cas returned from :meth:`lock`'s
            :class:`.MutationResult` object.

        See :meth:`lock` for an example.

        :raise: :exc:`.TemporaryFailError` if the CAS supplied does not
            match the CAS on the server (possibly because it was
            unlocked by previous call).

        .. seealso:: :meth:`lock`
        """
        return _Base.unlock(self, id, **forward_args({}, *options))

    def lock(self,  # type: CBCollection
             key,  # type: str
             *options,  # type: LockOptions
             **kwargs  # type: Any
             ):
        """Lock and retrieve a key-value entry in Couchbase.

        :param key: A string which is the key to lock.

        :param ttl: a TTL for which the lock should be valid.
            While the lock is active, attempts to access the key (via
            other :meth:`lock`, :meth:`upsert` or other mutation calls)
            will fail with an :exc:`.KeyExistsError`. Note that the
            value for this option is limited by the maximum allowable
            lock time determined by the server (currently, this is 30
            seconds). If passed a higher value, the server will silently
            lower this to its maximum limit.


        This function otherwise functions similarly to :meth:`get`;
        specifically, it will return the value upon success. Note the
        :attr:`~.MutationResult.cas` value from the :class:`.MutationResult` object.
        This will be needed to :meth:`unlock` the key.

        Note the lock will also be implicitly released if modified by
        one of the :meth:`upsert` family of functions when the valid CAS
        is supplied

        :raise: :exc:`.TemporaryFailError` if the key is already locked.
        :raise: See :meth:`get` for possible exceptions

        Lock a key ::

            rv = cb.lock("locked_key", ttl=5)
            # This key is now locked for the next 5 seconds.
            # attempts to access this key will fail until the lock
            # is released.

            # do important stuff...

            cb.unlock("locked_key", rv.cas)

        Lock a key, implicitly unlocking with :meth:`upsert` with CAS ::

            rv = self.cb.lock("locked_key", ttl=5)
            new_value = rv.value.upper()
            cb.upsert("locked_key", new_value, rv.cas)


        Poll and Lock ::

            rv = None
            begin_time = time.time()
            while time.time() - begin_time < 15:
                try:
                    rv = cb.lock("key", ttl=10)
                    break
                except TemporaryFailError:
                    print("Key is currently locked.. waiting")
                    time.sleep(1)

            if not rv:
                raise Exception("Waited too long..")

            # Do stuff..

            cb.unlock("key", rv.cas)


        .. seealso:: :meth:`get`, :meth:`unlock`
        """
        final_options = forward_args(kwargs, *options)
        return _Base.lock(self, key, **final_options)

    def exists(self,      # type: CBCollection
               id,        # type: str
               *options,  # type: ExistsOptions
               **kwargs   # type: Any
                ):
        # type: (...) -> ExistsResult
        """Check to see if a key exists in this collection.

        :param str id: the id of the document.
        :param ExistsOptions *options: options for checking if a key exists.
        :return: An ExistsResult object with a boolean value indicating the presence of the document.
        :raise: Any exceptions raised by the underlying platform.
        """
        return ExistsResult(super(CBCollection,self).exists(id), **forward_args(kwargs, *options))


    @_mutate_result_and_inject
    def upsert(self,
               id,          # type: str
               value,       # type: Any
               *options,    # type: UpsertOptions
               **kwargs     # type: Any
               ):
        # type: (...) -> MutationResult
        """Unconditionally store the object in Couchbase.

        :param key:
            The key to set the value with. By default, the key must be
            either a :class:`bytes` or :class:`str` object encodable as
            UTF-8. If a custom `transcoder` class is used (see
            :meth:`~__init__`), then the key object is passed directly
            to the transcoder, which may serialize it how it wishes.
        :type key: string or bytes

        :param value: The value to set for the key.
            This should be a native Python value which will be transparently
            serialized to JSON by the library. Do not pass already-serialized
            JSON as the value or it will be serialized again.

            If you are using a different `format` setting (see `format`
            parameter), and/or a custom transcoder then value for this
            argument may need to conform to different criteria.

        :param int cas: The _CAS_ value to use. If supplied, the value
            will only be stored if it already exists with the supplied
            CAS

        :param expiry: If specified, the key will expire after this
            many seconds

        :param int format: If specified, indicates the `format` to use
            when encoding the value. If none is specified, it will use
            the `default_format` For more info see
            :attr:`~.default_format`

        :param int persist_to:
            Perform durability checking on this many nodes nodes for
            persistence to disk. See :meth:`endure` for more information

        :param int replicate_to: Perform durability checking on this
            many replicas for presence in memory. See :meth:`endure` for
            more information.

        :param Durability durability_level: Durability level

        :raise: :exc:`.ArgumentError` if an argument is supplied that is
            not applicable in this context. For example setting the CAS
            as a string.
        :raise: :exc`.CouchbaseNetworkError`
        :raise: :exc:`.KeyExistsError` if the key already exists on the
            server with a different CAS value.
        :raise: :exc:`.ValueFormatError` if the value cannot be
            serialized with chosen encoder, e.g. if you try to store a
            dictionary in plain mode.
        :return: :class:`~.Result`.

        Simple set::

            cb.upsert('key', 'value')

        Force JSON document format for value::

            cb.upsert('foo', {'bar': 'baz'}, format=couchbase_core.FMT_JSON)

        Insert JSON from a string::

            JSONstr = '{"key1": "value1", "key2": 123}'
            JSONobj = json.loads(JSONstr)
            cb.upsert("documentID", JSONobj, format=couchbase_core.FMT_JSON)

        Force UTF8 document format for value::

            cb.upsert('foo', "<xml></xml>", format=couchbase_core.FMT_UTF8)

        Perform optimistic locking by specifying last known CAS version::

            cb.upsert('foo', 'bar', cas=8835713818674332672)

        Simple set with durability::

            cb.upsert('key', 'value', durability_level=Durability.MAJORITY_AND_PERSIST_TO_ACTIVE)

        """

        final_options = forward_args(kwargs, *options)
        return ResultPrecursor(self.bucket.upsert(id, value, **final_options), final_options)

    def insert(self,
               id,  # type: str
               value,  # type: Any
               *options  # type: InsertOptions
               ):
        # type: (...) -> MutationResult
        pass

    @overload
    def insert(self,
               id,  # type: str
               value,  # type: Any
               expiry=None,  # type: timedelta
               format=None,  # type: str
               durability=None  # type: DurabilityType
               ):
        pass

    @_mutate_result_and_inject
    def insert(self, key, value, *options, **kwargs):
        # type: (...) -> ResultPrecursor
        """Store an object in Couchbase unless it already exists.

        Follows the same conventions as :meth:`upsert` but the value is
        stored only if it does not exist already. Conversely, the value
        is not stored if the key already exists.

        Notably missing from this method is the `cas` parameter, this is
        because `insert` will only succeed if a key does not already
        exist on the server (and thus can have no CAS)

        :raise: :exc:`.KeyExistsError` if the key already exists

        .. seealso:: :meth:`upsert`
        """

        final_options = forward_args(kwargs, *options)
        return ResultPrecursor(_Base.insert(self, key, value, **final_options), final_options)

    @overload
    def replace(self,
                id,  # type: str
                value,  # type: Any
                cas=0,  # type: int
                expiry=None,  # type: timedelta
                format=None,  # type: bool
                durability=None  # type: DurabilityType
                ):
        # type: (...) -> MutationResult
        pass

    @overload
    def replace(self,
                id,  # type: str
                value,  # type: Any
                options,  # type: ReplaceOptions
                **kwargs  # type: Any
                ):
        # type: (...) -> MutationResult
        pass

    @_mutate_result_and_inject
    def replace(self,
                id,  # type: str
                value,  # type: Any
                *options,
                **kwargs
                ):
        # type: (...) -> MutationResult
        """Store an object in Couchbase only if it already exists.

           Follows the same conventions as :meth:`upsert`, but the value is
           stored only if a previous value already exists.

           :raise: :exc:`.NotFoundError` if the key does not exist

           .. seealso:: :meth:`upsert`
        """

        final_options = forward_args(kwargs, *options)
        return ResultPrecursor(_Base.replace(self, id, value, **final_options), final_options)

    @_mutate_result_and_inject
    def remove(self,        # type: CBCollection
               id,          # type: str
               *options,    # type: RemoveOptions
               **kwargs
               ):
        # type: (...) -> MutationResult
        """Remove the key-value entry for a given key in Couchbase.

        :param str key: A string which is the key to remove. The format and
            type of the key follows the same conventions as in
            :meth:`upsert`
        :param RemoveOptions options: Options for removing key.
        :param Any kwargs: Override corresponding value in options
        :raise: :exc:`.NotFoundError` if the key does not exist.
        :raise: :exc:`.KeyExistsError` if a CAS was specified, but
            the CAS on the server had changed
        :return: A :class:`~.MutationResult` object.

        Simple remove::

            ok = cb.remove("key").success

        Don't complain if key does not exist::

            ok = cb.remove("key", quiet=True)

        Only remove if CAS matches our version::

            rv = cb.get("key")
            cb.remove("key", cas=rv.cas)
        """
        final_options = forward_args(kwargs, *options)
        return ResultPrecursor(self.bucket.remove(id, **final_options), final_options)

    @_inject_scope_and_collection
    def lookup_in(self,  # type: CBCollection
                  id,  # type: str
                  spec,  # type: LookupInSpec
                  *options,  # type: LookupInOptions
                  **kwargs  # type: Any
                  ):
        # type: (...) -> LookupInResult

        """Atomically retrieve one or more paths from a document.

        :param str id: The key of the document to lookup
        :param LookupInSpec spec: An iterable sequence of Specs (see :mod:`.couchbase_core.subdocument`)
        :param timedelta timeout: Timeout for operation

        :return: A :class:`.couchbase.LookupInResult` object.
            This object contains the results and any errors of the
            operation.

        Example::

            import couchbase_core.subdocument as SD
            rv = cb.lookup_in('user',
                              SD.get('email'),
                              SD.get('name'),
                              SD.exists('friends.therock'))

            email = rv[0]
            name = rv[1]
            friend_exists = rv.exists(2)

        """
        final_options = forward_args(kwargs, *options)
        return LookupInResult(self.bucket.lookup_in(id, spec, **final_options))

    @overload
    def mutate_in(self,
                  id,  # type: str
                  spec,  # type: MutateInSpec
                  *options  # type: MutateInOptions
                  ):
        # type: (...) -> MutateInResult
        pass

    @overload
    def mutate_in(self,
                  id,  # type: str
                  spec,  # type: MutateInSpec
                  create_doc=False,  # type: bool
                  insert_doc=False,  # type: bool
                  upsert_doc=False,  # type: bool
                  durability_level=Durability.NONE  # type: Durability
                  ):
        # type: (...) -> MutateInResult
        pass

    @_inject_scope_and_collection
    def mutate_in(self,  # type: CBCollection
                  id,  # type: str
                  spec,  # type: MutateInSpec
                  *options,  # type: MutateInOptions
                  **kwargs  # type: Any
                  ):
        # type: (...) -> MutateInResult
        """Perform multiple atomic modifications within a document.

        :param key: The key of the document to modify
        :param MutateInSpec spec: An iterable of specs (See :mod:`.couchbase.mutate_in.MutateInSpecItemBase`)
        :param bool create_doc:
            Whether the document should be create if it doesn't exist
        :param bool insert_doc: If the document should be created anew, and the
            operations performed *only* if it does not exist.
        :param bool upsert_doc: If the document should be created anew if it
            does not exist. If it does exist the commands are still executed.
        :param kwargs: CAS, etc.
        :return: A :class:`~.couchbase.MutationResult` object.

        Here's an example of adding a new tag to a "user" document
        and incrementing a modification counter::

            import couchbase_core.subdocument as SD
            # ....
            cb.mutate_in('user',
                          SD.array_addunique('tags', 'dog'),
                          SD.counter('updates', 1))

        .. note::

            The `insert_doc` and `upsert_doc` options are mutually exclusive.
            Use `insert_doc` when you wish to create a new document with
            extended attributes (xattrs).

        .. seealso:: :mod:`.couchbase_core.subdocument`
        """
        final_options = forward_args(kwargs, *options)
        return MutateInResult(self.bucket.mutate_in(id, spec, **final_options), **final_options)

    def binary(self):
        # type: (...) -> BinaryCollection
        pass

    @overload
    def append(self,
               id,  # type: str
               value,  # type: str
               *options  # type: AppendOptions
               ):
        # type: (...) -> MutationResult
        pass

    @overload
    def append(self,
               id,  # type: str
               value,  # type: str
               cas=0,  # type: int
               format=None,  # type: int
               durability=None  # type: DurabilityType
               ):
        pass

    @_mutate_result_and_inject
    def append(self,
               id,  # type: str
               value,  # type: str
               *options,  # type: Any
               **kwargs  # type: Any
               ):
        # type: (...) -> ResultPrecursor
        """Append a string to an existing value in Couchbase.

        :param string value: The data to append to the existing value.

        Other parameters follow the same conventions as :meth:`upsert`.

        The `format` argument must be one of
        :const:`~couchbase_core.FMT_UTF8` or :const:`~couchbase_core.FMT_BYTES`.
        If not specified, it will be :const:`~.FMT_UTF8` (overriding the
        :attr:`default_format` attribute). This is because JSON or
        Pickle formats will be nonsensical when random data is appended
        to them. If you wish to modify a JSON or Pickle encoded object,
        you will need to retrieve it (via :meth:`get`), modify it, and
        then store it again (using :meth:`upsert`).

        Additionally, you must ensure the value (and flags) for the
        current value is compatible with the data to be appended. For an
        example, you may append a :const:`~.FMT_BYTES` value to an
        existing :const:`~couchbase_core.FMT_JSON` value, but an error will
        be thrown when retrieving the value using :meth:`get` (you may
        still use the :attr:`data_passthrough` to overcome this).

        :raise: :exc:`.NotStoredError` if the key does not exist
        """
        x = _Base.append(self, id, value, forward_args(kwargs, *options))
        return ResultPrecursor(x, options)

    @overload
    def prepend(self,
                id,  # type: str
                value,  # type: Any
                cas=0,  # type: int
                format=None,  # type: int
                durability=None  # type: DurabilityType
                ):
        # type: (...) -> MutationResult
        pass

    @overload
    def prepend(self,
                id,  # type: str
                value,  # type: str
                *options  # type: PrependOptions
                ):
        # type: (...) -> MutationResult
        pass

    def prepend(self,
                id,  # type: str
                value,  # type: str
                *options,  # type: PrependOptions
                **kwargs  # type: Any
                ):
        # type: (...) -> ResultPrecursor
        """Prepend a string to an existing value in Couchbase.

        .. seealso:: :meth:`append`
        """
        x = _Base.prepend(self, id, value, **forward_args(kwargs, *options))
        return ResultPrecursor(x, options)

    @overload
    def increment(self,
                  id,  # type: str
                  delta,  # type: DeltaValue
                  initial=None,  # type: SignedInt64
                  expiry=None,  # type: timedelta
                  durability_level=Durability.NONE  # type: Durability
                  ):
        # type: (...) -> ResultPrecursor
        pass

    @overload
    def increment(self,
                  id,  # type: str
                  delta,  # type: DeltaValue
                  *options,  # type: CounterOptions
                  **kwargs
                  ):
        # type: (...) -> ResultPrecursor
        pass

    @_mutate_result_and_inject
    def increment(self,
                  id,  # type: str
                  delta,  # type: DeltaValue
                  *options,  # type: CounterOptions
                  **kwargs
                  ):
        # type: (...) -> ResultPrecursor
        """Increment the numeric value of an item.

        This method instructs the server to treat the item stored under
        the given key as a numeric counter.

        Counter operations require that the stored value
        exists as a string representation of a number (e.g. ``123``). If
        storing items using the :meth:`upsert` family of methods, and
        using the default :const:`couchbase_core.FMT_JSON` then the value
        will conform to this constraint.

        :param string key: A key whose counter value is to be modified
        :param DeltaValue delta: an amount by which the key should be incremented.
        :param couchbase.options.SignedInt64 initial: The initial value for the key, if it does not
           exist. If the key does not exist, this value is used, and
           `delta` is ignored. If this parameter is `None` then no
           initial value is used
        :param SignedInt64 initial: :class:`couchbase.options.SignedInt64` or `None`
        :param timedelta expiry: The lifetime for the key, after which it will
           expire
        :param Durability durability_level: Sync replication durability level.

        :raise: :exc:`.NotFoundError` if the key does not exist on the
           bucket (and `initial` was `None`)
        :raise: :exc:`.DeltaBadvalError` if the key exists, but the
           existing value is not numeric
        :return: A :class:`couchbase.result.MutationResult` object.

        Simple increment::

           rv = cb.increment("key")
           cb.get("key").content_as[int]
           # 42

        Increment by 10::

           rv = cb.increment("key", DeltaValue(10))


        Increment by 20, set initial value to 5 if it does not exist::

           rv = cb.increment("key", DeltaValue(20), initial=SignedInt64(5))

        """
        final_opts = self._check_delta_initial(kwargs, *options)
        x = _Base.counter(self, id, delta=int(DeltaValue.verified(delta)), **final_opts)
        return ResultPrecursor(x, final_opts)

    @overload
    def decrement(self,
                  id,  # type: str
                  delta,  # type: DeltaValue
                  initial=None,  # type: SignedInt64
                  expiry=None,  # type: timedelta
                  durability_level=Durability.NONE  # type: Durability
                  ):
        # type: (...) -> ResultPrecursor
        pass

    @overload
    def decrement(self,
                  id,  # type: str
                  delta,  # type: DeltaValue
                  *options,  # type: CounterOptions
                  **kwargs
                  ):
        # type: (...) -> ResultPrecursor
        pass

    @_mutate_result_and_inject
    def decrement(self,
                  id,  # type: str
                  delta,  # type: DeltaValue
                  *options,  # type: CounterOptions
                  **kwargs
                  ):
        # type: (...) -> ResultPrecursor
        """Decrement the numeric value of an item.

        This method instructs the server to treat the item stored under
        the given key as a numeric counter.

        Counter operations require that the stored value
        exists as a string representation of a number (e.g. ``123``). If
        storing items using the :meth:`upsert` family of methods, and
        using the default :const:`couchbase_core.FMT_JSON` then the value
        will conform to this constraint.

        :param string key: A key whose counter value is to be modified
        :param DeltaValue delta: an amount by which the key should be decremented.
        :param couchbase.options.SignedInt64 initial: The initial value for the key, if it does not
           exist. If the key does not exist, this value is used, and
           `delta` is ignored. If this parameter is `None` then no
           initial value is used
        :param SignedInt64 initial: :class:`couchbase.options.SignedInt64` or `None`
        :param timedelta expiry: The lifetime for the key, after which it will
           expire
        :param Durability durability_level: Sync replication durability level.

        :raise: :exc:`.NotFoundError` if the key does not exist on the
           bucket (and `initial` was `None`)
        :raise: :exc:`.DeltaBadvalError` if the key exists, but the
           existing value is not numeric
        :return: A :class:`couchbase.result.MutationResult` object.

        Simple decrement::

           rv = cb.decrement("key")
           cb.get("key").content_as[int]
           # 42

        Decrement by 10::

           rv = cb.decrement("key", DeltaValue(10))


        Decrement by 20, set initial value to 5 if it does not exist::

           rv = cb.decrement("key", DeltaValue(20), initial=SignedInt64(5))

        """

        final_opts = self._check_delta_initial(kwargs, *options)
        x = super(CBCollection,self).counter(id, delta=-int(DeltaValue.verified(delta)), **final_opts)
        return ResultPrecursor(x, final_opts)

    @staticmethod
    def _check_delta_initial(kwargs, *options):
        final_opts = forward_args(kwargs, *options)
        init_arg = final_opts.get('initial')
        initial = None if init_arg is None else int(SignedInt64.verified(init_arg))
        if initial is not None:
            final_opts['initial'] = initial
        return final_opts


class Scope(object):
    def __init__(self,  # type: Scope
                 parent,  # type: couchbase.bucket.Bucket
                 name=None  # type: str
                 ):
        # type: (...) -> Any
        """
        Collection scope representation.
        Constructor should only be invoked internally.

        :param parent: parent bucket.
        :param name: name of scope to open
        """
        self._name = name
        self.bucket = parent

    def __deepcopy__(self, memodict={}):
        result = copy.copy(self)
        return result

    @property
    def _realbucket(self):
        # type: (...) -> CoreClient
        return self.bucket._bucket

    @property
    def name(self):
        # type (...)->str
        """

        :return:    A string value that is the name of the collection.
        :except     ScopeNotFoundException
        :except     AuthorizationException
        """
        return self._name

    def default_collection(self,  # type: Scope
                           *options,  # type: Any
                           **kwargs  # type: Any
                           ):
        # type: (...) -> CBCollection
        """
        Returns the default collection for this bucket.

        :param collection_name: string identifier for a given collection.
        :param options: collection options
        :return: A :class:`.Collection` for a collection with the given name.

        :raise: CollectionNotFoundException
        :raise: AuthorizationException
        """
        return self._gen_collection(None, *options)

    def _gen_collection(self,
                        collection_name,  # type: Optional[str]
                        *options  # type: CollectionOptions
                        ):
        # type: (...) -> CBCollection
        return CBCollection.cast(self, collection_name, *options)
    @volatile
    def collection(self,
                        collection_name,  # type: str
                        *options  # type: CollectionOptions
                        ):
        # type: (...) -> CBCollection
        """
        Gets the named collection for this bucket.

        :param collection_name: string identifier for a given collection.
        :param options: collection options
        :return: A :class:`.Collection` for a collection with the given name.

        :raise: CollectionNotFoundException
        :raise: AuthorizationException

        """
        return self._gen_collection(collection_name, *options)


Collection = CBCollection

class AsyncCBCollection(AsyncClientFactory.gen_async_client(CBCollection)):
    def __init__(self, *args, **kwargs):
        super(AsyncCBCollection, self).__init__(*args, **kwargs)

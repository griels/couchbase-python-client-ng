import json

from couchbase_core._libcouchbase import Bucket as _Base

import couchbase_core.exceptions as E
from couchbase_core.analytics import AnalyticsQuery, DeferredAnalyticsQuery, DeferredAnalyticsRequest, AnalyticsRequest
from couchbase_core.exceptions import NotImplementedInV3
from couchbase_core.n1ql import N1QLQuery, N1QLRequest
from couchbase_core.views.iterator import View
from .views.params import make_options_string, make_dvpath
import couchbase_core._libcouchbase as _LCB
from couchbase_core._libcouchbase import FMT_JSON, FMT_BYTES

from couchbase_core import priv_constants as _P, fulltext as _SEARCH, _depr, subdocument as SD, exceptions
import couchbase_core.analytics
from typing import *
from .durability import Durability
from .result import Result
from boltons.funcutils import wraps

def _dsop(create_type=None, wrap_missing_path=True):
    import functools

    def real_decorator(fn):
        @functools.wraps(fn)
        def newfn(self, key, *args, **kwargs):
            try:
                return fn(self, key, *args, **kwargs)
            except E.NotFoundError:
                if kwargs.get('create'):
                    try:
                        self.insert(key, create_type())
                    except E.KeyExistsError:
                        pass
                    return fn(self, key, *args, **kwargs)
                else:
                    raise
            except E.SubdocPathNotFoundError:
                if wrap_missing_path:
                    raise IndexError(args[0])

        return newfn

    return real_decorator


ViewInstance = TypeVar('ViewInstance', bound=View)
ViewSubType = TypeVar('ViewSubType', bound=Type[ViewInstance])


class Client(_Base):
    _MEMCACHED_NOMULTI = ('stats', 'lookup_in', 'mutate_in')
    _MEMCACHED_OPERATIONS = ('upsert', 'get', 'insert', 'append', 'prepend',
                             'replace', 'remove', 'touch',
                             'unlock', 'stats',
                             'lookup_in', 'mutate_in')

    def __init__(self, *args, **kwargs):
        """Connect to a bucket.

        :param string connection_string:
            The connection string to use for connecting to the bucket.
            This is a URI-like string allowing specifying multiple hosts
            and a bucket name.

            The format of the connection string is the *scheme*
            (``couchbase`` for normal connections, ``couchbases`` for
            SSL enabled connections); a list of one or more *hostnames*
            delimited by commas; a *bucket* and a set of options.

            like so::

                couchbase://host1,host2,host3/bucketname?option1=value1&option2=value2

            If using the SSL scheme (``couchbases``), ensure to specify
            the ``certpath`` option to point to the location of the
            certificate on the client's filesystem; otherwise connection
            may fail with an error code indicating the server's
            certificate could not be trusted.

            See :ref:`connopts` for additional connection options.

        :param string username: username to connect to bucket with

        :param string password: the password of the bucket

        :param boolean quiet: the flag controlling whether to raise an
            exception when the client executes operations on
            non-existent keys. If it is `False` it will raise
            :exc:`.NotFoundError` exceptions. When
            set to `True` the operations will return `None` silently.

        :param boolean unlock_gil: If set (which is the default), the
            bucket object will release the python GIL when possible,
            allowing other (Python) threads to function in the
            background. This should be set to true if you are using
            threads in your application (and is the default), as
            otherwise all threads will be blocked while couchbase
            functions execute.

            You may turn this off for some performance boost and you are
            certain your application is not using threads

        :param transcoder:
            Set the transcoder object to use. This should conform to the
            interface in the documentation (it need not actually be a
            subclass). This can be either a class type to instantiate,
            or an initialized instance.
        :type transcoder: :class:`.Transcoder`

        :param lockmode: The *lockmode* for threaded access.
            See :ref:`multiple_threads` for more information.

        :param tracer: An OpenTracing tracer into which
            to propagate any tracing information. Requires
            tracing to be enabled.

        :raise: :exc:`.BucketNotFoundError` or :exc:`.AuthError` if
            there is no such bucket to connect to, or if invalid
            credentials were supplied.
        :raise: :exc:`.CouchbaseNetworkError` if the socket wasn't
            accessible (doesn't accept connections or doesn't respond
            in
        :raise: :exc:`.InvalidError` if the connection string
            was malformed.

        :return: instance of :class:`~couchbase_core.client.Client`


        Initialize bucket using default options::

            from couchbase_core.client import Client
            cb = Client('couchbase:///mybucket')

        Connect to protected bucket::

            cb = Client('couchbase:///protected', password='secret')

        Connect using a list of servers::

            cb = Client('couchbase://host1,host2,host3/mybucket')

        Connect using SSL::

            cb = Client('couchbases://securehost/bucketname?certpath=/var/cb-cert.pem')

        """
        _no_connect_exceptions = kwargs.pop('_no_connect_exceptions', False)
        _cntlopts = kwargs.pop('_cntl', {})

        # The following two blocks adapt some options from 1.x to proper
        # connection string (or lcb_cntl_string()) settings.
        strcntls = {}
        if 'timeout' in kwargs:
            _depr('timeout keyword argument',
                  'operation_timeout (with float value) in connection string')
            strcntls['operation_timeout'] = str(float(kwargs.pop('timeout')))

        if 'config_cache' in kwargs:
            _depr('config_cache keyword argument',
                  'config_cache in connection string')
            strcntls['config_cache'] = kwargs.pop('config_cache')

        tc = kwargs.get('transcoder')
        if isinstance(tc, type):
            kwargs['transcoder'] = tc()

        super(Client, self).__init__(*args, **kwargs)
        # Enable detailed error codes for network errors:
        self._cntlstr("detailed_errcodes", "1")

        # Enable self-identification in logs
        try:
            from couchbase_core._version import __version__ as cb_version
            self._cntlstr('client_string', 'PYCBC/' + cb_version)
        except E.NotSupportedError:
            pass

        for ctl, val in strcntls.items():
            self._cntlstr(ctl, val)

        for ctl, val in _cntlopts.items():
            self._cntl(ctl, val)

        try:
            self._do_ctor_connect()
        except E.CouchbaseError as e:
            if not _no_connect_exceptions:
                raise

    def _do_ctor_connect(self, *args, **kwargs):
        """This should be overidden by subclasses which want to use a
        different sort of connection behavior
        """
        self._connect()

    def __repr__(self):
        try:
            return ('<{modname}.{cls} bucket={bucket}, nodes={nodes} at 0x{oid:x}>'
                    ).format(modname=__name__, cls=self.__class__.__name__,
                             nodes=self.server_nodes, bucket=self.bucket,
                             oid=id(self))
        except Exception as e:
            return str(e)

    def _get_timeout_common(self, op):
        return self._cntl(op, value_type='timeout')

    def _set_timeout_common(self, op, value):
        value = float(value)
        if value <= 0:
            raise ValueError('Timeout must be greater than 0')

        self._cntl(op, value_type='timeout', value=value)

    def mkmeth(oldname, newname, _dst):
        def _tmpmeth(self, *args, **kwargs):
            _depr(oldname, newname)
            return _dst(self, *args, **kwargs)
        return _tmpmeth

    def _view(self, ddoc, view,
              use_devmode=False,
              params=None,
              unrecognized_ok=False,
              passthrough=False):
        """Internal method to Execute a view (MapReduce) query

        :param string ddoc: Name of the design document
        :param string view: Name of the view function to execute
        :param params: Extra options to pass to the view engine
        :type params: string or dict
        :return: a :class:`~couchbase_core.result.HttpResult` object.
        """

        if params:
            if not isinstance(params, str):
                params = make_options_string(
                    params,
                    unrecognized_ok=unrecognized_ok,
                    passthrough=passthrough)
        else:
            params = ""

        ddoc = self._mk_devmode(ddoc, use_devmode)
        url = make_dvpath(ddoc, view) + params

        ret = self._http_request(type=_LCB.LCB_HTTP_TYPE_VIEW,
                                 path=url,
                                 method=_LCB.LCB_HTTP_METHOD_GET,
                                 response_format=FMT_JSON)
        return ret

    def _cntl(self, *args, **kwargs):
        """Low-level interface to the underlying C library's settings. via
        ``lcb_cntl()``.

        This method accepts an opcode and an
        optional value. Constants are intentionally not defined for
        the various opcodes to allow saner error handling when an
        unknown opcode is not used.

        .. warning::

            If you pass the wrong parameters to this API call, your
            application may crash. For this reason, this is not a public
            API call. Nevertheless it may be used sparingly as a
            workaround for settings which may have not yet been exposed
            directly via a supported API

        :param int op: Type of cntl to access. These are defined in
          libcouchbase's ``cntl.h`` header file

        :param value: An optional value to supply for the operation.
            If a value is not passed then the operation will return the
            current value of the cntl without doing anything else.
            otherwise, it will interpret the cntl in a manner that makes
            sense. If the value is a float, it will be treated as a
            timeout value and will be multiplied by 1000000 to yield the
            microsecond equivalent for the library. If the value is a
            boolean, it is treated as a C ``int``

        :param value_type: String indicating the type of C-level value
            to be passed to ``lcb_cntl()``. The possible values are:

            * ``"string"`` - NUL-terminated `const char`.
                Pass a Python string
            * ``"int"`` - C ``int`` type. Pass a Python int
            * ``"uint32_t"`` - C ``lcb_uint32_t`` type.
                Pass a Python int
            * ``"unsigned"`` - C ``unsigned int`` type.
                Pass a Python int
            * ``"float"`` - C ``float`` type. Pass a Python float
            * ``"timeout"`` - The number of seconds as a float. This is
                converted into microseconds within the extension library.

        :return: If no `value` argument is provided, retrieves the
            current setting (per the ``value_type`` specification).
            Otherwise this function returns ``None``.
        """
        return _Base._cntl(self, *args, **kwargs)

    def _cntlstr(self, key, value):
        """
        Low-level interface to the underlying C library's settings.
        via ``lcb_cntl_string()``.

        This method accepts a key and a value. It can modify the same
        sort of settings as the :meth:`~._cntl` method, but may be a
        bit more convenient to follow in code.

        .. warning::

            See :meth:`~._cntl` for warnings.

        :param string key: The setting key
        :param string value: The setting value

        See the API documentation for libcouchbase for a list of
        acceptable setting keys.
        """
        return _Base._cntlstr(self, key, value)

    @staticmethod
    def lcb_version():
        return _LCB.lcb_version()

    def flush(self):
        """
        Clears the bucket's contents.

        .. note::

            This functionality requires that the flush option be
            enabled for the bucket by the cluster administrator. You
            can enable flush on the bucket using the administrative
            console (See http://docs.couchbase.com/admin/admin/UI/ui-data-buckets.html)

        .. note::

            This is a destructive operation, as it will clear all the
            data from the bucket.

        .. note::

            A successful execution of this method means that the bucket
            will have started the flush process. This does not
            necessarily mean that the bucket is actually empty.
        """
        path = '/pools/default/buckets/{0}/controller/doFlush'
        path = path.format(self.bucket)
        return self._http_request(type=_LCB.LCB_HTTP_TYPE_MANAGEMENT,
                                  path=path, method=_LCB.LCB_HTTP_METHOD_POST)

    def _wrap_dsop(self, sdres, has_value=False, **kwargs):
        from couchbase_core.items import Item
        it = Item(sdres.key)
        it.cas = sdres.cas
        if has_value:
            it.value = sdres[0]
        return it

    @property
    def closed(self):
        """Returns True if the object has been closed with :meth:`_close`"""
        return self._privflags & _LCB.PYCBC_CONN_F_CLOSED


    def mutate_in(self, key, specs, **kwargs):
        """Perform multiple atomic modifications within a document.

        :param key: The key of the document to modify
        :param specs: A list of specs (See :mod:`.couchbase_core.subdocument`)
        :param bool create_doc:
            Whether the document should be create if it doesn't exist
        :param bool insert_doc: If the document should be created anew, and the
            operations performed *only* if it does not exist.
        :param bool upsert_doc: If the document should be created anew if it
            does not exist. If it does exist the commands are still executed.
        :param kwargs: CAS, etc.
        :return: A :class:`~.couchbase_core.result.SubdocResult` object.

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

        # Note we don't verify the validity of the options. lcb does that for
        # us.
        sdflags = kwargs.pop('_sd_doc_flags', 0)

        if kwargs.pop('insert_doc', False):
            sdflags |= _P.CMDSUBDOC_F_INSERT_DOC
        if kwargs.pop('upsert_doc', False):
            sdflags |= _P.CMDSUBDOC_F_UPSERT_DOC

        # TODO: find a way of supporting this with LCB V4 API - PYCBC-584
        kwargs['_sd_doc_flags'] = sdflags
        return super(Client, self).mutate_in(key, tuple(specs), **kwargs)

    def lookup_in(self, key, specs, **kwargs):
        """Atomically retrieve one or more paths from a document.

        :param key: The key of the document to lookup
        :param spec: A list of specs (see :mod:`.couchbase_core.subdocument`)
        :return: A :class:`.couchbase_core.result.SubdocResult` object.
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

        .. seealso:: :meth:`retrieve_in` which acts as a convenience wrapper
        """
        return super(Client, self).lookup_in({key: tuple(specs)}, **kwargs)

    def get(self, *args, **kwargs):
        return super(Client, self).get(*args,**kwargs)

    def rget(self, key, replica_index=None, quiet=None, **kwargs):
        """Get an item from a replica node

        :param string key: The key to fetch
        :param int replica_index: The replica index to fetch.
            If this is ``None`` then this method will return once any
            replica responds. Use :attr:`configured_replica_count` to
            figure out the upper bound for this parameter.

            The value for this parameter must be a number between 0 and
            the value of :attr:`configured_replica_count`-1.
        :param boolean quiet: Whether to suppress errors when the key is
            not found

        This method (if `replica_index` is not supplied) functions like
        the :meth:`get` method that has been passed the `replica`
        parameter::

            c.get(key, replica=True)

        .. seealso:: :meth:`get` :meth:`rget_multi`
        """
        if replica_index is not None:
            return _Base._rgetix(self, key, replica=replica_index, **kwargs)
        else:
            return _Base._rget(self, key, **kwargs)

    def rgetall(self, key, **kwargs):
      return _Base._rgetall(self, key, **kwargs)

    def rget_multi(self, keys, replica_index=None, quiet=None):
        if replica_index is not None:
            return _Base._rgetix_multi(self, keys,
                                       replica=replica_index, quiet=quiet)
        else:
            return _Base._rget_multi(self, keys, quiet=quiet)

    def query(self, query, *args, **kwargs):
        """
        Execute a N1QL query.

        This method is mainly a wrapper around the :class:`~.N1QLQuery`
        and :class:`~.N1QLRequest` objects, which contain the inputs
        and outputs of the query.

        Using an explicit :class:`~.N1QLQuery`::

            query = N1QLQuery(
                'SELECT airportname FROM `travel-sample` WHERE city=$1', "Reno")
            # Use this option for often-repeated queries
            query.adhoc = False
            for row in cb.n1ql_query(query):
                print 'Name: {0}'.format(row['airportname'])

        Using an implicit :class:`~.N1QLQuery`::

            for row in cb.n1ql_query(
                'SELECT airportname, FROM `travel-sample` WHERE city="Reno"'):
                print 'Name: {0}'.format(row['airportname'])

        With the latter form, *args and **kwargs are forwarded to the
        N1QL Request constructor, optionally selected in kwargs['iterclass'],
        otherwise defaulting to :class:`~.N1QLRequest`.

        :param query: The query to execute. This may either be a
            :class:`.N1QLQuery` object, or a string (which will be
            implicitly converted to one).
        :param kwargs: Arguments for :class:`.N1QLRequest`.
        :return: An iterator which yields rows. Each row is a dictionary
            representing a single result
        """
        if not isinstance(query, N1QLQuery):
            query = N1QLQuery(query)


        return query.gen_iter(self, **kwargs)

    @staticmethod
    def _mk_devmode(n, use_devmode):
        if n.startswith('dev_') or not use_devmode:
            return n
        return 'dev_' + n

    def view_query(self,
                   design,  # type: str
                   view,  # type: str
                   use_devmode=False,  # type: bool
                   itercls = View,  # type: ViewSubType
                   **kwargs  # type: Any
                   ):
        # type: (...)->ViewInstance
        """
        Query a pre-defined MapReduce view, passing parameters.

        This method executes a view on the cluster. It accepts various
        parameters for the view and returns an iterable object
        (specifically, a :class:`~.View`).

        :param string design: The design document
        :param string view: The view function contained within the design
            document
        :param boolean use_devmode: Whether the view name should be
            transformed into a development-mode view. See documentation
            on :meth:`~.BucketManager.design_create` for more
            explanation.
        :param kwargs: Extra arguments passed to the :class:`~.View`
            object constructor.
        :param kwargs: Additional parameters passed to the
            :class:`~.View` constructor. See that class'
            documentation for accepted parameters.

        .. seealso::

            :class:`~.View`
                contains more extensive documentation and examples

            :class:`couchbase_core.views.params.Query`
                contains documentation on the available query options

            :class:`~.SpatialQuery`
                contains documentation on the available query options
                for Geospatial views.

        .. note::

            To query a spatial view, you must explicitly use the
            :class:`.SpatialQuery`. Passing key-value view parameters
            in ``kwargs`` is not supported for spatial views.

        """
        design = self._mk_devmode(design, use_devmode)
        return itercls(self, design, view, **kwargs)

    def ping(self, *options, **kwargs):
        """Ping cluster for latency/status information per-service

        Pings each node in the cluster, and
        returns a `dict` with 'type' keys (e.g 'n1ql', 'kv')
        and node service summary lists as a value.


        :raise: :exc:`.CouchbaseNetworkError`
        :return: `dict` where keys are stat keys and values are
            host-value pairs

        Ping cluster (works on couchbase buckets)::

            cb.ping()
            # {'services': {...}, ...}
        """
        resultdict = self._ping(*options, **kwargs )
        return json.loads(resultdict['services_json'])

    def diagnostics(self, *options, **kwargs):
        """Request diagnostics report about network connections

        Generates diagnostics for each node in the cluster.
        It returns a `dict` with details


        :raise: :exc:`.CouchbaseNetworkError`
        :return: `dict` where keys are stat keys and values are
            host-value pairs

        Get health info (works on couchbase buckets)::

            cb.diagnostics()
            # {
                  'config':
                  {
                     'id': node ID,
                     'last_activity_us': time since last activity in nanoseconds
                     'local': local server and port,
                     'remote': remote server and port,
                     'status': connection status
                  }
                  'id': client ID,
                  'sdk': sdk version,
                  'version': diagnostics API version
              }
        """
        return json.loads(self._diagnostics(*options, **kwargs)['health_json'])
    @staticmethod
    def gen_request(query, *args, **kwargs):
        if isinstance(query, couchbase_core.analytics.DeferredAnalyticsQuery):
            return couchbase_core.DeferredAnalyticsRequest(query, *args, **kwargs)
        elif isinstance(query,AnalyticsQuery):
            return couchbase_core.AnalyticsRequest(query, *args, **kwargs)


    def analytics_query(self, query, *args, **kwargs):
        """
        Execute an Analytics query.

        This method is mainly a wrapper around the :class:`~.AnalyticsQuery`
        and :class:`~.AnalyticsRequest` objects, which contain the inputs
        and outputs of the query.

        Using an explicit :class:`~.AnalyticsQuery`::

            query = AnalyticsQuery(
                "SELECT VALUE bw FROM breweries bw WHERE bw.name = ?", "Kona Brewing")
            for row in cb.analytics_query(query, "127.0.0.1"):
                print('Entry: {0}'.format(row))

        Using an implicit :class:`~.AnalyticsQuery`::

            for row in cb.analytics_query(
                "SELECT VALUE bw FROM breweries bw WHERE bw.name = ?", "127.0.0.1", "Kona Brewing"):
                print('Entry: {0}'.format(row))

        :param query: The query to execute. This may either be a
            :class:`.AnalyticsQuery` object, or a string (which will be
            implicitly converted to one).
        :param host: The host to send the request to.
        :param args: Positional arguments for :class:`.AnalyticsQuery`.
        :param kwargs: Named arguments for :class:`.AnalyticsQuery`.
        :return: An iterator which yields rows. Each row is a dictionary
            representing a single result
        """
        if not isinstance(query, AnalyticsQuery):
            query = AnalyticsQuery(query, *args, **kwargs)
        else:
            query.update(*args, **kwargs)

        return query.itercls()(query, None, self, **kwargs)

    def search(self, index, query, **kwargs):
        """
        Perform full-text searches

        .. versionadded:: 2.0.9

        .. warning::

            The full-text search API is experimental and subject to change

        :param str index: Name of the index to query
        :param couchbase_core.fulltext.SearchQuery query: Query to issue
        :param couchbase_core.fulltext.Params params: Additional query options
        :return: An iterator over query hits

        .. note:: You can avoid instantiating an explicit `Params` object
            and instead pass the parameters directly to the `search` method.

        .. code-block:: python

            it = cb.search('name', ft.MatchQuery('nosql'), limit=10)
            for hit in it:
                print(hit)

        """
        itercls = kwargs.pop('itercls', _SEARCH.SearchRequest)
        iterargs = itercls.mk_kwargs(kwargs)
        params = kwargs.pop('params', _SEARCH.Params(**kwargs))
        body = _SEARCH.make_search_body(index, query, params)
        return itercls(body, self, **iterargs)

    @overload
    def upsert_multi(self,  # type: Client
                     keys,  # type: Mapping[str,Any]
                     ttl=0,  # type: int
                     format=None,  # type: int
                     persist_to=0,  # type: int
                     replicate_to=0,  # type: int
                     durability_level=None  # type: Durability
                     ):
        pass

    def upsert_multi(self,  # type: Client
                     keys,  # type: Mapping[str,Any]
                     ttl=0,  # type: int
                     format=None,  # type: int
                     **kwargs
                     ):
        # type: (...) -> Result
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
            on the returned :class:`~couchbase_core.result.MultiResult` than
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
        return _Base.upsert_multi(self, keys, ttl=ttl, format=format,
                                  **kwargs)

    def insert_multi(self,  # type: Client
                     keys,  # type: Mapping[str,Any]
                     ttl=0,  # type: int
                     format=None,  # type: int
                     persist_to=0,  # type: int
                     replicate_to=0,  # type: int
                     durability_level=Durability.NONE  # type: Durability
                     ):
        # type: (...) -> Result
        """Add multiple keys. Multi variant of :meth:`insert`

        .. seealso:: :meth:`insert`, :meth:`upsert_multi`, :meth:`upsert`
        """
        return _Base.insert_multi(self, keys, ttl=ttl, format=format,
                                  persist_to=persist_to,
                                  replicate_to=replicate_to,
                                  durability_level=durability_level.value)

    def replace_multi(self,  # type: Client
                      keys,  # type: Mapping[str,Any]
                      ttl=0,  # type: int
                      format=None,  # type: int
                      persist_to=0,  # type: int
                      replicate_to=0,  # type: int
                      durability_level=Durability.NONE  # type: Durability
                      ):
        # type: (...) -> Result
        """
        Replace multiple keys. Multi variant of :meth:`replace`

        :param dict keys: replacement entries
        :param int ttl: If specified, sets the expiry value
            for all keys
        :param int format: If specified, this is the conversion format
            which will be used for _all_ the keys.
        :param int persist_to: Durability constraint for persistence.
            Note that it is more efficient to use :meth:`endure_multi`
            on the returned :class:`~couchbase_core.result.MultiResult` than
            using these parameters for a high volume of keys. Using
            these parameters however does save on latency as the
            constraint checking for each item is performed as soon as it
            is successfully stored.
        :param int replicate_to: Durability constraints for replication.
            See notes on the `persist_to` parameter for usage.
        :param Durability durability_level: Sync replication durability level.
            You should either use this or the old-style durability params above,
            but not both.
        :return:

        .. seealso:: :meth:`replace`, :meth:`upsert_multi`, :meth:`upsert`
        """
        return _Base.replace_multi(self, keys, ttl=ttl, format=format,
                                   persist_to=persist_to,
                                   replicate_to=replicate_to,
                                   durability_level=durability_level.value)

    def append_multi(self,  # type: Client
                     keys,  # type: Mapping[str,Any]
                     ttl=0,  # type: int
                     format=None,  # type: int
                     persist_to=0,  # type: int
                     replicate_to=0  # type: int
                     ):
        # type: (...) -> Result
        """Append to multiple keys. Multi variant of :meth:`append`.

        .. warning::

            If using the `Item` interface, use the :meth:`append_items`
            and :meth:`prepend_items` instead, as those will
            automatically update the :attr:`.Item.value`
            property upon successful completion.

        .. seealso:: :meth:`append`, :meth:`upsert_multi`, :meth:`upsert`
        """
        return _Base.append_multi(self, keys, format=format,
                                  persist_to=persist_to,
                                  replicate_to=replicate_to)

    def prepend_multi(self,  # type: Client
                      keys,  # type: Mapping[str,Any]
                      ttl=0,  # type: int
                      format=None,  # type: int
                      persist_to=0,  # type: int
                      replicate_to=0  # type: int
                      ):
        # type: (...) -> Result
        """Prepend to multiple keys. Multi variant of :meth:`prepend`

        .. seealso:: :meth:`prepend`, :meth:`upsert_multi`, :meth:`upsert`
        """
        return _Base.prepend_multi(self, keys, format=format,
                                   persist_to=persist_to,
                                   replicate_to=replicate_to)

    def get_multi(self, # type: Client
                  keys,  # type: Iterable[str]
                  ttl=0,  # type: int
                  quiet=None,  # type: bool
                  replica=False,  # type: bool
                  no_format=False  # type: bool
                  ):
        # type: (...) -> Result
        """Get multiple keys. Multi variant of :meth:`get`

        :param keys: keys the keys to fetch
        :type keys: :ref:`iterable<argtypes>`
        :param int ttl: Set the expiry for all keys when retrieving
        :param boolean replica:
            Whether the results should be obtained from a replica
            instead of the master. See :meth:`get` for more information
            about this parameter.
        :param Durability durability_level: Sync replication durability level.

        :return: A :class:`~.MultiResult` object. This is a dict-like
            object  and contains the keys (passed as) `keys` as the
            dictionary keys, and :class:`~.Result` objects as values
        """
        return _Base.get_multi(self, keys, ttl=ttl, quiet=quiet,
                               replica=replica, no_format=no_format)

    def touch_multi(self,  # type: Client
                    keys,  # type: Iterable[str]
                    ttl=0,  # type: int
                    durability_level=Durability.NONE  # type: Durability
                    ):
        # type: (...) -> Result
        """Touch multiple keys. Multi variant of :meth:`touch`

        :param keys: the keys to touch
        :type keys: :ref:`iterable<argtypes>`.
            ``keys`` can also be a dictionary with values being
            integers, in which case the value for each key will be used
            as the TTL instead of the global one (i.e. the one passed to
            this function)
        :param int ttl: The new expiry time
        :param Durability durability_level: Sync replication durability level.

        :return: A :class:`~.MultiResult` object

        Update three keys to expire in 10 seconds ::

            cb.touch_multi(("key1", "key2", "key3"), ttl=10)

        Update three keys with different expiry times ::

            cb.touch_multi({"foo" : 1, "bar" : 5, "baz" : 10})

        .. seealso:: :meth:`touch`
        """
        return _Base.touch_multi(self, keys, ttl=ttl, durability_level=durability_level.value)

    def lock_multi(self,  # type: Client
                   keys,  # type: Iterable[str]
                   ttl=0  # type: int
                   ):
        # type: (...) -> Result
        """Lock multiple keys. Multi variant of :meth:`lock`

        :param keys: the keys to lock
        :type keys: :ref:`iterable<argtypes>`
        :param int ttl: The lock timeout for all keys

        :return: a :class:`~.MultiResult` object

        .. seealso:: :meth:`lock`
        """
        return _Base.lock_multi(self, keys, ttl=ttl)

    def unlock_multi(self,  # type: Client
                     keys  # type: Iterable[str]
                     ):
        # type: (...) -> Result

        """Unlock multiple keys. Multi variant of :meth:`unlock`

        :param dict keys: the keys to unlock
        :return: a :class:`~couchbase_core.result.MultiResult` object

        The value of the ``keys`` argument should be either the CAS, or
        a previously returned :class:`Result` object from a :meth:`lock`
        call. Effectively, this means you may pass a
        :class:`~.MultiResult` as the ``keys`` argument.

        Thus, you can do something like ::

            keys = (....)
            rvs = cb.lock_multi(keys, ttl=5)
            # do something with rvs
            cb.unlock_multi(rvs)

        .. seealso:: :meth:`unlock`
        """
        return _Base.unlock_multi(self, keys)

    def observe_multi(self, keys, master_only=False):
        """Multi-variant of :meth:`observe`"""
        return _Base.observe_multi(self, keys, master_only=master_only)

    def endure_multi(self, keys, persist_to=-1, replicate_to=-1,
                     timeout=5.0, interval=0.010, check_removed=False):
        """Check durability requirements for multiple keys

        :param keys: The keys to check

        The type of keys may be one of the following:
            * Sequence of keys
            * A :class:`~couchbase_core.result.MultiResult` object
            * A ``dict`` with CAS values as the dictionary value
            * A sequence of :class:`~couchbase_core.result.Result` objects

        :return: A :class:`~.MultiResult` object
            of :class:`~.OperationResult` items.

        .. seealso:: :meth:`endure`
        """
        if not _LCB.PYCBC_ENDURE:
            raise NotImplementedInV3("Standalone endure")
        return _Base.endure_multi(self, keys, persist_to=persist_to,
                                  replicate_to=replicate_to,
                                  timeout=timeout, interval=interval,
                                  check_removed=check_removed)

    def remove_multi(self,
                     kvs,
                     quiet=None,
                     durability_level=Durability.NONE):
        """Remove multiple items from the cluster

        :param kvs: Iterable of keys to delete from the cluster. If you wish
            to specify a CAS for each item, then you may pass a dictionary
            of keys mapping to cas, like `remove_multi({k1:cas1, k2:cas2}`)
        :param quiet: Whether an exception should be raised if one or more
            items were not found
        :return: A :class:`~.MultiResult` containing :class:`~.OperationResult`
            values.
        :param Durability durability_level: Sync replication durability level.
        """
        return _Base.remove_multi(self, kvs, quiet=quiet, durability_level=durability_level.value)

    def counter_multi(self,
                      kvs,
                      initial=None,
                      delta=1,
                      ttl=0,
                      durability_level=Durability.NONE):
        """Perform counter operations on multiple items

        :param kvs: Keys to operate on. See below for more options
        :param initial: Initial value to use for all keys.
        :param delta: Delta value for all keys.
        :param ttl: Expiration value to use for all keys
        :param Durability durability_level: Sync replication durability level.

        :return: A :class:`~.MultiResult` containing :class:`~.ValueResult`
            values


        The `kvs` can be a:

        - Iterable of keys
            .. code-block:: python

                cb.counter_multi((k1, k2))

        - A dictionary mapping a key to its delta
            .. code-block:: python

                cb.counter_multi({
                    k1: 42,
                    k2: 99
                })

        - A dictionary mapping a key to its additional options
            .. code-block:: python

                cb.counter_multi({
                    k1: {'delta': 42, 'initial': 9, 'ttl': 300},
                    k2: {'delta': 99, 'initial': 4, 'ttl': 700}
                })


        When using a dictionary, you can override settings for each key on
        a per-key basis (for example, the initial value). Global settings
        (global here means something passed as a parameter to the method)
        will take effect for those values which do not have a given option
        specified.
        """
        return _Base.counter_multi(self, kvs, initial=initial, delta=delta,
                                   ttl=ttl, durability_level=durability_level.value)

    @classmethod
    def _gen_memd_wrappers(cls, factory):
        return Client._gen_memd_wrappers_retarget(cls, factory)
    @staticmethod
    def _gen_memd_wrappers_retarget(cls, factory):
        """Generates wrappers for all the memcached operations.
        :param factory: A function to be called to return the wrapped
            method. It will be called with two arguments; the first is
            the unbound method being wrapped, and the second is the name
            of such a method.

          The factory shall return a new unbound method

        :return: A dictionary of names mapping the API calls to the
            wrapped functions
        """
        d = {}
        for n in cls._MEMCACHED_OPERATIONS:
            for variant in (n, n + "_multi"):
                try:
                    d[variant] = factory(getattr(cls, variant), variant)
                except AttributeError:
                    if n in cls._MEMCACHED_NOMULTI:
                        continue
                    raise
        return d

    @_dsop(create_type=dict)
    def map_add(self, key, mapkey, value, create=False, **kwargs):
        """
        Set a value for a key in a map.

        .. warning::

            The functionality of the various `map_*`, `list_*`, `queue_*`
            and `set_*` functions are considered experimental and are included
            in the library to demonstrate new functionality.
            They may change in the future or be removed entirely!

            These functions are all wrappers around the :meth:`mutate_in` or
            :meth:`lookup_in` methods.

        :param key: The document ID of the map
        :param mapkey: The key in the map to set
        :param value: The value to use (anything serializable to JSON)
        :param create: Whether the map should be created if it does not exist
        :param kwargs: Additional arguments passed to :meth:`mutate_in`
        :return: A :class:`~.OperationResult`
        :raise: :cb_exc:`NotFoundError` if the document does not exist.
            and `create` was not specified

        .. Initialize a map and add a value

            cb.upsert('a_map', {})
            cb.map_add('a_map', 'some_key', 'some_value')
            cb.map_get('a_map', 'some_key').value  # => 'some_value'
            cb.get('a_map').value  # => {'some_key': 'some_value'}

        """
        op = SD.upsert(mapkey, value)
        sdres = Client.mutate_in(self, key, (op,), **kwargs)
        return self._wrap_dsop(sdres, **kwargs)

    @_dsop()
    def map_get(self, key, mapkey):
        """
        Retrieve a value from a map.

        :param str key: The document ID
        :param str mapkey: Key within the map to retrieve
        :return: :class:`~.ValueResult`
        :raise: :exc:`IndexError` if the mapkey does not exist
        :raise: :cb_exc:`NotFoundError` if the document does not exist.

        .. seealso:: :meth:`map_add` for an example
        """
        op = SD.get(mapkey)
        sdres = Client.lookup_in(self, key, (op,))
        return self._wrap_dsop(sdres, True)

    @_dsop()
    def map_remove(self, key, mapkey, **kwargs):
        """
        Remove an item from a map.

        :param str key: The document ID
        :param str mapkey: The key in the map
        :param kwargs: See :meth:`mutate_in` for options
        :raise: :exc:`IndexError` if the mapkey does not exist
        :raise: :cb_exc:`NotFoundError` if the document does not exist.

        .. Remove a map key-value pair:

            cb.map_remove('a_map', 'some_key')

        .. seealso:: :meth:`map_add`
        """
        op = SD.remove(mapkey)
        sdres = Client.mutate_in(self, key, (op,), **kwargs)
        return self._wrap_dsop(sdres, **kwargs)

    @_dsop()
    def map_size(self, key):
        """
        Get the number of items in the map.

        :param str key: The document ID of the map
        :return int: The number of items in the map
        :raise: :cb_exc:`NotFoundError` if the document does not exist.

        .. seealso:: :meth:`map_add`
        """

        return Client.lookup_in(self, key, (SD.get_count(''),))[0]

    @_dsop(create_type=list)
    def list_append(self, key, value, create=False, **kwargs):
        """
        Add an item to the end of a list.

        :param str key: The document ID of the list
        :param value: The value to append
        :param create: Whether the list should be created if it does not
               exist. Note that this option only works on servers >= 4.6
        :param kwargs: Additional arguments to :meth:`mutate_in`
        :return: :class:`~.OperationResult`.
        :raise: :cb_exc:`NotFoundError` if the document does not exist.
            and `create` was not specified.

        example::

            cb.list_append('a_list', 'hello')
            cb.list_append('a_list', 'world')

        .. seealso:: :meth:`map_add`
        """
        op = SD.array_append('', value)
        sdres = Client.mutate_in(self, key, (op,), **kwargs)
        return self._wrap_dsop(sdres, **kwargs)

    @_dsop(create_type=list)
    def list_prepend(self, key, value, create=False, **kwargs):
        """
        Add an item to the beginning of a list.

        :param str key: Document ID
        :param value: Value to prepend
        :param bool create:
            Whether the list should be created if it does not exist
        :param kwargs: Additional arguments to :meth:`mutate_in`.
        :return: :class:`OperationResult`.
        :raise: :cb_exc:`NotFoundError` if the document does not exist.
            and `create` was not specified.

        This function is identical to :meth:`list_append`, except for prepending
        rather than appending the item

        .. seealso:: :meth:`list_append`, :meth:`map_add`
        """
        op = SD.array_prepend('', value)
        sdres = Client.mutate_in(self, key, (op,), **kwargs)
        return self._wrap_dsop(sdres, **kwargs)

    @_dsop()
    def list_set(self, key, index, value, **kwargs):
        """
        Sets an item within a list at a given position.

        :param key: The key of the document
        :param index: The position to replace
        :param value: The value to be inserted
        :param kwargs: Additional arguments to :meth:`mutate_in`
        :return: :class:`OperationResult`
        :raise: :cb_exc:`NotFoundError` if the list does not exist
        :raise: :exc:`IndexError` if the index is out of bounds

        example::

            cb.upsert('a_list', ['hello', 'world'])
            cb.list_set('a_list', 1, 'good')
            cb.get('a_list').value # => ['hello', 'good']

        .. seealso:: :meth:`map_add`, :meth:`list_append`
        """
        op = SD.replace('[{0}]'.format(index), value)
        sdres = Client.mutate_in(self, key, (op,), **kwargs)
        return self._wrap_dsop(sdres, **kwargs)

    @_dsop(create_type=list)
    def set_add(self, key, value, create=False, **kwargs):
        """
        Add an item to a set if the item does not yet exist.

        :param key: The document ID
        :param value: Value to add
        :param create: Create the set if it does not exist
        :param kwargs: Arguments to :meth:`mutate_in`
        :return: A :class:`~.OperationResult` if the item was added,
        :raise: :cb_exc:`NotFoundError` if the document does not exist
            and `create` was not specified.

        .. seealso:: :meth:`map_add`
        """
        op = SD.array_addunique('', value)
        try:
            sdres = Client.mutate_in(self, key, (op,), **kwargs)
            return self._wrap_dsop(sdres, **kwargs)
        except E.SubdocPathExistsError:
            pass

    @_dsop()
    def set_remove(self, key, value, **kwargs):
        """
        Remove an item from a set.

        :param key: The docuent ID
        :param value: Value to remove
        :param kwargs: Arguments to :meth:`mutate_in`
        :return: A :class:`OperationResult` if the item was removed, false
                 otherwise
        :raise: :cb_exc:`NotFoundError` if the set does not exist.

        .. seealso:: :meth:`set_add`, :meth:`map_add`
        """
        while True:
            rv = Client.get(self, key)
            try:
                ix = rv.value.index(value)
                kwargs['cas'] = rv.cas
                return Client.list_remove(self, key, ix, **kwargs)
            except E.KeyExistsError:
                pass
            except ValueError:
                return

    def set_size(self, key):
        """
        Get the length of a set.

        :param key: The document ID of the set
        :return: The length of the set
        :raise: :cb_exc:`NotFoundError` if the set does not exist.

        """
        return Client.list_size(self, key)

    def set_contains(self, key, value):
        """
        Determine if an item exists in a set
        :param key: The document ID of the set
        :param value: The value to check for
        :return: True if `value` exists in the set
        :raise: :cb_exc:`NotFoundError` if the document does not exist
        """
        rv = Client.get(self, key)
        return value in rv.value

    @_dsop()
    def list_get(self, key, index):
        """
        Get a specific element within a list.

        :param key: The document ID
        :param index: The index to retrieve
        :return: :class:`ValueResult` for the element
        :raise: :exc:`IndexError` if the index does not exist
        :raise: :cb_exc:`NotFoundError` if the list does not exist
        """
        return Client.map_get(self, key, '[{0}]'.format(index))

    @_dsop()
    def list_remove(self, key, index, **kwargs):
        """
        Remove the element at a specific index from a list.

        :param key: The document ID of the list
        :param index: The index to remove
        :param kwargs: Arguments to :meth:`mutate_in`
        :return: :class:`OperationResult`
        :raise: :exc:`IndexError` if the index does not exist
        :raise: :cb_exc:`NotFoundError` if the list does not exist
        """
        return Client.map_remove(self, key, '[{0}]'.format(index), **kwargs)

    @_dsop()
    def list_size(self, key):
        """
        Retrieve the number of elements in the list.

        :param key: The document ID of the list
        :return: The number of elements within the list
        :raise: :cb_exc:`NotFoundError` if the list does not exist
        """
        return Client.map_size(self, key)

    @_dsop(create_type=list)
    def queue_push(self, key, value, create=False, **kwargs):
        """
        Add an item to the end of a queue.

        :param key: The document ID of the queue
        :param value: The item to add to the queue
        :param create: Whether the queue should be created if it does not exist
        :param kwargs: Arguments to pass to :meth:`mutate_in`
        :return: :class:`OperationResult`
        :raise: :cb_exc:`NotFoundError` if the queue does not exist and
            `create` was not specified.

        example::

            # Ensure it's removed first

            cb.remove('a_queue')
            cb.queue_push('a_queue', 'job9999', create=True)
            cb.queue_pop('a_queue').value  # => job9999
        """
        return Client.list_prepend(self, key, value, **kwargs)

    @_dsop()
    def queue_pop(self, key, **kwargs):
        """
        Remove and return the first item queue.

        :param key: The document ID
        :param kwargs: Arguments passed to :meth:`mutate_in`
        :return: A :class:`ValueResult`
        :raise: :cb_exc:`QueueEmpty` if there are no items in the queue.
        :raise: :cb_exc:`NotFoundError` if the queue does not exist.
        """
        while True:
            try:
                itm = Client.list_get(self, key, -1)
            except IndexError:
                raise E.QueueEmpty

            kwargs.update({k:v for k,v in getattr(itm,'__dict__',{}).items() if k in {'cas'}})
            try:
                Client.list_remove(self, key, -1, **kwargs)
                return itm
            except E.KeyExistsError:
                pass
            except IndexError:
                raise E.QueueEmpty

    @_dsop()
    def queue_size(self, key):
        """
        Get the length of the queue.

        :param key: The document ID of the queue
        :return: The length of the queue
        :raise: :cb_exc:`NotFoundError` if the queue does not exist.
        """
        return Client.list_size(self, key)

    dsops = (map_get,
             map_add,
             map_remove,
             queue_push,
             list_size,
             map_size,
             queue_pop,

             list_set,
             list_remove,
             list_prepend,
             list_get,
             queue_size,

             list_append,
             set_add,
             set_contains,
             set_remove,
             set_size)

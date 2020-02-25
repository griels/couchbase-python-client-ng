#
# Copyright 2013, Couchbase, Inc.
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
"""
The contents of this module do not have a stable API and are subject to
change
"""
from json import JSONEncoder
from time import time, sleep

import couchbase_core._libcouchbase as LCB
from boltons.funcutils import wraps

from couchbase_core import JSON, mk_formstr
import couchbase_core.exceptions as E
from couchbase_core._pyport import basestring
from couchbase_core.auth_domain import AuthDomain
from couchbase_core._libcouchbase import FMT_JSON
import re

METHMAP = {
    'GET': LCB.LCB_HTTP_METHOD_GET,
    'PUT': LCB.LCB_HTTP_METHOD_PUT,
    'POST': LCB.LCB_HTTP_METHOD_POST,
    'DELETE': LCB.LCB_HTTP_METHOD_DELETE
}


class NotReadyError(E.CouchbaseError):
    """
    Thrown when not all nodes could be ready (internal)
    """
    pass


class Admin(LCB.Collection):
    """
    An administrative connection to a Couchbase cluster.

    With this object, you can do things which affect the cluster, such as
    modifying buckets, allocating nodes, or retrieving information about
    the cluster.

    This object should **not** be used to perform Key/Value operations. The
    :class:`~couchbase_core.client.Client` is used for that.
    """
    def __init__(self, username, password, host='localhost', port=8091,
                 **kwargs):

        """Connect to a cluster

        :param string username: The administrative username for the cluster,
          this is typically ``Administrator``
        :param string password: The administrative password for the cluster,
          this is the password you entered when Couchbase was installed
        :param string host: The hostname or IP of one of the nodes which is
          currently a member of the cluster (or a newly allocated node, if
          you wish to operate on that)
        :param int port: The management port for the node

        :raise:
            :exc:`couchbase_core.exceptions.AuthError` if incorrect credentials
            were supplied

            :exc:`couchbase_core.exceptions.ConnectError` if there was a problem
            establishing a connection to the provided host

        :return: an instance of :class:`Admin`
        """
        connection_string = kwargs.pop('connection_string', None)
        bucket = kwargs.pop('bucket', 'default')
        if not connection_string:
            connection_string = "http://{0}:{1}".format(host, port)
            connection_string += "/{0}".format(bucket)
            connection_string += "?ipv6=" + kwargs.pop('ipv6', 'disabled')

        kwargs.update({
            'username': username,
            'password': password,
            'connection_string': connection_string,
            '_conntype': LCB.LCB_TYPE_CLUSTER
        })
        kwargs['bucket']=bucket
        super(Admin, self).__init__(**kwargs)
        self._connect()

    def http_request(self,
                     path,
                     method='GET',
                     content=None,
                     content_type="application/json",
                     response_format=FMT_JSON,
                     timeout=None):
        """
        Perform an administrative HTTP request. This request is sent out to
        the administrative API interface (i.e. the "Management/REST API")
        of the cluster.

        Note that this is a fairly low level function. You should use one
        of the helper methods in this class to perform your task, if
        possible.

        :param string path: The path portion (not including the host) of the
          rest call to perform. This should also include any encoded arguments.

        :param string method: This is the HTTP method to perform. Currently
          supported values are `GET`, `POST`, `PUT`, and `DELETE`

        :param bytes content: Content to be passed along in the request body.
          This is only applicable on `PUT` and `POST` methods.

        :param string content_type: Value for the HTTP ``Content-Type`` header.
          Currently this is ``application-json``, and should probably not be
          set to something else.

        :param int response_format:
          Hint about how to format the response. This goes into the
          :attr:`~.HttpResult.value` field of the
          :class:`~.HttpResult` object. The default is
          :const:`~couchbase_core.FMT_JSON`.

          Note that if the conversion fails, the content will be returned as
          ``bytes``

        :raise:
          :exc:`~.ArgumentError`
            if the method supplied was incorrect.
          :exc:`~.ConnectError`
            if there was a problem establishing a connection.
          :exc:`~.HTTPError`
            if the server responded with a negative reply

        :return: a :class:`~.HttpResult` object.

        .. seealso:: :meth:`bucket_create`, :meth:`bucket_remove`
        """
        imeth = None
        if not method in METHMAP:
            raise E.ArgumentError.pyexc("Unknown HTTP Method", method)

        imeth = METHMAP[method]
        return self._http_request(type=LCB.LCB_HTTP_TYPE_MANAGEMENT,
                                  path=path,
                                  method=imeth,
                                  content_type=content_type,
                                  post_data=content,
                                  response_format=response_format,
                                  timeout=timeout)

    bc_defaults=dict(bucket_type='couchbase',
                  bucket_password='', replicas=0, ram_quota=1024,
                  flush_enabled=False)

    def bucket_create(self, name, **kwargs):
        """
        Create a new bucket

        :param string name: The name of the bucket to create
        :param string bucket_type: The type of bucket to create. This
            can either be `couchbase` to create a couchbase_core style
            bucket (which persists data and supports replication) or
            `memcached` (which is memory-only and does not support
            replication).
            Since Couchbase version 5.0, you can also specify
            `ephemeral`, which is a replicated bucket which does
            not have strict disk persistence requirements
        :param string bucket_password: The bucket password. This can be
            empty to disable authentication. This can be changed later on
            using :meth:`bucket_update`
        :param int replicas: The number of replicas to use for this
            bucket. The maximum number of replicas is currently 3.
            This setting can be changed via :meth:`bucket_update`
        :param int ram_quota:
            The maximum amount of memory (per node) that this bucket
            may use, in megabytes. The minimum for this value is 100.
            This setting may be changed via :meth:`bucket_update`.
        :param bool flush_enabled:
            Whether the flush API is enabled. When the flush API is
            enabled, any client connected to the bucket is able to
            clear its contents. This may be useful in development but
            not recommended in production. This setting may be changed
            via :meth:`bucket_update`
        :return: A :class:`~.HttpResult`
        :raise: :exc:`~.HTTPError` if the bucket could not be created.
        """
        final_opts = dict(**Admin.bc_defaults)
        final_opts.update(**{k: v for k, v in kwargs.items() if (v is not None)})
        params = {
            'name': name,
            'bucketType': final_opts['bucket_type'],
            'authType': 'sasl',
            'saslPassword': final_opts['bucket_password'],
            'flushEnabled': int(final_opts['flush_enabled']),
            'ramQuotaMB': final_opts['ram_quota']
        }
        if final_opts['bucket_type'] in ('couchbase', 'membase', 'ephemeral'):
            params['replicaNumber'] = final_opts['replicas']

        return self.http_request(
            path='/pools/default/buckets', method='POST',
            content=mk_formstr(params),
            content_type='application/x-www-form-urlencoded')

    def bucket_remove(self, name):
        """
        Remove an existing bucket from the cluster

        :param string name: The name of the bucket to remove
        :return: A :class:`~.HttpResult`
        :raise: :exc:`~HTTPError` on error
        """
        return self.http_request(path='/pools/default/buckets/' + name,
                                 method='DELETE')

    bucket_delete = bucket_remove

    class BucketInfo(object):
        """
        Information about a bucket
        """
        def __init__(self,
                     raw_json  # type: JSON
                     ):
            self.raw_json = raw_json

        def name(self):
            """
            Name of the bucket.
            :return: A :class:`str` containing the bucket name.
            """
            return self.raw_json.get("name")

        def __str__(self):
            return "Bucket named {}".format(self.name)

    def buckets_list(self):
        """
        Retrieve the list of buckets from the server
        :return: An iterable of :Class:`Admin.BucketInfo` objects describing
        the buckets currently active on the cluster.
        """
        buckets_list = self.http_request(path='/pools/default/buckets', method='GET')
        return map(Admin.BucketInfo, buckets_list.value)

    def bucket_info(self, name):
        """
        Retrieve information about the bucket.

        :param string name: The name of the bucket
        :return: A :class:`~.HttpResult` object. The result's
            :attr:`~.HttpResult.value` attribute contains
            A dictionary containing the bucket's information.
            The returned object is considered to be opaque, and is
            intended primarily for use with :meth:`bucket_update`.
            Currently this returns the raw decoded JSON as emitted
            by the corresponding server-side API
        :raise: :exc:`~.HTTPError` if the request failed
        """
        return self.http_request(path='/pools/default/buckets/' + name)

    def wait_ready(self, name, timeout=5.0, sleep_interval=0.2):
        """
        Wait for a newly created bucket to be ready.

        :param string name: the name to wait for
        :param seconds timeout: the maximum amount of time to wait
        :param seconds sleep_interval: the number of time to sleep
            between each probe
        :raise: :exc:`.CouchbaseError` on internal HTTP error
        :raise: :exc:`NotReadyError` if all nodes could not be
            ready in time
        """
        end = time() + timeout
        while True:
            try:
                info = self.bucket_info(name).value
                for node in info['nodes']:
                    if node['status'] != 'healthy':
                        raise NotReadyError.pyexc('Not all nodes are healthy')
                return  # No error and all OK
            except E.CouchbaseError:
                if time() + sleep_interval > end:
                    raise
                sleep(sleep_interval)

    @staticmethod
    def _get_management_path(auth_domain, userid=None):

        if auth_domain == AuthDomain.Local:
            domain = 'local'
        elif auth_domain == AuthDomain.External:
            domain = 'external'
        else:
            raise E.ArgumentError.pyexc("Unknown Authentication Domain", auth_domain)

        path = '/settings/rbac/users/{0}'.format(domain)
        if userid is not None:
            path = '{0}/{1}'.format(path, userid)

        return path

    def users_get(self, domain):
        """
        Retrieve a list of users from the server.

        :param AuthDomain domain: The authentication domain to retrieve users from.
        :return: :class:`~.HttpResult`. The list of users can be obtained from
            the returned object's `value` property.
        """
        path = self._get_management_path(domain)
        return self.http_request(path=path,
                                 method='GET')

    def user_get(self, domain, userid, **kwargs):
        """
        Retrieve a user from the server

        :param AuthDomain domain: The authentication domain for the user.
        :param userid: The user ID.
        :raise: :exc:`couchbase_core.exceptions.HTTPError` if the user does not exist.
        :return: :class:`~.HttpResult`. The user can be obtained from the
            returned object's `value` property.
        """
        path = self._get_management_path(domain, userid)
        return self.http_request(path=path,
                                 method='GET',
                                 **kwargs)

    def user_upsert(self, domain, userid, password=None, roles=None, name=None):
        """
        Upsert a user in the cluster

        :param AuthDomain domain: The authentication domain for the user.
        :param userid: The user ID
        :param password: The user password
        :param roles: A list of roles. A role can either be a simple string,
            or a list of `(role, bucket)` pairs.
        :param name: Human-readable name
        :raise: :exc:`couchbase_core.exceptions.HTTPError` if the request fails.
        :return: :class:`~.HttpResult`

        Creating a new read-only admin user ::

            adm.upsert_user(AuthDomain.Local, 'mark', 's3cr3t', ['ro_admin'])

        An example of using more complex roles ::

            adm.upsert_user(AuthDomain.Local, 'mark', 's3cr3t',
                                              [('data_reader', '*'),
                                               ('data_writer', 'inbox')])


        .. warning::

           Due to the asynchronous nature of Couchbase management APIs, it may
           take a few moments for the new user settings to take effect.
        """
        if not roles or not isinstance(roles, list):
            raise E.ArgumentError("Roles must be a non-empty list")

        if password and domain == AuthDomain.External:
            raise E.ArgumentError("External domains must not have passwords")
        role_string = self.gen_role_list(roles)
        params = {
            'roles': role_string,
        }

        if password:
            params['password'] = password
        if name:
            params['name'] = name

        form = mk_formstr(params)
        path = self._get_management_path(domain, userid)
        return self.http_request(path=path,
                                 method='PUT',
                                 content_type='application/x-www-form-urlencoded',
                                 content=form)

    @staticmethod
    def gen_role_list(roles):
        tmplist = []
        for role in roles:
            tmplist.append(Admin.role_to_str(role))
        role_string = ','.join(tmplist)
        return role_string

    @staticmethod
    def role_to_str(role):
        name=None
        bucket=None
        try:
            if isinstance(role, basestring):
                name=role
            elif isinstance(role, dict):
                name, bucket = map(role.get, ('role','bucket'))
            else:
                name, bucket = role
        except Exception as e:
            pass
        if name and bucket:
            return '{0}[{1}]'.format(name,bucket)
        else:
            return name

    role_format = re.compile(r'^(?P<role>.*?)(|\[(?P<bucket>.*?)\])$')

    @staticmethod
    def str_to_role(param):
        return Admin.role_format.match(param).groupdict()

    def user_remove(self, domain, userid, **kwargs):
        """
        Remove a user
        :param AuthDomain domain: The authentication domain for the user.
        :param userid: The user ID to remove
        :raise: :exc:`couchbase_core.exceptions.HTTPError` if the user does not exist.
        :return: :class:`~.HttpResult`
        """
        path = self._get_management_path(domain, userid)
        return self.http_request(path=path,
                                 method='DELETE',
                                 **kwargs)

    # Add aliases to match RFC
    # Python SDK so far has used object-verb where RFC uses verb-object
    get_user = user_get
    get_users = users_get
    upsert_user = user_upsert
    remove_user = user_remove

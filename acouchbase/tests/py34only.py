import asyncio

from couchbase_core.experimental import enable; enable()
from .fixtures import asynct, AioTestCase
from couchbase_core.n1ql import N1QLQuery
from couchbase.exceptions import CouchbaseException
from unittest import SkipTest


class CouchbaseBeerTest(AioTestCase):
    def setUp(self, **kwargs):
        try:
            return super(CouchbaseBeerTest,self).setUp(bucket='beer-sample', **kwargs)
        except CouchbaseException:
            raise SkipTest("Need 'beer-sample' bucket for this")


class CouchbaseBeerKVTest(CouchbaseBeerTest):
    def setUp(self):
        super(CouchbaseBeerKVTest, self).setUp()

    @asynct
    @asyncio.coroutine
    def test_get_data(self):
        connargs=self.make_connargs(bucket='beer-sample')
        beer_default_collection = self.gen_collection(**connargs)

        yield from (beer_default_collection.on_connect() or asyncio.sleep(0.01))

        data = yield from beer_default_collection.get('21st_amendment_brewery_cafe')
        self.assertEqual("21st Amendment Brewery Cafe", data.content["name"])


class CouchbaseBeerViewTest(CouchbaseBeerTest):
    def setUp(self):
        super(CouchbaseBeerViewTest, self).setUp(type='Bucket')
    @asynct
    @asyncio.coroutine
    def test_query(self):

        beer_bucket = self.gen_cluster(**self.make_connargs()).bucket('beer-sample')

        yield from (beer_bucket.on_connect() or asyncio.sleep(0.01))
        viewiter = beer_bucket.view_query("beer", "brewery_beers", limit=10)
        yield from viewiter.future

        count = len(list(viewiter))

        self.assertEqual(count, 10)


class CouchbaseDefaultTestKV(AioTestCase):
    @asynct
    @asyncio.coroutine
    def test_upsert(self):
        import uuid

        expected = str(uuid.uuid4())

        default_collection = self.gen_collection(**self.make_connargs())
        yield from (default_collection.on_connect() or asyncio.sleep(0.01))

        yield from default_collection.upsert('hello', {"key": expected})

        obtained = yield from default_collection.get('hello')
        self.assertEqual({"key": expected}, obtained.content)


class CouchbaseDefaultTestN1QL(AioTestCase):
    def setUp(self, **kwargs):
        super(CouchbaseDefaultTestN1QL, self).setUp(type='Bucket',**kwargs)

    @asynct
    @asyncio.coroutine
    def test_n1ql(self):

        cluster = self.gen_cluster(**self.make_connargs())
        yield from (cluster.on_connect() or asyncio.sleep(0.01))

        it = cluster.query("SELECT mockrow")
        yield from it.future

        data = list(it)
        self.assertEqual('value', data[0]['row'])


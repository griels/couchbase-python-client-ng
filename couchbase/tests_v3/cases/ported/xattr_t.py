from couchbase.exceptions import  PathNotFoundException
from couchbase_tests.base import MockTestCase, CollectionTestCase
import couchbase.subdocument as SD


class XattrTest(CollectionTestCase):
    def test_xattrs_basic(self):
        cb = self.cb
        k = self.gen_key('xattrs')
        cb.upsert(k, {})

        # Try to upsert a single xattr
        rv = cb.mutate_in(k, [SD.upsert('my.attr', 'value',
                                       xattr=True,
                                       create_parents=True)])
        self.assertTrue(rv.success)

        body = cb.get(k)
        self.assertFalse('my' in body.content)
        self.assertFalse('my.attr' in body.content)

        # Try using lookup_in
        rv = cb.lookup_in(k, (SD.get('my.attr'),))
        self.assertRaises(PathNotFoundException, rv.exists, 0)

        # Finally, use lookup_in with 'xattrs' attribute enabled
        rv = cb.lookup_in(k, (SD.get('my.attr', xattr=True),))
        self.assertTrue(rv.exists(0))
        self.assertEqual('value', rv.content_as[str](0))
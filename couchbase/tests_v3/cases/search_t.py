# -*- coding:utf-8 -*-
#
# Copyright 2020, Couchbase, Inc.
# All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from unittest import SkipTest

import couchbase.search as search
from couchbase.management.search import SearchIndex
from couchbase.search import SearchResult
from couchbase_core.mutation_state import MutationState
from couchbase_tests.base import CouchbaseTestCase

try:
    from abc import ABC
except:
    from abc import ABCMeta

import time

import couchbase.exceptions

from couchbase import timedelta, iterable_wrapper

from couchbase_tests.base import ClusterTestCase
import couchbase.management
import json


class MRESWrapper(object):
    def __init__(self, **orig_json):
        self._orig_json=orig_json
        self._hits=self._orig_json['data'].pop('hits')
        self.done=False
        try:
            self._iterhits=iter(self._hits)
        except Exception as e:
            raise
    @property
    def value(self):
        return self._orig_json['data']
    def fetch(self, _):
        yield from self._iterhits
        self.done=True


class SearchRequestMock(search.SearchRequest):
    def __init__(self, body, parent, orig_json, **kwargs):
        self._orig_json=orig_json
        super(SearchRequestMock, self).__init__(body, parent, **kwargs)

    def _start(self):
        if self._mres:
            return

        self._mres = {None: MRESWrapper(**self._orig_json)}
        self.__raw = self._mres[None]
    @property
    def raw(self):
        try:
            return self._mres[None]
        except Exception as e:
            raise


class SearchResultMock(search.SearchResultBase, iterable_wrapper(SearchRequestMock)):
    pass


class SearchTest(ClusterTestCase):
    def setUp(self, *args, **kwargs):
        super(SearchTest, self).setUp(**kwargs)
        if self.is_mock:
            raise SkipTest("Search not available on Mock")
        self.cluster.search_indexes().upsert_index(
            SearchIndex(name="beer-search", idx_type="fulltext-index", source_type="couchbase", source_name="beer-sample"))

    def test_locations(self):
        initial = time.time()
        x = self.try_n_times_decorator(self.cluster.search_query, 10, 10)("beer-search", search.MatchQuery("Budweiser", prefix_length=0, fuzziness=0),
                                                                          search.SearchOptions(fields=["*"],limit=10, sort=["-_score"])
                                                                          )  # type: SearchResult
        self._check_search_result(initial, 6, x)

    def test_parsing_locations(self):
        with open("../sdk-testcases/search/good-response-61.json") as good_response_f:
            input=good_response_f.read()
            raw_json=json.loads(input)
            good_response = SearchResultMock(None, None, raw_json)
            first_row=good_response.rows()[0]
            self.assertIsInstance(first_row,search.SearchRow)
            locations=first_row.locations
            self.assertEqual(
                [search.SearchRowLocation(field='airlineid', term='airline_137', position=1, start=0, end=11, array_positions=None)], locations.get("airlineid", "airline_137"))
            self.assertEqual([search.SearchRowLocation(field='airlineid', term='airline_137', position=1, start=0, end=11, array_positions=None)], locations.get_all())
            self.assertSetEqual({'airline_137'}, locations.terms())
            self.assertEqual(['airline_137'], locations.terms_for("airlineid"))
            metadata=good_response.metadata()
            self.assertIsInstance(metadata, search.SearchMetaData)
            self.assertIsInstance(metadata.metrics, search.SearchMetrics)

            for key, err in metadata.errors.items():
                self.assertIsInstance(err, str)


    def test_cluster_search(self  # type: SearchTest
                            ):
        if self.is_mock:
            raise SkipTest("F.T.S. not supported by mock")
        most_common_term_max = 10
        initial = time.time()
        x = self.try_n_times_decorator(self.cluster.search_query, 10, 10)("beer-search", search.TermQuery("category"),
                                                                          facets={'fred': search.TermFacet('category',
                                                                                                           most_common_term_max)})  # type: SearchResult
        first_entry = x.rows()[0]
        self.assertEqual("brasserie_de_brunehaut-mont_st_aubert", first_entry.id)
        self._check_search_result(initial, 6, x)
        fred_facet = x.facets()['fred']
        self.assertIsInstance(fred_facet, search.SearchFacetResult)
        # self.assertEqual(len(fred_facet.terms()), most_common_term_max)

        self.assertRaises(couchbase.exceptions.SearchException, self.cluster.search_query, "beer-search",
                          search.TermQuery("category"),
                          facets={'fred': None})

    def _check_search_result(self, initial, min_hits, x):
        duration = time.time() - initial
        self.assertGreaterEqual(len(x.rows()), min_hits)
        for entry in x.rows():
            self.assertIsInstance(entry, search.SearchRow)
            self.assertIsInstance(entry.id, str)
            self.assertIsInstance(entry.score, float)
            self.assertIsInstance(entry.index, str)
            self.assertIsInstance(entry.fields, search.SearchRowFields)
            self.assertIsInstance(entry.locations, search.SearchRowLocations)
            print(entry)
            for location in entry.fields:
                self.assertIsInstance(location)
        metadata = x.metadata()
        self.assertIsInstance(metadata, search.SearchMetaData)
        metrics=metadata.metrics
        self.assertIsInstance(metrics.error_partition_count, int)
        self.assertIsInstance(metrics.max_score, float)
        self.assertIsInstance(metrics.success_partition_count, int)
        self.assertEqual(metrics.error_partition_count+metrics.success_partition_count, metrics.total_partition_count)
        took = metrics.took()
        self.assertIsInstance(took, timedelta)
        # TODO: lets revisit why we chose this 0.1.  I often find the difference is greater,
        # running the tests locally.  Commenting out for now...
        # self.assertAlmostEqual(took.total_seconds(), duration, delta=0.1)
        self.assertGreater(took.total_seconds(), 0)
        self.assertIsInstance(metadata.total_hits(), int)
        self.assertGreaterEqual(metadata.success_count(), min_hits)
        self.assertGreaterEqual(metadata.total_hits(), min_hits)


class SearchStringsTest(CouchbaseTestCase):
    def test_fuzzy(self):
        q = search.TermQuery('someterm', field='field', boost=1.5,
                               prefix_length=23, fuzziness=12)
        p = search.Params(explain=True)

        exp_json = {
            'query': {
                'term': 'someterm',
                'boost': 1.5,
                'fuzziness':  12,
                'prefix_length': 23,
                'field': 'field'
            },
            'indexName': 'someIndex',
            'explain': True
        }

        self.assertEqual(exp_json, search.make_search_body('someIndex', q, p))

    def test_match_phrase(self):
        exp_json = {
            'query': {
                'match_phrase': 'salty beers',
                'analyzer': 'analyzer',
                'boost': 1.5,
                'field': 'field'
            },
            'size': 10,
            'indexName': 'ix'
        }

        p = search.Params(limit=10)
        q = search.MatchPhraseQuery('salty beers', boost=1.5, analyzer='analyzer',
                                      field='field')
        self.assertEqual(exp_json, search.make_search_body('ix', q, p))

    def test_match_query(self):
        exp_json = {
            'query': {
                'match': 'salty beers',
                'analyzer': 'analyzer',
                'boost': 1.5,
                'field': 'field',
                'fuzziness': 1234,
                'prefix_length': 4
            },
            'size': 10,
            'indexName': 'ix'
        }

        q = search.MatchQuery('salty beers', boost=1.5, analyzer='analyzer',
                                field='field', fuzziness=1234, prefix_length=4)
        p = search.Params(limit=10)
        self.assertEqual(exp_json, search.make_search_body('ix', q, p))

    def test_string_query(self):
        exp_json = {
            'query': {
                'query': 'q*ry',
                'boost': 2.0,
            },
            'explain': True,
            'size': 10,
            'indexName': 'ix'
        }
        q = search.QueryStringQuery('q*ry', boost=2.0)
        p = search.Params(limit=10, explain=True)
        self.assertEqual(exp_json, search.make_search_body('ix', q, p))

    def test_params(self):
        self.assertEqual({}, search.Params().as_encodable('ix'))
        self.assertEqual({'size': 10}, search.Params(limit=10).as_encodable('ix'))
        self.assertEqual({'from': 100},
                         search.Params(skip=100).as_encodable('ix'))

        self.assertEqual({'explain': True},
                         search.Params(explain=True).as_encodable('ix'))

        self.assertEqual({'highlight': {'style': 'html'}},
                         search.Params(highlight_style='html').as_encodable('ix'))

        self.assertEqual({'highlight': {'style': 'ansi',
                                        'fields': ['foo', 'bar', 'baz']}},
                         search.Params(highlight_style='ansi',
                                       highlight_fields=['foo', 'bar', 'baz'])
                         .as_encodable('ix'))

        self.assertEqual({'fields': ['foo', 'bar', 'baz']},
                         search.Params(fields=['foo', 'bar', 'baz']
                                       ).as_encodable('ix'))

        self.assertEqual({'sort': ['f1', 'f2', '-_score']},
                         search.Params(sort=['f1', 'f2', '-_score']
                                       ).as_encodable('ix'))

        self.assertEqual({'sort': ['f1', 'f2', '-_score']},
                         search.Params(sort=search.SortString(
                             'f1', 'f2', '-_score')).as_encodable('ix'))

        p = search.Params(facets={
            'term': search.TermFacet('somefield', limit=10),
            'dr': search.DateFacet('datefield').add_range('name', 'start', 'end'),
            'nr': search.NumericFacet('numfield').add_range('name2', 0.0, 99.99)
        })
        exp = {
            'facets': {
                'term': {
                    'field': 'somefield',
                    'size': 10
                },
                'dr': {
                    'field': 'datefield',
                    'date_ranges': [{
                        'name': 'name',
                        'start': 'start',
                        'end': 'end'
                    }]
                },
                'nr': {
                    'field': 'numfield',
                    'numeric_ranges': [{
                        'name': 'name2',
                        'min': 0.0,
                        'max': 99.99
                    }]
                },
            }
        }
        self.assertEqual(exp, p.as_encodable('ix'))

    def test_facets(self):
        p = search.Params()
        f = search.NumericFacet('numfield')
        self.assertRaises(ValueError, p.facets.__setitem__, 'facetName', f)
        self.assertRaises(TypeError, f.add_range, 'range1')
        p.facets['facetName'] = f.add_range('range1', min=123, max=321)
        self.assertTrue('facetName' in p.facets)

        f = search.DateFacet('datefield')
        f.add_range('r1', start='2012', end='2013')
        f.add_range('r2', start='2014')
        f.add_range('r3', end='2015')
        exp = {
            'field': 'datefield',
            'date_ranges': [
                {'name': 'r1', 'start': '2012', 'end': '2013'},
                {'name': 'r2', 'start': '2014'},
                {'name': 'r3', 'end': '2015'}
            ]
        }
        self.assertEqual(exp, f.encodable)

        f = search.TermFacet('termfield')
        self.assertEqual({'field': 'termfield'}, f.encodable)
        f.limit = 10
        self.assertEqual({'field': 'termfield', 'size': 10}, f.encodable)

    def test_raw_query(self):
        qq = search.RawQuery({'foo': 'bar'})
        self.assertEqual({'foo': 'bar'}, qq.encodable)

    def test_wildcard_query(self):
        qq = search.WildcardQuery('f*o', field='wc')
        self.assertEqual({'wildcard': 'f*o', 'field': 'wc'}, qq.encodable)

    def test_docid_query(self):
        qq = search.DocIdQuery([])
        self.assertRaises(search.NoChildrenError, getattr, qq, 'encodable')
        qq.ids = ['foo', 'bar', 'baz']
        self.assertEqual({'ids': ['foo', 'bar', 'baz']}, qq.encodable)

    def test_boolean_query(self):
        prefix_q = search.PrefixQuery('someterm', boost=2)
        bool_q = search.BooleanQuery(
            must=prefix_q, must_not=prefix_q, should=prefix_q)
        exp = {'prefix': 'someterm', 'boost': 2.0}
        self.assertEqual({'conjuncts': [exp]},
                         bool_q.must.encodable)
        self.assertEqual({'min': 1, 'disjuncts': [exp]},
                         bool_q.should.encodable)
        self.assertEqual({'min': 1, 'disjuncts': [exp]},
                         bool_q.must_not.encodable)

        # Test multiple criteria in must and must_not
        pq_1 = search.PrefixQuery('someterm', boost=2)
        pq_2 = search.PrefixQuery('otherterm')
        bool_q = search.BooleanQuery(must=[pq_1, pq_2])
        exp = {
            'conjuncts': [
                {'prefix': 'someterm', 'boost': 2.0},
                {'prefix': 'otherterm'}
            ]
        }
        self.assertEqual({'must': exp}, bool_q.encodable)

    def test_daterange_query(self):
        self.assertRaises(TypeError, search.DateRangeQuery)
        dr = search.DateRangeQuery(end='theEnd')
        self.assertEqual({'end': 'theEnd'}, dr.encodable)
        dr = search.DateRangeQuery(start='theStart')
        self.assertEqual({'start': 'theStart'}, dr.encodable)
        dr = search.DateRangeQuery(start='theStart', end='theEnd')
        self.assertEqual({'start': 'theStart', 'end': 'theEnd'}, dr.encodable)
        dr = search.DateRangeQuery('', '')  # Empty strings should be ok
        self.assertEqual({'start': '', 'end': ''}, dr.encodable)

    def test_numrange_query(self):
        self.assertRaises(TypeError, search.NumericRangeQuery)
        nr = search.NumericRangeQuery(0, 0)  # Should be OK
        self.assertEqual({'min': 0, 'max': 0}, nr.encodable)
        nr = search.NumericRangeQuery(0.1, 0.9)
        self.assertEqual({'min': 0.1, 'max': 0.9}, nr.encodable)
        nr = search.NumericRangeQuery(max=0.9)
        self.assertEqual({'max': 0.9}, nr.encodable)
        nr = search.NumericRangeQuery(min=0.1)
        self.assertEqual({'min': 0.1}, nr.encodable)

    def test_disjunction_query(self):
        dq = search.DisjunctionQuery()
        self.assertEqual(1, dq.min)
        self.assertRaises(search.NoChildrenError, getattr, dq, 'encodable')

        dq.disjuncts.append(search.PrefixQuery('somePrefix'))
        self.assertEqual({'min': 1, 'disjuncts': [{'prefix': 'somePrefix'}]},
                         dq.encodable)
        self.assertRaises(ValueError, setattr, dq, 'min', 0)
        dq.min = 2
        self.assertRaises(search.NoChildrenError, getattr, dq, 'encodable')

    def test_conjunction_query(self):
        cq = search.ConjunctionQuery()
        self.assertRaises(search.NoChildrenError, getattr, cq, 'encodable')
        cq.conjuncts.append(search.PrefixQuery('somePrefix'))
        self.assertEqual({'conjuncts': [{'prefix': 'somePrefix'}]},
                         cq.encodable)

    def test_match_all_none_queries(self):
        self.assertEqual({'match_all': None}, search.MatchAllQuery().encodable)
        self.assertEqual({'match_none': None}, search.MatchNoneQuery().encodable)

    def test_phrase_query(self):
        pq = search.PhraseQuery('salty', 'beers')
        self.assertEqual({'terms': ['salty', 'beers']}, pq.encodable)

        pq = search.PhraseQuery()
        self.assertRaises(search.NoChildrenError, getattr, pq, 'encodable')
        pq.terms.append('salty')
        self.assertEqual({'terms': ['salty']}, pq.encodable)

    def test_prefix_query(self):
        pq = search.PrefixQuery('someterm', boost=1.5)
        self.assertEqual({'prefix': 'someterm', 'boost': 1.5}, pq.encodable)

    def test_regexp_query(self):
        pq = search.RegexQuery('some?regex')
        self.assertEqual({'regexp': 'some?regex'}, pq.encodable)

    def test_booleanfield_query(self):
        bq = search.BooleanFieldQuery(True)
        self.assertEqual({'bool': True}, bq.encodable)

    def test_consistency(self):
        uuid = str('10000')
        vb = 42
        seq = 101
        ixname = 'ix'

        mutinfo = (vb, uuid, seq, 'dummy-bucket-name')
        ms = MutationState()
        ms._add_scanvec(mutinfo)

        params = search.Params()
        params.consistent_with(ms)
        got = search.make_search_body('ix', search.MatchNoneQuery(), params)
        exp = {
            'indexName': ixname,
            'query': {
                'match_none': None
            },
            'ctl': {
                'consistency': {
                    'level': 'at_plus',
                    'vectors': {
                        ixname: {
                            '{0}/{1}'.format(vb, uuid): seq
                        }
                    }
                }
            }
        }
        self.assertEqual(exp, got)

    def test_advanced_sort(self):
        self.assertEqual({'by': 'score'}, search.SortScore().as_encodable())
        #test legacy 'descending' support
        self.assertEqual({'by': 'score', 'desc': False},
                         search.SortScore(descending=False).as_encodable())
        #official RFC format
        self.assertEqual({'by': 'score', 'desc': False},
                         search.SortScore(desc=False).as_encodable())
        self.assertEqual({'by': 'id'}, search.SortID().as_encodable())

        self.assertEqual({'by': 'field', 'field': 'foo'},
                         search.SortField('foo').as_encodable())
        self.assertEqual({'by': 'field', 'field': 'foo', 'type': 'int'},
                         search.SortField('foo', type='int').as_encodable())

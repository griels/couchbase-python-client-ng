from couchbase_core import JSON
from couchbase.options import OptionBlock, forward_args, Seconds, JSONOptionBlock
from couchbase_core.admin import Admin
from typing import *
from enum import Enum, auto, IntEnum


class InsertCollectionOptions(OptionBlock):
    pass


class InsertScopeOptions(OptionBlock):
    pass


class CollectionManager(object):
    def __init__(self,
                 admin_bucket,  # type: Admin
                 bucket_name  # type: str
                 ):
        self.admin_bucket = admin_bucket
        self.bucket_name = bucket_name

    def insert_collection(self,
                          collection_name,  # type: str
                          scope_name,  # type: str
                          *options  # type: InsertCollectionOptions
                          ):
        """
        Upsert a collection into the parent bucket

        :param collection_name: Collection name
        :param scope_name: Scope name
        :param options:
        :return:
        """

        path = "pools/default/buckets/default/collections/{}".format(scope_name)

        params = {
            'name': collection_name
        }

        form = self.admin_bucket._mk_formstr(params)
        return self.admin_bucket.http_request(path=path,
                                 method='POST',
                                 content_type='application/x-www-form-urlencoded',
                                 content=form)

    def insert_scope(self,
                     scope_name,  # type: str
                     *options  # type: InsertScopeOptions
                     ):
        """
        Upsert a collection into the parent bucket

        :param scope_name: Scope name
        :param options:
        :return:
        """

        path = "pools/default/buckets/default/collections"

        params = {
            'name': scope_name
        }

        form = self.admin_bucket._mk_formstr(params)
        return self.admin_bucket.http_request(path=path,
                                 method='POST',
                                 content_type='application/x-www-form-urlencoded',
                                 content=form)


class ISearchIndex(object):
    pass


class SourceType(IntEnum):
    COUCHBASE = auto()
    MEMCACHED = auto()


class IndexType(Enum):
    ALIAS = 'alias'
    INDEX = 'index'
    BLEVE = 'bleve'


T = TypeVar('T', bound=OptionBlock)


class NewSearchIndexOptions(JSONOptionBlock):
    def _mappings():
        return dict(index_params='indexParams', plan_params='planParams')

    def __init__(self, *args, **kwargs):
        super(NewSearchIndexOptions, self).__init__(*args,**kwargs)

    def UUID(self,  # type: T
             value  # type: str
             ):
        # type: (...)-> T
        self['UUID'] = value
        return self

    def index_params(self,  # type: T
                     value  # type: JSON
                     ):
        # type: (...)-> T
        self['index_params'] = value
        return self

    def plan_params(self,  # type: T
                    value  # type: JSON
                    ):
        # type: (...)-> T
        self['plan_params'] = value
        return self

    def timeout(self,  # type: T
                value  # type: Seconds
                ):
        # type: (...)-> T
        self['timeout'] = value
        return self


class GetSearchIndexOptions(OptionBlock):
    pass

class InsertSearchIndexOptions(OptionBlock):
    pass

class UpsertSearchIndexOptions(NewSearchIndexOptions):
    pass


class DropSearchIndexOptions(OptionBlock):
    pass


class GetIndexedSearchIndexOptions(OptionBlock):
    pass


class SearchIndexes(object):
    def __init__(self,  # type: SearchIndexes
                 admin_bucket  # type: Admin
                 ):
        # type: (...)->None
        self.admin_bucket = admin_bucket

    def get(self,  # type: SearchIndexes
            index_name,  # type: str
            options  # type: GetSearchIndexOptions
            ):
        # type: (...)->ISearchIndex
        raise NotImplementedError()

    def get_all(self,  # type: SearchIndexes
                options  # type: GetSearchIndexOptions
                ):
        # type: (...)->Iterable[ISearchIndex]
        raise NotImplementedError()

    def create(self,  # type: SearchIndexes
               index_name,  # type: str
               index_type,  # type: IndexType
               source_type,  # type: SourceType
               source_name,  # type: str
               options  # type: InsertSearchIndexOptions
               ):
        # type: (...)->None
        raise NotImplementedError()

    def _bleve(*options  # type: NewSearchIndexOptions
               ):
        # type: (...)->JSON
        return {
            "mapping": {
                "default_mapping": {
                    "enabled": True,
                    "dynamic": True,
                    "default_analyzer": ""
                },
                "type_field": "_type",
                "default_type": "_default",
                "default_analyzer": "standard",
                "default_datetime_parser": "dateTimeOptional",
                "default_field": "_all",
                "byte_array_converter": "json",
                "analysis": {}
            },
            "store": {
                "kvStoreName": "mossStore"
            }
        }

    def _alias(*options  # type: NewSearchIndexOptions
               ):
        # type: (...)->JSON
        return {
            "targets": {
                "yourIndexName": {
                    "indexUUID": ""
                }
            }
        }

    def upsert(self,  # type: SearchIndexes
               index_name,  # type: str
               index_type,  # type: IndexType
               source_type,  # type: SourceType
               source_name,  # type: str
               UUID=None,  # type: str
               index_params=None,  # type: JSON
               plan_params=None,  # type: JSON
               timeout=None  # type: Seconds
               ):
        # type: (...)->None
        pass

    def upsert(self,  # type: SearchIndexes
               index_name,  # type: str
               index_type,  # type: IndexType
               source_type,  # type: SourceType
               source_name,  # type: str
               *options,  # type: UpsertSearchIndexOptions
               ):
        # type: (...)->None
        pass

    def upsert(self,  # type: SearchIndexes
               index_name,  # type: str
               index_type,  # type: IndexType
               source_type,  # type: SourceType
               source_name,  # type: str
               *options,  # type: UpsertSearchIndexOptions
               **kwargs  # type: Any
               ):
        # type: (...)->None

        final_opts=forward_args(kwargs,*options)
        index_params_fn = {IndexType.ALIAS: SearchIndexes._alias,
                           IndexType.BLEVE: SearchIndexes._bleve}.get(index_type)
        params = {'indexParams': index_params_fn(source_type=source_type,
                                                 source_name=source_name,
                                                 **final_opts)} if index_params_fn else {}

        params.update(indexType=index_type.value)
        params.update(NewSearchIndexOptions.as_json(final_opts))

        content=self.admin_bucket._mk_formstr(params)
        return self.admin_bucket.http_request("/api/index/{}".format(index_name), 'PUT', content)

    def drop(self,  # type: SearchIndexes
             indexName,  # type: str
             options  # type: DropSearchIndexOptions
             ):
        # type: (...)->None
        raise NotImplementedError()

    def get_indexed_documents_count(self,  # type: SearchIndexes
                                    index_name,  # type: str
                                    options  # type: GetIndexedSearchIndexOptions
                                    ):
        # type: (...)->ISearchIndex
        raise NotImplementedError()

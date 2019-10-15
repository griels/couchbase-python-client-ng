from couchbase.management.generic import GenericManager
from typing import *


class AnalyticsIndexManager(GenericManager):
    def __init__(self, parent_cluster):
        super(AnalyticsIndexManager, self).__init__(parent_cluster)

    def create_dataverse(self,  # type: AnalyticsIndexManager
                         dataverseName,  # type: str
                         options  # type: CreateDataverseAnalyticsOptions
                         ):
        """
        Create Dataverse
        Creates a new dataverse.
        Signature
        void CreateDataverse(string dataverseName, [options])
        Parameters
        Required:
        dataverseName: string - name of the dataverse.
        Optional:
        IgnoreIfExists (bool) - ignore if the dataset already exists (send "IF NOT EXISTS" as part of the dataset creation query, e.g. CREATE DATAVERSE IF NOT EXISTS test ON default). Default to false.
        Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.
        Returns
        Throws
        DataverseAlreadyExistsException
        InvalidArgumentsException
        Any exceptions raised by the underlying platform"""

    def drop_dataverse(self,  # type: AnalyticsIndexManager
                       dataverseName,  # type: str
                       options  # type: DropDataverseAnalyticsOptions
                       ):
        """
        Drop Dataverse
        Drops a dataverse.
        Signature
        void DropDataverse(string dataverseName,  [options])
        Parameters
        Required:
        dataverseName: string - name of the dataverse.
        Optional:
        IgnoreIfNotExists (bool) - ignore if the dataset doesn't exists (send "IF EXISTS" as part of the dataset creation query, e.g. DROP DATAVERSE IF EXISTS test).
        Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.
        Returns
        Throws
        DataverseNotFoundException
        InvalidArgumentsException
        Any exceptions raised by the underlying platform"""

    def create_dataset(self,  # type: AnalyticsIndexManager
                       bucket_name,  # type: str
                       datasetName,  # type: str
                       options  # type: CreateDatasetAnalyticsOptions
                       ):
        """
        CreateDataset
        Creates a new dataset.
        Signature
        void CreateDataset(string datasetName, string bucket_name, [options])
        Parameters
        Required:
        datasetName: string - name of the dataset.
        bucket_name: string - name of the bucket.
        Optional:
        IgnoreIfExists (bool) - ignore if the dataset already exists (send "IF NOT EXISTS" as part of the dataset creation query, e.g. CREATE DATASET IF NOT EXISTS test ON default).c
        Condition (string) - Where clause to use for creating dataset.
        dataverse_name (string) - The name of the dataverse to use, default to none. If set then will be used as CREATE DATASET dataverseName.datasetName. If not set then will be CREATE DATASET datasetName.
        Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.
        Returns
        Throws
        DatasetAlreadyExistsException
        InvalidArgumentsException
        Any exceptions raised by the underlying platform"""

    def drop_dataset(self,  # type: AnalyticsIndexManager
                     datasetName,  # type: str
                     options  # type: DropDatasetAnalyticsOptions
                     ):
        """
        DropDataset
        Drops a dataset.
        Signature
        void DropDataset(string datasetName,  [options])
        Parameters
        Required:
        datasetName: string - name of the dataset.
        Optional:
        IgnoreIfNotExists (bool) - ignore if the dataset doesn't exists (send "IF EXISTS" as part of the dataset creation query, e.g. DROP DATASET IF EXISTS test).
        dataverse_name (string) - The name of the dataverse to use, default to none. If set then will be used as DROP DATASET dataverseName.datasetName. If not set then will be DROP DATASET datasetName.
        Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.
        Returns
        Throws
        DatasetNotFoundException
        InvalidArgumentsException
        Any exceptions raised by the underlying platform
        """

    def get_all_datasets(self,  # type: AnalyticsIndexManager
                         options  # type: GetAllDatasetAnalyticsOptions
                         ):
        # type: (...)->Iterable[AnalyticsDataset]

        """GetAllDatasets
        Gets all datasets (SELECT d.* FROM Metadata.`Dataset` d WHERE d.DataverseName <> "Metadata").
        Signature
        Iterable<AnalyticsDataset> GetAllDatasets([options])
        Parameters
        Required:
        Optional:
        Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.
        Returns
        Throws
        Any exceptions raised by the underlying platform"""

    def create_index(self,  # type: AnalyticsIndexManager
                     index_name,  # type: str
                     options  # type: CreateIndexAnalyticsOptions
                     ):
        """
        CreateIndex
        Creates a new index.
        Signature
        void CreateIndex(string index_name, string datasetName, map[string]string fields,  [options])
        Parameters
        Required:
        dataset_name: string - name of the dataset.
        index_name: string - name of the index.
        fields: map[string]string - the fields to create the index over. This is a map of the name of the field to the type of the field.
        Optional:
        IgnoreIfExists (bool) - don't error/throw if the index already exists. (send "IF NOT EXISTS" as part of the dataset creation query, e.g. CREATE INDEX test IF NOT EXISTS ON default) (Note: IF NOT EXISTS is not is in the same place as it is in CREATE DATASET)
        dataverse_name (string) - The name of the dataverse to use, default to none. If set then will be used as CREATE INDEX dataverseName.datasetName.index_name. If not set then will be CREATE INDEX datasetName.index_name.
        Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.Returns


        AnalyticsIndexAlreadyExistsException
        InvalidArgumentsException
        Any exceptions raised by the underlying platform"""

    def drop_index(self,  # type: AnalyticsIndexManager
                   datasetName,  # type: str
                   index_name,  # type: str,
                   options  # type: DropIndexAnalyticsOptions
                   ):
        """
        DropIndex
        Drops an index.
        Throws
        Signature
        void DropIndex(string index_name, string datasetName, [options])
        Parameters
        Required:
        index_name: string - name of the index.
        Optional:
        IgnoreIfNotExists (bool) - Don't error/throw if the index does not exist.
        dataverse_name (string) - The name of the dataverse to use, default to none. If set then will be used as DROP INDEX dataverseName.datasetName.index_name. If not set then will be DROP INDEX datasetName.index_name.
        Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.
        Returns
        Throws
        AnalyticsIndexNotFoundException
        InvalidArgumentsException
        Any exceptions raised by the underlying platform"""

    def get_all_indexes(self,  # type: AnalyticsIndexManager
                        options  # type: GetAllIndexesAnalyticsOptions
                        ):
        # type: (...)->Iterable[AnalyticsIndex]
        """
        GetAlIndexes
        Gets all indexes (SELECT d.* FROM Metadata.`Index` d WHERE d.DataverseName <> "Metadata").
        Signature
        Iterable<AnalyticsIndex> GetAllIndexes([options])
        Parameters
        Required:
        Optional:
        Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.
        Returns
        Throws
        Any exceptions raised by the underlying platform"""

    def connect_link(self,  # type: AnalyticsIndexManager
                     linkName,  # type: str
                     options  # type: ConnectLinkAnalyticsOptions
                     ):
        """
        Connect Link
        Connects a link.
        Signature
        void ConnectLink([options])
        Parameters
        Required:
        Optional:
        linkName: string - name of the link. Default to "Local".
        Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.
        Returns
        Throws
        AnalyticsLinkNotFoundException
        InvalidArgumentsException
        Any exceptions raised by the underlying platform"""

    def disconnect_link(self,  # type: AnalyticsIndexManager
                        linkName,  # type: str
                        options  # type: DisconnectLinkAnalyticsOptions
                        ):
        """
        Disconnect Link
        Disconnects a link.
        Signature
        void DisconnectLink([options])
        Parameters
        Required:
        Optional:
        linkName: string - name of the link. Default to "Local".
        Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.
        Returns
        Throws
        AnalyticsLinkNotFoundException
        InvalidArgumentsException
        Any exceptions raised by the underlying platform"""

    def get_pending_mutations(self,  # type: AnalyticsIndexManager
                              options  # type: GetPendingMutationsAnalyticsOptions
                              ):
        # type: (...)->int
        """
        Get Pending Mutations
        Gets the pending mutations for all datasets. This is returned in the form of dataverse.dataset: mutations. E.g.:
        {
            "Default.travel": 20688,
            "Default.thing": 0,
            "Default.default": 0,
            "Notdefault.default": 0
        }
        Note that if a link is disconnected then it will return no results. If all links are disconnected then an empty object is returned.
        Signature
        map[string]int GetPendingMutations( [options])
        Parameters
        Required:
        Optional:
        Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.
        Returns
        Throws
        Any exceptions raised by the underlying platform
        Uri
        GET http://localhost:8095/analytics/node/agg/stats/remaining"""


class AnalyticsDataset(object):
    def __init__(self):
        """AnalyticsDataset provides a means of mapping dataset details into an object."""

    @property
    def name(self):
        # type: (...)->str
        pass

    @property
    def dataverse_name(self):
        # type: (...)->str
        pass

    @property
    def link_name(self):
        # type: (...)->str
        pass

    @property
    def bucket_name(self):
        # type: (...)->str
        pass


class AnalyticsIndex(object):
    def __init__(self):
        """AnalyticsIndex provides a means of mapping analytics index details into an object."""

    @property
    def Name(self):
        # type: (...)->str
        pass

    @property
    def dataset_name(self):
        # type: (...)->str
        pass

    @property
    def dataverse_name(self):
        # type: (...)->str
        pass

    @property
    def IsPrimary(self):
        # type: (...)->bool
        pass


class CreateDataverseAnalyticsOptions(object):
    pass


class DropDataverseAnalyticsOptions(object):
    pass


class CreateDatasetAnalyticsOptions(object):
    pass


class DropDatasetAnalyticsOptions(object):
    pass


class AnalyticsDataset(object):
    pass


class GetAllDatasetAnalyticsOptions(object):
    pass


class CreateIndexAnalyticsOptions(object):
    pass


class DropIndexAnalyticsOptions(object):
    pass


class AnalyticsIndex(object):
    pass


class GetAllIndexesAnalyticsOptions(object):
    pass


class ConnectLinkAnalyticsOptions(object):
    pass


class DisconnectLinkAnalyticsOptions(object):
    pass


class GetPendingMutationsAnalyticsOptions(object):
    pass


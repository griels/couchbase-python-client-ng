SDK 3.0: Management APIs RFC

SDK-RFC #54

# Meta

*   Name: SDK Management APIs
*   RFC ID: 54
*   Start-Date: 2019-06-13
*   Owner: Charles Dixon
*   Current Status: draft







[Meta](#h.d61txvmb5lyx)

[Summary](#h.mupne99cshsu)

[Motivation](#h.fd9za96e3yg5)

[General Design](#h.k3nh685gh3zd)

[Service Not Configured](#h.fazo4li6zut4)

[Feature Not Found](#h.g3sb6exbieep)

[View Index Manager](#h.awf5c5g6sfub)

[Methods](#h.ltp1wzfhvkmd)

[GetDesignDocument](#h.9xwvwfmx35g1)

[GetAllDesignDocuments](#h.3cni9ir8h3pd)

[UpsertDesignDocument](#h.myqscrntq9od)

[DropDesignDocument](#h.fejq3trrq88k)

[PublishDesignDocument](#h.ytabqazgaibt)

[Query Index Manager](#h.vor45gro2p0)

[Methods](#h.vpcih9gceh5x)

[GetAllIndexes](#h.d9bt9ug8rdnk)

[CreateIndex](#h.25pbsjaw1r1t)

[CreatePrimaryIndex](#h.i3nri1f7emcm)

[DropIndex](#h.w5uphn3aj7a6)

[DropPrimaryIndex](#h.8fkshrim697h)

[WatchIndexes](#h.1jpy9kneh3ix)

[BuildDeferredIndexes](#h.2g1b86t843xh)

[Search Index Manager](#h.n72o3wjrgzcr)

[Methods](#h.7ypleagc8f02)

[GetIndex](#h.muduzks94csy)

[GetAllIndexes](#h.rm7ralf543po)

[UpsertIndex](#h.vojyv926dm9l)

[DropIndex](#h.7kr1kyi2cud7)

[GetIndexedDocumentsCount](#h.920wzxyyn8h0)

[PauseIngest](#h.shct6uc5c13v)

[ResumeIngest](#h.7b3my87vq187)

[AllowQuerying](#h.3b0hek5e6cru)

[DisallowQuerying](#h.burvg6qrwgc1)

[FreezePlan](#h.xed0g6nk80ih)

[UnfreezePlan](#h.o6413lybnsbd)

[AnalyzeDocument](#h.slz9r181j64v)

[Analytics Index Manager](#h.wey00euqxg6r)

[Create Dataverse](#h.84qyvlkb4ct)

[Drop Dataverse](#h.duuryzz83ji6)

[CreateDataset](#h.p8q696h2j1c2)

[DropDataset](#h.diqletr3ee8t)

[GetAllDatasets](#h.yeup6dx0ca2i)

[CreateIndex](#h.s2ix1a2i9750)

[DropIndex](#h.sp8nw6p5hw3y)

[GetAlIndexes](#h.gu1vgfz28b4q)

[Connect Link](#h.urr6tlame907)

[Disconnect Link](#h.f24cpp9is9ur)

[Get Pending Mutations](#h.43ulyhfxecvc)

[Bucket Manager](#h.a3jxd57mov7x)

[CreateBucket](#h.7azm73gy346n)

[UpdateBucket](#h.z6hp9xboxiox)

[DropBucket](#h.40gpci3gs7n9)

[GetBucket](#h.hsjjz8tpuhmp)

[GetAllBuckets](#h.rxc15d7zi17u)

[FlushBucket](#h.6lr2bzo2rpmg)

[User Manager](#h.e1pyjdt66quk)

[Role](#h.zhz0katumzwe)

[RoleAndDescription](#h.dvcwkh4ud3go)

[Origin](#h.n3o3qrb2hyz0)

[RoleAndOrigins](#h.qxxi2pw80si1)

[User](#h.3t1esyo2jmzd)

[UserAndMetadata](#h.ra67vzjmec2v)

[Group](#h.829b0i5yexun)

[Service Interface](#h.kgjocyhklu1b)

[GetUser](#h.1f3vxv6mfj2c)

[GetAllUsers](#h.8jz0zts2uhqs)

[UpsertUser](#h.dxc9109hkfhu)

[DropUser](#h.it10rl3v5b78)

[Available Roles](#h.orpyjhkf4za3)

[GetGroup](#h.m6gv1571p3x2)

[GetAllGroups](#h.h4uhsanhpfyb)

[UpsertGroup](#h.35x8b5tnome6)

[DropGroup](#h.bcaum5sclz6c)

[Collections Manager](#h.8zfr25d06mmc)

[Collection Exists](#h.jcy2l3znakl)

[Scope Exists](#h.c30miu3maaya)

[Get Scope](#h.y7nm7r1beg3i)

[Get All Scopes](#h.w9ysz23ucxr9)

[Create Collection](#h.v25764vsi0ze)

[Drop Collection](#h.2nrt7s3vbsx9)

[Create Scope](#h.80xchr7kse1x)

[Drop Scope](#h.bzbzwqo5ea52)

[Types](#h.hxsna6v0yga2)

[DesignDocument](#h.h075tca0i0r9)

[View](#h.ugcnslp1w79c)

[IQueryIndex Interface](#h.yipr3bi8gyda)

[AnalyticsDataset Interface](#h.t3sgseba5k26)

[AnalyticsIndex Interface](#h.cd1vwisd9cvl)

[BucketSettings](#h.bm3qgxw9689)

[CreateBucketSettings](#h.um6jv51ydhmv)

[SearchIndex](#h.w2u8bmxhvxn1)

[IUser Interface](#h.gc7j9dg0shou)

[ICollectionSpec Interface](#h.9moo4a588hua)

[IScopeSpec Interface](#h.zfjuduk2ojhv)

[References](#h.tatjn76gk22e)





# Summary

Defines the management APIs for SDK 3.0 that each SDK must implement.

# Motivation



# General Design

The management APIs are made up of several interfaces; Bucket Manager, User Manager, Search Index Manager, View Index Manager, Query Index Manager, Analytics Index Manager, and Collection Manager.



On the cluster interface:













IUserManager Users();



IBucketManager Buckets();



IQueryIndexManager QueryIndexes();



IAnalyticsIndexManager AnalyticsIndexes();









ISearchIndexManager SearchIndexes();











On the bucket interface:













ICollectionManager Collections();









IViewIndexManager ViewIndexes();











# Service Not Configured

If a manager is requested for a service which is not configured on the cluster then a ServiceNotConfiguredException must be raised. This can be detected by looking in the cluster config object, if the endpoint for the service has no servers listed then it is not configured.

# Feature Not Found

Some features, such as groups, certain functions, and collections are not supported on all server versions. If an endpoint is requested against a server version that does not support that endpoint then the HTTP response will be a 404 containing the body “Not Found.”. If this is returned then the SDK must return  a FeatureNotFoundException to the user.

# View Index Manager

The View Index Manager interface contains the means for managing design documents used for views.



A design document belongs to either the “development” or “production” namespace. A development document has a name that starts with “dev_”. This is an implementation detail we’ve chosen to hide from consumers of this API. Document names presented to the user (returned from the “get” and “get all” methods, for example) always have the “dev_” prefix stripped.



Whenever the user passes a design document name to any method of this API, the user may refer to the document using the “dev_” prefix regardless of whether the user is referring to a development document or production document. The “dev_” prefix is always stripped from user input, and the actual document name passed to the server is determined by the “namespace” argument..



All methods (except publish) have a required “namespace” argument indicating whether the operation targets a development document or a production document. The type of this argument is an enum called DesignDocumentNamespace with values PRODUCTION and DEVELOPMENT.















Interface IViewIndexManager {



        DesignDocumentGetDesignDocument(string designDocName, DesignDocumentNamespace namespace, GetDesignDocumentOptions options);



        Iterable GetAllDesignDocuments(DesignDocumentNamespace namespace, GetAllDesignDocumentsOptions options);



        void UpsertDesignDocument(DesignDocument indexData, DesignDocumentNamespace namespace, UpsertDesignDocumentOptions options);



        void DropDesignDocument(string designDocName, DesignDocumentNamespace namespace, DropDesignDocumentOptions options);





        void PublishDesignDocument(string designDocName, PublishDesignDocumentOptions options);

}



### Methods

The following methods must be implemented:

#### GetDesignDocument

Fetches a design document from the server if it exists.

Signature











DesignDocumentGetDesignDocument(string designDocName, DesignDocumentNamespace namespace, [options])
SDK 3.0: Management APIs RFC

SDK-RFC #54

# Meta

*   Name: SDK Management APIs
*   RFC ID: 54
*   Start-Date: 2019-06-13
*   Owner: Charles Dixon
*   Current Status: draft







[Meta](#h.d61txvmb5lyx)

[Summary](#h.mupne99cshsu)

[Motivation](#h.fd9za96e3yg5)

[General Design](#h.k3nh685gh3zd)

[Service Not Configured](#h.fazo4li6zut4)

[Feature Not Found](#h.g3sb6exbieep)

[View Index Manager](#h.awf5c5g6sfub)

[Methods](#h.ltp1wzfhvkmd)

[GetDesignDocument](#h.9xwvwfmx35g1)

[GetAllDesignDocuments](#h.3cni9ir8h3pd)

[UpsertDesignDocument](#h.myqscrntq9od)

[DropDesignDocument](#h.fejq3trrq88k)

[PublishDesignDocument](#h.ytabqazgaibt)

[Query Index Manager](#h.vor45gro2p0)

[Methods](#h.vpcih9gceh5x)

[GetAllIndexes](#h.d9bt9ug8rdnk)

[CreateIndex](#h.25pbsjaw1r1t)

[CreatePrimaryIndex](#h.i3nri1f7emcm)

[DropIndex](#h.w5uphn3aj7a6)

[DropPrimaryIndex](#h.8fkshrim697h)

[WatchIndexes](#h.1jpy9kneh3ix)

[BuildDeferredIndexes](#h.2g1b86t843xh)

[Search Index Manager](#h.n72o3wjrgzcr)

[Methods](#h.7ypleagc8f02)

[GetIndex](#h.muduzks94csy)

[GetAllIndexes](#h.rm7ralf543po)

[UpsertIndex](#h.vojyv926dm9l)

[DropIndex](#h.7kr1kyi2cud7)

[GetIndexedDocumentsCount](#h.920wzxyyn8h0)

[PauseIngest](#h.shct6uc5c13v)

[ResumeIngest](#h.7b3my87vq187)

[AllowQuerying](#h.3b0hek5e6cru)

[DisallowQuerying](#h.burvg6qrwgc1)

[FreezePlan](#h.xed0g6nk80ih)

[UnfreezePlan](#h.o6413lybnsbd)

[AnalyzeDocument](#h.slz9r181j64v)

[Analytics Index Manager](#h.wey00euqxg6r)

[Create Dataverse](#h.84qyvlkb4ct)

[Drop Dataverse](#h.duuryzz83ji6)

[CreateDataset](#h.p8q696h2j1c2)

[DropDataset](#h.diqletr3ee8t)

[GetAllDatasets](#h.yeup6dx0ca2i)

[CreateIndex](#h.s2ix1a2i9750)

[DropIndex](#h.sp8nw6p5hw3y)

[GetAlIndexes](#h.gu1vgfz28b4q)

[Connect Link](#h.urr6tlame907)

[Disconnect Link](#h.f24cpp9is9ur)

[Get Pending Mutations](#h.43ulyhfxecvc)

[Bucket Manager](#h.a3jxd57mov7x)

[CreateBucket](#h.7azm73gy346n)

[UpdateBucket](#h.z6hp9xboxiox)

[DropBucket](#h.40gpci3gs7n9)

[GetBucket](#h.hsjjz8tpuhmp)

[GetAllBuckets](#h.rxc15d7zi17u)

[FlushBucket](#h.6lr2bzo2rpmg)

[User Manager](#h.e1pyjdt66quk)

[Role](#h.zhz0katumzwe)

[RoleAndDescription](#h.dvcwkh4ud3go)

[Origin](#h.n3o3qrb2hyz0)

[RoleAndOrigins](#h.qxxi2pw80si1)

[User](#h.3t1esyo2jmzd)

[UserAndMetadata](#h.ra67vzjmec2v)

[Group](#h.829b0i5yexun)

[Service Interface](#h.kgjocyhklu1b)

[GetUser](#h.1f3vxv6mfj2c)

[GetAllUsers](#h.8jz0zts2uhqs)

[UpsertUser](#h.dxc9109hkfhu)

[DropUser](#h.it10rl3v5b78)

[Available Roles](#h.orpyjhkf4za3)

[GetGroup](#h.m6gv1571p3x2)

[GetAllGroups](#h.h4uhsanhpfyb)

[UpsertGroup](#h.35x8b5tnome6)

[DropGroup](#h.bcaum5sclz6c)

[Collections Manager](#h.8zfr25d06mmc)

[Collection Exists](#h.jcy2l3znakl)

[Scope Exists](#h.c30miu3maaya)

[Get Scope](#h.y7nm7r1beg3i)

[Get All Scopes](#h.w9ysz23ucxr9)

[Create Collection](#h.v25764vsi0ze)

[Drop Collection](#h.2nrt7s3vbsx9)

[Create Scope](#h.80xchr7kse1x)

[Drop Scope](#h.bzbzwqo5ea52)

[Types](#h.hxsna6v0yga2)

[DesignDocument](#h.h075tca0i0r9)

[View](#h.ugcnslp1w79c)

[IQueryIndex Interface](#h.yipr3bi8gyda)

[AnalyticsDataset Interface](#h.t3sgseba5k26)

[AnalyticsIndex Interface](#h.cd1vwisd9cvl)

[BucketSettings](#h.bm3qgxw9689)

[CreateBucketSettings](#h.um6jv51ydhmv)

[SearchIndex](#h.w2u8bmxhvxn1)

[IUser Interface](#h.gc7j9dg0shou)

[ICollectionSpec Interface](#h.9moo4a588hua)

[IScopeSpec Interface](#h.zfjuduk2ojhv)

[References](#h.tatjn76gk22e)





# Summary

Defines the management APIs for SDK 3.0 that each SDK must implement.

# Motivation



# General Design

The management APIs are made up of several interfaces; Bucket Manager, User Manager, Search Index Manager, View Index Manager, Query Index Manager, Analytics Index Manager, and Collection Manager.



On the cluster interface:













IUserManager Users();



IBucketManager Buckets();



IQueryIndexManager QueryIndexes();



IAnalyticsIndexManager AnalyticsIndexes();









ISearchIndexManager SearchIndexes();











On the bucket interface:













ICollectionManager Collections();









IViewIndexManager ViewIndexes();











# Service Not Configured

If a manager is requested for a service which is not configured on the cluster then a ServiceNotConfiguredException must be raised. This can be detected by looking in the cluster config object, if the endpoint for the service has no servers listed then it is not configured.

# Feature Not Found

Some features, such as groups, certain functions, and collections are not supported on all server versions. If an endpoint is requested against a server version that does not support that endpoint then the HTTP response will be a 404 containing the body “Not Found.”. If this is returned then the SDK must return  a FeatureNotFoundException to the user.

# View Index Manager

The View Index Manager interface contains the means for managing design documents used for views.



A design document belongs to either the “development” or “production” namespace. A development document has a name that starts with “dev_”. This is an implementation detail we’ve chosen to hide from consumers of this API. Document names presented to the user (returned from the “get” and “get all” methods, for example) always have the “dev_” prefix stripped.



Whenever the user passes a design document name to any method of this API, the user may refer to the document using the “dev_” prefix regardless of whether the user is referring to a development document or production document. The “dev_” prefix is always stripped from user input, and the actual document name passed to the server is determined by the “namespace” argument..



All methods (except publish) have a required “namespace” argument indicating whether the operation targets a development document or a production document. The type of this argument is an enum called DesignDocumentNamespace with values PRODUCTION and DEVELOPMENT.















Interface IViewIndexManager {



        DesignDocumentGetDesignDocument(string designDocName, DesignDocumentNamespace namespace, GetDesignDocumentOptions options);



        Iterable GetAllDesignDocuments(DesignDocumentNamespace namespace, GetAllDesignDocumentsOptions options);



        void UpsertDesignDocument(DesignDocument indexData, DesignDocumentNamespace namespace, UpsertDesignDocumentOptions options);



        void DropDesignDocument(string designDocName, DesignDocumentNamespace namespace, DropDesignDocumentOptions options);





        void PublishDesignDocument(string designDocName, PublishDesignDocumentOptions options);

}





















### Methods

The following methods must be implemented:

#### GetDesignDocument

Fetches a design document from the server if it exists.

Signature











DesignDocumentGetDesignDocument(string designDocName, DesignDocumentNamespace namespace, [options])









Parameters

*   Required:

*    designDocName: string - the name of the design document.
*   namespace: enum - PRODUCTION if the user is requesting a document from the production namespace, or DEVELOPMENT if from the development namespace.

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

An instance of DesignDocument.

Throws

*   DesignDocumentNotFoundException (http 404)
*   Any exceptions raised by the underlying platform

Uri

*   GET http://localhost:8092//_design/

Example response from server

{  

   "views":{  

      "test":{  

         "map":"function (doc, meta) {\n\t\t\t\t\t\t  emit(meta.id, null);\n\t\t\t\t\t\t}",

         "reduce":"_count"

      }

   }

}

#### GetAllDesignDocuments

Fetches all design documents from the server.

]

When processing the server response, the client must strip the “_design/” prefix from the document ID (as well as the “_dev” prefix if present). For example, a doc.meta.id value of “_design/foo” must be parsed as “foo”, and “_design/dev_bar” must be parsed as “bar”.

Signature











Iterable GetAllDesignDocuments(DesignDocumentNamespace namespace, [options])









Parameters

*   Required:

*   namespace (enum) - indicates whether the user wants to get production documents (PRODUCTION) or development documents (DEVELOPMENT).

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

An iterable of DesignDocument.

Throws

*   Any exceptions raised by the underlying platform

Uri

*   GET http://localhost:8091/pools/default/buckets//ddocs



Example response from server

{  

   "rows":[  

      {  

         "doc":{  

            "meta":{  

               "id":"_design/dev_test",

               "rev":"1-ae5e21ec"

            },

            "json":{  

               "views":{  

                  "test":{  

                     "map":"function (doc, meta) {\n\t\t\t\t\t\t  emit(meta.id, null);\n\t\t\t\t\t\t}",

                     "reduce":"_count"

                  }

               }

            }

         },

         "controllers":{  

            "compact":"/pools/default/buckets/default/ddocs/_design%2Fdev_test/controller/compactView",

            "setUpdateMinChanges":"/pools/default/buckets/default/ddocs/_design%2Fdev_test/controller/setUpdateMinChanges"

         }

      }

   ]

}

#### UpsertDesignDocument

Updates, or inserts, a design document.

Signature











void UpsertDesignDocument(DesignDocument designDocData, DesignDocumentNamespace namespace, [options])









Parameters

*   Required:

*   designDocData: DesignDocument - the data to use to create the design document
*   namespace (enum) - indicates whether the user wants to upsert the document to the production namespace (PRODUCTION) or development namespace (DEVELOPMENT).

*   Optional:

*   
*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   Any exceptions raised by the underlying platform

Uri

*   PUT http://localhost:8092//_design/

#### DropDesignDocument

Removes a design document.

Signature











void DropDesignDocument(string designDocName, DesignDocumentNamespace namespace,  [options])









Parameters

*   Required:

*   designDocName: string - the name of the design document.
*   namespace: enum - indicates whether the name refers to a production document (PRODUCTION) or a development document (DEVELOPMENT).

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   DesignDocumentNotFoundException (http 404)
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

Uri

*   DELETE http://localhost:8092//_design/

#### PublishDesignDocument

Publishes a design document. This method is equivalent to getting a document from the development namespace and upserting it to the production namespace.

Signature











void PublishDesignDocument(string designDocName, [options])









Parameters

*   Required:

*   designDocName: string - the name of the development design document.

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   DesignDocumentNotFoundException (http 404)
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

# Query Index Manager

The Query Index Manager interface contains the means for managing indexes used for queries.















public interface IQueryIndexManger{



        Iterable GetAllIndexes(string bucketName, GetAllQueryIndexOptions options);



void CreateIndex(string bucketName, string indexName, []string fields, CreateQueryIndexOptions options);



           void CreatePrimaryIndex(string bucketName, CreatePrimaryQueryIndexOptions options);



        void DropIndex(string bucketName, string indexName, DropQueryIndexOptions options);



            void DropPrimaryIndex(string bucketName, DropPrimaryQueryIndexOptions options);



void WatchIndexes(string bucketName, []string indexNames, timeout duration, WatchQueryIndexOptions options);

   

            void BuildDeferredIndexes(string bucketName, BuildQueryIndexOptions options);

}











### Methods

The following methods must be implemented:



#### GetAllIndexes

Fetches all indexes from the server.

Signature











Iterable GetAllIndexes(string bucketName, [options])









Parameters

*   Required:

*   BucketName: string - the name of the bucket.

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

N1QL

SELECT idx.* FROM system:indexes AS idx

    WHERE keyspace_id = "bucketName"

[[a]](#cmnt1)[[b]](#cmnt2)

    ORDER BY is_primary DESC, name ASC

Returns

An array of IQueryIndex.

Throws

*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

#### CreateIndex

Creates a new index.

Signature











void CreateIndex(string bucketName, string indexName, []string fields,  [options])









Parameters

*   Required:

*   BucketName: string - the name of the bucket.
*   IndexName: string - the name of the index.
*   fields: []string - the fields to create the index over.

*   Optional:

*   IgnoreIfExists (bool) - Don’t error/throw if the index already exists.
*   NumReplicas (int) - The number of replicas that this index should have. Uses the WITH keyword and num_replica.

*   CREATE INDEX indexNameON bucketName WITH { "num_replica": 2 }
*   [https://docs.couchbase.com/server/current/n1ql/n1ql-language-reference/createindex.html](https://www.google.com/url?q=https://docs.couchbase.com/server/current/n1ql/n1ql-language-reference/createindex.html&sa=D&ust=1569855744308000)

*   Deferred (bool) - Whether the index should be created as a deferred index.
*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   IndexAlreadyExistsException
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

#### CreatePrimaryIndex

Creates a new primary index.

Signature











void CreatePrimaryIndex(string bucketName, [options])









Parameters

*   Required:

*   BucketName: string - name of the bucket.

*   Optional:

*   IndexName: string - name of the index.
*   IgnoreIfExists (bool) - Don’t error/throw if the index already exists.
*   NumReplicas (int) - The number of replicas that this index should have. Uses the WITH keyword and num_replica.

*   CREATE INDEX indexNameON bucketName WITH { "num_replica": 2 }
*   [https://docs.couchbase.com/server/current/n1ql/n1ql-language-reference/createindex.html](https://www.google.com/url?q=https://docs.couchbase.com/server/current/n1ql/n1ql-language-reference/createindex.html&sa=D&ust=1569855744311000)

*   Deferred (bool) - Whether the index should be created as a deferred index.
*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   QueryIndexAlreadyExistsException
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

#### DropIndex

Drops an index.

Signature











void DropIndex(string bucketName, string indexName, [options])









Parameters

*   Required:

*   BucketName: string - name of the bucket.
*   IndexName: string - name of the index.

*   Optional:

*   IgnoreIfNotExists (bool) - Don’t error/throw if the index does not exist.
*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   QueryIndexNotFoundException
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

#### DropPrimaryIndex

Drops a primary index.

Signature











void DropPrimaryIndex(string bucketName, [options])









Parameters

*   Required:

*   BucketName: string - name of the bucket.

*   Optional:

*   IndexName: string - name of the index.
*   IgnoreIfNotExists (bool) - Don’t error/throw if the index does not exist.
*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   QueryIndexNotFoundException
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

#### WatchIndexes

Watch polls indexes until they are online.

Signature











void WatchIndexes(string bucketName, []string indexNames, timeout duration, [options])









Parameters

*   Required:

*   BucketName: string - name of the bucket.
*   IndexName: []string - name(s) of the index(es).
*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

*   Optional:

*   WatchPrimary (bool) - whether or not to watch the primary index.

Returns

Throws

*   QueryIndexNotFoundException
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

#### BuildDeferredIndexes[[c]](#cmnt3)[[d]](#cmnt4)

Build Deferred builds all indexes which are currently in deferred state.

Signature











void BuildDeferredIndexes(string bucketName, [options])









Parameters

*   Required:

*   BucketName: string - name of the bucket.

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   Any exceptions raised by the underlying platform
*   InvalidArgumentsException



# Search Index Manager

The Search Index Manager interface contains the means for managing indexes used for search. Search index definitions are purposefully left very dynamic as the index definitions on the server are complex. As such it is left to each SDK to implement its own dynamic type for this, JSONObject is used here to signify that. Stability level is uncommited?













public interface ISearchIndexManager{



        ISearchIndex GetIndex(string indexName, GetSearchIndexOptions options);



        Iterable GetAllIndexes(GetAllSearchIndexesOptions options);



         void UpsertIndex(ISearchIndex indexDefinition, UpsertSearchIndexOptions options);



        void DropIndex(string indexName, DropSearchIndexOptions options);



        int GetIndexedDocumentsCount(string indexName, GetIndexedSearchIndexOptions options);



        void PauseIngest(string indexName, PauseIngestSearchIndexOptions);



        void ResumeIngest(string indexName, ResumeIngestSearchIndexOptions);



        void AllowQuerying(string indexName, AllowQueryingSearchIndexOptions);



        void DisallowQuerying(string indexName, DisallowQueryingSearchIndexOptions);



        void FreezePlan(string indexName, FreezePlanSearchIndexOptions);



        void UnfreezePlan(string indexName, UnfreezePlanSearchIndexOptions);



           Iterable AnalyzeDocument(string indexName, JSONObject document, AnalyzeDocOptions options);

}











### Methods

The following methods must be implemented:

#### GetIndex

Fetches an index from the server if it exists.

Signature











ISearchIndex GetIndex(string indexName, [options])









Parameters

*   Required:

*    IndexName: string - name of the index.

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

An instance of ISearchIndex.

Throws

*   SearchIndexNotFoundException
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

Uri

*   GET http://localhost:8094/api/index/

#### GetAllIndexes

Fetches all indexes from the server.

Signature











Iterable GetAllIndexes([options])









Parameters

*   Required:
*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

An array of ISearchIndex.

Throws

*   Any exceptions raised by the underlying platform

Uri

*   GET http://localhost:8094/api/index

#### UpsertIndex

Creates, or updates, an index. .

Signature











void UpsertIndex(ISearchIndex indexDefinition, [options])









Parameters

*   Required:

*   indexDefinition: SearchIndex - the index definition

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   InvalidArgumentsException

*   If any of the following are empty:

*   Name
*   Type
*   SourceType

*   Any exceptions raised by the underlying platform

Uri

*   PUT [http://localhost:8094/api/index/](https://www.google.com/url?q=http://localhost:8094/api/index/&sa=D&ust=1569855744339000)

*   Should be sent with request header “cache-control” set to “no-cache”.

#### DropIndex

Drops an index.

Signature











void DropIndexstring indexName, [options])









Parameters

*   Required:

*   IndexName: string - name of the index.

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   SearchIndexNotFoundException
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

Uri

*   DELETE [http://localhost:8094/api/index/](https://www.google.com/url?q=http://localhost:8094/api/index/&sa=D&ust=1569855744343000)

#### GetIndexedDocumentsCount

Retrieves the number of documents that have been indexed for an index.

Signature











void GetIndexedDocumentsCount(string indexName, [options])









Parameters

*   Required:

*   IndexName: string - name of the index.

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   SearchIndexNotFoundException
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

Uri

*   GET [http://localhost:8094/api/index/](https://www.google.com/url?q=http://localhost:8094/api/index/&sa=D&ust=1569855744346000)/count

#### PauseIngest

Pauses updates and maintenance for an index.

Signature











void PauseIngest(string indexName, [options])









Parameters

*   Required:

*   IndexName: string - name of the index.

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   SearchIndexNotFoundException
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

Uri

*   POST /api/index/{indexName}/ingestControl/pause

#### ResumeIngest

Resumes updates and maintenance for an index.

Signature











void ResumeIngest(string indexName, [options])









Parameters

*   Required:

*   IndexName: string - name of the index.

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   SearchIndexNotFoundException
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

Uri

*   POST /api/index/{indexName}/ingestControl/resume

#### AllowQuerying

Allows querying against an index.

Signature











void AllowQuerying(string indexName, [options])









Parameters

*   Required:

*   IndexName: string - name of the index.

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   SearchIndexNotFoundException
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

Uri

*   POST /api/index/{indexName}/queryControl/allow

#### DisallowQuerying

Disallows querying against an index.

Signature











void DisallowQuerying(string indexName, [options])









Parameters

*   Required:

*   IndexName: string - name of the index.

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   SearchIndexNotFoundException
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

Uri

*   POST /api/index/{indexName}/queryControl/disallow

#### FreezePlan

Freeze the assignment of index partitions to nodes.

Signature











void FreezePlan(string indexName, [options])









Parameters

*   Required:

*   IndexName: string - name of the index.

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   SearchIndexNotFoundException
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

Uri

*   POST /api/index/{indexName}/planFreezeControl/freeze

#### UnfreezePlan

Unfreeze the assignment of index partitions to nodes.

Signature











void UnfreezePlan(string indexName, [options])









Parameters

*   Required:

*   IndexName: string - name of the index.

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   SearchIndexNotFoundException
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

Uri

*   POST /api/index/{indexName}/planFreezeControl/unfreeze



#### AnalyzeDocument

Allows users to see how a document is analyzed against a specific index.

Signature











Iterable AnalyzeDocument(string indexName, JSONObject document, [options])









Parameters

*   Required:

*   IndexName: string - name of the index.
*   Document: JSONObject - the document to be analyzed.

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

An iterable of JSONObject. The response from the server returns an object containing two top level keys: status and analyzed. The SDK must return the value containing within the analyze key.

Throws

*   SearchIndexNotFoundException
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

Uri

*   POST /api/index/{indexName}/analyzeDoc

*   As of build mad hatter 3839

# Analytics Index Manager

Stability level is not volatile.













public interface IAnalyticsIndexManager{



         void CreateDataverse(string dataverseName, CreateDataverseAnalyticsOptions options);



        void DropDataverse(string dataverseName, DropDataverseAnalyticsOptions options);



         void CreateDataset(string bucketName, string datasetName, CreateDatasetAnalyticsOptions options);



        void DropDataset(string datasetName, DropDatasetAnalyticsOptions options);



  Iterable GetAllDatasets(GetAllDatasetAnalyticsOptions options);



         void CreateIndex(string indexName, map[string]string fields, CreateIndexAnalyticsOptions options);



         void DropIndex(string datasetName, string indexName, DropIndexAnalyticsOptions options);



            Iterable GetAllIndexes(GetAllIndexesAnalyticsOptions options);



         void ConnectLink(string linkName, ConnectLinkAnalyticsOptions options);



         void DisconnectLink(string linkName, DisconnectLinkAnalyticsOptions options);



 map[string]int GetPendingMutations(GetPendingMutationsAnalyticsOptions options);

}





















#### Create Dataverse

Creates a new dataverse.

Signature











void CreateDataverse(string dataverseName, [options])









Parameters

*   Required:

*   dataverseName: string - name of the dataverse.

*   Optional:

*   IgnoreIfExists (bool) - ignore if the dataset already exists (send “IF NOT EXISTS” as part of the dataset creation query, e.g. CREATE DATAVERSE IF NOT EXISTS test ON default). Default to false.
*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   DataverseAlreadyExistsException
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

#### Drop Dataverse

Drops a dataverse.

Signature











void DropDataverse(string dataverseName,  [options])









Parameters

*   Required:

*   dataverseName: string - name of the dataverse.

*   Optional:

*   IgnoreIfNotExists (bool) - ignore if the dataset doesn’t exists (send “IF EXISTS” as part of the dataset creation query, e.g. DROP DATAVERSE IF EXISTS test).
*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   DataverseNotFoundException
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

#### CreateDataset

Creates a new dataset.

Signature











void CreateDataset(string datasetName, string bucketName, [options])









Parameters

*   Required:

*   datasetName: string - name of the dataset.
*   bucketName: string - name of the bucket.

*   Optional:

*   IgnoreIfExists (bool) - ignore if the dataset already exists (send “IF NOT EXISTS” as part of the dataset creation query, e.g. CREATE DATASET IF NOT EXISTS test ON default).c
*   Condition (string) - Where clause to use for creating dataset.
*   DataverseName (string) - The name of the dataverse to use, default to none. If set then will be used as CREATE DATASET dataverseName.datasetName. If not set then will be CREATE DATASET datasetName.
*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   DatasetAlreadyExistsException
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

#### DropDataset

Drops a dataset.

Signature











void DropDataset(string datasetName,  [options])









Parameters

*   Required:

*   datasetName: string - name of the dataset.

*   Optional:

*   IgnoreIfNotExists (bool) - ignore if the dataset doesn’t exists (send “IF EXISTS” as part of the dataset creation query, e.g. DROP DATASET IF EXISTS test).
*   DataverseName (string) - The name of the dataverse to use, default to none. If set then will be used as DROP DATASET dataverseName.datasetName. If not set then will be DROP DATASET datasetName.
*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   DatasetNotFoundException
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

#### GetAllDatasets

Gets all datasets (SELECT d.* FROM Metadata.`Dataset` d WHERE d.DataverseName  "Metadata").

Signature











Iterable GetAllDatasets([options])









Parameters

*   Required:
*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   Any exceptions raised by the underlying platform

#### CreateIndex

Creates a new index.

Signature











void CreateIndex(string indexName, string datasetName, map[string]string fields,  [options])









Parameters

*   Required:

*   DatasetName: string - name of the dataset.
*   IndexName: string - name of the index.
*   fields: map[string]string - the fields to create the index over. This is a map of the name of the field to the type of the field.

*   Optional:

*   IgnoreIfExists (bool) - don’t error/throw if the index already exists. (send “IF NOT EXISTS” as part of the dataset creation query, e.g. CREATE INDEX test IF NOT EXISTS ON default) (Note: IF NOT EXISTS is not is in the same place as it is in CREATE DATASET)
*   DataverseName (string) - The name of the dataverse to use, default to none. If set then will be used as CREATE INDEX dataverseName.datasetName.indexName. If not set then will be CREATE INDEX datasetName.indexName.
*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.Returns
*   

*   AnalyticsIndexAlreadyExistsException
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

#### DropIndex

Drops an index.

Throws

Signature











void DropIndex(string indexName, string datasetName, [options])









Parameters

*   Required:

*   IndexName: string - name of the index.

*   Optional:

*   IgnoreIfNotExists (bool) - Don’t error/throw if the index does not exist.
*   DataverseName (string) - The name of the dataverse to use, default to none. If set then will be used as DROP INDEX dataverseName.datasetName.indexName. If not set then will be DROP INDEX datasetName.indexName.
*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   AnalyticsIndexNotFoundException
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

#### GetAlIndexes

Gets all indexes (SELECT d.* FROM Metadata.`Index` d WHERE d.DataverseName  “Metadata”).

Signature











Iterable GetAllIndexes([options])









Parameters

*   Required:
*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   Any exceptions raised by the underlying platform

#### Connect Link

Connects a link.

Signature











void ConnectLink([options])









Parameters

*   Required:
*   Optional[[e]](#cmnt5)[[f]](#cmnt6)[[g]](#cmnt7)[[h]](#cmnt8):

*   linkName: string - name of the link. Default to “Local”.
*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   AnalyticsLinkNotFoundException
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

#### Disconnect Link

Disconnects a link.

Signature











void DisconnectLink([options])









Parameters

*   Required:
*   Optional:

*   linkName: string - name of the link. Default to “Local”.
*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   AnalyticsLinkNotFoundException
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

#### Get Pending Mutations

Gets the pending mutations for all datasets. This is returned in the form of dataverse.dataset: mutations. E.g.:

{

    "Default.travel": 20688,

    "Default.thing": 0,

    "Default.default": 0,

    "Notdefault.default": 0

}

Note that if a link is disconnected then it will return no results. If all links are disconnected then an empty object is returned.

Signature











map[string]int GetPendingMutations( [options])









Parameters

*   Required:
*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   Any exceptions raised by the underlying platform

Uri

*   GET http://localhost:8095/analytics/node/agg/stats/remaining

# Bucket Manager













public interface IBucketManager{



        void CreateBucket(CreateBucketSettings settings, CreateBucketOptions options);



        void UpdateBucket(BucketSettings settings, UpdateBucketOptions options);



        void DropBucket(string bucketName, DropBucketOptions options);



        BucketSettings GetBucket(string bucketName, GetBucketOptions options);



        Iterable GetAllBuckets(GetAllBucketOptions options);



            void FlushBucket(string bucketName, FlushBucketOptions options); // using the ns_server REST interface

}











#### CreateBucket

Creates a new bucket.

Signature











void CreateBucket(CreateBucketSettings settings, [options])









Parameters

*   Required: BucketSettings - settings for the bucket.
*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   BucketAlreadyExistsException(http 400 and content contains "Bucket with given name already exists")
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

Uri

*   POST [http://localhost:8092/pools/default/buckets](https://www.google.com/url?q=http://localhost:8092/pools/default/buckets&sa=D&ust=1569855744407000)

#### UpdateBucket

Updatesa bucket. In the docstring the SDK must include a section about how every setting must be set to what the user wants it to be after the update. Any settings that are not set to their desired values may be reverted to default values by the server.

Signature











void UpdateBucket(BucketSettings settings, [options])









Parameters

*   Required: BucketSettings - settings for the bucket.
*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   InvalidArgumentsException
*   BucketDoesNotExistException
*   Any exceptions raised by the underlying platform

Uri

*   POST http://localhost:8092/pools/default/buckets/

#### DropBucket

Removes a bucket.

Signature











void DropBucket(string bucketName, [options])









Parameters

*   Required:

*   bucketName: string - the name of the bucket.

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   BucketNotFoundException
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

Uri

*   DELETE http://localhost:8092/pools/default/buckets/

#### GetBucket

Gets a bucket’s settings.

Signature











BucketSettings GetBucket(bucketName string, [options])









Parameters

*   Required:

*   bucketName: string - the name of the bucket.

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

BucketSettings, settings for the bucket. Note: the ram quota returned is in bytes, not mb so requires x  / 1024 twice. Also Note: FlushEnabled is not a setting returned by the server, if flush is enabled then the doFlush endpoint will be listed and should be used to populate the field.

Throws

*   BucketNotFoundException
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

Uri

*   GET http://localhost:8092/pools/default/buckets/

#### GetAllBuckets

Gets all bucket settings. Note: the ram quota returned is in bytes, not mb so requires x  / 1024 twice.

Signature











Iterable GetAllBuckets([options])









Parameters

*   Required:
*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

An iterable of settings for each bucket.

Throws

*   Any exceptions raised by the underlying platform

Uri

*   GET http://localhost:8092/pools/default/buckets

#### FlushBucket

Flushes a bucket (uses the ns_server REST interface).

Signature











void FlushBucket(string bucketName, [options])









Parameters

*   Required:

*   bucketName: string - the name of the bucket.

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   BucketNotFoundException
*   InvalidArgumentsException
*   FlushDisabledException
*   Any exceptions raised by the underlying platform

Uri

*   POST http://localhost:8092//pools/default/buckets//controller/doFlush

# User Manager

Programmatic access to the user management REST API:

https://docs.couchbase.com/server/current/rest-api/rbac.html



Unless otherwise indicated, all objects SHOULD be immutable.

### Role

A role identifies a specific permission. CAVEAT: The properties of a role are likely to change with the introduction of collection-level permissions. Until then, here’s what the accessor methods look like:



*   String name()
*   Optional bucket()

### RoleAndDescription

Associates a role with its name and description. This is additional information only present in the “list available roles” response.



*   Role role()
*   String displayName()
*   String description()

### Origin

Indicates why the user has a specific role. If the type is “user” it means the role is assigned directly to the user. If the type is “group” it means the role is inherited from the group identified by the “name” field.



*   String type()
*   Optional name()

### RoleAndOrigins

Associates a role with its origins. This is how roles are returned by the “get user” and “get all users” responses.



*   Role role()
*   List origins()

### User

Mutable. Models the user properties that may be updated via this API. All properties of the User class MUST have associated setters except for “username” which is fixed when the object is created.



*   String username()
*   String displayName()
*   Set groups() - (names of the groups)
*   Set roles() - only roles assigned directly to the user (not inherited from groups)
*   String password() - From the user’s perspective the password property is “write-only”. The accessor SHOULD be hidden from the user and be visible only to the manager implementation.

### UserAndMetadata

Models the “get user” / “get all users” response. Associates the mutable properties of a user with derived properties such as the effective roles inherited from groups.



*   AuthDomain domain() - AuthDomain is an enumeration with values “local” and “external”. It MAY alternatively be represented as String.
*   User user() - returns a new mutable User object each time this method is called. Modifying the fields of the returned User MUST have no effect on the UserAndMetadata object it came from.
*   Set effectiveRoles() - all roles, regardless of origin.
*   List effectiveRolesAndOrigins() - same as effectiveRoles, but with origin information included.
*   Optional passwordChanged()
*   Set externalGroups()

### Group

Mutable. Defines a set of roles that may be inherited by users. All properties of the Group class MUST have associated setters except for “name” which is fixed when the object is created.



*   String name()
*   String description()
*   Set roles() - [Role](#h.zhz0katumzwe) as defined in the User Manager section
*   Optional ldapGroupReference()

## Service Interface













public interface IUserManager{



        UserAndMetadata GetUser(string username, GetUserOptions options);



        Iterable GetAllUsers(GetAllUsersOptions options);



            void UpsertUser(User user, UpsertUserOptions options);



        void DropUser(string userName, DropUserOptions options);



        Iterable AvailableRoles(AvailableRolesOptions options);



        Group GetGroup(string groupName, GetGroupOptions options);



        Iterable GetAllGroups(GetAllGroupsOptions options);



            void UpsertGroup(Group group, UpsertGroupOptions options);



        void DropGroup(string groupName, DropGroupOptions options);

}









#### 

#### GetUser

Gets a user.

Signature











UserAndMetadata GetUser(string username, [options])









Parameters

*   Required:

*   username: string - ID of the user.

*   Optional:

*   domainName: string - name of the user domain. Defaults to local.        
*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

An instance of UserAndMetadata.

Throws

*   UserNotFoundException
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform



Implementation Notes



When parsing the “get” and “getAll” responses, take care to distinguish between roles assigned directly to the user (role origin with type=”user”) and roles inherited from groups (role origin with type=”group” and name=).



If the server response does not include an “origins” field for a role, then it was generated by a server version prior to 6.5 and the SDK MUST treat the role as if it had a single origin of type=”user”.



#### GetAllUsers

Gets all users.

Signature











Iterable GetAllUsers([options])









Parameters

*   Required:
*   Optional:

*   domainName: string - name of the user domain. Defaults to local.
*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

An iterable collection of UserAndMetadata.

Throws

*   Any exceptions raised by the underlying platform

#### UpsertUser

Creates or updates a user.

Signature











void UpsertUser(User user, [options])









Parameters

*   Required:

*   user: User - the new version of the user.

*   Optional:

*   DomainName: string - name of the user domain (local | external). Defaults to local.
*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform



Implementation Notes



When building the PUT request to send to the REST endpoint, implementations MUST omit the “password” property if it is not present in the given User domain object (so that the password is only changed if the calling code provided a new password).



For backwards compatibility with Couchbase Server 6.0 and earlier, the “groups” parameter MUST be omitted if the group list is empty. Couchbase Server 6.5 treats the absent parameter the same as an explicit parameter with no value (removes any existing group associations, which is what we want in this case).



#### DropUser

Removes a user.

Signature











void DropUser(string username, [options])









Parameters

*   Required:

*   username: string - ID of the user.

*   Optional:

*   DomainName: string - name of the user domain. Defaults to local.
*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   UserNotFoundException
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform



#### Available Roles

Returns the roles supported by the server.

Signature











Iterable GetRoles([options])









Parameters

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

An iterable collection of RoleAndDescription.

Throws

*   Any exceptions raised by the underlying platform



#### GetGroup

Gets a group.



REST Endpoint: GET /settings/rbac/groups/

Signature











Group GetGroup(string groupName, [options])









Parameters

*   Required:

*   groupName: string - name of the group to get.

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

An instance of Group.

Throws

*   GroupNotFoundException
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform



#### GetAllGroups

Gets all groups.



REST Endpoint: GET /settings/rbac/groups

Signature











Iterable GetAllGroups([options])









Parameters

*   Required:
*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

An iterable collection of Group.

Throws

*   Any exceptions raised by the underlying platform

#### UpsertGroup

Creates or updates a group.



REST Endpoint: PUT /settings/rbac/groups/

This endpoint accepts application/x-www-form-urlencoded and requires the data be sent as form data. The name/id should not be included in the form data. Roles should be a comma separated list of strings. If, only if, the role contains a bucket name then the rolename should be suffixed with[] e.g. bucket_full_access[default],security_admin.

Signature











void UpsertGroup(Group group, [options])









Parameters

*   Required:

*   group: Group - the new version of the group.

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform



#### DropGroup

Removes a group.



REST Endpoint: DELETE /settings/rbac/groups/

Signature











void DropGroup(string groupName, [options])









Parameters

*   Required:

*   groupName: string - name of the group.

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   GroupNotFoundException
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

# Collections Manager

Note: due to [https://issues.couchbase.com/browse/MB-35386](https://www.google.com/url?q=https://issues.couchbase.com/browse/MB-35386&sa=D&ust=1569855744460000) CollectionExists, ScopeExists, and GetScope must support both forms of the manifest until SDK beta. That is, going forward:



{“uid”:“0",“scopes”:[{“name”:“_default”,“uid”:“0”,“collections”:[{“name”:“_default”,“uid”:“0"}]}]}



And for the sake of support for the server beta which did not have the fix in place:

{“uid”:0,“scopes”:{“_default”:{“uid”:0,“collections”:{“_default”:{“uid”:0}}}}}

It is recommended to try to parse the first form and fallback to the second so that it can be easily removed later.













public interface ICollectionManager{



            boolean CollectionExists(ICollectionSpec collection, CollectionExistsOptions options);



            boolean ScopeExists(string scopeName, ScopeExistsOptions options);



            IScopeSpec GetScope(string scopeName, GetScopeOptions options);



           Iterable GetAllScopes(GetAllScopesOptions options);



void CreateCollection(ICollectionSpec collection, CreateCollectionOptions options);



        void DropCollection(ICollectionSpec collection, DropCollectionOptions options);



         void CreateScope(IScopeSpec scope, CreateScopeOptions options);[[i]](#cmnt9)[[j]](#cmnt10)



        void DropScope(string scopeName, DropScopeOptions options);



        void FlushCollection[[k]](#cmnt11)[[l]](#cmnt12)[[m]](#cmnt13)[[n]](#cmnt14)(ICollectionSpec collection, FlushCollectionOptions options);

}





















#### Collection Exists

Checks for existence of a collection. This will fetch a manifest and then interrogate it to check that the scope name exists and then that the collection name exists within that scope.

Signature











boolean CollectionExists(ICollectionSpec collection,  [options])









Parameters

*   Required:

*   collection: ICollectionSpec - spec of the collection.

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   Any exceptions raised by the underlying platform
*   InvalidArgumentsException

Uri

*   GET /pools/default/buckets//collections

#### Scope Exists

Checks for existence of a scope. This will fetch a manifest and then interrogate it to check that the scope name exists.

Signature











boolean ScopeExists(String scopeName,  [options])









Parameters

*   Required:

*   scopeName: string - name of the scope.

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   Any exceptions raised by the underlying platform

Uri

*   GET /pools/default/buckets//collections

#### Get Scope

Gets a scope. This will fetch a manifest and then pull the scope out of it.

Signature











IScopeSpec GetScope(string scopeName,  [options])









Parameters

*   Required:

*   scopeName: string - name of the scope.

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   ScopeNotFoundException
*   Any exceptions raised by the underlying platform

Uri

*   GET /pools/default/buckets//collections

#### Get All Scopes

Gets all scopes. This will fetch a manifest and then pull the scopes out of it.

Signature











iterable GetAllScopes([options])









Parameters

*   Required:
*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   Any exceptions raised by the underlying platform

Uri

*   GET /pools/default/buckets//collections

#### Create Collection

Creates a new collection.

Signature











void CreateCollection(CollectionSpec collection, [options])









Parameters

*   Required:

*   collection: CollectionSpec - specification of the collection.

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   InvalidArgumentsException
*   CollectionAlreadyExistsException
*   ScopeNotFoundException
*   Any exceptions raised by the underlying platform

Uri

*   POST http://localhost:8091/pools/default/buckets//collections/ -d name=

#### Drop Collection

Removes a collection.

Signature











void DropCollection(ICollectionSpec collection, [options])









Parameters

*   Required:

*   collection: ICollectionSpec - namspece of the collection.

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   CollectionNotFoundException
*   Any exceptions raised by the underlying platform

Uri

*   DELETE http://localhost:8091/pools/default/buckets//collections//

#### Create Scope

Creates a new scope.

Signature











Void CreateScope(string scopeName, [options])









Parameters

*   Required:

*   scopeName: String - name of the scope.

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

Uri

*   POST [http://localhost:8091/pools/default/buckets/](https://www.google.com/url?q=http://localhost:8091/pools/default/buckets/&sa=D&ust=1569855744485000)/collections -d name=

#### Drop Scope

Removes a scope.

Signature











void DropScope(string scopeName, [options])









Parameters

*   Required:

*   collectionName: string - name of the collection.

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   ScopeNotFoundException
*   Any exceptions raised by the underlying platform

Uri

*   DELETE [http://localhost:8091/pools/default/buckets/](https://www.google.com/url?q=http://localhost:8091/pools/default/buckets/&sa=D&ust=1569855744488000)/collections/

# Types

#### DesignDocument

DesignDocument provides a means of mapping a design document into an object. It contains within it a map of View.













 type DesignDocument{



String Name();

                

        Map[String]IView Views();

}











#### View











 type View{



            String Map();

                

            String Reduce();

}









## 

#### IQueryIndex Interface

The IQueryIndex interface provides a means of mapping a query index into an object.













 interface IQueryIndex{



            String Name();

                

        Bool IsPrimary();



        IndexType Type();



        String State();



        String Keyspace();



Iterable IndexKey();



        Optional Condition();

}











#### AnalyticsDataset Interface

AnalyticsDataset provides a means of mapping dataset details into an object.













 interface AnalyticsDataset{



            String Name();

                

        String DataverseName();

                

        String LinkName();

                

        String BucketName();

}









#### AnalyticsIndex Interface

AnalyticsIndex provides a means of mapping analytics index details into an object.













 interface AnalyticsDataset{



            String Name();

                

        String DatasetName();



        String DataverseName();

                

        Bool IsPrimary();

}









#### 

#### BucketSettings

BucketSettings provides a means of mapping bucket settings into an object.

*   Name (string) - The name of the bucket.
*   FlushEnabled (bool) - Whether or not flush should be enabled on the bucket. Default to false.
*   RamQuotaMB (int) - Ram Quota in mb for the bucket. (rawRAM in the server payload)
*   NumReplicas (int) - The number of replicas for documents.
*   ReplicaIndexes (bool) - Whether replica indexes should be enabled for the bucket.
*   BucketType {couchbase (sent on wire as membase), memcached, ephemeral} - The type of the bucket. Default to couchbase.
*   EjectionMethod {fullEviction | valueOnly}. The eviction policy to use.
*   maxTTL (int) - Value for the maxTTL of new documents created without a ttl.
*   compressionMode {off | passive | active} - The compression mode to use.

#### CreateBucketSettings

CreateBucketSettings is a superset of BucketSettings providing one extra property:

*   ConflictResolutionType {Timestamp (sent as lww) | SequenceNumber (sent as seqno)}. The conflict resolution type to use.

The reasoning for this is that on Update ConflictResolutionType cannot be present in the JSON payload at all.



#### UpsertIndeSearchIndex

SearchIndex provides a means to map search indexes into object. The Params, SourceParams, and PlanParams fields are left to the SDK to decide what is idiomatic (e.g. JSONObject), the definitions of these fields is purposefully vague.











type SearchIndex struct {

        // UUID is required for updates. It provides a means of ensuring consistency, the UUID must match the UUID value

        // for the index on the server.

        UUID string `json:"uuid"`



        Name string `json:"name"`



        // SourceName is the name of the source of the data for the index e.g. bucket name.

        SourceName string `json:"sourceName,omitempty"`



        // Type is the type of index, e.g. fulltext-index or fulltext-alias.

        Type string `json:"type"`



        // IndexParams are index properties such as store type and mappings.

        Params map[string]interface{} `json:"params"`



        // SourceUUID is the UUID of the data source, this can be used to more tightly tie the index to a source.

        SourceUUID string `json:"sourceUUID,omitempty"`



        // SourceParams are extra parameters to be defined. These are usually things like advanced connection and tuning

        // parameters.

        SourceParams map[string]interface{} `json:"sourceParams,omitempty"`



        // SourceType is the type of the data source, e.g. couchbase or nil depending on the Type field.

        SourceType string `json:"sourceType"`



        // PlanParams are plan properties such as number of replicas and number of partitions.

        PlanParams map[string]interface{} `json:"planParams,omitempty"`

}













#### IUser Interface

The IUser interface provides a means of mapping user settings into an object.













 Interface IUser{



            String ID();



            String Name();

        

            Iterable Roles();

}











#### ICollectionSpec Interface













 Interface ICollectionSpec{



            String Name();

        

            String ScopeName();

}











#### IScopeSpec Interface













 Interface IScopeSpec{



            String Name();

        

            Iterable Collections();

}

















# References

*   Query index management

*   [https://github.com/couchbaselabs/sdk-rfcs/blob/master/rfc/0003-indexmanagement.md](https://www.google.com/url?q=https://github.com/couchbaselabs/sdk-rfcs/blob/master/rfc/0003-indexmanagement.md&sa=D&ust=1569855744515000)
*   [https://docs.couchbase.com/server/current/n1ql/n1ql-language-reference/](https://www.google.com/url?q=https://docs.couchbase.com/server/current/n1ql/n1ql-language-reference/&sa=D&ust=1569855744516000)

*   Search index management

*   [https://docs.google.com/document/d/1C4yfTj5u6ahRgk3ZIL_AkwPMeu9-hHY_lZcsDNeIP74](https://www.google.com/url?q=https://docs.google.com/document/d/1C4yfTj5u6ahRgk3ZIL_AkwPMeu9-hHY_lZcsDNeIP74&sa=D&ust=1569855744517000)
*   [https://docs.couchbase.com/server/6.0/rest-api/rest-fts-indexing.html](https://www.google.com/url?q=https://docs.couchbase.com/server/6.0/rest-api/rest-fts-indexing.html&sa=D&ust=1569855744517000)
*   [http://labs.couchbase.com/cbft/dev-guide/index-definitions/](https://www.google.com/url?q=http://labs.couchbase.com/cbft/dev-guide/index-definitions/&sa=D&ust=1569855744518000)

*   Outdated but contains some useful definitions for fields.

*   User Management

*   [https://github.com/couchbaselabs/sdk-rfcs/blob/master/rfc/0022-usermgmt.md](https://www.google.com/url?q=https://github.com/couchbaselabs/sdk-rfcs/blob/master/rfc/0022-usermgmt.md&sa=D&ust=1569855744518000)

*   Bucket Management

*   [https://docs.couchbase.com/server/current/rest-api/rest-bucket-intro.html](https://www.google.com/url?q=https://docs.couchbase.com/server/current/rest-api/rest-bucket-intro.html&sa=D&ust=1569855744519000)

*   Collection Management

*   [https://github.com/couchbase/ns_server/commit/4c1a9ea20fbdb148f68ec2ad7be9eed4c071bf9e](https://www.google.com/url?q=https://github.com/couchbase/ns_server/commit/4c1a9ea20fbdb148f68ec2ad7be9eed4c071bf9e&sa=D&ust=1569855744519000)
*   [https://docs.google.com/document/d/1X-v8GWQjplrMMaYwwWOzEuP4AUoDNIAvS39NmEjQ3_E/edit#heading=h.gprum229kohk](https://www.google.com/url?q=https://docs.google.com/document/d/1X-v8GWQjplrMMaYwwWOzEuP4AUoDNIAvS39NmEjQ3_E/edit%23heading%3Dh.gprum229kohk&sa=D&ust=1569855744520000)

*   Views REST API

*   [https://docs.couchbase.com/server/6.0/rest-api/rest-views-intro.html](https://www.google.com/url?q=https://docs.couchbase.com/server/6.0/rest-api/rest-views-intro.html&sa=D&ust=1569855744520000)

*   Groups and LDAP Groups

*   [https://docs.google.com/document/d/1wsjEmke80RW_sbW0ycS8yQl6rq5lzBbRWuelPZ1m9ZI/edit#](https://www.google.com/url?q=https://docs.google.com/document/d/1wsjEmke80RW_sbW0ycS8yQl6rq5lzBbRWuelPZ1m9ZI/edit%23&sa=D&ust=1569855744521000)
*   [https://docs.google.com/document/d/1cFZOz9n6ZKyq_thxCSteuLrZ0rJEh7AMT3MFbOHCchM/edit](https://www.google.com/url?q=https://docs.google.com/document/d/1cFZOz9n6ZKyq_thxCSteuLrZ0rJEh7AMT3MFbOHCchM/edit&sa=D&ust=1569855744521000)
*   [https://issues.couchbase.com/browse/MB-16035](https://www.google.com/url?q=https://issues.couchbase.com/browse/MB-16035&sa=D&ust=1569855744522000)

*   Analytics management

*   [https://docs.couchbase.com/server/current/analytics/5_ddl.html](https://www.google.com/url?q=https://docs.couchbase.com/server/current/analytics/5_ddl.html&sa=D&ust=1569855744522000)



# Changes

2019-09-30:

*   Remove dataverse name checking from all Analytics options blocks so that if the dataverse name is set we do not check if the dataset already contains it.
*   Added Condition to IQueryIndex.
*   Changed User AvailableRoles to GetRoles.
*   Change ConnectLink and DisconnectLink so that the name is optional, defaulting to Local.

2019-09-18:

*   Add FlushNotEnabledException to bucket Flush operation

2019-09-03:

*    Add numReplicas option to QueryIndexManager CreatePrimaryIndex



[[a]](#cmnt_ref1)Java path-finding impl also has AND `using` = \"gsi\"





[[b]](#cmnt_ref2)I believe this is from back in the very first versions of N1QL, where it was required to be specified.  I don't think we need to bring this behaviour forward.





[[c]](#cmnt_ref3)Java impl does this by getting all indexes and doing BUILD INDEX on any currently set to deferred.  Thought we weren't doing racey stuff like that in client as general rule?





[[d]](#cmnt_ref4)That wouldn't be racy, since your going to build exactly the indices that you find during the first call.  From a functional perspective, only indexes that were deferred at the time you called the method are being built, which I think makes sense.





[[e]](#cmnt_ref5)+charles.dixon@couchbase.com Should there be an optional `dataverse` parameter?





[[f]](#cmnt_ref6)And an optional `force` parameter?





[[g]](#cmnt_ref7)I guess we should make an escape style of parameter to future proof it.





[[h]](#cmnt_ref8)I don't think we need to have an escape hatch on something that only exists for ease of use.  Relatedly, why does CONNECT LINK even accept a dataverse name?





[[i]](#cmnt_ref9)There is still a question around this, I suggest that we just accept a string Name rather than a ScopeSpec and we don't create collections as a part of this. It isn't attempting to be an atomic operation that way.





[[j]](#cmnt_ref10)I would be in favour of this change.





[[k]](#cmnt_ref11)This is missing the function definition below like the others.





[[l]](#cmnt_ref12)There seems to be some confusion over what this command does. The collections design doc states that there will be a flush endpoint that we can call over REST. I don't believe that it's implemented by ns server yet though.





[[m]](#cmnt_ref13)https://docs.google.com/document/d/1X-v8GWQjplrMMaYwwWOzEuP4AUoDNIAvS39NmEjQ3_E/edit#heading=h.8c7d3zbqy7i is what I'm referring to





[[n]](#cmnt_ref14)Server-side flushing was not implemented, instead it was decided that flushing a collection could be achieved trivially by the SDK through the destruction and recreation of the collection.










Parameters

*   Required:

*    designDocName: string - the name of the design document.
*   namespace: enum - PRODUCTION if the user is requesting a document from the production namespace, or DEVELOPMENT if from the development namespace.

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

An instance of DesignDocument.

Throws

*   DesignDocumentNotFoundException (http 404)
*   Any exceptions raised by the underlying platform

Uri

*   GET http://localhost:8092//_design/

Example response from server

{  

   "views":{  

      "test":{  

         "map":"function (doc, meta) {\n\t\t\t\t\t\t  emit(meta.id, null);\n\t\t\t\t\t\t}",

         "reduce":"_count"

      }

   }

}

#### GetAllDesignDocuments

Fetches all design documents from the server.

]

When processing the server response, the client must strip the “_design/” prefix from the document ID (as well as the “_dev” prefix if present). For example, a doc.meta.id value of “_design/foo” must be parsed as “foo”, and “_design/dev_bar” must be parsed as “bar”.

Signature











Iterable GetAllDesignDocuments(DesignDocumentNamespace namespace, [options])









Parameters

*   Required:

*   namespace (enum) - indicates whether the user wants to get production documents (PRODUCTION) or development documents (DEVELOPMENT).

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

An iterable of DesignDocument.

Throws

*   Any exceptions raised by the underlying platform

Uri

*   GET http://localhost:8091/pools/default/buckets//ddocs



Example response from server

{  

   "rows":[  

      {  

         "doc":{  

            "meta":{  

               "id":"_design/dev_test",

               "rev":"1-ae5e21ec"

            },

            "json":{  

               "views":{  

                  "test":{  

                     "map":"function (doc, meta) {\n\t\t\t\t\t\t  emit(meta.id, null);\n\t\t\t\t\t\t}",

                     "reduce":"_count"

                  }

               }

            }

         },

         "controllers":{  

            "compact":"/pools/default/buckets/default/ddocs/_design%2Fdev_test/controller/compactView",

            "setUpdateMinChanges":"/pools/default/buckets/default/ddocs/_design%2Fdev_test/controller/setUpdateMinChanges"

         }

      }

   ]

}

#### UpsertDesignDocument

Updates, or inserts, a design document.

Signature











void UpsertDesignDocument(DesignDocument designDocData, DesignDocumentNamespace namespace, [options])









Parameters

*   Required:

*   designDocData: DesignDocument - the data to use to create the design document
*   namespace (enum) - indicates whether the user wants to upsert the document to the production namespace (PRODUCTION) or development namespace (DEVELOPMENT).

*   Optional:

*   
*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   Any exceptions raised by the underlying platform

Uri

*   PUT http://localhost:8092//_design/

#### DropDesignDocument

Removes a design document.

Signature











void DropDesignDocument(string designDocName, DesignDocumentNamespace namespace,  [options])









Parameters

*   Required:

*   designDocName: string - the name of the design document.
*   namespace: enum - indicates whether the name refers to a production document (PRODUCTION) or a development document (DEVELOPMENT).

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   DesignDocumentNotFoundException (http 404)
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

Uri

*   DELETE http://localhost:8092//_design/

#### PublishDesignDocument

Publishes a design document. This method is equivalent to getting a document from the development namespace and upserting it to the production namespace.

Signature











void PublishDesignDocument(string designDocName, [options])









Parameters

*   Required:

*   designDocName: string - the name of the development design document.

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   DesignDocumentNotFoundException (http 404)
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

# Query Index Manager

The Query Index Manager interface contains the means for managing indexes used for queries.















public interface IQueryIndexManger{



        Iterable GetAllIndexes(string bucketName, GetAllQueryIndexOptions options);



void CreateIndex(string bucketName, string indexName, []string fields, CreateQueryIndexOptions options);



           void CreatePrimaryIndex(string bucketName, CreatePrimaryQueryIndexOptions options);



        void DropIndex(string bucketName, string indexName, DropQueryIndexOptions options);



            void DropPrimaryIndex(string bucketName, DropPrimaryQueryIndexOptions options);



void WatchIndexes(string bucketName, []string indexNames, timeout duration, WatchQueryIndexOptions options);

   

            void BuildDeferredIndexes(string bucketName, BuildQueryIndexOptions options);

}











### Methods

The following methods must be implemented:



#### GetAllIndexes

Fetches all indexes from the server.

Signature











Iterable GetAllIndexes(string bucketName, [options])









Parameters

*   Required:

*   BucketName: string - the name of the bucket.

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

N1QL

SELECT idx.* FROM system:indexes AS idx

    WHERE keyspace_id = "bucketName"

[[a]](#cmnt1)[[b]](#cmnt2)

    ORDER BY is_primary DESC, name ASC

Returns

An array of IQueryIndex.

Throws

*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

#### CreateIndex

Creates a new index.

Signature











void CreateIndex(string bucketName, string indexName, []string fields,  [options])









Parameters

*   Required:

*   BucketName: string - the name of the bucket.
*   IndexName: string - the name of the index.
*   fields: []string - the fields to create the index over.

*   Optional:

*   IgnoreIfExists (bool) - Don’t error/throw if the index already exists.
*   NumReplicas (int) - The number of replicas that this index should have. Uses the WITH keyword and num_replica.

*   CREATE INDEX indexNameON bucketName WITH { "num_replica": 2 }
*   [https://docs.couchbase.com/server/current/n1ql/n1ql-language-reference/createindex.html](https://www.google.com/url?q=https://docs.couchbase.com/server/current/n1ql/n1ql-language-reference/createindex.html&sa=D&ust=1569855744308000)

*   Deferred (bool) - Whether the index should be created as a deferred index.
*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   IndexAlreadyExistsException
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

#### CreatePrimaryIndex

Creates a new primary index.

Signature











void CreatePrimaryIndex(string bucketName, [options])









Parameters

*   Required:

*   BucketName: string - name of the bucket.

*   Optional:

*   IndexName: string - name of the index.
*   IgnoreIfExists (bool) - Don’t error/throw if the index already exists.
*   NumReplicas (int) - The number of replicas that this index should have. Uses the WITH keyword and num_replica.

*   CREATE INDEX indexNameON bucketName WITH { "num_replica": 2 }
*   [https://docs.couchbase.com/server/current/n1ql/n1ql-language-reference/createindex.html](https://www.google.com/url?q=https://docs.couchbase.com/server/current/n1ql/n1ql-language-reference/createindex.html&sa=D&ust=1569855744311000)

*   Deferred (bool) - Whether the index should be created as a deferred index.
*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   QueryIndexAlreadyExistsException
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

#### DropIndex

Drops an index.

Signature











void DropIndex(string bucketName, string indexName, [options])









Parameters

*   Required:

*   BucketName: string - name of the bucket.
*   IndexName: string - name of the index.

*   Optional:

*   IgnoreIfNotExists (bool) - Don’t error/throw if the index does not exist.
*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   QueryIndexNotFoundException
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

#### DropPrimaryIndex

Drops a primary index.

Signature











void DropPrimaryIndex(string bucketName, [options])









Parameters

*   Required:

*   BucketName: string - name of the bucket.

*   Optional:

*   IndexName: string - name of the index.
*   IgnoreIfNotExists (bool) - Don’t error/throw if the index does not exist.
*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   QueryIndexNotFoundException
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

#### WatchIndexes

Watch polls indexes until they are online.

Signature











void WatchIndexes(string bucketName, []string indexNames, timeout duration, [options])









Parameters

*   Required:

*   BucketName: string - name of the bucket.
*   IndexName: []string - name(s) of the index(es).
*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

*   Optional:

*   WatchPrimary (bool) - whether or not to watch the primary index.

Returns

Throws

*   QueryIndexNotFoundException
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

#### BuildDeferredIndexes[[c]](#cmnt3)[[d]](#cmnt4)

Build Deferred builds all indexes which are currently in deferred state.

Signature











void BuildDeferredIndexes(string bucketName, [options])









Parameters

*   Required:

*   BucketName: string - name of the bucket.

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   Any exceptions raised by the underlying platform
*   InvalidArgumentsException



# Search Index Manager

The Search Index Manager interface contains the means for managing indexes used for search. Search index definitions are purposefully left very dynamic as the index definitions on the server are complex. As such it is left to each SDK to implement its own dynamic type for this, JSONObject is used here to signify that. Stability level is uncommited?













public interface ISearchIndexManager{



        ISearchIndex GetIndex(string indexName, GetSearchIndexOptions options);



        Iterable GetAllIndexes(GetAllSearchIndexesOptions options);



         void UpsertIndex(ISearchIndex indexDefinition, UpsertSearchIndexOptions options);



        void DropIndex(string indexName, DropSearchIndexOptions options);



        int GetIndexedDocumentsCount(string indexName, GetIndexedSearchIndexOptions options);



        void PauseIngest(string indexName, PauseIngestSearchIndexOptions);



        void ResumeIngest(string indexName, ResumeIngestSearchIndexOptions);



        void AllowQuerying(string indexName, AllowQueryingSearchIndexOptions);



        void DisallowQuerying(string indexName, DisallowQueryingSearchIndexOptions);



        void FreezePlan(string indexName, FreezePlanSearchIndexOptions);



        void UnfreezePlan(string indexName, UnfreezePlanSearchIndexOptions);



           Iterable AnalyzeDocument(string indexName, JSONObject document, AnalyzeDocOptions options);

}











### Methods

The following methods must be implemented:

#### GetIndex

Fetches an index from the server if it exists.

Signature











ISearchIndex GetIndex(string indexName, [options])









Parameters

*   Required:

*    IndexName: string - name of the index.

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

An instance of ISearchIndex.

Throws

*   SearchIndexNotFoundException
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

Uri

*   GET http://localhost:8094/api/index/

#### GetAllIndexes

Fetches all indexes from the server.

Signature











Iterable GetAllIndexes([options])









Parameters

*   Required:
*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

An array of ISearchIndex.

Throws

*   Any exceptions raised by the underlying platform

Uri

*   GET http://localhost:8094/api/index

#### UpsertIndex

Creates, or updates, an index. .

Signature











void UpsertIndex(ISearchIndex indexDefinition, [options])









Parameters

*   Required:

*   indexDefinition: SearchIndex - the index definition

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   InvalidArgumentsException

*   If any of the following are empty:

*   Name
*   Type
*   SourceType

*   Any exceptions raised by the underlying platform

Uri

*   PUT [http://localhost:8094/api/index/](https://www.google.com/url?q=http://localhost:8094/api/index/&sa=D&ust=1569855744339000)

*   Should be sent with request header “cache-control” set to “no-cache”.

#### DropIndex

Drops an index.

Signature











void DropIndexstring indexName, [options])









Parameters

*   Required:

*   IndexName: string - name of the index.

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   SearchIndexNotFoundException
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

Uri

*   DELETE [http://localhost:8094/api/index/](https://www.google.com/url?q=http://localhost:8094/api/index/&sa=D&ust=1569855744343000)

#### GetIndexedDocumentsCount

Retrieves the number of documents that have been indexed for an index.

Signature











void GetIndexedDocumentsCount(string indexName, [options])









Parameters

*   Required:

*   IndexName: string - name of the index.

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   SearchIndexNotFoundException
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

Uri

*   GET [http://localhost:8094/api/index/](https://www.google.com/url?q=http://localhost:8094/api/index/&sa=D&ust=1569855744346000)/count

#### PauseIngest

Pauses updates and maintenance for an index.

Signature











void PauseIngest(string indexName, [options])









Parameters

*   Required:

*   IndexName: string - name of the index.

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   SearchIndexNotFoundException
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

Uri

*   POST /api/index/{indexName}/ingestControl/pause

#### ResumeIngest

Resumes updates and maintenance for an index.

Signature











void ResumeIngest(string indexName, [options])









Parameters

*   Required:

*   IndexName: string - name of the index.

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   SearchIndexNotFoundException
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

Uri

*   POST /api/index/{indexName}/ingestControl/resume

#### AllowQuerying

Allows querying against an index.

Signature











void AllowQuerying(string indexName, [options])









Parameters

*   Required:

*   IndexName: string - name of the index.

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   SearchIndexNotFoundException
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

Uri

*   POST /api/index/{indexName}/queryControl/allow

#### DisallowQuerying

Disallows querying against an index.

Signature











void DisallowQuerying(string indexName, [options])









Parameters

*   Required:

*   IndexName: string - name of the index.

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   SearchIndexNotFoundException
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

Uri

*   POST /api/index/{indexName}/queryControl/disallow

#### FreezePlan

Freeze the assignment of index partitions to nodes.

Signature











void FreezePlan(string indexName, [options])









Parameters

*   Required:

*   IndexName: string - name of the index.

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   SearchIndexNotFoundException
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

Uri

*   POST /api/index/{indexName}/planFreezeControl/freeze

#### UnfreezePlan

Unfreeze the assignment of index partitions to nodes.

Signature











void UnfreezePlan(string indexName, [options])









Parameters

*   Required:

*   IndexName: string - name of the index.

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   SearchIndexNotFoundException
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

Uri

*   POST /api/index/{indexName}/planFreezeControl/unfreeze



#### AnalyzeDocument

Allows users to see how a document is analyzed against a specific index.

Signature











Iterable AnalyzeDocument(string indexName, JSONObject document, [options])









Parameters

*   Required:

*   IndexName: string - name of the index.
*   Document: JSONObject - the document to be analyzed.

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

An iterable of JSONObject. The response from the server returns an object containing two top level keys: status and analyzed. The SDK must return the value containing within the analyze key.

Throws

*   SearchIndexNotFoundException
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

Uri

*   POST /api/index/{indexName}/analyzeDoc

*   As of build mad hatter 3839

# Analytics Index Manager

Stability level is not volatile.













public interface IAnalyticsIndexManager{



         void CreateDataverse(string dataverseName, CreateDataverseAnalyticsOptions options);



        void DropDataverse(string dataverseName, DropDataverseAnalyticsOptions options);



         void CreateDataset(string bucketName, string datasetName, CreateDatasetAnalyticsOptions options);



        void DropDataset(string datasetName, DropDatasetAnalyticsOptions options);



  Iterable GetAllDatasets(GetAllDatasetAnalyticsOptions options);



         void CreateIndex(string indexName, map[string]string fields, CreateIndexAnalyticsOptions options);



         void DropIndex(string datasetName, string indexName, DropIndexAnalyticsOptions options);



            Iterable GetAllIndexes(GetAllIndexesAnalyticsOptions options);



         void ConnectLink(string linkName, ConnectLinkAnalyticsOptions options);



         void DisconnectLink(string linkName, DisconnectLinkAnalyticsOptions options);



 map[string]int GetPendingMutations(GetPendingMutationsAnalyticsOptions options);

}





















#### Create Dataverse

Creates a new dataverse.

Signature











void CreateDataverse(string dataverseName, [options])









Parameters

*   Required:

*   dataverseName: string - name of the dataverse.

*   Optional:

*   IgnoreIfExists (bool) - ignore if the dataset already exists (send “IF NOT EXISTS” as part of the dataset creation query, e.g. CREATE DATAVERSE IF NOT EXISTS test ON default). Default to false.
*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   DataverseAlreadyExistsException
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

#### Drop Dataverse

Drops a dataverse.

Signature











void DropDataverse(string dataverseName,  [options])









Parameters

*   Required:

*   dataverseName: string - name of the dataverse.

*   Optional:

*   IgnoreIfNotExists (bool) - ignore if the dataset doesn’t exists (send “IF EXISTS” as part of the dataset creation query, e.g. DROP DATAVERSE IF EXISTS test).
*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   DataverseNotFoundException
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

#### CreateDataset

Creates a new dataset.

Signature











void CreateDataset(string datasetName, string bucketName, [options])









Parameters

*   Required:

*   datasetName: string - name of the dataset.
*   bucketName: string - name of the bucket.

*   Optional:

*   IgnoreIfExists (bool) - ignore if the dataset already exists (send “IF NOT EXISTS” as part of the dataset creation query, e.g. CREATE DATASET IF NOT EXISTS test ON default).c
*   Condition (string) - Where clause to use for creating dataset.
*   DataverseName (string) - The name of the dataverse to use, default to none. If set then will be used as CREATE DATASET dataverseName.datasetName. If not set then will be CREATE DATASET datasetName.
*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   DatasetAlreadyExistsException
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

#### DropDataset

Drops a dataset.

Signature











void DropDataset(string datasetName,  [options])









Parameters

*   Required:

*   datasetName: string - name of the dataset.

*   Optional:

*   IgnoreIfNotExists (bool) - ignore if the dataset doesn’t exists (send “IF EXISTS” as part of the dataset creation query, e.g. DROP DATASET IF EXISTS test).
*   DataverseName (string) - The name of the dataverse to use, default to none. If set then will be used as DROP DATASET dataverseName.datasetName. If not set then will be DROP DATASET datasetName.
*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   DatasetNotFoundException
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

#### GetAllDatasets

Gets all datasets (SELECT d.* FROM Metadata.`Dataset` d WHERE d.DataverseName  "Metadata").

Signature











Iterable GetAllDatasets([options])









Parameters

*   Required:
*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   Any exceptions raised by the underlying platform

#### CreateIndex

Creates a new index.

Signature











void CreateIndex(string indexName, string datasetName, map[string]string fields,  [options])









Parameters

*   Required:

*   DatasetName: string - name of the dataset.
*   IndexName: string - name of the index.
*   fields: map[string]string - the fields to create the index over. This is a map of the name of the field to the type of the field.

*   Optional:

*   IgnoreIfExists (bool) - don’t error/throw if the index already exists. (send “IF NOT EXISTS” as part of the dataset creation query, e.g. CREATE INDEX test IF NOT EXISTS ON default) (Note: IF NOT EXISTS is not is in the same place as it is in CREATE DATASET)
*   DataverseName (string) - The name of the dataverse to use, default to none. If set then will be used as CREATE INDEX dataverseName.datasetName.indexName. If not set then will be CREATE INDEX datasetName.indexName.
*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.Returns
*   

*   AnalyticsIndexAlreadyExistsException
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

#### DropIndex

Drops an index.

Throws

Signature











void DropIndex(string indexName, string datasetName, [options])









Parameters

*   Required:

*   IndexName: string - name of the index.

*   Optional:

*   IgnoreIfNotExists (bool) - Don’t error/throw if the index does not exist.
*   DataverseName (string) - The name of the dataverse to use, default to none. If set then will be used as DROP INDEX dataverseName.datasetName.indexName. If not set then will be DROP INDEX datasetName.indexName.
*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   AnalyticsIndexNotFoundException
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

#### GetAlIndexes

Gets all indexes (SELECT d.* FROM Metadata.`Index` d WHERE d.DataverseName  “Metadata”).

Signature











Iterable GetAllIndexes([options])









Parameters

*   Required:
*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   Any exceptions raised by the underlying platform

#### Connect Link

Connects a link.

Signature











void ConnectLink([options])









Parameters

*   Required:
*   Optional[[e]](#cmnt5)[[f]](#cmnt6)[[g]](#cmnt7)[[h]](#cmnt8):

*   linkName: string - name of the link. Default to “Local”.
*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   AnalyticsLinkNotFoundException
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

#### Disconnect Link

Disconnects a link.

Signature











void DisconnectLink([options])









Parameters

*   Required:
*   Optional:

*   linkName: string - name of the link. Default to “Local”.
*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   AnalyticsLinkNotFoundException
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

#### Get Pending Mutations

Gets the pending mutations for all datasets. This is returned in the form of dataverse.dataset: mutations. E.g.:

{

    "Default.travel": 20688,

    "Default.thing": 0,

    "Default.default": 0,

    "Notdefault.default": 0

}

Note that if a link is disconnected then it will return no results. If all links are disconnected then an empty object is returned.

Signature











map[string]int GetPendingMutations( [options])









Parameters

*   Required:
*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   Any exceptions raised by the underlying platform

Uri

*   GET http://localhost:8095/analytics/node/agg/stats/remaining

# Bucket Manager













public interface IBucketManager{



        void CreateBucket(CreateBucketSettings settings, CreateBucketOptions options);



        void UpdateBucket(BucketSettings settings, UpdateBucketOptions options);



        void DropBucket(string bucketName, DropBucketOptions options);



        BucketSettings GetBucket(string bucketName, GetBucketOptions options);



        Iterable GetAllBuckets(GetAllBucketOptions options);



            void FlushBucket(string bucketName, FlushBucketOptions options); // using the ns_server REST interface

}











#### CreateBucket

Creates a new bucket.

Signature











void CreateBucket(CreateBucketSettings settings, [options])









Parameters

*   Required: BucketSettings - settings for the bucket.
*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   BucketAlreadyExistsException(http 400 and content contains "Bucket with given name already exists")
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

Uri

*   POST [http://localhost:8092/pools/default/buckets](https://www.google.com/url?q=http://localhost:8092/pools/default/buckets&sa=D&ust=1569855744407000)

#### UpdateBucket

Updatesa bucket. In the docstring the SDK must include a section about how every setting must be set to what the user wants it to be after the update. Any settings that are not set to their desired values may be reverted to default values by the server.

Signature











void UpdateBucket(BucketSettings settings, [options])









Parameters

*   Required: BucketSettings - settings for the bucket.
*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   InvalidArgumentsException
*   BucketDoesNotExistException
*   Any exceptions raised by the underlying platform

Uri

*   POST http://localhost:8092/pools/default/buckets/

#### DropBucket

Removes a bucket.

Signature











void DropBucket(string bucketName, [options])









Parameters

*   Required:

*   bucketName: string - the name of the bucket.

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   BucketNotFoundException
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

Uri

*   DELETE http://localhost:8092/pools/default/buckets/

#### GetBucket

Gets a bucket’s settings.

Signature











BucketSettings GetBucket(bucketName string, [options])









Parameters

*   Required:

*   bucketName: string - the name of the bucket.

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

BucketSettings, settings for the bucket. Note: the ram quota returned is in bytes, not mb so requires x  / 1024 twice. Also Note: FlushEnabled is not a setting returned by the server, if flush is enabled then the doFlush endpoint will be listed and should be used to populate the field.

Throws

*   BucketNotFoundException
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

Uri

*   GET http://localhost:8092/pools/default/buckets/

#### GetAllBuckets

Gets all bucket settings. Note: the ram quota returned is in bytes, not mb so requires x  / 1024 twice.

Signature











Iterable GetAllBuckets([options])









Parameters

*   Required:
*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

An iterable of settings for each bucket.

Throws

*   Any exceptions raised by the underlying platform

Uri

*   GET http://localhost:8092/pools/default/buckets

#### FlushBucket

Flushes a bucket (uses the ns_server REST interface).

Signature











void FlushBucket(string bucketName, [options])









Parameters

*   Required:

*   bucketName: string - the name of the bucket.

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   BucketNotFoundException
*   InvalidArgumentsException
*   FlushDisabledException
*   Any exceptions raised by the underlying platform

Uri

*   POST http://localhost:8092//pools/default/buckets//controller/doFlush

# User Manager

Programmatic access to the user management REST API:

https://docs.couchbase.com/server/current/rest-api/rbac.html



Unless otherwise indicated, all objects SHOULD be immutable.

### Role

A role identifies a specific permission. CAVEAT: The properties of a role are likely to change with the introduction of collection-level permissions. Until then, here’s what the accessor methods look like:



*   String name()
*   Optional bucket()

### RoleAndDescription

Associates a role with its name and description. This is additional information only present in the “list available roles” response.



*   Role role()
*   String displayName()
*   String description()

### Origin

Indicates why the user has a specific role. If the type is “user” it means the role is assigned directly to the user. If the type is “group” it means the role is inherited from the group identified by the “name” field.



*   String type()
*   Optional name()

### RoleAndOrigins

Associates a role with its origins. This is how roles are returned by the “get user” and “get all users” responses.



*   Role role()
*   List origins()

### User

Mutable. Models the user properties that may be updated via this API. All properties of the User class MUST have associated setters except for “username” which is fixed when the object is created.



*   String username()
*   String displayName()
*   Set groups() - (names of the groups)
*   Set roles() - only roles assigned directly to the user (not inherited from groups)
*   String password() - From the user’s perspective the password property is “write-only”. The accessor SHOULD be hidden from the user and be visible only to the manager implementation.

### UserAndMetadata

Models the “get user” / “get all users” response. Associates the mutable properties of a user with derived properties such as the effective roles inherited from groups.



*   AuthDomain domain() - AuthDomain is an enumeration with values “local” and “external”. It MAY alternatively be represented as String.
*   User user() - returns a new mutable User object each time this method is called. Modifying the fields of the returned User MUST have no effect on the UserAndMetadata object it came from.
*   Set effectiveRoles() - all roles, regardless of origin.
*   List effectiveRolesAndOrigins() - same as effectiveRoles, but with origin information included.
*   Optional passwordChanged()
*   Set externalGroups()

### Group

Mutable. Defines a set of roles that may be inherited by users. All properties of the Group class MUST have associated setters except for “name” which is fixed when the object is created.



*   String name()
*   String description()
*   Set roles() - [Role](#h.zhz0katumzwe) as defined in the User Manager section
*   Optional ldapGroupReference()

## Service Interface













public interface IUserManager{



        UserAndMetadata GetUser(string username, GetUserOptions options);



        Iterable GetAllUsers(GetAllUsersOptions options);



            void UpsertUser(User user, UpsertUserOptions options);



        void DropUser(string userName, DropUserOptions options);



        Iterable AvailableRoles(AvailableRolesOptions options);



        Group GetGroup(string groupName, GetGroupOptions options);



        Iterable GetAllGroups(GetAllGroupsOptions options);



            void UpsertGroup(Group group, UpsertGroupOptions options);



        void DropGroup(string groupName, DropGroupOptions options);

}









#### 

#### GetUser

Gets a user.

Signature











UserAndMetadata GetUser(string username, [options])









Parameters

*   Required:

*   username: string - ID of the user.

*   Optional:

*   domainName: string - name of the user domain. Defaults to local.        
*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

An instance of UserAndMetadata.

Throws

*   UserNotFoundException
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform



Implementation Notes



When parsing the “get” and “getAll” responses, take care to distinguish between roles assigned directly to the user (role origin with type=”user”) and roles inherited from groups (role origin with type=”group” and name=).



If the server response does not include an “origins” field for a role, then it was generated by a server version prior to 6.5 and the SDK MUST treat the role as if it had a single origin of type=”user”.



#### GetAllUsers

Gets all users.

Signature











Iterable GetAllUsers([options])









Parameters

*   Required:
*   Optional:

*   domainName: string - name of the user domain. Defaults to local.
*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

An iterable collection of UserAndMetadata.

Throws

*   Any exceptions raised by the underlying platform

#### UpsertUser

Creates or updates a user.

Signature











void UpsertUser(User user, [options])









Parameters

*   Required:

*   user: User - the new version of the user.

*   Optional:

*   DomainName: string - name of the user domain (local | external). Defaults to local.
*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform



Implementation Notes



When building the PUT request to send to the REST endpoint, implementations MUST omit the “password” property if it is not present in the given User domain object (so that the password is only changed if the calling code provided a new password).



For backwards compatibility with Couchbase Server 6.0 and earlier, the “groups” parameter MUST be omitted if the group list is empty. Couchbase Server 6.5 treats the absent parameter the same as an explicit parameter with no value (removes any existing group associations, which is what we want in this case).



#### DropUser

Removes a user.

Signature











void DropUser(string username, [options])









Parameters

*   Required:

*   username: string - ID of the user.

*   Optional:

*   DomainName: string - name of the user domain. Defaults to local.
*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   UserNotFoundException
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform



#### Available Roles

Returns the roles supported by the server.

Signature











Iterable GetRoles([options])









Parameters

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

An iterable collection of RoleAndDescription.

Throws

*   Any exceptions raised by the underlying platform



#### GetGroup

Gets a group.



REST Endpoint: GET /settings/rbac/groups/

Signature











Group GetGroup(string groupName, [options])









Parameters

*   Required:

*   groupName: string - name of the group to get.

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

An instance of Group.

Throws

*   GroupNotFoundException
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform



#### GetAllGroups

Gets all groups.



REST Endpoint: GET /settings/rbac/groups

Signature











Iterable GetAllGroups([options])









Parameters

*   Required:
*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

An iterable collection of Group.

Throws

*   Any exceptions raised by the underlying platform

#### UpsertGroup

Creates or updates a group.



REST Endpoint: PUT /settings/rbac/groups/

This endpoint accepts application/x-www-form-urlencoded and requires the data be sent as form data. The name/id should not be included in the form data. Roles should be a comma separated list of strings. If, only if, the role contains a bucket name then the rolename should be suffixed with[] e.g. bucket_full_access[default],security_admin.

Signature











void UpsertGroup(Group group, [options])









Parameters

*   Required:

*   group: Group - the new version of the group.

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform



#### DropGroup

Removes a group.



REST Endpoint: DELETE /settings/rbac/groups/

Signature











void DropGroup(string groupName, [options])









Parameters

*   Required:

*   groupName: string - name of the group.

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   GroupNotFoundException
*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

# Collections Manager

Note: due to [https://issues.couchbase.com/browse/MB-35386](https://www.google.com/url?q=https://issues.couchbase.com/browse/MB-35386&sa=D&ust=1569855744460000) CollectionExists, ScopeExists, and GetScope must support both forms of the manifest until SDK beta. That is, going forward:



{“uid”:“0",“scopes”:[{“name”:“_default”,“uid”:“0”,“collections”:[{“name”:“_default”,“uid”:“0"}]}]}



And for the sake of support for the server beta which did not have the fix in place:

{“uid”:0,“scopes”:{“_default”:{“uid”:0,“collections”:{“_default”:{“uid”:0}}}}}

It is recommended to try to parse the first form and fallback to the second so that it can be easily removed later.













public interface ICollectionManager{



            boolean CollectionExists(ICollectionSpec collection, CollectionExistsOptions options);



            boolean ScopeExists(string scopeName, ScopeExistsOptions options);



            IScopeSpec GetScope(string scopeName, GetScopeOptions options);



           Iterable GetAllScopes(GetAllScopesOptions options);



void CreateCollection(ICollectionSpec collection, CreateCollectionOptions options);



        void DropCollection(ICollectionSpec collection, DropCollectionOptions options);



         void CreateScope(IScopeSpec scope, CreateScopeOptions options);[[i]](#cmnt9)[[j]](#cmnt10)



        void DropScope(string scopeName, DropScopeOptions options);



        void FlushCollection[[k]](#cmnt11)[[l]](#cmnt12)[[m]](#cmnt13)[[n]](#cmnt14)(ICollectionSpec collection, FlushCollectionOptions options);

}





















#### Collection Exists

Checks for existence of a collection. This will fetch a manifest and then interrogate it to check that the scope name exists and then that the collection name exists within that scope.

Signature











boolean CollectionExists(ICollectionSpec collection,  [options])









Parameters

*   Required:

*   collection: ICollectionSpec - spec of the collection.

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   Any exceptions raised by the underlying platform
*   InvalidArgumentsException

Uri

*   GET /pools/default/buckets//collections

#### Scope Exists

Checks for existence of a scope. This will fetch a manifest and then interrogate it to check that the scope name exists.

Signature











boolean ScopeExists(String scopeName,  [options])









Parameters

*   Required:

*   scopeName: string - name of the scope.

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   Any exceptions raised by the underlying platform

Uri

*   GET /pools/default/buckets//collections

#### Get Scope

Gets a scope. This will fetch a manifest and then pull the scope out of it.

Signature











IScopeSpec GetScope(string scopeName,  [options])









Parameters

*   Required:

*   scopeName: string - name of the scope.

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   ScopeNotFoundException
*   Any exceptions raised by the underlying platform

Uri

*   GET /pools/default/buckets//collections

#### Get All Scopes

Gets all scopes. This will fetch a manifest and then pull the scopes out of it.

Signature











iterable GetAllScopes([options])









Parameters

*   Required:
*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   Any exceptions raised by the underlying platform

Uri

*   GET /pools/default/buckets//collections

#### Create Collection

Creates a new collection.

Signature











void CreateCollection(CollectionSpec collection, [options])









Parameters

*   Required:

*   collection: CollectionSpec - specification of the collection.

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   InvalidArgumentsException
*   CollectionAlreadyExistsException
*   ScopeNotFoundException
*   Any exceptions raised by the underlying platform

Uri

*   POST http://localhost:8091/pools/default/buckets//collections/ -d name=

#### Drop Collection

Removes a collection.

Signature











void DropCollection(ICollectionSpec collection, [options])









Parameters

*   Required:

*   collection: ICollectionSpec - namspece of the collection.

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   CollectionNotFoundException
*   Any exceptions raised by the underlying platform

Uri

*   DELETE http://localhost:8091/pools/default/buckets//collections//

#### Create Scope

Creates a new scope.

Signature











Void CreateScope(string scopeName, [options])









Parameters

*   Required:

*   scopeName: String - name of the scope.

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   InvalidArgumentsException
*   Any exceptions raised by the underlying platform

Uri

*   POST [http://localhost:8091/pools/default/buckets/](https://www.google.com/url?q=http://localhost:8091/pools/default/buckets/&sa=D&ust=1569855744485000)/collections -d name=

#### Drop Scope

Removes a scope.

Signature











void DropScope(string scopeName, [options])









Parameters

*   Required:

*   collectionName: string - name of the collection.

*   Optional:

*   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

Returns

Throws

*   ScopeNotFoundException
*   Any exceptions raised by the underlying platform

Uri

*   DELETE [http://localhost:8091/pools/default/buckets/](https://www.google.com/url?q=http://localhost:8091/pools/default/buckets/&sa=D&ust=1569855744488000)/collections/

# Types

#### DesignDocument

DesignDocument provides a means of mapping a design document into an object. It contains within it a map of View.













 type DesignDocument{



String Name();

                

        Map[String]IView Views();

}











#### View











 type View{



            String Map();

                

            String Reduce();

}









## 

#### IQueryIndex Interface

The IQueryIndex interface provides a means of mapping a query index into an object.













 interface IQueryIndex{



            String Name();

                

        Bool IsPrimary();



        IndexType Type();



        String State();



        String Keyspace();



Iterable IndexKey();



        Optional Condition();

}











#### AnalyticsDataset Interface

AnalyticsDataset provides a means of mapping dataset details into an object.













 interface AnalyticsDataset{



            String Name();

                

        String DataverseName();

                

        String LinkName();

                

        String BucketName();

}









#### AnalyticsIndex Interface

AnalyticsIndex provides a means of mapping analytics index details into an object.













 interface AnalyticsDataset{



            String Name();

                

        String DatasetName();



        String DataverseName();

                

        Bool IsPrimary();

}









#### 

#### BucketSettings

BucketSettings provides a means of mapping bucket settings into an object.

*   Name (string) - The name of the bucket.
*   FlushEnabled (bool) - Whether or not flush should be enabled on the bucket. Default to false.
*   RamQuotaMB (int) - Ram Quota in mb for the bucket. (rawRAM in the server payload)
*   NumReplicas (int) - The number of replicas for documents.
*   ReplicaIndexes (bool) - Whether replica indexes should be enabled for the bucket.
*   BucketType {couchbase (sent on wire as membase), memcached, ephemeral} - The type of the bucket. Default to couchbase.
*   EjectionMethod {fullEviction | valueOnly}. The eviction policy to use.
*   maxTTL (int) - Value for the maxTTL of new documents created without a ttl.
*   compressionMode {off | passive | active} - The compression mode to use.

#### CreateBucketSettings

CreateBucketSettings is a superset of BucketSettings providing one extra property:

*   ConflictResolutionType {Timestamp (sent as lww) | SequenceNumber (sent as seqno)}. The conflict resolution type to use.

The reasoning for this is that on Update ConflictResolutionType cannot be present in the JSON payload at all.



#### UpsertIndeSearchIndex

SearchIndex provides a means to map search indexes into object. The Params, SourceParams, and PlanParams fields are left to the SDK to decide what is idiomatic (e.g. JSONObject), the definitions of these fields is purposefully vague.











type SearchIndex struct {

        // UUID is required for updates. It provides a means of ensuring consistency, the UUID must match the UUID value

        // for the index on the server.

        UUID string `json:"uuid"`



        Name string `json:"name"`



        // SourceName is the name of the source of the data for the index e.g. bucket name.

        SourceName string `json:"sourceName,omitempty"`



        // Type is the type of index, e.g. fulltext-index or fulltext-alias.

        Type string `json:"type"`



        // IndexParams are index properties such as store type and mappings.

        Params map[string]interface{} `json:"params"`



        // SourceUUID is the UUID of the data source, this can be used to more tightly tie the index to a source.

        SourceUUID string `json:"sourceUUID,omitempty"`



        // SourceParams are extra parameters to be defined. These are usually things like advanced connection and tuning

        // parameters.

        SourceParams map[string]interface{} `json:"sourceParams,omitempty"`



        // SourceType is the type of the data source, e.g. couchbase or nil depending on the Type field.

        SourceType string `json:"sourceType"`



        // PlanParams are plan properties such as number of replicas and number of partitions.

        PlanParams map[string]interface{} `json:"planParams,omitempty"`

}













#### IUser Interface

The IUser interface provides a means of mapping user settings into an object.













 Interface IUser{



            String ID();



            String Name();

        

            Iterable Roles();

}











#### ICollectionSpec Interface













 Interface ICollectionSpec{



            String Name();

        

            String ScopeName();

}











#### IScopeSpec Interface













 Interface IScopeSpec{



            String Name();

        

            Iterable Collections();

}

















# References

*   Query index management

*   [https://github.com/couchbaselabs/sdk-rfcs/blob/master/rfc/0003-indexmanagement.md](https://www.google.com/url?q=https://github.com/couchbaselabs/sdk-rfcs/blob/master/rfc/0003-indexmanagement.md&sa=D&ust=1569855744515000)
*   [https://docs.couchbase.com/server/current/n1ql/n1ql-language-reference/](https://www.google.com/url?q=https://docs.couchbase.com/server/current/n1ql/n1ql-language-reference/&sa=D&ust=1569855744516000)

*   Search index management

*   [https://docs.google.com/document/d/1C4yfTj5u6ahRgk3ZIL_AkwPMeu9-hHY_lZcsDNeIP74](https://www.google.com/url?q=https://docs.google.com/document/d/1C4yfTj5u6ahRgk3ZIL_AkwPMeu9-hHY_lZcsDNeIP74&sa=D&ust=1569855744517000)
*   [https://docs.couchbase.com/server/6.0/rest-api/rest-fts-indexing.html](https://www.google.com/url?q=https://docs.couchbase.com/server/6.0/rest-api/rest-fts-indexing.html&sa=D&ust=1569855744517000)
*   [http://labs.couchbase.com/cbft/dev-guide/index-definitions/](https://www.google.com/url?q=http://labs.couchbase.com/cbft/dev-guide/index-definitions/&sa=D&ust=1569855744518000)

*   Outdated but contains some useful definitions for fields.

*   User Management

*   [https://github.com/couchbaselabs/sdk-rfcs/blob/master/rfc/0022-usermgmt.md](https://www.google.com/url?q=https://github.com/couchbaselabs/sdk-rfcs/blob/master/rfc/0022-usermgmt.md&sa=D&ust=1569855744518000)

*   Bucket Management

*   [https://docs.couchbase.com/server/current/rest-api/rest-bucket-intro.html](https://www.google.com/url?q=https://docs.couchbase.com/server/current/rest-api/rest-bucket-intro.html&sa=D&ust=1569855744519000)

*   Collection Management

*   [https://github.com/couchbase/ns_server/commit/4c1a9ea20fbdb148f68ec2ad7be9eed4c071bf9e](https://www.google.com/url?q=https://github.com/couchbase/ns_server/commit/4c1a9ea20fbdb148f68ec2ad7be9eed4c071bf9e&sa=D&ust=1569855744519000)
*   [https://docs.google.com/document/d/1X-v8GWQjplrMMaYwwWOzEuP4AUoDNIAvS39NmEjQ3_E/edit#heading=h.gprum229kohk](https://www.google.com/url?q=https://docs.google.com/document/d/1X-v8GWQjplrMMaYwwWOzEuP4AUoDNIAvS39NmEjQ3_E/edit%23heading%3Dh.gprum229kohk&sa=D&ust=1569855744520000)

*   Views REST API

*   [https://docs.couchbase.com/server/6.0/rest-api/rest-views-intro.html](https://www.google.com/url?q=https://docs.couchbase.com/server/6.0/rest-api/rest-views-intro.html&sa=D&ust=1569855744520000)

*   Groups and LDAP Groups

*   [https://docs.google.com/document/d/1wsjEmke80RW_sbW0ycS8yQl6rq5lzBbRWuelPZ1m9ZI/edit#](https://www.google.com/url?q=https://docs.google.com/document/d/1wsjEmke80RW_sbW0ycS8yQl6rq5lzBbRWuelPZ1m9ZI/edit%23&sa=D&ust=1569855744521000)
*   [https://docs.google.com/document/d/1cFZOz9n6ZKyq_thxCSteuLrZ0rJEh7AMT3MFbOHCchM/edit](https://www.google.com/url?q=https://docs.google.com/document/d/1cFZOz9n6ZKyq_thxCSteuLrZ0rJEh7AMT3MFbOHCchM/edit&sa=D&ust=1569855744521000)
*   [https://issues.couchbase.com/browse/MB-16035](https://www.google.com/url?q=https://issues.couchbase.com/browse/MB-16035&sa=D&ust=1569855744522000)

*   Analytics management

*   [https://docs.couchbase.com/server/current/analytics/5_ddl.html](https://www.google.com/url?q=https://docs.couchbase.com/server/current/analytics/5_ddl.html&sa=D&ust=1569855744522000)



# Changes

2019-09-30:

*   Remove dataverse name checking from all Analytics options blocks so that if the dataverse name is set we do not check if the dataset already contains it.
*   Added Condition to IQueryIndex.
*   Changed User AvailableRoles to GetRoles.
*   Change ConnectLink and DisconnectLink so that the name is optional, defaulting to Local.

2019-09-18:

*   Add FlushNotEnabledException to bucket Flush operation

2019-09-03:

*    Add numReplicas option to QueryIndexManager CreatePrimaryIndex



[[a]](#cmnt_ref1)Java path-finding impl also has AND `using` = \"gsi\"





[[b]](#cmnt_ref2)I believe this is from back in the very first versions of N1QL, where it was required to be specified.  I don't think we need to bring this behaviour forward.





[[c]](#cmnt_ref3)Java impl does this by getting all indexes and doing BUILD INDEX on any currently set to deferred.  Thought we weren't doing racey stuff like that in client as general rule?





[[d]](#cmnt_ref4)That wouldn't be racy, since your going to build exactly the indices that you find during the first call.  From a functional perspective, only indexes that were deferred at the time you called the method are being built, which I think makes sense.





[[e]](#cmnt_ref5)+charles.dixon@couchbase.com Should there be an optional `dataverse` parameter?





[[f]](#cmnt_ref6)And an optional `force` parameter?





[[g]](#cmnt_ref7)I guess we should make an escape style of parameter to future proof it.





[[h]](#cmnt_ref8)I don't think we need to have an escape hatch on something that only exists for ease of use.  Relatedly, why does CONNECT LINK even accept a dataverse name?





[[i]](#cmnt_ref9)There is still a question around this, I suggest that we just accept a string Name rather than a ScopeSpec and we don't create collections as a part of this. It isn't attempting to be an atomic operation that way.





[[j]](#cmnt_ref10)I would be in favour of this change.





[[k]](#cmnt_ref11)This is missing the function definition below like the others.





[[l]](#cmnt_ref12)There seems to be some confusion over what this command does. The collections design doc states that there will be a flush endpoint that we can call over REST. I don't believe that it's implemented by ns server yet though.





[[m]](#cmnt_ref13)https://docs.google.com/document/d/1X-v8GWQjplrMMaYwwWOzEuP4AUoDNIAvS39NmEjQ3_E/edit#heading=h.8c7d3zbqy7i is what I'm referring to





[[n]](#cmnt_ref14)Server-side flushing was not implemented, instead it was decided that flushing a collection could be achieved trivially by the SDK through the destruction and recreation of the collection.

SDK 3.0: Management APIs RFC

  SDK-RFC #54

  # Meta

  *   Name: SDK Management APIs
  *   RFC ID: 54
  *   Start-Date: 2019-06-13
  *   Owner: Charles Dixon
  *   Current Status: draft

  

  

  

  [Meta](#h.d61txvmb5lyx)

  [Summary](#h.mupne99cshsu)

  [Motivation](#h.fd9za96e3yg5)

  [General Design](#h.k3nh685gh3zd)

  [Service Not Configured](#h.fazo4li6zut4)

  [Feature Not Found](#h.g3sb6exbieep)

  [View Index Manager](#h.awf5c5g6sfub)

  [Methods](#h.ltp1wzfhvkmd)

  [GetDesignDocument](#h.9xwvwfmx35g1)

  [GetAllDesignDocuments](#h.3cni9ir8h3pd)

  [UpsertDesignDocument](#h.myqscrntq9od)

  [DropDesignDocument](#h.fejq3trrq88k)

  [PublishDesignDocument](#h.ytabqazgaibt)

  [Query Index Manager](#h.vor45gro2p0)

  [Methods](#h.vpcih9gceh5x)

  [GetAllIndexes](#h.d9bt9ug8rdnk)

  [CreateIndex](#h.25pbsjaw1r1t)

  [CreatePrimaryIndex](#h.i3nri1f7emcm)

  [DropIndex](#h.w5uphn3aj7a6)

  [DropPrimaryIndex](#h.8fkshrim697h)

  [WatchIndexes](#h.1jpy9kneh3ix)

  [BuildDeferredIndexes](#h.2g1b86t843xh)

  [Search Index Manager](#h.n72o3wjrgzcr)

  [Methods](#h.7ypleagc8f02)

  [GetIndex](#h.muduzks94csy)

  [GetAllIndexes](#h.rm7ralf543po)

  [UpsertIndex](#h.vojyv926dm9l)

  [DropIndex](#h.7kr1kyi2cud7)

  [GetIndexedDocumentsCount](#h.920wzxyyn8h0)

  [PauseIngest](#h.shct6uc5c13v)

  [ResumeIngest](#h.7b3my87vq187)

  [AllowQuerying](#h.3b0hek5e6cru)

  [DisallowQuerying](#h.burvg6qrwgc1)

  [FreezePlan](#h.xed0g6nk80ih)

  [UnfreezePlan](#h.o6413lybnsbd)

  [AnalyzeDocument](#h.slz9r181j64v)

  [Analytics Index Manager](#h.wey00euqxg6r)

  [Create Dataverse](#h.84qyvlkb4ct)

  [Drop Dataverse](#h.duuryzz83ji6)

  [CreateDataset](#h.p8q696h2j1c2)

  [DropDataset](#h.diqletr3ee8t)

  [GetAllDatasets](#h.yeup6dx0ca2i)

  [CreateIndex](#h.s2ix1a2i9750)

  [DropIndex](#h.sp8nw6p5hw3y)

  [GetAlIndexes](#h.gu1vgfz28b4q)

  [Connect Link](#h.urr6tlame907)

  [Disconnect Link](#h.f24cpp9is9ur)

  [Get Pending Mutations](#h.43ulyhfxecvc)

  [Bucket Manager](#h.a3jxd57mov7x)

  [CreateBucket](#h.7azm73gy346n)

  [UpdateBucket](#h.z6hp9xboxiox)

  [DropBucket](#h.40gpci3gs7n9)

  [GetBucket](#h.hsjjz8tpuhmp)

  [GetAllBuckets](#h.rxc15d7zi17u)

  [FlushBucket](#h.6lr2bzo2rpmg)

  [User Manager](#h.e1pyjdt66quk)

  [Role](#h.zhz0katumzwe)

  [RoleAndDescription](#h.dvcwkh4ud3go)

  [Origin](#h.n3o3qrb2hyz0)

  [RoleAndOrigins](#h.qxxi2pw80si1)

  [User](#h.3t1esyo2jmzd)

  [UserAndMetadata](#h.ra67vzjmec2v)

  [Group](#h.829b0i5yexun)

  [Service Interface](#h.kgjocyhklu1b)

  [GetUser](#h.1f3vxv6mfj2c)

  [GetAllUsers](#h.8jz0zts2uhqs)

  [UpsertUser](#h.dxc9109hkfhu)

  [DropUser](#h.it10rl3v5b78)

  [Available Roles](#h.orpyjhkf4za3)

  [GetGroup](#h.m6gv1571p3x2)

  [GetAllGroups](#h.h4uhsanhpfyb)

  [UpsertGroup](#h.35x8b5tnome6)

  [DropGroup](#h.bcaum5sclz6c)

  [Collections Manager](#h.8zfr25d06mmc)

  [Collection Exists](#h.jcy2l3znakl)

  [Scope Exists](#h.c30miu3maaya)

  [Get Scope](#h.y7nm7r1beg3i)

  [Get All Scopes](#h.w9ysz23ucxr9)

  [Create Collection](#h.v25764vsi0ze)

  [Drop Collection](#h.2nrt7s3vbsx9)

  [Create Scope](#h.80xchr7kse1x)

  [Drop Scope](#h.bzbzwqo5ea52)

  [Types](#h.hxsna6v0yga2)

  [DesignDocument](#h.h075tca0i0r9)

  [View](#h.ugcnslp1w79c)

  [IQueryIndex Interface](#h.yipr3bi8gyda)

  [AnalyticsDataset Interface](#h.t3sgseba5k26)

  [AnalyticsIndex Interface](#h.cd1vwisd9cvl)

  [BucketSettings](#h.bm3qgxw9689)

  [CreateBucketSettings](#h.um6jv51ydhmv)

  [SearchIndex](#h.w2u8bmxhvxn1)

  [IUser Interface](#h.gc7j9dg0shou)

  [ICollectionSpec Interface](#h.9moo4a588hua)

  [IScopeSpec Interface](#h.zfjuduk2ojhv)

  [References](#h.tatjn76gk22e)

  

  

  # Summary

  Defines the management APIs for SDK 3.0 that each SDK must implement.

  # Motivation

  

  # General Design

  The management APIs are made up of several interfaces; Bucket Manager, User Manager, Search Index Manager, View Index Manager, Query Index Manager, Analytics Index Manager, and Collection Manager.

  

  On the cluster interface:

  

  

  

  

  

  

  IUserManager Users();

  

  IBucketManager Buckets();

  

  IQueryIndexManager QueryIndexes();

  

  IAnalyticsIndexManager AnalyticsIndexes();

  

  

  

  

  ISearchIndexManager SearchIndexes();

  

  

  

  

  

  On the bucket interface:

  

  

  

  

  

  

  ICollectionManager Collections();

  

  

  

  

  IViewIndexManager ViewIndexes();

  

  

  

  

  

  # Service Not Configured

  If a manager is requested for a service which is not configured on the cluster then a ServiceNotConfiguredException must be raised. This can be detected by looking in the cluster config object, if the endpoint for the service has no servers listed then it is not configured.

  # Feature Not Found

  Some features, such as groups, certain functions, and collections are not supported on all server versions. If an endpoint is requested against a server version that does not support that endpoint then the HTTP response will be a 404 containing the body “Not Found.”. If this is returned then the SDK must return  a FeatureNotFoundException to the user.

  # View Index Manager

  The View Index Manager interface contains the means for managing design documents used for views.

  

  A design document belongs to either the “development” or “production” namespace. A development document has a name that starts with “dev_”. This is an implementation detail we’ve chosen to hide from consumers of this API. Document names presented to the user (returned from the “get” and “get all” methods, for example) always have the “dev_” prefix stripped.

  

  Whenever the user passes a design document name to any method of this API, the user may refer to the document using the “dev_” prefix regardless of whether the user is referring to a development document or production document. The “dev_” prefix is always stripped from user input, and the actual document name passed to the server is determined by the “namespace” argument..

  

  All methods (except publish) have a required “namespace” argument indicating whether the operation targets a development document or a production document. The type of this argument is an enum called DesignDocumentNamespace with values PRODUCTION and DEVELOPMENT.

  

  

  

  

  

  

  

  Interface IViewIndexManager {

  

          DesignDocumentGetDesignDocument(string designDocName, DesignDocumentNamespace namespace, GetDesignDocumentOptions options);

  

          Iterable GetAllDesignDocuments(DesignDocumentNamespace namespace, GetAllDesignDocumentsOptions options);

  

          void UpsertDesignDocument(DesignDocument indexData, DesignDocumentNamespace namespace, UpsertDesignDocumentOptions options);

  

          void DropDesignDocument(string designDocName, DesignDocumentNamespace namespace, DropDesignDocumentOptions options);

  

  

          void PublishDesignDocument(string designDocName, PublishDesignDocumentOptions options);

  }

  

  

  

  

  

  

  

  

  

  

  ### Methods

  The following methods must be implemented:

  #### GetDesignDocument

  Fetches a design document from the server if it exists.

  Signature

  

  

  

  

  

  DesignDocumentGetDesignDocument(string designDocName, DesignDocumentNamespace namespace, [options])
  SDK 3.0: Management APIs RFC

  SDK-RFC #54

  # Meta

  *   Name: SDK Management APIs
  *   RFC ID: 54
  *   Start-Date: 2019-06-13
  *   Owner: Charles Dixon
  *   Current Status: draft

  

  

  

  [Meta](#h.d61txvmb5lyx)

  [Summary](#h.mupne99cshsu)

  [Motivation](#h.fd9za96e3yg5)

  [General Design](#h.k3nh685gh3zd)

  [Service Not Configured](#h.fazo4li6zut4)

  [Feature Not Found](#h.g3sb6exbieep)

  [View Index Manager](#h.awf5c5g6sfub)

  [Methods](#h.ltp1wzfhvkmd)

  [GetDesignDocument](#h.9xwvwfmx35g1)

  [GetAllDesignDocuments](#h.3cni9ir8h3pd)

  [UpsertDesignDocument](#h.myqscrntq9od)

  [DropDesignDocument](#h.fejq3trrq88k)

  [PublishDesignDocument](#h.ytabqazgaibt)

  [Query Index Manager](#h.vor45gro2p0)

  [Methods](#h.vpcih9gceh5x)

  [GetAllIndexes](#h.d9bt9ug8rdnk)

  [CreateIndex](#h.25pbsjaw1r1t)

  [CreatePrimaryIndex](#h.i3nri1f7emcm)

  [DropIndex](#h.w5uphn3aj7a6)

  [DropPrimaryIndex](#h.8fkshrim697h)

  [WatchIndexes](#h.1jpy9kneh3ix)

  [BuildDeferredIndexes](#h.2g1b86t843xh)

  [Search Index Manager](#h.n72o3wjrgzcr)

  [Methods](#h.7ypleagc8f02)

  [GetIndex](#h.muduzks94csy)

  [GetAllIndexes](#h.rm7ralf543po)

  [UpsertIndex](#h.vojyv926dm9l)

  [DropIndex](#h.7kr1kyi2cud7)

  [GetIndexedDocumentsCount](#h.920wzxyyn8h0)

  [PauseIngest](#h.shct6uc5c13v)

  [ResumeIngest](#h.7b3my87vq187)

  [AllowQuerying](#h.3b0hek5e6cru)

  [DisallowQuerying](#h.burvg6qrwgc1)

  [FreezePlan](#h.xed0g6nk80ih)

  [UnfreezePlan](#h.o6413lybnsbd)

  [AnalyzeDocument](#h.slz9r181j64v)

  [Analytics Index Manager](#h.wey00euqxg6r)

  [Create Dataverse](#h.84qyvlkb4ct)

  [Drop Dataverse](#h.duuryzz83ji6)

  [CreateDataset](#h.p8q696h2j1c2)

  [DropDataset](#h.diqletr3ee8t)

  [GetAllDatasets](#h.yeup6dx0ca2i)

  [CreateIndex](#h.s2ix1a2i9750)

  [DropIndex](#h.sp8nw6p5hw3y)

  [GetAlIndexes](#h.gu1vgfz28b4q)

  [Connect Link](#h.urr6tlame907)

  [Disconnect Link](#h.f24cpp9is9ur)

  [Get Pending Mutations](#h.43ulyhfxecvc)

  [Bucket Manager](#h.a3jxd57mov7x)

  [CreateBucket](#h.7azm73gy346n)

  [UpdateBucket](#h.z6hp9xboxiox)

  [DropBucket](#h.40gpci3gs7n9)

  [GetBucket](#h.hsjjz8tpuhmp)

  [GetAllBuckets](#h.rxc15d7zi17u)

  [FlushBucket](#h.6lr2bzo2rpmg)

  [User Manager](#h.e1pyjdt66quk)

  [Role](#h.zhz0katumzwe)

  [RoleAndDescription](#h.dvcwkh4ud3go)

  [Origin](#h.n3o3qrb2hyz0)

  [RoleAndOrigins](#h.qxxi2pw80si1)

  [User](#h.3t1esyo2jmzd)

  [UserAndMetadata](#h.ra67vzjmec2v)

  [Group](#h.829b0i5yexun)

  [Service Interface](#h.kgjocyhklu1b)

  [GetUser](#h.1f3vxv6mfj2c)

  [GetAllUsers](#h.8jz0zts2uhqs)

  [UpsertUser](#h.dxc9109hkfhu)

  [DropUser](#h.it10rl3v5b78)

  [Available Roles](#h.orpyjhkf4za3)

  [GetGroup](#h.m6gv1571p3x2)

  [GetAllGroups](#h.h4uhsanhpfyb)

  [UpsertGroup](#h.35x8b5tnome6)

  [DropGroup](#h.bcaum5sclz6c)

  [Collections Manager](#h.8zfr25d06mmc)

  [Collection Exists](#h.jcy2l3znakl)

  [Scope Exists](#h.c30miu3maaya)

  [Get Scope](#h.y7nm7r1beg3i)

  [Get All Scopes](#h.w9ysz23ucxr9)

  [Create Collection](#h.v25764vsi0ze)

  [Drop Collection](#h.2nrt7s3vbsx9)

  [Create Scope](#h.80xchr7kse1x)

  [Drop Scope](#h.bzbzwqo5ea52)

  [Types](#h.hxsna6v0yga2)

  [DesignDocument](#h.h075tca0i0r9)

  [View](#h.ugcnslp1w79c)

  [IQueryIndex Interface](#h.yipr3bi8gyda)

  [AnalyticsDataset Interface](#h.t3sgseba5k26)

  [AnalyticsIndex Interface](#h.cd1vwisd9cvl)

  [BucketSettings](#h.bm3qgxw9689)

  [CreateBucketSettings](#h.um6jv51ydhmv)

  [SearchIndex](#h.w2u8bmxhvxn1)

  [IUser Interface](#h.gc7j9dg0shou)

  [ICollectionSpec Interface](#h.9moo4a588hua)

  [IScopeSpec Interface](#h.zfjuduk2ojhv)

  [References](#h.tatjn76gk22e)

  

  

  # Summary

  Defines the management APIs for SDK 3.0 that each SDK must implement.

  # Motivation

  

  # General Design

  The management APIs are made up of several interfaces; Bucket Manager, User Manager, Search Index Manager, View Index Manager, Query Index Manager, Analytics Index Manager, and Collection Manager.

  

  On the cluster interface:

  

  

  

  

  

  

  IUserManager Users();

  

  IBucketManager Buckets();

  

  IQueryIndexManager QueryIndexes();

  

  IAnalyticsIndexManager AnalyticsIndexes();

  

  

  

  

  ISearchIndexManager SearchIndexes();

  

  

  

  

  

  On the bucket interface:

  

  

  

  

  

  

  ICollectionManager Collections();

  

  

  

  

  IViewIndexManager ViewIndexes();

  

  

  

  

  

  # Service Not Configured

  If a manager is requested for a service which is not configured on the cluster then a ServiceNotConfiguredException must be raised. This can be detected by looking in the cluster config object, if the endpoint for the service has no servers listed then it is not configured.

  # Feature Not Found

  Some features, such as groups, certain functions, and collections are not supported on all server versions. If an endpoint is requested against a server version that does not support that endpoint then the HTTP response will be a 404 containing the body “Not Found.”. If this is returned then the SDK must return  a FeatureNotFoundException to the user.

  # View Index Manager

  The View Index Manager interface contains the means for managing design documents used for views.

  

  A design document belongs to either the “development” or “production” namespace. A development document has a name that starts with “dev_”. This is an implementation detail we’ve chosen to hide from consumers of this API. Document names presented to the user (returned from the “get” and “get all” methods, for example) always have the “dev_” prefix stripped.

  

  Whenever the user passes a design document name to any method of this API, the user may refer to the document using the “dev_” prefix regardless of whether the user is referring to a development document or production document. The “dev_” prefix is always stripped from user input, and the actual document name passed to the server is determined by the “namespace” argument..

  

  All methods (except publish) have a required “namespace” argument indicating whether the operation targets a development document or a production document. The type of this argument is an enum called DesignDocumentNamespace with values PRODUCTION and DEVELOPMENT.

  

  

  

  

  

  

  

  Interface IViewIndexManager {

  

          DesignDocumentGetDesignDocument(string designDocName, DesignDocumentNamespace namespace, GetDesignDocumentOptions options);

  

          Iterable GetAllDesignDocuments(DesignDocumentNamespace namespace, GetAllDesignDocumentsOptions options);

  

          void UpsertDesignDocument(DesignDocument indexData, DesignDocumentNamespace namespace, UpsertDesignDocumentOptions options);

  

          void DropDesignDocument(string designDocName, DesignDocumentNamespace namespace, DropDesignDocumentOptions options);

  

  

          void PublishDesignDocument(string designDocName, PublishDesignDocumentOptions options);

  }

  

  

  

  

  

  

  

  

  

  

  ### Methods

  The following methods must be implemented:

  #### GetDesignDocument

  Fetches a design document from the server if it exists.

  Signature

  

  

  

  

  

  DesignDocumentGetDesignDocument(string designDocName, DesignDocumentNamespace namespace, [options])

  

  

  

  

  Parameters

  *   Required:

  *    designDocName: string - the name of the design document.
  *   namespace: enum - PRODUCTION if the user is requesting a document from the production namespace, or DEVELOPMENT if from the development namespace.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  An instance of DesignDocument.

  Throws

  *   DesignDocumentNotFoundException (http 404)
  *   Any exceptions raised by the underlying platform

  Uri

  *   GET http://localhost:8092//_design/

  Example response from server

  {  

     "views":{  

        "test":{  

           "map":"function (doc, meta) {\n\t\t\t\t\t\t  emit(meta.id, null);\n\t\t\t\t\t\t}",

           "reduce":"_count"

        }

     }

  }

  #### GetAllDesignDocuments

  Fetches all design documents from the server.

  ]

  When processing the server response, the client must strip the “_design/” prefix from the document ID (as well as the “_dev” prefix if present). For example, a doc.meta.id value of “_design/foo” must be parsed as “foo”, and “_design/dev_bar” must be parsed as “bar”.

  Signature

  

  

  

  

  

  Iterable GetAllDesignDocuments(DesignDocumentNamespace namespace, [options])

  

  

  

  

  Parameters

  *   Required:

  *   namespace (enum) - indicates whether the user wants to get production documents (PRODUCTION) or development documents (DEVELOPMENT).

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  An iterable of DesignDocument.

  Throws

  *   Any exceptions raised by the underlying platform

  Uri

  *   GET http://localhost:8091/pools/default/buckets//ddocs

  

  Example response from server

  {  

     "rows":[  

        {  

           "doc":{  

              "meta":{  

                 "id":"_design/dev_test",

                 "rev":"1-ae5e21ec"

              },

              "json":{  

                 "views":{  

                    "test":{  

                       "map":"function (doc, meta) {\n\t\t\t\t\t\t  emit(meta.id, null);\n\t\t\t\t\t\t}",

                       "reduce":"_count"

                    }

                 }

              }

           },

           "controllers":{  

              "compact":"/pools/default/buckets/default/ddocs/_design%2Fdev_test/controller/compactView",

              "setUpdateMinChanges":"/pools/default/buckets/default/ddocs/_design%2Fdev_test/controller/setUpdateMinChanges"

           }

        }

     ]

  }

  #### UpsertDesignDocument

  Updates, or inserts, a design document.

  Signature

  

  

  

  

  

  void UpsertDesignDocument(DesignDocument designDocData, DesignDocumentNamespace namespace, [options])

  

  

  

  

  Parameters

  *   Required:

  *   designDocData: DesignDocument - the data to use to create the design document
  *   namespace (enum) - indicates whether the user wants to upsert the document to the production namespace (PRODUCTION) or development namespace (DEVELOPMENT).

  *   Optional:

  *   
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   Any exceptions raised by the underlying platform

  Uri

  *   PUT http://localhost:8092//_design/

  #### DropDesignDocument

  Removes a design document.

  Signature

  

  

  

  

  

  void DropDesignDocument(string designDocName, DesignDocumentNamespace namespace,  [options])

  

  

  

  

  Parameters

  *   Required:

  *   designDocName: string - the name of the design document.
  *   namespace: enum - indicates whether the name refers to a production document (PRODUCTION) or a development document (DEVELOPMENT).

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   DesignDocumentNotFoundException (http 404)
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  Uri

  *   DELETE http://localhost:8092//_design/

  #### PublishDesignDocument

  Publishes a design document. This method is equivalent to getting a document from the development namespace and upserting it to the production namespace.

  Signature

  

  

  

  

  

  void PublishDesignDocument(string designDocName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   designDocName: string - the name of the development design document.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   DesignDocumentNotFoundException (http 404)
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  # Query Index Manager

  The Query Index Manager interface contains the means for managing indexes used for queries.

  

  

  

  

  

  

  

  public interface IQueryIndexManger{

  

          Iterable GetAllIndexes(string bucketName, GetAllQueryIndexOptions options);

  

  void CreateIndex(string bucketName, string indexName, []string fields, CreateQueryIndexOptions options);

  

             void CreatePrimaryIndex(string bucketName, CreatePrimaryQueryIndexOptions options);

  

          void DropIndex(string bucketName, string indexName, DropQueryIndexOptions options);

  

              void DropPrimaryIndex(string bucketName, DropPrimaryQueryIndexOptions options);

  

  void WatchIndexes(string bucketName, []string indexNames, timeout duration, WatchQueryIndexOptions options);

     

              void BuildDeferredIndexes(string bucketName, BuildQueryIndexOptions options);

  }

  

  

  

  

  

  ### Methods

  The following methods must be implemented:

  

  #### GetAllIndexes

  Fetches all indexes from the server.

  Signature

  

  

  

  

  

  Iterable GetAllIndexes(string bucketName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   BucketName: string - the name of the bucket.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  N1QL

  SELECT idx.* FROM system:indexes AS idx

      WHERE keyspace_id = "bucketName"

  [[a]](#cmnt1)[[b]](#cmnt2)

      ORDER BY is_primary DESC, name ASC

  Returns

  An array of IQueryIndex.

  Throws

  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  #### CreateIndex

  Creates a new index.

  Signature

  

  

  

  

  

  void CreateIndex(string bucketName, string indexName, []string fields,  [options])

  

  

  

  

  Parameters

  *   Required:

  *   BucketName: string - the name of the bucket.
  *   IndexName: string - the name of the index.
  *   fields: []string - the fields to create the index over.

  *   Optional:

  *   IgnoreIfExists (bool) - Don’t error/throw if the index already exists.
  *   NumReplicas (int) - The number of replicas that this index should have. Uses the WITH keyword and num_replica.

  *   CREATE INDEX indexNameON bucketName WITH { "num_replica": 2 }
  *   [https://docs.couchbase.com/server/current/n1ql/n1ql-language-reference/createindex.html](https://www.google.com/url?q=https://docs.couchbase.com/server/current/n1ql/n1ql-language-reference/createindex.html&sa=D&ust=1569855744308000)

  *   Deferred (bool) - Whether the index should be created as a deferred index.
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   IndexAlreadyExistsException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  #### CreatePrimaryIndex

  Creates a new primary index.

  Signature

  

  

  

  

  

  void CreatePrimaryIndex(string bucketName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   BucketName: string - name of the bucket.

  *   Optional:

  *   IndexName: string - name of the index.
  *   IgnoreIfExists (bool) - Don’t error/throw if the index already exists.
  *   NumReplicas (int) - The number of replicas that this index should have. Uses the WITH keyword and num_replica.

  *   CREATE INDEX indexNameON bucketName WITH { "num_replica": 2 }
  *   [https://docs.couchbase.com/server/current/n1ql/n1ql-language-reference/createindex.html](https://www.google.com/url?q=https://docs.couchbase.com/server/current/n1ql/n1ql-language-reference/createindex.html&sa=D&ust=1569855744311000)

  *   Deferred (bool) - Whether the index should be created as a deferred index.
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   QueryIndexAlreadyExistsException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  #### DropIndex

  Drops an index.

  Signature

  

  

  

  

  

  void DropIndex(string bucketName, string indexName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   BucketName: string - name of the bucket.
  *   IndexName: string - name of the index.

  *   Optional:

  *   IgnoreIfNotExists (bool) - Don’t error/throw if the index does not exist.
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   QueryIndexNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  #### DropPrimaryIndex

  Drops a primary index.

  Signature

  

  

  

  

  

  void DropPrimaryIndex(string bucketName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   BucketName: string - name of the bucket.

  *   Optional:

  *   IndexName: string - name of the index.
  *   IgnoreIfNotExists (bool) - Don’t error/throw if the index does not exist.
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   QueryIndexNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  #### WatchIndexes

  Watch polls indexes until they are online.

  Signature

  

  

  

  

  

  void WatchIndexes(string bucketName, []string indexNames, timeout duration, [options])

  

  

  

  

  Parameters

  *   Required:

  *   BucketName: string - name of the bucket.
  *   IndexName: []string - name(s) of the index(es).
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  *   Optional:

  *   WatchPrimary (bool) - whether or not to watch the primary index.

  Returns

  Throws

  *   QueryIndexNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  #### BuildDeferredIndexes[[c]](#cmnt3)[[d]](#cmnt4)

  Build Deferred builds all indexes which are currently in deferred state.

  Signature

  

  

  

  

  

  void BuildDeferredIndexes(string bucketName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   BucketName: string - name of the bucket.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   Any exceptions raised by the underlying platform
  *   InvalidArgumentsException

  

  # Search Index Manager

  The Search Index Manager interface contains the means for managing indexes used for search. Search index definitions are purposefully left very dynamic as the index definitions on the server are complex. As such it is left to each SDK to implement its own dynamic type for this, JSONObject is used here to signify that. Stability level is uncommited?

  

  

  

  

  

  

  public interface ISearchIndexManager{

  

          ISearchIndex GetIndex(string indexName, GetSearchIndexOptions options);

  

          Iterable GetAllIndexes(GetAllSearchIndexesOptions options);

  

           void UpsertIndex(ISearchIndex indexDefinition, UpsertSearchIndexOptions options);

  

          void DropIndex(string indexName, DropSearchIndexOptions options);

  

          int GetIndexedDocumentsCount(string indexName, GetIndexedSearchIndexOptions options);

  

          void PauseIngest(string indexName, PauseIngestSearchIndexOptions);

  

          void ResumeIngest(string indexName, ResumeIngestSearchIndexOptions);

  

          void AllowQuerying(string indexName, AllowQueryingSearchIndexOptions);

  

          void DisallowQuerying(string indexName, DisallowQueryingSearchIndexOptions);

  

          void FreezePlan(string indexName, FreezePlanSearchIndexOptions);

  

          void UnfreezePlan(string indexName, UnfreezePlanSearchIndexOptions);

  

             Iterable AnalyzeDocument(string indexName, JSONObject document, AnalyzeDocOptions options);

  }

  

  

  

  

  

  ### Methods

  The following methods must be implemented:

  #### GetIndex

  Fetches an index from the server if it exists.

  Signature

  

  

  

  

  

  ISearchIndex GetIndex(string indexName, [options])

  

  

  

  

  Parameters

  *   Required:

  *    IndexName: string - name of the index.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  An instance of ISearchIndex.

  Throws

  *   SearchIndexNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  Uri

  *   GET http://localhost:8094/api/index/

  #### GetAllIndexes

  Fetches all indexes from the server.

  Signature

  

  

  

  

  

  Iterable GetAllIndexes([options])

  

  

  

  

  Parameters

  *   Required:
  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  An array of ISearchIndex.

  Throws

  *   Any exceptions raised by the underlying platform

  Uri

  *   GET http://localhost:8094/api/index

  #### UpsertIndex

  Creates, or updates, an index. .

  Signature

  

  

  

  

  

  void UpsertIndex(ISearchIndex indexDefinition, [options])

  

  

  

  

  Parameters

  *   Required:

  *   indexDefinition: SearchIndex - the index definition

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   InvalidArgumentsException

  *   If any of the following are empty:

  *   Name
  *   Type
  *   SourceType

  *   Any exceptions raised by the underlying platform

  Uri

  *   PUT [http://localhost:8094/api/index/](https://www.google.com/url?q=http://localhost:8094/api/index/&sa=D&ust=1569855744339000)

  *   Should be sent with request header “cache-control” set to “no-cache”.

  #### DropIndex

  Drops an index.

  Signature

  

  

  

  

  

  void DropIndexstring indexName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   IndexName: string - name of the index.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   SearchIndexNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  Uri

  *   DELETE [http://localhost:8094/api/index/](https://www.google.com/url?q=http://localhost:8094/api/index/&sa=D&ust=1569855744343000)

  #### GetIndexedDocumentsCount

  Retrieves the number of documents that have been indexed for an index.

  Signature

  

  

  

  

  

  void GetIndexedDocumentsCount(string indexName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   IndexName: string - name of the index.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   SearchIndexNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  Uri

  *   GET [http://localhost:8094/api/index/](https://www.google.com/url?q=http://localhost:8094/api/index/&sa=D&ust=1569855744346000)/count

  #### PauseIngest

  Pauses updates and maintenance for an index.

  Signature

  

  

  

  

  

  void PauseIngest(string indexName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   IndexName: string - name of the index.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   SearchIndexNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  Uri

  *   POST /api/index/{indexName}/ingestControl/pause

  #### ResumeIngest

  Resumes updates and maintenance for an index.

  Signature

  

  

  

  

  

  void ResumeIngest(string indexName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   IndexName: string - name of the index.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   SearchIndexNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  Uri

  *   POST /api/index/{indexName}/ingestControl/resume

  #### AllowQuerying

  Allows querying against an index.

  Signature

  

  

  

  

  

  void AllowQuerying(string indexName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   IndexName: string - name of the index.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   SearchIndexNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  Uri

  *   POST /api/index/{indexName}/queryControl/allow

  #### DisallowQuerying

  Disallows querying against an index.

  Signature

  

  

  

  

  

  void DisallowQuerying(string indexName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   IndexName: string - name of the index.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   SearchIndexNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  Uri

  *   POST /api/index/{indexName}/queryControl/disallow

  #### FreezePlan

  Freeze the assignment of index partitions to nodes.

  Signature

  

  

  

  

  

  void FreezePlan(string indexName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   IndexName: string - name of the index.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   SearchIndexNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  Uri

  *   POST /api/index/{indexName}/planFreezeControl/freeze

  #### UnfreezePlan

  Unfreeze the assignment of index partitions to nodes.

  Signature

  

  

  

  

  

  void UnfreezePlan(string indexName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   IndexName: string - name of the index.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   SearchIndexNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  Uri

  *   POST /api/index/{indexName}/planFreezeControl/unfreeze

  

  #### AnalyzeDocument

  Allows users to see how a document is analyzed against a specific index.

  Signature

  

  

  

  

  

  Iterable AnalyzeDocument(string indexName, JSONObject document, [options])

  

  

  

  

  Parameters

  *   Required:

  *   IndexName: string - name of the index.
  *   Document: JSONObject - the document to be analyzed.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  An iterable of JSONObject. The response from the server returns an object containing two top level keys: status and analyzed. The SDK must return the value containing within the analyze key.

  Throws

  *   SearchIndexNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  Uri

  *   POST /api/index/{indexName}/analyzeDoc

  *   As of build mad hatter 3839

  # Analytics Index Manager

  Stability level is not volatile.

  

  

  

  

  

  

  public interface IAnalyticsIndexManager{

  

           void CreateDataverse(string dataverseName, CreateDataverseAnalyticsOptions options);

  

          void DropDataverse(string dataverseName, DropDataverseAnalyticsOptions options);

  

           void CreateDataset(string bucketName, string datasetName, CreateDatasetAnalyticsOptions options);

  

          void DropDataset(string datasetName, DropDatasetAnalyticsOptions options);

  

    Iterable GetAllDatasets(GetAllDatasetAnalyticsOptions options);

  

           void CreateIndex(string indexName, map[string]string fields, CreateIndexAnalyticsOptions options);

  

           void DropIndex(string datasetName, string indexName, DropIndexAnalyticsOptions options);

  

              Iterable GetAllIndexes(GetAllIndexesAnalyticsOptions options);

  

           void ConnectLink(string linkName, ConnectLinkAnalyticsOptions options);

  

           void DisconnectLink(string linkName, DisconnectLinkAnalyticsOptions options);

  

   map[string]int GetPendingMutations(GetPendingMutationsAnalyticsOptions options);

  }

  

  

  

  

  

  

  

  

  

  

  #### Create Dataverse

  Creates a new dataverse.

  Signature

  

  

  

  

  

  void CreateDataverse(string dataverseName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   dataverseName: string - name of the dataverse.

  *   Optional:

  *   IgnoreIfExists (bool) - ignore if the dataset already exists (send “IF NOT EXISTS” as part of the dataset creation query, e.g. CREATE DATAVERSE IF NOT EXISTS test ON default). Default to false.
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   DataverseAlreadyExistsException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  #### Drop Dataverse

  Drops a dataverse.

  Signature

  

  

  

  

  

  void DropDataverse(string dataverseName,  [options])

  

  

  

  

  Parameters

  *   Required:

  *   dataverseName: string - name of the dataverse.

  *   Optional:

  *   IgnoreIfNotExists (bool) - ignore if the dataset doesn’t exists (send “IF EXISTS” as part of the dataset creation query, e.g. DROP DATAVERSE IF EXISTS test).
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   DataverseNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  #### CreateDataset

  Creates a new dataset.

  Signature

  

  

  

  

  

  void CreateDataset(string datasetName, string bucketName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   datasetName: string - name of the dataset.
  *   bucketName: string - name of the bucket.

  *   Optional:

  *   IgnoreIfExists (bool) - ignore if the dataset already exists (send “IF NOT EXISTS” as part of the dataset creation query, e.g. CREATE DATASET IF NOT EXISTS test ON default).c
  *   Condition (string) - Where clause to use for creating dataset.
  *   DataverseName (string) - The name of the dataverse to use, default to none. If set then will be used as CREATE DATASET dataverseName.datasetName. If not set then will be CREATE DATASET datasetName.
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   DatasetAlreadyExistsException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  #### DropDataset

  Drops a dataset.

  Signature

  

  

  

  

  

  void DropDataset(string datasetName,  [options])

  

  

  

  

  Parameters

  *   Required:

  *   datasetName: string - name of the dataset.

  *   Optional:

  *   IgnoreIfNotExists (bool) - ignore if the dataset doesn’t exists (send “IF EXISTS” as part of the dataset creation query, e.g. DROP DATASET IF EXISTS test).
  *   DataverseName (string) - The name of the dataverse to use, default to none. If set then will be used as DROP DATASET dataverseName.datasetName. If not set then will be DROP DATASET datasetName.
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   DatasetNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  #### GetAllDatasets

  Gets all datasets (SELECT d.* FROM Metadata.`Dataset` d WHERE d.DataverseName  "Metadata").

  Signature

  

  

  

  

  

  Iterable GetAllDatasets([options])

  

  

  

  

  Parameters

  *   Required:
  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   Any exceptions raised by the underlying platform

  #### CreateIndex

  Creates a new index.

  Signature

  

  

  

  

  

  void CreateIndex(string indexName, string datasetName, map[string]string fields,  [options])

  

  

  

  

  Parameters

  *   Required:

  *   DatasetName: string - name of the dataset.
  *   IndexName: string - name of the index.
  *   fields: map[string]string - the fields to create the index over. This is a map of the name of the field to the type of the field.

  *   Optional:

  *   IgnoreIfExists (bool) - don’t error/throw if the index already exists. (send “IF NOT EXISTS” as part of the dataset creation query, e.g. CREATE INDEX test IF NOT EXISTS ON default) (Note: IF NOT EXISTS is not is in the same place as it is in CREATE DATASET)
  *   DataverseName (string) - The name of the dataverse to use, default to none. If set then will be used as CREATE INDEX dataverseName.datasetName.indexName. If not set then will be CREATE INDEX datasetName.indexName.
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.Returns
  *   

  *   AnalyticsIndexAlreadyExistsException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  #### DropIndex

  Drops an index.

  Throws

  Signature

  

  

  

  

  

  void DropIndex(string indexName, string datasetName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   IndexName: string - name of the index.

  *   Optional:

  *   IgnoreIfNotExists (bool) - Don’t error/throw if the index does not exist.
  *   DataverseName (string) - The name of the dataverse to use, default to none. If set then will be used as DROP INDEX dataverseName.datasetName.indexName. If not set then will be DROP INDEX datasetName.indexName.
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   AnalyticsIndexNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  #### GetAlIndexes

  Gets all indexes (SELECT d.* FROM Metadata.`Index` d WHERE d.DataverseName  “Metadata”).

  Signature

  

  

  

  

  

  Iterable GetAllIndexes([options])

  

  

  

  

  Parameters

  *   Required:
  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   Any exceptions raised by the underlying platform

  #### Connect Link

  Connects a link.

  Signature

  

  

  

  

  

  void ConnectLink([options])

  

  

  

  

  Parameters

  *   Required:
  *   Optional[[e]](#cmnt5)[[f]](#cmnt6)[[g]](#cmnt7)[[h]](#cmnt8):

  *   linkName: string - name of the link. Default to “Local”.
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   AnalyticsLinkNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  #### Disconnect Link

  Disconnects a link.

  Signature

  

  

  

  

  

  void DisconnectLink([options])

  

  

  

  

  Parameters

  *   Required:
  *   Optional:

  *   linkName: string - name of the link. Default to “Local”.
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   AnalyticsLinkNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  #### Get Pending Mutations

  Gets the pending mutations for all datasets. This is returned in the form of dataverse.dataset: mutations. E.g.:

  {

      "Default.travel": 20688,

      "Default.thing": 0,

      "Default.default": 0,

      "Notdefault.default": 0

  }

  Note that if a link is disconnected then it will return no results. If all links are disconnected then an empty object is returned.

  Signature

  

  

  

  

  

  map[string]int GetPendingMutations( [options])

  

  

  

  

  Parameters

  *   Required:
  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   Any exceptions raised by the underlying platform

  Uri

  *   GET http://localhost:8095/analytics/node/agg/stats/remaining

  # Bucket Manager

  

  

  

  

  

  

  public interface IBucketManager{

  

          void CreateBucket(CreateBucketSettings settings, CreateBucketOptions options);

  

          void UpdateBucket(BucketSettings settings, UpdateBucketOptions options);

  

          void DropBucket(string bucketName, DropBucketOptions options);

  

          BucketSettings GetBucket(string bucketName, GetBucketOptions options);

  

          Iterable GetAllBuckets(GetAllBucketOptions options);

  

              void FlushBucket(string bucketName, FlushBucketOptions options); // using the ns_server REST interface

  }

  

  

  

  

  

  #### CreateBucket

  Creates a new bucket.

  Signature

  

  

  

  

  

  void CreateBucket(CreateBucketSettings settings, [options])

  

  

  

  

  Parameters

  *   Required: BucketSettings - settings for the bucket.
  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   BucketAlreadyExistsException(http 400 and content contains "Bucket with given name already exists")
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  Uri

  *   POST [http://localhost:8092/pools/default/buckets](https://www.google.com/url?q=http://localhost:8092/pools/default/buckets&sa=D&ust=1569855744407000)

  #### UpdateBucket

  Updatesa bucket. In the docstring the SDK must include a section about how every setting must be set to what the user wants it to be after the update. Any settings that are not set to their desired values may be reverted to default values by the server.

  Signature

  

  

  

  

  

  void UpdateBucket(BucketSettings settings, [options])

  

  

  

  

  Parameters

  *   Required: BucketSettings - settings for the bucket.
  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   InvalidArgumentsException
  *   BucketDoesNotExistException
  *   Any exceptions raised by the underlying platform

  Uri

  *   POST http://localhost:8092/pools/default/buckets/

  #### DropBucket

  Removes a bucket.

  Signature

  

  

  

  

  

  void DropBucket(string bucketName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   bucketName: string - the name of the bucket.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   BucketNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  Uri

  *   DELETE http://localhost:8092/pools/default/buckets/

  #### GetBucket

  Gets a bucket’s settings.

  Signature

  

  

  

  

  

  BucketSettings GetBucket(bucketName string, [options])

  

  

  

  

  Parameters

  *   Required:

  *   bucketName: string - the name of the bucket.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  BucketSettings, settings for the bucket. Note: the ram quota returned is in bytes, not mb so requires x  / 1024 twice. Also Note: FlushEnabled is not a setting returned by the server, if flush is enabled then the doFlush endpoint will be listed and should be used to populate the field.

  Throws

  *   BucketNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  Uri

  *   GET http://localhost:8092/pools/default/buckets/

  #### GetAllBuckets

  Gets all bucket settings. Note: the ram quota returned is in bytes, not mb so requires x  / 1024 twice.

  Signature

  

  

  

  

  

  Iterable GetAllBuckets([options])

  

  

  

  

  Parameters

  *   Required:
  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  An iterable of settings for each bucket.

  Throws

  *   Any exceptions raised by the underlying platform

  Uri

  *   GET http://localhost:8092/pools/default/buckets

  #### FlushBucket

  Flushes a bucket (uses the ns_server REST interface).

  Signature

  

  

  

  

  

  void FlushBucket(string bucketName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   bucketName: string - the name of the bucket.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   BucketNotFoundException
  *   InvalidArgumentsException
  *   FlushDisabledException
  *   Any exceptions raised by the underlying platform

  Uri

  *   POST http://localhost:8092//pools/default/buckets//controller/doFlush

  # User Manager

  Programmatic access to the user management REST API:

  https://docs.couchbase.com/server/current/rest-api/rbac.html

  

  Unless otherwise indicated, all objects SHOULD be immutable.

  ### Role

  A role identifies a specific permission. CAVEAT: The properties of a role are likely to change with the introduction of collection-level permissions. Until then, here’s what the accessor methods look like:

  

  *   String name()
  *   Optional bucket()

  ### RoleAndDescription

  Associates a role with its name and description. This is additional information only present in the “list available roles” response.

  

  *   Role role()
  *   String displayName()
  *   String description()

  ### Origin

  Indicates why the user has a specific role. If the type is “user” it means the role is assigned directly to the user. If the type is “group” it means the role is inherited from the group identified by the “name” field.

  

  *   String type()
  *   Optional name()

  ### RoleAndOrigins

  Associates a role with its origins. This is how roles are returned by the “get user” and “get all users” responses.

  

  *   Role role()
  *   List origins()

  ### User

  Mutable. Models the user properties that may be updated via this API. All properties of the User class MUST have associated setters except for “username” which is fixed when the object is created.

  

  *   String username()
  *   String displayName()
  *   Set groups() - (names of the groups)
  *   Set roles() - only roles assigned directly to the user (not inherited from groups)
  *   String password() - From the user’s perspective the password property is “write-only”. The accessor SHOULD be hidden from the user and be visible only to the manager implementation.

  ### UserAndMetadata

  Models the “get user” / “get all users” response. Associates the mutable properties of a user with derived properties such as the effective roles inherited from groups.

  

  *   AuthDomain domain() - AuthDomain is an enumeration with values “local” and “external”. It MAY alternatively be represented as String.
  *   User user() - returns a new mutable User object each time this method is called. Modifying the fields of the returned User MUST have no effect on the UserAndMetadata object it came from.
  *   Set effectiveRoles() - all roles, regardless of origin.
  *   List effectiveRolesAndOrigins() - same as effectiveRoles, but with origin information included.
  *   Optional passwordChanged()
  *   Set externalGroups()

  ### Group

  Mutable. Defines a set of roles that may be inherited by users. All properties of the Group class MUST have associated setters except for “name” which is fixed when the object is created.

  

  *   String name()
  *   String description()
  *   Set roles() - [Role](#h.zhz0katumzwe) as defined in the User Manager section
  *   Optional ldapGroupReference()

  ## Service Interface

  

  

  

  

  

  

  public interface IUserManager{

  

          UserAndMetadata GetUser(string username, GetUserOptions options);

  

          Iterable GetAllUsers(GetAllUsersOptions options);

  

              void UpsertUser(User user, UpsertUserOptions options);

  

          void DropUser(string userName, DropUserOptions options);

  

          Iterable AvailableRoles(AvailableRolesOptions options);

  

          Group GetGroup(string groupName, GetGroupOptions options);

  

          Iterable GetAllGroups(GetAllGroupsOptions options);

  

              void UpsertGroup(Group group, UpsertGroupOptions options);

  

          void DropGroup(string groupName, DropGroupOptions options);

  }

  

  

  

  

  #### 

  #### GetUser

  Gets a user.

  Signature

  

  

  

  

  

  UserAndMetadata GetUser(string username, [options])

  

  

  

  

  Parameters

  *   Required:

  *   username: string - ID of the user.

  *   Optional:

  *   domainName: string - name of the user domain. Defaults to local.        
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  An instance of UserAndMetadata.

  Throws

  *   UserNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  

  Implementation Notes

  

  When parsing the “get” and “getAll” responses, take care to distinguish between roles assigned directly to the user (role origin with type=”user”) and roles inherited from groups (role origin with type=”group” and name=).

  

  If the server response does not include an “origins” field for a role, then it was generated by a server version prior to 6.5 and the SDK MUST treat the role as if it had a single origin of type=”user”.

  

  #### GetAllUsers

  Gets all users.

  Signature

  

  

  

  

  

  Iterable GetAllUsers([options])

  

  

  

  

  Parameters

  *   Required:
  *   Optional:

  *   domainName: string - name of the user domain. Defaults to local.
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  An iterable collection of UserAndMetadata.

  Throws

  *   Any exceptions raised by the underlying platform

  #### UpsertUser

  Creates or updates a user.

  Signature

  

  

  

  

  

  void UpsertUser(User user, [options])

  

  

  

  

  Parameters

  *   Required:

  *   user: User - the new version of the user.

  *   Optional:

  *   DomainName: string - name of the user domain (local | external). Defaults to local.
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  

  Implementation Notes

  

  When building the PUT request to send to the REST endpoint, implementations MUST omit the “password” property if it is not present in the given User domain object (so that the password is only changed if the calling code provided a new password).

  

  For backwards compatibility with Couchbase Server 6.0 and earlier, the “groups” parameter MUST be omitted if the group list is empty. Couchbase Server 6.5 treats the absent parameter the same as an explicit parameter with no value (removes any existing group associations, which is what we want in this case).

  

  #### DropUser

  Removes a user.

  Signature

  

  

  

  

  

  void DropUser(string username, [options])

  

  

  

  

  Parameters

  *   Required:

  *   username: string - ID of the user.

  *   Optional:

  *   DomainName: string - name of the user domain. Defaults to local.
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   UserNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  

  #### Available Roles

  Returns the roles supported by the server.

  Signature

  

  

  

  

  

  Iterable GetRoles([options])

  

  

  

  

  Parameters

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  An iterable collection of RoleAndDescription.

  Throws

  *   Any exceptions raised by the underlying platform

  

  #### GetGroup

  Gets a group.

  

  REST Endpoint: GET /settings/rbac/groups/

  Signature

  

  

  

  

  

  Group GetGroup(string groupName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   groupName: string - name of the group to get.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  An instance of Group.

  Throws

  *   GroupNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  

  #### GetAllGroups

  Gets all groups.

  

  REST Endpoint: GET /settings/rbac/groups

  Signature

  

  

  

  

  

  Iterable GetAllGroups([options])

  

  

  

  

  Parameters

  *   Required:
  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  An iterable collection of Group.

  Throws

  *   Any exceptions raised by the underlying platform

  #### UpsertGroup

  Creates or updates a group.

  

  REST Endpoint: PUT /settings/rbac/groups/

  This endpoint accepts application/x-www-form-urlencoded and requires the data be sent as form data. The name/id should not be included in the form data. Roles should be a comma separated list of strings. If, only if, the role contains a bucket name then the rolename should be suffixed with[] e.g. bucket_full_access[default],security_admin.

  Signature

  

  

  

  

  

  void UpsertGroup(Group group, [options])

  

  

  

  

  Parameters

  *   Required:

  *   group: Group - the new version of the group.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  

  #### DropGroup

  Removes a group.

  

  REST Endpoint: DELETE /settings/rbac/groups/

  Signature

  

  

  

  

  

  void DropGroup(string groupName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   groupName: string - name of the group.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   GroupNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  # Collections Manager

  Note: due to [https://issues.couchbase.com/browse/MB-35386](https://www.google.com/url?q=https://issues.couchbase.com/browse/MB-35386&sa=D&ust=1569855744460000) CollectionExists, ScopeExists, and GetScope must support both forms of the manifest until SDK beta. That is, going forward:

  

  {“uid”:“0",“scopes”:[{“name”:“_default”,“uid”:“0”,“collections”:[{“name”:“_default”,“uid”:“0"}]}]}

  

  And for the sake of support for the server beta which did not have the fix in place:

  {“uid”:0,“scopes”:{“_default”:{“uid”:0,“collections”:{“_default”:{“uid”:0}}}}}

  It is recommended to try to parse the first form and fallback to the second so that it can be easily removed later.

  

  

  

  

  

  

  public interface ICollectionManager{

  

              boolean CollectionExists(ICollectionSpec collection, CollectionExistsOptions options);

  

              boolean ScopeExists(string scopeName, ScopeExistsOptions options);

  

              IScopeSpec GetScope(string scopeName, GetScopeOptions options);

  

             Iterable GetAllScopes(GetAllScopesOptions options);

  

  void CreateCollection(ICollectionSpec collection, CreateCollectionOptions options);

  

          void DropCollection(ICollectionSpec collection, DropCollectionOptions options);

  

           void CreateScope(IScopeSpec scope, CreateScopeOptions options);[[i]](#cmnt9)[[j]](#cmnt10)

  

          void DropScope(string scopeName, DropScopeOptions options);

  

          void FlushCollection[[k]](#cmnt11)[[l]](#cmnt12)[[m]](#cmnt13)[[n]](#cmnt14)(ICollectionSpec collection, FlushCollectionOptions options);

  }

  

  

  

  

  

  

  

  

  

  

  #### Collection Exists

  Checks for existence of a collection. This will fetch a manifest and then interrogate it to check that the scope name exists and then that the collection name exists within that scope.

  Signature

  

  

  

  

  

  boolean CollectionExists(ICollectionSpec collection,  [options])

  

  

  

  

  Parameters

  *   Required:

  *   collection: ICollectionSpec - spec of the collection.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   Any exceptions raised by the underlying platform
  *   InvalidArgumentsException

  Uri

  *   GET /pools/default/buckets//collections

  #### Scope Exists

  Checks for existence of a scope. This will fetch a manifest and then interrogate it to check that the scope name exists.

  Signature

  

  

  

  

  

  boolean ScopeExists(String scopeName,  [options])

  

  

  

  

  Parameters

  *   Required:

  *   scopeName: string - name of the scope.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   Any exceptions raised by the underlying platform

  Uri

  *   GET /pools/default/buckets//collections

  #### Get Scope

  Gets a scope. This will fetch a manifest and then pull the scope out of it.

  Signature

  

  

  

  

  

  IScopeSpec GetScope(string scopeName,  [options])

  

  

  

  

  Parameters

  *   Required:

  *   scopeName: string - name of the scope.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   ScopeNotFoundException
  *   Any exceptions raised by the underlying platform

  Uri

  *   GET /pools/default/buckets//collections

  #### Get All Scopes

  Gets all scopes. This will fetch a manifest and then pull the scopes out of it.

  Signature

  

  

  

  

  

  iterable GetAllScopes([options])

  

  

  

  

  Parameters

  *   Required:
  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   Any exceptions raised by the underlying platform

  Uri

  *   GET /pools/default/buckets//collections

  #### Create Collection

  Creates a new collection.

  Signature

  

  

  

  

  

  void CreateCollection(CollectionSpec collection, [options])

  

  

  

  

  Parameters

  *   Required:

  *   collection: CollectionSpec - specification of the collection.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   InvalidArgumentsException
  *   CollectionAlreadyExistsException
  *   ScopeNotFoundException
  *   Any exceptions raised by the underlying platform

  Uri

  *   POST http://localhost:8091/pools/default/buckets//collections/ -d name=

  #### Drop Collection

  Removes a collection.

  Signature

  

  

  

  

  

  void DropCollection(ICollectionSpec collection, [options])

  

  

  

  

  Parameters

  *   Required:

  *   collection: ICollectionSpec - namspece of the collection.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   CollectionNotFoundException
  *   Any exceptions raised by the underlying platform

  Uri

  *   DELETE http://localhost:8091/pools/default/buckets//collections//

  #### Create Scope

  Creates a new scope.

  Signature

  

  

  

  

  

  Void CreateScope(string scopeName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   scopeName: String - name of the scope.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  Uri

  *   POST [http://localhost:8091/pools/default/buckets/](https://www.google.com/url?q=http://localhost:8091/pools/default/buckets/&sa=D&ust=1569855744485000)/collections -d name=

  #### Drop Scope

  Removes a scope.

  Signature

  

  

  

  

  

  void DropScope(string scopeName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   collectionName: string - name of the collection.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   ScopeNotFoundException
  *   Any exceptions raised by the underlying platform

  Uri

  *   DELETE [http://localhost:8091/pools/default/buckets/](https://www.google.com/url?q=http://localhost:8091/pools/default/buckets/&sa=D&ust=1569855744488000)/collections/

  # Types

  #### DesignDocument

  DesignDocument provides a means of mapping a design document into an object. It contains within it a map of View.

  

  

  

  

  

  

   type DesignDocument{

  

  String Name();

                  

          Map[String]IView Views();

  }

  

  

  

  

  

  #### View

  

  

  

  

  

   type View{

  

              String Map();

                  

              String Reduce();

  }

  

  

  

  

  ## 

  #### IQueryIndex Interface

  The IQueryIndex interface provides a means of mapping a query index into an object.

  

  

  

  

  

  

   interface IQueryIndex{

  

              String Name();

                  

          Bool IsPrimary();

  

          IndexType Type();

  

          String State();

  

          String Keyspace();

  

  Iterable IndexKey();

  

          Optional Condition();

  }

  

  

  

  

  

  #### AnalyticsDataset Interface

  AnalyticsDataset provides a means of mapping dataset details into an object.

  

  

  

  

  

  

   interface AnalyticsDataset{

  

              String Name();

                  

          String DataverseName();

                  

          String LinkName();

                  

          String BucketName();

  }

  

  

  

  

  #### AnalyticsIndex Interface

  AnalyticsIndex provides a means of mapping analytics index details into an object.

  

  

  

  

  

  

   interface AnalyticsDataset{

  

              String Name();

                  

          String DatasetName();

  

          String DataverseName();

                  

          Bool IsPrimary();

  }

  

  

  

  

  #### 

  #### BucketSettings

  BucketSettings provides a means of mapping bucket settings into an object.

  *   Name (string) - The name of the bucket.
  *   FlushEnabled (bool) - Whether or not flush should be enabled on the bucket. Default to false.
  *   RamQuotaMB (int) - Ram Quota in mb for the bucket. (rawRAM in the server payload)
  *   NumReplicas (int) - The number of replicas for documents.
  *   ReplicaIndexes (bool) - Whether replica indexes should be enabled for the bucket.
  *   BucketType {couchbase (sent on wire as membase), memcached, ephemeral} - The type of the bucket. Default to couchbase.
  *   EjectionMethod {fullEviction | valueOnly}. The eviction policy to use.
  *   maxTTL (int) - Value for the maxTTL of new documents created without a ttl.
  *   compressionMode {off | passive | active} - The compression mode to use.

  #### CreateBucketSettings

  CreateBucketSettings is a superset of BucketSettings providing one extra property:

  *   ConflictResolutionType {Timestamp (sent as lww) | SequenceNumber (sent as seqno)}. The conflict resolution type to use.

  The reasoning for this is that on Update ConflictResolutionType cannot be present in the JSON payload at all.

  

  #### UpsertIndeSearchIndex

  SearchIndex provides a means to map search indexes into object. The Params, SourceParams, and PlanParams fields are left to the SDK to decide what is idiomatic (e.g. JSONObject), the definitions of these fields is purposefully vague.

  

  

  

  

  

  type SearchIndex struct {

          // UUID is required for updates. It provides a means of ensuring consistency, the UUID must match the UUID value

          // for the index on the server.

          UUID string `json:"uuid"`

  

          Name string `json:"name"`

  

          // SourceName is the name of the source of the data for the index e.g. bucket name.

          SourceName string `json:"sourceName,omitempty"`

  

          // Type is the type of index, e.g. fulltext-index or fulltext-alias.

          Type string `json:"type"`

  

          // IndexParams are index properties such as store type and mappings.

          Params map[string]interface{} `json:"params"`

  

          // SourceUUID is the UUID of the data source, this can be used to more tightly tie the index to a source.

          SourceUUID string `json:"sourceUUID,omitempty"`

  

          // SourceParams are extra parameters to be defined. These are usually things like advanced connection and tuning

          // parameters.

          SourceParams map[string]interface{} `json:"sourceParams,omitempty"`

  

          // SourceType is the type of the data source, e.g. couchbase or nil depending on the Type field.

          SourceType string `json:"sourceType"`

  

          // PlanParams are plan properties such as number of replicas and number of partitions.

          PlanParams map[string]interface{} `json:"planParams,omitempty"`

  }

  

  

  

  

  

  

  #### IUser Interface

  The IUser interface provides a means of mapping user settings into an object.

  

  

  

  

  

  

   Interface IUser{

  

              String ID();

  

              String Name();

          

              Iterable Roles();

  }

  

  

  

  

  

  #### ICollectionSpec Interface

  

  

  

  

  

  

   Interface ICollectionSpec{

  

              String Name();

          

              String ScopeName();

  }

  

  

  

  

  

  #### IScopeSpec Interface

  

  

  

  

  

  

   Interface IScopeSpec{

  

              String Name();

          

              Iterable Collections();

  }

  

  

  

  

  

  

  

  

  # References

  *   Query index management

  *   [https://github.com/couchbaselabs/sdk-rfcs/blob/master/rfc/0003-indexmanagement.md](https://www.google.com/url?q=https://github.com/couchbaselabs/sdk-rfcs/blob/master/rfc/0003-indexmanagement.md&sa=D&ust=1569855744515000)
  *   [https://docs.couchbase.com/server/current/n1ql/n1ql-language-reference/](https://www.google.com/url?q=https://docs.couchbase.com/server/current/n1ql/n1ql-language-reference/&sa=D&ust=1569855744516000)

  *   Search index management

  *   [https://docs.google.com/document/d/1C4yfTj5u6ahRgk3ZIL_AkwPMeu9-hHY_lZcsDNeIP74](https://www.google.com/url?q=https://docs.google.com/document/d/1C4yfTj5u6ahRgk3ZIL_AkwPMeu9-hHY_lZcsDNeIP74&sa=D&ust=1569855744517000)
  *   [https://docs.couchbase.com/server/6.0/rest-api/rest-fts-indexing.html](https://www.google.com/url?q=https://docs.couchbase.com/server/6.0/rest-api/rest-fts-indexing.html&sa=D&ust=1569855744517000)
  *   [http://labs.couchbase.com/cbft/dev-guide/index-definitions/](https://www.google.com/url?q=http://labs.couchbase.com/cbft/dev-guide/index-definitions/&sa=D&ust=1569855744518000)

  *   Outdated but contains some useful definitions for fields.

  *   User Management

  *   [https://github.com/couchbaselabs/sdk-rfcs/blob/master/rfc/0022-usermgmt.md](https://www.google.com/url?q=https://github.com/couchbaselabs/sdk-rfcs/blob/master/rfc/0022-usermgmt.md&sa=D&ust=1569855744518000)

  *   Bucket Management

  *   [https://docs.couchbase.com/server/current/rest-api/rest-bucket-intro.html](https://www.google.com/url?q=https://docs.couchbase.com/server/current/rest-api/rest-bucket-intro.html&sa=D&ust=1569855744519000)

  *   Collection Management

  *   [https://github.com/couchbase/ns_server/commit/4c1a9ea20fbdb148f68ec2ad7be9eed4c071bf9e](https://www.google.com/url?q=https://github.com/couchbase/ns_server/commit/4c1a9ea20fbdb148f68ec2ad7be9eed4c071bf9e&sa=D&ust=1569855744519000)
  *   [https://docs.google.com/document/d/1X-v8GWQjplrMMaYwwWOzEuP4AUoDNIAvS39NmEjQ3_E/edit#heading=h.gprum229kohk](https://www.google.com/url?q=https://docs.google.com/document/d/1X-v8GWQjplrMMaYwwWOzEuP4AUoDNIAvS39NmEjQ3_E/edit%23heading%3Dh.gprum229kohk&sa=D&ust=1569855744520000)

  *   Views REST API

  *   [https://docs.couchbase.com/server/6.0/rest-api/rest-views-intro.html](https://www.google.com/url?q=https://docs.couchbase.com/server/6.0/rest-api/rest-views-intro.html&sa=D&ust=1569855744520000)

  *   Groups and LDAP Groups

  *   [https://docs.google.com/document/d/1wsjEmke80RW_sbW0ycS8yQl6rq5lzBbRWuelPZ1m9ZI/edit#](https://www.google.com/url?q=https://docs.google.com/document/d/1wsjEmke80RW_sbW0ycS8yQl6rq5lzBbRWuelPZ1m9ZI/edit%23&sa=D&ust=1569855744521000)
  *   [https://docs.google.com/document/d/1cFZOz9n6ZKyq_thxCSteuLrZ0rJEh7AMT3MFbOHCchM/edit](https://www.google.com/url?q=https://docs.google.com/document/d/1cFZOz9n6ZKyq_thxCSteuLrZ0rJEh7AMT3MFbOHCchM/edit&sa=D&ust=1569855744521000)
  *   [https://issues.couchbase.com/browse/MB-16035](https://www.google.com/url?q=https://issues.couchbase.com/browse/MB-16035&sa=D&ust=1569855744522000)

  *   Analytics management

  *   [https://docs.couchbase.com/server/current/analytics/5_ddl.html](https://www.google.com/url?q=https://docs.couchbase.com/server/current/analytics/5_ddl.html&sa=D&ust=1569855744522000)

  

  # Changes

  2019-09-30:

  *   Remove dataverse name checking from all Analytics options blocks so that if the dataverse name is set we do not check if the dataset already contains it.
  *   Added Condition to IQueryIndex.
  *   Changed User AvailableRoles to GetRoles.
  *   Change ConnectLink and DisconnectLink so that the name is optional, defaulting to Local.

  2019-09-18:

  *   Add FlushNotEnabledException to bucket Flush operation

  2019-09-03:

  *    Add numReplicas option to QueryIndexManager CreatePrimaryIndex

  

  [[a]](#cmnt_ref1)Java path-finding impl also has AND `using` = \"gsi\"

  

  

  [[b]](#cmnt_ref2)I believe this is from back in the very first versions of N1QL, where it was required to be specified.  I don't think we need to bring this behaviour forward.

  

  

  [[c]](#cmnt_ref3)Java impl does this by getting all indexes and doing BUILD INDEX on any currently set to deferred.  Thought we weren't doing racey stuff like that in client as general rule?

  

  

  [[d]](#cmnt_ref4)That wouldn't be racy, since your going to build exactly the indices that you find during the first call.  From a functional perspective, only indexes that were deferred at the time you called the method are being built, which I think makes sense.

  

  

  [[e]](#cmnt_ref5)+charles.dixon@couchbase.com Should there be an optional `dataverse` parameter?

  

  

  [[f]](#cmnt_ref6)And an optional `force` parameter?

  

  

  [[g]](#cmnt_ref7)I guess we should make an escape style of parameter to future proof it.

  

  

  [[h]](#cmnt_ref8)I don't think we need to have an escape hatch on something that only exists for ease of use.  Relatedly, why does CONNECT LINK even accept a dataverse name?

  

  

  [[i]](#cmnt_ref9)There is still a question around this, I suggest that we just accept a string Name rather than a ScopeSpec and we don't create collections as a part of this. It isn't attempting to be an atomic operation that way.

  

  

  [[j]](#cmnt_ref10)I would be in favour of this change.

  

  

  [[k]](#cmnt_ref11)This is missing the function definition below like the others.

  

  

  [[l]](#cmnt_ref12)There seems to be some confusion over what this command does. The collections design doc states that there will be a flush endpoint that we can call over REST. I don't believe that it's implemented by ns server yet though.

  

  

  [[m]](#cmnt_ref13)https://docs.google.com/document/d/1X-v8GWQjplrMMaYwwWOzEuP4AUoDNIAvS39NmEjQ3_E/edit#heading=h.8c7d3zbqy7i is what I'm referring to

  

  

  [[n]](#cmnt_ref14)Server-side flushing was not implemented, instead it was decided that flushing a collection could be achieved trivially by the SDK through the destruction and recreation of the collection.

  
  

  

  

  

  Parameters

  *   Required:

  *    designDocName: string - the name of the design document.
  *   namespace: enum - PRODUCTION if the user is requesting a document from the production namespace, or DEVELOPMENT if from the development namespace.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  An instance of DesignDocument.

  Throws

  *   DesignDocumentNotFoundException (http 404)
  *   Any exceptions raised by the underlying platform

  Uri

  *   GET http://localhost:8092//_design/

  Example response from server

  {  

     "views":{  

        "test":{  

           "map":"function (doc, meta) {\n\t\t\t\t\t\t  emit(meta.id, null);\n\t\t\t\t\t\t}",

           "reduce":"_count"

        }

     }

  }

  #### GetAllDesignDocuments

  Fetches all design documents from the server.

  ]

  When processing the server response, the client must strip the “_design/” prefix from the document ID (as well as the “_dev” prefix if present). For example, a doc.meta.id value of “_design/foo” must be parsed as “foo”, and “_design/dev_bar” must be parsed as “bar”.

  Signature

  

  

  

  

  

  Iterable GetAllDesignDocuments(DesignDocumentNamespace namespace, [options])

  

  

  

  

  Parameters

  *   Required:

  *   namespace (enum) - indicates whether the user wants to get production documents (PRODUCTION) or development documents (DEVELOPMENT).

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  An iterable of DesignDocument.

  Throws

  *   Any exceptions raised by the underlying platform

  Uri

  *   GET http://localhost:8091/pools/default/buckets//ddocs

  

  Example response from server

  {  

     "rows":[  

        {  

           "doc":{  

              "meta":{  

                 "id":"_design/dev_test",

                 "rev":"1-ae5e21ec"

              },

              "json":{  

                 "views":{  

                    "test":{  

                       "map":"function (doc, meta) {\n\t\t\t\t\t\t  emit(meta.id, null);\n\t\t\t\t\t\t}",

                       "reduce":"_count"

                    }

                 }

              }

           },

           "controllers":{  

              "compact":"/pools/default/buckets/default/ddocs/_design%2Fdev_test/controller/compactView",

              "setUpdateMinChanges":"/pools/default/buckets/default/ddocs/_design%2Fdev_test/controller/setUpdateMinChanges"

           }

        }

     ]

  }

  #### UpsertDesignDocument

  Updates, or inserts, a design document.

  Signature

  

  

  

  

  

  void UpsertDesignDocument(DesignDocument designDocData, DesignDocumentNamespace namespace, [options])

  

  

  

  

  Parameters

  *   Required:

  *   designDocData: DesignDocument - the data to use to create the design document
  *   namespace (enum) - indicates whether the user wants to upsert the document to the production namespace (PRODUCTION) or development namespace (DEVELOPMENT).

  *   Optional:

  *   
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   Any exceptions raised by the underlying platform

  Uri

  *   PUT http://localhost:8092//_design/

  #### DropDesignDocument

  Removes a design document.

  Signature

  

  

  

  

  

  void DropDesignDocument(string designDocName, DesignDocumentNamespace namespace,  [options])

  

  

  

  

  Parameters

  *   Required:

  *   designDocName: string - the name of the design document.
  *   namespace: enum - indicates whether the name refers to a production document (PRODUCTION) or a development document (DEVELOPMENT).

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   DesignDocumentNotFoundException (http 404)
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  Uri

  *   DELETE http://localhost:8092//_design/

  #### PublishDesignDocument

  Publishes a design document. This method is equivalent to getting a document from the development namespace and upserting it to the production namespace.

  Signature

  

  

  

  

  

  void PublishDesignDocument(string designDocName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   designDocName: string - the name of the development design document.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   DesignDocumentNotFoundException (http 404)
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  # Query Index Manager

  The Query Index Manager interface contains the means for managing indexes used for queries.

  

  

  

  

  

  

  

  public interface IQueryIndexManger{

  

          Iterable GetAllIndexes(string bucketName, GetAllQueryIndexOptions options);

  

  void CreateIndex(string bucketName, string indexName, []string fields, CreateQueryIndexOptions options);

  

             void CreatePrimaryIndex(string bucketName, CreatePrimaryQueryIndexOptions options);

  

          void DropIndex(string bucketName, string indexName, DropQueryIndexOptions options);

  

              void DropPrimaryIndex(string bucketName, DropPrimaryQueryIndexOptions options);

  

  void WatchIndexes(string bucketName, []string indexNames, timeout duration, WatchQueryIndexOptions options);

     

              void BuildDeferredIndexes(string bucketName, BuildQueryIndexOptions options);

  }

  

  

  

  

  

  ### Methods

  The following methods must be implemented:

  

  #### GetAllIndexes

  Fetches all indexes from the server.

  Signature

  

  

  

  

  

  Iterable GetAllIndexes(string bucketName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   BucketName: string - the name of the bucket.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  N1QL

  SELECT idx.* FROM system:indexes AS idx

      WHERE keyspace_id = "bucketName"

  [[a]](#cmnt1)[[b]](#cmnt2)

      ORDER BY is_primary DESC, name ASC

  Returns

  An array of IQueryIndex.

  Throws

  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  #### CreateIndex

  Creates a new index.

  Signature

  

  

  

  

  

  void CreateIndex(string bucketName, string indexName, []string fields,  [options])

  

  

  

  

  Parameters

  *   Required:

  *   BucketName: string - the name of the bucket.
  *   IndexName: string - the name of the index.
  *   fields: []string - the fields to create the index over.

  *   Optional:

  *   IgnoreIfExists (bool) - Don’t error/throw if the index already exists.
  *   NumReplicas (int) - The number of replicas that this index should have. Uses the WITH keyword and num_replica.

  *   CREATE INDEX indexNameON bucketName WITH { "num_replica": 2 }
  *   [https://docs.couchbase.com/server/current/n1ql/n1ql-language-reference/createindex.html](https://www.google.com/url?q=https://docs.couchbase.com/server/current/n1ql/n1ql-language-reference/createindex.html&sa=D&ust=1569855744308000)

  *   Deferred (bool) - Whether the index should be created as a deferred index.
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   IndexAlreadyExistsException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  #### CreatePrimaryIndex

  Creates a new primary index.

  Signature

  

  

  

  

  

  void CreatePrimaryIndex(string bucketName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   BucketName: string - name of the bucket.

  *   Optional:

  *   IndexName: string - name of the index.
  *   IgnoreIfExists (bool) - Don’t error/throw if the index already exists.
  *   NumReplicas (int) - The number of replicas that this index should have. Uses the WITH keyword and num_replica.

  *   CREATE INDEX indexNameON bucketName WITH { "num_replica": 2 }
  *   [https://docs.couchbase.com/server/current/n1ql/n1ql-language-reference/createindex.html](https://www.google.com/url?q=https://docs.couchbase.com/server/current/n1ql/n1ql-language-reference/createindex.html&sa=D&ust=1569855744311000)

  *   Deferred (bool) - Whether the index should be created as a deferred index.
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   QueryIndexAlreadyExistsException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  #### DropIndex

  Drops an index.

  Signature

  

  

  

  

  

  void DropIndex(string bucketName, string indexName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   BucketName: string - name of the bucket.
  *   IndexName: string - name of the index.

  *   Optional:

  *   IgnoreIfNotExists (bool) - Don’t error/throw if the index does not exist.
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   QueryIndexNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  #### DropPrimaryIndex

  Drops a primary index.

  Signature

  

  

  

  

  

  void DropPrimaryIndex(string bucketName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   BucketName: string - name of the bucket.

  *   Optional:

  *   IndexName: string - name of the index.
  *   IgnoreIfNotExists (bool) - Don’t error/throw if the index does not exist.
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   QueryIndexNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  #### WatchIndexes

  Watch polls indexes until they are online.

  Signature

  

  

  

  

  

  void WatchIndexes(string bucketName, []string indexNames, timeout duration, [options])

  

  

  

  

  Parameters

  *   Required:

  *   BucketName: string - name of the bucket.
  *   IndexName: []string - name(s) of the index(es).
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  *   Optional:

  *   WatchPrimary (bool) - whether or not to watch the primary index.

  Returns

  Throws

  *   QueryIndexNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  #### BuildDeferredIndexes[[c]](#cmnt3)[[d]](#cmnt4)

  Build Deferred builds all indexes which are currently in deferred state.

  Signature

  

  

  

  

  

  void BuildDeferredIndexes(string bucketName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   BucketName: string - name of the bucket.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   Any exceptions raised by the underlying platform
  *   InvalidArgumentsException

  

  # Search Index Manager

  The Search Index Manager interface contains the means for managing indexes used for search. Search index definitions are purposefully left very dynamic as the index definitions on the server are complex. As such it is left to each SDK to implement its own dynamic type for this, JSONObject is used here to signify that. Stability level is uncommited?

  

  

  

  

  

  

  public interface ISearchIndexManager{

  

          ISearchIndex GetIndex(string indexName, GetSearchIndexOptions options);

  

          Iterable GetAllIndexes(GetAllSearchIndexesOptions options);

  

           void UpsertIndex(ISearchIndex indexDefinition, UpsertSearchIndexOptions options);

  

          void DropIndex(string indexName, DropSearchIndexOptions options);

  

          int GetIndexedDocumentsCount(string indexName, GetIndexedSearchIndexOptions options);

  

          void PauseIngest(string indexName, PauseIngestSearchIndexOptions);

  

          void ResumeIngest(string indexName, ResumeIngestSearchIndexOptions);

  

          void AllowQuerying(string indexName, AllowQueryingSearchIndexOptions);

  

          void DisallowQuerying(string indexName, DisallowQueryingSearchIndexOptions);

  

          void FreezePlan(string indexName, FreezePlanSearchIndexOptions);

  

          void UnfreezePlan(string indexName, UnfreezePlanSearchIndexOptions);

  

             Iterable AnalyzeDocument(string indexName, JSONObject document, AnalyzeDocOptions options);

  }

  

  

  

  

  

  ### Methods

  The following methods must be implemented:

  #### GetIndex

  Fetches an index from the server if it exists.

  Signature

  

  

  

  

  

  ISearchIndex GetIndex(string indexName, [options])

  

  

  

  

  Parameters

  *   Required:

  *    IndexName: string - name of the index.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  An instance of ISearchIndex.

  Throws

  *   SearchIndexNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  Uri

  *   GET http://localhost:8094/api/index/

  #### GetAllIndexes

  Fetches all indexes from the server.

  Signature

  

  

  

  

  

  Iterable GetAllIndexes([options])

  

  

  

  

  Parameters

  *   Required:
  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  An array of ISearchIndex.

  Throws

  *   Any exceptions raised by the underlying platform

  Uri

  *   GET http://localhost:8094/api/index

  #### UpsertIndex

  Creates, or updates, an index. .

  Signature

  

  

  

  

  

  void UpsertIndex(ISearchIndex indexDefinition, [options])

  

  

  

  

  Parameters

  *   Required:

  *   indexDefinition: SearchIndex - the index definition

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   InvalidArgumentsException

  *   If any of the following are empty:

  *   Name
  *   Type
  *   SourceType

  *   Any exceptions raised by the underlying platform

  Uri

  *   PUT [http://localhost:8094/api/index/](https://www.google.com/url?q=http://localhost:8094/api/index/&sa=D&ust=1569855744339000)

  *   Should be sent with request header “cache-control” set to “no-cache”.

  #### DropIndex

  Drops an index.

  Signature

  

  

  

  

  

  void DropIndexstring indexName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   IndexName: string - name of the index.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   SearchIndexNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  Uri

  *   DELETE [http://localhost:8094/api/index/](https://www.google.com/url?q=http://localhost:8094/api/index/&sa=D&ust=1569855744343000)

  #### GetIndexedDocumentsCount

  Retrieves the number of documents that have been indexed for an index.

  Signature

  

  

  

  

  

  void GetIndexedDocumentsCount(string indexName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   IndexName: string - name of the index.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   SearchIndexNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  Uri

  *   GET [http://localhost:8094/api/index/](https://www.google.com/url?q=http://localhost:8094/api/index/&sa=D&ust=1569855744346000)/count

  #### PauseIngest

  Pauses updates and maintenance for an index.

  Signature

  

  

  

  

  

  void PauseIngest(string indexName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   IndexName: string - name of the index.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   SearchIndexNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  Uri

  *   POST /api/index/{indexName}/ingestControl/pause

  #### ResumeIngest

  Resumes updates and maintenance for an index.

  Signature

  

  

  

  

  

  void ResumeIngest(string indexName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   IndexName: string - name of the index.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   SearchIndexNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  Uri

  *   POST /api/index/{indexName}/ingestControl/resume

  #### AllowQuerying

  Allows querying against an index.

  Signature

  

  

  

  

  

  void AllowQuerying(string indexName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   IndexName: string - name of the index.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   SearchIndexNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  Uri

  *   POST /api/index/{indexName}/queryControl/allow

  #### DisallowQuerying

  Disallows querying against an index.

  Signature

  

  

  

  

  

  void DisallowQuerying(string indexName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   IndexName: string - name of the index.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   SearchIndexNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  Uri

  *   POST /api/index/{indexName}/queryControl/disallow

  #### FreezePlan

  Freeze the assignment of index partitions to nodes.

  Signature

  

  

  

  

  

  void FreezePlan(string indexName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   IndexName: string - name of the index.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   SearchIndexNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  Uri

  *   POST /api/index/{indexName}/planFreezeControl/freeze

  #### UnfreezePlan

  Unfreeze the assignment of index partitions to nodes.

  Signature

  

  

  

  

  

  void UnfreezePlan(string indexName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   IndexName: string - name of the index.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   SearchIndexNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  Uri

  *   POST /api/index/{indexName}/planFreezeControl/unfreeze

  

  #### AnalyzeDocument

  Allows users to see how a document is analyzed against a specific index.

  Signature

  

  

  

  

  

  Iterable AnalyzeDocument(string indexName, JSONObject document, [options])

  

  

  

  

  Parameters

  *   Required:

  *   IndexName: string - name of the index.
  *   Document: JSONObject - the document to be analyzed.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  An iterable of JSONObject. The response from the server returns an object containing two top level keys: status and analyzed. The SDK must return the value containing within the analyze key.

  Throws

  *   SearchIndexNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  Uri

  *   POST /api/index/{indexName}/analyzeDoc

  *   As of build mad hatter 3839

  # Analytics Index Manager

  Stability level is not volatile.

  

  

  

  

  

  

  public interface IAnalyticsIndexManager{

  

           void CreateDataverse(string dataverseName, CreateDataverseAnalyticsOptions options);

  

          void DropDataverse(string dataverseName, DropDataverseAnalyticsOptions options);

  

           void CreateDataset(string bucketName, string datasetName, CreateDatasetAnalyticsOptions options);

  

          void DropDataset(string datasetName, DropDatasetAnalyticsOptions options);

  

    Iterable GetAllDatasets(GetAllDatasetAnalyticsOptions options);

  

           void CreateIndex(string indexName, map[string]string fields, CreateIndexAnalyticsOptions options);

  

           void DropIndex(string datasetName, string indexName, DropIndexAnalyticsOptions options);

  

              Iterable GetAllIndexes(GetAllIndexesAnalyticsOptions options);

  

           void ConnectLink(string linkName, ConnectLinkAnalyticsOptions options);

  

           void DisconnectLink(string linkName, DisconnectLinkAnalyticsOptions options);

  

   map[string]int GetPendingMutations(GetPendingMutationsAnalyticsOptions options);

  }

  

  

  

  

  

  

  

  

  

  

  #### Create Dataverse

  Creates a new dataverse.

  Signature

  

  

  

  

  

  void CreateDataverse(string dataverseName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   dataverseName: string - name of the dataverse.

  *   Optional:

  *   IgnoreIfExists (bool) - ignore if the dataset already exists (send “IF NOT EXISTS” as part of the dataset creation query, e.g. CREATE DATAVERSE IF NOT EXISTS test ON default). Default to false.
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   DataverseAlreadyExistsException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  #### Drop Dataverse

  Drops a dataverse.

  Signature

  

  

  

  

  

  void DropDataverse(string dataverseName,  [options])

  

  

  

  

  Parameters

  *   Required:

  *   dataverseName: string - name of the dataverse.

  *   Optional:

  *   IgnoreIfNotExists (bool) - ignore if the dataset doesn’t exists (send “IF EXISTS” as part of the dataset creation query, e.g. DROP DATAVERSE IF EXISTS test).
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   DataverseNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  #### CreateDataset

  Creates a new dataset.

  Signature

  

  

  

  

  

  void CreateDataset(string datasetName, string bucketName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   datasetName: string - name of the dataset.
  *   bucketName: string - name of the bucket.

  *   Optional:

  *   IgnoreIfExists (bool) - ignore if the dataset already exists (send “IF NOT EXISTS” as part of the dataset creation query, e.g. CREATE DATASET IF NOT EXISTS test ON default).c
  *   Condition (string) - Where clause to use for creating dataset.
  *   DataverseName (string) - The name of the dataverse to use, default to none. If set then will be used as CREATE DATASET dataverseName.datasetName. If not set then will be CREATE DATASET datasetName.
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   DatasetAlreadyExistsException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  #### DropDataset

  Drops a dataset.

  Signature

  

  

  

  

  

  void DropDataset(string datasetName,  [options])

  

  

  

  

  Parameters

  *   Required:

  *   datasetName: string - name of the dataset.

  *   Optional:

  *   IgnoreIfNotExists (bool) - ignore if the dataset doesn’t exists (send “IF EXISTS” as part of the dataset creation query, e.g. DROP DATASET IF EXISTS test).
  *   DataverseName (string) - The name of the dataverse to use, default to none. If set then will be used as DROP DATASET dataverseName.datasetName. If not set then will be DROP DATASET datasetName.
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   DatasetNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  #### GetAllDatasets

  Gets all datasets (SELECT d.* FROM Metadata.`Dataset` d WHERE d.DataverseName  "Metadata").

  Signature

  

  

  

  

  

  Iterable GetAllDatasets([options])

  

  

  

  

  Parameters

  *   Required:
  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   Any exceptions raised by the underlying platform

  #### CreateIndex

  Creates a new index.

  Signature

  

  

  

  

  

  void CreateIndex(string indexName, string datasetName, map[string]string fields,  [options])

  

  

  

  

  Parameters

  *   Required:

  *   DatasetName: string - name of the dataset.
  *   IndexName: string - name of the index.
  *   fields: map[string]string - the fields to create the index over. This is a map of the name of the field to the type of the field.

  *   Optional:

  *   IgnoreIfExists (bool) - don’t error/throw if the index already exists. (send “IF NOT EXISTS” as part of the dataset creation query, e.g. CREATE INDEX test IF NOT EXISTS ON default) (Note: IF NOT EXISTS is not is in the same place as it is in CREATE DATASET)
  *   DataverseName (string) - The name of the dataverse to use, default to none. If set then will be used as CREATE INDEX dataverseName.datasetName.indexName. If not set then will be CREATE INDEX datasetName.indexName.
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.Returns
  *   

  *   AnalyticsIndexAlreadyExistsException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  #### DropIndex

  Drops an index.

  Throws

  Signature

  

  

  

  

  

  void DropIndex(string indexName, string datasetName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   IndexName: string - name of the index.

  *   Optional:

  *   IgnoreIfNotExists (bool) - Don’t error/throw if the index does not exist.
  *   DataverseName (string) - The name of the dataverse to use, default to none. If set then will be used as DROP INDEX dataverseName.datasetName.indexName. If not set then will be DROP INDEX datasetName.indexName.
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   AnalyticsIndexNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  #### GetAlIndexes

  Gets all indexes (SELECT d.* FROM Metadata.`Index` d WHERE d.DataverseName  “Metadata”).

  Signature

  

  

  

  

  

  Iterable GetAllIndexes([options])

  

  

  

  

  Parameters

  *   Required:
  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   Any exceptions raised by the underlying platform

  #### Connect Link

  Connects a link.

  Signature

  

  

  

  

  

  void ConnectLink([options])

  

  

  

  

  Parameters

  *   Required:
  *   Optional[[e]](#cmnt5)[[f]](#cmnt6)[[g]](#cmnt7)[[h]](#cmnt8):

  *   linkName: string - name of the link. Default to “Local”.
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   AnalyticsLinkNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  #### Disconnect Link

  Disconnects a link.

  Signature

  

  

  

  

  

  void DisconnectLink([options])

  

  

  

  

  Parameters

  *   Required:
  *   Optional:

  *   linkName: string - name of the link. Default to “Local”.
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   AnalyticsLinkNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  #### Get Pending Mutations

  Gets the pending mutations for all datasets. This is returned in the form of dataverse.dataset: mutations. E.g.:

  {

      "Default.travel": 20688,

      "Default.thing": 0,

      "Default.default": 0,

      "Notdefault.default": 0

  }

  Note that if a link is disconnected then it will return no results. If all links are disconnected then an empty object is returned.

  Signature

  

  

  

  

  

  map[string]int GetPendingMutations( [options])

  

  

  

  

  Parameters

  *   Required:
  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   Any exceptions raised by the underlying platform

  Uri

  *   GET http://localhost:8095/analytics/node/agg/stats/remaining

  # Bucket Manager

  

  

  

  

  

  

  public interface IBucketManager{

  

          void CreateBucket(CreateBucketSettings settings, CreateBucketOptions options);

  

          void UpdateBucket(BucketSettings settings, UpdateBucketOptions options);

  

          void DropBucket(string bucketName, DropBucketOptions options);

  

          BucketSettings GetBucket(string bucketName, GetBucketOptions options);

  

          Iterable GetAllBuckets(GetAllBucketOptions options);

  

              void FlushBucket(string bucketName, FlushBucketOptions options); // using the ns_server REST interface

  }

  

  

  

  

  

  #### CreateBucket

  Creates a new bucket.

  Signature

  

  

  

  

  

  void CreateBucket(CreateBucketSettings settings, [options])

  

  

  

  

  Parameters

  *   Required: BucketSettings - settings for the bucket.
  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   BucketAlreadyExistsException(http 400 and content contains "Bucket with given name already exists")
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  Uri

  *   POST [http://localhost:8092/pools/default/buckets](https://www.google.com/url?q=http://localhost:8092/pools/default/buckets&sa=D&ust=1569855744407000)

  #### UpdateBucket

  Updatesa bucket. In the docstring the SDK must include a section about how every setting must be set to what the user wants it to be after the update. Any settings that are not set to their desired values may be reverted to default values by the server.

  Signature

  

  

  

  

  

  void UpdateBucket(BucketSettings settings, [options])

  

  

  

  

  Parameters

  *   Required: BucketSettings - settings for the bucket.
  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   InvalidArgumentsException
  *   BucketDoesNotExistException
  *   Any exceptions raised by the underlying platform

  Uri

  *   POST http://localhost:8092/pools/default/buckets/

  #### DropBucket

  Removes a bucket.

  Signature

  

  

  

  

  

  void DropBucket(string bucketName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   bucketName: string - the name of the bucket.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   BucketNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  Uri

  *   DELETE http://localhost:8092/pools/default/buckets/

  #### GetBucket

  Gets a bucket’s settings.

  Signature

  

  

  

  

  

  BucketSettings GetBucket(bucketName string, [options])

  

  

  

  

  Parameters

  *   Required:

  *   bucketName: string - the name of the bucket.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  BucketSettings, settings for the bucket. Note: the ram quota returned is in bytes, not mb so requires x  / 1024 twice. Also Note: FlushEnabled is not a setting returned by the server, if flush is enabled then the doFlush endpoint will be listed and should be used to populate the field.

  Throws

  *   BucketNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  Uri

  *   GET http://localhost:8092/pools/default/buckets/

  #### GetAllBuckets

  Gets all bucket settings. Note: the ram quota returned is in bytes, not mb so requires x  / 1024 twice.

  Signature

  

  

  

  

  

  Iterable GetAllBuckets([options])

  

  

  

  

  Parameters

  *   Required:
  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  An iterable of settings for each bucket.

  Throws

  *   Any exceptions raised by the underlying platform

  Uri

  *   GET http://localhost:8092/pools/default/buckets

  #### FlushBucket

  Flushes a bucket (uses the ns_server REST interface).

  Signature

  

  

  

  

  

  void FlushBucket(string bucketName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   bucketName: string - the name of the bucket.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   BucketNotFoundException
  *   InvalidArgumentsException
  *   FlushDisabledException
  *   Any exceptions raised by the underlying platform

  Uri

  *   POST http://localhost:8092//pools/default/buckets//controller/doFlush

  # User Manager

  Programmatic access to the user management REST API:

  https://docs.couchbase.com/server/current/rest-api/rbac.html

  

  Unless otherwise indicated, all objects SHOULD be immutable.

  ### Role

  A role identifies a specific permission. CAVEAT: The properties of a role are likely to change with the introduction of collection-level permissions. Until then, here’s what the accessor methods look like:

  

  *   String name()
  *   Optional bucket()

  ### RoleAndDescription

  Associates a role with its name and description. This is additional information only present in the “list available roles” response.

  

  *   Role role()
  *   String displayName()
  *   String description()

  ### Origin

  Indicates why the user has a specific role. If the type is “user” it means the role is assigned directly to the user. If the type is “group” it means the role is inherited from the group identified by the “name” field.

  

  *   String type()
  *   Optional name()

  ### RoleAndOrigins

  Associates a role with its origins. This is how roles are returned by the “get user” and “get all users” responses.

  

  *   Role role()
  *   List origins()

  ### User

  Mutable. Models the user properties that may be updated via this API. All properties of the User class MUST have associated setters except for “username” which is fixed when the object is created.

  

  *   String username()
  *   String displayName()
  *   Set groups() - (names of the groups)
  *   Set roles() - only roles assigned directly to the user (not inherited from groups)
  *   String password() - From the user’s perspective the password property is “write-only”. The accessor SHOULD be hidden from the user and be visible only to the manager implementation.

  ### UserAndMetadata

  Models the “get user” / “get all users” response. Associates the mutable properties of a user with derived properties such as the effective roles inherited from groups.

  

  *   AuthDomain domain() - AuthDomain is an enumeration with values “local” and “external”. It MAY alternatively be represented as String.
  *   User user() - returns a new mutable User object each time this method is called. Modifying the fields of the returned User MUST have no effect on the UserAndMetadata object it came from.
  *   Set effectiveRoles() - all roles, regardless of origin.
  *   List effectiveRolesAndOrigins() - same as effectiveRoles, but with origin information included.
  *   Optional passwordChanged()
  *   Set externalGroups()

  ### Group

  Mutable. Defines a set of roles that may be inherited by users. All properties of the Group class MUST have associated setters except for “name” which is fixed when the object is created.

  

  *   String name()
  *   String description()
  *   Set roles() - [Role](#h.zhz0katumzwe) as defined in the User Manager section
  *   Optional ldapGroupReference()

  ## Service Interface

  

  

  

  

  

  

  public interface IUserManager{

  

          UserAndMetadata GetUser(string username, GetUserOptions options);

  

          Iterable GetAllUsers(GetAllUsersOptions options);

  

              void UpsertUser(User user, UpsertUserOptions options);

  

          void DropUser(string userName, DropUserOptions options);

  

          Iterable AvailableRoles(AvailableRolesOptions options);

  

          Group GetGroup(string groupName, GetGroupOptions options);

  

          Iterable GetAllGroups(GetAllGroupsOptions options);

  

              void UpsertGroup(Group group, UpsertGroupOptions options);

  

          void DropGroup(string groupName, DropGroupOptions options);

  }

  

  

  

  

  #### 

  #### GetUser

  Gets a user.

  Signature

  

  

  

  

  

  UserAndMetadata GetUser(string username, [options])

  

  

  

  

  Parameters

  *   Required:

  *   username: string - ID of the user.

  *   Optional:

  *   domainName: string - name of the user domain. Defaults to local.        
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  An instance of UserAndMetadata.

  Throws

  *   UserNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  

  Implementation Notes

  

  When parsing the “get” and “getAll” responses, take care to distinguish between roles assigned directly to the user (role origin with type=”user”) and roles inherited from groups (role origin with type=”group” and name=).

  

  If the server response does not include an “origins” field for a role, then it was generated by a server version prior to 6.5 and the SDK MUST treat the role as if it had a single origin of type=”user”.

  

  #### GetAllUsers

  Gets all users.

  Signature

  

  

  

  

  

  Iterable GetAllUsers([options])

  

  

  

  

  Parameters

  *   Required:
  *   Optional:

  *   domainName: string - name of the user domain. Defaults to local.
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  An iterable collection of UserAndMetadata.

  Throws

  *   Any exceptions raised by the underlying platform

  #### UpsertUser

  Creates or updates a user.

  Signature

  

  

  

  

  

  void UpsertUser(User user, [options])

  

  

  

  

  Parameters

  *   Required:

  *   user: User - the new version of the user.

  *   Optional:

  *   DomainName: string - name of the user domain (local | external). Defaults to local.
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  

  Implementation Notes

  

  When building the PUT request to send to the REST endpoint, implementations MUST omit the “password” property if it is not present in the given User domain object (so that the password is only changed if the calling code provided a new password).

  

  For backwards compatibility with Couchbase Server 6.0 and earlier, the “groups” parameter MUST be omitted if the group list is empty. Couchbase Server 6.5 treats the absent parameter the same as an explicit parameter with no value (removes any existing group associations, which is what we want in this case).

  

  #### DropUser

  Removes a user.

  Signature

  

  

  

  

  

  void DropUser(string username, [options])

  

  

  

  

  Parameters

  *   Required:

  *   username: string - ID of the user.

  *   Optional:

  *   DomainName: string - name of the user domain. Defaults to local.
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   UserNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  

  #### Available Roles

  Returns the roles supported by the server.

  Signature

  

  

  

  

  

  Iterable GetRoles([options])

  

  

  

  

  Parameters

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  An iterable collection of RoleAndDescription.

  Throws

  *   Any exceptions raised by the underlying platform

  

  #### GetGroup

  Gets a group.

  

  REST Endpoint: GET /settings/rbac/groups/

  Signature

  

  

  

  

  

  Group GetGroup(string groupName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   groupName: string - name of the group to get.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  An instance of Group.

  Throws

  *   GroupNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  

  #### GetAllGroups

  Gets all groups.

  

  REST Endpoint: GET /settings/rbac/groups

  Signature

  

  

  

  

  

  Iterable GetAllGroups([options])

  

  

  

  

  Parameters

  *   Required:
  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  An iterable collection of Group.

  Throws

  *   Any exceptions raised by the underlying platform

  #### UpsertGroup

  Creates or updates a group.

  

  REST Endpoint: PUT /settings/rbac/groups/

  This endpoint accepts application/x-www-form-urlencoded and requires the data be sent as form data. The name/id should not be included in the form data. Roles should be a comma separated list of strings. If, only if, the role contains a bucket name then the rolename should be suffixed with[] e.g. bucket_full_access[default],security_admin.

  Signature

  

  

  

  

  

  void UpsertGroup(Group group, [options])

  

  

  

  

  Parameters

  *   Required:

  *   group: Group - the new version of the group.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  

  #### DropGroup

  Removes a group.

  

  REST Endpoint: DELETE /settings/rbac/groups/

  Signature

  

  

  

  

  

  void DropGroup(string groupName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   groupName: string - name of the group.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   GroupNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  # Collections Manager

  Note: due to [https://issues.couchbase.com/browse/MB-35386](https://www.google.com/url?q=https://issues.couchbase.com/browse/MB-35386&sa=D&ust=1569855744460000) CollectionExists, ScopeExists, and GetScope must support both forms of the manifest until SDK beta. That is, going forward:

  

  {“uid”:“0",“scopes”:[{“name”:“_default”,“uid”:“0”,“collections”:[{“name”:“_default”,“uid”:“0"}]}]}

  

  And for the sake of support for the server beta which did not have the fix in place:

  {“uid”:0,“scopes”:{“_default”:{“uid”:0,“collections”:{“_default”:{“uid”:0}}}}}

  It is recommended to try to parse the first form and fallback to the second so that it can be easily removed later.

  

  

  

  

  

  

  public interface ICollectionManager{

  

              boolean CollectionExists(ICollectionSpec collection, CollectionExistsOptions options);

  

              boolean ScopeExists(string scopeName, ScopeExistsOptions options);

  

              IScopeSpec GetScope(string scopeName, GetScopeOptions options);

  

             Iterable GetAllScopes(GetAllScopesOptions options);

  

  void CreateCollection(ICollectionSpec collection, CreateCollectionOptions options);

  

          void DropCollection(ICollectionSpec collection, DropCollectionOptions options);

  

           void CreateScope(IScopeSpec scope, CreateScopeOptions options);[[i]](#cmnt9)[[j]](#cmnt10)

  

          void DropScope(string scopeName, DropScopeOptions options);

  

          void FlushCollection[[k]](#cmnt11)[[l]](#cmnt12)[[m]](#cmnt13)[[n]](#cmnt14)(ICollectionSpec collection, FlushCollectionOptions options);

  }

  

  

  

  

  

  

  

  

  

  

  #### Collection Exists

  Checks for existence of a collection. This will fetch a manifest and then interrogate it to check that the scope name exists and then that the collection name exists within that scope.

  Signature

  

  

  

  

  

  boolean CollectionExists(ICollectionSpec collection,  [options])

  

  

  

  

  Parameters

  *   Required:

  *   collection: ICollectionSpec - spec of the collection.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   Any exceptions raised by the underlying platform
  *   InvalidArgumentsException

  Uri

  *   GET /pools/default/buckets//collections

  #### Scope Exists

  Checks for existence of a scope. This will fetch a manifest and then interrogate it to check that the scope name exists.

  Signature

  

  

  

  

  

  boolean ScopeExists(String scopeName,  [options])

  

  

  

  

  Parameters

  *   Required:

  *   scopeName: string - name of the scope.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   Any exceptions raised by the underlying platform

  Uri

  *   GET /pools/default/buckets//collections

  #### Get Scope

  Gets a scope. This will fetch a manifest and then pull the scope out of it.

  Signature

  

  

  

  

  

  IScopeSpec GetScope(string scopeName,  [options])

  

  

  

  

  Parameters

  *   Required:

  *   scopeName: string - name of the scope.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   ScopeNotFoundException
  *   Any exceptions raised by the underlying platform

  Uri

  *   GET /pools/default/buckets//collections

  #### Get All Scopes

  Gets all scopes. This will fetch a manifest and then pull the scopes out of it.

  Signature

  

  

  

  

  

  iterable GetAllScopes([options])

  

  

  

  

  Parameters

  *   Required:
  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   Any exceptions raised by the underlying platform

  Uri

  *   GET /pools/default/buckets//collections

  #### Create Collection

  Creates a new collection.

  Signature

  

  

  

  

  

  void CreateCollection(CollectionSpec collection, [options])

  

  

  

  

  Parameters

  *   Required:

  *   collection: CollectionSpec - specification of the collection.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   InvalidArgumentsException
  *   CollectionAlreadyExistsException
  *   ScopeNotFoundException
  *   Any exceptions raised by the underlying platform

  Uri

  *   POST http://localhost:8091/pools/default/buckets//collections/ -d name=

  #### Drop Collection

  Removes a collection.

  Signature

  

  

  

  

  

  void DropCollection(ICollectionSpec collection, [options])

  

  

  

  

  Parameters

  *   Required:

  *   collection: ICollectionSpec - namspece of the collection.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   CollectionNotFoundException
  *   Any exceptions raised by the underlying platform

  Uri

  *   DELETE http://localhost:8091/pools/default/buckets//collections//

  #### Create Scope

  Creates a new scope.

  Signature

  

  

  

  

  

  Void CreateScope(string scopeName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   scopeName: String - name of the scope.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  Uri

  *   POST [http://localhost:8091/pools/default/buckets/](https://www.google.com/url?q=http://localhost:8091/pools/default/buckets/&sa=D&ust=1569855744485000)/collections -d name=

  #### Drop Scope

  Removes a scope.

  Signature

  

  

  

  

  

  void DropScope(string scopeName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   collectionName: string - name of the collection.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   ScopeNotFoundException
  *   Any exceptions raised by the underlying platform

  Uri

  *   DELETE [http://localhost:8091/pools/default/buckets/](https://www.google.com/url?q=http://localhost:8091/pools/default/buckets/&sa=D&ust=1569855744488000)/collections/

  # Types

  #### DesignDocument

  DesignDocument provides a means of mapping a design document into an object. It contains within it a map of View.

  

  

  

  

  

  

   type DesignDocument{

  

  String Name();

                  

          Map[String]IView Views();

  }

  

  

  

  

  

  #### View

  

  

  

  

  

   type View{

  

              String Map();

                  

              String Reduce();

  }

  

  

  

  

  ## 

  #### IQueryIndex Interface

  The IQueryIndex interface provides a means of mapping a query index into an object.

  

  

  

  

  

  

   interface IQueryIndex{

  

              String Name();

                  

          Bool IsPrimary();

  

          IndexType Type();

  

          String State();

  

          String Keyspace();

  

  Iterable IndexKey();

  

          Optional Condition();

  }

  

  

  

  

  

  #### AnalyticsDataset Interface

  AnalyticsDataset provides a means of mapping dataset details into an object.

  

  

  

  

  

  

   interface AnalyticsDataset{

  

              String Name();

                  

          String DataverseName();

                  

          String LinkName();

                  

          String BucketName();

  }

  

  

  

  

  #### AnalyticsIndex Interface

  AnalyticsIndex provides a means of mapping analytics index details into an object.

  

  

  

  

  

  

   interface AnalyticsDataset{

  

              String Name();

                  

          String DatasetName();

  

          String DataverseName();

                  

          Bool IsPrimary();

  }

  

  

  

  

  #### 

  #### BucketSettings

  BucketSettings provides a means of mapping bucket settings into an object.

  *   Name (string) - The name of the bucket.
  *   FlushEnabled (bool) - Whether or not flush should be enabled on the bucket. Default to false.
  *   RamQuotaMB (int) - Ram Quota in mb for the bucket. (rawRAM in the server payload)
  *   NumReplicas (int) - The number of replicas for documents.
  *   ReplicaIndexes (bool) - Whether replica indexes should be enabled for the bucket.
  *   BucketType {couchbase (sent on wire as membase), memcached, ephemeral} - The type of the bucket. Default to couchbase.
  *   EjectionMethod {fullEviction | valueOnly}. The eviction policy to use.
  *   maxTTL (int) - Value for the maxTTL of new documents created without a ttl.
  *   compressionMode {off | passive | active} - The compression mode to use.

  #### CreateBucketSettings

  CreateBucketSettings is a superset of BucketSettings providing one extra property:

  *   ConflictResolutionType {Timestamp (sent as lww) | SequenceNumber (sent as seqno)}. The conflict resolution type to use.

  The reasoning for this is that on Update ConflictResolutionType cannot be present in the JSON payload at all.

  

  #### UpsertIndeSearchIndex

  SearchIndex provides a means to map search indexes into object. The Params, SourceParams, and PlanParams fields are left to the SDK to decide what is idiomatic (e.g. JSONObject), the definitions of these fields is purposefully vague.

  

  

  

  

  

  type SearchIndex struct {

          // UUID is required for updates. It provides a means of ensuring consistency, the UUID must match the UUID value

          // for the index on the server.

          UUID string `json:"uuid"`

  

          Name string `json:"name"`

  

          // SourceName is the name of the source of the data for the index e.g. bucket name.

          SourceName string `json:"sourceName,omitempty"`

  

          // Type is the type of index, e.g. fulltext-index or fulltext-alias.

          Type string `json:"type"`

  

          // IndexParams are index properties such as store type and mappings.

          Params map[string]interface{} `json:"params"`

  

          // SourceUUID is the UUID of the data source, this can be used to more tightly tie the index to a source.

          SourceUUID string `json:"sourceUUID,omitempty"`

  

          // SourceParams are extra parameters to be defined. These are usually things like advanced connection and tuning

          // parameters.

          SourceParams map[string]interface{} `json:"sourceParams,omitempty"`

  

          // SourceType is the type of the data source, e.g. couchbase or nil depending on the Type field.

          SourceType string `json:"sourceType"`

  

          // PlanParams are plan properties such as number of replicas and number of partitions.

          PlanParams map[string]interface{} `json:"planParams,omitempty"`

  }

  

  

  

  

  

  

  #### IUser Interface

  The IUser interface provides a means of mapping user settings into an object.

  

  

  

  

  

  

   Interface IUser{

  

              String ID();

  

              String Name();

          

              Iterable Roles();

  }

  

  

  

  

  

  #### ICollectionSpec Interface

  

  

  

  

  

  

   Interface ICollectionSpec{

  

              String Name();

          

              String ScopeName();

  }

  

  

  

  

  

  #### IScopeSpec Interface

  

  

  

  

  

  

   Interface IScopeSpec{

  

              String Name();

          

              Iterable Collections();

  }

  

  

  

  

  

  

  

  

  # References

  *   Query index management

  *   [https://github.com/couchbaselabs/sdk-rfcs/blob/master/rfc/0003-indexmanagement.md](https://www.google.com/url?q=https://github.com/couchbaselabs/sdk-rfcs/blob/master/rfc/0003-indexmanagement.md&sa=D&ust=1569855744515000)
  *   [https://docs.couchbase.com/server/current/n1ql/n1ql-language-reference/](https://www.google.com/url?q=https://docs.couchbase.com/server/current/n1ql/n1ql-language-reference/&sa=D&ust=1569855744516000)

  *   Search index management

  *   [https://docs.google.com/document/d/1C4yfTj5u6ahRgk3ZIL_AkwPMeu9-hHY_lZcsDNeIP74](https://www.google.com/url?q=https://docs.google.com/document/d/1C4yfTj5u6ahRgk3ZIL_AkwPMeu9-hHY_lZcsDNeIP74&sa=D&ust=1569855744517000)
  *   [https://docs.couchbase.com/server/6.0/rest-api/rest-fts-indexing.html](https://www.google.com/url?q=https://docs.couchbase.com/server/6.0/rest-api/rest-fts-indexing.html&sa=D&ust=1569855744517000)
  *   [http://labs.couchbase.com/cbft/dev-guide/index-definitions/](https://www.google.com/url?q=http://labs.couchbase.com/cbft/dev-guide/index-definitions/&sa=D&ust=1569855744518000)

  *   Outdated but contains some useful definitions for fields.

  *   User Management

  *   [https://github.com/couchbaselabs/sdk-rfcs/blob/master/rfc/0022-usermgmt.md](https://www.google.com/url?q=https://github.com/couchbaselabs/sdk-rfcs/blob/master/rfc/0022-usermgmt.md&sa=D&ust=1569855744518000)

  *   Bucket Management

  *   [https://docs.couchbase.com/server/current/rest-api/rest-bucket-intro.html](https://www.google.com/url?q=https://docs.couchbase.com/server/current/rest-api/rest-bucket-intro.html&sa=D&ust=1569855744519000)

  *   Collection Management

  *   [https://github.com/couchbase/ns_server/commit/4c1a9ea20fbdb148f68ec2ad7be9eed4c071bf9e](https://www.google.com/url?q=https://github.com/couchbase/ns_server/commit/4c1a9ea20fbdb148f68ec2ad7be9eed4c071bf9e&sa=D&ust=1569855744519000)
  *   [https://docs.google.com/document/d/1X-v8GWQjplrMMaYwwWOzEuP4AUoDNIAvS39NmEjQ3_E/edit#heading=h.gprum229kohk](https://www.google.com/url?q=https://docs.google.com/document/d/1X-v8GWQjplrMMaYwwWOzEuP4AUoDNIAvS39NmEjQ3_E/edit%23heading%3Dh.gprum229kohk&sa=D&ust=1569855744520000)

  *   Views REST API

  *   [https://docs.couchbase.com/server/6.0/rest-api/rest-views-intro.html](https://www.google.com/url?q=https://docs.couchbase.com/server/6.0/rest-api/rest-views-intro.html&sa=D&ust=1569855744520000)

  *   Groups and LDAP Groups

  *   [https://docs.google.com/document/d/1wsjEmke80RW_sbW0ycS8yQl6rq5lzBbRWuelPZ1m9ZI/edit#](https://www.google.com/url?q=https://docs.google.com/document/d/1wsjEmke80RW_sbW0ycS8yQl6rq5lzBbRWuelPZ1m9ZI/edit%23&sa=D&ust=1569855744521000)
  *   [https://docs.google.com/document/d/1cFZOz9n6ZKyq_thxCSteuLrZ0rJEh7AMT3MFbOHCchM/edit](https://www.google.com/url?q=https://docs.google.com/document/d/1cFZOz9n6ZKyq_thxCSteuLrZ0rJEh7AMT3MFbOHCchM/edit&sa=D&ust=1569855744521000)
  *   [https://issues.couchbase.com/browse/MB-16035](https://www.google.com/url?q=https://issues.couchbase.com/browse/MB-16035&sa=D&ust=1569855744522000)

  *   Analytics management

  *   [https://docs.couchbase.com/server/current/analytics/5_ddl.html](https://www.google.com/url?q=https://docs.couchbase.com/server/current/analytics/5_ddl.html&sa=D&ust=1569855744522000)

  

  # Changes

  2019-09-30:

  *   Remove dataverse name checking from all Analytics options blocks so that if the dataverse name is set we do not check if the dataset already contains it.
  *   Added Condition to IQueryIndex.
  *   Changed User AvailableRoles to GetRoles.
  *   Change ConnectLink and DisconnectLink so that the name is optional, defaulting to Local.

  2019-09-18:

  *   Add FlushNotEnabledException to bucket Flush operation

  2019-09-03:

  *    Add numReplicas option to QueryIndexManager CreatePrimaryIndex

  

  [[a]](#cmnt_ref1)Java path-finding impl also has AND `using` = \"gsi\"

  

  

  [[b]](#cmnt_ref2)I believe this is from back in the very first versions of N1QL, where it was required to be specified.  I don't think we need to bring this behaviour forward.

  

  

  [[c]](#cmnt_ref3)Java impl does this by getting all indexes and doing BUILD INDEX on any currently set to deferred.  Thought we weren't doing racey stuff like that in client as general rule?

  

  

  [[d]](#cmnt_ref4)That wouldn't be racy, since your going to build exactly the indices that you find during the first call.  From a functional perspective, only indexes that were deferred at the time you called the method are being built, which I think makes sense.

  

  

  [[e]](#cmnt_ref5)+charles.dixon@couchbase.com Should there be an optional `dataverse` parameter?

  

  

  [[f]](#cmnt_ref6)And an optional `force` parameter?

  

  

  [[g]](#cmnt_ref7)I guess we should make an escape style of parameter to future proof it.

  

  

  [[h]](#cmnt_ref8)I don't think we need to have an escape hatch on something that only exists for ease of use.  Relatedly, why does CONNECT LINK even accept a dataverse name?

  

  

  [[i]](#cmnt_ref9)There is still a question around this, I suggest that we just accept a string Name rather than a ScopeSpec and we don't create collections as a part of this. It isn't attempting to be an atomic operation that way.

  

  

  [[j]](#cmnt_ref10)I would be in favour of this change.

  

  

  [[k]](#cmnt_ref11)This is missing the function definition below like the others.

  

  

  [[l]](#cmnt_ref12)There seems to be some confusion over what this command does. The collections design doc states that there will be a flush endpoint that we can call over REST. I don't believe that it's implemented by ns server yet though.

  

  
  SDK 3.0: Management APIs RFC

  SDK-RFC #54

  # Meta

  *   Name: SDK Management APIs
  *   RFC ID: 54
  *   Start-Date: 2019-06-13
  *   Owner: Charles Dixon
  *   Current Status: draft

  

  

  

  [Meta](#h.d61txvmb5lyx)

  [Summary](#h.mupne99cshsu)

  [Motivation](#h.fd9za96e3yg5)

  [General Design](#h.k3nh685gh3zd)

  [Service Not Configured](#h.fazo4li6zut4)

  [Feature Not Found](#h.g3sb6exbieep)

  [View Index Manager](#h.awf5c5g6sfub)

  [Methods](#h.ltp1wzfhvkmd)

  [GetDesignDocument](#h.9xwvwfmx35g1)

  [GetAllDesignDocuments](#h.3cni9ir8h3pd)

  [UpsertDesignDocument](#h.myqscrntq9od)

  [DropDesignDocument](#h.fejq3trrq88k)

  [PublishDesignDocument](#h.ytabqazgaibt)

  [Query Index Manager](#h.vor45gro2p0)

  [Methods](#h.vpcih9gceh5x)

  [GetAllIndexes](#h.d9bt9ug8rdnk)

  [CreateIndex](#h.25pbsjaw1r1t)

  [CreatePrimaryIndex](#h.i3nri1f7emcm)

  [DropIndex](#h.w5uphn3aj7a6)

  [DropPrimaryIndex](#h.8fkshrim697h)

  [WatchIndexes](#h.1jpy9kneh3ix)

  [BuildDeferredIndexes](#h.2g1b86t843xh)

  [Search Index Manager](#h.n72o3wjrgzcr)

  [Methods](#h.7ypleagc8f02)

  [GetIndex](#h.muduzks94csy)

  [GetAllIndexes](#h.rm7ralf543po)

  [UpsertIndex](#h.vojyv926dm9l)

  [DropIndex](#h.7kr1kyi2cud7)

  [GetIndexedDocumentsCount](#h.920wzxyyn8h0)

  [PauseIngest](#h.shct6uc5c13v)

  [ResumeIngest](#h.7b3my87vq187)

  [AllowQuerying](#h.3b0hek5e6cru)

  [DisallowQuerying](#h.burvg6qrwgc1)

  [FreezePlan](#h.xed0g6nk80ih)

  [UnfreezePlan](#h.o6413lybnsbd)

  [AnalyzeDocument](#h.slz9r181j64v)

  [Analytics Index Manager](#h.wey00euqxg6r)

  [Create Dataverse](#h.84qyvlkb4ct)

  [Drop Dataverse](#h.duuryzz83ji6)

  [CreateDataset](#h.p8q696h2j1c2)

  [DropDataset](#h.diqletr3ee8t)

  [GetAllDatasets](#h.yeup6dx0ca2i)

  [CreateIndex](#h.s2ix1a2i9750)

  [DropIndex](#h.sp8nw6p5hw3y)

  [GetAlIndexes](#h.gu1vgfz28b4q)

  [Connect Link](#h.urr6tlame907)

  [Disconnect Link](#h.f24cpp9is9ur)

  [Get Pending Mutations](#h.43ulyhfxecvc)

  [Bucket Manager](#h.a3jxd57mov7x)

  [CreateBucket](#h.7azm73gy346n)

  [UpdateBucket](#h.z6hp9xboxiox)

  [DropBucket](#h.40gpci3gs7n9)

  [GetBucket](#h.hsjjz8tpuhmp)

  [GetAllBuckets](#h.rxc15d7zi17u)

  [FlushBucket](#h.6lr2bzo2rpmg)

  [User Manager](#h.e1pyjdt66quk)

  [Role](#h.zhz0katumzwe)

  [RoleAndDescription](#h.dvcwkh4ud3go)

  [Origin](#h.n3o3qrb2hyz0)

  [RoleAndOrigins](#h.qxxi2pw80si1)

  [User](#h.3t1esyo2jmzd)

  [UserAndMetadata](#h.ra67vzjmec2v)

  [Group](#h.829b0i5yexun)

  [Service Interface](#h.kgjocyhklu1b)

  [GetUser](#h.1f3vxv6mfj2c)

  [GetAllUsers](#h.8jz0zts2uhqs)

  [UpsertUser](#h.dxc9109hkfhu)

  [DropUser](#h.it10rl3v5b78)

  [Available Roles](#h.orpyjhkf4za3)

  [GetGroup](#h.m6gv1571p3x2)

  [GetAllGroups](#h.h4uhsanhpfyb)

  [UpsertGroup](#h.35x8b5tnome6)

  [DropGroup](#h.bcaum5sclz6c)

  [Collections Manager](#h.8zfr25d06mmc)

  [Collection Exists](#h.jcy2l3znakl)

  [Scope Exists](#h.c30miu3maaya)

  [Get Scope](#h.y7nm7r1beg3i)

  [Get All Scopes](#h.w9ysz23ucxr9)

  [Create Collection](#h.v25764vsi0ze)

  [Drop Collection](#h.2nrt7s3vbsx9)

  [Create Scope](#h.80xchr7kse1x)

  [Drop Scope](#h.bzbzwqo5ea52)

  [Types](#h.hxsna6v0yga2)

  [DesignDocument](#h.h075tca0i0r9)

  [View](#h.ugcnslp1w79c)

  [IQueryIndex Interface](#h.yipr3bi8gyda)

  [AnalyticsDataset Interface](#h.t3sgseba5k26)

  [AnalyticsIndex Interface](#h.cd1vwisd9cvl)

  [BucketSettings](#h.bm3qgxw9689)

  [CreateBucketSettings](#h.um6jv51ydhmv)

  [SearchIndex](#h.w2u8bmxhvxn1)

  [IUser Interface](#h.gc7j9dg0shou)

  [ICollectionSpec Interface](#h.9moo4a588hua)

  [IScopeSpec Interface](#h.zfjuduk2ojhv)

  [References](#h.tatjn76gk22e)

  

  

  # Summary

  Defines the management APIs for SDK 3.0 that each SDK must implement.

  # Motivation

  

  # General Design

  The management APIs are made up of several interfaces; Bucket Manager, User Manager, Search Index Manager, View Index Manager, Query Index Manager, Analytics Index Manager, and Collection Manager.

  

  On the cluster interface:

  

  

  

  

  

  

  IUserManager Users();

  

  IBucketManager Buckets();

  

  IQueryIndexManager QueryIndexes();

  

  IAnalyticsIndexManager AnalyticsIndexes();

  

  

  

  

  ISearchIndexManager SearchIndexes();

  

  

  

  

  

  On the bucket interface:

  

  

  

  

  

  

  ICollectionManager Collections();

  

  

  

  

  IViewIndexManager ViewIndexes();

  

  

  

  

  

  # Service Not Configured

  If a manager is requested for a service which is not configured on the cluster then a ServiceNotConfiguredException must be raised. This can be detected by looking in the cluster config object, if the endpoint for the service has no servers listed then it is not configured.

  # Feature Not Found

  Some features, such as groups, certain functions, and collections are not supported on all server versions. If an endpoint is requested against a server version that does not support that endpoint then the HTTP response will be a 404 containing the body “Not Found.”. If this is returned then the SDK must return  a FeatureNotFoundException to the user.

  # View Index Manager

  The View Index Manager interface contains the means for managing design documents used for views.

  

  A design document belongs to either the “development” or “production” namespace. A development document has a name that starts with “dev_”. This is an implementation detail we’ve chosen to hide from consumers of this API. Document names presented to the user (returned from the “get” and “get all” methods, for example) always have the “dev_” prefix stripped.

  

  Whenever the user passes a design document name to any method of this API, the user may refer to the document using the “dev_” prefix regardless of whether the user is referring to a development document or production document. The “dev_” prefix is always stripped from user input, and the actual document name passed to the server is determined by the “namespace” argument..

  

  All methods (except publish) have a required “namespace” argument indicating whether the operation targets a development document or a production document. The type of this argument is an enum called DesignDocumentNamespace with values PRODUCTION and DEVELOPMENT.

  

  

  

  

  

  

  

  Interface IViewIndexManager {

  

          DesignDocumentGetDesignDocument(string designDocName, DesignDocumentNamespace namespace, GetDesignDocumentOptions options);

  

          Iterable GetAllDesignDocuments(DesignDocumentNamespace namespace, GetAllDesignDocumentsOptions options);

  

          void UpsertDesignDocument(DesignDocument indexData, DesignDocumentNamespace namespace, UpsertDesignDocumentOptions options);

  

          void DropDesignDocument(string designDocName, DesignDocumentNamespace namespace, DropDesignDocumentOptions options);

  

  

          void PublishDesignDocument(string designDocName, PublishDesignDocumentOptions options);

  }

  

  

  

  

  

  

  

  

  

  

  ### Methods

  The following methods must be implemented:

  #### GetDesignDocument

  Fetches a design document from the server if it exists.

  Signature

  

  

  

  

  

  DesignDocumentGetDesignDocument(string designDocName, DesignDocumentNamespace namespace, [options])
  SDK 3.0: Management APIs RFC

  SDK-RFC #54

  # Meta

  *   Name: SDK Management APIs
  *   RFC ID: 54
  *   Start-Date: 2019-06-13
  *   Owner: Charles Dixon
  *   Current Status: draft

  

  

  

  [Meta](#h.d61txvmb5lyx)

  [Summary](#h.mupne99cshsu)

  [Motivation](#h.fd9za96e3yg5)

  [General Design](#h.k3nh685gh3zd)

  [Service Not Configured](#h.fazo4li6zut4)

  [Feature Not Found](#h.g3sb6exbieep)

  [View Index Manager](#h.awf5c5g6sfub)

  [Methods](#h.ltp1wzfhvkmd)

  [GetDesignDocument](#h.9xwvwfmx35g1)

  [GetAllDesignDocuments](#h.3cni9ir8h3pd)

  [UpsertDesignDocument](#h.myqscrntq9od)

  [DropDesignDocument](#h.fejq3trrq88k)

  [PublishDesignDocument](#h.ytabqazgaibt)

  [Query Index Manager](#h.vor45gro2p0)

  [Methods](#h.vpcih9gceh5x)

  [GetAllIndexes](#h.d9bt9ug8rdnk)

  [CreateIndex](#h.25pbsjaw1r1t)

  [CreatePrimaryIndex](#h.i3nri1f7emcm)

  [DropIndex](#h.w5uphn3aj7a6)

  [DropPrimaryIndex](#h.8fkshrim697h)

  [WatchIndexes](#h.1jpy9kneh3ix)

  [BuildDeferredIndexes](#h.2g1b86t843xh)

  [Search Index Manager](#h.n72o3wjrgzcr)

  [Methods](#h.7ypleagc8f02)

  [GetIndex](#h.muduzks94csy)

  [GetAllIndexes](#h.rm7ralf543po)

  [UpsertIndex](#h.vojyv926dm9l)

  [DropIndex](#h.7kr1kyi2cud7)

  [GetIndexedDocumentsCount](#h.920wzxyyn8h0)

  [PauseIngest](#h.shct6uc5c13v)

  [ResumeIngest](#h.7b3my87vq187)

  [AllowQuerying](#h.3b0hek5e6cru)

  [DisallowQuerying](#h.burvg6qrwgc1)

  [FreezePlan](#h.xed0g6nk80ih)

  [UnfreezePlan](#h.o6413lybnsbd)

  [AnalyzeDocument](#h.slz9r181j64v)

  [Analytics Index Manager](#h.wey00euqxg6r)

  [Create Dataverse](#h.84qyvlkb4ct)

  [Drop Dataverse](#h.duuryzz83ji6)

  [CreateDataset](#h.p8q696h2j1c2)

  [DropDataset](#h.diqletr3ee8t)

  [GetAllDatasets](#h.yeup6dx0ca2i)

  [CreateIndex](#h.s2ix1a2i9750)

  [DropIndex](#h.sp8nw6p5hw3y)

  [GetAlIndexes](#h.gu1vgfz28b4q)

  [Connect Link](#h.urr6tlame907)

  [Disconnect Link](#h.f24cpp9is9ur)

  [Get Pending Mutations](#h.43ulyhfxecvc)

  [Bucket Manager](#h.a3jxd57mov7x)

  [CreateBucket](#h.7azm73gy346n)

  [UpdateBucket](#h.z6hp9xboxiox)

  [DropBucket](#h.40gpci3gs7n9)

  [GetBucket](#h.hsjjz8tpuhmp)

  [GetAllBuckets](#h.rxc15d7zi17u)

  [FlushBucket](#h.6lr2bzo2rpmg)

  [User Manager](#h.e1pyjdt66quk)

  [Role](#h.zhz0katumzwe)

  [RoleAndDescription](#h.dvcwkh4ud3go)

  [Origin](#h.n3o3qrb2hyz0)

  [RoleAndOrigins](#h.qxxi2pw80si1)

  [User](#h.3t1esyo2jmzd)

  [UserAndMetadata](#h.ra67vzjmec2v)

  [Group](#h.829b0i5yexun)

  [Service Interface](#h.kgjocyhklu1b)

  [GetUser](#h.1f3vxv6mfj2c)

  [GetAllUsers](#h.8jz0zts2uhqs)

  [UpsertUser](#h.dxc9109hkfhu)

  [DropUser](#h.it10rl3v5b78)

  [Available Roles](#h.orpyjhkf4za3)

  [GetGroup](#h.m6gv1571p3x2)

  [GetAllGroups](#h.h4uhsanhpfyb)

  [UpsertGroup](#h.35x8b5tnome6)

  [DropGroup](#h.bcaum5sclz6c)

  [Collections Manager](#h.8zfr25d06mmc)

  [Collection Exists](#h.jcy2l3znakl)

  [Scope Exists](#h.c30miu3maaya)

  [Get Scope](#h.y7nm7r1beg3i)

  [Get All Scopes](#h.w9ysz23ucxr9)

  [Create Collection](#h.v25764vsi0ze)

  [Drop Collection](#h.2nrt7s3vbsx9)

  [Create Scope](#h.80xchr7kse1x)

  [Drop Scope](#h.bzbzwqo5ea52)

  [Types](#h.hxsna6v0yga2)

  [DesignDocument](#h.h075tca0i0r9)

  [View](#h.ugcnslp1w79c)

  [IQueryIndex Interface](#h.yipr3bi8gyda)

  [AnalyticsDataset Interface](#h.t3sgseba5k26)

  [AnalyticsIndex Interface](#h.cd1vwisd9cvl)

  [BucketSettings](#h.bm3qgxw9689)

  [CreateBucketSettings](#h.um6jv51ydhmv)

  [SearchIndex](#h.w2u8bmxhvxn1)

  [IUser Interface](#h.gc7j9dg0shou)

  [ICollectionSpec Interface](#h.9moo4a588hua)

  [IScopeSpec Interface](#h.zfjuduk2ojhv)

  [References](#h.tatjn76gk22e)

  

  

  # Summary

  Defines the management APIs for SDK 3.0 that each SDK must implement.

  # Motivation

  

  # General Design

  The management APIs are made up of several interfaces; Bucket Manager, User Manager, Search Index Manager, View Index Manager, Query Index Manager, Analytics Index Manager, and Collection Manager.

  

  On the cluster interface:

  

  

  

  

  

  

  IUserManager Users();

  

  IBucketManager Buckets();

  

  IQueryIndexManager QueryIndexes();

  

  IAnalyticsIndexManager AnalyticsIndexes();

  

  

  

  

  ISearchIndexManager SearchIndexes();

  

  

  

  

  

  On the bucket interface:

  

  

  

  

  

  

  ICollectionManager Collections();

  

  

  

  

  IViewIndexManager ViewIndexes();

  

  

  

  

  

  # Service Not Configured

  If a manager is requested for a service which is not configured on the cluster then a ServiceNotConfiguredException must be raised. This can be detected by looking in the cluster config object, if the endpoint for the service has no servers listed then it is not configured.

  # Feature Not Found

  Some features, such as groups, certain functions, and collections are not supported on all server versions. If an endpoint is requested against a server version that does not support that endpoint then the HTTP response will be a 404 containing the body “Not Found.”. If this is returned then the SDK must return  a FeatureNotFoundException to the user.

  # View Index Manager

  The View Index Manager interface contains the means for managing design documents used for views.

  

  A design document belongs to either the “development” or “production” namespace. A development document has a name that starts with “dev_”. This is an implementation detail we’ve chosen to hide from consumers of this API. Document names presented to the user (returned from the “get” and “get all” methods, for example) always have the “dev_” prefix stripped.

  

  Whenever the user passes a design document name to any method of this API, the user may refer to the document using the “dev_” prefix regardless of whether the user is referring to a development document or production document. The “dev_” prefix is always stripped from user input, and the actual document name passed to the server is determined by the “namespace” argument..

  

  All methods (except publish) have a required “namespace” argument indicating whether the operation targets a development document or a production document. The type of this argument is an enum called DesignDocumentNamespace with values PRODUCTION and DEVELOPMENT.

  

  

  

  

  

  

  

  Interface IViewIndexManager {

  

          DesignDocumentGetDesignDocument(string designDocName, DesignDocumentNamespace namespace, GetDesignDocumentOptions options);

  

          Iterable GetAllDesignDocuments(DesignDocumentNamespace namespace, GetAllDesignDocumentsOptions options);

  

          void UpsertDesignDocument(DesignDocument indexData, DesignDocumentNamespace namespace, UpsertDesignDocumentOptions options);

  

          void DropDesignDocument(string designDocName, DesignDocumentNamespace namespace, DropDesignDocumentOptions options);

  

  

          void PublishDesignDocument(string designDocName, PublishDesignDocumentOptions options);

  }

  

  

  

  

  

  

  

  

  

  

  ### Methods

  The following methods must be implemented:

  #### GetDesignDocument

  Fetches a design document from the server if it exists.

  Signature

  

  

  

  

  

  DesignDocumentGetDesignDocument(string designDocName, DesignDocumentNamespace namespace, [options])

  

  

  

  

  Parameters

  *   Required:

  *    designDocName: string - the name of the design document.
  *   namespace: enum - PRODUCTION if the user is requesting a document from the production namespace, or DEVELOPMENT if from the development namespace.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  An instance of DesignDocument.

  Throws

  *   DesignDocumentNotFoundException (http 404)
  *   Any exceptions raised by the underlying platform

  Uri

  *   GET http://localhost:8092//_design/

  Example response from server

  {  

     "views":{  

        "test":{  

           "map":"function (doc, meta) {\n\t\t\t\t\t\t  emit(meta.id, null);\n\t\t\t\t\t\t}",

           "reduce":"_count"

        }

     }

  }

  #### GetAllDesignDocuments

  Fetches all design documents from the server.

  ]

  When processing the server response, the client must strip the “_design/” prefix from the document ID (as well as the “_dev” prefix if present). For example, a doc.meta.id value of “_design/foo” must be parsed as “foo”, and “_design/dev_bar” must be parsed as “bar”.

  Signature

  

  

  

  

  

  Iterable GetAllDesignDocuments(DesignDocumentNamespace namespace, [options])

  

  

  

  

  Parameters

  *   Required:

  *   namespace (enum) - indicates whether the user wants to get production documents (PRODUCTION) or development documents (DEVELOPMENT).

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  An iterable of DesignDocument.

  Throws

  *   Any exceptions raised by the underlying platform

  Uri

  *   GET http://localhost:8091/pools/default/buckets//ddocs

  

  Example response from server

  {  

     "rows":[  

        {  

           "doc":{  

              "meta":{  

                 "id":"_design/dev_test",

                 "rev":"1-ae5e21ec"

              },

              "json":{  

                 "views":{  

                    "test":{  

                       "map":"function (doc, meta) {\n\t\t\t\t\t\t  emit(meta.id, null);\n\t\t\t\t\t\t}",

                       "reduce":"_count"

                    }

                 }

              }

           },

           "controllers":{  

              "compact":"/pools/default/buckets/default/ddocs/_design%2Fdev_test/controller/compactView",

              "setUpdateMinChanges":"/pools/default/buckets/default/ddocs/_design%2Fdev_test/controller/setUpdateMinChanges"

           }

        }

     ]

  }

  #### UpsertDesignDocument

  Updates, or inserts, a design document.

  Signature

  

  

  

  

  

  void UpsertDesignDocument(DesignDocument designDocData, DesignDocumentNamespace namespace, [options])

  

  

  

  

  Parameters

  *   Required:

  *   designDocData: DesignDocument - the data to use to create the design document
  *   namespace (enum) - indicates whether the user wants to upsert the document to the production namespace (PRODUCTION) or development namespace (DEVELOPMENT).

  *   Optional:

  *   
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   Any exceptions raised by the underlying platform

  Uri

  *   PUT http://localhost:8092//_design/

  #### DropDesignDocument

  Removes a design document.

  Signature

  

  

  

  

  

  void DropDesignDocument(string designDocName, DesignDocumentNamespace namespace,  [options])

  

  

  

  

  Parameters

  *   Required:

  *   designDocName: string - the name of the design document.
  *   namespace: enum - indicates whether the name refers to a production document (PRODUCTION) or a development document (DEVELOPMENT).

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   DesignDocumentNotFoundException (http 404)
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  Uri

  *   DELETE http://localhost:8092//_design/

  #### PublishDesignDocument

  Publishes a design document. This method is equivalent to getting a document from the development namespace and upserting it to the production namespace.

  Signature

  

  

  

  

  

  void PublishDesignDocument(string designDocName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   designDocName: string - the name of the development design document.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   DesignDocumentNotFoundException (http 404)
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  # Query Index Manager

  The Query Index Manager interface contains the means for managing indexes used for queries.

  

  

  

  

  

  

  

  public interface IQueryIndexManger{

  

          Iterable GetAllIndexes(string bucketName, GetAllQueryIndexOptions options);

  

  void CreateIndex(string bucketName, string indexName, []string fields, CreateQueryIndexOptions options);

  

             void CreatePrimaryIndex(string bucketName, CreatePrimaryQueryIndexOptions options);

  

          void DropIndex(string bucketName, string indexName, DropQueryIndexOptions options);

  

              void DropPrimaryIndex(string bucketName, DropPrimaryQueryIndexOptions options);

  

  void WatchIndexes(string bucketName, []string indexNames, timeout duration, WatchQueryIndexOptions options);

     

              void BuildDeferredIndexes(string bucketName, BuildQueryIndexOptions options);

  }

  

  

  

  

  

  ### Methods

  The following methods must be implemented:

  

  #### GetAllIndexes

  Fetches all indexes from the server.

  Signature

  

  

  

  

  

  Iterable GetAllIndexes(string bucketName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   BucketName: string - the name of the bucket.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  N1QL

  SELECT idx.* FROM system:indexes AS idx

      WHERE keyspace_id = "bucketName"

  [[a]](#cmnt1)[[b]](#cmnt2)

      ORDER BY is_primary DESC, name ASC

  Returns

  An array of IQueryIndex.

  Throws

  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  #### CreateIndex

  Creates a new index.

  Signature

  

  

  

  

  

  void CreateIndex(string bucketName, string indexName, []string fields,  [options])

  

  

  

  

  Parameters

  *   Required:

  *   BucketName: string - the name of the bucket.
  *   IndexName: string - the name of the index.
  *   fields: []string - the fields to create the index over.

  *   Optional:

  *   IgnoreIfExists (bool) - Don’t error/throw if the index already exists.
  *   NumReplicas (int) - The number of replicas that this index should have. Uses the WITH keyword and num_replica.

  *   CREATE INDEX indexNameON bucketName WITH { "num_replica": 2 }
  *   [https://docs.couchbase.com/server/current/n1ql/n1ql-language-reference/createindex.html](https://www.google.com/url?q=https://docs.couchbase.com/server/current/n1ql/n1ql-language-reference/createindex.html&sa=D&ust=1569855744308000)

  *   Deferred (bool) - Whether the index should be created as a deferred index.
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   IndexAlreadyExistsException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  #### CreatePrimaryIndex

  Creates a new primary index.

  Signature

  

  

  

  

  

  void CreatePrimaryIndex(string bucketName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   BucketName: string - name of the bucket.

  *   Optional:

  *   IndexName: string - name of the index.
  *   IgnoreIfExists (bool) - Don’t error/throw if the index already exists.
  *   NumReplicas (int) - The number of replicas that this index should have. Uses the WITH keyword and num_replica.

  *   CREATE INDEX indexNameON bucketName WITH { "num_replica": 2 }
  *   [https://docs.couchbase.com/server/current/n1ql/n1ql-language-reference/createindex.html](https://www.google.com/url?q=https://docs.couchbase.com/server/current/n1ql/n1ql-language-reference/createindex.html&sa=D&ust=1569855744311000)

  *   Deferred (bool) - Whether the index should be created as a deferred index.
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   QueryIndexAlreadyExistsException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  #### DropIndex

  Drops an index.

  Signature

  

  

  

  

  

  void DropIndex(string bucketName, string indexName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   BucketName: string - name of the bucket.
  *   IndexName: string - name of the index.

  *   Optional:

  *   IgnoreIfNotExists (bool) - Don’t error/throw if the index does not exist.
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   QueryIndexNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  #### DropPrimaryIndex

  Drops a primary index.

  Signature

  

  

  

  

  

  void DropPrimaryIndex(string bucketName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   BucketName: string - name of the bucket.

  *   Optional:

  *   IndexName: string - name of the index.
  *   IgnoreIfNotExists (bool) - Don’t error/throw if the index does not exist.
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   QueryIndexNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  #### WatchIndexes

  Watch polls indexes until they are online.

  Signature

  

  

  

  

  

  void WatchIndexes(string bucketName, []string indexNames, timeout duration, [options])

  

  

  

  

  Parameters

  *   Required:

  *   BucketName: string - name of the bucket.
  *   IndexName: []string - name(s) of the index(es).
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  *   Optional:

  *   WatchPrimary (bool) - whether or not to watch the primary index.

  Returns

  Throws

  *   QueryIndexNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  #### BuildDeferredIndexes[[c]](#cmnt3)[[d]](#cmnt4)

  Build Deferred builds all indexes which are currently in deferred state.

  Signature

  

  

  

  

  

  void BuildDeferredIndexes(string bucketName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   BucketName: string - name of the bucket.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   Any exceptions raised by the underlying platform
  *   InvalidArgumentsException

  

  # Search Index Manager

  The Search Index Manager interface contains the means for managing indexes used for search. Search index definitions are purposefully left very dynamic as the index definitions on the server are complex. As such it is left to each SDK to implement its own dynamic type for this, JSONObject is used here to signify that. Stability level is uncommited?

  

  

  

  

  

  

  public interface ISearchIndexManager{

  

          ISearchIndex GetIndex(string indexName, GetSearchIndexOptions options);

  

          Iterable GetAllIndexes(GetAllSearchIndexesOptions options);

  

           void UpsertIndex(ISearchIndex indexDefinition, UpsertSearchIndexOptions options);

  

          void DropIndex(string indexName, DropSearchIndexOptions options);

  

          int GetIndexedDocumentsCount(string indexName, GetIndexedSearchIndexOptions options);

  

          void PauseIngest(string indexName, PauseIngestSearchIndexOptions);

  

          void ResumeIngest(string indexName, ResumeIngestSearchIndexOptions);

  

          void AllowQuerying(string indexName, AllowQueryingSearchIndexOptions);

  

          void DisallowQuerying(string indexName, DisallowQueryingSearchIndexOptions);

  

          void FreezePlan(string indexName, FreezePlanSearchIndexOptions);

  

          void UnfreezePlan(string indexName, UnfreezePlanSearchIndexOptions);

  

             Iterable AnalyzeDocument(string indexName, JSONObject document, AnalyzeDocOptions options);

  }

  

  

  

  

  

  ### Methods

  The following methods must be implemented:

  #### GetIndex

  Fetches an index from the server if it exists.

  Signature

  

  

  

  

  

  ISearchIndex GetIndex(string indexName, [options])

  

  

  

  

  Parameters

  *   Required:

  *    IndexName: string - name of the index.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  An instance of ISearchIndex.

  Throws

  *   SearchIndexNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  Uri

  *   GET http://localhost:8094/api/index/

  #### GetAllIndexes

  Fetches all indexes from the server.

  Signature

  

  

  

  

  

  Iterable GetAllIndexes([options])

  

  

  

  

  Parameters

  *   Required:
  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  An array of ISearchIndex.

  Throws

  *   Any exceptions raised by the underlying platform

  Uri

  *   GET http://localhost:8094/api/index

  #### UpsertIndex

  Creates, or updates, an index. .

  Signature

  

  

  

  

  

  void UpsertIndex(ISearchIndex indexDefinition, [options])

  

  

  

  

  Parameters

  *   Required:

  *   indexDefinition: SearchIndex - the index definition

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   InvalidArgumentsException

  *   If any of the following are empty:

  *   Name
  *   Type
  *   SourceType

  *   Any exceptions raised by the underlying platform

  Uri

  *   PUT [http://localhost:8094/api/index/](https://www.google.com/url?q=http://localhost:8094/api/index/&sa=D&ust=1569855744339000)

  *   Should be sent with request header “cache-control” set to “no-cache”.

  #### DropIndex

  Drops an index.

  Signature

  

  

  

  

  

  void DropIndexstring indexName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   IndexName: string - name of the index.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   SearchIndexNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  Uri

  *   DELETE [http://localhost:8094/api/index/](https://www.google.com/url?q=http://localhost:8094/api/index/&sa=D&ust=1569855744343000)

  #### GetIndexedDocumentsCount

  Retrieves the number of documents that have been indexed for an index.

  Signature

  

  

  

  

  

  void GetIndexedDocumentsCount(string indexName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   IndexName: string - name of the index.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   SearchIndexNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  Uri

  *   GET [http://localhost:8094/api/index/](https://www.google.com/url?q=http://localhost:8094/api/index/&sa=D&ust=1569855744346000)/count

  #### PauseIngest

  Pauses updates and maintenance for an index.

  Signature

  

  

  

  

  

  void PauseIngest(string indexName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   IndexName: string - name of the index.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   SearchIndexNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  Uri

  *   POST /api/index/{indexName}/ingestControl/pause

  #### ResumeIngest

  Resumes updates and maintenance for an index.

  Signature

  

  

  

  

  

  void ResumeIngest(string indexName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   IndexName: string - name of the index.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   SearchIndexNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  Uri

  *   POST /api/index/{indexName}/ingestControl/resume

  #### AllowQuerying

  Allows querying against an index.

  Signature

  

  

  

  

  

  void AllowQuerying(string indexName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   IndexName: string - name of the index.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   SearchIndexNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  Uri

  *   POST /api/index/{indexName}/queryControl/allow

  #### DisallowQuerying

  Disallows querying against an index.

  Signature

  

  

  

  

  

  void DisallowQuerying(string indexName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   IndexName: string - name of the index.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   SearchIndexNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  Uri

  *   POST /api/index/{indexName}/queryControl/disallow

  #### FreezePlan

  Freeze the assignment of index partitions to nodes.

  Signature

  

  

  

  

  

  void FreezePlan(string indexName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   IndexName: string - name of the index.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   SearchIndexNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  Uri

  *   POST /api/index/{indexName}/planFreezeControl/freeze

  #### UnfreezePlan

  Unfreeze the assignment of index partitions to nodes.

  Signature

  

  

  

  

  

  void UnfreezePlan(string indexName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   IndexName: string - name of the index.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   SearchIndexNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  Uri

  *   POST /api/index/{indexName}/planFreezeControl/unfreeze

  

  #### AnalyzeDocument

  Allows users to see how a document is analyzed against a specific index.

  Signature

  

  

  

  

  

  Iterable AnalyzeDocument(string indexName, JSONObject document, [options])

  

  

  

  

  Parameters

  *   Required:

  *   IndexName: string - name of the index.
  *   Document: JSONObject - the document to be analyzed.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  An iterable of JSONObject. The response from the server returns an object containing two top level keys: status and analyzed. The SDK must return the value containing within the analyze key.

  Throws

  *   SearchIndexNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  Uri

  *   POST /api/index/{indexName}/analyzeDoc

  *   As of build mad hatter 3839

  # Analytics Index Manager

  Stability level is not volatile.

  

  

  

  

  

  

  public interface IAnalyticsIndexManager{

  

           void CreateDataverse(string dataverseName, CreateDataverseAnalyticsOptions options);

  

          void DropDataverse(string dataverseName, DropDataverseAnalyticsOptions options);

  

           void CreateDataset(string bucketName, string datasetName, CreateDatasetAnalyticsOptions options);

  

          void DropDataset(string datasetName, DropDatasetAnalyticsOptions options);

  

    Iterable GetAllDatasets(GetAllDatasetAnalyticsOptions options);

  

           void CreateIndex(string indexName, map[string]string fields, CreateIndexAnalyticsOptions options);

  

           void DropIndex(string datasetName, string indexName, DropIndexAnalyticsOptions options);

  

              Iterable GetAllIndexes(GetAllIndexesAnalyticsOptions options);

  

           void ConnectLink(string linkName, ConnectLinkAnalyticsOptions options);

  

           void DisconnectLink(string linkName, DisconnectLinkAnalyticsOptions options);

  

   map[string]int GetPendingMutations(GetPendingMutationsAnalyticsOptions options);

  }

  

  

  

  

  

  

  

  

  

  

  #### Create Dataverse

  Creates a new dataverse.

  Signature

  

  

  

  

  

  void CreateDataverse(string dataverseName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   dataverseName: string - name of the dataverse.

  *   Optional:

  *   IgnoreIfExists (bool) - ignore if the dataset already exists (send “IF NOT EXISTS” as part of the dataset creation query, e.g. CREATE DATAVERSE IF NOT EXISTS test ON default). Default to false.
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   DataverseAlreadyExistsException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  #### Drop Dataverse

  Drops a dataverse.

  Signature

  

  

  

  

  

  void DropDataverse(string dataverseName,  [options])

  

  

  

  

  Parameters

  *   Required:

  *   dataverseName: string - name of the dataverse.

  *   Optional:

  *   IgnoreIfNotExists (bool) - ignore if the dataset doesn’t exists (send “IF EXISTS” as part of the dataset creation query, e.g. DROP DATAVERSE IF EXISTS test).
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   DataverseNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  #### CreateDataset

  Creates a new dataset.

  Signature

  

  

  

  

  

  void CreateDataset(string datasetName, string bucketName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   datasetName: string - name of the dataset.
  *   bucketName: string - name of the bucket.

  *   Optional:

  *   IgnoreIfExists (bool) - ignore if the dataset already exists (send “IF NOT EXISTS” as part of the dataset creation query, e.g. CREATE DATASET IF NOT EXISTS test ON default).c
  *   Condition (string) - Where clause to use for creating dataset.
  *   DataverseName (string) - The name of the dataverse to use, default to none. If set then will be used as CREATE DATASET dataverseName.datasetName. If not set then will be CREATE DATASET datasetName.
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   DatasetAlreadyExistsException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  #### DropDataset

  Drops a dataset.

  Signature

  

  

  

  

  

  void DropDataset(string datasetName,  [options])

  

  

  

  

  Parameters

  *   Required:

  *   datasetName: string - name of the dataset.

  *   Optional:

  *   IgnoreIfNotExists (bool) - ignore if the dataset doesn’t exists (send “IF EXISTS” as part of the dataset creation query, e.g. DROP DATASET IF EXISTS test).
  *   DataverseName (string) - The name of the dataverse to use, default to none. If set then will be used as DROP DATASET dataverseName.datasetName. If not set then will be DROP DATASET datasetName.
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   DatasetNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  #### GetAllDatasets

  Gets all datasets (SELECT d.* FROM Metadata.`Dataset` d WHERE d.DataverseName  "Metadata").

  Signature

  

  

  

  

  

  Iterable GetAllDatasets([options])

  

  

  

  

  Parameters

  *   Required:
  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   Any exceptions raised by the underlying platform

  #### CreateIndex

  Creates a new index.

  Signature

  

  

  

  

  

  void CreateIndex(string indexName, string datasetName, map[string]string fields,  [options])

  

  

  

  

  Parameters

  *   Required:

  *   DatasetName: string - name of the dataset.
  *   IndexName: string - name of the index.
  *   fields: map[string]string - the fields to create the index over. This is a map of the name of the field to the type of the field.

  *   Optional:

  *   IgnoreIfExists (bool) - don’t error/throw if the index already exists. (send “IF NOT EXISTS” as part of the dataset creation query, e.g. CREATE INDEX test IF NOT EXISTS ON default) (Note: IF NOT EXISTS is not is in the same place as it is in CREATE DATASET)
  *   DataverseName (string) - The name of the dataverse to use, default to none. If set then will be used as CREATE INDEX dataverseName.datasetName.indexName. If not set then will be CREATE INDEX datasetName.indexName.
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.Returns
  *   

  *   AnalyticsIndexAlreadyExistsException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  #### DropIndex

  Drops an index.

  Throws

  Signature

  

  

  

  

  

  void DropIndex(string indexName, string datasetName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   IndexName: string - name of the index.

  *   Optional:

  *   IgnoreIfNotExists (bool) - Don’t error/throw if the index does not exist.
  *   DataverseName (string) - The name of the dataverse to use, default to none. If set then will be used as DROP INDEX dataverseName.datasetName.indexName. If not set then will be DROP INDEX datasetName.indexName.
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   AnalyticsIndexNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  #### GetAlIndexes

  Gets all indexes (SELECT d.* FROM Metadata.`Index` d WHERE d.DataverseName  “Metadata”).

  Signature

  

  

  

  

  

  Iterable GetAllIndexes([options])

  

  

  

  

  Parameters

  *   Required:
  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   Any exceptions raised by the underlying platform

  #### Connect Link

  Connects a link.

  Signature

  

  

  

  

  

  void ConnectLink([options])

  

  

  

  

  Parameters

  *   Required:
  *   Optional[[e]](#cmnt5)[[f]](#cmnt6)[[g]](#cmnt7)[[h]](#cmnt8):

  *   linkName: string - name of the link. Default to “Local”.
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   AnalyticsLinkNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  #### Disconnect Link

  Disconnects a link.

  Signature

  

  

  

  

  

  void DisconnectLink([options])

  

  

  

  

  Parameters

  *   Required:
  *   Optional:

  *   linkName: string - name of the link. Default to “Local”.
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   AnalyticsLinkNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  #### Get Pending Mutations

  Gets the pending mutations for all datasets. This is returned in the form of dataverse.dataset: mutations. E.g.:

  {

      "Default.travel": 20688,

      "Default.thing": 0,

      "Default.default": 0,

      "Notdefault.default": 0

  }

  Note that if a link is disconnected then it will return no results. If all links are disconnected then an empty object is returned.

  Signature

  

  

  

  

  

  map[string]int GetPendingMutations( [options])

  

  

  

  

  Parameters

  *   Required:
  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   Any exceptions raised by the underlying platform

  Uri

  *   GET http://localhost:8095/analytics/node/agg/stats/remaining

  # Bucket Manager

  

  

  

  

  

  

  public interface IBucketManager{

  

          void CreateBucket(CreateBucketSettings settings, CreateBucketOptions options);

  

          void UpdateBucket(BucketSettings settings, UpdateBucketOptions options);

  

          void DropBucket(string bucketName, DropBucketOptions options);

  

          BucketSettings GetBucket(string bucketName, GetBucketOptions options);

  

          Iterable GetAllBuckets(GetAllBucketOptions options);

  

              void FlushBucket(string bucketName, FlushBucketOptions options); // using the ns_server REST interface

  }

  

  

  

  

  

  #### CreateBucket

  Creates a new bucket.

  Signature

  

  

  

  

  

  void CreateBucket(CreateBucketSettings settings, [options])

  

  

  

  

  Parameters

  *   Required: BucketSettings - settings for the bucket.
  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   BucketAlreadyExistsException(http 400 and content contains "Bucket with given name already exists")
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  Uri

  *   POST [http://localhost:8092/pools/default/buckets](https://www.google.com/url?q=http://localhost:8092/pools/default/buckets&sa=D&ust=1569855744407000)

  #### UpdateBucket

  Updatesa bucket. In the docstring the SDK must include a section about how every setting must be set to what the user wants it to be after the update. Any settings that are not set to their desired values may be reverted to default values by the server.

  Signature

  

  

  

  

  

  void UpdateBucket(BucketSettings settings, [options])

  

  

  

  

  Parameters

  *   Required: BucketSettings - settings for the bucket.
  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   InvalidArgumentsException
  *   BucketDoesNotExistException
  *   Any exceptions raised by the underlying platform

  Uri

  *   POST http://localhost:8092/pools/default/buckets/

  #### DropBucket

  Removes a bucket.

  Signature

  

  

  

  

  

  void DropBucket(string bucketName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   bucketName: string - the name of the bucket.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   BucketNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  Uri

  *   DELETE http://localhost:8092/pools/default/buckets/

  #### GetBucket

  Gets a bucket’s settings.

  Signature

  

  

  

  

  

  BucketSettings GetBucket(bucketName string, [options])

  

  

  

  

  Parameters

  *   Required:

  *   bucketName: string - the name of the bucket.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  BucketSettings, settings for the bucket. Note: the ram quota returned is in bytes, not mb so requires x  / 1024 twice. Also Note: FlushEnabled is not a setting returned by the server, if flush is enabled then the doFlush endpoint will be listed and should be used to populate the field.

  Throws

  *   BucketNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  Uri

  *   GET http://localhost:8092/pools/default/buckets/

  #### GetAllBuckets

  Gets all bucket settings. Note: the ram quota returned is in bytes, not mb so requires x  / 1024 twice.

  Signature

  

  

  

  

  

  Iterable GetAllBuckets([options])

  

  

  

  

  Parameters

  *   Required:
  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  An iterable of settings for each bucket.

  Throws

  *   Any exceptions raised by the underlying platform

  Uri

  *   GET http://localhost:8092/pools/default/buckets

  #### FlushBucket

  Flushes a bucket (uses the ns_server REST interface).

  Signature

  

  

  

  

  

  void FlushBucket(string bucketName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   bucketName: string - the name of the bucket.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   BucketNotFoundException
  *   InvalidArgumentsException
  *   FlushDisabledException
  *   Any exceptions raised by the underlying platform

  Uri

  *   POST http://localhost:8092//pools/default/buckets//controller/doFlush

  # User Manager

  Programmatic access to the user management REST API:

  https://docs.couchbase.com/server/current/rest-api/rbac.html

  

  Unless otherwise indicated, all objects SHOULD be immutable.

  ### Role

  A role identifies a specific permission. CAVEAT: The properties of a role are likely to change with the introduction of collection-level permissions. Until then, here’s what the accessor methods look like:

  

  *   String name()
  *   Optional bucket()

  ### RoleAndDescription

  Associates a role with its name and description. This is additional information only present in the “list available roles” response.

  

  *   Role role()
  *   String displayName()
  *   String description()

  ### Origin

  Indicates why the user has a specific role. If the type is “user” it means the role is assigned directly to the user. If the type is “group” it means the role is inherited from the group identified by the “name” field.

  

  *   String type()
  *   Optional name()

  ### RoleAndOrigins

  Associates a role with its origins. This is how roles are returned by the “get user” and “get all users” responses.

  

  *   Role role()
  *   List origins()

  ### User

  Mutable. Models the user properties that may be updated via this API. All properties of the User class MUST have associated setters except for “username” which is fixed when the object is created.

  

  *   String username()
  *   String displayName()
  *   Set groups() - (names of the groups)
  *   Set roles() - only roles assigned directly to the user (not inherited from groups)
  *   String password() - From the user’s perspective the password property is “write-only”. The accessor SHOULD be hidden from the user and be visible only to the manager implementation.

  ### UserAndMetadata

  Models the “get user” / “get all users” response. Associates the mutable properties of a user with derived properties such as the effective roles inherited from groups.

  

  *   AuthDomain domain() - AuthDomain is an enumeration with values “local” and “external”. It MAY alternatively be represented as String.
  *   User user() - returns a new mutable User object each time this method is called. Modifying the fields of the returned User MUST have no effect on the UserAndMetadata object it came from.
  *   Set effectiveRoles() - all roles, regardless of origin.
  *   List effectiveRolesAndOrigins() - same as effectiveRoles, but with origin information included.
  *   Optional passwordChanged()
  *   Set externalGroups()

  ### Group

  Mutable. Defines a set of roles that may be inherited by users. All properties of the Group class MUST have associated setters except for “name” which is fixed when the object is created.

  

  *   String name()
  *   String description()
  *   Set roles() - [Role](#h.zhz0katumzwe) as defined in the User Manager section
  *   Optional ldapGroupReference()

  ## Service Interface

  

  

  

  

  

  

  public interface IUserManager{

  

          UserAndMetadata GetUser(string username, GetUserOptions options);

  

          Iterable GetAllUsers(GetAllUsersOptions options);

  

              void UpsertUser(User user, UpsertUserOptions options);

  

          void DropUser(string userName, DropUserOptions options);

  

          Iterable AvailableRoles(AvailableRolesOptions options);

  

          Group GetGroup(string groupName, GetGroupOptions options);

  

          Iterable GetAllGroups(GetAllGroupsOptions options);

  

              void UpsertGroup(Group group, UpsertGroupOptions options);

  

          void DropGroup(string groupName, DropGroupOptions options);

  }

  

  

  

  

  #### 

  #### GetUser

  Gets a user.

  Signature

  

  

  

  

  

  UserAndMetadata GetUser(string username, [options])

  

  

  

  

  Parameters

  *   Required:

  *   username: string - ID of the user.

  *   Optional:

  *   domainName: string - name of the user domain. Defaults to local.        
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  An instance of UserAndMetadata.

  Throws

  *   UserNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  

  Implementation Notes

  

  When parsing the “get” and “getAll” responses, take care to distinguish between roles assigned directly to the user (role origin with type=”user”) and roles inherited from groups (role origin with type=”group” and name=).

  

  If the server response does not include an “origins” field for a role, then it was generated by a server version prior to 6.5 and the SDK MUST treat the role as if it had a single origin of type=”user”.

  

  #### GetAllUsers

  Gets all users.

  Signature

  

  

  

  

  

  Iterable GetAllUsers([options])

  

  

  

  

  Parameters

  *   Required:
  *   Optional:

  *   domainName: string - name of the user domain. Defaults to local.
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  An iterable collection of UserAndMetadata.

  Throws

  *   Any exceptions raised by the underlying platform

  #### UpsertUser

  Creates or updates a user.

  Signature

  

  

  

  

  

  void UpsertUser(User user, [options])

  

  

  

  

  Parameters

  *   Required:

  *   user: User - the new version of the user.

  *   Optional:

  *   DomainName: string - name of the user domain (local | external). Defaults to local.
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  

  Implementation Notes

  

  When building the PUT request to send to the REST endpoint, implementations MUST omit the “password” property if it is not present in the given User domain object (so that the password is only changed if the calling code provided a new password).

  

  For backwards compatibility with Couchbase Server 6.0 and earlier, the “groups” parameter MUST be omitted if the group list is empty. Couchbase Server 6.5 treats the absent parameter the same as an explicit parameter with no value (removes any existing group associations, which is what we want in this case).

  

  #### DropUser

  Removes a user.

  Signature

  

  

  

  

  

  void DropUser(string username, [options])

  

  

  

  

  Parameters

  *   Required:

  *   username: string - ID of the user.

  *   Optional:

  *   DomainName: string - name of the user domain. Defaults to local.
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   UserNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  

  #### Available Roles

  Returns the roles supported by the server.

  Signature

  

  

  

  

  

  Iterable GetRoles([options])

  

  

  

  

  Parameters

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  An iterable collection of RoleAndDescription.

  Throws

  *   Any exceptions raised by the underlying platform

  

  #### GetGroup

  Gets a group.

  

  REST Endpoint: GET /settings/rbac/groups/

  Signature

  

  

  

  

  

  Group GetGroup(string groupName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   groupName: string - name of the group to get.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  An instance of Group.

  Throws

  *   GroupNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  

  #### GetAllGroups

  Gets all groups.

  

  REST Endpoint: GET /settings/rbac/groups

  Signature

  

  

  

  

  

  Iterable GetAllGroups([options])

  

  

  

  

  Parameters

  *   Required:
  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  An iterable collection of Group.

  Throws

  *   Any exceptions raised by the underlying platform

  #### UpsertGroup

  Creates or updates a group.

  

  REST Endpoint: PUT /settings/rbac/groups/

  This endpoint accepts application/x-www-form-urlencoded and requires the data be sent as form data. The name/id should not be included in the form data. Roles should be a comma separated list of strings. If, only if, the role contains a bucket name then the rolename should be suffixed with[] e.g. bucket_full_access[default],security_admin.

  Signature

  

  

  

  

  

  void UpsertGroup(Group group, [options])

  

  

  

  

  Parameters

  *   Required:

  *   group: Group - the new version of the group.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  

  #### DropGroup

  Removes a group.

  

  REST Endpoint: DELETE /settings/rbac/groups/

  Signature

  

  

  

  

  

  void DropGroup(string groupName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   groupName: string - name of the group.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   GroupNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  # Collections Manager

  Note: due to [https://issues.couchbase.com/browse/MB-35386](https://www.google.com/url?q=https://issues.couchbase.com/browse/MB-35386&sa=D&ust=1569855744460000) CollectionExists, ScopeExists, and GetScope must support both forms of the manifest until SDK beta. That is, going forward:

  

  {“uid”:“0",“scopes”:[{“name”:“_default”,“uid”:“0”,“collections”:[{“name”:“_default”,“uid”:“0"}]}]}

  

  And for the sake of support for the server beta which did not have the fix in place:

  {“uid”:0,“scopes”:{“_default”:{“uid”:0,“collections”:{“_default”:{“uid”:0}}}}}

  It is recommended to try to parse the first form and fallback to the second so that it can be easily removed later.

  

  

  

  

  

  

  public interface ICollectionManager{

  

              boolean CollectionExists(ICollectionSpec collection, CollectionExistsOptions options);

  

              boolean ScopeExists(string scopeName, ScopeExistsOptions options);

  

              IScopeSpec GetScope(string scopeName, GetScopeOptions options);

  

             Iterable GetAllScopes(GetAllScopesOptions options);

  

  void CreateCollection(ICollectionSpec collection, CreateCollectionOptions options);

  

          void DropCollection(ICollectionSpec collection, DropCollectionOptions options);

  

           void CreateScope(IScopeSpec scope, CreateScopeOptions options);[[i]](#cmnt9)[[j]](#cmnt10)

  

          void DropScope(string scopeName, DropScopeOptions options);

  

          void FlushCollection[[k]](#cmnt11)[[l]](#cmnt12)[[m]](#cmnt13)[[n]](#cmnt14)(ICollectionSpec collection, FlushCollectionOptions options);

  }

  

  

  

  

  

  

  

  

  

  

  #### Collection Exists

  Checks for existence of a collection. This will fetch a manifest and then interrogate it to check that the scope name exists and then that the collection name exists within that scope.

  Signature

  

  

  

  

  

  boolean CollectionExists(ICollectionSpec collection,  [options])

  

  

  

  

  Parameters

  *   Required:

  *   collection: ICollectionSpec - spec of the collection.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   Any exceptions raised by the underlying platform
  *   InvalidArgumentsException

  Uri

  *   GET /pools/default/buckets//collections

  #### Scope Exists

  Checks for existence of a scope. This will fetch a manifest and then interrogate it to check that the scope name exists.

  Signature

  

  

  

  

  

  boolean ScopeExists(String scopeName,  [options])

  

  

  

  

  Parameters

  *   Required:

  *   scopeName: string - name of the scope.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   Any exceptions raised by the underlying platform

  Uri

  *   GET /pools/default/buckets//collections

  #### Get Scope

  Gets a scope. This will fetch a manifest and then pull the scope out of it.

  Signature

  

  

  

  

  

  IScopeSpec GetScope(string scopeName,  [options])

  

  

  

  

  Parameters

  *   Required:

  *   scopeName: string - name of the scope.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   ScopeNotFoundException
  *   Any exceptions raised by the underlying platform

  Uri

  *   GET /pools/default/buckets//collections

  #### Get All Scopes

  Gets all scopes. This will fetch a manifest and then pull the scopes out of it.

  Signature

  

  

  

  

  

  iterable GetAllScopes([options])

  

  

  

  

  Parameters

  *   Required:
  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   Any exceptions raised by the underlying platform

  Uri

  *   GET /pools/default/buckets//collections

  #### Create Collection

  Creates a new collection.

  Signature

  

  

  

  

  

  void CreateCollection(CollectionSpec collection, [options])

  

  

  

  

  Parameters

  *   Required:

  *   collection: CollectionSpec - specification of the collection.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   InvalidArgumentsException
  *   CollectionAlreadyExistsException
  *   ScopeNotFoundException
  *   Any exceptions raised by the underlying platform

  Uri

  *   POST http://localhost:8091/pools/default/buckets//collections/ -d name=

  #### Drop Collection

  Removes a collection.

  Signature

  

  

  

  

  

  void DropCollection(ICollectionSpec collection, [options])

  

  

  

  

  Parameters

  *   Required:

  *   collection: ICollectionSpec - namspece of the collection.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   CollectionNotFoundException
  *   Any exceptions raised by the underlying platform

  Uri

  *   DELETE http://localhost:8091/pools/default/buckets//collections//

  #### Create Scope

  Creates a new scope.

  Signature

  

  

  

  

  

  Void CreateScope(string scopeName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   scopeName: String - name of the scope.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  Uri

  *   POST [http://localhost:8091/pools/default/buckets/](https://www.google.com/url?q=http://localhost:8091/pools/default/buckets/&sa=D&ust=1569855744485000)/collections -d name=

  #### Drop Scope

  Removes a scope.

  Signature

  

  

  

  

  

  void DropScope(string scopeName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   collectionName: string - name of the collection.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   ScopeNotFoundException
  *   Any exceptions raised by the underlying platform

  Uri

  *   DELETE [http://localhost:8091/pools/default/buckets/](https://www.google.com/url?q=http://localhost:8091/pools/default/buckets/&sa=D&ust=1569855744488000)/collections/

  # Types

  #### DesignDocument

  DesignDocument provides a means of mapping a design document into an object. It contains within it a map of View.

  

  

  

  

  

  

   type DesignDocument{

  

  String Name();

                  

          Map[String]IView Views();

  }

  

  

  

  

  

  #### View

  

  

  

  

  

   type View{

  

              String Map();

                  

              String Reduce();

  }

  

  

  

  

  ## 

  #### IQueryIndex Interface

  The IQueryIndex interface provides a means of mapping a query index into an object.

  

  

  

  

  

  

   interface IQueryIndex{

  

              String Name();

                  

          Bool IsPrimary();

  

          IndexType Type();

  

          String State();

  

          String Keyspace();

  

  Iterable IndexKey();

  

          Optional Condition();

  }

  

  

  

  

  

  #### AnalyticsDataset Interface

  AnalyticsDataset provides a means of mapping dataset details into an object.

  

  

  

  

  

  

   interface AnalyticsDataset{

  

              String Name();

                  

          String DataverseName();

                  

          String LinkName();

                  

          String BucketName();

  }

  

  

  

  

  #### AnalyticsIndex Interface

  AnalyticsIndex provides a means of mapping analytics index details into an object.

  

  

  

  

  

  

   interface AnalyticsDataset{

  

              String Name();

                  

          String DatasetName();

  

          String DataverseName();

                  

          Bool IsPrimary();

  }

  

  

  

  

  #### 

  #### BucketSettings

  BucketSettings provides a means of mapping bucket settings into an object.

  *   Name (string) - The name of the bucket.
  *   FlushEnabled (bool) - Whether or not flush should be enabled on the bucket. Default to false.
  *   RamQuotaMB (int) - Ram Quota in mb for the bucket. (rawRAM in the server payload)
  *   NumReplicas (int) - The number of replicas for documents.
  *   ReplicaIndexes (bool) - Whether replica indexes should be enabled for the bucket.
  *   BucketType {couchbase (sent on wire as membase), memcached, ephemeral} - The type of the bucket. Default to couchbase.
  *   EjectionMethod {fullEviction | valueOnly}. The eviction policy to use.
  *   maxTTL (int) - Value for the maxTTL of new documents created without a ttl.
  *   compressionMode {off | passive | active} - The compression mode to use.

  #### CreateBucketSettings

  CreateBucketSettings is a superset of BucketSettings providing one extra property:

  *   ConflictResolutionType {Timestamp (sent as lww) | SequenceNumber (sent as seqno)}. The conflict resolution type to use.

  The reasoning for this is that on Update ConflictResolutionType cannot be present in the JSON payload at all.

  

  #### UpsertIndeSearchIndex

  SearchIndex provides a means to map search indexes into object. The Params, SourceParams, and PlanParams fields are left to the SDK to decide what is idiomatic (e.g. JSONObject), the definitions of these fields is purposefully vague.

  

  

  

  

  

  type SearchIndex struct {

          // UUID is required for updates. It provides a means of ensuring consistency, the UUID must match the UUID value

          // for the index on the server.

          UUID string `json:"uuid"`

  

          Name string `json:"name"`

  

          // SourceName is the name of the source of the data for the index e.g. bucket name.

          SourceName string `json:"sourceName,omitempty"`

  

          // Type is the type of index, e.g. fulltext-index or fulltext-alias.

          Type string `json:"type"`

  

          // IndexParams are index properties such as store type and mappings.

          Params map[string]interface{} `json:"params"`

  

          // SourceUUID is the UUID of the data source, this can be used to more tightly tie the index to a source.

          SourceUUID string `json:"sourceUUID,omitempty"`

  

          // SourceParams are extra parameters to be defined. These are usually things like advanced connection and tuning

          // parameters.

          SourceParams map[string]interface{} `json:"sourceParams,omitempty"`

  

          // SourceType is the type of the data source, e.g. couchbase or nil depending on the Type field.

          SourceType string `json:"sourceType"`

  

          // PlanParams are plan properties such as number of replicas and number of partitions.

          PlanParams map[string]interface{} `json:"planParams,omitempty"`

  }

  

  

  

  

  

  

  #### IUser Interface

  The IUser interface provides a means of mapping user settings into an object.

  

  

  

  

  

  

   Interface IUser{

  

              String ID();

  

              String Name();

          

              Iterable Roles();

  }

  

  

  

  

  

  #### ICollectionSpec Interface

  

  

  

  

  

  

   Interface ICollectionSpec{

  

              String Name();

          

              String ScopeName();

  }

  

  

  

  

  

  #### IScopeSpec Interface

  

  

  

  

  

  

   Interface IScopeSpec{

  

              String Name();

          

              Iterable Collections();

  }

  

  

  

  

  

  

  

  

  # References

  *   Query index management

  *   [https://github.com/couchbaselabs/sdk-rfcs/blob/master/rfc/0003-indexmanagement.md](https://www.google.com/url?q=https://github.com/couchbaselabs/sdk-rfcs/blob/master/rfc/0003-indexmanagement.md&sa=D&ust=1569855744515000)
  *   [https://docs.couchbase.com/server/current/n1ql/n1ql-language-reference/](https://www.google.com/url?q=https://docs.couchbase.com/server/current/n1ql/n1ql-language-reference/&sa=D&ust=1569855744516000)

  *   Search index management

  *   [https://docs.google.com/document/d/1C4yfTj5u6ahRgk3ZIL_AkwPMeu9-hHY_lZcsDNeIP74](https://www.google.com/url?q=https://docs.google.com/document/d/1C4yfTj5u6ahRgk3ZIL_AkwPMeu9-hHY_lZcsDNeIP74&sa=D&ust=1569855744517000)
  *   [https://docs.couchbase.com/server/6.0/rest-api/rest-fts-indexing.html](https://www.google.com/url?q=https://docs.couchbase.com/server/6.0/rest-api/rest-fts-indexing.html&sa=D&ust=1569855744517000)
  *   [http://labs.couchbase.com/cbft/dev-guide/index-definitions/](https://www.google.com/url?q=http://labs.couchbase.com/cbft/dev-guide/index-definitions/&sa=D&ust=1569855744518000)

  *   Outdated but contains some useful definitions for fields.

  *   User Management

  *   [https://github.com/couchbaselabs/sdk-rfcs/blob/master/rfc/0022-usermgmt.md](https://www.google.com/url?q=https://github.com/couchbaselabs/sdk-rfcs/blob/master/rfc/0022-usermgmt.md&sa=D&ust=1569855744518000)

  *   Bucket Management

  *   [https://docs.couchbase.com/server/current/rest-api/rest-bucket-intro.html](https://www.google.com/url?q=https://docs.couchbase.com/server/current/rest-api/rest-bucket-intro.html&sa=D&ust=1569855744519000)

  *   Collection Management

  *   [https://github.com/couchbase/ns_server/commit/4c1a9ea20fbdb148f68ec2ad7be9eed4c071bf9e](https://www.google.com/url?q=https://github.com/couchbase/ns_server/commit/4c1a9ea20fbdb148f68ec2ad7be9eed4c071bf9e&sa=D&ust=1569855744519000)
  *   [https://docs.google.com/document/d/1X-v8GWQjplrMMaYwwWOzEuP4AUoDNIAvS39NmEjQ3_E/edit#heading=h.gprum229kohk](https://www.google.com/url?q=https://docs.google.com/document/d/1X-v8GWQjplrMMaYwwWOzEuP4AUoDNIAvS39NmEjQ3_E/edit%23heading%3Dh.gprum229kohk&sa=D&ust=1569855744520000)

  *   Views REST API

  *   [https://docs.couchbase.com/server/6.0/rest-api/rest-views-intro.html](https://www.google.com/url?q=https://docs.couchbase.com/server/6.0/rest-api/rest-views-intro.html&sa=D&ust=1569855744520000)

  *   Groups and LDAP Groups

  *   [https://docs.google.com/document/d/1wsjEmke80RW_sbW0ycS8yQl6rq5lzBbRWuelPZ1m9ZI/edit#](https://www.google.com/url?q=https://docs.google.com/document/d/1wsjEmke80RW_sbW0ycS8yQl6rq5lzBbRWuelPZ1m9ZI/edit%23&sa=D&ust=1569855744521000)
  *   [https://docs.google.com/document/d/1cFZOz9n6ZKyq_thxCSteuLrZ0rJEh7AMT3MFbOHCchM/edit](https://www.google.com/url?q=https://docs.google.com/document/d/1cFZOz9n6ZKyq_thxCSteuLrZ0rJEh7AMT3MFbOHCchM/edit&sa=D&ust=1569855744521000)
  *   [https://issues.couchbase.com/browse/MB-16035](https://www.google.com/url?q=https://issues.couchbase.com/browse/MB-16035&sa=D&ust=1569855744522000)

  *   Analytics management

  *   [https://docs.couchbase.com/server/current/analytics/5_ddl.html](https://www.google.com/url?q=https://docs.couchbase.com/server/current/analytics/5_ddl.html&sa=D&ust=1569855744522000)

  

  # Changes

  2019-09-30:

  *   Remove dataverse name checking from all Analytics options blocks so that if the dataverse name is set we do not check if the dataset already contains it.
  *   Added Condition to IQueryIndex.
  *   Changed User AvailableRoles to GetRoles.
  *   Change ConnectLink and DisconnectLink so that the name is optional, defaulting to Local.

  2019-09-18:

  *   Add FlushNotEnabledException to bucket Flush operation

  2019-09-03:

  *    Add numReplicas option to QueryIndexManager CreatePrimaryIndex

  

  [[a]](#cmnt_ref1)Java path-finding impl also has AND `using` = \"gsi\"

  

  

  [[b]](#cmnt_ref2)I believe this is from back in the very first versions of N1QL, where it was required to be specified.  I don't think we need to bring this behaviour forward.

  

  

  [[c]](#cmnt_ref3)Java impl does this by getting all indexes and doing BUILD INDEX on any currently set to deferred.  Thought we weren't doing racey stuff like that in client as general rule?

  

  

  [[d]](#cmnt_ref4)That wouldn't be racy, since your going to build exactly the indices that you find during the first call.  From a functional perspective, only indexes that were deferred at the time you called the method are being built, which I think makes sense.

  

  

  [[e]](#cmnt_ref5)+charles.dixon@couchbase.com Should there be an optional `dataverse` parameter?

  

  

  [[f]](#cmnt_ref6)And an optional `force` parameter?

  

  

  [[g]](#cmnt_ref7)I guess we should make an escape style of parameter to future proof it.

  

  

  [[h]](#cmnt_ref8)I don't think we need to have an escape hatch on something that only exists for ease of use.  Relatedly, why does CONNECT LINK even accept a dataverse name?

  

  

  [[i]](#cmnt_ref9)There is still a question around this, I suggest that we just accept a string Name rather than a ScopeSpec and we don't create collections as a part of this. It isn't attempting to be an atomic operation that way.

  

  

  [[j]](#cmnt_ref10)I would be in favour of this change.

  

  

  [[k]](#cmnt_ref11)This is missing the function definition below like the others.

  

  

  [[l]](#cmnt_ref12)There seems to be some confusion over what this command does. The collections design doc states that there will be a flush endpoint that we can call over REST. I don't believe that it's implemented by ns server yet though.

  

  

  [[m]](#cmnt_ref13)https://docs.google.com/document/d/1X-v8GWQjplrMMaYwwWOzEuP4AUoDNIAvS39NmEjQ3_E/edit#heading=h.8c7d3zbqy7i is what I'm referring to

  

  

  [[n]](#cmnt_ref14)Server-side flushing was not implemented, instead it was decided that flushing a collection could be achieved trivially by the SDK through the destruction and recreation of the collection.

  
  

  

  

  

  Parameters

  *   Required:

  *    designDocName: string - the name of the design document.
  *   namespace: enum - PRODUCTION if the user is requesting a document from the production namespace, or DEVELOPMENT if from the development namespace.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  An instance of DesignDocument.

  Throws

  *   DesignDocumentNotFoundException (http 404)
  *   Any exceptions raised by the underlying platform

  Uri

  *   GET http://localhost:8092//_design/

  Example response from server

  {  

     "views":{  

        "test":{  

           "map":"function (doc, meta) {\n\t\t\t\t\t\t  emit(meta.id, null);\n\t\t\t\t\t\t}",

           "reduce":"_count"

        }

     }

  }

  #### GetAllDesignDocuments

  Fetches all design documents from the server.

  ]

  When processing the server response, the client must strip the “_design/” prefix from the document ID (as well as the “_dev” prefix if present). For example, a doc.meta.id value of “_design/foo” must be parsed as “foo”, and “_design/dev_bar” must be parsed as “bar”.

  Signature

  

  

  

  

  

  Iterable GetAllDesignDocuments(DesignDocumentNamespace namespace, [options])

  

  

  

  

  Parameters

  *   Required:

  *   namespace (enum) - indicates whether the user wants to get production documents (PRODUCTION) or development documents (DEVELOPMENT).

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  An iterable of DesignDocument.

  Throws

  *   Any exceptions raised by the underlying platform

  Uri

  *   GET http://localhost:8091/pools/default/buckets//ddocs

  

  Example response from server

  {  

     "rows":[  

        {  

           "doc":{  

              "meta":{  

                 "id":"_design/dev_test",

                 "rev":"1-ae5e21ec"

              },

              "json":{  

                 "views":{  

                    "test":{  

                       "map":"function (doc, meta) {\n\t\t\t\t\t\t  emit(meta.id, null);\n\t\t\t\t\t\t}",

                       "reduce":"_count"

                    }

                 }

              }

           },

           "controllers":{  

              "compact":"/pools/default/buckets/default/ddocs/_design%2Fdev_test/controller/compactView",

              "setUpdateMinChanges":"/pools/default/buckets/default/ddocs/_design%2Fdev_test/controller/setUpdateMinChanges"

           }

        }

     ]

  }

  #### UpsertDesignDocument

  Updates, or inserts, a design document.

  Signature

  

  

  

  

  

  void UpsertDesignDocument(DesignDocument designDocData, DesignDocumentNamespace namespace, [options])

  

  

  

  

  Parameters

  *   Required:

  *   designDocData: DesignDocument - the data to use to create the design document
  *   namespace (enum) - indicates whether the user wants to upsert the document to the production namespace (PRODUCTION) or development namespace (DEVELOPMENT).

  *   Optional:

  *   
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   Any exceptions raised by the underlying platform

  Uri

  *   PUT http://localhost:8092//_design/

  #### DropDesignDocument

  Removes a design document.

  Signature

  

  

  

  

  

  void DropDesignDocument(string designDocName, DesignDocumentNamespace namespace,  [options])

  

  

  

  

  Parameters

  *   Required:

  *   designDocName: string - the name of the design document.
  *   namespace: enum - indicates whether the name refers to a production document (PRODUCTION) or a development document (DEVELOPMENT).

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   DesignDocumentNotFoundException (http 404)
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  Uri

  *   DELETE http://localhost:8092//_design/

  #### PublishDesignDocument

  Publishes a design document. This method is equivalent to getting a document from the development namespace and upserting it to the production namespace.

  Signature

  

  

  

  

  

  void PublishDesignDocument(string designDocName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   designDocName: string - the name of the development design document.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   DesignDocumentNotFoundException (http 404)
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  # Query Index Manager

  The Query Index Manager interface contains the means for managing indexes used for queries.

  

  

  

  

  

  

  

  public interface IQueryIndexManger{

  

          Iterable GetAllIndexes(string bucketName, GetAllQueryIndexOptions options);

  

  void CreateIndex(string bucketName, string indexName, []string fields, CreateQueryIndexOptions options);

  

             void CreatePrimaryIndex(string bucketName, CreatePrimaryQueryIndexOptions options);

  

          void DropIndex(string bucketName, string indexName, DropQueryIndexOptions options);

  

              void DropPrimaryIndex(string bucketName, DropPrimaryQueryIndexOptions options);

  

  void WatchIndexes(string bucketName, []string indexNames, timeout duration, WatchQueryIndexOptions options);

     

              void BuildDeferredIndexes(string bucketName, BuildQueryIndexOptions options);

  }

  

  

  

  

  

  ### Methods

  The following methods must be implemented:

  

  #### GetAllIndexes

  Fetches all indexes from the server.

  Signature

  

  

  

  

  

  Iterable GetAllIndexes(string bucketName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   BucketName: string - the name of the bucket.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  N1QL

  SELECT idx.* FROM system:indexes AS idx

      WHERE keyspace_id = "bucketName"

  [[a]](#cmnt1)[[b]](#cmnt2)

      ORDER BY is_primary DESC, name ASC

  Returns

  An array of IQueryIndex.

  Throws

  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  #### CreateIndex

  Creates a new index.

  Signature

  

  

  

  

  

  void CreateIndex(string bucketName, string indexName, []string fields,  [options])

  

  

  

  

  Parameters

  *   Required:

  *   BucketName: string - the name of the bucket.
  *   IndexName: string - the name of the index.
  *   fields: []string - the fields to create the index over.

  *   Optional:

  *   IgnoreIfExists (bool) - Don’t error/throw if the index already exists.
  *   NumReplicas (int) - The number of replicas that this index should have. Uses the WITH keyword and num_replica.

  *   CREATE INDEX indexNameON bucketName WITH { "num_replica": 2 }
  *   [https://docs.couchbase.com/server/current/n1ql/n1ql-language-reference/createindex.html](https://www.google.com/url?q=https://docs.couchbase.com/server/current/n1ql/n1ql-language-reference/createindex.html&sa=D&ust=1569855744308000)

  *   Deferred (bool) - Whether the index should be created as a deferred index.
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   IndexAlreadyExistsException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  #### CreatePrimaryIndex

  Creates a new primary index.

  Signature

  

  

  

  

  

  void CreatePrimaryIndex(string bucketName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   BucketName: string - name of the bucket.

  *   Optional:

  *   IndexName: string - name of the index.
  *   IgnoreIfExists (bool) - Don’t error/throw if the index already exists.
  *   NumReplicas (int) - The number of replicas that this index should have. Uses the WITH keyword and num_replica.

  *   CREATE INDEX indexNameON bucketName WITH { "num_replica": 2 }
  *   [https://docs.couchbase.com/server/current/n1ql/n1ql-language-reference/createindex.html](https://www.google.com/url?q=https://docs.couchbase.com/server/current/n1ql/n1ql-language-reference/createindex.html&sa=D&ust=1569855744311000)

  *   Deferred (bool) - Whether the index should be created as a deferred index.
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   QueryIndexAlreadyExistsException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  #### DropIndex

  Drops an index.

  Signature

  

  

  

  

  

  void DropIndex(string bucketName, string indexName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   BucketName: string - name of the bucket.
  *   IndexName: string - name of the index.

  *   Optional:

  *   IgnoreIfNotExists (bool) - Don’t error/throw if the index does not exist.
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   QueryIndexNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  #### DropPrimaryIndex

  Drops a primary index.

  Signature

  

  

  

  

  

  void DropPrimaryIndex(string bucketName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   BucketName: string - name of the bucket.

  *   Optional:

  *   IndexName: string - name of the index.
  *   IgnoreIfNotExists (bool) - Don’t error/throw if the index does not exist.
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   QueryIndexNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  #### WatchIndexes

  Watch polls indexes until they are online.

  Signature

  

  

  

  

  

  void WatchIndexes(string bucketName, []string indexNames, timeout duration, [options])

  

  

  

  

  Parameters

  *   Required:

  *   BucketName: string - name of the bucket.
  *   IndexName: []string - name(s) of the index(es).
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  *   Optional:

  *   WatchPrimary (bool) - whether or not to watch the primary index.

  Returns

  Throws

  *   QueryIndexNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  #### BuildDeferredIndexes[[c]](#cmnt3)[[d]](#cmnt4)

  Build Deferred builds all indexes which are currently in deferred state.

  Signature

  

  

  

  

  

  void BuildDeferredIndexes(string bucketName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   BucketName: string - name of the bucket.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   Any exceptions raised by the underlying platform
  *   InvalidArgumentsException

  

  # Search Index Manager

  The Search Index Manager interface contains the means for managing indexes used for search. Search index definitions are purposefully left very dynamic as the index definitions on the server are complex. As such it is left to each SDK to implement its own dynamic type for this, JSONObject is used here to signify that. Stability level is uncommited?

  

  

  

  

  

  

  public interface ISearchIndexManager{

  

          ISearchIndex GetIndex(string indexName, GetSearchIndexOptions options);

  

          Iterable GetAllIndexes(GetAllSearchIndexesOptions options);

  

           void UpsertIndex(ISearchIndex indexDefinition, UpsertSearchIndexOptions options);

  

          void DropIndex(string indexName, DropSearchIndexOptions options);

  

          int GetIndexedDocumentsCount(string indexName, GetIndexedSearchIndexOptions options);

  

          void PauseIngest(string indexName, PauseIngestSearchIndexOptions);

  

          void ResumeIngest(string indexName, ResumeIngestSearchIndexOptions);

  

          void AllowQuerying(string indexName, AllowQueryingSearchIndexOptions);

  

          void DisallowQuerying(string indexName, DisallowQueryingSearchIndexOptions);

  

          void FreezePlan(string indexName, FreezePlanSearchIndexOptions);

  

          void UnfreezePlan(string indexName, UnfreezePlanSearchIndexOptions);

  

             Iterable AnalyzeDocument(string indexName, JSONObject document, AnalyzeDocOptions options);

  }

  

  

  

  

  

  ### Methods

  The following methods must be implemented:

  #### GetIndex

  Fetches an index from the server if it exists.

  Signature

  

  

  

  

  

  ISearchIndex GetIndex(string indexName, [options])

  

  

  

  

  Parameters

  *   Required:

  *    IndexName: string - name of the index.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  An instance of ISearchIndex.

  Throws

  *   SearchIndexNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  Uri

  *   GET http://localhost:8094/api/index/

  #### GetAllIndexes

  Fetches all indexes from the server.

  Signature

  

  

  

  

  

  Iterable GetAllIndexes([options])

  

  

  

  

  Parameters

  *   Required:
  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  An array of ISearchIndex.

  Throws

  *   Any exceptions raised by the underlying platform

  Uri

  *   GET http://localhost:8094/api/index

  #### UpsertIndex

  Creates, or updates, an index. .

  Signature

  

  

  

  

  

  void UpsertIndex(ISearchIndex indexDefinition, [options])

  

  

  

  

  Parameters

  *   Required:

  *   indexDefinition: SearchIndex - the index definition

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   InvalidArgumentsException

  *   If any of the following are empty:

  *   Name
  *   Type
  *   SourceType

  *   Any exceptions raised by the underlying platform

  Uri

  *   PUT [http://localhost:8094/api/index/](https://www.google.com/url?q=http://localhost:8094/api/index/&sa=D&ust=1569855744339000)

  *   Should be sent with request header “cache-control” set to “no-cache”.

  #### DropIndex

  Drops an index.

  Signature

  

  

  

  

  

  void DropIndexstring indexName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   IndexName: string - name of the index.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   SearchIndexNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  Uri

  *   DELETE [http://localhost:8094/api/index/](https://www.google.com/url?q=http://localhost:8094/api/index/&sa=D&ust=1569855744343000)

  #### GetIndexedDocumentsCount

  Retrieves the number of documents that have been indexed for an index.

  Signature

  

  

  

  

  

  void GetIndexedDocumentsCount(string indexName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   IndexName: string - name of the index.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   SearchIndexNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  Uri

  *   GET [http://localhost:8094/api/index/](https://www.google.com/url?q=http://localhost:8094/api/index/&sa=D&ust=1569855744346000)/count

  #### PauseIngest

  Pauses updates and maintenance for an index.

  Signature

  

  

  

  

  

  void PauseIngest(string indexName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   IndexName: string - name of the index.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   SearchIndexNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  Uri

  *   POST /api/index/{indexName}/ingestControl/pause

  #### ResumeIngest

  Resumes updates and maintenance for an index.

  Signature

  

  

  

  

  

  void ResumeIngest(string indexName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   IndexName: string - name of the index.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   SearchIndexNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  Uri

  *   POST /api/index/{indexName}/ingestControl/resume

  #### AllowQuerying

  Allows querying against an index.

  Signature

  

  

  

  

  

  void AllowQuerying(string indexName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   IndexName: string - name of the index.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   SearchIndexNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  Uri

  *   POST /api/index/{indexName}/queryControl/allow

  #### DisallowQuerying

  Disallows querying against an index.

  Signature

  

  

  

  

  

  void DisallowQuerying(string indexName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   IndexName: string - name of the index.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   SearchIndexNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  Uri

  *   POST /api/index/{indexName}/queryControl/disallow

  #### FreezePlan

  Freeze the assignment of index partitions to nodes.

  Signature

  

  

  

  

  

  void FreezePlan(string indexName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   IndexName: string - name of the index.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   SearchIndexNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  Uri

  *   POST /api/index/{indexName}/planFreezeControl/freeze

  #### UnfreezePlan

  Unfreeze the assignment of index partitions to nodes.

  Signature

  

  

  

  

  

  void UnfreezePlan(string indexName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   IndexName: string - name of the index.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   SearchIndexNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  Uri

  *   POST /api/index/{indexName}/planFreezeControl/unfreeze

  

  #### AnalyzeDocument

  Allows users to see how a document is analyzed against a specific index.

  Signature

  

  

  

  

  

  Iterable AnalyzeDocument(string indexName, JSONObject document, [options])

  

  

  

  

  Parameters

  *   Required:

  *   IndexName: string - name of the index.
  *   Document: JSONObject - the document to be analyzed.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  An iterable of JSONObject. The response from the server returns an object containing two top level keys: status and analyzed. The SDK must return the value containing within the analyze key.

  Throws

  *   SearchIndexNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  Uri

  *   POST /api/index/{indexName}/analyzeDoc

  *   As of build mad hatter 3839

  # Analytics Index Manager

  Stability level is not volatile.

  

  

  

  

  

  

  public interface IAnalyticsIndexManager{

  

           void CreateDataverse(string dataverseName, CreateDataverseAnalyticsOptions options);

  

          void DropDataverse(string dataverseName, DropDataverseAnalyticsOptions options);

  

           void CreateDataset(string bucketName, string datasetName, CreateDatasetAnalyticsOptions options);

  

          void DropDataset(string datasetName, DropDatasetAnalyticsOptions options);

  

    Iterable GetAllDatasets(GetAllDatasetAnalyticsOptions options);

  

           void CreateIndex(string indexName, map[string]string fields, CreateIndexAnalyticsOptions options);

  

           void DropIndex(string datasetName, string indexName, DropIndexAnalyticsOptions options);

  

              Iterable GetAllIndexes(GetAllIndexesAnalyticsOptions options);

  

           void ConnectLink(string linkName, ConnectLinkAnalyticsOptions options);

  

           void DisconnectLink(string linkName, DisconnectLinkAnalyticsOptions options);

  

   map[string]int GetPendingMutations(GetPendingMutationsAnalyticsOptions options);

  }

  

  

  

  

  

  

  

  

  

  

  #### Create Dataverse

  Creates a new dataverse.

  Signature

  

  

  

  

  

  void CreateDataverse(string dataverseName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   dataverseName: string - name of the dataverse.

  *   Optional:

  *   IgnoreIfExists (bool) - ignore if the dataset already exists (send “IF NOT EXISTS” as part of the dataset creation query, e.g. CREATE DATAVERSE IF NOT EXISTS test ON default). Default to false.
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   DataverseAlreadyExistsException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  #### Drop Dataverse

  Drops a dataverse.

  Signature

  

  

  

  

  

  void DropDataverse(string dataverseName,  [options])

  

  

  

  

  Parameters

  *   Required:

  *   dataverseName: string - name of the dataverse.

  *   Optional:

  *   IgnoreIfNotExists (bool) - ignore if the dataset doesn’t exists (send “IF EXISTS” as part of the dataset creation query, e.g. DROP DATAVERSE IF EXISTS test).
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   DataverseNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  #### CreateDataset

  Creates a new dataset.

  Signature

  

  

  

  

  

  void CreateDataset(string datasetName, string bucketName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   datasetName: string - name of the dataset.
  *   bucketName: string - name of the bucket.

  *   Optional:

  *   IgnoreIfExists (bool) - ignore if the dataset already exists (send “IF NOT EXISTS” as part of the dataset creation query, e.g. CREATE DATASET IF NOT EXISTS test ON default).c
  *   Condition (string) - Where clause to use for creating dataset.
  *   DataverseName (string) - The name of the dataverse to use, default to none. If set then will be used as CREATE DATASET dataverseName.datasetName. If not set then will be CREATE DATASET datasetName.
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   DatasetAlreadyExistsException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  #### DropDataset

  Drops a dataset.

  Signature

  

  

  

  

  

  void DropDataset(string datasetName,  [options])

  

  

  

  

  Parameters

  *   Required:

  *   datasetName: string - name of the dataset.

  *   Optional:

  *   IgnoreIfNotExists (bool) - ignore if the dataset doesn’t exists (send “IF EXISTS” as part of the dataset creation query, e.g. DROP DATASET IF EXISTS test).
  *   DataverseName (string) - The name of the dataverse to use, default to none. If set then will be used as DROP DATASET dataverseName.datasetName. If not set then will be DROP DATASET datasetName.
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   DatasetNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  #### GetAllDatasets

  Gets all datasets (SELECT d.* FROM Metadata.`Dataset` d WHERE d.DataverseName  "Metadata").

  Signature

  

  

  

  

  

  Iterable GetAllDatasets([options])

  

  

  

  

  Parameters

  *   Required:
  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   Any exceptions raised by the underlying platform

  #### CreateIndex

  Creates a new index.

  Signature

  

  

  

  

  

  void CreateIndex(string indexName, string datasetName, map[string]string fields,  [options])

  

  

  

  

  Parameters

  *   Required:

  *   DatasetName: string - name of the dataset.
  *   IndexName: string - name of the index.
  *   fields: map[string]string - the fields to create the index over. This is a map of the name of the field to the type of the field.

  *   Optional:

  *   IgnoreIfExists (bool) - don’t error/throw if the index already exists. (send “IF NOT EXISTS” as part of the dataset creation query, e.g. CREATE INDEX test IF NOT EXISTS ON default) (Note: IF NOT EXISTS is not is in the same place as it is in CREATE DATASET)
  *   DataverseName (string) - The name of the dataverse to use, default to none. If set then will be used as CREATE INDEX dataverseName.datasetName.indexName. If not set then will be CREATE INDEX datasetName.indexName.
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.Returns
  *   

  *   AnalyticsIndexAlreadyExistsException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  #### DropIndex

  Drops an index.

  Throws

  Signature

  

  

  

  

  

  void DropIndex(string indexName, string datasetName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   IndexName: string - name of the index.

  *   Optional:

  *   IgnoreIfNotExists (bool) - Don’t error/throw if the index does not exist.
  *   DataverseName (string) - The name of the dataverse to use, default to none. If set then will be used as DROP INDEX dataverseName.datasetName.indexName. If not set then will be DROP INDEX datasetName.indexName.
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   AnalyticsIndexNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  #### GetAlIndexes

  Gets all indexes (SELECT d.* FROM Metadata.`Index` d WHERE d.DataverseName  “Metadata”).

  Signature

  

  

  

  

  

  Iterable GetAllIndexes([options])

  

  

  

  

  Parameters

  *   Required:
  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   Any exceptions raised by the underlying platform

  #### Connect Link

  Connects a link.

  Signature

  

  

  

  

  

  void ConnectLink([options])

  

  

  

  

  Parameters

  *   Required:
  *   Optional[[e]](#cmnt5)[[f]](#cmnt6)[[g]](#cmnt7)[[h]](#cmnt8):

  *   linkName: string - name of the link. Default to “Local”.
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   AnalyticsLinkNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  #### Disconnect Link

  Disconnects a link.

  Signature

  

  

  

  

  

  void DisconnectLink([options])

  

  

  

  

  Parameters

  *   Required:
  *   Optional:

  *   linkName: string - name of the link. Default to “Local”.
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   AnalyticsLinkNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  #### Get Pending Mutations

  Gets the pending mutations for all datasets. This is returned in the form of dataverse.dataset: mutations. E.g.:

  {

      "Default.travel": 20688,

      "Default.thing": 0,

      "Default.default": 0,

      "Notdefault.default": 0

  }

  Note that if a link is disconnected then it will return no results. If all links are disconnected then an empty object is returned.

  Signature

  

  

  

  

  

  map[string]int GetPendingMutations( [options])

  

  

  

  

  Parameters

  *   Required:
  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   Any exceptions raised by the underlying platform

  Uri

  *   GET http://localhost:8095/analytics/node/agg/stats/remaining

  # Bucket Manager

  

  

  

  

  

  

  public interface IBucketManager{

  

          void CreateBucket(CreateBucketSettings settings, CreateBucketOptions options);

  

          void UpdateBucket(BucketSettings settings, UpdateBucketOptions options);

  

          void DropBucket(string bucketName, DropBucketOptions options);

  

          BucketSettings GetBucket(string bucketName, GetBucketOptions options);

  

          Iterable GetAllBuckets(GetAllBucketOptions options);

  

              void FlushBucket(string bucketName, FlushBucketOptions options); // using the ns_server REST interface

  }

  

  

  

  

  

  #### CreateBucket

  Creates a new bucket.

  Signature

  

  

  

  

  

  void CreateBucket(CreateBucketSettings settings, [options])

  

  

  

  

  Parameters

  *   Required: BucketSettings - settings for the bucket.
  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   BucketAlreadyExistsException(http 400 and content contains "Bucket with given name already exists")
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  Uri

  *   POST [http://localhost:8092/pools/default/buckets](https://www.google.com/url?q=http://localhost:8092/pools/default/buckets&sa=D&ust=1569855744407000)

  #### UpdateBucket

  Updatesa bucket. In the docstring the SDK must include a section about how every setting must be set to what the user wants it to be after the update. Any settings that are not set to their desired values may be reverted to default values by the server.

  Signature

  

  

  

  

  

  void UpdateBucket(BucketSettings settings, [options])

  

  

  

  

  Parameters

  *   Required: BucketSettings - settings for the bucket.
  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   InvalidArgumentsException
  *   BucketDoesNotExistException
  *   Any exceptions raised by the underlying platform

  Uri

  *   POST http://localhost:8092/pools/default/buckets/

  #### DropBucket

  Removes a bucket.

  Signature

  

  

  

  

  

  void DropBucket(string bucketName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   bucketName: string - the name of the bucket.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   BucketNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  Uri

  *   DELETE http://localhost:8092/pools/default/buckets/

  #### GetBucket

  Gets a bucket’s settings.

  Signature

  

  

  

  

  

  BucketSettings GetBucket(bucketName string, [options])

  

  

  

  

  Parameters

  *   Required:

  *   bucketName: string - the name of the bucket.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  BucketSettings, settings for the bucket. Note: the ram quota returned is in bytes, not mb so requires x  / 1024 twice. Also Note: FlushEnabled is not a setting returned by the server, if flush is enabled then the doFlush endpoint will be listed and should be used to populate the field.

  Throws

  *   BucketNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  Uri

  *   GET http://localhost:8092/pools/default/buckets/

  #### GetAllBuckets

  Gets all bucket settings. Note: the ram quota returned is in bytes, not mb so requires x  / 1024 twice.

  Signature

  

  

  

  

  

  Iterable GetAllBuckets([options])

  

  

  

  

  Parameters

  *   Required:
  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  An iterable of settings for each bucket.

  Throws

  *   Any exceptions raised by the underlying platform

  Uri

  *   GET http://localhost:8092/pools/default/buckets

  #### FlushBucket

  Flushes a bucket (uses the ns_server REST interface).

  Signature

  

  

  

  

  

  void FlushBucket(string bucketName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   bucketName: string - the name of the bucket.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   BucketNotFoundException
  *   InvalidArgumentsException
  *   FlushDisabledException
  *   Any exceptions raised by the underlying platform

  Uri

  *   POST http://localhost:8092//pools/default/buckets//controller/doFlush

  # User Manager

  Programmatic access to the user management REST API:

  https://docs.couchbase.com/server/current/rest-api/rbac.html

  

  Unless otherwise indicated, all objects SHOULD be immutable.

  ### Role

  A role identifies a specific permission. CAVEAT: The properties of a role are likely to change with the introduction of collection-level permissions. Until then, here’s what the accessor methods look like:

  

  *   String name()
  *   Optional bucket()

  ### RoleAndDescription

  Associates a role with its name and description. This is additional information only present in the “list available roles” response.

  

  *   Role role()
  *   String displayName()
  *   String description()

  ### Origin

  Indicates why the user has a specific role. If the type is “user” it means the role is assigned directly to the user. If the type is “group” it means the role is inherited from the group identified by the “name” field.

  

  *   String type()
  *   Optional name()

  ### RoleAndOrigins

  Associates a role with its origins. This is how roles are returned by the “get user” and “get all users” responses.

  

  *   Role role()
  *   List origins()

  ### User

  Mutable. Models the user properties that may be updated via this API. All properties of the User class MUST have associated setters except for “username” which is fixed when the object is created.

  

  *   String username()
  *   String displayName()
  *   Set groups() - (names of the groups)
  *   Set roles() - only roles assigned directly to the user (not inherited from groups)
  *   String password() - From the user’s perspective the password property is “write-only”. The accessor SHOULD be hidden from the user and be visible only to the manager implementation.

  ### UserAndMetadata

  Models the “get user” / “get all users” response. Associates the mutable properties of a user with derived properties such as the effective roles inherited from groups.

  

  *   AuthDomain domain() - AuthDomain is an enumeration with values “local” and “external”. It MAY alternatively be represented as String.
  *   User user() - returns a new mutable User object each time this method is called. Modifying the fields of the returned User MUST have no effect on the UserAndMetadata object it came from.
  *   Set effectiveRoles() - all roles, regardless of origin.
  *   List effectiveRolesAndOrigins() - same as effectiveRoles, but with origin information included.
  *   Optional passwordChanged()
  *   Set externalGroups()

  ### Group

  Mutable. Defines a set of roles that may be inherited by users. All properties of the Group class MUST have associated setters except for “name” which is fixed when the object is created.

  

  *   String name()
  *   String description()
  *   Set roles() - [Role](#h.zhz0katumzwe) as defined in the User Manager section
  *   Optional ldapGroupReference()

  ## Service Interface

  

  

  

  

  

  

  public interface IUserManager{

  

          UserAndMetadata GetUser(string username, GetUserOptions options);

  

          Iterable GetAllUsers(GetAllUsersOptions options);

  

              void UpsertUser(User user, UpsertUserOptions options);

  

          void DropUser(string userName, DropUserOptions options);

  

          Iterable AvailableRoles(AvailableRolesOptions options);

  

          Group GetGroup(string groupName, GetGroupOptions options);

  

          Iterable GetAllGroups(GetAllGroupsOptions options);

  

              void UpsertGroup(Group group, UpsertGroupOptions options);

  

          void DropGroup(string groupName, DropGroupOptions options);

  }

  

  

  

  

  #### 

  #### GetUser

  Gets a user.

  Signature

  

  

  

  

  

  UserAndMetadata GetUser(string username, [options])

  

  

  

  

  Parameters

  *   Required:

  *   username: string - ID of the user.

  *   Optional:

  *   domainName: string - name of the user domain. Defaults to local.        
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  An instance of UserAndMetadata.

  Throws

  *   UserNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  

  Implementation Notes

  

  When parsing the “get” and “getAll” responses, take care to distinguish between roles assigned directly to the user (role origin with type=”user”) and roles inherited from groups (role origin with type=”group” and name=).

  

  If the server response does not include an “origins” field for a role, then it was generated by a server version prior to 6.5 and the SDK MUST treat the role as if it had a single origin of type=”user”.

  

  #### GetAllUsers

  Gets all users.

  Signature

  

  

  

  

  

  Iterable GetAllUsers([options])

  

  

  

  

  Parameters

  *   Required:
  *   Optional:

  *   domainName: string - name of the user domain. Defaults to local.
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  An iterable collection of UserAndMetadata.

  Throws

  *   Any exceptions raised by the underlying platform

  #### UpsertUser

  Creates or updates a user.

  Signature

  

  

  

  

  

  void UpsertUser(User user, [options])

  

  

  

  

  Parameters

  *   Required:

  *   user: User - the new version of the user.

  *   Optional:

  *   DomainName: string - name of the user domain (local | external). Defaults to local.
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  

  Implementation Notes

  

  When building the PUT request to send to the REST endpoint, implementations MUST omit the “password” property if it is not present in the given User domain object (so that the password is only changed if the calling code provided a new password).

  

  For backwards compatibility with Couchbase Server 6.0 and earlier, the “groups” parameter MUST be omitted if the group list is empty. Couchbase Server 6.5 treats the absent parameter the same as an explicit parameter with no value (removes any existing group associations, which is what we want in this case).

  

  #### DropUser

  Removes a user.

  Signature

  

  

  

  

  

  void DropUser(string username, [options])

  

  

  

  

  Parameters

  *   Required:

  *   username: string - ID of the user.

  *   Optional:

  *   DomainName: string - name of the user domain. Defaults to local.
  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   UserNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  

  #### Available Roles

  Returns the roles supported by the server.

  Signature

  

  

  

  

  

  Iterable GetRoles([options])

  

  

  

  

  Parameters

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  An iterable collection of RoleAndDescription.

  Throws

  *   Any exceptions raised by the underlying platform

  

  #### GetGroup

  Gets a group.

  

  REST Endpoint: GET /settings/rbac/groups/

  Signature

  

  

  

  

  

  Group GetGroup(string groupName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   groupName: string - name of the group to get.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  An instance of Group.

  Throws

  *   GroupNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  

  #### GetAllGroups

  Gets all groups.

  

  REST Endpoint: GET /settings/rbac/groups

  Signature

  

  

  

  

  

  Iterable GetAllGroups([options])

  

  

  

  

  Parameters

  *   Required:
  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  An iterable collection of Group.

  Throws

  *   Any exceptions raised by the underlying platform

  #### UpsertGroup

  Creates or updates a group.

  

  REST Endpoint: PUT /settings/rbac/groups/

  This endpoint accepts application/x-www-form-urlencoded and requires the data be sent as form data. The name/id should not be included in the form data. Roles should be a comma separated list of strings. If, only if, the role contains a bucket name then the rolename should be suffixed with[] e.g. bucket_full_access[default],security_admin.

  Signature

  

  

  

  

  

  void UpsertGroup(Group group, [options])

  

  

  

  

  Parameters

  *   Required:

  *   group: Group - the new version of the group.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  

  #### DropGroup

  Removes a group.

  

  REST Endpoint: DELETE /settings/rbac/groups/

  Signature

  

  

  

  

  

  void DropGroup(string groupName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   groupName: string - name of the group.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   GroupNotFoundException
  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  # Collections Manager

  Note: due to [https://issues.couchbase.com/browse/MB-35386](https://www.google.com/url?q=https://issues.couchbase.com/browse/MB-35386&sa=D&ust=1569855744460000) CollectionExists, ScopeExists, and GetScope must support both forms of the manifest until SDK beta. That is, going forward:

  

  {“uid”:“0",“scopes”:[{“name”:“_default”,“uid”:“0”,“collections”:[{“name”:“_default”,“uid”:“0"}]}]}

  

  And for the sake of support for the server beta which did not have the fix in place:

  {“uid”:0,“scopes”:{“_default”:{“uid”:0,“collections”:{“_default”:{“uid”:0}}}}}

  It is recommended to try to parse the first form and fallback to the second so that it can be easily removed later.

  

  

  

  

  

  

  public interface ICollectionManager{

  

              boolean CollectionExists(ICollectionSpec collection, CollectionExistsOptions options);

  

              boolean ScopeExists(string scopeName, ScopeExistsOptions options);

  

              IScopeSpec GetScope(string scopeName, GetScopeOptions options);

  

             Iterable GetAllScopes(GetAllScopesOptions options);

  

  void CreateCollection(ICollectionSpec collection, CreateCollectionOptions options);

  

          void DropCollection(ICollectionSpec collection, DropCollectionOptions options);

  

           void CreateScope(IScopeSpec scope, CreateScopeOptions options);[[i]](#cmnt9)[[j]](#cmnt10)

  

          void DropScope(string scopeName, DropScopeOptions options);

  

          void FlushCollection[[k]](#cmnt11)[[l]](#cmnt12)[[m]](#cmnt13)[[n]](#cmnt14)(ICollectionSpec collection, FlushCollectionOptions options);

  }

  

  

  

  

  

  

  

  

  

  

  #### Collection Exists

  Checks for existence of a collection. This will fetch a manifest and then interrogate it to check that the scope name exists and then that the collection name exists within that scope.

  Signature

  

  

  

  

  

  boolean CollectionExists(ICollectionSpec collection,  [options])

  

  

  

  

  Parameters

  *   Required:

  *   collection: ICollectionSpec - spec of the collection.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   Any exceptions raised by the underlying platform
  *   InvalidArgumentsException

  Uri

  *   GET /pools/default/buckets//collections

  #### Scope Exists

  Checks for existence of a scope. This will fetch a manifest and then interrogate it to check that the scope name exists.

  Signature

  

  

  

  

  

  boolean ScopeExists(String scopeName,  [options])

  

  

  

  

  Parameters

  *   Required:

  *   scopeName: string - name of the scope.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   Any exceptions raised by the underlying platform

  Uri

  *   GET /pools/default/buckets//collections

  #### Get Scope

  Gets a scope. This will fetch a manifest and then pull the scope out of it.

  Signature

  

  

  

  

  

  IScopeSpec GetScope(string scopeName,  [options])

  

  

  

  

  Parameters

  *   Required:

  *   scopeName: string - name of the scope.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   ScopeNotFoundException
  *   Any exceptions raised by the underlying platform

  Uri

  *   GET /pools/default/buckets//collections

  #### Get All Scopes

  Gets all scopes. This will fetch a manifest and then pull the scopes out of it.

  Signature

  

  

  

  

  

  iterable GetAllScopes([options])

  

  

  

  

  Parameters

  *   Required:
  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   Any exceptions raised by the underlying platform

  Uri

  *   GET /pools/default/buckets//collections

  #### Create Collection

  Creates a new collection.

  Signature

  

  

  

  

  

  void CreateCollection(CollectionSpec collection, [options])

  

  

  

  

  Parameters

  *   Required:

  *   collection: CollectionSpec - specification of the collection.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   InvalidArgumentsException
  *   CollectionAlreadyExistsException
  *   ScopeNotFoundException
  *   Any exceptions raised by the underlying platform

  Uri

  *   POST http://localhost:8091/pools/default/buckets//collections/ -d name=

  #### Drop Collection

  Removes a collection.

  Signature

  

  

  

  

  

  void DropCollection(ICollectionSpec collection, [options])

  

  

  

  

  Parameters

  *   Required:

  *   collection: ICollectionSpec - namspece of the collection.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   CollectionNotFoundException
  *   Any exceptions raised by the underlying platform

  Uri

  *   DELETE http://localhost:8091/pools/default/buckets//collections//

  #### Create Scope

  Creates a new scope.

  Signature

  

  

  

  

  

  Void CreateScope(string scopeName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   scopeName: String - name of the scope.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   InvalidArgumentsException
  *   Any exceptions raised by the underlying platform

  Uri

  *   POST [http://localhost:8091/pools/default/buckets/](https://www.google.com/url?q=http://localhost:8091/pools/default/buckets/&sa=D&ust=1569855744485000)/collections -d name=

  #### Drop Scope

  Removes a scope.

  Signature

  

  

  

  

  

  void DropScope(string scopeName, [options])

  

  

  

  

  Parameters

  *   Required:

  *   collectionName: string - name of the collection.

  *   Optional:

  *   Timeout or timeoutMillis (int/duration) - the time allowed for the operation to be terminated. This is controlled by the client.

  Returns

  Throws

  *   ScopeNotFoundException
  *   Any exceptions raised by the underlying platform

  Uri

  *   DELETE [http://localhost:8091/pools/default/buckets/](https://www.google.com/url?q=http://localhost:8091/pools/default/buckets/&sa=D&ust=1569855744488000)/collections/

  # Types

  #### DesignDocument

  DesignDocument provides a means of mapping a design document into an object. It contains within it a map of View.

  

  

  

  

  

  

   type DesignDocument{

  

  String Name();

                  

          Map[String]IView Views();

  }

  

  

  

  

  

  #### View

  

  

  

  

  

   type View{

  

              String Map();

                  

              String Reduce();

  }

  

  

  

  

  ## 

  #### IQueryIndex Interface

  The IQueryIndex interface provides a means of mapping a query index into an object.

  

  

  

  

  

  

   interface IQueryIndex{

  

              String Name();

                  

          Bool IsPrimary();

  

          IndexType Type();

  

          String State();

  

          String Keyspace();

  

  Iterable IndexKey();

  

          Optional Condition();

  }

  

  

  

  

  

  #### AnalyticsDataset Interface

  AnalyticsDataset provides a means of mapping dataset details into an object.

  

  

  

  

  

  

   interface AnalyticsDataset{

  

              String Name();

                  

          String DataverseName();

                  

          String LinkName();

                  

          String BucketName();

  }

  

  

  

  

  #### AnalyticsIndex Interface

  AnalyticsIndex provides a means of mapping analytics index details into an object.

  

  

  

  

  

  

   interface AnalyticsDataset{

  

              String Name();

                  

          String DatasetName();

  

          String DataverseName();

                  

          Bool IsPrimary();

  }

  

  

  

  

  #### 

  #### BucketSettings

  BucketSettings provides a means of mapping bucket settings into an object.

  *   Name (string) - The name of the bucket.
  *   FlushEnabled (bool) - Whether or not flush should be enabled on the bucket. Default to false.
  *   RamQuotaMB (int) - Ram Quota in mb for the bucket. (rawRAM in the server payload)
  *   NumReplicas (int) - The number of replicas for documents.
  *   ReplicaIndexes (bool) - Whether replica indexes should be enabled for the bucket.
  *   BucketType {couchbase (sent on wire as membase), memcached, ephemeral} - The type of the bucket. Default to couchbase.
  *   EjectionMethod {fullEviction | valueOnly}. The eviction policy to use.
  *   maxTTL (int) - Value for the maxTTL of new documents created without a ttl.
  *   compressionMode {off | passive | active} - The compression mode to use.

  #### CreateBucketSettings

  CreateBucketSettings is a superset of BucketSettings providing one extra property:

  *   ConflictResolutionType {Timestamp (sent as lww) | SequenceNumber (sent as seqno)}. The conflict resolution type to use.

  The reasoning for this is that on Update ConflictResolutionType cannot be present in the JSON payload at all.

  

  #### UpsertIndeSearchIndex

  SearchIndex provides a means to map search indexes into object. The Params, SourceParams, and PlanParams fields are left to the SDK to decide what is idiomatic (e.g. JSONObject), the definitions of these fields is purposefully vague.

  

  

  

  

  

  type SearchIndex struct {

          // UUID is required for updates. It provides a means of ensuring consistency, the UUID must match the UUID value

          // for the index on the server.

          UUID string `json:"uuid"`

  

          Name string `json:"name"`

  

          // SourceName is the name of the source of the data for the index e.g. bucket name.

          SourceName string `json:"sourceName,omitempty"`

  

          // Type is the type of index, e.g. fulltext-index or fulltext-alias.

          Type string `json:"type"`

  

          // IndexParams are index properties such as store type and mappings.

          Params map[string]interface{} `json:"params"`

  

          // SourceUUID is the UUID of the data source, this can be used to more tightly tie the index to a source.

          SourceUUID string `json:"sourceUUID,omitempty"`

  

          // SourceParams are extra parameters to be defined. These are usually things like advanced connection and tuning

          // parameters.

          SourceParams map[string]interface{} `json:"sourceParams,omitempty"`

  

          // SourceType is the type of the data source, e.g. couchbase or nil depending on the Type field.

          SourceType string `json:"sourceType"`

  

          // PlanParams are plan properties such as number of replicas and number of partitions.

          PlanParams map[string]interface{} `json:"planParams,omitempty"`

  }

  

  

  

  

  

  

  #### IUser Interface

  The IUser interface provides a means of mapping user settings into an object.

  

  

  

  

  

  

   Interface IUser{

  

              String ID();

  

              String Name();

          

              Iterable Roles();

  }

  

  

  

  

  

  #### ICollectionSpec Interface

  

  

  

  

  

  

   Interface ICollectionSpec{

  

              String Name();

          

              String ScopeName();

  }

  

  

  

  

  

  #### IScopeSpec Interface

  

  

  

  

  

  

   Interface IScopeSpec{

  

              String Name();

          

              Iterable Collections();

  }

  

  

  

  

  

  

  

  

  # References

  *   Query index management

  *   [https://github.com/couchbaselabs/sdk-rfcs/blob/master/rfc/0003-indexmanagement.md](https://www.google.com/url?q=https://github.com/couchbaselabs/sdk-rfcs/blob/master/rfc/0003-indexmanagement.md&sa=D&ust=1569855744515000)
  *   [https://docs.couchbase.com/server/current/n1ql/n1ql-language-reference/](https://www.google.com/url?q=https://docs.couchbase.com/server/current/n1ql/n1ql-language-reference/&sa=D&ust=1569855744516000)

  *   Search index management

  *   [https://docs.google.com/document/d/1C4yfTj5u6ahRgk3ZIL_AkwPMeu9-hHY_lZcsDNeIP74](https://www.google.com/url?q=https://docs.google.com/document/d/1C4yfTj5u6ahRgk3ZIL_AkwPMeu9-hHY_lZcsDNeIP74&sa=D&ust=1569855744517000)
  *   [https://docs.couchbase.com/server/6.0/rest-api/rest-fts-indexing.html](https://www.google.com/url?q=https://docs.couchbase.com/server/6.0/rest-api/rest-fts-indexing.html&sa=D&ust=1569855744517000)
  *   [http://labs.couchbase.com/cbft/dev-guide/index-definitions/](https://www.google.com/url?q=http://labs.couchbase.com/cbft/dev-guide/index-definitions/&sa=D&ust=1569855744518000)

  *   Outdated but contains some useful definitions for fields.

  *   User Management

  *   [https://github.com/couchbaselabs/sdk-rfcs/blob/master/rfc/0022-usermgmt.md](https://www.google.com/url?q=https://github.com/couchbaselabs/sdk-rfcs/blob/master/rfc/0022-usermgmt.md&sa=D&ust=1569855744518000)

  *   Bucket Management

  *   [https://docs.couchbase.com/server/current/rest-api/rest-bucket-intro.html](https://www.google.com/url?q=https://docs.couchbase.com/server/current/rest-api/rest-bucket-intro.html&sa=D&ust=1569855744519000)

  *   Collection Management

  *   [https://github.com/couchbase/ns_server/commit/4c1a9ea20fbdb148f68ec2ad7be9eed4c071bf9e](https://www.google.com/url?q=https://github.com/couchbase/ns_server/commit/4c1a9ea20fbdb148f68ec2ad7be9eed4c071bf9e&sa=D&ust=1569855744519000)
  *   [https://docs.google.com/document/d/1X-v8GWQjplrMMaYwwWOzEuP4AUoDNIAvS39NmEjQ3_E/edit#heading=h.gprum229kohk](https://www.google.com/url?q=https://docs.google.com/document/d/1X-v8GWQjplrMMaYwwWOzEuP4AUoDNIAvS39NmEjQ3_E/edit%23heading%3Dh.gprum229kohk&sa=D&ust=1569855744520000)

  *   Views REST API

  *   [https://docs.couchbase.com/server/6.0/rest-api/rest-views-intro.html](https://www.google.com/url?q=https://docs.couchbase.com/server/6.0/rest-api/rest-views-intro.html&sa=D&ust=1569855744520000)

  *   Groups and LDAP Groups

  *   [https://docs.google.com/document/d/1wsjEmke80RW_sbW0ycS8yQl6rq5lzBbRWuelPZ1m9ZI/edit#](https://www.google.com/url?q=https://docs.google.com/document/d/1wsjEmke80RW_sbW0ycS8yQl6rq5lzBbRWuelPZ1m9ZI/edit%23&sa=D&ust=1569855744521000)
  *   [https://docs.google.com/document/d/1cFZOz9n6ZKyq_thxCSteuLrZ0rJEh7AMT3MFbOHCchM/edit](https://www.google.com/url?q=https://docs.google.com/document/d/1cFZOz9n6ZKyq_thxCSteuLrZ0rJEh7AMT3MFbOHCchM/edit&sa=D&ust=1569855744521000)
  *   [https://issues.couchbase.com/browse/MB-16035](https://www.google.com/url?q=https://issues.couchbase.com/browse/MB-16035&sa=D&ust=1569855744522000)

  *   Analytics management

  *   [https://docs.couchbase.com/server/current/analytics/5_ddl.html](https://www.google.com/url?q=https://docs.couchbase.com/server/current/analytics/5_ddl.html&sa=D&ust=1569855744522000)

  

  # Changes

  2019-09-30:

  *   Remove dataverse name checking from all Analytics options blocks so that if the dataverse name is set we do not check if the dataset already contains it.
  *   Added Condition to IQueryIndex.
  *   Changed User AvailableRoles to GetRoles.
  *   Change ConnectLink and DisconnectLink so that the name is optional, defaulting to Local.

  2019-09-18:

  *   Add FlushNotEnabledException to bucket Flush operation

  2019-09-03:

  *    Add numReplicas option to QueryIndexManager CreatePrimaryIndex

  

  [[a]](#cmnt_ref1)Java path-finding impl also has AND `using` = \"gsi\"

  

  

  [[b]](#cmnt_ref2)I believe this is from back in the very first versions of N1QL, where it was required to be specified.  I don't think we need to bring this behaviour forward.

  

  

  [[c]](#cmnt_ref3)Java impl does this by getting all indexes and doing BUILD INDEX on any currently set to deferred.  Thought we weren't doing racey stuff like that in client as general rule?

  

  

  [[d]](#cmnt_ref4)That wouldn't be racy, since your going to build exactly the indices that you find during the first call.  From a functional perspective, only indexes that were deferred at the time you called the method are being built, which I think makes sense.

  

  

  [[e]](#cmnt_ref5)+charles.dixon@couchbase.com Should there be an optional `dataverse` parameter?

  

  

  [[f]](#cmnt_ref6)And an optional `force` parameter?

  

  

  [[g]](#cmnt_ref7)I guess we should make an escape style of parameter to future proof it.

  

  

  [[h]](#cmnt_ref8)I don't think we need to have an escape hatch on something that only exists for ease of use.  Relatedly, why does CONNECT LINK even accept a dataverse name?

  

  

  [[i]](#cmnt_ref9)There is still a question around this, I suggest that we just accept a string Name rather than a ScopeSpec and we don't create collections as a part of this. It isn't attempting to be an atomic operation that way.

  

  

  [[j]](#cmnt_ref10)I would be in favour of this change.

  

  

  [[k]](#cmnt_ref11)This is missing the function definition below like the others.

  

  

  [[l]](#cmnt_ref12)There seems to be some confusion over what this command does. The collections design doc states that there will be a flush endpoint that we can call over REST. I don't believe that it's implemented by ns server yet though.

  

  

  [[m]](#cmnt_ref13)https://docs.google.com/document/d/1X-v8GWQjplrMMaYwwWOzEuP4AUoDNIAvS39NmEjQ3_E/edit#heading=h.8c7d3zbqy7i is what I'm referring to

  

  

  [[n]](#cmnt_ref14)Server-side flushing was not implemented, instead it was decided that flushing a collection could be achieved trivially by the SDK through the destruction and recreation of the collection.

  
  [[m]](#cmnt_ref13)https://docs.google.com/document/d/1X-v8GWQjplrMMaYwwWOzEuP4AUoDNIAvS39NmEjQ3_E/edit#heading=h.8c7d3zbqy7i is what I'm referring to

  

  

  [[n]](#cmnt_ref14)Server-side flushing was not implemented, instead it was decided that flushing a collection could be achieved trivially by the SDK through the destruction and recreation of the collection.

  
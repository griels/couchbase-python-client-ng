from couchbase_core.cluster import PasswordAuthenticator
from datetime import timedelta
from couchbase.cluster import Cluster, ClusterOptions, QueryOptions, ClusterTimeoutOptions, QueryScanConsistency
from couchbase_core.cluster import PasswordAuthenticator
from couchbase.management.collections import CollectionSpec
from couchbase.exceptions import ScopeAlreadyExistsException, CollectionAlreadyExistsException, ScopeNotFoundException
import traceback
import couchbase
couchbase.enable_logging()
import logging
import sys
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
couchbase.enable_logging()

def main():
	pass_auth = PasswordAuthenticator('Administrator', 'password')
	timeout = timedelta(seconds=10)
	timeout_options = ClusterTimeoutOptions(kv_timeout=timeout,
										    query_timeout=timeout)
	options = ClusterOptions(authenticator=pass_auth,timeout_options=timeout_options)
	cluster = Cluster(connection_string='couchbase://10.143.210.101', options=options)
	bucket = cluster.bucket('bucket-1')
	try:
		bucket.collections().create_scope('scope-1')
	except ScopeAlreadyExistsException:
		pass
	while True:
		import logging
		logging.info("Trying to create collection")
		try:
			bucket.collections().create_collection(CollectionSpec('collection-1', 'scope-1'))
			break
		except Exception as e:
			try:
				logging.error(traceback.format_exc())
				raise e
			except CollectionAlreadyExistsException:
				break
			except ScopeNotFoundException:
				continue

	import datetime
	deadline = datetime.datetime.now()+datetime.timedelta(seconds=60)
	collection=None
	while True:
		try:
			collection = bucket.scope('scope-1').collection('collection-1')
			break
		except:
			if datetime.datetime.now()<deadline:
				continue
			raise

	try:
		cluster.query("CREATE PRIMARY INDEX `primary_idx` ON default:`bucket-1`.`scope-1`.`collection-1`")
		cluster.query("CREATE INDEX `primary_idx` ON default:`bucket-1`.`scope-1`.`collection-1`(field1)")
	except Exception as e:
		logging.error(traceback.format_exc())

	doc = {'field1': "value1"}
	for i in range(10000):
		key = str(i)
		collection.upsert(key, doc, persist_to=0, replicate_to=0, ttl=0)

	statement = "SELECT * FROM default:`bucket-1`.`scope-1`.`collection-1` USE KEYS[$1];"

	while True:
		for i in range(10000):
			args = [str(i)]
			query_opts = QueryOptions(adhoc=False, scan_consistency=QueryScanConsistency.NOT_BOUNDED, positional_parameters=args)
			res = cluster.query(statement, query_opts)
			for row in res:
				print(row)


if __name__ == '__main__':
    main()
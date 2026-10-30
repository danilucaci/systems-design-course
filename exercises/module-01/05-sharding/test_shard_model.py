import unittest
from shard_model import ShardedStore, Unavailable, StaleRoute


class ShardingTests(unittest.TestCase):
    def test_frozen_bucket_rejects_writes_and_cutover_fences_old_route(self):
        store=ShardedStore(); old=store.route('tenant-a'); store.write('tenant-a','v1',old)
        store.freeze(old.bucket)
        with self.assertRaises(Unavailable): store.write('tenant-a','v2',old)
        store.copy(old.bucket,'C'); store.cutover(old.bucket)
        with self.assertRaises(StaleRoute): store.write('tenant-a','stale',old)
        self.assertEqual(store.read('tenant-a',store.route('tenant-a')),'v1')

    def test_copy_is_required_and_abort_reopens_source(self):
        store=ShardedStore(); route=store.route('a'); store.freeze(route.bucket)
        with self.assertRaises(ValueError): store.cutover(route.bucket)
        store.abort(route.bucket); store.write('a','value',route)
        self.assertEqual(store.read('a',route),'value')

    def test_directory_partition_fails_closed(self):
        store=ShardedStore(); route=store.route('a'); store.directory_available=False
        with self.assertRaises(Unavailable): store.write('a','value',route)

    def test_only_migrated_bucket_changes_owner(self):
        store=ShardedStore(); before=dict(store.owners); bucket=3
        store.freeze(bucket); store.copy(bucket,'C'); store.cutover(bucket)
        self.assertEqual([i for i in before if before[i]!=store.owners[i]],[bucket])

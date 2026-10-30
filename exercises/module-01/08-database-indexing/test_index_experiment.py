import unittest
from db_fixture import DatabaseFixture, DSN
from index_experiment import experiment


def walk(plan):
    yield plan
    for child in plan.get('Plans',[]): yield from walk(child)


@unittest.skipUnless(DSN,'Set MODULE1_DATABASE_URL for real PostgreSQL query plans')
class IndexTests(DatabaseFixture,unittest.TestCase):
    def test_matching_index_avoids_sort_and_reduces_buffer_accesses(self):
        with self.connect() as connection: result=experiment(connection)
        before=result['before']['Plan']; after=result['after']['Plan']
        self.assertEqual(after['Actual Rows'],20)
        self.assertTrue(any(p.get('Index Name')=='index_lab_owner_created' for p in walk(after)))
        self.assertFalse(any(p['Node Type']=='Sort' for p in walk(after)))
        accesses=lambda p:p.get('Shared Hit Blocks',0)+p.get('Shared Read Blocks',0)
        self.assertLess(accesses(after),accesses(before))

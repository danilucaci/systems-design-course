import unittest
from uuid import uuid4
import psycopg
from db_fixture import DatabaseFixture, DSN


@unittest.skipUnless(DSN, 'Set MODULE1_DATABASE_URL for real PostgreSQL checks')
class SchemaTests(DatabaseFixture, unittest.TestCase):
    def test_foreign_owner_cannot_attach_a_stop(self):
        journey=uuid4()
        with self.connect() as connection:
            connection.execute("INSERT INTO journeys(id,owner_id,name) VALUES (%s,'00000000-0000-0000-0000-000000000001','Trip')",(journey,))
        with self.assertRaises(psycopg.errors.ForeignKeyViolation), self.connect() as connection:
            connection.execute("INSERT INTO journey_stops VALUES ('00000000-0000-0000-0000-000000000002',%s,0,%s)",(journey,uuid4()))

    def test_failed_transaction_does_not_leave_parent_row(self):
        journey=uuid4()
        with self.assertRaises(psycopg.errors.CheckViolation), self.connect() as connection:
            connection.execute("INSERT INTO journeys(id,owner_id,name) VALUES (%s,'00000000-0000-0000-0000-000000000001','Trip')",(journey,))
            connection.execute("INSERT INTO journey_stops VALUES ('00000000-0000-0000-0000-000000000001',%s,-1,%s)",(journey,uuid4()))
        with self.connect() as connection:
            self.assertEqual(connection.execute('SELECT count(*) FROM journeys WHERE id=%s',(journey,)).fetchone()[0],0)

    def test_stale_version_cannot_overwrite_newer_edit(self):
        journey=uuid4()
        with self.connect() as connection:
            connection.execute("INSERT INTO journeys(id,owner_id,name) VALUES (%s,'00000000-0000-0000-0000-000000000001','Initial')",(journey,))
            self.assertEqual(connection.execute("UPDATE journeys SET name='First',version=version+1 WHERE id=%s AND version=1",(journey,)).rowcount,1)
            self.assertEqual(connection.execute("UPDATE journeys SET name='Stale',version=version+1 WHERE id=%s AND version=1",(journey,)).rowcount,0)

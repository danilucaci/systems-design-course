"""Creates and drops only a uniquely named schema owned by this test run."""
import os
from pathlib import Path
from uuid import uuid4
import psycopg
from psycopg import sql

DSN = os.environ.get('MODULE1_DATABASE_URL')
ROOT = Path(__file__).resolve().parent


class DatabaseFixture:
    @classmethod
    def setUpClass(cls):
        cls.schema = 'm1_test_' + uuid4().hex
        with psycopg.connect(DSN) as connection:
            connection.execute(sql.SQL('CREATE SCHEMA {}').format(sql.Identifier(cls.schema)))
            connection.execute(sql.SQL('SET search_path TO {}').format(sql.Identifier(cls.schema)))
            connection.execute((ROOT/'03-data-modeling/schema.sql').read_text())
            connection.execute("INSERT INTO users(id,email) VALUES ('00000000-0000-0000-0000-000000000001','alice@example.test'),('00000000-0000-0000-0000-000000000002','bob@example.test')")

    @classmethod
    def tearDownClass(cls):
        with psycopg.connect(DSN) as connection:
            connection.execute(sql.SQL('DROP SCHEMA {} CASCADE').format(sql.Identifier(cls.schema)))

    def connect(self):
        return psycopg.connect(DSN, options=f'-csearch_path={self.schema}')

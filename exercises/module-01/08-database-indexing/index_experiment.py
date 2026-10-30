"""Synthetic PostgreSQL access-path comparison; never disables sequential scans."""
import json
import os
from uuid import uuid4
import psycopg
from psycopg import sql

QUERY='SELECT id,created_at,payload FROM index_lab_events WHERE owner_id=42 ORDER BY created_at DESC,id DESC LIMIT 20'


def experiment(connection):
    connection.execute('CREATE TABLE index_lab_events(id bigint PRIMARY KEY,owner_id integer NOT NULL,created_at timestamptz NOT NULL,payload text NOT NULL)')
    connection.execute("INSERT INTO index_lab_events SELECT i,i%1000,timestamptz '2026-01-01 00:00:00+00'+i*interval '1 second',repeat('x',100) FROM generate_series(1,100000) AS i")
    connection.execute('ANALYZE index_lab_events')
    before=connection.execute('EXPLAIN (ANALYZE,BUFFERS,FORMAT JSON) '+QUERY).fetchone()[0][0]
    connection.execute('CREATE INDEX index_lab_owner_created ON index_lab_events(owner_id,created_at DESC,id DESC)')
    connection.execute('ANALYZE index_lab_events')
    after=connection.execute('EXPLAIN (ANALYZE,BUFFERS,FORMAT JSON) '+QUERY).fetchone()[0][0]
    return {'server_version':connection.execute('SHOW server_version').fetchone()[0],
            'fixture_rows':100000,'query':QUERY,'before':before,'after':after,
            'index_bytes':connection.execute("SELECT pg_relation_size('index_lab_owner_created')").fetchone()[0]}


if __name__=='__main__':
    schema='m1_index_'+uuid4().hex
    with psycopg.connect(os.environ['MODULE1_DATABASE_URL'],autocommit=True) as connection:
        connection.execute(sql.SQL('CREATE SCHEMA {}').format(sql.Identifier(schema)))
        try:
            connection.execute(sql.SQL('SET search_path TO {}').format(sql.Identifier(schema)))
            print(json.dumps(experiment(connection),indent=2))
        finally:
            connection.execute(sql.SQL('DROP SCHEMA {} CASCADE').format(sql.Identifier(schema)))

import os
from pathlib import Path
import psycopg

SCHEMA = Path(__file__).with_name('schema.sql').read_text()
ALICE = '00000000-0000-0000-0000-000000000001'
BOB = '00000000-0000-0000-0000-000000000002'

if __name__ == '__main__':
    with psycopg.connect(os.environ['MODULE1_DATABASE_URL']) as connection:
        connection.execute(SCHEMA)
        connection.execute('INSERT INTO users(id,email) VALUES (%s,%s),(%s,%s) ON CONFLICT DO NOTHING',
                           (ALICE, 'alice@example.test', BOB, 'bob@example.test'))
    print('Lab schema and synthetic users are ready; no existing rows were deleted.')

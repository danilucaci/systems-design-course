import asyncio
import hashlib
import unittest
from uuid import UUID, uuid4
from httpx import ASGITransport, AsyncClient
from api import create_app
from db_fixture import DatabaseFixture, DSN

ALICE = UUID('00000000-0000-0000-0000-000000000001')
BOB = UUID('00000000-0000-0000-0000-000000000002')
AUTH = {'Authorization': 'Bearer alice-token'}


@unittest.skipUnless(DSN, 'Set MODULE1_DATABASE_URL for real PostgreSQL integration checks')
class ApiTests(DatabaseFixture, unittest.IsolatedAsyncioTestCase):
    def client(self,raise_errors=True):
        app=create_app(DSN,{'alice-token':ALICE,'bob-token':BOB},self.schema)
        return AsyncClient(transport=ASGITransport(app=app,raise_app_exceptions=raise_errors),base_url='http://lab')

    async def post(self,client,key,name='Trip'):
        return await client.post('/v1/journeys',json={'name':name},headers={**AUTH,'Idempotency-Key':key})

    async def test_authentication_and_validation(self):
        async with self.client() as client:
            self.assertEqual((await client.get('/v1/journeys')).status_code,401)
            self.assertEqual((await client.get('/v1/journeys?limit=999',headers=AUTH)).status_code,422)
            self.assertEqual((await self.post(client,'blank','   ')).status_code,422)

    async def test_replay_and_payload_conflict(self):
        async with self.client() as client:
            key=str(uuid4()); first=await self.post(client,key); replay=await self.post(client,key)
            self.assertEqual((first.status_code,replay.status_code),(201,200))
            self.assertEqual(first.json(),replay.json())
            self.assertEqual((await self.post(client,key,'Changed')).status_code,409)

    async def test_replay_keeps_original_snapshot_after_later_edit(self):
        async with self.client() as client:
            key=str(uuid4()); first=await self.post(client,key)
            with self.connect() as connection:
                connection.execute("UPDATE journeys SET name='Edited',version=version+1 WHERE id=%s",(UUID(first.json()['id']),))
            self.assertEqual((await self.post(client,key)).json(),first.json())

    async def test_owner_filter_applies_to_detail_and_list(self):
        async with self.client() as client:
            item=(await self.post(client,str(uuid4()))).json()
            bob={'Authorization':'Bearer bob-token'}
            self.assertEqual((await client.get('/v1/journeys/'+item['id'],headers=bob)).status_code,404)
            self.assertEqual((await client.get('/v1/journeys',headers=bob)).json()['items'],[])

    async def test_concurrent_same_key_creates_one_journey(self):
        key=str(uuid4())
        async with self.client() as client: responses=await asyncio.gather(self.post(client,key),self.post(client,key))
        self.assertEqual(sorted(item.status_code for item in responses),[200,201])
        self.assertEqual(responses[0].json()['id'],responses[1].json()['id'])

    async def test_cursor_pages_do_not_repeat_existing_rows(self):
        async with self.client() as client:
            for _ in range(3): await self.post(client,str(uuid4()))
            first=(await client.get('/v1/journeys?limit=2',headers=AUTH)).json()
            second=(await client.get('/v1/journeys',params={'limit':2,'after':first['next_after']},headers=AUTH)).json()
            self.assertTrue(first['next_after'])
            self.assertFalse({x['id'] for x in first['items']} & {x['id'] for x in second['items']})

    async def test_lock_timeout_returns_retryable_failure(self):
        key=str(uuid4())
        lock=int.from_bytes(hashlib.blake2b(f'{ALICE}:create:{key}'.encode(),digest_size=8).digest(),'big',signed=True)
        with self.connect() as connection:
            connection.execute('SELECT pg_advisory_xact_lock(%s)',(lock,))
            async with self.client() as client:
                response=await self.post(client,key)
                self.assertEqual(response.status_code,503)
                self.assertEqual(response.headers['Retry-After'],'1')
        async with self.client() as client: self.assertEqual((await self.post(client,key)).status_code,201)

    async def test_failed_operation_record_rolls_back_journey(self):
        key='fail_second_statement'; name='must-rollback-'+str(uuid4())
        with self.connect() as connection:
            connection.execute("ALTER TABLE create_requests ADD CONSTRAINT test_rejection CHECK(operation_key <> 'fail_second_statement')")
        try:
            async with self.client(raise_errors=False) as client:
                self.assertEqual((await self.post(client,key,name)).status_code,500)
            with self.connect() as connection:
                self.assertEqual(connection.execute('SELECT count(*) FROM journeys WHERE name=%s',(name,)).fetchone()[0],0)
                self.assertEqual(connection.execute('SELECT count(*) FROM create_requests WHERE operation_key=%s',(key,)).fetchone()[0],0)
        finally:
            with self.connect() as connection: connection.execute('ALTER TABLE create_requests DROP CONSTRAINT test_rejection')

"""Local teaching API. Demo bearer tokens are supplied by the caller, not an identity provider."""
import hashlib
import hmac
import json
import re
from typing import Annotated
from uuid import UUID, uuid4

import psycopg
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb
from fastapi import Depends, FastAPI, Header, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, ConfigDict, Field, field_validator


class JourneyInput(BaseModel):
    model_config = ConfigDict(extra='forbid')
    name: str = Field(min_length=1, max_length=120)

    @field_validator('name')
    @classmethod
    def clean_name(cls, value):
        value = value.strip()
        if not value: raise ValueError('name cannot be blank')
        return value


def create_app(database_url: str, principals: dict[str, UUID], schema: str = 'public') -> FastAPI:
    if not re.fullmatch(r'[a-z][a-z0-9_]{0,62}', schema): raise ValueError('invalid schema')
    if not principals: raise ValueError('at least one demo principal is required')
    app = FastAPI(title='Module 1 journey lab')
    bearer = HTTPBearer(auto_error=False)

    def owner(credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)]):
        if credentials:
            for token, user_id in principals.items():
                if hmac.compare_digest(credentials.credentials.encode(), token.encode()): return user_id
        raise HTTPException(401, 'Valid bearer credentials required', headers={'WWW-Authenticate': 'Bearer'})

    def connect():
        return psycopg.connect(database_url, row_factory=dict_row,
                               options=f'-csearch_path={schema} -cstatement_timeout=3000 -clock_timeout=1000')

    @app.exception_handler(psycopg.OperationalError)
    @app.exception_handler(psycopg.errors.QueryCanceled)
    def temporary_failure(request, error):
        return JSONResponse(status_code=503, content={'detail': 'Database temporarily unavailable; retry creation with the same operation key'}, headers={'Retry-After': '1'})

    @app.post('/v1/journeys')
    def create_journey(body: JourneyInput, user_id: Annotated[UUID, Depends(owner)],
                       operation_key: Annotated[str, Header(alias='Idempotency-Key', min_length=1, max_length=80)]):
        if not re.fullmatch(r'[A-Za-z0-9._:-]+', operation_key): raise HTTPException(422, 'Invalid operation key')
        digest = hashlib.sha256(json.dumps(body.model_dump(), sort_keys=True, separators=(',', ':')).encode()).digest()
        lock = int.from_bytes(hashlib.blake2b(f'{user_id}:create:{operation_key}'.encode(), digest_size=8).digest(), 'big', signed=True)
        with connect() as connection:
            connection.execute('SELECT pg_advisory_xact_lock(%s)', (lock,))
            previous = connection.execute('SELECT payload_hash,response_snapshot FROM create_requests WHERE owner_id=%s AND operation_key=%s', (user_id, operation_key)).fetchone()
            if previous:
                if bytes(previous['payload_hash']) != digest: raise HTTPException(409, 'Operation key was used with another payload')
                journey = previous['response_snapshot']
                status = 200
            else:
                journey_id = uuid4()
                journey = connection.execute('INSERT INTO journeys(id,owner_id,name) VALUES (%s,%s,%s) RETURNING id,name,created_at,version', (journey_id, user_id, body.name)).fetchone()
                connection.execute('INSERT INTO create_requests(owner_id,operation_key,payload_hash,journey_id,response_snapshot) VALUES (%s,%s,%s,%s,%s)', (user_id, operation_key, digest, journey_id, Jsonb(jsonable_encoder(journey))))
                status = 201
        return JSONResponse(status_code=status, content=jsonable_encoder(journey), headers={'Location': f'/v1/journeys/{journey["id"]}', 'Cache-Control': 'private, no-store'})

    @app.get('/v1/journeys/{journey_id}')
    def get_journey(journey_id: UUID, user_id: Annotated[UUID, Depends(owner)]):
        with connect() as connection:
            row = connection.execute('SELECT id,name,created_at,version FROM journeys WHERE owner_id=%s AND id=%s', (user_id, journey_id)).fetchone()
        if not row: raise HTTPException(404, 'Journey not found')
        return JSONResponse(content=jsonable_encoder(row), headers={'Cache-Control': 'private, no-store'})

    @app.get('/v1/journeys')
    def list_journeys(user_id: Annotated[UUID, Depends(owner)], after: UUID | None = None,
                      limit: Annotated[int, Query(ge=1, le=50)] = 20):
        with connect() as connection:
            rows = connection.execute('SELECT id,name,created_at,version FROM journeys WHERE owner_id=%s AND (%s::uuid IS NULL OR id>%s) ORDER BY id LIMIT %s', (user_id, after, after, limit+1)).fetchall()
        page = rows[:limit]
        return JSONResponse(content=jsonable_encoder({'items': page, 'next_after': page[-1]['id'] if len(rows)>limit else None}), headers={'Cache-Control': 'private, no-store'})

    return app


if __name__ == '__main__':
    import os
    import uvicorn
    app = create_app(os.environ['MODULE1_DATABASE_URL'], {'alice-lab-token': UUID('00000000-0000-0000-0000-000000000001'), 'bob-lab-token': UUID('00000000-0000-0000-0000-000000000002')})
    uvicorn.run(app, host='127.0.0.1', port=8001)

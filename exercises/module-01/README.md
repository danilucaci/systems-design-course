# Module 1 local labs

These labs use synthetic data. The API, schema, and index experiment use a real PostgreSQL 18 instance. Caching, sharding, consistent hashing, CAP, and capacity examples are local models with explicitly limited guarantees. Reading the HTML course requires none of these services and makes no background requests.

## Environment

Use Python 3.12 and Docker with the daemon running. From the repository root:

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r exercises/module-01/requirements.txt
```

If you use uv, `uv venv --python 3.12 .venv` and `uv pip install --python .venv/bin/python -r exercises/module-01/requirements.txt` are equivalent setup options. The versions are pinned to the environment used for this batch, not a promise that future releases have the same behavior. PostgreSQL minor updates may change planner costs and timings; record the server version with measurements.

Start a disposable database. It binds only to loopback. The password below is a public, local-lab value and must never protect real data:

```bash
docker run --detach --rm --name system-course-module1-db \
  --env POSTGRES_USER=course --env POSTGRES_PASSWORD=course_lab_only \
  --env POSTGRES_DB=course --publish 127.0.0.1:55432:5432 postgres:18
export MODULE1_DATABASE_URL=postgresql://course:course_lab_only@127.0.0.1:55432/course
docker exec system-course-module1-db pg_isready -U course -d course
```

Wait for pg_isready to report acceptance before continuing. If this named container already exists, inspect it rather than creating another with the same name. No host database directory is mounted; stopping this `--rm` container discards its lab data. Do not substitute a production database URL.

## Checks

```bash
.venv/bin/python exercises/module-01/run_checks.py
```

The runner discovers all nine exercise directories. PostgreSQL checks create uniquely named schemas and remove only those schemas. They are skipped, with an explicit reason, if MODULE1_DATABASE_URL is absent. A passing run with skips does not validate the API, schema, or query plans. Imports still require the pinned dependencies.

The networking checks are deterministic mocks of transport boundaries; a live verified HTTPS probe is separate:

```bash
.venv/bin/python exercises/module-01/01-networking-essentials/network_probe.py https://www.python.org/
```

This probe opens a fresh HTTP/1.1 HTTPS-over-TCP connection and limits its body sample. Its socket timeout is not a total deadline and does not directly bound system DNS resolution. It does not benchmark browser HTTP/2 or HTTP/3, follow redirects, or expose a clean isolated TCP measurement.

## API and schema

Initialize the fresh lab schema, then run the loopback-only API:

```bash
.venv/bin/python exercises/module-01/03-data-modeling/bootstrap.py
.venv/bin/python exercises/module-01/02-api-design/api.py
```

In another terminal, send a synthetic authenticated creation:

```bash
curl -i http://127.0.0.1:8001/v1/journeys \
  -H 'Authorization: Bearer alice-lab-token' \
  -H 'Idempotency-Key: weekend-001' \
  -H 'Content-Type: application/json' \
  -d '{"name":"Weekend route"}'
```

Repeat the same intent with the same key and body. First creation returns 201; replay returns 200 with the original response snapshot. A changed accepted payload under that key returns 409. Use bob-lab-token to confirm that Alice's resource is hidden. The list endpoint accepts `limit` from 1 to 50 and an optional UUID `after`; it sorts UUIDs ascending, not chronologically.

The server-configured demo token map illustrates identity and ownership only. There is no identity provider, session management, browser CORS setup, public HTTPS listener, production connection pool, migration framework, event broker, or delete endpoint. Do not publish the lab server. The schema and transaction tests validate the narrower promises taught in these lessons.

## Other experiments

```bash
.venv/bin/python exercises/module-01/06-consistent-hashing/hash_ring.py
.venv/bin/python exercises/module-01/08-database-indexing/index_experiment.py
.venv/bin/python exercises/module-01/09-numbers-to-know/capacity.py
```

The index experiment creates its own uniquely named schema, seeds 100,000 synthetic rows, compares EXPLAIN ANALYZE plans without and with a matching index, then removes its schema. It leaves planner choices enabled. Timing and cache state vary; compare the plan, buffer accesses, and write/storage cost rather than quoting a universal speedup. The saved observed-plan.json records one actual authoring run.

Caching and partition exercises are driven by their tests and worked solutions. The cache coordinates only one asyncio event loop. The shard model executes sequential freeze/copy/cutover steps in memory. The hash ring assigns owners without moving data. The CAP model uses a fixed primary for its CP case and deliberately omits failover and crash durability. None is a distributed database implementation.

## Cleanup

Stop the API with Ctrl-C in its terminal, then remove only this lab container:

```bash
docker stop system-course-module1-db
```

The container removes itself and loses the disposable data. Keep source files and pinned requirements; .venv is ignored by Git. Each lesson links a worked solution so you can compare predictions before reading answers.

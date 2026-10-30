# API design — worked solution

Use the [lab guide](../README.md) to run the server. Send `Authorization: Bearer alice-lab-token`, `Idempotency-Key: trip-001`, and `{"name":"Weekend route"}` to `POST /v1/journeys`. A first creation returns 201, a Location header, and a journey identifier. Repeating that key with the same accepted payload returns 200 and the original response snapshot. Changing the name under that key returns 409. Generate a fresh key for a genuinely different intended creation.

Bob's detail request returns 404, and his list excludes Alice's journey. The authorization condition belongs in SQL, not in a frontend array filter. Missing credentials return 401. The synthetic token map is a local teaching substitute for an identity provider and must not be deployed as real authentication.

For pagination, record each page's IDs and next cursor. A page of exactly two items can be the final page; requesting a third row internally determines whether another cursor is necessary. The actual lab sorts UUIDs in ascending order, so its list is not a newest-first feed.

A chronological contract can order `created_at DESC, id DESC` and carry both values in an opaque cursor. The next-page query retains the owner filter and uses:

```sql
SELECT id, name, created_at
FROM journeys
WHERE owner_id = $1
  AND (created_at, id) < ($2::timestamptz, $3::uuid)
ORDER BY created_at DESC, id DESC
LIMIT $4;
```

These are PostgreSQL positional parameters, not a complete psycopg invocation. Bind parameters using the driver's syntax in application code. A supporting index begins with owner and then the ordering tuple. Validate and bind the cursor to its filter/order contract; never accept a cursor as evidence of authorization.

A concurrent new journey ahead of the cursor belongs on an earlier page and can be absent from the current traversal. This is an explicitly live list. For a consistent export, use a server-managed snapshot or materialized export with a defined expiry and access policy.

Publishing directly to a broker after commit leaves a crash window. Publishing before commit can announce a journey that later rolls back. An outbox records an event beside the journey in the same database transaction; a worker publishes it with retries, and consumers deduplicate by stable event identity. Delivery and downstream side effects still need their own contracts. The API lab deliberately contains no broker or outbox implementation.

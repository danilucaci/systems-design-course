# Database indexing — worked solution

The supplied observed-plan.json records one PostgreSQL 18.6 run, with a sequential scan and sort before the composite index and an ordered index scan afterward. Root shared-buffer accesses were 1,924 before and 23 after: 20 shared hits plus 3 shared reads. The index occupied 4,079,616 bytes. Your timing and plan details may differ; retain your server version and fixture description.

Read the scan below Limit. Both plans return twenty rows, but the pre-index path must inspect a much larger relation and sort matching candidates. Parent buffer counters include child work; do not sum the tree. A shared read means a PostgreSQL buffer miss, not necessarily an uncached physical device access.

For a chronological owner list, use an index on `(owner_id, created_at DESC, id DESC)` and a continuation predicate `(created_at, id) < (cursor_time, cursor_id)` while retaining owner equality. Fetch limit plus one and publish a cursor only when more rows exist. A timestamp without the ID tie-breaker can skip equal-time rows.

A global newest feed has no owner equality, so a time/ID-leading index can provide the direct global order. PostgreSQL 18 may find other strategies for some distributions, but an owner-leading index is not the same access path. Separate indexes can sometimes combine filters without preserving the ordered LIMIT benefit of one composite structure.

Before deployment, measure write latency and throughput, WAL/I/O, index size, and cache pressure on representative inserts and updates. Account for concurrent build behavior and verify that the index is valid afterward. The local experiment uses a normal build in a disposable schema and does not validate a production rollout.

The automated check keeps sequential scans enabled, checks the chosen index and missing Sort node, verifies twenty results, and compares buffer work. It avoids exact timing assertions because they would be sensitive to unrelated scheduling and cache state.

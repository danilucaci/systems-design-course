# Database indexing

Lesson 1.08 · Core concepts

## A. Learning objectives and prerequisites

You should be able to derive an index from a concrete query, read the important parts of a PostgreSQL execution plan, explain the order of a composite B-tree, and measure the write and storage cost of the improvement. You should also recognize when a sequential scan is a reasonable choice rather than evidence that the database ignored your work.

Read [data modeling](03-data-modeling.md) and [API design](02-api-design.md). The experiment uses PostgreSQL 18 and 100,000 synthetic rows in a uniquely owned lab schema. Its recorded timings are observations from one local run, not production benchmarks or universal latency numbers.

## B. Mental model and intuition

An index is an additional structure maintained to make particular access paths cheaper. It trades write work and space for fewer comparisons, fewer data-page visits, useful ordering, or a directly enforced uniqueness rule. The right question is “which rows and order does this query need?” rather than “which columns should have an index?”

Imagine a journey list that needs the twenty newest rows belonging to one owner. A table scan can inspect every row, discard other owners, and sort the survivors. A matching index can navigate to that owner's ordered range and stop after enough rows. The benefit comes from avoiding work, not from a magical property attached to the column name.

Your frontend's pagination contract matters here. A stable ordering tuple and bounded page size give the database a precise early-stop opportunity. Asking for every row, sorting in application memory, and then displaying twenty items defeats much of the index's potential value.

## C. Deep technical explanation

### B-tree structure and heap access

A B-tree maintains ordered keys in pages with a balanced navigation structure. Searches traverse internal pages to a relevant leaf range, then scan suitable entries. A table's rows live separately in PostgreSQL's heap, so an ordinary index scan commonly visits heap pages to retrieve selected values and check tuple visibility. A short logical lookup can still involve many page accesses when many scattered rows qualify.

The familiar logarithmic-search explanation is useful but incomplete for system design. Page size, cache residency, selectivity, row width, physical correlation, MVCC visibility, and result count influence actual cost. An index finding half a large table can be less efficient than a sequential scan, especially when fetching heap pages in scattered order.

An index can also provide output order. A query that needs `ORDER BY created_at DESC, id DESC LIMIT 20` benefits when the scan already produces that order after its equality filters. Avoiding a large sort and stopping early can matter more than the raw search complexity.

### Composite order follows the query

For the synthetic feed, the relevant index is `(owner_id, created_at DESC, id DESC)`. Owner equality selects one contiguous region; within it, time and ID provide the required newest-first order. The ID breaks timestamp ties. A keyset continuation can use the same tuple ordering, keeping filtering, order, cursor, and index aligned.

Separate indexes on owner and creation time are not equivalent. PostgreSQL can combine indexes for some filters, but a bitmap combination generally does not preserve the desired index order for an immediate ordered LIMIT. The planner must evaluate the whole query rather than collecting every index whose column name appears in it.

Avoid the absolute claim that a composite B-tree is unusable unless its first column is filtered. PostgreSQL 18 has additional strategies, including skip scans in suitable cases. Leading equality constraints and the first relevant range remain central to understanding efficient navigation; use the actual version's plan to evaluate other shapes. [PostgreSQL 18 multicolumn indexes](https://www.postgresql.org/docs/18/indexes-multicolumn.html).

A different feed may need a different index. An unscoped global newest-events query does not get the same direct ordered range from an owner-leading index. A query that filters by owner but orders by name also has a different ordering requirement. Do not create a universal wide index and assume its permutations are interchangeable.

### Selectivity, expressions, and partial indexes

Selectivity describes how much of the relation qualifies. A rare owner can benefit from an index while a very common status may not. Data skew matters: the average number of rows per owner can hide a large tenant with a very different plan. Statistics help the planner estimate these populations, and ANALYZE updates them.

Write predicates that expose the intended range. Comparing a timestamp to lower and upper bounds is often more directly supported by a normal timestamp index than applying a date conversion to every row. Ensure the bounds represent the desired timezone; a local calendar day across a daylight-saving transition is not always 86,400 seconds.

Expression indexes can support a matching expression such as a normalized lookup, and partial indexes can store only rows satisfying a useful stable predicate, such as active tasks. The query must be compatible with the index expression or predicate under planner rules. Parameterization and prepared-plan choices can affect what is provable, so inspect the actual application query rather than a hand-edited version that happens to use constants. [CREATE INDEX documentation](https://www.postgresql.org/docs/18/sql-createindex.html).

### Read EXPLAIN as a work plan

Plain EXPLAIN shows the estimated plan. EXPLAIN ANALYZE executes the query and records observed work. Planner cost values are internal estimates, not milliseconds. Compare estimated and actual row counts, scan choice, filters, sort behavior, loop counts, and buffers before declaring the query solved. [PostgreSQL EXPLAIN](https://www.postgresql.org/docs/18/using-explain.html).

Plans are trees. A Limit can sit above a Sort above a Sequential Scan. The root returning twenty rows does not mean only twenty table rows were examined. Inspect the child scan and removed-row information. Where a node executes multiple loops, actual row and timing figures need interpretation with their loop counts rather than being treated as one global total.

Buffers describe accesses through PostgreSQL's buffer machinery. Shared hits and reads are different; a shared read can still be served by the operating system cache rather than a physical disk. Parent-node counts can include descendant work, so summing every node can double-count. Compare like-for-like plan locations and report exactly what you measured.

For mutating statements, EXPLAIN ANALYZE really executes the mutation. Use isolated data and an appropriate transaction policy; do not paste it into a production write path as if it were a read-only planner inspection. This lesson's experiment executes SELECTs against a disposable synthetic fixture.

### Covering indexes and visibility

An index-only scan can return values available from an appropriate index, but PostgreSQL still needs to establish visibility under MVCC. Its visibility map can avoid heap checks for qualifying all-visible pages; recently changed pages may still require heap fetches. INCLUDE columns can cover additional output fields while increasing index size and write cost. [Index-only scans](https://www.postgresql.org/docs/18/indexes-index-only-scans.html).

The experiment selects a payload that is not included in the composite index. It therefore demonstrates an ordinary ordered index scan, not a promise of zero heap access. A giant covering index containing every response field can waste memory and amplify writes. Measure the specific benefit and account for churn and visibility behavior.

Other index types serve other access patterns. GIN is useful for suitable containment and full-text operations, GiST supports appropriate spatial and other operator classes, and BRIN can exploit physical correlation for some large relations. A B-tree over latitude and longitude is not a general nearest-station search solution. Spatial querying receives dedicated treatment later, with PostGIS and distance semantics explicitly tested.

### Every index changes writes and operations

Inserts, deletes, and relevant updates maintain additional index entries and generate related storage and logging work. Wider and more numerous indexes compete for cache and take time to build, replicate, back up, and restore. Some updates can avoid new index entries under PostgreSQL's HOT conditions, but this is conditional behavior, not a reason to ignore indexed-column churn.

A regular CREATE INDEX can block concurrent writes while building. CONCURRENTLY supports a different production rollout path with extra work, waits, failure states, and restrictions, including not running inside an ordinary transaction block. Inspect its documented lifecycle and verify the resulting index is valid. The isolated experiment uses the simpler regular build because no user traffic shares its fixture.

An index improvement should include a removal and monitoring decision. Track useful query latency and rows/buffers examined, write throughput, storage growth, and usage over a representative period. An apparently unused index may enforce a constraint or serve an infrequent critical operation; verify its role before dropping it.

## D. Architecture and data flow

The access path changes; the query's ownership and ordering contract remain the same.

```mermaid
flowchart LR
    Query[Owner filter and newest 20] --> Planner[Planner and statistics]
    Planner --> Scan[Ordered composite index scan]
    Scan --> Heap[Heap visibility and payload]
    Heap --> Result[Return bounded page]
```

Before the index, the recorded fixture uses a sequential scan and sort. After the index, the planner can seek the owner/time range and stop after twenty results. The diagram shows the improved path; inspect the saved plans for both alternatives. Nothing about an index removes the need for the owner filter or a stable pagination tuple.

## E. Real-world examples

For an illustrative StopAround newest-journeys feed, use owner equality and descending creation/ID order. The current API lab deliberately exposes UUID-ascending pagination, so this is a proposed alternative contract and query, not a claim that adding this index silently changes that endpoint's semantics. Change the cursor and public ordering together if the product needs chronology.

For a separate task tracker, an active-task list by project can benefit from a small partial index when completed tasks dominate history. If the product later asks for a full historical export, that index may not help. The same table can have several legitimate workloads with different access paths and limits.

In the observed PostgreSQL 18.6 lab run, root shared-buffer accesses decreased from 1,924 to 23, and the added index occupied 4,079,616 bytes. Recorded execution times were 3.176 ms and 0.063 ms. These are one synthetic local run with its particular cache state; they are not a general speedup claim or a cold-disk benchmark. [Recorded plans](../../exercises/module-01/08-database-indexing/observed-plan.json).

## F. Executable example

The full [experiment](../../exercises/module-01/08-database-indexing/index_experiment.py) seeds its own 100,000-row schema and saves both JSON plans. Follow [the guide](../../exercises/module-01/README.md) for the database and dependencies, then run:

```bash
.venv/bin/python exercises/module-01/08-database-indexing/index_experiment.py
```

<!-- Listing: exercises/module-01/08-database-indexing/index_experiment.py -->

```python
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
```

The test leaves sequential scans enabled and checks the planner's chosen index, absence of a separate sort, twenty output rows, and fewer root buffer accesses. It deliberately avoids an exact timing threshold, which would mostly test local scheduling and cache conditions. Planner choices can change with versions, data, and statistics; investigate a changed plan before forcing an index.

## G. Architectural decisions and trade-offs

Add the narrowest index that materially improves a defined query under representative load. Consider whether the index also enforces a required constraint or supports another important path. A composite key with equality, range, and order aligned is often more useful than several guessed single-column indexes.

Use covering or partial indexes when the reduced work outweighs width, churn, and predicate restrictions. Separate interactive pages from large exports so a small-page optimization does not become an excuse to return an unbounded response. For a very small table, a scan can remain the simpler efficient choice.

Plan rollout and rollback with the same care as the SQL definition. Reserve build capacity, observe long transactions and replication, verify validity, and remove redundant structures only after understanding their constraints and real usage.

## H. Common failures and debugging

If an index is not chosen, inspect selectivity, table size, stale statistics, predicate expression, parameter types, sort requirements, and the exact application query. Disabling sequential scans can demonstrate an alternative path but is not evidence that forcing it is the right production fix.

If EXPLAIN looks fast while the endpoint is slow, include connection acquisition, transaction waits, serialization, network transfer, and N+1 calls. If row estimates differ greatly from actual counts, investigate skew and statistics before adding another index with the same mistaken assumptions.

If writes regress after indexing, measure changed indexes, WAL and I/O, indexed-column updates, and storage/cache pressure. If an index-only plan still fetches heap rows, inspect visibility and churn. If an online build fails, inspect invalid index state rather than assuming the name's existence proves a usable structure.

## I. Practical exercise

Run the experiment and identify the before and after scan nodes. Record estimated and actual rows, sort behavior, root hit/read buffers, execution time, and index bytes. Explain why root rows alone do not quantify scanned work and why shared reads are not necessarily physical disk reads.

Then design an owner-scoped chronological cursor query and its index. Explain how the design changes for a global newest-events feed and why separate owner/time indexes are not equivalent for the ordered LIMIT. Include one write-cost measurement you would collect before deploying the index. Compare with the [worked solution](../../exercises/module-01/08-database-indexing/SOLUTION.md).

## J. Interview and senior-engineering assessment

1. What work can a matching ordered index avoid?
2. Why does composite column order matter?
3. When can a sequential scan be the right plan?
4. What is the difference between EXPLAIN and EXPLAIN ANALYZE?
5. Why can an index-only scan still perform heap fetches?
6. What costs accompany an additional index?
7. Why is the observed millisecond improvement not a production guarantee?

## Assessment solutions

### 1. Filtering, sorting, and unnecessary page visits

The engine can navigate directly to a qualifying range, produce the requested order, and stop after a bounded page. It can avoid scanning unrelated owners and sorting all matches. A normal index scan may still fetch heap values and visibility information.

### 2. The structure is lexicographically ordered

Leading equality conditions select a range whose later keys have useful ordering. An owner-leading time index directly supports one owner's newest rows, while a global newest feed has a different shape. Version-specific planner strategies can support other uses, so avoid absolute unusability rules.

### 3. Large fractions or small relations

If most rows qualify or the table is small, a scan can cost less than many index and heap visits. Data distribution, caching, and output requirements matter. An unused index in one plan is not automatically a planner failure.

### 4. Estimates versus executed observations

EXPLAIN reports a planned access path and estimated costs/rows. ANALYZE executes it and records actual behavior. Costs are not milliseconds, and mutating statements really mutate when executed. Use safe isolated data for experiments.

### 5. Values and visibility are separate

Available index values are insufficient if MVCC visibility still needs heap checks. The visibility map can permit avoiding those checks for all-visible pages. Frequent writes can reduce that benefit, and INCLUDE width adds maintenance cost.

### 6. Maintained structures consume resources

Account for write work, storage, cache competition, logging, build capacity, replication, backup, and restore. A constraint-backed index also has a correctness role. Measure a representative workload before declaring an extra index free or redundant.

### 7. The fixture fixes only some variables

Hardware, version, cache state, concurrent work, row distribution, and query parameters change performance. The structural evidence is less work and an appropriate access path; the saved timing is an observation that can be reproduced or challenged, not an SLO.

## K. Key takeaways and navigation

Design indexes from concrete filters, ordering, and bounds. Read plans as work, validate on real data, and budget the write and operational costs.

Next: [1.09 — Numbers to know](09-numbers-to-know.md). Previous: [1.07 — CAP theorem](07-cap-theorem.md).

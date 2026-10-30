# Sharding

Lesson 1.05 · Core concepts

## A. Learning objectives and prerequisites

You should be able to distinguish sharding from replication and local table partitioning, evaluate a partition key against reads and invariants, identify hot shards, and describe a migration that does not allow stale routers to keep writing to the old owner. You should also be able to explain when one PostgreSQL instance remains the better design.

Read [data modeling](03-data-modeling.md) and [caching](04-caching.md). The exercise uses an in-memory sequential model, not a cluster or a live migration tool. All shard counts, tenant sizes, traffic rates, and migration scenarios are illustrative. The aim is to learn ownership and failure reasoning before operating a distributed database.

## B. Mental model and intuition

Sharding assigns different authoritative subsets of data to different storage owners. Replication stores additional copies of the same subset. A cache remembers a reusable answer; it does not become a shard merely because it contains only some keys. These mechanisms can coexist, but they solve different problems.

Imagine splitting a large shared filing room between several buildings. Every new document needs a stable rule for finding its authoritative building. A visitor carrying an old directory must not be allowed to keep changing the previous copy after a folder moves. The hard work is not drawing several database boxes; it is preserving ownership, routing, and invariants while data and traffic move.

For StopAround, private journeys naturally group by owner, while station search groups by geography and route corridor. One partition key is unlikely to optimize both. Separate the access patterns before deciding whether they belong in one sharded model, independent projections, or still one well-indexed database.

## C. Deep technical explanation

### Start with evidence for the split

A large table does not automatically require sharding. Measure query plans, working-set size, write throughput, lock contention, storage growth, maintenance windows, and failover requirements. Missing indexes, long transactions, oversized responses, and inefficient joins can create symptoms that more databases merely reproduce. Vertical capacity, better queries, local partitioning, and read replicas may satisfy the requirement at much lower operational cost.

Local PostgreSQL table partitioning divides a logical table into physical partitions managed by one database system, enabling pruning and lifecycle operations under its rules. It does not by itself distribute authoritative writes across independent PostgreSQL servers. Unique and primary-key constraints on a partitioned table also have partition-key requirements that affect schema design. [PostgreSQL 18 partitioning](https://www.postgresql.org/docs/18/ddl-partitioning.html).

Sharding becomes attractive when a measured resource or isolation boundary needs multiple authoritative owners and the application's access patterns can tolerate that split. Record the target bottleneck and an acceptance metric. “Support more users” is too vague to establish whether a migration paid for its new failure modes.

### Partition-key choices

Hashing a tenant or user identifier spreads many independent owners across shards and preserves locality for their data. A tenant's journey list, stops, and idempotency records can share a transaction boundary if they live on one shard. A cross-tenant report now needs fan-out, a separate analytical store, or a maintained global projection.

Range partitioning supports ordered access and targeted movement, but growing keys can concentrate writes on the newest range. Geographic partitioning helps nearby searches, yet dense cities and cross-boundary routes can produce skew and fan-out. Time-based partitions simplify retention for observations, but the newest period can receive nearly all writes. The useful question is which workload becomes local and which becomes distributed.

Do not shard by a mutable display attribute unless its movement protocol is part of the design. A user's country or a station's provider mapping can change. Stable identity generally makes a better routing basis; separate mutable access projections when needed. A deterministic key should be available before a request performs a global lookup, or that lookup becomes another critical dependency.

### Skew is about work, not just row count

A shard with one unusually active tenant can be overloaded while peers are idle. Equal key counts do not imply equal bytes, write rates, CPU, or lock contention. A popular station identifier may be one hot key that no ownership hash can split by itself. Cache reads, isolate a large tenant, partition a suitable sub-aggregate, or redesign the operation according to the actual bottleneck.

Choose and observe per-shard metrics: request rate, service time, queue age, CPU, I/O, storage, replication lag, and tenant contribution under a privacy-aware diagnostics policy. A fleet-wide average can hide a failing shard. Capacity planning should account for the busiest surviving shard after failure or movement, not only the average before either event.

### Routing and virtual buckets

Directly computing `hash(key) modulo server_count` is simple, but changing server count remaps many keys. An indirection layer can map stable logical buckets to physical shard owners. The hash chooses a bucket; a versioned directory chooses its current owner. Moving one bucket changes the directory entry without changing the hash function for unrelated data.

The directory is part of correctness. Routers can cache it for speed, but storage must reject stale ownership epochs or the migration must safely drain and prevent old writers. Checking a route only in an application process is insufficient: a writer can pass that check, pause, and resume after cutover. The authority check and accepted write need an atomic or equivalently fenced boundary at the actual storage owner.

The lab models this boundary as one sequential `check` followed immediately by an in-memory assignment with no concurrent execution. Its directory is authoritative and all writes fail closed if that directory is unavailable. This is useful for histories, but is not a protocol for safely consulting a remote directory and then writing an independent database under arbitrary delays.

### Moving a bucket safely

A simple migration can trade availability for an easier proof. Freeze writes for the bucket, drain accepted in-flight writes, copy a consistent source state, verify the copy, publish the new owner with a higher epoch, and reject writes under the old epoch. Reopen traffic only after the new ownership state is established. Reads need a policy too: pause them or serve an explicitly valid snapshot rather than accidentally mixing states.

The sequential lab freezes both reads and writes for that bucket, copies its current dictionary, advances ownership, and fences old routes. Other buckets remain unchanged. An abort before cutover reopens the source. The model retains old copies but does not route to them. Real implementation requires durable migration state, data verification, crash recovery, and enforcement across every writer.

For less downtime, systems can snapshot while copying, capture subsequent changes, reconcile them, and perform a shorter fenced cutover. Deletes, ordering, duplicate events, and writer progress all matter. Naive dual writing to two independent databases creates partial-success states: source-only, destination-only, or conflicting order. Calling it “dual write” does not specify which copy wins after a crash.

Migration throughput competes with application traffic. Rate-limit copy work, track remaining data and change backlog, reserve destination capacity, and establish abort criteria. If catch-up receives changes faster than it can apply them, a low-downtime migration may never reach cutover. A small freeze can be safer than an elaborate mechanism the team cannot verify.

### Cross-shard invariants and operations

A foreign key inside one PostgreSQL database cannot directly enforce a relationship in another independent database. Co-locate aggregates whose invariants require local transactions where possible. Global uniqueness may need a coordinator, a carefully scoped namespace, or a different product rule. Cross-shard transfers can require distributed transactions or an explicitly compensating workflow, with user-visible intermediate states.

Operational tasks also distribute. Backups must support an understandable restore point across related shards. Schema changes must coexist with mixed versions during rollout. Global queries require partial-failure and pagination policies. A router bug can send traffic to the wrong owner even when every database is healthy. Include these costs in the decision, not as a footnote after choosing the partition key.

## D. Architecture and data flow

The movement protocol below favors a short, explicit pause over concurrent writes during copying.

```mermaid
flowchart LR
    Owner[Current owner and epoch] --> Freeze[Freeze and drain bucket]
    Freeze --> Copy[Copy and verify state]
    Copy --> Cutover[Publish next owner epoch]
    Cutover --> Fence[Reject stale routes]
```

Each transition must be recoverable in a real implementation. The lab keeps these states only in memory; restarting the Python object loses them. Its tests establish the sequencing rule and stale-route rejection within one process. They do not establish online migration, crash durability, quorum membership, or a distributed fence implementation.

## E. Real-world examples

For an illustrative future StopAround scale, user-owned journeys might be assigned by owner identifier, keeping a user's stops and creation records together. Public station search could use a geographic read projection with a different partitioning policy. A route crossing two geographic cells would need a merged result and deduplication, even though saving the private journey remains one owner-local transaction.

For a separate example, a business-to-business task service shards by organization. Most reads and writes stay local, but one very large organization dominates a shard. Adding random organizations to new shards does not relieve that tenant's write contention. The service might isolate it, split an independent project aggregate, or change the contended operation. The solution follows the hotspot's unit of work.

These are proposed designs, not documented architectures of named companies. Before adopting either, compare the measured bottleneck with the simpler single-database alternatives and estimate the team's ability to operate migration, restore, and routing failures.

## F. Executable example

The full [shard model](../../exercises/module-01/05-sharding/shard_model.py) uses sixteen stable buckets and a versioned owner per bucket. Run its tests through [the lab guide](../../exercises/module-01/README.md). The code makes the freeze, copy, cutover, and abort steps explicit so you can inspect intermediate states.

<!-- Listing: exercises/module-01/05-sharding/shard_model.py -->

```python
"""Sequential freeze/copy/fence model, not a live database migration tool."""
import hashlib
from dataclasses import dataclass


class Unavailable(Exception): pass
class StaleRoute(Exception): pass


@dataclass(frozen=True)
class Route:
    bucket: int
    shard: str
    epoch: int


class ShardedStore:
    def __init__(self, buckets=16):
        if not isinstance(buckets,int) or buckets < 1: raise ValueError('positive bucket count required')
        self.buckets=buckets
        self.owners={i:Route(i,'A' if i%2==0 else 'B',1) for i in range(buckets)}
        self.data={'A':{},'B':{},'C':{}}
        self.frozen=set(); self.prepared={}; self.directory_available=True

    def bucket(self,key): return int.from_bytes(hashlib.sha256(key.encode()).digest()[:8],'big')%self.buckets

    def route(self,key):
        if not self.directory_available: raise Unavailable('authoritative directory unreachable')
        return self.owners[self.bucket(key)]

    def check(self,key,route):
        current=self.route(key)
        if route != current: raise StaleRoute('refresh ownership and retry safely')
        if current.bucket in self.frozen: raise Unavailable('bucket migration is frozen')

    def write(self,key,value,route):
        self.check(key,route); self.data[route.shard][key]=value

    def read(self,key,route):
        self.check(key,route); return self.data[route.shard].get(key)

    def freeze(self,bucket):
        if not self.directory_available: raise Unavailable('directory unreachable')
        if bucket not in self.owners or bucket in self.frozen: raise ValueError('invalid or already frozen bucket')
        self.frozen.add(bucket)

    def copy(self,bucket,target):
        if bucket not in self.frozen or target not in self.data or target==self.owners[bucket].shard:
            raise ValueError('freeze a bucket and choose another existing shard')
        source=self.owners[bucket].shard
        snapshot={k:v for k,v in self.data[source].items() if self.bucket(k)==bucket}
        for key in list(self.data[target]):
            if self.bucket(key)==bucket: del self.data[target][key]
        self.data[target].update(snapshot)
        self.prepared[bucket]=target

    def cutover(self,bucket):
        if not self.directory_available: raise Unavailable('directory unreachable')
        if bucket not in self.frozen or bucket not in self.prepared: raise ValueError('copy before cutover')
        old=self.owners[bucket]
        self.owners[bucket]=Route(bucket,self.prepared.pop(bucket),old.epoch+1)
        self.frozen.remove(bucket)

    def abort(self,bucket):
        if not self.directory_available: raise Unavailable('directory unreachable')
        self.prepared.pop(bucket,None); self.frozen.discard(bucket)
```

Every operation is sequential in this model. Do not wrap `check` and a remote SQL write around network awaits and claim the same guarantee. A real fence has to stop a writer whose route became stale after it began executing. Old physical copies are deliberately retained for inspection; cleanup is a separate operational action after ownership and recovery policy are settled.

## G. Architectural decisions and trade-offs

Choose a partition key by transaction locality, query fan-out, skew, and movement cost. A perfectly even hash can be worse than a somewhat uneven tenant layout if every business operation becomes cross-shard. Conversely, one huge tenant can exceed a shard even when every other tenant is local.

Stable virtual buckets make incremental movement explicit, but add directory consistency and routing complexity. Consistent hashing, covered next, offers another placement mechanism; it still requires safe ownership transfer and routing agreement. Neither mapping strategy copies data or implements failure recovery by itself.

A freeze-and-copy migration sacrifices availability for a simpler correctness argument. Change capture and catch-up reduce pause time while adding ordering, durability, and reconciliation responsibilities. State the maximum acceptable pause and recovery behavior before selecting the more complex path.

## H. Common failures and debugging

For an overloaded shard, compare bytes and work rates by shard and by aggregate. Uniform row counts can conceal a hot tenant or large objects. For missing rows after movement, inspect routing epoch, copy completeness, deleted records, and whether reads accidentally reach an old owner.

For divergent copies, inspect every writer and migration transition. A stale router accepted by the old database is a fencing failure, not merely a cache-refresh delay. For an endless catch-up phase, compare change arrival with apply throughput and reserve capacity before trying another cutover.

For directory failure, observe whether the system fails closed or silently accepts ownership guesses. The correct degraded behavior depends on the protocol; the lab deliberately rejects operations. Exercise restore and rollback plans as well as the successful migration path.

## I. Practical exercise

Write values under several tenant keys, retain one old route, and migrate that route's bucket to shard C. Before copying, attempt a write while frozen. After cutover, attempt a write with the retained route, then refresh routing and verify the value. Confirm that unrelated buckets keep their owners.

Design the same migration for real PostgreSQL shards on paper. State where in-flight writers drain, where an epoch is enforced atomically with the write, what is durable before each transition, and how a crash after copy but before cutover is recovered. Explain why a router-only check is insufficient. Compare with the [worked solution](../../exercises/module-01/05-sharding/SOLUTION.md).

## J. Interview and senior-engineering assessment

1. How do sharding, replication, and local partitioning differ?
2. What makes an owner identifier a useful or problematic partition key?
3. Why can equal key counts still produce an overloaded shard?
4. What does a virtual-bucket directory add?
5. Why must old writers be fenced during cutover?
6. What failure states does naive dual writing create?
7. When would you postpone sharding?

## Assessment solutions

### 1. Ownership, copies, and local organization

Sharding assigns different authoritative subsets to different owners. Replication copies a subset for durability or reads. Local partitioning organizes one logical database table into partitions under that database's capabilities. None automatically supplies the others' guarantees.

### 2. Local invariants versus skew

Owner-based placement keeps related data and transactions together, but cross-owner queries fan out and a very large owner can dominate one shard. Evaluate actual aggregate sizes and work rates, not only how uniformly identifiers hash.

### 3. Work is uneven

Values differ in size, read popularity, write frequency, and contention. One hot key remains one owner even with an ideal hash. Measure the saturated resource and choose a remedy that splits or reduces that work.

### 4. Stable indirection

The hash selects a stable bucket and the directory selects its current physical owner. Moving a bucket avoids changing unrelated assignments. The directory becomes a versioned correctness dependency requiring agreement, cache policy, and failure handling.

### 5. A stale route can outlive publication

A writer can hold an old route or pause after validating it. If the old owner still accepts its mutation, copies diverge. Drain accepted work and enforce ownership at the write boundary; publishing a new map alone cannot stop that writer.

### 6. Partial and differently ordered success

One destination can accept while the other fails, and concurrent updates can arrive in different orders. Recovery needs authoritative ordering, deduplication, delete handling, and reconciliation. Two independent successful calls are not an atomic transaction.

### 7. When simpler capacity meets the requirement

Fix measured query, index, transaction, payload, and maintenance problems first. If one database with appropriate capacity and recovery meets the target, sharding's routing, movement, cross-shard invariants, and operational costs have no demonstrated benefit yet.

## K. Key takeaways and navigation

Sharding is a decision about authoritative ownership and local invariants. Placement, movement, fencing, and operations all belong in the design.

Next: [1.06 — Consistent hashing](06-consistent-hashing.md). Previous: [1.04 — Caching](04-caching.md).

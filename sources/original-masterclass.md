# System Design Masterclass — Senior Frontend → Senior Full-Stack

**Edition:** October 2026  
**Course base:** [Hello Interview — System Design in a Hurry](https://www.hellointerview.com/learn/system-design/in-a-hurry/introduction)  
**Format:** Original companion course — topic map follows the source's overall organization, with custom teaching, exercises and full-stack labs. **Not a reproduction of the source text.**

## Goal and learning contract

You can already lead frontend architecture. Your next step is being able to own the full request/data lifecycle: choose an API contract, design a relational schema, implement transactional behavior, operate the service, explain reliability and failure modes, and know **when not** to introduce distributed complexity.

**Teaching loop for every lesson:** (1) intuition, (2) mechanism, (3) trade-offs, (4) real-world example, (5) hands-on exercise, (6) check for understanding. Pass the lesson when you can explain the *why*, not just name a technology.

**Suggested pacing:** 3–5 learning sessions a week, with deeper design exercises and implementation labs spread over several sessions. Treat the TOC as a complete syllabus, not a mandate to master every specialist technology in a single pass. Go deep first on HTTP, API design, SQL/PostgreSQL, transactions, caching, queues, security, deployment and observability. Each later chapter revisits earlier ideas.

**Contents status:** Lesson 0.01 is fully written below; all other lessons currently contain an objective and teaching template and will be developed with you sequentially. This is a study companion, not 98 completed tutorials.

**Lesson status:** `⬜` Not started · `🟡` In progress · `✅` Passed. Track completion in your own copy of this file or in this conversation.

## Table of contents

### [Module 0 — Foundations & delivery framework](#module-0) (3 lessons)

- ⬜ **[0.01 Introduction](#lesson-0-01)** — What system design is, real-world ownership versus interviews, trade-offs
- ⬜ **[0.02 How to prepare](#lesson-0-02)** — A deliberate learning loop, practice, feedback, and depth
- ⬜ **[0.03 Delivery framework](#lesson-0-03)** — Requirements, entities, APIs, data flows, high-level design, deep dives

### [Module 1 — Core concepts](#module-1) (9 lessons)

- ⬜ **[1.01 Networking essentials](#lesson-1-01)** — DNS, TCP, TLS, HTTP, CDNs, latency, timeouts
- ⬜ **[1.02 API design](#lesson-1-02)** — REST, resource contracts, auth, idempotency, pagination, versioning
- ⬜ **[1.03 Data modeling](#lesson-1-03)** — Entities, relationships, constraints, normalization, transactions
- ⬜ **[1.04 Caching](#lesson-1-04)** — Cache placement, TTL, invalidation, consistency, stampedes
- ⬜ **[1.05 Sharding](#lesson-1-05)** — Partition keys, hotspots, rebalancing, operational cost
- ⬜ **[1.06 Consistent hashing](#lesson-1-06)** — Distribution, virtual nodes, scale-in/out
- ⬜ **[1.07 CAP theorem](#lesson-1-07)** — Consistency, availability, partitions, eventual convergence
- ⬜ **[1.08 Database indexing](#lesson-1-08)** — B-trees, composite indexes, query plans, write overhead
- ⬜ **[1.09 Numbers to know](#lesson-1-09)** — Throughput, latency, storage, rough capacity estimates

### [Module 2 — Key technologies](#module-2) (22 lessons)

- ⬜ **[2.01 Core database](#lesson-2-01)** — What persistence must guarantee
- ⬜ **[2.02 Relational databases](#lesson-2-02)** — SQL, relational integrity, ACID, isolation
- ⬜ **[2.03 NoSQL databases](#lesson-2-03)** — Access patterns, key-value, document and wide-column systems
- ⬜ **[2.04 Blob storage](#lesson-2-04)** — Object stores, signed uploads and CDN delivery
- ⬜ **[2.05 Search-optimized database](#lesson-2-05)** — Inverted indexes and search use cases
- ⬜ **[2.06 API gateway](#lesson-2-06)** — Routing, rate limits and authentication boundaries
- ⬜ **[2.07 Load balancer](#lesson-2-07)** — L4 versus L7, health checks and failover
- ⬜ **[2.08 Queue](#lesson-2-08)** — Async processing, delivery semantics, poison messages
- ⬜ **[2.09 Streams and event sourcing](#lesson-2-09)** — Logs, offsets, consumer groups and event history
- ⬜ **[2.10 Distributed lock](#lesson-2-10)** — Mutual exclusion, leases and fencing
- ⬜ **[2.11 Distributed cache](#lesson-2-11)** — Replication, eviction and invalidation
- ⬜ **[2.12 CDN](#lesson-2-12)** — Edge caching, cache-control, origin protection
- ⬜ **[2.13 Redis deep dive](#lesson-2-13)** — Data structures, caching and coordination
- ⬜ **[2.14 Elasticsearch deep dive](#lesson-2-14)** — Inverted indexes, relevance, refresh delay
- ⬜ **[2.15 Kafka deep dive](#lesson-2-15)** — Partitions, durable events, ordering and retries
- ⬜ **[2.16 Temporal deep dive](#lesson-2-16)** — Durable workflows and process recovery
- ⬜ **[2.17 API Gateway deep dive](#lesson-2-17)** — Gateway trade-offs and security
- ⬜ **[2.18 Cassandra deep dive](#lesson-2-18)** — Wide-column architecture and high-write workloads
- ⬜ **[2.19 DynamoDB deep dive](#lesson-2-19)** — Partition keys, secondary indexes and capacity
- ⬜ **[2.20 PostgreSQL deep dive](#lesson-2-20)** — SQL, transactions, indexes, EXPLAIN, replication
- ⬜ **[2.21 Flink deep dive](#lesson-2-21)** — Stream processing, event time and state
- ⬜ **[2.22 ZooKeeper deep dive](#lesson-2-22)** — Coordination, watches and consensus context

### [Module 3 — Common patterns](#module-3) (9 lessons)

- ⬜ **[3.01 Real-time updates](#lesson-3-01)** — Polling, SSE, WebSockets, connections and reconnection
- ⬜ **[3.02 Dealing with contention](#lesson-3-02)** — Optimistic concurrency, locking, queues
- ⬜ **[3.03 Multi-step processes](#lesson-3-03)** — Sagas, compensations, workflows and durable execution
- ⬜ **[3.04 Scaling reads](#lesson-3-04)** — Read replicas, caches, denormalized projections
- ⬜ **[3.05 Scaling writes](#lesson-3-05)** — Partitioning, batching, buffering and backpressure
- ⬜ **[3.06 Handling large blobs](#lesson-3-06)** — Direct upload, multipart upload, metadata and CDN
- ⬜ **[3.07 Managing long-running tasks](#lesson-3-07)** — Jobs, queues, retries, visibility and status
- ⬜ **[3.08 Proximity-based services](#lesson-3-08)** — Spatial indexing, geohashes and nearest-neighbor queries
- ⬜ **[3.09 Pattern selection](#lesson-3-09)** — Diagnosing bottlenecks before adding complexity

### [Module 4 — Question breakdowns and practice](#module-4) (36 lessons)

- ⬜ **[4.01 Bitly](#lesson-4-01)** — URL IDs, redirects and storage
- ⬜ **[4.02 Dropbox](#lesson-4-02)** — File uploads, synchronization and metadata
- ⬜ **[4.03 Local delivery service](#lesson-4-03)** — Orders, assignment and tracking
- ⬜ **[4.04 Ticketmaster](#lesson-4-04)** — Inventory, seat holds and high contention
- ⬜ **[4.05 Facebook News Feed](#lesson-4-05)** — Fanout and ranking
- ⬜ **[4.06 Tinder](#lesson-4-06)** — Matching, discovery and location
- ⬜ **[4.07 LeetCode](#lesson-4-07)** — Sandboxed code execution and job orchestration
- ⬜ **[4.08 WhatsApp](#lesson-4-08)** — Messaging, delivery guarantees and offline devices
- ⬜ **[4.09 Rate limiter](#lesson-4-09)** — Counters, token buckets and distributed coordination
- ⬜ **[4.10 YouTube](#lesson-4-10)** — Upload, transcoding and streaming
- ⬜ **[4.11 Facebook Live Comments](#lesson-4-11)** — Real-time event delivery
- ⬜ **[4.12 YouTube Top K](#lesson-4-12)** — Streaming aggregation and top-k algorithms
- ⬜ **[4.13 Uber](#lesson-4-13)** — Location, dispatch and matching
- ⬜ **[4.14 Web crawler](#lesson-4-14)** — URL scheduling, politeness and deduplication
- ⬜ **[4.15 Ad click aggregator](#lesson-4-15)** — Event ingestion and time-window aggregation
- ⬜ **[4.16 Facebook Post Search](#lesson-4-16)** — Indexing and distributed search
- ⬜ **[4.17 Yelp](#lesson-4-17)** — Geo-search, reviews and ranking
- ⬜ **[4.18 Instagram](#lesson-4-18)** — Media lifecycle and social feeds
- ⬜ **[4.19 Strava](#lesson-4-19)** — Activity ingestion and geo data
- ⬜ **[4.20 Distributed cache](#lesson-4-20)** — Cache nodes, partitioning and eviction
- ⬜ **[4.21 Online auction](#lesson-4-21)** — Bidding, ordering and contention
- ⬜ **[4.22 Job scheduler](#lesson-4-22)** — Scheduling, execution and retries
- ⬜ **[4.23 News aggregator](#lesson-4-23)** — Ingestion, dedupe and ranking
- ⬜ **[4.24 Price tracking service](#lesson-4-24)** — Crawling, change detection and alerts
- ⬜ **[4.25 Notification system](#lesson-4-25)** — Multi-channel delivery and preferences
- ⬜ **[4.26 Robinhood](#lesson-4-26)** — Quotes, orders and financial correctness
- ⬜ **[4.27 Google Docs](#lesson-4-27)** — Collaborative editing and concurrency
- ⬜ **[4.28 Payment system](#lesson-4-28)** — Idempotency, ledger design and reconciliation
- ⬜ **[4.29 Metrics monitoring](#lesson-4-29)** — High-cardinality ingestion and time series
- ⬜ **[4.30 Online chess](#lesson-4-30)** — Game state, timing and real-time moves
- ⬜ **[4.31 ChatGPT](#lesson-4-31)** — Request streaming, inference scheduling and conversation state
- ⬜ **[4.32 Flash sale](#lesson-4-32)** — Traffic bursts, inventory and oversell prevention
- ⬜ **[4.33 Extra practice: food reviews](#lesson-4-33)** — A service with reviews, discovery and moderation
- ⬜ **[4.34 Extra practice: game leaderboard](#lesson-4-34)** — Rank storage and hot keys
- ⬜ **[4.35 Extra practice: donations](#lesson-4-35)** — Donation processing and accounting
- ⬜ **[4.36 Extra practice: GitHub Actions](#lesson-4-36)** — Durable workflow jobs and execution fleets

### [Module 5 — Advanced topics](#module-5) (5 lessons)

- ⬜ **[5.01 Proximity search](#lesson-5-01)** — Spatial indexing and relevance
- ⬜ **[5.02 Vector databases](#lesson-5-02)** — Embeddings, approximate nearest neighbors, hybrid search
- ⬜ **[5.03 Time-series databases](#lesson-5-03)** — Retention, downsampling and high-volume writes
- ⬜ **[5.04 Data structures for big data](#lesson-5-04)** — Bloom filters, sketches and approximate counting
- ⬜ **[5.05 Change data capture](#lesson-5-05)** — WAL, outbox, event projections and replication

### [Module 6 — In the wild: real engineering stories](#module-6) (6 lessons)

- ⬜ **[6.01 Shopify inventory reservations](#lesson-6-01)** — Inventory correctness under concurrency
- ⬜ **[6.02 Discord message storage](#lesson-6-02)** — Message partitioning and access patterns
- ⬜ **[6.03 Slack job queue](#lesson-6-03)** — Operational queues at scale
- ⬜ **[6.04 Figma multiplayer](#lesson-6-04)** — Collaboration and concurrent edits
- ⬜ **[6.05 Spotify data lake](#lesson-6-05)** — Analytical pipelines and data evolution
- ⬜ **[6.06 Meta ZGateway](#lesson-6-06)** — Edge systems and service infrastructure

### [Module 7 — Full-stack implementation labs (custom additions)](#module-7) (8 lessons)

- ⬜ **[7.01 Backend foundations](#lesson-7-01)** — FastAPI service, typed contracts and local environment
- ⬜ **[7.02 SQL and transactions](#lesson-7-02)** — PostgreSQL schema, migration, index, EXPLAIN and isolation
- ⬜ **[7.03 Authentication and authorization](#lesson-7-03)** — Identity, sessions, JWT trade-offs, RBAC and ownership checks
- ⬜ **[7.04 Caching and performance](#lesson-7-04)** — Redis, cache policies, profiling and load testing
- ⬜ **[7.05 Background processing](#lesson-7-05)** — Queue, idempotent worker, retries and dead-letter handling
- ⬜ **[7.06 Infrastructure and deployment](#lesson-7-06)** — Containers, CI/CD, environments and secrets
- ⬜ **[7.07 Reliability and security](#lesson-7-07)** — Tracing, metrics, alerting, backups, threat modeling and recovery
- ⬜ **[7.08 Capstone design review](#lesson-7-08)** — Architecture decision record, failure drills and senior-level presentation

## Course approach

The source's *overview chapters* and its *sidebar deep-dives* are both represented above. The standalone *Key technologies* chapter includes its overview categories and ten deeper technology guides. *Question breakdowns* contains the 32 written case studies plus four extra practice prompts. The *Common patterns* module includes the seven detailed guides and two overview topics. **Module 7** is unique to this study plan and turns interview knowledge into production skills.

We will work in the order shown. During the case-study module, we may solve an easier problem first and then compare alternative designs before seeing any model solution. You will design things, write short APIs/SQL, reason about capacity, and defend a trade-off.

<a id="module-0"></a>

## Module 0 — Foundations & delivery framework

**Outcome:** think like a backend system owner; structure an ambiguous design problem and identify the first critical decisions.

<a id="lesson-0-01"></a>

### 0.01 — Introduction

**Target:** What system design is, real-world ownership versus interviews, trade-offs.

#### 1. The mental model

System design is deciding **what components exist, what responsibilities they own, how data moves between them, and what happens when the workload or environment changes**. A senior engineer also explains trade-offs, tests assumptions and plans for operational failure.

A complete system is not a fancy diagram. A request starts at a client and ends in a business outcome: the right data is read or written, within an acceptable time, without compromising authorization or data integrity.

#### 2. Example: a route-aware stop finder

Imagine a web application where drivers enter a route and available range, and the app returns reachable stops.

```text
Browser (React / Next.js)
  |
  | HTTPS GET /v1/stops?route_id=...&range_km=...
  v
Backend (FastAPI)
  |-- validates request and permissions
  |-- coordinates route filtering and business rules
  v
PostgreSQL + PostGIS
  |-- stores stops, location and metadata
  |-- queries stops in/near the route corridor
  v
Backend -> JSON response -> Browser renders results
```

**Frontend perspective:** request state, perceived latency, accessible states, error UI, rendering.  
**Backend perspective:** authorization, validation, query cost, spatial index behavior, transactional changes, instrumentation and response bounds.  
**System perspective:** what occurs when a route provider times out, search demand increases, results get stale, or the database is unavailable?

Start with **one backend and one database**. Introducing ten microservices is not evidence of seniority. Add complexity because a measured requirement demands it.

#### 3. Functional vs non-functional requirements

Functional: *Users can submit a route, find reachable stops, and compare options.*  
Non-functional: *For a defined normal traffic workload, 95% of searches finish in under 700 ms* (a **hypothetical target**, not a measured value). Consider security, data freshness, availability and cost as separate properties. Performance targets must be measured end-to-end; p95 means 95% of observations are at or below the stated duration in the chosen measurement interval.

#### 4. A first decision table

| Decision | Default | Revisit when… |
|---|---|---|
| Client/server interaction | HTTPS/JSON APIs | Frequent bidirectional real-time interactions are needed |
| Main datastore | PostgreSQL + PostGIS | Query shape, consistency or load justifies something else |
| Deployment | One service with multiple instances if needed | Independent scaling or operational boundaries justify separation |
| Cache | None initially | Profiling shows repeated expensive reads and acceptable staleness |
| Asynchronous work | In-process for genuinely short operations | Long or failure-prone steps require durable jobs |

#### 5. Senior-level thinking

The wrong question: *“Should I use Kafka and Redis?”*  
The better question: *“What are my load, latency, consistency and failure requirements, and what is the least complex design that satisfies them?”*

A senior engineer does not merely recognize tools. They can explain **why the current architecture is sufficient**, what would force a redesign, and how to validate the decision with metrics.

#### 6. Practice: do this before Lesson 0.02

1. State three functional requirements for the route-aware stop finder.
2. Choose three measurable non-functional requirements. Label assumptions versus confirmed needs.
3. Draw a request path from browser to persistence and back. Identify two likely failure points.
4. Explain one reason **not** to add Redis on day one and one signal that would make you reconsider.
5. Define what should happen if the external route provider times out after the backend has already started processing.

**Assessment:** Your answers should be specific enough that another engineer could implement and test them. Bring your answers into the chat; I'll review them, discuss the trade-offs, and then teach 0.02.

---

<a id="lesson-0-02"></a>

### 0.02 — How to prepare

**Target:** A deliberate learning loop, practice, feedback, and depth.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-0-03"></a>

### 0.03 — Delivery framework

**Target:** Requirements, entities, APIs, data flows, high-level design, deep dives.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="module-1"></a>

## Module 1 — Core concepts

**Outcome:** use fundamental system design language accurately and connect it to actual implementation choices.

<a id="lesson-1-01"></a>

### 1.01 — Networking essentials

**Target:** DNS, TCP, TLS, HTTP, CDNs, latency, timeouts.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-1-02"></a>

### 1.02 — API design

**Target:** REST, resource contracts, auth, idempotency, pagination, versioning.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-1-03"></a>

### 1.03 — Data modeling

**Target:** Entities, relationships, constraints, normalization, transactions.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-1-04"></a>

### 1.04 — Caching

**Target:** Cache placement, TTL, invalidation, consistency, stampedes.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-1-05"></a>

### 1.05 — Sharding

**Target:** Partition keys, hotspots, rebalancing, operational cost.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-1-06"></a>

### 1.06 — Consistent hashing

**Target:** Distribution, virtual nodes, scale-in/out.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-1-07"></a>

### 1.07 — CAP theorem

**Target:** Consistency, availability, partitions, eventual convergence.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-1-08"></a>

### 1.08 — Database indexing

**Target:** B-trees, composite indexes, query plans, write overhead.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-1-09"></a>

### 1.09 — Numbers to know

**Target:** Throughput, latency, storage, rough capacity estimates.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="module-2"></a>

## Module 2 — Key technologies

**Outcome:** know what each infrastructure component is for, how it fails, and when a simpler alternative suffices.

<a id="lesson-2-01"></a>

### 2.01 — Core database

**Target:** What persistence must guarantee.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-2-02"></a>

### 2.02 — Relational databases

**Target:** SQL, relational integrity, ACID, isolation.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-2-03"></a>

### 2.03 — NoSQL databases

**Target:** Access patterns, key-value, document and wide-column systems.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-2-04"></a>

### 2.04 — Blob storage

**Target:** Object stores, signed uploads and CDN delivery.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-2-05"></a>

### 2.05 — Search-optimized database

**Target:** Inverted indexes and search use cases.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-2-06"></a>

### 2.06 — API gateway

**Target:** Routing, rate limits and authentication boundaries.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-2-07"></a>

### 2.07 — Load balancer

**Target:** L4 versus L7, health checks and failover.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-2-08"></a>

### 2.08 — Queue

**Target:** Async processing, delivery semantics, poison messages.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-2-09"></a>

### 2.09 — Streams and event sourcing

**Target:** Logs, offsets, consumer groups and event history.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-2-10"></a>

### 2.10 — Distributed lock

**Target:** Mutual exclusion, leases and fencing.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-2-11"></a>

### 2.11 — Distributed cache

**Target:** Replication, eviction and invalidation.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-2-12"></a>

### 2.12 — CDN

**Target:** Edge caching, cache-control, origin protection.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-2-13"></a>

### 2.13 — Redis deep dive

**Target:** Data structures, caching and coordination.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-2-14"></a>

### 2.14 — Elasticsearch deep dive

**Target:** Inverted indexes, relevance, refresh delay.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-2-15"></a>

### 2.15 — Kafka deep dive

**Target:** Partitions, durable events, ordering and retries.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-2-16"></a>

### 2.16 — Temporal deep dive

**Target:** Durable workflows and process recovery.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-2-17"></a>

### 2.17 — API Gateway deep dive

**Target:** Gateway trade-offs and security.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-2-18"></a>

### 2.18 — Cassandra deep dive

**Target:** Wide-column architecture and high-write workloads.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-2-19"></a>

### 2.19 — DynamoDB deep dive

**Target:** Partition keys, secondary indexes and capacity.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-2-20"></a>

### 2.20 — PostgreSQL deep dive

**Target:** SQL, transactions, indexes, EXPLAIN, replication.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-2-21"></a>

### 2.21 — Flink deep dive

**Target:** Stream processing, event time and state.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-2-22"></a>

### 2.22 — ZooKeeper deep dive

**Target:** Coordination, watches and consensus context.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="module-3"></a>

## Module 3 — Common patterns

**Outcome:** identify recurring failure/scaling shapes and apply patterns with justified trade-offs.

<a id="lesson-3-01"></a>

### 3.01 — Real-time updates

**Target:** Polling, SSE, WebSockets, connections and reconnection.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-3-02"></a>

### 3.02 — Dealing with contention

**Target:** Optimistic concurrency, locking, queues.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-3-03"></a>

### 3.03 — Multi-step processes

**Target:** Sagas, compensations, workflows and durable execution.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-3-04"></a>

### 3.04 — Scaling reads

**Target:** Read replicas, caches, denormalized projections.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-3-05"></a>

### 3.05 — Scaling writes

**Target:** Partitioning, batching, buffering and backpressure.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-3-06"></a>

### 3.06 — Handling large blobs

**Target:** Direct upload, multipart upload, metadata and CDN.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-3-07"></a>

### 3.07 — Managing long-running tasks

**Target:** Jobs, queues, retries, visibility and status.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-3-08"></a>

### 3.08 — Proximity-based services

**Target:** Spatial indexing, geohashes and nearest-neighbor queries.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-3-09"></a>

### 3.09 — Pattern selection

**Target:** Diagnosing bottlenecks before adding complexity.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="module-4"></a>

## Module 4 — Question breakdowns and practice

**Outcome:** independently produce a credible design, explore bottlenecks, and communicate the decision trail.

<a id="lesson-4-01"></a>

### 4.01 — Bitly

**Target:** URL IDs, redirects and storage.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-4-02"></a>

### 4.02 — Dropbox

**Target:** File uploads, synchronization and metadata.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-4-03"></a>

### 4.03 — Local delivery service

**Target:** Orders, assignment and tracking.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-4-04"></a>

### 4.04 — Ticketmaster

**Target:** Inventory, seat holds and high contention.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-4-05"></a>

### 4.05 — Facebook News Feed

**Target:** Fanout and ranking.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-4-06"></a>

### 4.06 — Tinder

**Target:** Matching, discovery and location.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-4-07"></a>

### 4.07 — LeetCode

**Target:** Sandboxed code execution and job orchestration.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-4-08"></a>

### 4.08 — WhatsApp

**Target:** Messaging, delivery guarantees and offline devices.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-4-09"></a>

### 4.09 — Rate limiter

**Target:** Counters, token buckets and distributed coordination.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-4-10"></a>

### 4.10 — YouTube

**Target:** Upload, transcoding and streaming.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-4-11"></a>

### 4.11 — Facebook Live Comments

**Target:** Real-time event delivery.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-4-12"></a>

### 4.12 — YouTube Top K

**Target:** Streaming aggregation and top-k algorithms.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-4-13"></a>

### 4.13 — Uber

**Target:** Location, dispatch and matching.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-4-14"></a>

### 4.14 — Web crawler

**Target:** URL scheduling, politeness and deduplication.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-4-15"></a>

### 4.15 — Ad click aggregator

**Target:** Event ingestion and time-window aggregation.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-4-16"></a>

### 4.16 — Facebook Post Search

**Target:** Indexing and distributed search.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-4-17"></a>

### 4.17 — Yelp

**Target:** Geo-search, reviews and ranking.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-4-18"></a>

### 4.18 — Instagram

**Target:** Media lifecycle and social feeds.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-4-19"></a>

### 4.19 — Strava

**Target:** Activity ingestion and geo data.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-4-20"></a>

### 4.20 — Distributed cache

**Target:** Cache nodes, partitioning and eviction.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-4-21"></a>

### 4.21 — Online auction

**Target:** Bidding, ordering and contention.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-4-22"></a>

### 4.22 — Job scheduler

**Target:** Scheduling, execution and retries.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-4-23"></a>

### 4.23 — News aggregator

**Target:** Ingestion, dedupe and ranking.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-4-24"></a>

### 4.24 — Price tracking service

**Target:** Crawling, change detection and alerts.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-4-25"></a>

### 4.25 — Notification system

**Target:** Multi-channel delivery and preferences.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-4-26"></a>

### 4.26 — Robinhood

**Target:** Quotes, orders and financial correctness.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-4-27"></a>

### 4.27 — Google Docs

**Target:** Collaborative editing and concurrency.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-4-28"></a>

### 4.28 — Payment system

**Target:** Idempotency, ledger design and reconciliation.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-4-29"></a>

### 4.29 — Metrics monitoring

**Target:** High-cardinality ingestion and time series.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-4-30"></a>

### 4.30 — Online chess

**Target:** Game state, timing and real-time moves.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-4-31"></a>

### 4.31 — ChatGPT

**Target:** Request streaming, inference scheduling and conversation state.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-4-32"></a>

### 4.32 — Flash sale

**Target:** Traffic bursts, inventory and oversell prevention.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-4-33"></a>

### 4.33 — Extra practice: food reviews

**Target:** A service with reviews, discovery and moderation.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-4-34"></a>

### 4.34 — Extra practice: game leaderboard

**Target:** Rank storage and hot keys.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-4-35"></a>

### 4.35 — Extra practice: donations

**Target:** Donation processing and accounting.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-4-36"></a>

### 4.36 — Extra practice: GitHub Actions

**Target:** Durable workflow jobs and execution fleets.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="module-5"></a>

## Module 5 — Advanced topics

**Outcome:** recognize advanced workload shapes and understand the tools and limitations in each.

<a id="lesson-5-01"></a>

### 5.01 — Proximity search

**Target:** Spatial indexing and relevance.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-5-02"></a>

### 5.02 — Vector databases

**Target:** Embeddings, approximate nearest neighbors, hybrid search.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-5-03"></a>

### 5.03 — Time-series databases

**Target:** Retention, downsampling and high-volume writes.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-5-04"></a>

### 5.04 — Data structures for big data

**Target:** Bloom filters, sketches and approximate counting.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-5-05"></a>

### 5.05 — Change data capture

**Target:** WAL, outbox, event projections and replication.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="module-6"></a>

## Module 6 — In the wild: real engineering stories

**Outcome:** extract useful engineering lessons from production architectures rather than memorizing diagrams.

<a id="lesson-6-01"></a>

### 6.01 — Shopify inventory reservations

**Target:** Inventory correctness under concurrency.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-6-02"></a>

### 6.02 — Discord message storage

**Target:** Message partitioning and access patterns.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-6-03"></a>

### 6.03 — Slack job queue

**Target:** Operational queues at scale.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-6-04"></a>

### 6.04 — Figma multiplayer

**Target:** Collaboration and concurrent edits.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-6-05"></a>

### 6.05 — Spotify data lake

**Target:** Analytical pipelines and data evolution.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-6-06"></a>

### 6.06 — Meta ZGateway

**Target:** Edge systems and service infrastructure.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="module-7"></a>

## Module 7 — Full-stack implementation labs (custom additions)

**Outcome:** be able to implement, deploy and operate a practical full-stack backend.

<a id="lesson-7-01"></a>

### 7.01 — Backend foundations

**Target:** FastAPI service, typed contracts and local environment.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-7-02"></a>

### 7.02 — SQL and transactions

**Target:** PostgreSQL schema, migration, index, EXPLAIN and isolation.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-7-03"></a>

### 7.03 — Authentication and authorization

**Target:** Identity, sessions, JWT trade-offs, RBAC and ownership checks.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-7-04"></a>

### 7.04 — Caching and performance

**Target:** Redis, cache policies, profiling and load testing.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-7-05"></a>

### 7.05 — Background processing

**Target:** Queue, idempotent worker, retries and dead-letter handling.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-7-06"></a>

### 7.06 — Infrastructure and deployment

**Target:** Containers, CI/CD, environments and secrets.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-7-07"></a>

### 7.07 — Reliability and security

**Target:** Tracing, metrics, alerting, backups, threat modeling and recovery.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

<a id="lesson-7-08"></a>

### 7.08 — Capstone design review

**Target:** Architecture decision record, failure drills and senior-level presentation.

**Session template (to complete together):** intuition → mechanics → alternatives → production failure modes → practical exercise → 3–5 question assessment.

## Senior full-stack readiness rubric

Before finishing the curriculum, you should be able to do the following without copying a reference architecture:

- **APIs:** design documented interfaces with pagination, authentication, request validation, idempotency and useful failure responses.
- **Data:** choose constraints, indexes and transaction boundaries; write and interpret SQL queries and basic query plans.
- **Distributed behavior:** explain retries, duplicate delivery, at-least-once processing, stale caches, locks and data races.
- **Infrastructure:** deploy a service with configuration, secrets, migrations, health checks and a rollback strategy.
- **Reliability:** set service-level objectives, instrument telemetry, identify bottlenecks and describe an incident response.
- **Communication:** document trade-offs in an Architecture Decision Record, critique your own design and justify simplicity.

**Next lesson:** 0.02 — How to prepare. First, complete the five practice questions in 0.01.

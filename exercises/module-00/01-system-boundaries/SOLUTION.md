# Worked solution: system boundaries and workload

Attempt [the exercise](../../../lessons/module-00/01-from-features-to-systems.md#i-practical-exercise) first. This is one defensible solution to the stated hypothetical workload, not a description of the current StopAround application.

## Requirements and invariants

The search accepts a supported route and fuel preference, then returns matching station observations and observation times. The save operation creates a private journey owned by the authenticated caller and returns a stable identifier.

For the exercise, define the latency indicator as the fraction of eligible searches receiving a valid response within 1.5 seconds, measured from API ingress to completion of response transmission at that boundary. Target at least 95% over seven days. This is a combined timeliness-and-success target; count timeouts as failures. It excludes the browser's network and rendering time, which need a separate user-experience measurement.

Define availability as valid search responses divided by eligible searches over 30 days, with an illustrative 99.5% target. Count dependency timeouts and overload rejections as failed eligible searches. A 4xx response is not automatically a caller mistake: classification follows the request contract and failure cause. Missing final responses must remain visible through ingress accounting and deadlines rather than disappearing from success-only instrumentation.

Three invariants are: only the owner can read or mutate a private journey; each successful retry of one save operation identifies the same journey; and an observation older than 30 minutes is accompanied by a freshness warning. Distinguish observation time from import time. Reimporting an old observation does not make it fresh. Compare timestamps at a defined response-evaluation time with monitored clock synchronization.

## Responsibilities

The browser collects input, renders warnings, and retains a save operation key across retries. The API validates input, authenticates the caller, enforces resource ownership, bounds provider work, and coordinates durable writes. PostgreSQL owns saved journeys and committed operation outcomes. The import process validates external observations and preserves their source timestamps. The routing provider owns the computation it performs; its failure is not evidence that no station exists.

## Capacity calculation

`100,000 users/day × 4 searches/user = 400,000 searches/day`.

`400,000 searches/day ÷ 86,400 seconds/day = 4.6296 searches/second` average.

`4.6296 × 8 = 37.0370 searches/second` illustrative peak.

At a stable peak interval, `37.0370 requests/second × 0.300 seconds/request = 11.1111 requests` in flight on average. At a 3-second mean residence time, `37.0370 × 3 = 111.1111 requests`.

If each search performs one database operation holding a connection for 20 milliseconds, a separate illustrative estimate is `37.0370 operations/second × 0.020 seconds/operation = 0.7407 occupied connections` on average. This is not a recommended pool size: it excludes bursts, long transactions, imports, other endpoints, and capacity limits. It demonstrates why request lifetime and connection lifetime are different quantities.

## Lost response and retry

The browser sends operation K with payload P as user U. The API validates the request. Within a database transaction, it coordinates the unique operation identity `(U, K)`, stores a fingerprint of P, creates the journey, and records its result. It commits; the response is lost. The browser retries with U, K, and P. The API finds the committed operation, checks the fingerprint, and returns the same journey identifier.

Concurrent attempts must coordinate on the durable unique identity. A conflicting in-progress attempt may wait for the transaction or receive a documented retryable response. A changed payload under the same key is a conflict. A rollback leaves no successful operation outcome. Define key retention before promising an unlimited deduplication window. This is a protocol design exercise; a later idempotency lesson must implement and test these cases.

## Infrastructure decisions

Begin without a separate search cache: the exercise provides no measured read bottleneck and freshness rules already require care. Revisit caching if repeated equivalent searches consume a measured resource and acceptable reuse rules are defined.

Begin without a broker for interactive searches. A bounded request matches the product contract. Run imports as a scheduled process. Consider durable jobs when work needs resumability, deferred completion, or explicit backlog handling. Neither a cache nor a broker replaces ownership checks or a transaction protocol.

## Failure investigation and degradation

Correlate API residence time with provider duration, attempt rate, database query duration, and pool checkout waits. Compare mean and tail latency. Check whether recent deployments extended transaction lifetimes or changed queries. Stable ingress with rising occupancy points to longer work or waiting, not necessarily more users.

If a route cannot be computed and no permitted route-specific fallback exists, return a clear temporary failure within the deadline. If the product explicitly permits an approximate result using a previously computed compatible route, label its age and limitations. An HTTP 200 containing an empty list would conceal a failed computation.

For the workshop extension, two callers can both read one remaining seat and both create reservations. Move the capacity decision and accepted reservation into one coordinated database operation or transaction. Conditional updates, row locks, or serializable transactions with retries are candidate mechanisms; each must also address cancellation and replayed requests.

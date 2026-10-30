# Networking essentials — worked solution

The supplied intervals total 520 ms: 20 + 90 + 300 + 80 + 30. Label the other 180 ms **unexplained**. The initial hypothesis is queuing or an omitted boundary; the numbers do not prove it. Verify that the supplied intervals are disjoint for the same request before adding them.

```text
Browser -> resolver
Browser -> edge/proxy -> worker admission -> handler -> database
Browser <- edge/proxy <- handler after commit
            response can disappear on this return path
```

First add correlated proxy timestamps for receiving the request, beginning the upstream exchange, and receiving upstream headers. Then measure application arrival to handler admission and connection-pool acquisition. These distinguish transit/proxy waiting, worker waiting, and downstream waiting. If all are accounted for, inspect browser scheduling and body consumption with the same request identifier. Do not log bearer tokens or raw private route data.

An illustrative one-second budget can reserve 200 ms for frontend/edge transport and response handling, 100 ms for admission, and 700 ms for application work. Within that last interval, reserve 100 ms for validation, commit, and serialization, leaving at most 600 ms for dependencies. These are proposed limits, not measurements or a universal good configuration. A dependency retry consumes what remains of the same 600 ms; it does not receive a new budget.

Give the API ownership of transient provider retries. The UI should reuse the same operation key for a repeated save and reconcile the persisted outcome. It should not generate a new key merely because the first response timed out. The API's durable operation record must commit with the journey; an in-memory remembered key cannot survive a restart.

The probe's first DNS lookup changes the environment for the subsequent connect lookup, and its connection interval includes TLS and library lookup work. Each execution opens a fresh connection. A second execution can benefit from resolver or network caches, but does not demonstrate persistent-connection reuse. Record the destination, timestamp, client location, status, and measured labels. An unreachable public endpoint is an environmental result, not evidence that the deterministic unit tests failed.

Check your answer: does each hypothesis predict a different measurement, is the missing interval still marked unknown, and can a lost response be retried without creating another journey? Run the Module 1 checks described in [the lab guide](../README.md).

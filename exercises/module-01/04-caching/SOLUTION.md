# Caching — worked solution

Twenty overlapping misses for one key should invoke one origin loader and share its result in this process. The tests hold that loader behind an event, admit callers, and then release it. Canceling one waiter should leave the shared load available to another; shutdown intentionally cancels shared work.

One hundred distinct keys are a different workload. With eight active distinct loads held open, new distinct misses receive CacheBusy. Existing-key waiters can join admitted work. This component does not cap the total number of incoming requests or waiters; the hosting API needs its own admission and deadline limits. Timeouts prevent a cooperative asynchronous loader from occupying a slot indefinitely.

The invalidation race is:

```text
R: miss -> read version 1 -----------------> fill version 1
W:               commit version 2 -> delete key
```

The final cache can contain version 1. Commit-then-delete is a sensible baseline, not a universal freshness proof. For a public price display, choose a bounded stale policy and show provider observation time. A 30-second cache residence limit alone does not bound provider source age. During provider failure, permit only a separately defined stale window and limit origin refresh work.

For permissions, a stale “allowed” decision can leak private data after revocation. Prefer a fresh authorization check or an explicitly designed revocation/invalidation mechanism. A user-scoped result key prevents accidental cross-user reuse but does not by itself revoke a previously valid user.

Monitor source age and representation version, useful hit rate, distinct active loads, rejected loads, pending waiters at the API, evictions, and memory. The tested cache holds UTF-8 strings with a configured byte limit and bounds entry count; its loader must still bound upstream bodies before allocation. It does not implement Redis locks or distributed invalidation.

# Sharding — worked solution

Resolve and retain a route, write a value, then freeze its bucket. Writes and reads for that bucket raise Unavailable. Copy to C and publish cutover; the new route has the same bucket, owner C, and epoch incremented by one. The old route raises StaleRoute. Refreshing the route returns the copied value. The ownership map for every other bucket remains unchanged.

Aborting before cutover reopens the original owner. Copying alone does not change authority. Data left on a destination after an aborted copy is not authoritative, and the next copy clears stale destination keys in that bucket before installing the source snapshot. In a real system, cleanup and space limits still need explicit operation plans.

A real pause-based migration needs a durable migration identity and state machine. Fence new writes at the source, wait for previously accepted transactions to finish, copy a consistent state, verify counts and stronger content checks as appropriate, and establish destination readiness. Publish new ownership under a coordinated epoch, with the old owner unable to accept late writes. Reopen traffic under the new epoch.

The atomic enforcement location matters. A router can validate epoch 1, pause, and resume a write after epoch 2 is published. An independent remote database write will not know that the router's earlier check expired. Use a storage-enforced fence or a lock/drain protocol that prevents such a writer from committing. Merely refreshing the router map more often does not close the race.

Crash before cutover should leave a durable state that identifies the source as authority and permits a verified retry or abort. Crash after ownership publication should recover the new owner without reopening stale source writers. The in-memory model does not persist either state and is not evidence of crash-safe migration.

Directory unavailability deliberately fails closed in the model. A real design may maintain safely fenced local ownership, but that requires a specified agreement protocol. Consistent hashing changes the mapping mechanism; it does not remove these ownership transitions.

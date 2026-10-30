# Consistent hashing — worked solution

With A at 20, B at 60, and C at 90, the supplied keys map as follows:

| Key position | Initial owner | After adding D at 45 | After then removing B |
|---|---|---|---|
| 10 | A | A | A |
| 20 | A | A | A |
| 35 | B | D | D |
| 60 | B | B | C |
| 85 | C | C | C |
| 95 | A | A | A |

This uses the inclusive-successor boundary: a key exactly at a token belongs to that token's owner. After D joins, only key 35 among this supplied set moves, and its destination is D. After B leaves the expanded ring, key 60 moves to C. Other keys in B's former interval would also move; the table is not the entire ring.

Run the digest-based example for observed distribution. To compare one and 128 virtual nodes, construct HashRing with the same physical names and different virtual_nodes values, then count owners for a fixed key set. Report the fixture and count; do not infer universal balance from one sample. Changing virtual-node count for existing nodes is itself a membership/configuration transition.

For a disposable cache, a new owner can miss and reload from an authority under bounded origin capacity. For durable journey storage, missing data on the new owner requires a transfer and recovery protocol. Copy the relevant state, reconcile concurrent changes if allowed, publish ownership under a coordinated epoch, and fence old writers. Also define replication and acknowledged-write durability separately.

The checks verify deterministic membership ordering, addition and removal properties, exact boundaries, and wraparound. They do not test a distributed membership service, node failure, data transfer, or recovery from an old owner that continues running.

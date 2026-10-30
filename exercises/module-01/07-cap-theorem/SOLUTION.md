# CAP theorem — worked solution

In cp mode, partition, write 1 at A, and read B: the read raises Unavailable. A remains the fixed authority. After heal, both reads return 1. In ap mode, the same B-side read succeeds with 0, demonstrating a successful stale observation after the A write completed. Healing propagates 1 when there is no competing update.

For concurrent AP assignments, A holds `(1, A, 10)` and B holds `(1, B, 20)`. Healing chooses the larger logical-counter/node tuple, so both return 20. This is a deterministic tie-break, not proof that B's human action happened later. A's assignment is not retained in the merged register.

A public-price contract can permit stale observations if it exposes their observation time and bounds the product's stale-serving policy under stated assumptions. During a prolonged partition, a strict source-age bound may require stopping successful reads once that bound is exceeded. Eventual consistency alone cannot guarantee the bound.

A private-edit contract can require the authoritative owner/version check, return an unavailable status when that authority cannot be established, and preserve the original operation key through retries. Do not switch to an independently writable old replica merely to obtain a successful status. A previously accepted write can still have an unknown client outcome if its response was lost.

Three replicas add placement choices, not an automatic consistency guarantee. A majority protocol can let an authoritative majority continue while a minority rejects operations, but membership, promotion, versioning, and fencing must be specified. A fleet-wide availability SLO can remain useful while differing from the theorem's universal guarantee.

The tests verify these local histories only. They do not run network servers, implement a consensus algorithm, model primary crashes, or prove a real database's partition behavior.

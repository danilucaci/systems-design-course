# Data modeling — worked solution

User to journey is one-to-many. Journey to stop is one-to-many. A completed create request has an owner/key primary key and references exactly one journey. Multiple different creation requests may create journeys with the same name. The composite foreign keys prevent owner and journey from disagreeing; they do not implement read authorization or database row-level security.

A Bob-owned stop for Alice's journey fails the composite foreign key. A negative position fails CHECK. A second stop at the same journey/position fails the primary key. Positions 0 and 2 without position 1 are permitted, as are repeated station identifiers at distinct positions. Station existence is not checked by this intentionally limited schema.

A station extension can use a stable station identifier with provider identities in a separate mapping table. Store price observations with station, provider, stable provider-observation identifier, decimal amount, currency, volume unit, observed-at, and ingested-at. A unique provider/observation pair deduplicates repeated deliveries. If the provider lacks stable identifiers, define a documented approximation and its collision and correction behavior rather than assuming timestamps are unique.

The latest-price projection chooses a deterministic winning observation for a station and fuel type under a freshness policy. It can retain observation ID and observed-at, allowing readers to expose age. Rebuild it from authoritative observations and periodically compare it with source history. Late arrival must not blindly replace a newer event just because it was ingested later.

For atomic reordering, lock the journey row, verify the expected journey version and authenticated owner, then replace its small stop set inside the same transaction and increment the journey version. Deleting and reinserting the set avoids transient primary-key collisions from swapping positions. Validate the full proposed set before changing it. Other stop writers must follow the same parent-lock/version protocol; the database does not infer that convention from the foreign key.

For a larger ordered set, alternative rank schemes or a deferrable uniqueness design can reduce rewrite work, but add their own ordering and concurrency rules. Begin with the short, bounded transaction when the product has a modest number of stops.

Run the checks from [the lab guide](../README.md). They create unique temporary schemas, use real PostgreSQL transactions, and remove only the schemas they created. A passing schema test does not establish an unimplemented station catalog, migration strategy, or spatial index.

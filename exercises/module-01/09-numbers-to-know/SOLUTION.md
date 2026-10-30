# Numbers to know — worked solution

All values below are illustrative inputs and arithmetic, not measured instance capacity or a production recommendation.

| Quantity | Calculation | Result |
|---|---|---|
| Mean in-flight attempts | 500/s × 0.2 s | 100 |
| Nominal capacity at 60% target | 500/s ÷ 0.6 | about 833.3/s |
| Logical retained bytes | 20/s × 86,400 s/day × 30 days × 1,000 B | 51,840,000,000 B |
| Logical GB and GiB | bytes ÷ 10^9; bytes ÷ 2^30 | 51.84 GB; about 48.28 GiB |
| Three copies plus 30% overhead | logical bytes × 3 × 1.3 | 202,176,000,000 B |
| Response bodies | 500/s × 2,000 B | 1 MB/s; 8 megabits/s |
| Instances tolerating one loss | (N − 1) × 300/s × 0.6 ≥ 500/s | N = 4 |

At 1.5 mean attempts, attempted rate is 750/s, average in-flight attempts are 150 if mean attempt time stays 200 ms, and nominal capacity is 1,250/s. One-failure sizing becomes `(N − 1) × 300 × 0.6 >= 750`, so N = 6 under the linear-scaling assumption. Retry failure often also raises duration, so constant latency must be tested.

Logical retained rows and bytes stay unchanged because the write input counts distinct records and the model assumes idempotent retried mutations. Doubling record size doubles both logical and modeled physical storage, without changing request concurrency. Response bandwidth changes only if response size or attempted response traffic also changes; record size and response size are independent inputs.

The queue grows at 100 − 50 = 50 jobs/s for thirty seconds, accumulating 1,500 jobs. Afterward it drains at 50 − 25 = 25 jobs/s, requiring sixty seconds under the constant-rate assumptions. Dividing by the full 50/s would incorrectly ignore ongoing arrivals.

Three influential unknowns are peak endpoint mix and fan-out, mean latency/connection hold time under failure, and physical storage per logical record including indexes. Measure provider calls per admitted request, trace the relevant timing boundaries under representative load, and compare encoded payload, table, and index sizes. Also inspect backup and migration space separately; the model explicitly excludes them.

The executable checks validate unit conversions, retry arithmetic, and invalid inputs. They do not establish a latency SLO, a benchmark for a particular machine, or the linear scaling assumed in the instance-count example.

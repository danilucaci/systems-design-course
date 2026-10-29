# Worked solution: prepare with an evidence log

Attempt [lesson 0.02's exercise](../../../lessons/module-00/02-how-to-prepare.md#i-practical-exercise) before reading this example. This is a local learning experiment; none of its counts is a production throughput measurement.

## Question, invariant, and prediction

Question: does one shared gate bound active work without dropping submitted operations?

Invariant: the number of operations in the counted work interval never exceeds the shared permit limit. Completion requirement: all ten submitted operations eventually finish in this successful, uncancelled workload.

Before execution, predict maximum-active counts of 1, 2, and 10 for the three limits, with a completed count of 10 in each run. A zero-request workload should report zero for both counters.

## Evidence to record

Run the script and test commands given in the lesson, and record the actual Python version from your environment. The probe prints one JSON object per configuration. Compare the values to your predictions rather than recording only that the program exited successfully.

The active interval begins after permit acquisition and ends in `finally`. Waiting for a permit is outside that count. All tasks share one event loop and one semaphore object during each probe invocation. `asyncio.sleep(0)` exposes overlap by yielding; it does not represent 300 milliseconds of provider work.

## Mutation and its interpretation

In a disposable copy, create a separate semaphore inside each `operation` and use that local gate. Every operation can acquire its own permit, so the group is no longer limited to two. The maximum-active assertion should fail for ten submitted operations, even though all ten still complete.

This mutation checks whether the test can detect loss of shared coordination. It does not prove the test detects every possible concurrency defect. Restore the original code after the experiment.

## Limits of the conclusion

The local probe does not establish that several API processes obey one global limit. Each process could have its own gate and permit budget.

It also does not establish the allowed call rate, latency, cancellation behavior, or availability of a real routing provider. A concurrency budget and a requests-per-second budget are different constraints. Integration tests and representative measurements are needed for those boundaries.

## StopAround investigation

Hypothesis A: the provider takes longer, but the API checks out database connections only during short database operations. Hypothesis B: requests hold checked-out connections while awaiting the provider, so the slowdown also consumes pool capacity.

Measure provider-call duration and database connection checkout-to-return duration for correlated requests. Also separate time waiting to acquire a connection from time holding one. Inspect the code path that determines when a connection is acquired and released.

An unsafe conclusion is “increase the pool because the API is slow.” A larger pool may only let more work accumulate against a constrained database. First identify which boundary is responsible for longer occupancy.

## A useful continuation checkpoint

“The single-process probe completed ten operations and bounded active work to two. The deliberately unshared-gate mutation failed the maximum-active assertion. Next, inspect the StopAround search path to find whether provider calls occur inside a database connection's lifetime. Correlate the two timing intervals before changing a pool budget.”

For the workshop extension, check accepted reservation count, final capacity, and the outcomes returned to both callers. With one remaining seat and two competing new reservations, the intended contract might allow exactly one accepted reservation and one conflict. A test that inspects HTTP status alone could miss an incorrect stored count or a response sent before commit.

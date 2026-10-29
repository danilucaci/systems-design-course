# How to prepare

Lesson 0.02 · Foundations & delivery framework

## A. Learning objectives and prerequisites

By the end of this lesson, you should be able to build a learning session around a specific engineering question, make a prediction before running an experiment, choose evidence that can disprove a design claim, and decide whether you are ready to move on. You should also distinguish an interview explanation from an implementation check and an operational check.

Read [0.01 — Introduction](01-from-features-to-systems.md) first. It establishes system boundaries, invariants, unknown outcomes, and the difference between rate and concurrency. You need enough Python familiarity to run a short script; understanding every asyncio detail is not a prerequisite. Async Python receives its own treatment during backend foundations.

This lesson prepares you to use [0.03 — Delivery framework](../../COURSE_TOC.md#lesson-0-03), then work through [Module 1](../../COURSE_TOC.md#module-1). The [worked exercise solution](../../exercises/module-00/02-how-to-prepare/SOLUTION.md) is separate so you can make your own predictions first.

## B. Mental model and intuition

Prepare to make a decision, not to recognize a diagram. Reading about a queue can help you explain its vocabulary, but production work asks different questions: what survives a crash, who retries, how duplicates are handled, and which observation would reveal a growing backlog?

A useful learning session leaves behind a small claim and evidence about that claim. For example: “Limiting concurrent calls to two will keep active calls at or below two, while eventually completing all ten submitted operations.” That claim has a boundary, an expected result, and a way to fail. “I understand concurrency” has none of those properties.

Your frontend experience already provides a good starting point. You distinguish a component's inputs from its internal state, inspect a waterfall when an interaction is slow, and test the behavior that a user observes. Apply the same habits to services and data. Draw the boundary, identify the state, inspect the events, and check the promised outcome.

The course will repeatedly use a loop: explain a mechanism, predict its behavior, exercise it, inspect evidence, and revise the explanation. The purpose is not to collect passing experiments. A surprising result is valuable when you can locate the assumption it contradicts. Confidence should become more specific as you learn, rather than simply becoming stronger.

## C. Deep technical explanation

### Turn a topic into a question you can answer

A topic names a large area: transactions, caching, replication, or authentication. A question identifies a decision inside that area. “Can two requests reserve the last seat?” is a better starting question than “How does PostgreSQL work?” The smaller question gives you a workload, a required property, and a concrete failure to investigate.

Write three things before using a tool. First, state the property you want to preserve. Second, state what you believe the mechanism will do. Third, identify an observation that would show the belief is wrong. For the concurrency example, the property is bounded active work. The mechanism is a shared gate. A maximum-active counter greater than the limit would refute the claim.

Be careful about the scope of a successful observation. A local gate may coordinate operations inside one process; it does not demonstrate coordination across three API processes. A fake provider can reveal scheduling behavior; it does not establish a real provider's rate limit. Every conclusion needs a boundary as explicit as the experiment's inputs.

### Separate three kinds of competence

**Explanation competence** means you can describe the mechanism and its trade-offs. For example, you can distinguish waiting for an available resource from performing useful work. Explain the state transitions with a small request timeline, without relying on a product name as the explanation.

**Implementation competence** means code enforces the property under relevant conditions. A concurrency limiter must release its permit when work fails. A write must preserve ownership checks on every path. A test should observe the promised outcome, not merely assert that a helper was called.

**Operational competence** means you can detect and recover when assumptions fail. If a dependency becomes slow, which metric distinguishes too much incoming work from longer residence time? What can you disable safely? What state remains after a process restarts? These questions require evidence from the running boundary, not just a unit test.

You do not need all three at maximum depth before proceeding with every introductory lesson. You do need to record which one you have exercised. An articulate explanation plus one happy-path test is useful progress, but it is not proof that the service is ready for production.

### Choose evidence that distinguishes competing explanations

Suppose an API becomes slow while traffic stays flat. One hypothesis is that the external route provider is slower. Another is that database connections are held while the API waits for that provider. These hypotheses can both be true, but they predict different resource behavior. Measure provider duration and connection checkout duration separately; a total request timer alone cannot distinguish them.

An experiment becomes more useful when alternative explanations predict different observations. If you are testing a concurrency limit, compare one permit, two permits, and a limit large enough for all submitted work. If the measured maximum is identical in every case, investigate whether the workload actually overlaps or whether the metric measures the wrong interval.

Controlled experiments change a relevant input while holding other assumptions steady. They are especially useful in an isolated development environment. In production, prefer existing observations and low-risk mitigations before deliberately disturbing a service. Google's [Effective Troubleshooting](https://sre.google/sre-book/effective-troubleshooting/) describes diagnosis as forming hypotheses and looking for confirming or disconfirming evidence.

### Design a test around an observable contract

A good test needs a contract, an input, and an observation. “All ten requests finish, with no more than two active operations at once” yields two independent assertions. Testing only the limit might miss dropped requests. Testing only the completion count might miss an ineffective limit.

Make the observation at the point where the property matters. Increment an active-operation counter after acquiring the gate, not before it. Counting before acquisition would measure active plus waiting operations. Both quantities can be useful, but they answer different questions. This is the same boundary discipline used in latency and database-pool measurements.

Prefer a deterministic way to expose the condition you care about. A scheduling yield lets several tasks become runnable without claiming a real network delay. For an eventual database race test, coordinate the competing operations deliberately instead of hoping a sufficiently large number of random requests happens to reveal the bug.

Passing tests reduce uncertainty within their scope. They do not prove that every failure has been considered. Google's [Testing for Reliability](https://sre.google/sre-book/testing-reliability/) distinguishes different testing boundaries and explains why passing tests alone do not establish reliability. Use that limitation to choose your next check, rather than abandoning useful automated tests.

### Keep an evidence log that another engineer could use

For each substantial exercise, save a compact record:

- Question and invariant.
- Assumptions, including process count and workload.
- Prediction made before execution.
- Exact command and relevant input values.
- Observed result and what it rules out.
- What remains untested and the next decision.

This is not a diary of every keystroke. It is a reproducible argument. Someone else should be able to rerun the experiment and understand why it supports a particular conclusion. Include versions when behavior depends on a database, library, or deployment configuration.

Use measured and illustrative values differently. A value printed by a toy model is evidence about that model's behavior. It is not a measured capacity of your FastAPI application, even if the model uses the same number of requests. A performance report needs the environment, representative data, workload shape, and measurement method.

### Build a sustainable sequence of sessions

After a workday, use a bounded question rather than an open-ended objective such as “learn distributed systems tonight.” An illustrative 30-minute session might use five minutes to reconstruct the mechanism, ten minutes for one experiment, ten minutes to explain the result and try a counterexample, and five minutes to record the remaining uncertainty.

The time allocation is a planning example, not a scientific prescription. A transaction lab may need several sessions; a prerequisite explanation may need one. End at a clear checkpoint rather than declaring a lesson complete because the allotted time expired.

At the next session, try to reconstruct the decision before rereading your notes. If you cannot explain which observation supported it, you have identified a precise gap. Revisit that gap instead of restarting an entire module. Readiness comes from the ability to apply and challenge an explanation, not the number of pages you have scrolled past.

## D. Architecture and data flow

The experiment has two paths: submitted work and evidence about that work. Keeping them distinct prevents a test from measuring a quantity that merely looks like the desired result.

```text
10 submitted operations
        |
        v
Shared gate: at most 2 permits
        |
        v
Active work interval ---------> active / maximum-active counters
        |
        v
Completion ------------------> completed-operation counter

Prediction: maximum_active <= 2 AND completed == 10
Observation: compare both counters, then revise or retain the claim
```

Waiting operations remain outside the active-work counter. The experiment uses one process and one event loop. That boundary is part of its design, and changing to several processes requires a new coordination question. The diagram does not imply a distributed queue, worker fleet, or production telemetry pipeline.

## E. Real-world examples

For StopAround, prepare for a slow-search investigation by writing down the request stages: validation, route computation, database access, ranking, and serialization. Then name one observation for each stage. If all you collect is total endpoint duration, several plausible causes remain indistinguishable.

Practice with a hypothetical incident: traffic is steady, provider duration grows, and connection wait time also grows. Your first question should be whether the API checks out a connection before waiting for the provider. Inspect the relevant code path and timing boundaries before proposing a larger database pool. An observed overlap can support that hypothesis; a graph alone cannot establish which request paths hold the connections.

For an independent example, consider a workshop reservation endpoint. A test that receives two successful HTTP responses does not prove the last seat was reserved correctly. Inspect accepted reservations and remaining capacity after the competing operations. You may need an assertion that exactly one request succeeds, one receives a conflict, and the stored capacity stays nonnegative.

These are illustrative exercises, not reports of production measurements. The transferable preparation habit is to choose evidence that reflects the business invariant rather than a convenient proxy such as a response code, helper invocation, or dashboard color.

## F. Executable example

This scheduling probe gives you a small mechanism to predict and test. It runs entirely locally with Python 3.10 or later. Ten operations compete for a shared semaphore, which is a counter of available permits. An operation acquires a permit before entering the interval counted as active and releases it on exit.

The executable source is [concurrency_probe.py](../../exercises/module-00/02-how-to-prepare/concurrency_probe.py):

```python
"""A local scheduling experiment, not a network or throughput benchmark."""

import asyncio
import json


async def probe(requests: int, limit: int) -> dict[str, int]:
    if type(requests) is not int or type(limit) is not int:
        raise ValueError("requests and limit must be integers")
    if not 0 <= requests <= 10_000 or not 1 <= limit <= 10_000:
        raise ValueError("requests must be 0..10000 and limit must be 1..10000")
    gate = asyncio.Semaphore(limit)
    active = maximum = completed = 0

    async def operation():
        nonlocal active, maximum, completed
        async with gate:
            active += 1
            maximum = max(maximum, active)
            try:
                await asyncio.sleep(0)
                completed += 1
            finally:
                active -= 1

    await asyncio.gather(*(operation() for _ in range(requests)))
    return {"completed": completed, "maximum_active": maximum}


async def main():
    for limit in (1, 2, 10):
        result = await probe(requests=10, limit=limit)
        print(json.dumps({"limit": limit, **result}))


if __name__ == "__main__":
    asyncio.run(main())
```

Before running it, predict the maximum active operations for limits 1, 2, and 10. Then run:

```sh
python3 exercises/module-00/02-how-to-prepare/concurrency_probe.py
python3 -m unittest discover -s exercises/module-00/02-how-to-prepare -v
```

For this workload and explicit scheduling yield, the three runs complete ten operations and reach maximum-active values of 1, 2, and 10 respectively. The tests also check an empty workload and reject invalid inputs before scheduling. The 10,000-operation bound is an explicit local-lab resource limit, not an estimate of a production service's capacity.

`asyncio.sleep(0)` yields control; it does not model a particular number of network milliseconds. The output contains counts, not latency or throughput measurements. `finally` restores the active counter if the operation exits exceptionally, while the context manager releases its permit. These behaviors are described in the Python documentation for [sleep](https://docs.python.org/3.10/library/asyncio-task.html#asyncio.sleep) and [semaphores](https://docs.python.org/3.10/library/asyncio-sync.html#asyncio.Semaphore). This example does not implement provider timeouts, durable jobs, or distributed coordination.

For a useful mutation experiment in a temporary copy, replace the shared gate with a separate semaphore inside each operation. Predict why the two-permit test should fail, then confirm the failure. Do not preserve that mutation as the solution. The failing test establishes that the gate must be shared across the operations it coordinates.

## G. Architectural decisions and trade-offs

Choose the learning method according to the uncertainty you need to reduce. More infrastructure does not automatically produce stronger evidence.

| Method | What it can establish | What still needs a different check |
|---|---|---|
| Explain a request timeline | You can identify boundaries and state transitions | The code actually follows that timeline |
| Small deterministic model | A mechanism behaves under explicit assumptions | A real dependency has the same behavior |
| Integration test | Components preserve a contract together | The production workload and failure distribution |
| Representative load test | Resource and latency behavior in the tested environment | Recovery from failures not included in the workload |
| Failure drill | Detection and recovery for a defined incident | Every other failure path |

Use the smallest experiment that distinguishes the current hypotheses. A model is appropriate for learning a scheduling boundary. Use PostgreSQL for a claim about PostgreSQL transaction behavior; a Python dictionary cannot establish that claim. Use a real HTTP boundary when client cancellation, response loss, or authentication behavior is the subject.

Keep interview practice and implementation practice connected but separate. An interview answer must communicate a defensible design under time constraints. An implementation exercise must demonstrate the contract. Operational practice adds telemetry, recovery, and the cost of change. Each produces evidence that the others cannot replace.

## H. Common failures and debugging

**Mistaking familiarity for readiness.** You recognize the diagram but cannot explain which state survives a restart. Close the reference and draw the failure timeline. If you cannot do it, record that exact gap and revisit the mechanism.

**Using a test that cannot fail for the claimed bug.** A test checks only that ten operations finish, so removing the concurrency limit leaves it green. Add the maximum-active assertion. A targeted mutation is a useful check that the assertion observes the property you intend.

**Measuring at the wrong boundary.** You count waiting requests as active provider calls. Inspect where counters are incremented and decremented. Give active work and queued work different names; a single ambiguous “in flight” metric can conceal the distinction.

**Changing too many inputs.** You change concurrency, request volume, data size, and retry policy, then attribute the result to one of them. Restore a baseline and vary one relevant factor. If factors must change together, state why and narrow the conclusion accordingly.

**Turning toy output into a production recommendation.** A local counter test passes with ten operations, so you choose ten database connections. Identify the missing evidence: real hold times, other workloads, bursts, process count, and database limits. The model did not answer the sizing question.

**Collecting tools instead of decisions.** You set up a broker before identifying a durability requirement. Return to the invariant and failure timeline. If a scheduled command meets the current contract, learning its recovery behavior is more valuable than configuring infrastructure without a reason.

## I. Practical exercise

Create a short evidence log for the scheduling probe, then prepare the next real-system experiment. Work through this before opening the [solution](../../exercises/module-00/02-how-to-prepare/SOLUTION.md).

1. State the bounded-work invariant and predict all three probe outputs before execution.
2. Run the script and tests. Record the command, Python version, result, and the boundary the counters measure.
3. In a temporary copy, move the semaphore inside each operation. Explain why a limit of two no longer constrains the group, then verify that the targeted test detects it.
4. Write two claims the successful original probe does not establish. One must involve several processes and one must involve a real external provider.
5. Design a StopAround investigation that distinguishes slow route computation from long database connection occupancy. Name the two measurements and identify an unsafe conclusion to avoid.
6. Write a checkpoint for a later session: the precise unresolved question, the next experiment, and what outcome would change your design.

The deliverable is the reasoning and a reproducible evidence log, not a screenshot of green tests. A strong answer explains both the supported claim and its limits. For additional practice, propose the database-state assertions needed to test the workshop's last-seat invariant.

## J. Interview and senior-engineering assessment

1. What makes “I understand queues” a weaker readiness claim than a specific delivery and recovery contract?
2. Why does testing both completion count and maximum active work matter in the probe?
3. A test passes with a local semaphore. Can you conclude that three API processes share its limit?
4. Why does a deliberately coordinated interleaving often teach more than a large random request burst?
5. Your model predicts a correct result, but an integration test fails. Which source should you trust, and how do you investigate?
6. What information belongs in a useful continuation checkpoint after a short evening session?
7. When should you move on from a lesson even though you have not implemented every production detail?

## Assessment solutions

### 1. A readiness claim needs an observable boundary

Queue vocabulary does not specify whether acknowledged work survives a restart, whether processing may repeat, or how a stuck item becomes visible. A useful claim identifies the operation, its guarantees, and the evidence that checks those guarantees. You can then test a defined failure instead of treating the presence of a queue product as proof of reliability.

### 2. The properties fail independently

A broken implementation can keep active work below two by silently dropping eight operations. Another can complete everything while allowing all ten to overlap. The completion assertion detects the first defect; the maximum-active assertion detects the second. Together they describe the intended local contract more accurately, while still leaving timeout and cancellation behavior to separate checks.

### 3. Process scope is part of the assumption

The semaphore belongs to one Python process and coordinates the operations that share that object. Three independently created gates do not form one global limit. A multi-process design needs an explicit shared coordination mechanism or a deliberately divided budget. The experiment supports a local scheduling claim, not a distributed one.

### 4. A controlled schedule makes the mechanism visible

A random burst might never create the problematic overlap, or might fail in ways you cannot reproduce. Deliberately arranging the relevant ordering makes the assumption testable. Randomized stress can supplement that test, but it should not be the only evidence for a race condition whose critical sequence you already understand.

### 5. Treat the disagreement as evidence

Do not dismiss the failing integration test merely because the model is simpler. Check the test's setup and observation boundary, reproduce the failure, and compare the real component's behavior with the model's assumptions. The model may omit transaction isolation, serialization, network outcomes, or process scope. Fix the explanation or implementation according to the actual contract, then retain a regression test for the discovered gap.

### 6. Record the decision still in front of you

Write the current claim, the assumptions, the exact result already observed, and the next question. Include a command or file location needed to resume. “Continue studying caching” is too vague; “test whether two simultaneous misses cause duplicate provider calls under this cache policy” identifies an executable next step and the result that could change the design.

### 7. Move on with an accurate account of the remaining gap

Proceed when you can explain the mechanism, predict an important failure, complete the required exercise, and distinguish tested behavior from assumptions. An introductory lesson need not solve all later production topics. Record a specific dependency to revisit, such as cancellation cleanup or cross-process coordination, and return to it in the relevant lesson. Do not count an unknown requirement as solved.

## K. Key takeaways and navigation

Prepare by turning topics into falsifiable engineering questions. Keep explanation, implementation, and operation distinct. Predict before executing, measure at the contract boundary, and test outcomes that can fail independently. A small experiment is strong evidence for a small claim; increasing the claim requires additional evidence.

Use a bounded session and leave a precise checkpoint. Your existing frontend debugging skills transfer when you follow ownership and state across the API and data layers. The goal is to make justified decisions and recover from failed assumptions, rather than recognize a standard architecture.

Review [0.01 — Introduction](01-from-features-to-systems.md), attempt the [exercise](#i-practical-exercise), or compare the [worked solution](../../exercises/module-00/02-how-to-prepare/SOLUTION.md). Next is [0.03 — Delivery framework](../../COURSE_TOC.md#lesson-0-03), currently listed in the verified syllabus and scheduled for the next writing batch.

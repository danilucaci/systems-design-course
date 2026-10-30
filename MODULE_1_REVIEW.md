# Module 1 review

Reviewed on 2026-10-30 against the user’s Module 1 request, the original brief, CONTENT_SPEC.md, and the student profile. Working-tree scope includes new files and changes since commit 8ba77b230a02f1f4571b90fefd0ed7333fe0e94c. No remaining actionable findings were identified after the fixes below.

## Independent review results

| Review | Result |
|---|---|
| Standards | One P3 finding: word-count guidance was a hard validation failure. Changed it to a reported warning. The reviewer confirmed outliers warn while malformed structure still fails. No remaining findings. |
| Requirements | All nine original Module 1 topics satisfy the lesson contract, with substantive teaching, tested examples, trade-offs, exercises, seven reasoned assessment answers each, and separate worked solutions. No actionable requirements findings. |

The reviewers inspected canonical content and code independently. The requirements reviewer independently ran six HTML checks. Database and browser results below were verified by the primary agent; neither reviewer independently repeated those integrations.

## Issues corrected during implementation and review

- A cache-diagram arrow label extended above the SVG view box. Added top space and regenerated the SVG and standalone page; all nine diagrams now have no text outside their bounds at the checked widths.
- Core-concept word-count guidance incorrectly aborted the lesson validator. It now emits a warning for manual depth review.
- Export metadata still recorded two lessons and two diagrams. Updated it to eleven lessons and eleven diagrams, and added consistency checks to prevent stale counts in future batches.
- The CAP figure’s initial event order was corrected to partition, then acknowledged write, then the alternative B-side read behaviors.
- Idempotency replays retain the original response snapshot after later edits. A dedicated PostgreSQL integration check verifies this behavior.
- Cache loads have a timeout, canceled waiters do not cancel shared work, and shutdown releases pending tasks. These behaviors have executable checks.
- Diagram closing explicitly restores the page’s reading position and focus. A native-coordinate browser check preserved the exact scroll offset and restored the original SVG.

The last four items were implementation corrections and checks, not additional outstanding findings from the independent reviewers.

## Evidence

- 38 Module 1 checks passed with Python 3.12.14 and real PostgreSQL 18.6, with no database skips. They cover concurrent idempotency, original-response replay, payload conflicts, ownership, pagination, lock timeout, atomic rollback, relational constraints, stale-version rejection, cache concurrency/cancellation/expiry/limits, shard fencing, hash-ring boundaries and movement, CAP histories, actual query plans, and capacity arithmetic.
- 10 Node checks passed: six HTML/content/export checks and four reader-state checks. Rendered code preserves source indentation and newlines exactly.
- Two textbook checks and nine prior Module 0 exercise checks passed. Total: 59 automated tests, plus the separate canonical lesson validator.
- A real HTTP smoke test started the loopback API: create 201, same-key replay 200 with the same snapshot, other-owner read 404.
- A live HTTPS probe to python.org returned 200 and read only the configured 4,096-byte sample. Its timing labels retain the limitations explained in lesson 1.01.
- Browser checks used 1280 × 720 and a 390 × 844 viewport. Desktop content is 840px wide with 20px prose. All nine SVGs fit their containers; phone containers measured 331px. Phone enlargement exposes a 900px SVG in a scrollable region. Light/dark appearance, text adjustment, phone section navigation, written/planned search, answer disclosures, and completion across reload were exercised. The temporary completion mark was undone.
- The synthetic index run and exact plans are saved in exercises/module-01/08-database-indexing/observed-plan.json. It is an observation, not a production performance promise.

## Limits and remaining work

The course has eleven written lessons out of 98. Module 1 is nine of nine; 0.03 — Delivery framework and the other 86 planned lessons still need content.

The standalone HTML provides offline lesson and solution reading and embeds the linked implementations. The complete executable lab, including test files and its database fixture, lives in the repository; the HTML is not a lab archive or an in-browser backend runtime.

Direct file-protocol behavior, other browser engines, physical mobile devices, a full accessibility audit, production load/failover, and deployments were not tested. Browser checks used a temporary loopback preview. The distributed examples are local models with their limitations stated in the lessons, not implementations of distributed databases or consensus.

## Read and reproduce

- [Open the reader](System_Design_Fullstack_Course.html)
- [Canonical first lesson](lessons/module-01/01-networking-essentials.md)
- [Lab setup and checks](exercises/module-01/README.md)
- [Course validation](COURSE_VALIDATION.md)
- [Browser evidence](course-ui/module1-review.png)

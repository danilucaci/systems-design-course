# Course validation — current batch

Validated on 2026-10-29. The course is incomplete; two lessons are fully written.

## Content and curriculum

| Measure | Result |
|---|---:|
| Verified syllabus lessons | 98 |
| Modules | 8 |
| Fully written lessons | 2 |
| Planned lessons without placeholder files | 96 |
| Canonical lesson word count, excluding fenced blocks | 7,074 |
| Combined textbook word estimate, including worked solutions | 8,865 |
| Substantial exercises / worked solutions | 2 / 2 |
| Assessment questions / separate answers | 14 / 14 |
| Embedded SVG diagrams | 2 |
| Additional text data-flow diagram | 1 |
| Local Markdown links and fragments checked | 66 |

Word counts are mechanical estimates outside fenced blocks and include headings, link destinations, and export anchor markup where present. They are a depth signal, not proof of teaching quality.

Written lessons:

- [0.01 — Introduction](lessons/module-00/01-from-features-to-systems.md): 3,699 words.
- [0.02 — How to prepare](lessons/module-00/02-how-to-prepare.md): 3,375 words.

Both lessons have the required eleven content sections, a separate assessment-solutions section, seven questions and seven model answers, a substantial exercise, a separate worked solution, and an executable example.

The two preserved originals match on all 98 IDs, titles, objectives, module assignments, and order. Their hashes were verified. No lessons were removed or merged, including the eight practical full-stack labs. All planned lesson paths remain absent; the syllabus records are metadata, not fabricated lesson content.

## Automated checks

- Six HTML/content checks: source paragraph/heading/table/code preservation; offline assets; internal anchors without duplicate IDs; accurate export metadata; planned lesson catalogues without placeholder articles; and study controls without promotional panels.
- Four reader-state checks: sequential stale-tab updates preserve completion; storage failures propagate; provisional IDs and anchors migrate; and invalid stored preferences are normalized.
- Two textbook checks: every written lesson and solution survives assembly, including code blocks; navigation is rebased without rewriting code.
- Four concurrency-probe checks: bounded active work without dropped operations, different overlap under serial/wide limits, zero work, and invalid inputs.
- Five capacity-model checks passed. Together with the other suites, all 21 automated tests passed in this batch.
- The new probe printed completed=10 with maximum-active values of 1, 2, and 10 for the respective limits. These are local scheduling results, not production performance benchmarks.
- Canonical Python listings match their executable files. Both manifest source hashes, planned/written file status, and current local file links were checked.

## Reader and browser checks

The reader now uses 20px default body text, adjustable from 18px to 24px, with 1.8 line height. Code and table text follow the reading-size control. A 21px preference survived reload; code measured 17px at the restored 20px body setting. The main reading area is approximately 840px wide on a desktop viewport.

Desktop checks used 1440 × 960; phone checks used 390 × 844. The phone document had no horizontal overflow. The section index remained available, opened, and navigated to the exercise. The full 98-lesson syllabus is available through Contents; planned entries are clearly marked.

The reported diagram clipping was reproduced: a 900px SVG inside a 700px viewport. After the fix, both diagrams measured 840px within an 840px desktop container and 331px within a 331px phone container. Default diagrams fit without forced horizontal scrolling. Enlarge opens a separate view and returns the same SVG to the document on close without duplicated IDs.

Navigation between lessons 0.01 and 0.02 works. Search found the planned Database indexing lesson and labeled it as not yet written. Existing hidden-solution search behavior and disclosure markup are retained. Completion changed to 1/2, survived reload, and its test record was cleared. No browser warning or error logs were reported during the current checks.

There are no external runtime scripts, styles, fonts, images, API calls, or diagram-rendering services. The source Mermaid blocks are paired with reviewed SVG equivalents; unsupported new diagram sources fail the build rather than disappearing silently.

## Remaining limits

The other 96 lessons still need full teaching content. The next writing batch is 0.03 — Delivery framework. The final textbook/course definition of done is not satisfied.

The browser tool disallows direct file URLs, so browser interactions were checked through a temporary loopback HTTP preview. Direct-file storage behavior and additional browser engines have not been verified. Storage is local to the browser and file/origin.

Reader-state tests cover sequential stale-tab changes. Local storage is not a cross-process transactional database; simultaneous conflicting writes do not have a distributed-consistency guarantee.

Progress JSON export is available; progress import is not implemented. The downloaded file was not inspected end to end. A full accessibility audit, real mobile devices, print behavior, cancellation of the toy Python workload, and real API/database/deployment integrations were not tested.

## Re-run

~~~sh
python3 scripts/build_textbook.py
node scripts/build_course.mjs
node --test scripts/test_course.mjs scripts/test_reader_state.mjs
python3 -m unittest discover -s scripts -v
python3 -m unittest discover -s exercises/module-00/01-system-boundaries -v
python3 -m unittest discover -s exercises/module-00/02-how-to-prepare -v
~~~

See [CHECKPOINT.md](CHECKPOINT.md) for the next small writing batch.

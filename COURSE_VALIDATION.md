# Course validation — Module 1 batch

Validated on 2026-10-30. Module 1 is complete; the full course remains a working edition.

## Content and curriculum

| Measure | Current total | Module 1 batch |
|---|---:|---:|
| Verified syllabus lessons | 98 | 9 original topics preserved |
| Written lessons | 11 | 9 |
| Planned lessons without placeholder files | 87 | 0 |
| Canonical prose word estimate | 30,058 | 23,010 |
| Exercises and separate worked solutions | 11 each | 9 each |
| Assessment questions and reasoned answers | 77 each | 63 each |
| Embedded SVG diagrams | 11 | 9 |

Prose counts exclude fenced blocks and include headings and link text/destinations. They are depth indicators, not quality gates. Every new core-concept lesson is approximately 2,400–2,800 words by this method and has all twelve required second-level sections. The validator checks section order, question/answer numbering, local links and fragments, canonical code listing parity, diagram registrations/XML, absent planned files, and manifest/export count consistency.

The preserved original source hashes still match the manifest. All 98 IDs, titles, objectives, module assignments, and order remain preserved. Module 0 has two of three lessons written; Module 1 has nine of nine. No planned lesson has a fabricated placeholder file.

## Automated and execution checks

All 59 automated tests passed: 38 Module 1 lab checks with actual PostgreSQL 18.6, ten Node HTML/reader-state checks, two textbook checks, and nine existing Module 0 exercise checks. The separate canonical lesson validator passed without word-count warnings. Its warning branch and structural failure behavior were also exercised during independent review.

The API checks use real transactions in uniquely named test schemas and remove only their own schemas. They cover duplicate concurrent creations, original response snapshots, cross-user isolation, bounded pagination, lock timeout, and a failed operation-record insert rolling back its journey. Schema tests cover composite ownership references, constraint rollback, and optimistic versions. No database checks were skipped.

The cache tests use events and a controlled expiry clock, plus an asynchronous loader-timeout check. The shard/hash/CAP examples test the specified local histories and placement properties; they do not claim distributed crash durability. Capacity tests verify unit-aware arithmetic and rejected nonphysical inputs.

The API also ran through its actual command-line entry point with successful synthetic HTTP requests. The networking script completed a verified HTTPS request with a bounded body sample. The index experiment recorded actual before/after JSON plans for 100,000 synthetic rows; tests leave sequential scans enabled and avoid exact timing assertions.

Both exports preserve canonical paragraphs, headings, tables, code, and complete worked solutions. Code indentation/newlines remain exact. Generated IDs are unique, internal links resolve, all 98 syllabus records remain available, and planned items have no content articles. Runtime scripts/styles/assets are embedded without external dependencies or background API calls. External reference links still require internet access.

## Browser checks

Checked in the in-app browser at 1280 × 720 and a 390 × 844 viewport. Body prose measured 20px; controls changed it to 21px and back to 20px. Desktop content measured 840px. Phone SVG containers measured 331px with no forced horizontal overflow. All nine new diagrams had no text outside the SVG bounds after fixing the cache arrow label.

Enlarge displayed an 1114px SVG on desktop and a horizontally scrollable 900px SVG on the phone-sized viewport. Close and Escape restored the same SVG without duplicate IDs. Native-coordinate open/close preserved the exact page scroll position. Phone section-index navigation placed the exercise below the sticky header.

Search returned the written CAP lesson and labeled Kafka as planned. Assessment answers and the separate worked solution opened correctly. A temporary completion mark survived reload and was undone. Light and dark themes were inspected. The default viewport was restored after testing.

## Review and limitations

Independent standards and requirements reviews completed. The standards P3 word-count gate was fixed and confirmed; the requirements review had no actionable findings. See [the review report](MODULE_1_REVIEW.md) for corrections and evidence.

The full course is not complete: 87 lessons remain planned, including 0.03. Direct file-protocol interactions, other browser engines, physical devices, full accessibility/print audits, production load/failover, and deployment were not tested. The HTML supports offline reading; full lab tests remain repository files. Progress import is not implemented, and progress-download contents were not inspected end to end. Local storage does not guarantee transactional concurrent edits across tabs.

## Reproduce

```bash
python3 scripts/validate_lessons.py
python3 scripts/build_module1_diagrams.py
python3 scripts/build_textbook.py
node scripts/build_course.mjs
node --test scripts/test_course.mjs scripts/test_reader_state.mjs
python3 -m unittest discover -s scripts -v
python3 -m unittest discover -s exercises/module-00/01-system-boundaries -v
python3 -m unittest discover -s exercises/module-00/02-how-to-prepare -v
```

For Module 1 dependencies, PostgreSQL, and the 38 lab checks, follow [the lab guide](exercises/module-01/README.md). Browser proof is saved in [module1-review.png](course-ui/module1-review.png). Temporary services started for verification were stopped afterward.

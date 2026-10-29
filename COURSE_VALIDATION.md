# Course validation — batch 1

Validated on 2026-10-29. This is an incomplete course with one fully written provisional introduction.

## Content inventory

| Measure | Result |
|---|---:|
| Lessons expected by the supplied brief | 98 |
| Original curriculum verified | No |
| Lessons mapped to verified original curriculum | 0 |
| Fully written provisional lessons | 1 |
| Canonical lesson files currently written | 1, with provisional identity |
| Lesson word count excluding fenced code and diagrams | 3,646 |
| Substantial practical exercises | 1 |
| Assessment questions / separate model answers | 7 / 7 |
| Mermaid diagram sources | 2 |

The fully written lesson is [From frontend features to production systems](lessons/module-00/01-from-features-to-systems.md). Its file is the canonical prose for this new content, but its position in the original curriculum is unverified. No other lessons have been written, and none are represented by empty lesson files.

Word count uses a mechanical word-token count outside fenced blocks, including headings and Markdown link text/destinations. It is approximate and is not a quality score. Supporting project documents and the separate exercise solution are excluded.

## Checks performed

- All eleven required content sections are present, plus a separate assessment-solutions section, in the specified order.
- Seven numbered assessment questions each have a numbered model answer.
- The lesson includes a worked mechanism discussion, trade-offs, failure diagnosis, capacity arithmetic, and a substantial exercise with a separate worked solution.
- The complete Python listing matches its executable source file exactly after trimming outer whitespace.
- All local Markdown file links and explicit fragment destinations resolve in the current source tree.
- Manifest paths resolve, the provisional lesson ID is unique, and module references match.
- The capacity model ran successfully and printed 4.6296 average requests/second, 37.0370 peak requests/second, and 11.1111 mean in-flight requests, rounded here for display.
- Five Python unit tests passed: reference arithmetic, tenfold latency growth, zero volume, invalid assumptions, and overflow.
- The two Mermaid sources were inspected for matching participants, dependencies, and the lost-response protocol. Reviewed SVG equivalents are embedded in the HTML and were rendered in the browser. The SVG-to-Mermaid source mapping is exact; a changed or unknown source requires a corresponding reviewed SVG before the HTML build succeeds.
- Manual conceptual review checked measurement boundaries, mean-versus-percentile usage, process concurrency, PostgreSQL isolation references, retry uncertainty, and atomic deduplication assumptions.
- Technical references were checked against primary documentation. All illustrative numbers and architectures are explicitly labeled.
- Follow-up export: `System_Design_Fullstack_Masterclass.md` contains the complete first lesson and worked exercise solution. It is generated directly from their source files, with heading levels and link destinations adapted for the combined document.
- Two textbook tests passed: complete source-content and fenced-block preservation, plus navigation rewriting without altering code. All 30 local links across the source tree and export resolved.
- The standalone HTML working edition contains the full first lesson and worked solution, generated from their canonical Markdown. All canonical paragraphs, headings, table cells, and code blocks are checked for preservation.
- Four HTML tests passed: content preservation, no external runtime assets or network calls, internal anchors without duplicate IDs, and accurate working-edition metadata/downloaded Markdown content. The export is reproducible from its sources.
- Desktop rendering was inspected at 1440 × 960. Mobile rendering was inspected at 390 × 844 without document-level horizontal overflow. Wide code, tables, and diagrams have their own scrollable containers.
- Search found text inside a closed worked solution; selecting the result opened the correct disclosure. Mobile search displayed a clear empty state for an unmatched query.
- Completion and theme choices survived reload. Overall and module counters updated. Reset confirmation, cancellation, and confirmed reset were checked, and test completion was cleared afterward.
- The capacity calculator returned 11.11 mean in-flight requests at 300 milliseconds and 111.11 at 3 seconds. An invalid multiplier displayed an error and cleared misleading results.
- Progress export displayed success feedback. The downloaded file was not inspected end to end; the automation download wait was interrupted. Markdown download content matches the working textbook in the embedded data.
- Mobile menu opening, closing via lesson selection, and focus on its close control were checked. Controls have labels, dialogs use native modal behavior, and a skip link is present. This is a manual accessibility smoke check, not a complete audit.
- No browser error or warning logs were reported during the core checks.

Re-run the executable checks from the repository root:

```sh
python3 exercises/module-00/01-system-boundaries/load_model.py
python3 -m unittest discover -s exercises/module-00/01-system-boundaries -v
python3 scripts/build_textbook.py
python3 -m unittest discover -s scripts -v
node scripts/build_course.mjs
node --test scripts/test_course.mjs
```

## Remaining limitations

The two original course files are missing. Their complete 98-lesson sequence, exact module hierarchy, discrepancies, and practical full-stack module cannot yet be inventoried. There are no verified previous/next lesson destinations; the introduction links to the checkpoint instead of an invented next lesson.

A partial combined Markdown textbook has been built. Source-content parity, unchanged fenced code/diagrams, and local links/anchors were checked for this export. Its internal exercise links resolve to the embedded worked solution. The title page identifies the edition as partial.

The standalone HTML working edition is built and checked for the available lesson. Its previous/next controls are disabled at the current boundaries. Navigation across several lessons cannot be exercised until more lessons exist.

The HTML has no external scripts, stylesheets, fonts, images, network fetches, or runtime diagram service. Reference links are optional external navigation. The browser automation tool disallows `file:` URLs, so direct-file storage behavior was not tested. Browser interactions were checked using the permitted local HTTP preview. Storage behavior varies by browser and origin; a visible warning handles unavailable local storage.

The export provides progress JSON download and reset. Progress import is not implemented. The exported file was not inspected on disk. A complete accessibility audit, additional browser engines, print layout, and real mobile devices have not been checked.

The Python program is a deterministic planning model, not a load test. No live API, PostgreSQL server, provider integration, concurrent-save implementation, or deployment has been exercised. These belong in the relevant later lessons. No production performance claims are made.

The [checkpoint](CHECKPOINT.md) identifies the next small batch. The full project does not satisfy the definition of done yet.

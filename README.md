# System design course

A personal study reader for a senior frontend engineer developing senior full-stack skills.

[Open the HTML reader](System_Design_Fullstack_Course.html) · [Read the textbook](System_Design_Fullstack_Masterclass.md) · [Full syllabus](COURSE_TOC.md)

## Start studying

1. [0.01 — Introduction](lessons/module-00/01-from-features-to-systems.md)
2. [0.02 — How to prepare](lessons/module-00/02-how-to-prepare.md)

Module 1 is also complete: [1.01 — Networking essentials](lessons/module-01/01-networking-essentials.md) through [1.09 — Numbers to know](lessons/module-01/09-numbers-to-know.md). Its nine lessons cover networking, API design, data modeling, caching, sharding, consistent hashing, CAP, indexing, and capacity estimates. Each includes an exercise, worked solution, seven assessment answers, and a runnable example. See the [Module 1 lab guide](exercises/module-01/README.md) for its Python 3.12 environment and disposable PostgreSQL 18 database.

There are 11 fully written lessons out of 98 across eight modules. The remaining 87, including 0.03 — Delivery framework, are planned with no placeholder lesson pages.

The HTML file contains its own text, diagrams, code, styles, and scripts. It can be opened in a browser without a server. External reference links need internet access. Browser-tool checks use a local HTTP preview because the automation tool disallows direct file URLs.

## Reading controls

Body text starts at 20px with generous spacing. A− and A+ adjust it from 18px to 24px and also resize code and tables. Light and dark modes are available. Contents provides the full syllabus; On this page provides section links on every screen size. Solutions remain closed until you open them.

The reader remembers your lesson and section, completion, text size, and theme in browser storage. Existing provisional introduction IDs migrate to lesson 0.01. Sequential updates from another tab merge with the latest saved state. A failed write is reported beside the completion control; in-memory progress can still be exported. Export downloads JSON; progress import is not implemented.

## Background and source material

- [Student background](STUDENT_PROFILE.md)
- [Verified source inventory](SOURCE_INVENTORY.md)
- [Content specification](CONTENT_SPEC.md)
- [Machine-readable manifest](course-manifest.json)
- [Validation report](COURSE_VALIDATION.md)
- [Next writing checkpoint](CHECKPOINT.md)

## Rebuild and check

Use Python 3.10+ syntax support and Node.js 20 or later. No package installation is needed for the HTML build; its MIT-licensed Markdown parser is included.

~~~sh
python3 scripts/build_textbook.py
node scripts/build_course.mjs
python3 scripts/validate_lessons.py
node --test scripts/test_course.mjs scripts/test_reader_state.mjs
python3 -m unittest discover -s scripts -v
python3 -m unittest discover -s exercises/module-00/01-system-boundaries -v
python3 -m unittest discover -s exercises/module-00/02-how-to-prepare -v
~~~

The Module 1 lab checks require the separate environment and database described in their guide. To regenerate its authored diagrams, run `python3 scripts/build_module1_diagrams.py` before rebuilding both exports.

Add complete content in the agreed batch size. Rebuild both exports from the canonical files. The build rejects Mermaid diagrams without corresponding reviewed offline SVG assets. See [the Module 1 review](MODULE_1_REVIEW.md) for findings and verification limits.

# Senior Full-Stack System Design Masterclass

This course is being written in small, reviewable batches. The target is the 98-lesson curriculum described in the supplied brief. The original Markdown and HTML courses have not been supplied, so their lesson titles, numbering, and module boundaries are not yet verified.

## First reading

[Open the interactive HTML course](System_Design_Fullstack_Course.html). Open the file in a browser to read the full first lesson, explore its diagrams and capacity calculator, search the content, and track completion. It works without a server or internet connection; external reference links need internet access.

[Read the Markdown textbook — working edition](System_Design_Fullstack_Masterclass.md). It contains the first complete lesson and its worked exercise solution in one file.

[From frontend features to production systems](lessons/module-00/01-from-features-to-systems.md) is a complete introductory lesson with an exercise, seven assessment questions, separate answers, and a tested Python workload model. Its placement in Module 0 is provisional until the original curriculum is available.

## Project files

- [Source inventory](SOURCE_INVENTORY.md): available inputs, missing inputs, and reference hierarchy.
- [Lesson specification](CONTENT_SPEC.md): the content and quality requirements for each lesson.
- [Course manifest](course-manifest.json): machine-readable content status and validation.
- [Validation report](COURSE_VALIDATION.md): measured progress and remaining limitations.
- [Continuation checkpoint](CHECKPOINT.md): the exact next batch.
- [First exercise solution](exercises/module-00/01-system-boundaries/SOLUTION.md): a worked requirements and capacity exercise.

Run the introductory example from this directory with Python 3.10 or later:

```sh
python3 exercises/module-00/01-system-boundaries/load_model.py
python3 -m unittest discover -s exercises/module-00/01-system-boundaries -v
```

## Batch size

Write one substantial lesson per batch initially. Finish its content, exercise, factual checks, and manifest update before starting the next. Larger batches can follow once the curriculum and lesson format are settled.

Rebuild the working exports from the canonical sources:

```sh
python3 scripts/build_textbook.py
node scripts/build_course.mjs
```

The HTML build uses the included MIT-licensed Marked parser; no package installation is required. It embeds its styles, scripts, diagrams, lesson content, worked solution, and referenced project resources into one file. The two SVG diagrams are reviewed equivalents of the current Mermaid sources. The build rejects Mermaid blocks without a matching SVG in `course-ui/diagrams/manifest.json`.

Both exports contain the content written so far. Completion is measured against the available lessons; the page separately displays the 98-lesson target. Browser storage is local to the browser and file/origin. The progress menu can export a JSON record or reset completion. Importing exported progress is not implemented.

Run the HTML checks with `node --test scripts/test_course.mjs`. The [validation report](COURSE_VALIDATION.md) records browser checks and their limits.

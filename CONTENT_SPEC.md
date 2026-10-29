# Canonical lesson specification

## Content ownership and identity

One Markdown file is the canonical prose for each written lesson. The manifest records its stable ID, original display number and title, module, path, status, prerequisites, exercise paths, and validation results. The 98-lesson curriculum has been verified against both preserved originals in sources/. Planned records preserve its structure without creating placeholder lesson files.

Generate the eventual textbook and HTML lesson bodies from those same files. Include complete exercises and assessment answers. Keep executable examples beside their exercise solutions; verify that any complete code listing in a lesson matches its executable file.

## Required lesson sections

Use these second-level headings, in this order, with a separate answer section after the assessment:

1. `A. Learning objectives and prerequisites`
2. `B. Mental model and intuition`
3. `C. Deep technical explanation`
4. `D. Architecture and data flow`
5. `E. Real-world examples`
6. `F. Executable example`
7. `G. Architectural decisions and trade-offs`
8. `H. Common failures and debugging`
9. `I. Practical exercise`
10. `J. Interview and senior-engineering assessment`
11. `Assessment solutions`
12. `K. Key takeaways and navigation`

Each lesson needs mechanisms, assumptions, realistic failures, decision criteria, one substantial exercise, and 5–10 assessment questions with reasoned answers. Code is required where it helps understanding; it must include execution instructions and appropriate checks. Introductory lessons can use a small local model rather than an artificial production service.

## Teaching and accuracy

Teach an experienced React/Next.js/TypeScript engineer. Explain unfamiliar backend mechanisms from first principles without introductory programming material. Use Python/FastAPI, PostgreSQL/PostGIS, and TypeScript when relevant. Explain when a simpler architecture satisfies the requirements.

Mark all hypothetical workloads, targets, incidents, and architectures as illustrative. Show units and assumptions in calculations. Cite primary technical sources near supported claims. Distinguish documented company facts from teaching examples. Check version-sensitive behavior against official documentation.

Follow the brief's category-specific depth targets. Treat word counts as a warning signal, not proof of quality. Every lesson needs manual conceptual review in addition to mechanical checks.

Complete system-design problems must follow all seventeen steps in the brief, from requirements through evolution at greater scale. An introductory boundary or estimation exercise is not a complete system-design problem.

## Validation and publication

After each batch, check section presence, substantive content, question/answer coverage, local file links and explicit anchors, code execution, and calculations. Update the manifest, validation report, and checkpoint. Record what was actually tested and any manual or environmental limitations.

Mermaid source remains in Markdown. The HTML build uses reviewed, embedded SVG equivalents and rejects diagram sources without matching assets. The output works offline. Source inspection alone does not establish rendering correctness; browser checks must cover the changed diagrams and interactions.

The reader serves one learner studying after work. Use 20px default body text with an 18–24px adjustment range, comfortable line length, generous line spacing, larger code, and quiet light/dark colors. Keep the section index and downloads usable on phones. Exclude promotional banners, logos, decorative cards, and sales-oriented copy. Preserve existing progress IDs through aliases when a lesson is mapped or renamed.

Do not create empty lesson files to inflate progress. Missing source curriculum, unrendered diagrams, untested SQL, and incomplete exports remain explicit limitations.

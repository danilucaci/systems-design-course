import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';
import { Marked, Renderer } from './vendor/marked.mjs';

export const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const read = file => fs.readFileSync(path.join(ROOT, file), 'utf8');
export const escape = text => String(text).replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[char]);
const slug = title => title.toLowerCase().replace(/[^\p{L}\p{N}_ -]/gu, '').replace(/ /g, '-');

function highlight(code, language) {
  if (language !== 'python') return escape(code);
  const pattern = /#[^\n]*|"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|\b(?:from|import|def|for|in|if|not|or|and|raise|return|as|with|class|else|True|False|None)\b|\b\d+(?:_\d+)*(?:\.\d+)?\b/g;
  let result = '', offset = 0;
  for (const match of code.matchAll(pattern)) {
    const kind = match[0].startsWith('#') ? 'comment' : /^["']/.test(match[0]) ? 'string' : /^\d/.test(match[0]) ? 'number' : 'keyword';
    result += escape(code.slice(offset, match.index)) + `<span class="token-${kind}">${escape(match[0])}</span>`;
    offset = match.index + match[0].length;
  }
  return result + escape(code.slice(offset));
}

export function buildCourse() {
  const manifest = JSON.parse(read('course-manifest.json'));
  const modules = [...manifest.modules].sort((a, b) => a.order - b.order);
  const catalog = modules.flatMap(module => manifest.lessons.filter(lesson => lesson.module_id === module.id).sort((a, b) => a.order - b.order));
  const lessons = modules.flatMap(module => manifest.lessons.filter(lesson => lesson.module_id === module.id && ['written_pending_curriculum_mapping', 'complete'].includes(lesson.status)).sort((a, b) => a.order - b.order));
  if (!lessons.length) throw new Error('No written lessons are available');
  const documents = new Map();
  for (const lesson of lessons) {
    documents.set(path.resolve(ROOT, lesson.path), lesson.id);
    documents.set(path.resolve(ROOT, lesson.exercise_solution_path), lesson.id + '--exercise-solution');
  }
  const diagrams = JSON.parse(read('course-ui/diagrams/manifest.json'));
  const resources = {}, lessonData = [];
  function hrefFor(href, source) {
    if (/^(https?:|mailto:)/i.test(href)) return href;
    if (/^[a-z]+:/i.test(href)) throw new Error(`Unsupported link scheme: ${href}`);
    const [filename, fragment] = href.split('#');
    const destination = filename ? path.resolve(path.dirname(source), decodeURIComponent(filename)) : source;
    if (documents.has(destination)) return '#' + documents.get(destination) + (fragment ? '--' + fragment : '');
    if (destination === path.join(ROOT, 'README.md')) return '#' + lessons[0].id;
    if (destination === path.join(ROOT, 'COURSE_TOC.md')) {
      if (!fragment) return '#course-contents';
      const item = catalog.find(lesson => lesson.id === fragment);
      if (item) return '#' + (item.status === 'complete' ? item.id : 'planned-' + item.id);
      return '#nav-' + fragment;
    }
    if (!destination.startsWith(ROOT + path.sep) || !fs.statSync(destination).isFile()) throw new Error(`Missing course resource: ${href}`);
    const id = 'resource-' + createHash('sha256').update(path.relative(ROOT, destination)).digest('hex').slice(0, 10);
    resources[id] = { title: path.basename(destination), content: fs.readFileSync(destination, 'utf8') };
    return '#' + id;
  }
  function parserFor(source, prefix, headingOffset = 0) {
    const renderer = new Renderer();
    renderer.heading = function({ tokens, depth, text }) {
      const level = Math.min(6, depth + headingOffset);
      const id = depth === 1 ? prefix + '-title' : prefix + '--' + slug(text);
      return `<h${level} id="${escape(id)}">${this.parser.parseInline(tokens)}</h${level}>\n`;
    };
    renderer.link = function({ href, title, tokens }) {
      const external = /^(https?:|mailto:)/i.test(href);
      return `<a href="${escape(hrefFor(href, source))}"${title ? ` title="${escape(title)}"` : ''}${external ? ' target="_blank" rel="noopener noreferrer"' : ''}>${this.parser.parseInline(tokens)}</a>`;
    };
    renderer.code = function({ text, lang }) {
      const language = (lang || 'text').split(/\s/)[0];
      if (language === 'mermaid') {
        const diagram = diagrams.find(item => item.source.trim() === text.trim());
        if (!diagram) throw new Error('A Mermaid diagram needs a corresponding reviewed offline SVG');
        return `<figure class="diagram"><figcaption><strong>${escape(diagram.title)}</strong><button type="button" data-enlarge-diagram aria-label="Enlarge ${escape(diagram.title)}">Enlarge</button></figcaption><div class="diagram-viewport" tabindex="0" role="region" aria-label="Architecture diagram">${read(diagram.path)}</div><details><summary>View Mermaid source</summary><pre>${escape(text)}</pre></details></figure>`;
      }
      return `<figure class="codeblock"><figcaption><span>${escape(language)}</span><button type="button" class="copy-code" aria-label="Copy ${escape(language)} code">Copy</button></figcaption><pre tabindex="0"><code class="language-${escape(language)}">${highlight(text, language)}</code></pre></figure>`;
    };
    const defaultTable = renderer.table;
    renderer.table = function(token) {
      return '<div class="table-scroll" tabindex="0" role="region" aria-label="Scrollable comparison table">' + defaultTable.call(this, token) + '</div>';
    };
    return new Marked({ renderer, gfm: true });
  }
  const navigation = modules.map(module => {
    const children = catalog.filter(lesson => lesson.module_id === module.id);
    const written = children.filter(lesson => lesson.status === 'complete');
    return `<details class="module" id="nav-${escape(module.id)}"${written.length ? ' open' : ''}><summary>${module.order}. ${escape(module.title)}<span class="module-caption">${written.length} of ${children.length} written${written.length ? ` · <span data-module-count="${escape(module.id)}">0 / ${written.length}</span> completed` : ''}</span></summary><ol>${children.map(lesson => lesson.status === 'complete' ? `<li><a class="lesson-nav" href="#${escape(lesson.id)}" data-lesson-link="${escape(lesson.id)}"><span class="lesson-number">${escape(lesson.display_id)}</span><span>${escape(lesson.title)}</span><span class="completion-icon" data-completion-icon="${escape(lesson.id)}" aria-label="Not completed">○</span></a></li>` : `<li><span class="planned-lesson" id="planned-${escape(lesson.id)}" tabindex="-1"><span class="lesson-number">${escape(lesson.display_id)}</span><span>${escape(lesson.title)}<small class="planned-label">Planned</small></span></span></li>`).join('')}</ol></details>`;
  }).join('');
  const articles = lessons.map((lesson, index) => {
    const module = modules.find(item => item.id === lesson.module_id);
    const source = path.resolve(ROOT, lesson.path), raw = read(lesson.path);
    const parser = parserFor(source, lesson.id);
    const tokens = parser.lexer(raw);
    const titleToken = tokens.find(token => token.type === 'heading' && token.depth === 1);
    const sections = [], intro = [];
    let section;
    for (const token of tokens) {
      if (token === titleToken) continue;
      if (token.type === 'heading' && token.depth === 2) {
        section = { title: token.text, id: lesson.id + '--' + slug(token.text), tokens: [token] }; sections.push(section);
      } else if (section) section.tokens.push(token);
      else intro.push(token);
    }
    const compiledSections = sections.map(item => {
      const body = parser.parse(item.tokens.map(token => token.raw).join(''));
      const attributes = `data-section data-title="${escape(item.title)}" data-anchor="${escape(item.id)}"`;
      if (item.title === 'Assessment solutions') {
        const heading = body.match(/^<h2[^>]*>.*?<\/h2>/s)?.[0];
        return `<details class="solutions" ${attributes}><summary>${heading}<span>Reveal model answers</span></summary><div class="solution-body">${body.replace(heading, '')}</div></details>`;
      }
      return `<section class="lesson-section${item.title.startsWith('I.') ? ' exercise-section' : ''}" ${attributes}>${body}${item.title.startsWith('C.') && lesson.interactive_example === 'load_model' ? loadLab(lesson.id) : ''}</section>`;
    }).join('\n');
    const solutionPrefix = lesson.id + '--exercise-solution';
    const solutionParser = parserFor(path.resolve(ROOT, lesson.exercise_solution_path), solutionPrefix, 1);
    const solution = solutionParser.parse(read(lesson.exercise_solution_path));
    const solutionHeading = solution.match(/^<h2[^>]*>.*?<\/h2>/s)?.[0];
    const solutionBody = solution.replace(solutionHeading, '');
    const solutionId = solutionPrefix + '-title';
    sections.push({ id: solutionId, title: 'Worked exercise solution' });
    lessonData.push({ id: lesson.id, title: lesson.title, moduleId: lesson.module_id, sections: sections.map(({ id, title }) => ({ id, title })) });
    // The resource identity also names this disclosure, so source links open it directly.
    const solutionDetails = `<details class="worked-solution" id="${escape(solutionPrefix)}" data-section data-title="Worked exercise solution" data-anchor="${escape(solutionId)}"><summary>${solutionHeading}<span>Reveal worked solution</span></summary><div class="solution-body">${solutionBody}</div></details>`;
    const exercise = sections.find(item => item.title.startsWith('I.')).id;
    const questionCount = lesson.validation.assessment_question_count;
    const minutes = Math.ceil(lesson.word_count / 210);
    const next = index < lessons.length - 1 ? lessons[index + 1] : catalog.find(item => item.id === lesson.next_lesson_id);
    const previous = index ? lessons[index - 1] : null;
    return `<article data-lesson id="${escape(lesson.id)}"><header class="lesson-header"><div class="lesson-kicker">${parser.parse(intro.map(token => token.raw).join(''))}</div>${parser.parse(titleToken.raw)}<div class="lesson-meta"><span>${minutes} min read</span><span>${questionCount} questions</span><a href="#${escape(exercise)}">Exercise</a></div></header><details class="section-index"><summary>On this page</summary><nav data-outline aria-label="Lesson sections">${sections.map(section => `<a href="#${escape(section.id)}">${escape(section.title.replace(/^[A-K]\. /, ''))}</a>`).join('')}</nav></details>${compiledSections}${solutionDetails}<div class="lesson-finish"><p>Complete the exercise and assessment, then record your progress.</p><button class="primary-button completion-button" type="button" aria-pressed="false" data-complete="${escape(lesson.id)}">Mark complete</button><span class="save-feedback" data-save-feedback role="status"></span></div><nav class="lesson-pagination" aria-label="Previous and next lesson">${previous ? `<a href="#${escape(previous.id)}">← ${escape(previous.display_id)} ${escape(previous.title)}</a>` : '<span>First lesson</span>'}${next ? `<a href="#${next.status === 'complete' ? '' : 'planned-'}${escape(next.id)}">${escape(next.display_id)} ${escape(next.title)}${next.status === 'complete' ? '' : ' (planned)'} →</a>` : '<span>Last lesson</span>'}</nav></article>`;
  }).join('\n');
  const data = { version: 1, title: manifest.title, expectedLessonCount: manifest.expected_lesson_count, modules: modules.map(module => ({ id: module.id, title: module.title })), catalog: catalog.map(lesson => ({ id: lesson.id, displayId: lesson.display_id, title: lesson.title, objective: lesson.objective, moduleId: lesson.module_id, status: lesson.status })), aliases: Object.fromEntries(catalog.flatMap(lesson => (lesson.aliases || []).map(alias => [alias, lesson.id]))), lessons: lessonData, resources, markdown: read('System_Design_Fullstack_Masterclass.md') };
  const replacements = {
    STYLES: read('course-ui/course.css'), SCRIPT: read('course-ui/course.js').replace('/* READER_STATE */', read('course-ui/reader-state.mjs').replace(/^export /gm, '')),
    NAVIGATION: navigation, LESSONS: articles, AVAILABLE: String(lessons.length), EXPECTED: String(manifest.expected_lesson_count),
    DATA: JSON.stringify(data).replace(/</g, '\\u003c'),
  };
  return read('course-ui/template.html').replace(/\{\{([A-Z]+)\}\}/g, (_, name) => replacements[name]);
}

function loadLab(id) {
  return `<div class="load-lab"><span class="eyebrow">TRY THE MENTAL MODEL</span><h3>What happens when a request slows down?</h3><p>Change the assumptions. See how average in-flight requests change at a stable peak rate.</p><div class="lab-inputs"><label>Requests per day<input type="number" min="0" step="any" value="400000" aria-describedby="${escape(id)}-lab-note"></label><label>Peak multiplier<input type="number" min="1" step="any" value="8"></label><label>Mean latency (ms)<input type="number" min="0.001" step="any" value="300"></label></div><p class="lab-error" role="alert" hidden>Use finite numbers: daily requests ≥ 0, peak multiplier ≥ 1, and mean latency > 0.</p><div class="lab-output" aria-live="polite" aria-atomic="true"><div><strong data-lab-value>4.63</strong><span>Average rate</span><small>requests / second</small></div><div><strong data-lab-value>37.04</strong><span>Peak rate</span><small>requests / second</small></div><div><strong data-lab-value>11.11</strong><span>Mean in flight</span><small>requests</small></div></div><div class="lab-controls"><span>Try a dependency:</span><button type="button" data-latency="300">Healthy · 300 ms</button><button type="button" data-latency="3000">Slow · 3,000 ms</button></div><p class="lab-caveat" id="${escape(id)}-lab-note">L = λ × W uses mean values and matching boundaries in a stable regime. This is an illustrative estimate, not a benchmark or a database pool size.</p></div>`;
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const output = path.join(ROOT, 'System_Design_Fullstack_Course.html');
  fs.writeFileSync(output, buildCourse());
  console.log(`Built ${output}`);
}

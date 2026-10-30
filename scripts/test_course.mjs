import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import test from 'node:test';
import { Marked } from './vendor/marked.mjs';
import { buildCourse, ROOT } from './build_course.mjs';

const html = buildCourse();
const markup = html.replace(/<(script|style)\b[^>]*>[\s\S]*?<\/\1>/g, '');
const data = JSON.parse(html.match(/<script type="application\/json" id="course-data">([\s\S]*?)<\/script>/)[1]);
const manifest = JSON.parse(fs.readFileSync(path.join(ROOT, 'course-manifest.json'), 'utf8'));
const marked = new Marked();
const plain = input => input.replace(/<[^>]*>/g, '').replace(/&(?:amp|lt|gt|quot|#39);/g, entity => ({ '&amp;': '&', '&lt;': '<', '&gt;': '>', '&quot;': '"', '&#39;': "'" })[entity]).replace(/\s+/g, ' ').trim();
const codeText = input => input.replace(/<[^>]*>/g, '').replace(/&(?:amp|lt|gt|quot|#39);/g, entity => ({ '&amp;': '&', '&lt;': '<', '&gt;': '>', '&quot;': '"', '&#39;': "'" })[entity]);

test('every canonical paragraph, heading, table cell, and code block is included', () => {
  const rendered = plain(markup);
  const listings = [...markup.matchAll(/<pre[^>]*><code[^>]*>([\s\S]*?)<\/code><\/pre>/g)].map(match => codeText(match[1]));
  let checked = 0;
  for (const lesson of manifest.lessons) {
    if (!data.lessons.some(item => item.id === lesson.id)) continue;
    for (const filename of [lesson.path, lesson.exercise_solution_path]) {
      const tokens = marked.lexer(fs.readFileSync(path.join(ROOT, filename), 'utf8'));
      marked.walkTokens(tokens, token => {
        if (['paragraph', 'heading', 'code', 'text'].includes(token.type)) {
          const expected = token.type === 'code' ? token.text.replace(/\s+/g, ' ').trim() : plain(marked.parse(token.raw || ''));
          if (expected) { assert.ok(rendered.includes(expected), `Missing content: ${expected.slice(0, 100)}`); checked++; }
          if (token.type === 'code' && token.lang !== 'mermaid') assert.ok(listings.includes(token.text), `Code whitespace changed: ${token.text.slice(0, 60)}`);
        }
        if (token.type === 'table') {
          for (const cell of [...token.header, ...token.rows.flat()]) assert.ok(rendered.includes(plain(marked.parse(cell.text))));
        }
      });
    }
  }
  assert.ok(checked > 100);
});

test('standalone page has no external scripts, styles, images, imports, or fetches', () => {
  const runtime = [...html.matchAll(/<script(?![^>]*type="application\/json")[^>]*>([\s\S]*?)<\/script>/g)].map(match => match[1]).join('\n');
  const styles = [...html.matchAll(/<style[^>]*>([\s\S]*?)<\/style>/g)].map(match => match[1]).join('\n');
  assert.doesNotMatch(markup, /<(?:script|img|link|iframe|source)\b[^>]*(?:src|href)\s*=/i);
  assert.doesNotMatch(html, /<script\b[^>]*\bsrc\s*=/i);
  assert.doesNotMatch(runtime, /\bfetch\(|XMLHttpRequest|WebSocket\(/);
  assert.doesNotMatch(styles, /@import|url\(https?:/);
  const expectedDiagrams = manifest.lessons.filter(lesson => lesson.status === 'complete').reduce((total, lesson) => total + lesson.validation.mermaid_diagram_count, 0);
  assert.equal((markup.match(/<svg[^>]*role="img"/g) || []).length, expectedDiagrams);
  assert.ok(data.markdown.includes('Assessment solutions'));
});

test('all generated internal links and outline anchors resolve without duplicate IDs', () => {
  const ids = [...markup.matchAll(/\bid="([^"]+)"/g)].map(match => match[1]);
  assert.equal(new Set(ids).size, ids.length, 'Duplicate element IDs');
  const allowed = new Set([...ids, ...Object.keys(data.resources), 'course-contents']);
  for (const match of markup.matchAll(/href="#([^"]+)"/g)) assert.ok(allowed.has(match[1]), `Missing anchor: ${match[1]}`);
  for (const lesson of data.lessons) {
    for (const section of lesson.sections) assert.ok(allowed.has(section.id), `Missing outline: ${section.id}`);
  }
});

test('working edition, disclosure controls, and exported sources remain accurate', () => {
  assert.equal(data.lessons.length, manifest.lessons.filter(lesson => lesson.status === 'complete').length);
  assert.equal(data.catalog.length, manifest.expected_lesson_count);
  assert.equal(data.expectedLessonCount, 98);
  assert.ok(markup.includes(`${data.lessons.length} written`));
  assert.match(markup, /class="solutions"/);
  assert.match(markup, /class="worked-solution"/);
  assert.equal(data.markdown, fs.readFileSync(path.join(ROOT, 'System_Design_Fullstack_Masterclass.md'), 'utf8'));
  assert.equal(html, fs.readFileSync(path.join(ROOT, 'System_Design_Fullstack_Course.html'), 'utf8'));
});

test('every planned lesson is listed without a placeholder article', () => {
  const planned = data.catalog.filter(lesson => lesson.status !== 'complete');
  for (const lesson of planned) {
    assert.ok(markup.includes(`id="planned-${lesson.id}"`));
    assert.ok(!markup.includes(`data-lesson id="${lesson.id}"`));
  }
  assert.equal((markup.match(/class="module"/g) || []).length, manifest.modules.length);
});

test('reading controls and the section index are available in the simple layout', () => {
  assert.match(markup, /aria-label="Increase text size"/);
  assert.match(markup, /aria-label="Decrease text size"/);
  assert.equal((markup.match(/class="section-index"/g) || []).length, data.lessons.length);
  assert.match(markup, /data-action="download-markdown"/);
  assert.doesNotMatch(markup, /hero-aside|hero-actions|brand-mark|Make the knowledge yours/);
});

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

test('every canonical paragraph, heading, table cell, and code block is included', () => {
  const rendered = plain(markup);
  let checked = 0;
  for (const lesson of manifest.lessons) {
    if (!data.lessons.some(item => item.id === lesson.id)) continue;
    for (const filename of [lesson.path, lesson.exercise_solution_path]) {
      const tokens = marked.lexer(fs.readFileSync(path.join(ROOT, filename), 'utf8'));
      marked.walkTokens(tokens, token => {
        if (['paragraph', 'heading', 'code', 'text'].includes(token.type)) {
          const expected = token.type === 'code' ? token.text.replace(/\s+/g, ' ').trim() : plain(marked.parse(token.raw || ''));
          if (expected) { assert.ok(rendered.includes(expected), `Missing content: ${expected.slice(0, 100)}`); checked++; }
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
  assert.doesNotMatch(html, /<(?:script|img|link|iframe|source)\b[^>]*(?:src|href)\s*=/i);
  assert.doesNotMatch(html, /@import|url\(https?:|\bfetch\(|XMLHttpRequest|WebSocket\(/);
  assert.equal((markup.match(/<svg[^>]*role="img"/g) || []).length, 2);
  assert.ok(data.markdown.includes('Assessment solutions'));
});

test('all generated internal links and outline anchors resolve without duplicate IDs', () => {
  const ids = [...markup.matchAll(/\bid="([^"]+)"/g)].map(match => match[1]);
  assert.equal(new Set(ids).size, ids.length, 'Duplicate element IDs');
  const allowed = new Set([...ids, ...Object.keys(data.resources)]);
  for (const match of markup.matchAll(/href="#([^"]+)"/g)) assert.ok(allowed.has(match[1]), `Missing anchor: ${match[1]}`);
  for (const lesson of data.lessons) {
    for (const section of lesson.sections) assert.ok(allowed.has(section.id), `Missing outline: ${section.id}`);
  }
});

test('working edition, disclosure controls, and exported sources remain accurate', () => {
  assert.equal(data.lessons.length, 1);
  assert.equal(data.expectedLessonCount, 98);
  assert.match(markup, /1 complete lesson available/);
  assert.match(markup, /class="solutions"/);
  assert.match(markup, /class="worked-solution"/);
  assert.equal(data.markdown, fs.readFileSync(path.join(ROOT, 'System_Design_Fullstack_Masterclass.md'), 'utf8'));
  assert.equal(html, fs.readFileSync(path.join(ROOT, 'System_Design_Fullstack_Course.html'), 'utf8'));
});

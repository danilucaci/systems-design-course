import assert from 'node:assert/strict';
import test from 'node:test';
import { normalizeReaderState, readReaderState, writeReaderState } from '../course-ui/reader-state.mjs';

const ids = ['lesson-0-01', 'lesson-0-02'];
const aliases = { 'provisional-m0-01': 'lesson-0-01' };
const key = 'reader';
const memoryStorage = () => {
  let value = null;
  return { getItem: () => value, setItem: (_key, next) => { value = next; } };
};

test('a stale tab changing the theme preserves another tab’s completion', () => {
  const storage = memoryStorage();
  const stale = readReaderState(storage, key, ids, aliases);
  writeReaderState(storage, key, ids, aliases, state => ({ ...state, completed: ['lesson-0-01'] }));
  writeReaderState(storage, key, ids, aliases, state => ({ ...state, theme: stale.theme === 'light' ? 'dark' : 'light' }));
  assert.deepEqual(readReaderState(storage, key, ids, aliases).completed, ['lesson-0-01']);
});

test('storage failures propagate so the UI cannot claim persistence', () => {
  const storage = { getItem: () => null, setItem: () => { throw new Error('storage blocked'); } };
  assert.throws(() => writeReaderState(storage, key, ids, aliases, state => ({ ...state, completed: ids })), /storage blocked/);
});

test('provisional completion and section anchors migrate without losing progress', () => {
  const result = normalizeReaderState({ completed: ['provisional-m0-01'], lastLesson: 'provisional-m0-01', lastAnchor: 'provisional-m0-01--i-practical-exercise' }, ids, aliases);
  assert.deepEqual(result.completed, ['lesson-0-01']);
  assert.equal(result.lastLesson, 'lesson-0-01');
  assert.equal(result.lastAnchor, 'lesson-0-01--i-practical-exercise');
});

test('invalid stored values do not leak into reading controls', () => {
  const result = normalizeReaderState({ completed: [ids[0], ids[0], 'unknown'], textSize: 100, theme: 'anything' }, ids, aliases);
  assert.equal(result.textSize, 24);
  assert.equal(result.theme, 'light');
  assert.deepEqual(result.completed, [ids[0]]);
  assert.equal(normalizeReaderState(null, ids).textSize, 20);
});

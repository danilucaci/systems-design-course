export function normalizeReaderState(value, ids, aliases = {}) {
  const canonical = id => aliases[id] || id;
  const valid = new Set(ids);
  const saved = value && typeof value === 'object' ? value : {};
  const completed = Array.isArray(saved.completed) ? saved.completed.map(canonical).filter(id => valid.has(id)) : [];
  const lastLesson = valid.has(canonical(saved.lastLesson)) ? canonical(saved.lastLesson) : ids[0];
  let lastAnchor = typeof saved.lastAnchor === 'string' ? saved.lastAnchor : lastLesson;
  for (const [oldId, newId] of Object.entries(aliases)) {
    if (lastAnchor === oldId || lastAnchor.startsWith(oldId + '--')) lastAnchor = newId + lastAnchor.slice(oldId.length);
  }
  return { version: 1, completed: [...new Set(completed)], theme: saved.theme === 'dark' ? 'dark' : 'light', textSize: Number.isFinite(saved.textSize) ? Math.max(18, Math.min(24, saved.textSize)) : 20, lastLesson, lastAnchor };
}

export function readReaderState(storage, key, ids, aliases) {
  const raw = storage.getItem(key);
  let value;
  try { value = raw ? JSON.parse(raw) : {}; }
  catch { value = {}; }
  return normalizeReaderState(value, ids, aliases);
}

export function writeReaderState(storage, key, ids, aliases, change) {
  const latest = readReaderState(storage, key, ids, aliases);
  const next = normalizeReaderState(change(latest), ids, aliases);
  storage.setItem(key, JSON.stringify(next));
  return next;
}

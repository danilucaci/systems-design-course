(() => {
  'use strict';
  /* READER_STATE */
  const data = JSON.parse(document.getElementById('course-data').textContent);
  const $ = (selector, scope = document) => scope.querySelector(selector);
  const $$ = (selector, scope = document) => [...scope.querySelectorAll(selector)];
  const key = 'system-design-masterclass-v1';
  const ids = data.catalog.map(lesson => lesson.id);
  const writtenIds = new Set(data.lessons.map(lesson => lesson.id));
  const warning = $('#storage-warning');
  let pendingChanges = [];
  let state;
  try { state = readReaderState(localStorage, key, ids, data.aliases); }
  catch { state = normalizeReaderState({}, ids, data.aliases); warning.hidden = false; }

  function save(change) {
    pendingChanges.push(change);
    try {
      state = writeReaderState(localStorage, key, ids, data.aliases, latest => pendingChanges.reduce((value, edit) => edit(value), latest));
      pendingChanges = [];
      warning.hidden = true;
      return true;
    } catch {
      state = normalizeReaderState(change(state), ids, data.aliases);
      warning.hidden = false;
      return false;
    }
  }
  function updateProgress() {
    const count = state.completed.filter(id => writtenIds.has(id)).length;
    $$('[data-progress-count]').forEach(node => { node.textContent = `${count} / ${data.lessons.length}`; });
    $$('[data-progress-bar]').forEach(node => { node.max = data.lessons.length; node.value = count; });
    $$('[data-progress-description]').forEach(node => { node.textContent = `${count} of ${data.lessons.length} written lessons completed`; });
    data.modules.forEach(module => {
      const lessons = data.lessons.filter(lesson => lesson.moduleId === module.id);
      $$(`[data-module-count="${module.id}"]`).forEach(node => { node.textContent = `${lessons.filter(lesson => state.completed.includes(lesson.id)).length} / ${lessons.length}`; });
    });
    data.lessons.forEach(lesson => {
      const done = state.completed.includes(lesson.id);
      $$(`[data-complete="${lesson.id}"]`).forEach(button => {
        button.setAttribute('aria-pressed', String(done));
        button.textContent = done ? 'Completed · undo' : 'Mark complete';
      });
      const icon = $(`[data-completion-icon="${lesson.id}"]`);
      if (icon) { icon.textContent = done ? '✓' : '○'; icon.setAttribute('aria-label', done ? 'Completed' : 'Not completed'); }
    });
  }
  function applyPreferences() {
    document.documentElement.dataset.theme = state.theme;
    document.documentElement.style.setProperty('--reading-size', state.textSize + 'px');
    const label = state.theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode';
    $('.theme-toggle').setAttribute('aria-label', label);
    $('.theme-toggle').textContent = state.theme === 'dark' ? 'Light' : 'Dark';
    $('[data-text-size="-1"]').disabled = state.textSize <= 18;
    $('[data-text-size="1"]').disabled = state.textSize >= 24;
  }
  $('.theme-toggle').addEventListener('click', () => {
    save(latest => ({ ...latest, theme: latest.theme === 'dark' ? 'light' : 'dark' }));
    applyPreferences(); updateProgress();
  });
  $$('[data-text-size]').forEach(button => button.addEventListener('click', () => {
    save(latest => ({ ...latest, textSize: latest.textSize + Number(button.dataset.textSize) }));
    applyPreferences(); updateProgress();
  }));
  addEventListener('storage', event => {
    if (event.key !== key && event.key !== null) return;
    try { state = pendingChanges.reduce((value, edit) => edit(value), readReaderState(localStorage, key, ids, data.aliases)); applyPreferences(); updateProgress(); }
    catch { warning.hidden = false; }
  });

  const sidebar = $('#sidebar');
  function closeMenu() {
    document.body.classList.remove('menu-open'); $('.menu-backdrop').hidden = true;
    $('#workspace').inert = false; $('.contents-toggle').setAttribute('aria-expanded', 'false');
    sidebar.removeAttribute('role'); sidebar.removeAttribute('aria-modal');
  }
  function openMenu() {
    if (matchMedia('(min-width: 1101px)').matches) return;
    document.body.classList.add('menu-open'); $('.menu-backdrop').hidden = false;
    $('#workspace').inert = true; $('.contents-toggle').setAttribute('aria-expanded', 'true');
    sidebar.setAttribute('role', 'dialog'); sidebar.setAttribute('aria-modal', 'true'); $('.mobile-close').focus();
  }
  $('.contents-toggle').addEventListener('click', openMenu);
  $('.mobile-close').addEventListener('click', () => { closeMenu(); $('.contents-toggle').focus(); });
  $('.menu-backdrop').addEventListener('click', () => { closeMenu(); $('.contents-toggle').focus(); });
  matchMedia('(min-width: 1101px)').addEventListener('change', event => { if (event.matches) closeMenu(); });

  const articles = $$('article[data-lesson]');
  let currentLesson = data.lessons[0], currentResource;
  function showLesson(id) {
    currentLesson = data.lessons.find(lesson => lesson.id === id) || data.lessons[0];
    articles.forEach(article => { article.hidden = article.id !== currentLesson.id; });
    $$('.lesson-nav').forEach(link => {
      if (link.dataset.lessonLink === currentLesson.id) {
        link.setAttribute('aria-current', 'page'); link.closest('details').open = true;
      } else link.removeAttribute('aria-current');
    });
    $('#breadcrumb-module').textContent = data.modules.find(module => module.id === currentLesson.moduleId).title;
    document.title = currentLesson.title + ' · System design';
  }
  function canonicalAnchor(hash) {
    let id;
    try { id = decodeURIComponent(hash.replace(/^#/, '')); } catch { return ''; }
    for (const [oldId, newId] of Object.entries(data.aliases)) {
      if (id === oldId || id.startsWith(oldId + '--')) return newId + id.slice(oldId.length);
    }
    return id;
  }
  function setHash(hash, replace = false) {
    try { history[replace ? 'replaceState' : 'pushState'](null, '', hash); }
    catch { location.hash = hash; }
  }
  function navigate(hash, focus = false) {
    const id = canonicalAnchor(hash);
    if (Object.hasOwn(data.resources, id)) {
      currentResource = data.resources[id];
      $('#resource-title').textContent = currentResource.title;
      $('#resource-content').textContent = currentResource.content;
      closeMenu(); if (!$('#resource-dialog').open) $('#resource-dialog').showModal(); return;
    }
    if ($('#resource-dialog').open) $('#resource-dialog').close();
    const target = document.getElementById(id);
    if (id === 'course-contents' || target?.closest('#sidebar')) {
      openMenu();
      if (target) {
        const module = target.closest('details'); if (module) module.open = true;
        target.scrollIntoView({ block: 'center' }); if (focus) target.focus();
      }
      return;
    }
    const article = target?.closest('article[data-lesson]');
    if (!article) return;
    showLesson(article.id);
    for (let ancestor = target; ancestor && ancestor !== article; ancestor = ancestor.parentElement) {
      if (ancestor.tagName === 'DETAILS') ancestor.open = true;
    }
    closeMenu();
    save(latest => ({ ...latest, lastLesson: currentLesson.id, lastAnchor: id })); updateProgress();
    requestAnimationFrame(() => {
      target.scrollIntoView({ block: 'start', behavior: 'instant' });
      if (focus) { target.setAttribute('tabindex', '-1'); target.focus({ preventScroll: true }); }
    });
  }
  document.addEventListener('click', event => {
    const link = event.target.closest('a[href^="#"]');
    if (!link || link.classList.contains('skip-link') || event.metaKey || event.ctrlKey) return;
    event.preventDefault();
    const hash = link.getAttribute('href');
    if (location.hash !== hash) setHash(hash);
    if ($('#search-dialog').open) $('#search-dialog').close();
    const index = link.closest('.section-index'); if (index) index.open = false;
    navigate(hash, true);
  });
  addEventListener('hashchange', () => navigate(location.hash));
  addEventListener('popstate', () => navigate(location.hash || '#' + currentLesson.id));

  let toastTimer;
  function toast(message) {
    clearTimeout(toastTimer); $('#toast').textContent = message; $('#toast').hidden = false;
    toastTimer = setTimeout(() => { $('#toast').hidden = true; }, 3500);
  }
  function download(name, contents, type) {
    const url = URL.createObjectURL(new Blob([contents], { type }));
    const link = document.createElement('a'); link.href = url; link.download = name;
    document.body.append(link); link.click(); link.remove(); setTimeout(() => URL.revokeObjectURL(url), 1000);
  }
  $('#download-resource').addEventListener('click', () => { if (currentResource) download(currentResource.title, currentResource.content, 'text/plain;charset=utf-8'); });

  const searchEntries = articles.flatMap(article => $$('[data-section]', article).map(section => ({ id: section.dataset.anchor, title: section.dataset.title, lessonId: article.id, lesson: data.lessons.find(lesson => lesson.id === article.id).title, text: section.textContent.replace(/\s+/g, ' ').trim() })));
  function search() {
    const query = $('#course-search').value.trim().toLocaleLowerCase();
    const lessonMatches = query ? data.catalog.filter(lesson => (lesson.title + ' ' + lesson.objective).toLocaleLowerCase().includes(query)) : [];
    const matchedIds = new Set(lessonMatches.map(lesson => lesson.id));
    const sections = query ? searchEntries.filter(entry => !matchedIds.has(entry.lessonId) && entry.text.toLocaleLowerCase().includes(query)) : [];
    const results = $('#search-results'); results.replaceChildren();
    const count = lessonMatches.length + sections.length;
    $('#search-status').textContent = !query ? 'Search written content and the full syllabus.' : count ? `${count} matches${count > 30 ? ' · showing the first 30' : ''}` : 'No matches. Try another word or phrase.';
    const entries = [...lessonMatches.map(lesson => ({ id: lesson.id, title: `${lesson.displayId} ${lesson.title}`, context: lesson.status === 'complete' ? 'Written lesson' : 'Planned · not yet written', text: lesson.objective, written: lesson.status === 'complete' })), ...sections.map(section => ({ ...section, context: section.lesson, written: true }))];
    entries.slice(0, 30).forEach(entry => {
      const result = document.createElement(entry.written ? 'a' : 'div'); result.className = 'search-result';
      if (entry.written) result.href = '#' + entry.id;
      const context = document.createElement('small'); context.textContent = entry.context;
      const title = document.createElement('strong'); title.textContent = entry.title;
      const snippet = document.createElement('p');
      const start = Math.max(0, entry.text.toLocaleLowerCase().indexOf(query) - 60);
      snippet.textContent = (start ? '…' : '') + entry.text.slice(start, start + 180) + (entry.text.length > start + 180 ? '…' : '');
      result.append(context, title, snippet); results.append(result);
    });
  }
  $('#course-search').addEventListener('input', search);
  function openSearch() { closeMenu(); $$('dialog[open]').forEach(dialog => dialog.close()); $('#search-dialog').showModal(); $('#course-search').focus(); }
  document.addEventListener('click', event => {
    const action = event.target.closest('[data-action]')?.dataset.action;
    if (action === 'search') openSearch();
    if (action === 'export') {
      if (!pendingChanges.length) { try { state = readReaderState(localStorage, key, ids, data.aliases); } catch {} }
      download('system-design-progress.json', JSON.stringify({ ...state, exportedAt: new Date().toISOString() }, null, 2), 'application/json');
      toast('Progress download requested.');
    }
    if (action === 'reset') { closeMenu(); $('#reset-dialog').showModal(); }
    if (action === 'download-markdown') download('System_Design_Fullstack_Masterclass.md', data.markdown, 'text/markdown;charset=utf-8');
    if (event.target.closest('[data-close-dialog]')) {
      const dialog = event.target.closest('dialog'); dialog.close();
      if (dialog.id === 'resource-dialog') setHash('#' + currentLesson.id, true);
    }
    const button = event.target.closest('[data-complete]');
    if (button) {
      const id = button.dataset.complete;
      const persisted = save(latest => ({ ...latest, completed: latest.completed.includes(id) ? latest.completed.filter(item => item !== id) : [...latest.completed, id] }));
      updateProgress();
      $('[data-save-feedback]', button.closest('article')).textContent = persisted ? 'Progress saved.' : 'Recorded for this session only. Browser storage is unavailable; export your progress before closing.';
    }
  });
  $('#confirm-reset').addEventListener('click', () => {
    const persisted = save(latest => ({ ...latest, completed: [] }));
    updateProgress(); $('#reset-dialog').close(); toast(persisted ? 'Completion reset.' : 'Completion reset for this session only.');
  });
  document.addEventListener('keydown', event => {
    if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') { event.preventDefault(); if (!$('#search-dialog').open) openSearch(); }
    if (document.body.classList.contains('menu-open')) {
      if (event.key === 'Escape') { closeMenu(); $('.contents-toggle').focus(); }
      if (event.key === 'Tab') {
        const items = $$('button, a[href], summary', sidebar).filter(item => item.getClientRects().length);
        const first = items[0], last = items.at(-1);
        if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
        if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
      }
    }
  });
  let enlargedDiagram;
  $$('[data-enlarge-diagram]').forEach(button => button.addEventListener('click', () => {
    const figure = button.closest('figure');
    const svg = $('svg', figure);
    const placeholder = document.createElement('div');
    placeholder.style.height = svg.getBoundingClientRect().height + 'px';
    svg.replaceWith(placeholder);
    enlargedDiagram = { svg, placeholder };
    $('#diagram-title').textContent = $('figcaption strong', figure).textContent;
    $('#diagram-content').append(svg);
    $('#diagram-dialog').showModal();
  }));
  $('#diagram-dialog').addEventListener('close', () => {
    if (enlargedDiagram) { enlargedDiagram.placeholder.replaceWith(enlargedDiagram.svg); enlargedDiagram = null; }
  });
  $$('.copy-code').forEach(button => button.addEventListener('click', async () => {
    const code = $('code', button.closest('figure'));
    try { await navigator.clipboard.writeText(code.textContent); toast('Code copied.'); }
    catch {
      const selection = getSelection(), range = document.createRange(); range.selectNodeContents(code); selection.removeAllRanges(); selection.addRange(range);
      toast('Code selected. Press Ctrl+C or ⌘C to copy.');
    }
  }));
  $$('.load-lab').forEach(lab => {
    const inputs = $$('input', lab);
    function calculate() {
      const [daily, factor, latency] = inputs.map(input => input.value.trim() === '' ? NaN : Number(input.value));
      const values = [daily / 86400, daily / 86400 * factor, daily / 86400 * factor * (latency / 1000)];
      const valid = [daily, factor, latency, ...values].every(Number.isFinite) && daily >= 0 && factor >= 1 && latency > 0;
      $('.lab-error', lab).hidden = valid;
      inputs.forEach((input, index) => input.setAttribute('aria-invalid', String(!Number.isFinite([daily, factor, latency][index]) || [daily < 0, factor < 1, latency <= 0][index])));
      $$('[data-lab-value]', lab).forEach((node, index) => { node.textContent = valid ? values[index].toLocaleString('en-US', { maximumFractionDigits: 2, minimumFractionDigits: 2 }) : '—'; });
    }
    inputs.forEach(input => input.addEventListener('input', calculate));
    $$('[data-latency]', lab).forEach(button => button.addEventListener('click', () => { inputs[2].value = button.dataset.latency; calculate(); }));
    calculate();
  });
  let readingScheduled = false;
  function rememberPosition() {
    readingScheduled = false;
    if (document.body.classList.contains('menu-open') || $('dialog[open]')) return;
    const headings = currentLesson.sections.map(section => document.getElementById(section.id)).filter(node => node.getClientRects().length);
    const active = [...headings].reverse().find(node => node.getBoundingClientRect().top <= 120);
    const anchor = active?.id || currentLesson.id;
    if (anchor !== state.lastAnchor) save(latest => ({ ...latest, lastLesson: currentLesson.id, lastAnchor: anchor }));
  }
  addEventListener('scroll', () => { if (!readingScheduled) { readingScheduled = true; requestAnimationFrame(rememberPosition); } }, { passive: true });
  applyPreferences(); updateProgress(); showLesson(state.lastLesson);
  const resume = location.hash || '#' + state.lastAnchor;
  if (document.getElementById(canonicalAnchor(resume)) || canonicalAnchor(resume) === 'course-contents' || Object.hasOwn(data.resources, canonicalAnchor(resume))) navigate(resume);
})();

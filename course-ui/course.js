(() => {
  'use strict';
  const data = JSON.parse(document.getElementById('course-data').textContent);
  const $ = (selector, scope = document) => scope.querySelector(selector);
  const $$ = (selector, scope = document) => [...scope.querySelectorAll(selector)];
  const key = 'system-design-masterclass-v1';
  const lessonIds = new Set(data.lessons.map(lesson => lesson.id));
  const warning = $('#storage-warning');
  let state = { version: 1, completed: [], theme: 'light', lastLesson: data.lessons[0].id };
  try {
    const saved = JSON.parse(localStorage.getItem(key) || 'null');
    if (saved?.version === 1) {
      state.completed = Array.isArray(saved.completed) ? [...new Set(saved.completed.filter(id => lessonIds.has(id)))] : [];
      if (saved.theme === 'dark' || saved.theme === 'light') state.theme = saved.theme;
      if (lessonIds.has(saved.lastLesson)) state.lastLesson = saved.lastLesson;
    } else if (matchMedia('(prefers-color-scheme: dark)').matches) state.theme = 'dark';
  } catch { warning.hidden = false; }

  function save() {
    try { localStorage.setItem(key, JSON.stringify(state)); }
    catch { warning.hidden = false; }
  }
  let toastTimer;
  function toast(message) {
    clearTimeout(toastTimer);
    $('#toast').textContent = message;
    $('#toast').hidden = false;
    toastTimer = setTimeout(() => { $('#toast').hidden = true; }, 3500);
  }
  function download(name, contents, type) {
    const url = URL.createObjectURL(new Blob([contents], { type }));
    const link = document.createElement('a');
    link.href = url; link.download = name;
    document.body.append(link); link.click(); link.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }
  function updateProgress() {
    const count = state.completed.length;
    $$('[data-progress-count]').forEach(node => { node.textContent = `${count} / ${data.lessons.length}`; });
    $$('[data-progress-bar]').forEach(node => { node.max = data.lessons.length; node.value = count; });
    $$('[data-progress-description]').forEach(node => { node.textContent = `${count} of ${data.lessons.length} available lessons completed`; });
    data.modules.forEach(module => {
      const lessons = data.lessons.filter(lesson => lesson.moduleId === module.id);
      $$(`[data-module-count="${module.id}"]`).forEach(node => {
        node.textContent = `${lessons.filter(lesson => state.completed.includes(lesson.id)).length} / ${lessons.length}`;
      });
    });
    data.lessons.forEach(lesson => {
      const done = state.completed.includes(lesson.id);
      $$(`[data-complete="${lesson.id}"]`).forEach(button => {
        button.setAttribute('aria-pressed', String(done));
        button.textContent = done ? '✓ Lesson completed' : 'Mark lesson complete ✓';
      });
      const icon = $(`[data-completion-icon="${lesson.id}"]`);
      if (icon) { icon.textContent = done ? '✓' : '○'; icon.setAttribute('aria-label', done ? 'Completed' : 'Not completed'); }
    });
  }
  function setTheme() {
    document.documentElement.dataset.theme = state.theme;
    const label = state.theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode';
    $('.theme-toggle').setAttribute('aria-label', label);
    $('.theme-toggle').title = label;
    $('.theme-toggle').textContent = state.theme === 'dark' ? '☀' : '◐';
  }
  $('.theme-toggle').addEventListener('click', () => {
    state.theme = state.theme === 'dark' ? 'light' : 'dark'; setTheme(); save();
  });
  const sidebar = $('#sidebar');
  function closeMenu() {
    document.body.classList.remove('menu-open');
    $('.menu-backdrop').hidden = true;
    $('#workspace').inert = false;
    $('.mobile-menu').setAttribute('aria-expanded', 'false');
    sidebar.removeAttribute('role'); sidebar.removeAttribute('aria-modal');
  }
  $('.mobile-menu').addEventListener('click', () => {
    document.body.classList.add('menu-open'); $('.menu-backdrop').hidden = false;
    $('#workspace').inert = true; $('.mobile-menu').setAttribute('aria-expanded', 'true');
    sidebar.setAttribute('role', 'dialog'); sidebar.setAttribute('aria-modal', 'true');
    $('.mobile-close').focus();
  });
  $('.mobile-close').addEventListener('click', () => { closeMenu(); $('.mobile-menu').focus(); });
  $('.menu-backdrop').addEventListener('click', () => { closeMenu(); $('.mobile-menu').focus(); });
  matchMedia('(min-width: 701px)').addEventListener('change', event => { if (event.matches) closeMenu(); });

  const articles = $$('article[data-lesson]');
  let currentLesson = data.lessons[0];
  const outline = $('#page-outline');
  function showLesson(id) {
    currentLesson = data.lessons.find(lesson => lesson.id === id) || data.lessons[0];
    articles.forEach(article => { article.hidden = article.id !== currentLesson.id; });
    $$('.lesson-nav').forEach(link => {
      if (link.dataset.lessonLink === currentLesson.id) link.setAttribute('aria-current', 'page');
      else link.removeAttribute('aria-current');
    });
    $('#breadcrumb-module').textContent = data.modules.find(module => module.id === currentLesson.moduleId).title;
    outline.replaceChildren();
    currentLesson.sections.forEach(section => {
      const link = document.createElement('a'); link.href = '#' + section.id;
      link.textContent = section.title.replace(/^[A-K]\. /, ''); outline.append(link);
    });
    state.lastLesson = currentLesson.id; save();
    document.title = currentLesson.title + ' — System Design';
  }
  let currentResource;
  function navigate(hash, focus = false) {
    const id = decodeURIComponent(hash.replace(/^#/, ''));
    const resource = data.resources[id];
    if (resource) {
      currentResource = resource;
      $('#resource-title').textContent = resource.title;
      $('#resource-content').textContent = resource.content;
      closeMenu();
      if (!$('#resource-dialog').open) $('#resource-dialog').showModal();
      return;
    }
    if ($('#resource-dialog').open) $('#resource-dialog').close();
    const target = document.getElementById(id);
    const article = target?.closest('article[data-lesson]');
    if (!article) return;
    showLesson(article.id);
    let ancestor = target;
    while (ancestor && ancestor !== article) {
      if (ancestor.tagName === 'DETAILS') ancestor.open = true;
      ancestor = ancestor.parentElement;
    }
    closeMenu();
    requestAnimationFrame(() => {
      target.scrollIntoView({ block: 'start', behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth' });
      if (focus) { target.setAttribute('tabindex', '-1'); target.focus({ preventScroll: true }); }
    });
  }
  document.addEventListener('click', event => {
    const link = event.target.closest('a[href^="#"]');
    if (!link || link.classList.contains('skip-link') || event.metaKey || event.ctrlKey) return;
    event.preventDefault();
    const hash = link.getAttribute('href');
    if (location.hash !== hash) history.pushState(null, '', hash);
    if ($('#search-dialog').open) $('#search-dialog').close();
    navigate(hash, true);
  });
  addEventListener('hashchange', () => navigate(location.hash));
  addEventListener('popstate', () => navigate(location.hash || '#' + currentLesson.id));
  $('#download-resource').addEventListener('click', () => {
    if (currentResource) download(currentResource.title, currentResource.content, 'text/plain;charset=utf-8');
  });

  const searchEntries = articles.flatMap(article => $$('[data-section]', article).map(section => ({
    id: section.dataset.anchor, title: section.dataset.title,
    lesson: data.lessons.find(lesson => lesson.id === article.id).title,
    text: section.textContent.replace(/\s+/g, ' ').trim(),
  })));
  function search() {
    const query = $('#course-search').value.trim().toLocaleLowerCase();
    const matches = query ? searchEntries.filter(entry => (entry.lesson + ' ' + entry.title + ' ' + entry.text).toLocaleLowerCase().includes(query)) : [];
    $('#search-status').textContent = !query ? 'Search lesson text, exercises, and solutions.' : matches.length ? `${matches.length} matching sections` : 'No matches. Try a different word or phrase.';
    const results = $('#search-results'); results.replaceChildren();
    matches.slice(0, 15).forEach(entry => {
      const link = document.createElement('a'); link.className = 'search-result'; link.href = '#' + entry.id;
      const title = document.createElement('strong'); title.textContent = entry.title;
      const context = document.createElement('small'); context.textContent = entry.lesson;
      const snippet = document.createElement('p');
      const index = entry.text.toLocaleLowerCase().indexOf(query);
      const start = Math.max(0, index - 65);
      snippet.textContent = (start ? '…' : '') + entry.text.slice(start, start + 190) + (entry.text.length > start + 190 ? '…' : '');
      link.append(context, title, snippet); results.append(link);
    });
  }
  $('#course-search').addEventListener('input', search);
  function openSearch() { closeMenu(); $('#search-dialog').showModal(); $('#course-search').focus(); }
  document.addEventListener('click', event => {
    const action = event.target.closest('[data-action]')?.dataset.action;
    if (action === 'search') openSearch();
    if (action === 'export') {
      download('system-design-progress.json', JSON.stringify({ ...state, exportedAt: new Date().toISOString() }, null, 2), 'application/json');
      toast('Progress exported as a JSON file.');
    }
    if (action === 'reset') { closeMenu(); $('#reset-dialog').showModal(); }
    if (action === 'download-markdown') download('System_Design_Fullstack_Masterclass.md', data.markdown, 'text/markdown;charset=utf-8');
    if (event.target.closest('[data-close-dialog]')) event.target.closest('dialog').close();
    const button = event.target.closest('[data-complete]');
    if (button) {
      const id = button.dataset.complete;
      state.completed = state.completed.includes(id) ? state.completed.filter(item => item !== id) : [...state.completed, id];
      save(); updateProgress();
      toast(state.completed.includes(id) ? 'Lesson completed. Your progress is saved.' : 'Lesson marked as in progress.');
    }
    const next = event.target.closest('[data-goto-lesson]');
    if (next && !next.disabled) { history.pushState(null, '', '#' + next.dataset.gotoLesson); navigate(location.hash, true); }
  });
  $('#confirm-reset').addEventListener('click', () => {
    state.completed = []; save(); updateProgress(); $('#reset-dialog').close(); toast('Learning progress reset.');
  });
  document.addEventListener('keydown', event => {
    if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') {
      event.preventDefault(); if (!$('#search-dialog').open) openSearch();
    }
    if (document.body.classList.contains('menu-open')) {
      if (event.key === 'Escape') { closeMenu(); $('.mobile-menu').focus(); }
      if (event.key === 'Tab') {
        const items = $$('button, a[href], summary', sidebar).filter(item => item.getClientRects().length);
        const first = items[0], last = items.at(-1);
        if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
        if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
      }
    }
  });
  $$('.copy-code').forEach(button => button.addEventListener('click', async () => {
    const code = $('code', button.closest('figure'));
    try {
      await navigator.clipboard.writeText(code.textContent); toast('Code copied.');
    } catch {
      const selection = getSelection(); const range = document.createRange();
      range.selectNodeContents(code); selection.removeAllRanges(); selection.addRange(range);
      toast('Code selected. Press Ctrl+C or ⌘C to copy.');
    }
  }));

  $$('.load-lab').forEach(lab => {
    const inputs = $$('input', lab);
    function calculate() {
      const [daily, factor, latency] = inputs.map(input => input.value.trim() === '' ? NaN : Number(input.value));
      const average = daily / 86400, peak = average * factor, occupancy = peak * latency / 1000;
      const valid = [daily, factor, latency, average, peak, occupancy].every(Number.isFinite) && daily >= 0 && factor >= 1 && latency > 0;
      $('.lab-error', lab).hidden = valid;
      inputs.forEach(input => input.setAttribute('aria-invalid', String(!input.checkValidity() || !valid)));
      $$('[data-lab-value]', lab).forEach((node, index) => {
        node.textContent = valid ? [average, peak, occupancy][index].toLocaleString('en-US', { maximumFractionDigits: 2, minimumFractionDigits: 2 }) : '—';
      });
    }
    inputs.forEach(input => input.addEventListener('input', calculate));
    $$('[data-latency]', lab).forEach(button => button.addEventListener('click', () => { inputs[2].value = button.dataset.latency; calculate(); }));
    calculate();
  });
  let readingScheduled = false;
  function updateReading() {
    readingScheduled = false;
    const article = document.getElementById(currentLesson.id);
    const top = article.getBoundingClientRect().top + scrollY;
    const end = top + article.offsetHeight - innerHeight;
    const percent = end <= top ? 100 : Math.max(0, Math.min(100, (scrollY - top) / (end - top) * 100));
    $('#reading-fill').style.width = percent + '%';
    const headings = currentLesson.sections.map(section => document.getElementById(section.id)).filter(node => node.getClientRects().length);
    const active = [...headings].reverse().find(node => node.getBoundingClientRect().top <= 145) || headings[0];
    $$('a', outline).forEach(link => {
      if (link.hash === '#' + active?.id) link.setAttribute('aria-current', 'location'); else link.removeAttribute('aria-current');
    });
  }
  addEventListener('scroll', () => { if (!readingScheduled) { readingScheduled = true; requestAnimationFrame(updateReading); } }, { passive: true });
  addEventListener('resize', updateReading);
  document.addEventListener('toggle', updateReading, true);
  setTheme(); updateProgress(); showLesson(state.lastLesson);
  if (location.hash) navigate(location.hash); updateReading();
})();

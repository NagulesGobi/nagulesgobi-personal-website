/* The live site's theme switch, dock and search palette, shared with the case study pages (assets/js/site.js). */
(function () {
  var doc = document.documentElement, RM = matchMedia('(prefers-reduced-motion: reduce)').matches, MQ = matchMedia('(prefers-color-scheme: dark)');
  function isDark() { var t = doc.dataset.theme; return t ? t === 'dark' : MQ.matches; }
  function syncTheme() { doc.classList.toggle('is-dark', isDark()); dispatchEvent(new Event('ng-theme')); }
  syncTheme(); MQ.addEventListener('change', syncTheme);
  document.querySelectorAll('.theme-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var next = isDark() ? 'light' : 'dark';
      var apply = function () { doc.dataset.theme = next; try { localStorage.setItem('ng-theme', next); } catch (e) {} syncTheme(); };
      if (!document.startViewTransition || RM) return apply();
      var r = btn.getBoundingClientRect(), x = r.left + r.width / 2, y = r.top + r.height / 2;
      var end = Math.hypot(Math.max(x, innerWidth - x), Math.max(y, innerHeight - y));
      document.startViewTransition(apply).ready.then(function () {
        doc.animate({ clipPath: ['circle(0px at ' + x + 'px ' + y + 'px)', 'circle(' + end + 'px at ' + x + 'px ' + y + 'px)'] },
          { duration: 900, easing: 'cubic-bezier(.65,0,.35,1)', pseudoElement: '::view-transition-new(root)' });
      });
    });
  });
})();
(function () {
  var doc = document.documentElement;
  var RM = matchMedia('(prefers-reduced-motion: reduce)').matches, FINE = matchMedia('(hover: hover) and (pointer: fine)').matches;

  /* Dock minimise: fold into the round N-mark on scroll down, open on scroll up, hover, focus or tap */
  var mdock = document.querySelector('[data-dock]');
  if (mdock) {
    var lastY = scrollY, acc = 0;
    var dmark = mdock.querySelector('.dk-mark');
    var openedAt = 0;
    function setMini(on) { if (!on && mdock.classList.contains('mini')) openedAt = Date.now(); mdock.classList.remove('hold'); mdock.classList.toggle('mini', on); }
    addEventListener('scroll', function () {
      var y = scrollY, dy = y - lastY; lastY = y;
      if (y < 120) { acc = 0; setMini(false); return; }
      if (mdock.matches(':hover') || mdock.contains(document.activeElement)) return;
      acc = (dy > 0) === (acc > 0) ? acc + dy : dy;
      if (acc > 40) setMini(true); else if (acc < -40) { hoverOpened = false; setMini(false); }
    }, { passive: true });
    var hoverOpened = false, foldT = 0;
    mdock.addEventListener('pointerenter', function (e) {
      if (e.pointerType !== 'mouse') return;
      clearTimeout(foldT); mdock.classList.remove('hold');
      if (mdock.classList.contains('mini')) { hoverOpened = true; setMini(false); }
    });
    // opened by hovering the round button: fold back, gently, once the pointer leaves
    mdock.addEventListener('pointerleave', function (e) {
      if (e.pointerType !== 'mouse' || !hoverOpened) return;
      clearTimeout(foldT); mdock.classList.add('hold');
      foldT = setTimeout(function () {
        hoverOpened = false; mdock.classList.remove('hold');
        if (scrollY >= 120 && !mdock.contains(document.activeElement) && !document.querySelector('.finder:not([hidden])')) setMini(true);
      }, 450);
    });
    mdock.addEventListener('focusin', function () { setMini(false); });
    if (dmark) dmark.addEventListener('click', function (e) { if (mdock.classList.contains('mini') || Date.now() - openedAt < 400) { e.preventDefault(); setMini(false); } });
  }

  /* Dock: liquid-glass magnification. The slot sizes are fixed while hovered (CSS), so the
     item boxes never move; tiles scale and slide with transforms only, which cannot feed back. */
  var dock = document.querySelector('[data-dock]');
  if (dock && FINE && !RM) {
    var kids = Array.prototype.slice.call(dock.children), raf = 0, px = null;
    function dockApply() {
      raf = 0;
      if (px === null || innerWidth <= 820) {
        dock.style.removeProperty('--mx');
        kids.forEach(function (k) { k.style.removeProperty('--tx'); var t = k.querySelector('.dk-tile'); if (t) t.style.removeProperty('--ts'); });
        return;
      }
      var dr = dock.getBoundingClientRect(); dock.style.setProperty('--mx', (px - dr.left) + 'px');
      var extra = kids.map(function (k) {
        var t = k.classList.contains('dk-item') && k.querySelector('.dk-tile'); if (!t) return 0;
        var r = k.getBoundingClientRect(), d = px - (r.left + r.width / 2), f = Math.exp(-(d * d) / (2 * 46 * 46)), ts = 1 + 0.2 * f;
        t.style.setProperty('--ts', ts.toFixed(3)); return r.width * (ts - 1);
      });
      kids.forEach(function (k, i) {
        var before = 0, after = 0;
        for (var j = 0; j < kids.length; j++) { if (j < i) before += extra[j]; else if (j > i) after += extra[j]; }
        k.style.setProperty('--tx', ((before - after) * 0.24).toFixed(2) + 'px');
      });
    }
    dock.addEventListener('pointermove', function (e) { px = e.clientX; dock.classList.add('live'); if (!raf) raf = requestAnimationFrame(dockApply); });
    dock.addEventListener('pointerleave', function () { px = null; dock.classList.remove('live'); if (!raf) raf = requestAnimationFrame(dockApply); });
  }


  /* Search palette */
  var finder = document.querySelector('.finder');
  if (!finder) return;
  var input = finder.querySelector('input'), list = finder.querySelector('.fd-list'), empty = finder.querySelector('.fd-empty');
  var rows = Array.prototype.slice.call(list.querySelectorAll('li[role="option"]')), groups = Array.prototype.slice.call(list.querySelectorAll('.fd-group'));
  var lastFocus = null, idx = 0;
  function visible() { return rows.filter(function (r) { return !r.hidden; }); }
  function mark(i) {
    var v = visible(); if (!v.length) return;
    idx = (i + v.length) % v.length;
    rows.forEach(function (r) { r.classList.remove('on'); r.removeAttribute('aria-selected'); });
    v[idx].classList.add('on'); v[idx].setAttribute('aria-selected', 'true');
    v[idx].scrollIntoView({ block: 'nearest' });
  }
  function filter() {
    var q = input.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
    rows.forEach(function (r) { var t = (r.firstElementChild.getAttribute('data-text') || '').toLowerCase(); r.hidden = !q.every(function (w) { return t.indexOf(w) > -1; }); });
    groups.forEach(function (g) { var n = g.nextElementSibling, any = false; while (n && !n.classList.contains('fd-group')) { if (!n.hidden) any = true; n = n.nextElementSibling; } g.hidden = !any; });
    empty.hidden = visible().length > 0;
    mark(0);
  }
  function open() {
    if (!finder.hidden) return;
    lastFocus = document.activeElement; finder.hidden = false; input.value = ''; filter();
    doc.style.overflow = 'hidden'; setTimeout(function () { input.focus(); }, 20);
  }
  function close() {
    if (finder.hidden) return;
    finder.hidden = true; doc.style.overflow = '';
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }
  document.querySelectorAll('[data-finder-open]').forEach(function (b) { b.addEventListener('click', open); });
  finder.querySelectorAll('[data-finder-close]').forEach(function (b) { b.addEventListener('click', close); });
  input.addEventListener('input', filter);
  finder.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') { e.preventDefault(); close(); }
    else if (e.key === 'ArrowDown') { e.preventDefault(); mark(idx + 1); }
    else if (e.key === 'ArrowUp') { e.preventDefault(); mark(idx - 1); }
    else if (e.key === 'Enter') { var v = visible()[idx]; if (v) { e.preventDefault(); v.firstElementChild.click(); } }
    else if (e.key === 'Tab') { e.preventDefault(); input.focus(); }
  });
  rows.forEach(function (r) {
    r.addEventListener('pointermove', function () { var v = visible(), i = v.indexOf(r); if (i > -1 && i !== idx) mark(i); });
    var a = r.firstElementChild;
    a.addEventListener('click', function () {
      if (a.hasAttribute('data-theme-toggle')) { var t = document.querySelector('.dock .theme-btn'); close(); if (t) t.click(); return; }
      // same-page hash links: close first so the page can scroll
      var url = new URL(a.href, location.href);
      if (url.pathname === location.pathname && url.hash) close();
    });
  });
  document.addEventListener('keydown', function (e) {
    var typing = /input|textarea|select/i.test((e.target.tagName || '')) || e.target.isContentEditable;
    if ((e.metaKey || e.ctrlKey) && (e.key === 'k' || e.key === 'K')) { e.preventDefault(); finder.hidden ? open() : close(); }
    else if (e.key === '/' && !typing && finder.hidden) { e.preventDefault(); open(); }
  });
})();

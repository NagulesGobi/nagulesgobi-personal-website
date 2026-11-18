/* Case study pages: chapters, a pinned rail and the same dot engine as the main pages.
   Every section with a heading becomes a numbered chapter; the rail's drawing becomes that chapter's number as you
   scroll, and the index shows where you are. The case pages switch theme through assets/js/site.js, so the dots are
   told when data-theme changes. */
import { startDots } from './dots.js';

const flow = document.querySelector('.cs-flow'), list = document.querySelector('.cs-index ol');
const chapters = [];
if (flow && list) {
  const esc = t => t.replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  [...flow.children].forEach(sec => {
    const h = sec.querySelector('.case-sec > h2, .section-head h2'); if (!h) return;
    const n = String(chapters.length + 1).padStart(2, '0');
    sec.id = sec.id || 'chapter-' + n;
    sec.dataset.dots = 'num:' + n; sec.dataset.artRef = '#cs-art';
    const label = h.textContent.replace(/\s+/g, ' ').trim().replace(/[.:]$/, '');
    list.insertAdjacentHTML('beforeend', `<li><a href="#${sec.id}"><span class="n">${n}</span><span class="t">${esc(label)}</span></a></li>`);
    chapters.push({ sec, link: list.lastElementChild.firstElementChild });
  });
  // the chapter whose top has passed 40% of the screen is the current one
  let raf = 0;
  const spy = () => { raf = 0; const line = innerHeight * .4; let cur = null;
    for (const c of chapters) if (c.sec.getBoundingClientRect().top <= line) cur = c;
    chapters.forEach(c => c === cur ? c.link.setAttribute('aria-current', 'true') : c.link.removeAttribute('aria-current')); };
  addEventListener('scroll', () => { if (!raf) raf = requestAnimationFrame(spy); }, { passive: true }); spy();
}

new MutationObserver(() => dispatchEvent(new Event('ng-theme'))).observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme', 'class'] });
startDots({ intro: false });

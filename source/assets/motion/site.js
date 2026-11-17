/* Shared behaviour for the main pages (home, work, about, contact, dotXline) */
import { startDots } from './dots.js';

const RM = matchMedia('(prefers-reduced-motion: reduce)').matches;
const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
document.documentElement.classList.remove('no-js');

/* Smooth scroll (off for reduced motion) */
let lenis = null;
if (!RM && window.Lenis) {
  lenis = new Lenis({ lerp: .1, smoothWheel: true });
  (function raf(t) { lenis.raf(t); requestAnimationFrame(raf); })(performance.now());
}
$$('a[href^="#"]').forEach(a => a.addEventListener('click', e => {
  const id = a.getAttribute('href'); if (id.length < 2 || !$(id)) return;
  e.preventDefault(); lenis ? lenis.scrollTo(id, { offset: -80, duration: 1.4 }) : $(id).scrollIntoView({ behavior: RM ? 'auto' : 'smooth' });
}));

/* Reveal on enter */
const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), { threshold: .15, rootMargin: '0px 0px -8% 0px' });
$$('.rv').forEach(el => RM ? el.classList.add('in') : io.observe(el));

/* London clock */
$$('[data-clock]').forEach(el => { const tick = () => el.textContent = new Intl.DateTimeFormat('en-GB', { timeZone: 'Europe/London', hour: '2-digit', minute: '2-digit' }).format(new Date()); tick(); setInterval(tick, 20000); });
$$('[data-year]').forEach(el => el.textContent = new Date().getFullYear());

/* Count-up facts */
const cio = new IntersectionObserver(es => es.forEach(e => {
  if (!e.isIntersecting) return; cio.unobserve(e.target);
  const el = e.target, to = +el.dataset.count, suf = el.dataset.suffix || ''; if (RM) { el.textContent = to + suf; return; }
  const t0 = performance.now(); (function step(n) { const p = Math.min(1, (n - t0) / 1400), v = 1 - Math.pow(1 - p, 3); el.textContent = Math.round(to * v) + suf; if (p < 1) requestAnimationFrame(step); })(t0);
}), { threshold: .6 });
$$('[data-count]').forEach(el => cio.observe(el));

/* Filters (work page) */
$$('[data-filter-group]').forEach(group => {
  const target = $(group.dataset.filterGroup), items = $$('[data-cat]', target);
  $$('button', group).forEach(b => b.addEventListener('click', () => {
    $$('button', group).forEach(x => x.setAttribute('aria-pressed', x === b));
    const f = b.dataset.filter; items.forEach(it => it.hidden = f !== 'all' && !it.dataset.cat.split(' ').includes(f));
  }));
});

/* Lightbox (brand gallery) */
const lb = $('.lightbox');
if (lb) {
  $$('[data-full]').forEach(b => b.addEventListener('click', () => {
    $('img', lb).src = b.dataset.full; $('img', lb).alt = b.dataset.title; $('p', lb).textContent = b.dataset.title + ' · ' + b.dataset.sub; lb.showModal();
  }));
  $('.close', lb).addEventListener('click', () => lb.close());
  lb.addEventListener('click', e => { if (e.target === lb) lb.close(); });
}

/* Contact form: writes the email for you */
const form = $('[data-mailform]');
if (form) {
  $$('.chips button', form).forEach(b => b.addEventListener('click', () => b.setAttribute('aria-pressed', b.getAttribute('aria-pressed') !== 'true')));
  form.addEventListener('submit', e => {
    e.preventDefault();
    const name = form.name.value.trim(), email = form.email.value.trim(), msg = form.message.value.trim(), err = $('[data-err]', form);
    const bad = !name ? form.name : !/^\S+@\S+\.\S+$/.test(email) ? form.email : !msg ? form.message : null;
    if (bad) { err.textContent = bad === form.email ? 'Please add an email address I can reply to.' : `Please add your ${bad.name}.`; bad.focus(); return; }
    err.textContent = '';
    const want = $$('.chips button[aria-pressed="true"]', form).map(b => b.textContent).join(', ');
    const body = `${msg}\n\n${want ? 'Looking for: ' + want + '\n' : ''}${form.company.value ? 'Company: ' + form.company.value + '\n' : ''}${name}\n${email}`;
    location.href = `mailto:contact@nagulesgobi.com?subject=${encodeURIComponent('Hello from ' + name)}&body=${encodeURIComponent(body)}`;
  });
}
$$('[data-copy]').forEach(b => b.addEventListener('click', async () => {
  try { await navigator.clipboard.writeText(b.dataset.copy); b.textContent = 'Copied'; } catch { b.textContent = 'Press Ctrl+C'; }
  setTimeout(() => b.textContent = 'Copy email', 2000);
}));

/* Work index: the project in the middle of the screen is the current one */
const rowsEl = $$('.wl-row'), nowN = $('[data-wl-n]'), nowName = $('[data-wl-name]');
if (rowsEl.length) {
  let raf = 0;
  const spy = () => { raf = 0; const mid = innerHeight / 2; let best = null, bd = 1e9;
    rowsEl.forEach(r => { const b = r.getBoundingClientRect(), d = Math.abs(b.top + Math.min(b.height, innerHeight) / 2 - mid); if (b.top < mid + 40 && d < bd) { bd = d; best = r; } });
    rowsEl.forEach(r => r.classList.toggle('on', r === best));
    const i = best ? rowsEl.indexOf(best) + 1 : 0;
    if (nowN) nowN.textContent = `0${i} / 0${rowsEl.length}`; if (nowName) nowName.textContent = best ? best.dataset.name : 'Selected work'; };
  addEventListener('scroll', () => { if (!raf) raf = requestAnimationFrame(spy); }, { passive: true }); spy();
}

/* About: the process line fills as the section scrolls through the middle of the screen */
const proc = $('[data-process]');
if (proc) {
  const steps = $$('li', proc); let raf = 0;
  const fill = () => { raf = 0; const r = proc.getBoundingClientRect(), phone = innerWidth < 900;
    const p = RM ? 1 : Math.max(0, Math.min(1, phone ? (innerHeight * .6 - r.top) / r.height : (innerHeight * .85 - r.top) / (innerHeight * .5)));
    proc.style.setProperty('--p', p.toFixed(3));
    steps.forEach((li, i) => li.classList.toggle('on', p >= (phone ? i / steps.length : i / (steps.length - 1)) - .001)); };
  addEventListener('scroll', () => { if (!raf) raf = requestAnimationFrame(fill); }, { passive: true }); fill();
}

/* Dots */
startDots({ intro: document.body.dataset.intro === 'on' && !sessionStorage.getItem('ng-seen'), lenis });
sessionStorage.setItem('ng-seen', '1');

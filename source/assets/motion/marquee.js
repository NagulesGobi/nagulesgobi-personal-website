/* The scrolling marquee from the live home page (assets/js/site.js and base.css), used on the home page.
   Two rows: solid and outline, moving in opposite directions, speeding up with scroll and reversing when you scroll up. */
(function () {
  var css = '' +
    '.marquee{position:relative;z-index:2;padding:34px 0;border-block:1px solid var(--line);overflow:hidden;background:var(--bg);color:var(--text)}' +
    '.marquee-row{display:flex;white-space:nowrap}' +
    '.marquee-row+.marquee-row{margin-top:8px}' +
    '.marquee-track{display:flex;align-items:center;gap:40px;padding-right:40px;flex-shrink:0;will-change:transform}' +
    '.marquee span{font:600 clamp(44px,7vw,104px)/1.05 "Barlow Semi Condensed","Arial Narrow",system-ui,sans-serif;text-transform:uppercase;letter-spacing:-.01em}' +
    '.marquee b{font-size:clamp(22px,3vw,40px);color:var(--accent)}' +
    '.marquee .outline span{color:transparent;-webkit-text-stroke:1.5px var(--mq-faint,#8D877C)}' +
    ':root[data-theme="dark"]{--mq-faint:#6F6A62}@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--mq-faint:#6F6A62}}';
  var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);

  var RM = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var rows = [].slice.call(document.querySelectorAll('[data-marquee]')).map(function (row) {
    var track = row.firstElementChild, copy = track.cloneNode(true); copy.setAttribute('aria-hidden', 'true'); row.appendChild(copy);
    var m = { row: row, tracks: [track, copy], dir: +row.dataset.marquee, speed: +(row.dataset.speed || 0.6), x: 0, w: 0, vis: true };
    new IntersectionObserver(function (e) { m.vis = e[0].isIntersecting; }).observe(row);
    return m;
  });
  function measure() { rows.forEach(function (m) { m.w = m.tracks[0].offsetWidth; }); }
  measure(); addEventListener('resize', measure); document.fonts && document.fonts.ready.then(measure);
  if (RM || !rows.length) return;
  var lastY = scrollY, vel = 0;
  (function frame() {
    var y = scrollY, dy = y - lastY; lastY = y; vel += (dy - vel) * 0.12;
    rows.forEach(function (m) {
      if (!m.vis || !m.w) return;
      m.x -= (m.speed + Math.abs(vel) * 0.25) * m.dir * (vel < 0 ? -1 : 1);
      if (m.x <= -m.w) m.x += m.w; if (m.x > 0) m.x -= m.w;
      var tf = 'translate3d(' + m.x.toFixed(2) + 'px,0,0)';
      m.tracks[0].style.transform = tf; m.tracks[1].style.transform = tf;
    });
    requestAnimationFrame(frame);
  })();
})();

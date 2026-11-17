/* Dot artwork for the main pages.
   The same dots as the live hero logo: small squares on an even grid (6 px apart, 62% filled; 4 px on phones),
   pushed by the cursor and settling back with the same spring. As the page scrolls, the dots leave one artwork
   and rebuild the next. Each artwork sits exactly inside its [data-art] box, so it lines up with the layout. */
import * as THREE from 'three';

const RM = matchMedia('(prefers-reduced-motion: reduce)').matches;
const DARK = matchMedia('(prefers-color-scheme: dark)');
const C = 640; // drawing canvas size
const N_D = 'M12.75 8H56.72A30.53 30.53 0 0 1 87.25 38.53V38.53H73.82V38.53A17.1 17.1 0 0 0 56.72 21.43H35.68L73.82 59.57V51.97H87.25V92L26.18 30.93V51.97A17.1 17.1 0 0 0 43.28 69.07H43.28V82.5H43.28A30.53 30.53 0 0 1 12.75 51.97Z';
const rr = (x, X, Y, W, H, R) => { x.beginPath(); x.roundRect(X, Y, W, H, R); x.fill(); };
const grad = (x, x0, y0, x1, y1) => { const g = x.createLinearGradient(x0, y0, x1, y1); g.addColorStop(0, '#FF9124'); g.addColorStop(.3, '#FF4A2C'); g.addColorStop(.55, '#FF2440'); g.addColorStop(1, '#FF008E'); return g; };
const glyph = (txt, size = 520) => (x, k) => { x.fillStyle = k.ink; x.font = `600 ${size}px "Barlow Semi Condensed"`; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText(txt, C / 2, C / 2); };

/* The artworks. k = theme colours. Each draws inside a 640 box; it is cropped to its ink and fitted afterwards. */
export const SHAPES = {
  n(x) { x.scale(6.4, 6.4); const g = x.createRadialGradient(12.75, 8, 0, 12.75, 8, 108); g.addColorStop(0, '#FF9124'); g.addColorStop(.3, '#FF4A2C'); g.addColorStop(.55, '#FF2440'); g.addColorStop(1, '#FF008E'); x.fillStyle = g; x.fill(new Path2D(N_D)); },
  notes(x, k) { const n = [[40, 60, -5, '#F7CE46'], [250, 40, 4, '#FF9EB0'], [460, 80, -3, '#8FD6BE'], [60, 270, 5, '#9EC5FF'], [270, 250, -4, '#F7CE46'], [470, 290, 6, '#FF9EB0'], [120, 470, -2, '#8FD6BE'], [340, 460, 3, '#9EC5FF']];
    for (const [X, Y, a, c] of n) { x.save(); x.translate(X + 65, Y + 65); x.rotate(a * Math.PI / 180); x.fillStyle = c; x.fillRect(-65, -65, 130, 130); x.fillStyle = k.ink; x.fillRect(-44, -34, 72, 9); x.fillRect(-44, -14, 52, 9); x.restore(); } },
  // iPhone 17 Pro proportions: body 71.9 x 150 mm (0.479), corner 18% of width, bezel 3.7%, screen corner 14.3%, Dynamic Island 31% of the screen
  wire(x, k) { x.strokeStyle = k.ink; x.lineWidth = 9; x.beginPath(); x.roundRect(180.5, 24.5, 279, 591, 48); x.stroke(); x.fillStyle = k.ink; rr(x, 279, 40, 82, 22, 11);
    x.fillStyle = k.soft; rr(x, 206, 92, 140, 20, 8); rr(x, 206, 128, 228, 128, 14); rr(x, 206, 274, 228, 18, 8); rr(x, 206, 304, 170, 18, 8);
    rr(x, 206, 342, 106, 96, 14); rr(x, 328, 342, 106, 96, 14); rr(x, 206, 456, 228, 18, 8); rr(x, 206, 548, 228, 46, 23);
    x.strokeStyle = k.soft; x.lineWidth = 5; x.beginPath(); x.moveTo(206, 128); x.lineTo(434, 256); x.moveTo(434, 128); x.lineTo(206, 256); x.stroke(); },
  ui(x, k) { x.fillStyle = k.ink; rr(x, 176, 20, 288, 600, 52); x.fillStyle = k.paper; rr(x, 187, 31, 266, 578, 41); x.fillStyle = k.ink; rr(x, 279, 40, 82, 24, 12);
    rr(x, 206, 92, 140, 22, 8); x.fillStyle = grad(x, 206, 128, 434, 256); rr(x, 206, 128, 228, 128, 16); x.fillStyle = k.ink; rr(x, 206, 274, 228, 16, 8); x.fillStyle = k.faint; rr(x, 206, 302, 160, 14, 7);
    x.fillStyle = '#0F9D7A'; rr(x, 206, 342, 106, 96, 18); x.fillStyle = '#F5A524'; rr(x, 328, 342, 106, 96, 18); x.fillStyle = k.ink; rr(x, 206, 548, 228, 46, 23); },
  proto(x, k) { SHAPES.wire(x, k); x.strokeStyle = '#FF2440'; x.lineWidth = 7; x.setLineDash([16, 12]); x.beginPath(); x.moveTo(434, 192); x.bezierCurveTo(600, 192, 600, 571, 434, 571); x.stroke(); x.setLineDash([]);
    x.fillStyle = '#FF2440'; x.beginPath(); x.moveTo(434, 571); x.lineTo(462, 552); x.lineTo(462, 590); x.fill(); },
  code: glyph('</>', 420),
  xpense(x) { x.scale(.62, .62); x.translate(-80, 30); x.fillStyle = '#A6DCC9'; rr(x, 158, 291, 708, 188, 94); x.fillStyle = '#F5A524'; rr(x, 335, 545, 531, 188, 94); x.fillStyle = '#0F9D7A'; rr(x, 158, 545, 487, 188, 94); },
  tockbee(x, k) { x.scale(6.4, 6.4); x.fillStyle = '#FF4F5A'; x.fill(new Path2D('M50 14a36 36 0 1 1 0 72a36 36 0 1 1 0-72zM50 24a26 26 0 1 0 0 52a26 26 0 1 0 0-52z'), 'evenodd');
    x.save(); x.translate(50, 50); x.rotate(-Math.PI / 4); x.fillStyle = k.dark ? '#F1ECE2' : '#2A1712'; rr(x, -5, -5, 41, 10, 5); x.restore(); x.fillStyle = '#FFB627'; x.beginPath(); x.arc(71.92, 28.08, 11, 0, 7); x.fill(); },
  freshbit(x, k) { x.scale(.625, .625); x.fillStyle = k.dark ? '#F1ECE2' : '#0E1A12'; x.fill(new Path2D('M512 205H819V512C819 682 682 819 512 819H205V512C205 342 342 205 512 205ZM353 630L630 353L681 404L404 681Z'), 'evenodd');
    x.strokeStyle = '#B9E62E'; x.lineWidth = 58; x.lineCap = 'round'; x.beginPath(); x.moveTo(392, 642); x.lineTo(642, 392); x.stroke(); },
  tiles(x, k) { const t = [[20, 20, 300, 230, k.ink], [340, 20, 280, 340, '#0F9D7A'], [20, 270, 300, 350, '#FF4F5A'], [340, 380, 130, 240, '#F5A524'], [490, 380, 130, 240, k.soft]];
    for (const [X, Y, W, H, c] of t) { x.fillStyle = c; rr(x, X, Y, W, H, 22); } },
  hello: glyph('HELLO', 250),
  at: glyph('@', 560),
  zero: glyph('0', 600), times: glyph('×', 600), one: glyph('1', 600),
  dotx(x) { x.translate(-10, 40); x.scale(7.4, 7.4); x.strokeStyle = '#D97706'; x.lineWidth = 10; x.lineCap = 'round'; x.lineJoin = 'round';
    x.stroke(new Path2D('M63.44 36.56 L38.69 61.31 A16 16 0 1 1 38.69 38.69 L61.31 61.31 A9 9 0 0 0 76.68 54.95 L76.68 20.00')); },
  // client marks, cut from each project's own cover or logo file
  chatvertiser: { image: 'assets/img/motion/mark-chatvertiser.png', mode: 'ink' },
  greenlife: { image: 'assets/img/motion/mark-greenlife.png', mode: 'color' },
  'puff-count': { image: 'assets/img/motion/mark-puffcount.png', mode: 'color' },
  pocket: { image: 'assets/img/motion/mark-pocket.png', mode: 'color' },
  // brand and print: a pen-tool curve with its anchors and handles
  pen(x, k) { x.strokeStyle = grad(x, 60, 560, 580, 80); x.lineWidth = 34; x.lineCap = 'round'; x.beginPath(); x.moveTo(70, 540); x.bezierCurveTo(70, 160, 570, 480, 570, 100); x.stroke();
    x.strokeStyle = k.ink; x.lineWidth = 6; x.beginPath(); x.moveTo(70, 540); x.lineTo(70, 300); x.moveTo(570, 100); x.lineTo(570, 340); x.stroke();
    x.fillStyle = k.ink; for (const [X, Y] of [[70, 540], [570, 100]]) x.fillRect(X - 30, Y - 30, 60, 60); x.fillStyle = k.paper; for (const [X, Y] of [[70, 540], [570, 100]]) x.fillRect(X - 18, Y - 18, 36, 36);
    x.fillStyle = k.ink; for (const [X, Y] of [[70, 300], [570, 340]]) { x.beginPath(); x.arc(X, Y, 22, 0, 7); x.fill(); } },
  ask: glyph('?', 600),
  portrait: { image: 'assets/img/me/portrait.webp' }
};

function theme() {
  const t = document.documentElement.dataset.theme, dark = t ? t === 'dark' : DARK.matches;
  return dark ? { dark, ink: '#F1ECE2', paper: '#1C1B18', soft: '#4A463F', faint: '#7A746B' } : { dark, ink: '#15130F', paper: '#FBF9F4', soft: '#CFC7B8', faint: '#8D877C' };
}
const imgCache = {};
function loadImg(src) { return imgCache[src] ||= new Promise(r => { const i = new Image(); i.onload = () => r(i); i.onerror = () => r(null); i.src = src; }); }

/* Draw, crop to ink, then sample on a square grid that gives `gap` screen px between dots at `size` px */
function sampleShape(key, size, gap, k, img, boxW = size, boxH = size) {
  if (key === 'off') { const z = new Float32Array(1); return { n: 1, x: z, y: z, r: z, g: z, b: z, s: z }; } // dots gather and fade over text-heavy sections
  const cv = document.createElement('canvas'); cv.width = cv.height = C;
  const x = cv.getContext('2d', { willReadFrequently: true });
  const def = SHAPES[key];
  let halftone = false, mode = def && def.mode;
  if (def && def.image) {
    if (!img) return null; halftone = !mode;
    const s = Math.min(C / img.width, C / img.height); x.drawImage(img, (C - img.width * s) / 2, (C - img.height * s) / 2, img.width * s, img.height * s);
  } else def(x, k);
  const d = x.getImageData(0, 0, C, C).data;
  let x0 = C, y0 = C, x1 = 0, y1 = 0;
  for (let y = 0; y < C; y += 2) for (let xx = 0; xx < C; xx += 2) if (d[(y * C + xx) * 4 + 3] > 110) { if (xx < x0) x0 = xx; if (xx > x1) x1 = xx; if (y < y0) y0 = y; if (y > y1) y1 = y; }
  const bw = Math.max(1, x1 - x0), bh = Math.max(1, y1 - y0), scale = Math.min(boxW / bw, boxH / bh), step = gap / scale;
  const pts = [], cols = [], sz = [];
  for (let y = y0 + step / 2; y <= y1; y += step) for (let xx = x0 + step / 2; xx <= x1; xx += step) {
    const i = ((y | 0) * C + (xx | 0)) * 4; if (d[i + 3] <= 110) continue;
    let m = 1, r = d[i], g = d[i + 1], b = d[i + 2];
    if (halftone) { // a halftone: darker means a bigger dot; the light backdrop drops out
      const L = (.299 * r + .587 * g + .114 * b) / 255; if (L > .8) continue;
      m = Math.min(1.35, .35 + (1 - L) * 1.25); const c = k.dark ? [241, 236, 226] : [21, 19, 15]; r = c[0]; g = c[1]; b = c[2];
    }
    if (mode === 'ink') { const c = k.dark ? [241, 236, 226] : [21, 19, 15]; r = c[0]; g = c[1]; b = c[2]; }
    pts.push((xx - (x0 + x1) / 2) * scale, (y - (y0 + y1) / 2) * scale); cols.push(r / 255, g / 255, b / 255); sz.push(m);
  }
  // scattered order, so a morph scatters instead of sliding row by row; seeded, so a rebuild keeps every dot in place
  const n = sz.length, ord = Array.from({ length: n }, (_, i) => i);
  let seed = n * 2654435761 >>> 0; const rnd = () => (seed = (seed * 1664525 + 1013904223) >>> 0) / 4294967296;
  for (let i = n - 1; i > 0; i--) { const j = Math.floor(rnd() * (i + 1)); [ord[i], ord[j]] = [ord[j], ord[i]]; }
  return { n, x: Float32Array.from(ord, i => pts[i * 2]), y: Float32Array.from(ord, i => pts[i * 2 + 1]),
    r: Float32Array.from(ord, i => cols[i * 3]), g: Float32Array.from(ord, i => cols[i * 3 + 1]), b: Float32Array.from(ord, i => cols[i * 3 + 2]), s: Float32Array.from(ord, i => sz[i]) };
}

export async function startDots({ intro = false, lenis = null } = {}) {
  const canvas = document.getElementById('dots'); if (!canvas) return;
  const stages = [...document.querySelectorAll('[data-dots]')];
  if (!stages.length) return;
  await document.fonts.ready;
  const imgs = {}; for (const key of new Set(stages.map(s => s.dataset.dots))) if (SHAPES[key]?.image) imgs[key] = await loadImg(SHAPES[key].image);

  const renderer = new THREE.WebGLRenderer({ canvas, antialias: false, alpha: true, powerPreference: 'high-performance' });
  const PR = Math.min(devicePixelRatio, 2); renderer.setPixelRatio(PR);
  const scene = new THREE.Scene(), camera = new THREE.OrthographicCamera(0, 1, 0, -1, -100, 100);
  const geo = new THREE.BufferGeometry();
  const mat = new THREE.ShaderMaterial({ transparent: true, depthWrite: false, depthTest: false, vertexColors: true,
    uniforms: { uPR: { value: PR }, uDot: { value: 3.7 } },
    vertexShader: 'attribute float aS; attribute float aA; varying vec3 vC; varying float vA; uniform float uPR; uniform float uDot; void main(){ vC = color; vA = aA; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.); gl_PointSize = max(0., uDot * aS * uPR); }',
    fragmentShader: 'varying vec3 vC; varying float vA; void main(){ if (vA < .01) discard; gl_FragColor = vec4(vC, vA); }' });
  const points = new THREE.Points(geo, mat); points.frustumCulled = false; scene.add(points);

  let W = 0, H = 0, P = 0, gap = 6, list = [], pos, col, aS, aA, px, py, vx, vy, rnd, delay;
  const ptr = { x: -9999, y: -9999, on: false }, shocks = [];
  addEventListener('pointermove', e => { ptr.x = e.clientX; ptr.y = e.clientY; ptr.on = true; }, { passive: true });
  document.addEventListener('pointerleave', () => { ptr.on = false; });
  addEventListener('pointerdown', e => { if (e.target.closest('a, button, input, textarea, summary')) return; shocks.push({ x: e.clientX, y: e.clientY + (lenis ? lenis.scroll : scrollY), r: 0, f: 9 }); });

  function build() {
    W = innerWidth; H = innerHeight; renderer.setSize(W, H, false);
    camera.left = 0; camera.right = W; camera.top = 0; camera.bottom = -H; camera.updateProjectionMatrix();
    const phone = W < 900; gap = phone ? 4 : 6; mat.uniforms.uDot.value = gap * .62;
    const k = theme(), sy = scrollY;
    list = stages.map(el => {
      // an artwork either sits inside its section, or is a shared pinned box (data-art-ref) that several sections redraw
      const ref = el.dataset.artRef && document.querySelector(el.dataset.artRef);
      const art = el.querySelector('[data-art]') || ref || el, r = art.getBoundingClientRect();
      if (!r.width || !r.height && ref) return null; // hidden at this width
      const size = Math.min(r.width, r.height || r.width), bw = r.width, bh = r.height || r.width;
      const s = { el, key: el.dataset.dots, small: art.hasAttribute('data-small'), cx: r.left + r.width / 2, cy: r.top + sy + r.height / 2, size, shape: sampleShape(el.dataset.dots, size, gap, k, imgs[el.dataset.dots], bw, bh) };
      if (ref) { // the pinned box: work out where it sits for any scroll position, so the dots stay locked to it
        const pin = ref.closest('.wl-pin') || ref, box = pin.parentElement.getBoundingClientRect(), pr = pin.getBoundingClientRect();
        s.ref = ref; s.pin = { T: parseFloat(getComputedStyle(pin).top) || 0, lo: box.top + sy, hi: box.bottom + sy - pr.height, off: r.top - pr.top + r.height / 2 };
        const e = el.getBoundingClientRect(); s.mid = e.top + sy + Math.min(e.height, H) / 2;
      }
      return s;
    }).filter(s => s && s.shape);
    if (!list.length) return;
    const maxScroll = document.documentElement.scrollHeight - H;
    list.forEach(s => { s.anchor = Math.max(0, Math.min(maxScroll, (s.mid ?? s.cy) - H / 2)); });
    list.sort((a, b) => a.anchor - b.anchor);
    const need = Math.max(...list.map(s => s.shape.n));
    if (need !== P) {
      const oldX = px, oldY = py, oldP = P; P = need;
      pos = new Float32Array(P * 3); col = new Float32Array(P * 3); aS = new Float32Array(P); aA = new Float32Array(P);
      px = new Float32Array(P); py = new Float32Array(P); vx = new Float32Array(P); vy = new Float32Array(P); rnd = new Float32Array(P * 3); delay = new Float32Array(P);
      for (let i = 0; i < P; i++) {
        rnd[i * 3] = Math.random() - .5; rnd[i * 3 + 1] = Math.random() - .5; rnd[i * 3 + 2] = Math.random() * 6.283;
        if (oldX && i < oldP) { px[i] = oldX[i]; py[i] = oldY[i]; }
        else { const a = Math.random() * 6.283, rad = Math.max(W, H) * (.6 + Math.random() * .6); px[i] = W / 2 + Math.cos(a) * rad; py[i] = sy + H / 2 + Math.sin(a) * rad; }
      }
      geo.setAttribute('position', new THREE.BufferAttribute(pos, 3).setUsage(THREE.DynamicDrawUsage));
      geo.setAttribute('color', new THREE.BufferAttribute(col, 3).setUsage(THREE.DynamicDrawUsage));
      geo.setAttribute('aS', new THREE.BufferAttribute(aS, 1).setUsage(THREE.DynamicDrawUsage));
      geo.setAttribute('aA', new THREE.BufferAttribute(aA, 1).setUsage(THREE.DynamicDrawUsage));
    }
    // the intro builds the first artwork from the top-left corner outward, like the live logo
    const f = list[0]; if (f) for (let i = 0; i < P; i++) { const j = i % f.shape.n; delay[i] = ((f.shape.x[j] + f.shape.y[j]) / Math.max(1, f.size) + 1) * 450 + Math.random() * 250; }
    if (RM) for (let i = 0; i < P; i++) { px[i] = -9999; }
  }
  let rt; addEventListener('resize', () => { clearTimeout(rt); rt = setTimeout(build, 180); });
  addEventListener('ng-theme', () => { clearTimeout(rt); rt = setTimeout(build, 30); });
  new ResizeObserver(() => { clearTimeout(rt); rt = setTimeout(build, 180); }).observe(document.body);
  build();

  const born = performance.now() - (intro && !RM ? 0 : 99999);
  function frame(now) {
    const y = lenis ? lenis.scroll : scrollY, t = now / 1000;
    if (!list.length) { renderer.clear(); requestAnimationFrame(frame); return; }
    const pinY = s => s.pin ? Math.min(s.pin.hi, Math.max(s.pin.lo, y + s.pin.T)) + s.pin.off : s.cy;
    // which two artworks are we between, and how far
    let a = list[0], b = list[0], m = 0;
    for (let i = 0; i < list.length - 1; i++) {
      if (y >= list[i].anchor && y <= list[i + 1].anchor) {
        a = list[i]; b = list[i + 1];
        const f = (y - a.anchor) / Math.max(1, b.anchor - a.anchor), e = Math.min(1, Math.max(0, (f - .3) / .4)); m = e * e * (3 - 2 * e); break;
      }
      if (y > list[i + 1].anchor) { a = b = list[i + 1]; }
    }
    // each artwork scrolls with its own box; mid-way the dots travel between the two
    const ax = a.cx, ay = pinY(a), bx = b.cx, by = pinY(b); // page coordinates
    const pyx = ptr.x, pyy = ptr.y + y;
    const aOff = a.key === 'off', bOff = b.key === 'off';
    // fading into a text section: the dots stay on the artwork and fade, they never cross the text
    // small artworks sit next to headings: they dissolve in place instead of flying across the text
    const dissolve = a !== b && (a.small || b.small || W < 900) && !aOff && !bOff;
    const burst = RM || aOff || bOff || dissolve ? 0 : Math.sin(m * Math.PI), spread = Math.min(a.size, b.size, 600) * (a.ref && a.ref === b.ref ? .16 : .35);
    const R = Math.max(90, W * .09), R2 = R * R;
    for (let i = 0; i < P; i++) {
      const A = aOff ? b.shape : a.shape, B = bOff ? a.shape : b.shape, ia = i % A.n, ib = i % B.n;
      const ax2 = aOff ? bx : ax, ay2 = aOff ? by : ay, bx2 = bOff ? ax : bx, by2 = bOff ? ay : by;
      const mm = dissolve ? (m < .5 ? 0 : 1) : m;
      let tx = (ax2 + A.x[ia]) * (1 - mm) + (bx2 + B.x[ib]) * mm + rnd[i * 3] * burst * spread;
      let ty = (ay2 + A.y[ia]) * (1 - mm) + (by2 + B.y[ib]) * mm + rnd[i * 3 + 1] * burst * spread;
      // duplicates (when the artwork has fewer dots than the pool) are hidden
      const visA = i < A.n ? 1 : 0, visB = i < B.n ? 1 : 0;
      aA[i] = dissolve ? (m < .5 ? visA * (1 - m * 2) : visB * (m * 2 - 1)) : (aOff ? 0 : visA) * (1 - m) + (bOff ? 0 : visB) * m;
      if (dissolve && aA[i] < .02) { vx[i] = vy[i] = 0; px[i] = tx; py[i] = ty; } // move only while invisible
      aS[i] = (A.s[ia] * (1 - mm) + B.s[ib] * mm) * (1 + burst * rnd[i * 3 + 1] * .8);
      col[i * 3] = A.r[ia] * (1 - mm) + B.r[ib] * mm; col[i * 3 + 1] = A.g[ia] * (1 - mm) + B.g[ib] * mm; col[i * 3 + 2] = A.b[ia] * (1 - mm) + B.b[ib] * mm;
      if (RM) { px[i] = tx; py[i] = ty; }
      else if (now - born < delay[i]) { /* waiting for the intro */ }
      else {
        tx += Math.sin(t * 1.4 + rnd[i * 3 + 2]) * .9; ty += Math.cos(t * 1.1 + rnd[i * 3 + 2]) * .9;
        vx[i] += (tx - px[i]) * .045; vy[i] += (ty - py[i]) * .045;
        if (ptr.on) { const dx = px[i] - pyx, dy = py[i] - pyy, d2 = dx * dx + dy * dy; if (d2 < R2 && d2 > .01) { const d = Math.sqrt(d2), f = (1 - d / R) * 7.5; vx[i] += dx / d * f; vy[i] += dy / d * f; } }
        for (const s of shocks) { const sx = px[i] - s.x, sy2 = py[i] - s.y, sd = Math.sqrt(sx * sx + sy2 * sy2) || 1, band = Math.abs(sd - s.r); if (band < 40) { const f = (1 - band / 40) * s.f; vx[i] += sx / sd * f; vy[i] += sy2 / sd * f; } }
        vx[i] *= .82; vy[i] *= .82; px[i] += vx[i]; py[i] += vy[i];
      }
      pos[i * 3] = Math.round(px[i]); pos[i * 3 + 1] = -(Math.round(py[i]) - y); pos[i * 3 + 2] = 0;
    }
    for (let k = shocks.length - 1; k >= 0; k--) { shocks[k].r += 14; shocks[k].f *= .93; if (shocks[k].f < .2) shocks.splice(k, 1); }
    geo.attributes.position.needsUpdate = geo.attributes.color.needsUpdate = geo.attributes.aS.needsUpdate = geo.attributes.aA.needsUpdate = true;
    renderer.render(scene, camera);
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
}

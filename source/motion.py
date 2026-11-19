"""The main pages of nagulesgobi.com: home, work, about, contact and dotXline.
Called from source/build.py (run `python3 source/build.py` from the repository root); writes the pages to the root.
Copy comes from the site's own pages and case studies; images are the site's assets (assets/img, assets/img/motion)."""
import hashlib, html, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
OUT = ROOT
A = 'assets/img/'                 # site images, from the root pages
M = 'assets/img/motion/'          # clean screen crops and client marks used by these pages
E = lambda t: html.escape(t, quote=True)
V = hashlib.sha1(b''.join(open(os.path.join(HERE, 'assets', 'motion', f), 'rb').read() for f in ('motion.css', 'dock.css', 'dots.js', 'site.js', 'dock.js', 'marquee.js'))).hexdigest()[:8]
SIZES = json.load(open(os.path.join(HERE, 'img-sizes.json')))
src = open(os.path.join(HERE, 'build.py')).read()
g = src[src.index('GALLERY = ['):]; g = g[:g.index('\n]') + 2]
GALLERY = re.findall(r"\('([^']+)', '([^']+)', '([^']*)', '([^']*)', (?:True|False)\)", g)

MARK100 = open(os.path.join(HERE, 'parts', 'site-parts.txt')).read().split('\n')[3]
STOPS = '<stop offset="0" stop-color="#FF9124"/><stop offset=".3" stop-color="#FF4A2C"/><stop offset=".55" stop-color="#FF2440"/><stop offset="1" stop-color="#FF008E"/>'
ICONS = {'work.html': 'M4 7h16v13H4zM9 7V4h6v3M4 12h16', 'about.html': 'M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM4 21c1-4 4-6 8-6s7 2 8 6',
         'contact.html': 'M3 6h18v12H3zM3 7l9 6 9-6', 'search': 'M11 18a7 7 0 1 0 0-14 7 7 0 0 0 0 14zM21 21l-5-5'}
DX_MARK = ('<svg class="dk-dx" viewBox="0.37 0.37 87.31 87.31" aria-hidden="true"><path transform="translate(0 1.025)" '
           'd="M63.44 36.56 L38.69 61.31 A16 16 0 1 1 38.69 38.69 L61.31 61.31 A9 9 0 0 0 76.68 54.95 L76.68 20.00" '
           'fill="none" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/></svg>')
THEME_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle class="sun" cx="12" cy="12" r="5"/><g class="rays"><path d="M12 1.5v2.2M12 20.3v2.2M1.5 12h2.2M20.3 12h2.2M4.6 4.6l1.6 1.6M17.8 17.8l1.6 1.6M4.6 19.4l1.6-1.6M17.8 6.2l1.6-1.6"/></g><circle class="moon-cut" cx="17" cy="7" r="5"/></svg>'


def icon(key):
    return DX_MARK if key == 'dotxline.html' else f'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="{ICONS[key]}"/></svg>'


def dock(file):
    def item(h, t):
        return f'<a class="dk-item" href="{h}"{" aria-current=\"page\"" if h == file else ""} aria-label="{t}"><span class="dk-tile">{icon(h)}</span><span class="dk-tip">{t}</span></a>'
    items = [('Pages', 'Home', 'Products, designed and built end to end', 'index.html'), ('Pages', 'Work', 'Product case studies, brand and print', 'work.html'),
             ('Pages', 'Brand and print', f'{len(GALLERY)} logos, campaigns, print and packaging pieces', 'work.html#brand'), ('Pages', 'dotXline', 'My product company in Cardiff', 'dotxline.html'),
             ('Pages', 'About', 'Story, process and capabilities', 'about.html'), ('Pages', 'Contact', 'Hire me for a role or a project', 'contact.html')]
    items += [('Case studies', t, kd, f'work/{sl}.html') for sl, t, kd in CASE_KINDS]
    out, last = '', None
    for g, t, sub, h in items:
        if g != last: out += f'<li class="fd-group" role="presentation">{g}</li>'; last = g
        out += f'<li role="option"><a href="{h}" data-text="{(t + " " + sub + " " + g).lower()}"><b>{t}</b><span>{sub}</span><i aria-hidden="true">↵</i></a></li>'
    out += '<li class="fd-group" role="presentation">Actions</li><li role="option"><a href="mailto:nagulesgobi@dotxline.com" data-text="email contact hire mail"><b>Email me</b><span>nagulesgobi@dotxline.com</span><i aria-hidden="true">↵</i></a></li>'
    out += '<li role="option"><button type="button" data-theme-toggle data-text="theme dark light mode switch"><b>Switch theme</b><span>Light or dark</span><i aria-hidden="true">↵</i></button></li>'
    return f'''<header class="dock-wrap">
  <nav class="dock" aria-label="Main" data-dock>
    <a class="dk-item dk-mark" href="index.html"{" aria-current=\"page\"" if file == "index.html" else ""} aria-label="Nagules Gobi, home"><span class="dk-tile"><svg viewBox="0 0 100 100" aria-hidden="true"><defs><radialGradient id="dkg" gradientUnits="userSpaceOnUse" cx="15" cy="8" r="113">{STOPS}</radialGradient></defs><path fill="url(#dkg)" d="{MARK100}"/></svg></span><span class="dk-tip">Home</span></a>
    <i class="dk-sep" aria-hidden="true"></i>
    {''.join(item(h, t) for h, t in PAGES[1:])}
    <i class="dk-sep" aria-hidden="true"></i>
    <button class="dk-item" type="button" data-finder-open aria-label="Search the site (Command K)" aria-haspopup="dialog"><span class="dk-tile">{icon('search')}</span><span class="dk-tip">Search <kbd>⌘K</kbd></span></button>
    <button class="dk-item theme-btn" type="button" aria-label="Switch between light and dark theme"><span class="dk-tile">{THEME_SVG}</span><span class="dk-tip">Theme</span></button>
    <a class="dk-hire" href="contact.html"><span class="pulse" aria-hidden="true"></span>Hire me</a>
  </nav>
</header>
<div class="finder" role="dialog" aria-modal="true" aria-label="Search the site" hidden>
  <div class="fd-backdrop" data-finder-close></div>
  <div class="fd-panel">
    <label class="fd-field"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="{ICONS['search']}"/></svg><input type="text" placeholder="Search pages and case studies" autocomplete="off" spellcheck="false" aria-label="Search" aria-controls="fd-list"><kbd>Esc</kbd></label>
    <ul class="fd-list" id="fd-list" role="listbox">{out}</ul>
    <p class="fd-empty" hidden>Nothing matches. Try “app”, “brand” or “contact”.</p>
    <div class="fd-foot mono"><span>↑ ↓ to move</span><span>↵ to open</span><span>⌘K or / to search</span></div>
  </div>
</div>'''


PAGES = [('index.html', 'Home'), ('work.html', 'Work'), ('about.html', 'About'), ('dotxline.html', 'dotXline'), ('contact.html', 'Contact')]
CASE_KINDS = [('xpense', 'Xpense', 'iPhone app · dotXline'), ('tockbee', 'Tockbee', 'iPhone and Android app · dotXline'), ('freshbit', 'FreshBit', 'iPhone, iPad and Mac app · dotXline'),
              ('chatvertiser', 'Chatvertiser', 'Web design · Ad tech UX'), ('greenlife', 'Greenlife', 'App design · Grocery'), ('puff-count', 'Puff Count', 'App design · Health'), ('pocket', 'Pocket', 'iOS app design · Personal finance')]
CASES = [(sl, t) for sl, t, _ in CASE_KINDS]


def img(path, alt, cls='', lazy=True, key=None):
    w, h = SIZES.get(key or path.rsplit('.', 1)[0], (None, None))
    wh = f' width="{w}" height="{h}"' if w else ''
    return f'<img src="{A}{path}" alt="{alt}"{wh}{" loading=\"lazy\" decoding=\"async\"" if lazy else ""}{f" class=\"{cls}\"" if cls else ""}>'


def phones(kind, shots, label, reveal=True):
    ims = ''.join(f'<div class="phone"><img src="{s}" alt="{label} screen" width="402" height="874" loading="lazy" decoding="async"></div>' for s in shots)
    return f'<div class="phones {kind}{" rv" if reveal else ""}" style="--d:.1s">{ims}</div>'


XP = [M + 'xp-screen-1.webp', M + 'xp-screen-3.webp']
TB = [A + 'apps/tockbee-today.webp', A + 'apps/tockbee-shifts.webp']
FB = [A + 'kit/fb2-phone-light.webp', A + 'kit/fb2-phone-dark.webp']   # real FreshBit renders, full size, same 402:874 shape


def page(file, title, desc, body, intro=False):
    canon = '' if file == 'index.html' else file
    nav = ''.join(f'<a href="{f}"{" aria-current=\"page\"" if f == file else ""}>{t}</a>' for f, t in PAGES[1:])
    cases = ''.join(f'<li><a href="work/{s}.html">{t}</a></li>' for s, t in CASES)
    return f'''<!doctype html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<script>try {{ var t = localStorage.getItem('ng-theme'); if (t === 'light' || t === 'dark') document.documentElement.dataset.theme = t; }} catch (e) {{}}</script>
<meta name="theme-color" content="#F3EFE7" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#12110F" media="(prefers-color-scheme: dark)">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:type" content="website">
<meta property="og:image" content="https://www.nagulesgobi.com/assets/brand/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="https://www.nagulesgobi.com/{canon}">
<link rel="icon" href="favicon.ico" sizes="48x48">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="manifest" href="site.webmanifest">
<link rel="modulepreload" href="assets/motion/dots.js">
{'<link rel="preload" as="image" href="assets/img/motion/portrait-dots.webp">' if file == 'about.html' else ''}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Semi+Condensed:wght@500;600;700&family=Barlow:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/motion/motion.css?v={V}">
<link rel="stylesheet" href="assets/motion/dock.css?v={V}">
<script src="assets/motion/dock.js?v={V}" defer></script>
<script src="https://cdn.jsdelivr.net/npm/lenis@1.1.13/dist/lenis.min.js" defer></script>
<script type="module" src="assets/motion/site.js?v={V}"></script>
</head>
<body data-intro="{'on' if intro else 'off'}">
<a class="skip" href="#main">Skip to content</a>
<canvas id="dots" aria-hidden="true"></canvas>
{dock(file)}
<main id="main">
{body}
</main>
<footer class="site-foot">
  <div class="wrap">
    <p class="kicker">Open to product design roles and freelance projects</p>
    <a class="big" href="mailto:nagulesgobi@dotxline.com">nagulesgobi@dotxline.com</a>
    <div class="foot-cols">
      <div><h4>Nagules Gobi</h4><p class="hint">Product designer in the United Kingdom. Director of dotXline LTD.</p><p class="hint" style="margin-top:8px">London <span data-clock>--:--</span></p></div>
      <div><h4>Pages</h4><ul>{''.join(f'<li><a href="{f}">{t}</a></li>' for f, t in PAGES)}</ul></div>
      <div><h4>Case studies</h4><ul>{cases}</ul></div>
      <div><h4>Elsewhere</h4><ul><li><a href="https://dotxline.com" target="_blank" rel="noopener">dotxline.com ↗</a></li><li><a href="https://www.behance.net/gallery/224174429/Chatvertiser" target="_blank" rel="noopener">Behance ↗</a></li><li><a href="mailto:nagulesgobi@dotxline.com">Email</a></li></ul></div>
    </div>
    <div class="foot-row"><p>© <span data-year>2026</span> Nagules Gobi · Product designer, United Kingdom</p><p>Designed and built by me</p></div>
  </div>
</footer>
{'<script src="assets/motion/marquee.js?v={V}" defer></script>' if file == 'index.html' else ''}
</body>
</html>
'''


def k(n, text):
    return f'<p class="kicker rv">{f"<span class=\"n\">{n}</span>" if n else ""}{text}</p>'


# ------------------------------------------------------------------ home
STEPS = [('notes', 'Discovery', 'Research the people, the goal and the constraints.'),
         ('wire', 'Wireframes', 'Structure and flow before any polish.'),
         ('ui', 'UI design', 'High-fidelity screens and a visual system.'),
         ('proto', 'Prototype', 'An interactive version to test and refine.'),
         ('code', 'Build', 'I build it with AI-assisted development, or hand clean specs to your developers.')]

APPS = [('xpense', 'xp', XP, 'Xpense', 'iPhone app · dotXline', 'Every penny, in plain sight.', 'A calm, native iPhone expense tracker. Log spending, set budgets and goals, and split costs with friends.', ['iPhone', 'SwiftUI', 'No ads'], 'Live on the App Store', ''),
        ('tockbee', 'tb', TB, 'Tockbee', 'iPhone and Android app · dotXline', 'Every hour you work, on the record.', 'Tockbee clocks you in when you arrive at work, works out your pay and take-home, and checks your payslip against the hours you really worked.', ['iPhone and Android', 'React Native', 'No tracking'], 'Live on the App Store', ''),
        ('freshbit', 'fb', FB, 'FreshBit', 'iPhone, iPad and Mac app · dotXline', 'News that checks first.', 'Confirmed news for designers and developers. FreshBit reads 51 trusted sources, groups the articles about the same event and scores each story out of 100.', ['iPhone, iPad and Mac', 'Expo and SwiftUI', 'No ads'], 'In TestFlight testing', 'test')]


def app_stage(a, i, heading_tag='h2', total=None):
    key, cls, shots, name, kind, line, about, tags, status, st = a
    return f'''<section class="stage app" id="{key}" data-dots="{key}" aria-labelledby="app-{key}">
  <div class="wrap">
    <div class="copy">
      <div class="art" data-art data-small aria-hidden="true"></div>
      <p class="kicker rv"><span class="n">0{i + 1}{f' / 0{total}' if total else ''}</span>{kind}</p>
      <{heading_tag} id="app-{key}" class="rv" style="--d:.05s">{name}</{heading_tag}>
      <p class="lead rv" style="--d:.1s"><strong>{line}</strong> {about}</p>
      <ul class="tags rv" style="--d:.15s">{''.join(f'<li>{t}</li>' for t in tags)}<li class="status {st}">{status}</li></ul>
      <div class="btns rv" style="--d:.2s"><a class="btn btn-solid" href="work/{key}.html">Read the case study</a></div>
    </div>
    {phones(cls, shots, name)}
  </div>
</section>'''


CLIENT = [('chatvertiser', 'Chatvertiser', 'Web design · Ad tech UX', 'An AI-powered advertising platform that turns conversations into conversion tools.', 'work/cv-cover.webp'),
          ('greenlife', 'Greenlife', 'App design · Grocery', 'A grocery shopping app that helps people buy their favourite fruit and vegetables from home, fast.', 'work/greenlife.webp'),
          ('puff-count', 'Puff Count', 'App design · Health', 'A mobile app that tracks nicotine consumption, with daily limits and onboarding that helps people quit vaping.', 'work/pc-cover.webp'),
          ('pocket', 'Pocket', 'iOS app design · Personal finance', 'A personal wallet app for iPhone: log expenses by category, see weekly statistics and keep your balance under control.', 'work/pw-cover.webp')]


def rows():
    return '<ol class="rows">' + ''.join(f'''<li class="rv" style="--d:{i * .05:.2f}s"><a href="work/{s}.html"><span class="no mono">0{i + 1}</span><span><span class="kind mono">{kd}</span><h3>{t}</h3></span><p class="desc">{d}</p><figure>{img(p, t)}</figure></a></li>''' for i, (s, t, kd, d, p) in enumerate(CLIENT)) + '</ol>'


MARQUEE = '''<section class="marquee" aria-label="Disciplines">
  <div class="marquee-row" data-marquee="1"><div class="marquee-track"><span>UX/UI Design</span><b>✦</b><span>App Development</span><b>✦</b><span>Product Design</span><b>✦</b><span>Web Development</span><b>✦</b><span>Brand Identity</span><b>✦</b></div></div>
  <div class="marquee-row outline" data-marquee="-1" aria-hidden="true"><div class="marquee-track"><span>iPhone &amp; Android Apps</span><b>✦</b><span>AI-Assisted Development</span><b>✦</b><span>Websites &amp; Web Apps</span><b>✦</b><span>Design Strategy</span><b>✦</b><span>Graphic Design</span><b>✦</b></div></div>
</section>'''

FACTS = '''<div class="facts rv" style="--d:.3s"><div><b data-count="30" data-suffix="+">30+</b><span>projects designed</span></div><div><b data-count="3">3</b><span>countries</span></div><div><b data-count="4">4</b><span>years</span></div><div><b data-count="2">2</b><span>apps on the App Store</span></div></div>'''

SERVICES = [('Strategy', 'Product design strategy', 'User-focused strategy rooted in research and aligned with business goals.'),
            ('Interfaces', 'Web & app design', 'Concept to high-fidelity design for web, iPhone and Android.'),
            ('Usability', 'UI/UX optimisation', 'Engaging, accessible interfaces that perform better.'),
            ('Identity', 'Brand identity', 'Logos and visual systems that give a product its voice.'),
            ('Apps', 'App development', 'iPhone, Android and web apps designed and built end to end, like Xpense and Tockbee.'),
            ('Building', 'AI-assisted development', 'Designs turned into working front ends and apps, reviewed and refined by me.')]


def steps_html():
    return ''.join(f'''<section class="stage{' flip' if i % 2 else ''}" data-dots="{key}" aria-labelledby="st-{i}">
  <div class="wrap">
    <div class="copy">{k(f'0{i + 1} / 05', 'How I work')}<h2 id="st-{i}" class="rv" style="--d:.05s">{t}</h2><p class="lead rv" style="--d:.1s">{d}</p></div>
    <div class="art" data-art aria-hidden="true"></div>
  </div>
</section>''' for i, (key, t, d) in enumerate(STEPS))


def tiles(items):
    return '<div class="grid3">' + ''.join(f'<article class="tile rv" style="--d:{i * .05:.2f}s"><p class="kicker">{a}</p><h3>{b}</h3><p>{c}</p></article>' for i, (a, b, c) in enumerate(items)) + '</div>'


home = f'''<section class="stage hero" data-dots="n" aria-labelledby="h1">
  <div class="wrap">
    <div class="copy">
      <p class="me-chip rv">{img('me/portrait.webp', 'Portrait of Nagules Gobi', lazy=False)}<span>Hi, I’m <b>Nagules Gobi</b>. Product designer who builds websites and apps too. Director of dotXline LTD.</span></p>
      <h1 id="h1" class="rv" style="--d:.05s"><span class="ln">Products,</span> <span class="ln">designed</span> <span class="ln">and built</span> <span class="ln ac">end to end.</span></h1>
      <p class="lead rv" style="--d:.12s">Websites, web apps and mobile apps, from first sketch to working code in SwiftUI, React Native and AI-assisted development.</p>
      <div class="btns rv" style="--d:.2s"><a class="btn btn-solid" href="work.html">See the work</a><a class="btn btn-line" href="contact.html">Hire me</a></div>
      {FACTS}
    </div>
    <div class="art" data-art aria-hidden="true"></div>
  </div>
</section>
{MARQUEE}
<section class="section" id="process" data-dots="off" aria-labelledby="process-h">
  <div class="wrap head"><div>{k('', 'How I work')}<h2 id="process-h" class="rv">From first question to working product.</h2></div><p class="rv">The same five steps on every project. Timelines depend on the size of the work, and I share one after our first call.</p></div>
</section>
{steps_html()}
<section class="section" id="apps" data-dots="off" aria-labelledby="apps-h">
  <div class="wrap head"><div>{k('', 'My apps · dotXline LTD')}<h2 id="apps-h" class="rv">Designed by me. Built by me.</h2></div><p class="rv">Xpense, Tockbee and FreshBit are the apps of dotXline LTD, my product company in Cardiff. I designed every screen and built all three. Two are live on the App Store, one is in testing.</p></div>
</section>
{''.join(app_stage(a, i) for i, a in enumerate(APPS))}
<section class="section" id="work" data-dots="off" aria-labelledby="work-h">
  <div class="wrap">
    <div class="head"><div>{k('', 'Client work')}<h2 id="work-h" class="rv">Products I designed for teams.</h2></div><p class="rv">Web, mobile and brand work for companies across three countries.</p></div>
    {rows()}
    <div class="btns rv" style="margin-top:var(--s5)"><a class="btn btn-line" href="work.html">All work and brand</a></div>
  </div>
</section>
<section class="section" data-dots="off" aria-labelledby="svc-h">
  <div class="wrap">
    <div class="head"><div>{k('', 'What I do')}<h2 id="svc-h" class="rv">What you get when you hire me.</h2></div><p class="rv">Clean interfaces that catch the eye and guide users without effort.</p></div>
    {tiles(SERVICES)}
  </div>
</section>
<section class="stage" data-dots="hello" aria-labelledby="hi-h">
  <div class="wrap">
    <div class="copy">{k('', 'Available now')}<h2 id="hi-h" class="rv" style="--d:.05s">Let’s work together.</h2><p class="lead rv" style="--d:.1s">Hiring for a product design role, or need a designer for a project? Tell me a little about it and I’ll get back to you.</p>
      <div class="btns rv" style="--d:.15s"><a class="btn btn-solid" href="contact.html">Start a conversation</a><a class="btn btn-line" href="mailto:nagulesgobi@dotxline.com">Email me</a></div></div>
    <div class="art" data-art data-wide aria-hidden="true"></div>
  </div>
</section>'''

# ------------------------------------------------------------------ work
# Not the home page again: one pinned dot drawing on the left, a scrolling index of projects on the right.
# As each project reaches the middle of the screen, the drawing rebuilds itself as that project's mark.
WORK = [(s2, t, kd, d, f'brand/board-{s2}.webp', st) for (s2, _c, _sh, t, kd, _l, d, _tg, st, _x) in APPS] + \
       [(s2, t, kd, d, p, '') for s2, t, kd, d, p in CLIENT]
WORK = [w if w[0] != 'greenlife' else w[:4] + ('GL', '') for w in WORK]  # a clean 4:3 crop of the cover, without the strip of screens


def wl_row(w, i):
    sl, t, kd, d, p, st = w
    who = 'My app · dotXline' if i < 3 else 'Client project'
    badge = f'<span class="status{" test" if "Test" in st else ""}">{st}</span>' if st else ''
    return f"""<li class="wl-row" id="{sl}" data-dots="{sl}" data-art-ref="#wl-art" data-name="{t}">
  <a href="work/{sl}.html">
    <p class="wl-meta mono"><span class="n">0{i + 1}</span><span>{who}</span>{badge}</p>
    <h2>{t}</h2>
    <p class="wl-kind mono">{kd.split(' · ')[0]}</p>
    <p class="wl-desc">{d}</p>
    <figure class="shot">{'<img src="' + M + 'gl-cover.webp" alt="Greenlife cover" width="960" height="720" loading="lazy" decoding="async">' if p == 'GL' else img(p, t + (' brand board' if i < 3 else ' cover'))}</figure>
    <span class="link"><span>Read the case study</span><i aria-hidden="true">→</i></span>
  </a>
</li>"""


gal = ''.join(f'''<button type="button" class="rv" data-cat="{cat}" data-full="{A}brand/{key}.webp" data-title="{t}" data-sub="{sub}"><figure>{img('brand/' + key + '.webp', t, key='brand/' + key if 'brand/' + key in SIZES else 'logo/' + key.replace('logo-', ''))}</figure><span class="cap"><b>{t}</b><span>{sub}</span></span></button>''' for key, t, sub, cat in GALLERY)

work = f'''<section class="worklist" aria-labelledby="h1">
  <div class="wrap wl">
    <div class="wl-pin" aria-hidden="true">
      <div class="art" id="wl-art"></div>
      <p class="wl-now mono"><span class="n" data-wl-n>00 / 07</span><span data-wl-name>Selected work</span></p>
    </div>
    <div class="wl-list">
      <header class="wl-intro" data-dots="tiles" data-art-ref="#wl-art">
        <p class="kicker rv">Work · 2019 to now</p>
        <h1 id="h1" class="rv" style="--d:.05s">Selected <span class="ac">work.</span></h1>
        <p class="lead rv" style="--d:.12s">Two kinds of work on one page: the products and apps I design and build, and the brands, campaigns and print I give a visual voice.</p>
        <ul class="wl-jump rv" style="--d:.2s">{''.join(f'<li><a href="#{w[0]}"><span class="mono">0{i + 1}</span>{w[1]}</a></li>' for i, w in enumerate(WORK))}<li><a href="#brand"><span class="mono">+</span>Brand and print</a></li></ul>
      </header>
      <ol class="wl-rows">{''.join(wl_row(w, i) for i, w in enumerate(WORK))}</ol>
    </div>
  </div>
</section>
<section class="section" id="brand" data-dots="off" aria-labelledby="bw-h">
  <div class="wrap">
    <div class="head"><div>{k('02', 'Brand and print')}<h2 id="bw-h" class="rv">Every pixel shaped with purpose.</h2></div><p class="rv">Logos, campaigns, print and packaging that help businesses stand out. {len(GALLERY)} pieces. Select any of them to view it full screen.</p></div>
    <div class="filters rv" role="group" aria-label="Filter brand work" data-filter-group="#gallery"><button type="button" data-filter="all" aria-pressed="true">All</button><button type="button" data-filter="identity" aria-pressed="false">Logos and identity</button><button type="button" data-filter="campaign" aria-pressed="false">Campaigns</button><button type="button" data-filter="print" aria-pressed="false">Print</button><button type="button" data-filter="packaging" aria-pressed="false">Packaging</button></div>
    <div class="gallery" id="gallery">{gal}</div>
  </div>
</section>
<dialog class="lightbox" aria-label="Brand work, full screen"><button class="close" type="button" aria-label="Close">×</button><img alt=""><p></p></dialog>'''

# ------------------------------------------------------------------ about
# Not the home page again: my story, then what went wrong and how I fixed it, then how I work as one timeline.
# The fixes are the ones recorded in the FreshBit case study (TestFlight testing on a real iPhone).
# Every story comes from a real fix: the FreshBit case study, and the commit history of the Xpense and Tockbee apps.
MOTION_VIS = '<div class="fx-vis fx-motion" aria-hidden="true"><span class="fx-col"><span class="fx-bar"></span><small>Custom bounce</small></span><span class="fx-col"><span class="fx-bar"></span><small>Native morph</small></span></div>'
CONTRAST_VIS = '<div class="fx-vis fx-contrast" aria-hidden="true"><span class="bad">Today<small>1.2:1</small></span><span class="good">Today<small>6.5:1</small></span></div>'
APP_ICON = {'Xpense': A + 'apps/xpense-icon.webp', 'Tockbee': A + 'apps/tockbee-icon.webp', 'FreshBit': A + 'kit/fb2-icon-light.webp'}
CAT = {'ux': 'User experience', 'ui': 'User interface', 'product': 'Product'}
FIXES = [
  ('ux', 'Xpense', 'The budget that never saved.',
   'The monthly budget used the decimal keypad, which has no Done key, and leaving Settings didn’t end the edit. The limit people typed was never saved.',
   'The budget now saves as you type, so there’s nothing to confirm and nothing to lose.', ''),
  ('ux', 'Tockbee', 'Face ID at the wrong moment.',
   'Location events open Tockbee in the background, unseen, and every one of those launches asked for Face ID.',
   'Face ID now asks only when you open the app yourself.', ''),
  ('ux', 'Xpense', 'Sign-in codes that didn’t fit.',
   'Email sign-in only took codes of one length, so a longer code from the email couldn’t be entered.',
   'It now accepts codes of 6 to 8 digits.', ''),
  ('ui', 'FreshBit', 'Lime text you could hardly read.',
   'The selected tab on the light tab bar was lime on a light background: about 1.2:1.',
   'Lime became a fill only, always with black text, and electric violet carries text on light backgrounds, 6.5:1. My rule since: never lime for text on a light background.', CONTRAST_VIS),
  ('ui', 'FreshBit', 'A header that felt custom, not native.',
   'The folding header used a custom bouncing animation I had made.',
   'I replaced it with Apple’s Liquid Glass morph, so it feels like part of the system.', MOTION_VIS),
  ('ui', 'Xpense', 'Custom glass effects on every screen.',
   'Xpense had its own glare and reflection effects layered across the interface.',
   'I removed them, rebuilt the forms as native SwiftUI, kept glass to the controls only, and respected Reduce Transparency.', ''),
  ('ui', 'Xpense', 'A blank flash at launch.',
   'Opening the app flashed a blank screen while it checked who was signed in.',
   'A branded splash, matching the app icon in light and dark, now stays up until sign-in is known.', ''),
  ('product', 'Tockbee', 'Asking before every clock-in.',
   'Arriving at work by location or Wi-Fi brought a question before Tockbee would clock you in.',
   'It now clocks you in and out automatically and sends a notification with Undo: fast by default, easy to reverse.', ''),
  ('product', 'Tockbee', 'Hours that went missing.',
   'Some genuine departures were dropped as repeats, and an old Undo could block the next day. For a pay tracker, a missed shift is missed money.',
   'Departures are no longer dropped, an old Undo no longer blocks the next day, sites are watched at 200 m or more, and the app checks your position when it opens to catch anything missed.', ''),
]

fixes = ''.join(f"""<li class="fx" data-cat="{cat}">
  <p class="fx-n mono"><span class="n">{i + 1:02d}</span><span>{CAT[cat]}</span><span class="fx-app"><img src="{APP_ICON[app]}" alt="" width="20" height="20" loading="lazy">{app}</span></p>
  <h3>{t}</h3>
  {vis}
  <div class="fx-pair"><div><p class="mono">What went wrong</p><p>{bad}</p></div><div><p class="mono">How I made it right</p><p>{good}</p></div></div>
</li>""" for i, (cat, app, t, bad, good, vis) in enumerate(FIXES))

process = ''.join(f'<li><span class="mono">0{i + 1}</span><b>{t}</b><p>{d}</p></li>' for i, (_, t, d) in enumerate(STEPS))

about = f'''<section class="stage hero" data-dots="portrait" aria-labelledby="h1">
  <div class="wrap">
    <div class="copy">
      <p class="kicker rv">About</p>
      <h1 id="h1" class="rv" style="--d:.05s">Designer. Director. <span class="ac">Builder.</span></h1>
      <p class="lead rv" style="--d:.12s">I design products people actually enjoy using, and I build my own.</p>
      <div class="btns rv" style="--d:.2s"><a class="btn btn-solid" href="#story">My story</a><a class="btn btn-line" href="contact.html">Hire me</a></div>
    </div>
    <div class="art" data-art role="img" aria-label="Portrait of Nagules Gobi, drawn in dots"></div>
  </div>
</section>
<section class="section" id="story" data-dots="off" aria-labelledby="story-h">
  <div class="wrap story">
    <figure class="story-photo rv">{img('me/portrait.webp', 'Nagules Gobi')}<figcaption class="mono"><span>Gobikrishna Naguleswararajah</span><span>Nagules Gobi</span></figcaption></figure>
    <div>
      {k('', 'My story')}<h2 id="story-h" class="rv">Hi, I’m Nagules.</h2>
      <div class="prose" style="margin-top:var(--s4)">
        <p class="rv">I’m a product designer in the United Kingdom working across UX/UI, web and app design, and brand identity. Over four years I’ve designed <strong>30+ projects across 3 countries</strong>, from ad-tech platforms and health apps to shopping apps and logos.</p>
        <p class="rv">I’m also <strong>Director of dotXline LTD</strong>, a product company in Cardiff. There I design and build Xpense, a calm iPhone expense tracker, and Tockbee, a shift and pay tracker for UK workers. Owning products end to end taught me to design for the people using them and for the team that has to build them.</p>
        <p class="rv">I studied for a BSc in Computing, and today I also build what I design. I use AI-assisted development to turn designs into working products quickly, then review and refine the code myself. It means I can prototype in code, test ideas with real users sooner, and talk to engineering teams in their own language.</p>
      </div>
      <dl class="deflist rv" style="margin-top:var(--s5)"><dt>Role</dt><dd>Product designer who builds</dd><dt>Company</dt><dd>Director, dotXline LTD</dd><dt>Education</dt><dd>BSc in Computing</dd><dt>Experience</dt><dd>4 years · 30+ projects designed</dd><dt>Open to</dt><dd>Roles and freelance</dd></dl>
    </div>
  </div>
</section>
<section class="section fixes" data-dots="off" aria-labelledby="fx-h">
  <div class="wrap">
    <div class="head">
      <div>{k('', 'What went wrong, and how I fixed it')}<h2 id="fx-h" class="rv">I test my own work until it’s right.</h2></div>
      <p class="rv">Real problems from Xpense, Tockbee and FreshBit, the apps I design and build at dotXline, and what I changed. I review recordings of real use on an iPhone and fix things build by build: FreshBit alone went through <strong>11 TestFlight builds</strong>.</p>
    </div>
    <div class="filters rv" role="group" aria-label="Filter the fixes" data-filter-group="#fx-list"><button type="button" data-filter="all" aria-pressed="true">All · {len(FIXES)}</button>{''.join(f'<button type="button" data-filter="{c}" aria-pressed="false">{n} · {sum(1 for f in FIXES if f[0] == c)}</button>' for c, n in CAT.items())}</div>
    <ol class="fx-list" id="fx-list">{fixes}</ol>
    <p class="rv fx-more"><a class="link" href="work/xpense.html"><span>Xpense case study</span><i aria-hidden="true">→</i></a><a class="link" href="work/tockbee.html"><span>Tockbee case study</span><i aria-hidden="true">→</i></a><a class="link" href="work/freshbit.html"><span>FreshBit case study</span><i aria-hidden="true">→</i></a></p>
  </div>
</section>
<section class="section process-sec" data-dots="off" aria-labelledby="how-h">
  <div class="wrap">
    <div class="head"><div>{k('', 'How I work')}<h2 id="how-h" class="rv">From first question to working product.</h2></div><p class="rv">The same five steps on every project. Timelines depend on the size of the work, and I share one after our first call.</p></div>
    <ol class="process" data-process>{process}</ol>
    <div class="btns rv" style="margin-top:var(--s6)"><a class="btn btn-solid" href="contact.html">Start a conversation</a><a class="btn btn-line" href="work.html">See the work</a></div>
  </div>
</section>'''

# ------------------------------------------------------------------ contact
CHIPS = ['Full-time role', 'Freelance project', 'App design', 'Website', 'Brand identity', 'Design and build']
FAQ = [('Can you guarantee improvements in conversions?', 'No designer can honestly guarantee a number. What I can promise is a process built on research, clear goals and testing, so every design decision is aimed at making your product easier to use and easier to say yes to.'),
       ('How much does it cost to design one web page?', 'It depends on scope: the content, the number of states and breakpoints, and whether you need a design system behind it. Tell me about your project and I’ll send a clear quote.'),
       ('What’s your process like, and how long does it take?', 'Discovery and research, then wireframes, UI design, an interactive prototype and a clean handoff to development. Timelines depend on the size of the project, and I’ll share one after our first call.'),
       ('Can you build what you design?', 'Yes. Alongside design, I build with code and AI-assisted development: interactive prototypes, front ends and full apps like Xpense and Tockbee at dotXline. For larger products I work with your engineers and hand over clean specs.'),
       ('Are you open to full-time roles?', 'Yes. I’m open to product design roles as well as freelance projects. Send me the details and let’s talk.')]
contact = f'''<section class="stage hero" data-dots="at" aria-labelledby="h1">
  <div class="wrap">
    <div class="copy">
      <p class="kicker rv"><span class="status">Available now</span></p>
      <h1 id="h1" class="rv" style="--d:.05s">Let’s work <span class="ac">together.</span></h1>
      <p class="lead rv" style="--d:.12s">Hiring for a product design role, or need a designer for a project? Tell me a little about it and I’ll get back to you.</p>
      <div class="btns rv" style="--d:.2s"><a class="btn btn-solid" href="#write">Write to me</a><button class="btn btn-line" type="button" data-copy="nagulesgobi@dotxline.com">Copy email</button></div>
    </div>
    <div class="art" data-art aria-hidden="true"></div>
  </div>
</section>
<section class="section" id="write" data-dots="off" aria-labelledby="form-h">
  <div class="wrap head" style="align-items:start">
    <div>{k('', 'Message')}<h2 id="form-h" class="rv">Tell me about it.</h2>
      <div class="prose rv" style="margin-top:var(--s4)"><p>Or email me directly at <a href="mailto:nagulesgobi@dotxline.com"><strong>nagulesgobi@dotxline.com</strong></a>.</p><p>Helpful to include: the role or project, your timeline, and a link to the product if there is one.</p><p>London time <strong data-clock>--:--</strong></p></div></div>
    <form class="form rv" data-mailform novalidate>
      <fieldset><legend>I’m looking for</legend><div class="chips">{''.join(f'<button type="button" aria-pressed="false">{c}</button>' for c in CHIPS)}</div></fieldset>
      <div class="two"><div class="field"><label for="f-name">Your name</label><input id="f-name" name="name" autocomplete="name" required></div><div class="field"><label for="f-email">Your email</label><input id="f-email" name="email" type="email" autocomplete="email" required></div></div>
      <div class="field"><label for="f-co">Company <span style="text-transform:none;letter-spacing:0">(optional)</span></label><input id="f-co" name="company" autocomplete="organization"></div>
      <div class="field"><label for="f-msg">Message</label><textarea id="f-msg" name="message" required></textarea></div>
      <p class="error" data-err role="alert"></p>
      <div class="btns"><button class="btn btn-solid" type="submit">Write the email</button></div>
      <p class="hint">This opens your mail app with the message ready to send. Nothing is stored here.</p>
    </form>
  </div>
</section>
<section class="stage flip faq-stage" data-dots="ask" aria-labelledby="faq-h">
  <div class="wrap">
    <div class="art" data-art aria-hidden="true"></div>
    <div class="copy">{k('', 'FAQ')}<h2 id="faq-h" class="rv">Questions, answered.</h2>
    <div class="faq rv" style="margin-top:var(--s4)">{''.join(f'<details><summary>{q}<i aria-hidden="true">+</i></summary><p>{a}</p></details>' for q, a in FAQ)}</div></div>
  </div>
</section>'''

# ------------------------------------------------------------------ dotxline
METHOD = [('zero', '0', 'Who we are.', 'A small product company in Cardiff. Every app starts as a blank page and one small, exact idea.'),
          ('times', '×', 'Where this meets that.', 'We look for the point where an everyday problem meets a simple answer: what you spent, the hours you worked, what you’re owed.'),
          ('one', '1', 'Then we finish it.', 'One app at a time, built natively and kept simple, until it does its job without fuss.')]
HABITS = [('Clear.', 'We say the number.', '“£3.40 logged to Food.” Plain words, specific amounts, no guessing.'),
          ('Calm.', 'Quiet interfaces', 'They stay out of your way and respect your attention. No guilt, no alarms.'),
          ('Private.', 'As little as possible.', 'No ads. No selling your data. Xpense keeps receipt photos on your iPhone and Tockbee collects no data at all.')]
dx = f'''<section class="stage hero" data-dots="dotx" aria-labelledby="h1">
  <div class="wrap">
    <div class="copy">
      <p class="kicker rv">My company · Director</p>
      <h1 id="h1" class="rv" style="--d:.05s">Small, exact apps that <span class="ac">just work.</span></h1>
      <p class="lead rv" style="--d:.12s">dotXline LTD is a product company in Cardiff. We make everyday money and work feel simple, one carefully built app at a time. As Director, I lead the product and design every screen.</p>
      <dl class="deflist rv" style="--d:.2s;margin-top:var(--s5)"><dt>Role</dt><dd>Director</dd><dt>Based in</dt><dd>Cardiff, United Kingdom</dd><dt>Apps</dt><dd>Xpense, Tockbee, FreshBit</dd></dl>
    </div>
    <div class="art" data-art role="img" aria-label="The dotXline mark, drawn in dots"></div>
  </div>
</section>
<section class="section" data-dots="off" aria-labelledby="m-h"><div class="wrap head"><div>{k('', 'The name is the method')}<h2 id="m-h" class="rv">We build from zero to one.</h2></div></div></section>
{''.join(f"""<section class="stage{' flip' if i % 2 else ''}" data-dots="{key}" aria-labelledby="m-{i}">
  <div class="wrap"><div class="copy">{k(sym, 'The method')}<h2 id="m-{i}" class="rv" style="--d:.05s">{t}</h2><p class="lead rv" style="--d:.1s">{d}</p></div><div class="art" data-art aria-hidden="true"></div></div>
</section>""" for i, (key, sym, t, d) in enumerate(METHOD))}
{''.join(app_stage(a, i) for i, a in enumerate(APPS))}
<section class="section" data-dots="off" aria-labelledby="hab-h">
  <div class="wrap">
    <div class="head"><div>{k('', 'How we work')}<h2 id="hab-h" class="rv">Three habits, in every app.</h2></div></div>
    {tiles(HABITS)}
    <div class="btns rv" style="margin-top:var(--s5)"><a class="btn btn-solid" href="https://dotxline.com" target="_blank" rel="noopener">Visit dotxline.com ↗</a></div>
  </div>
</section>'''

PAGE_META = [('index.html', 'Nagules Gobi · UX/UI Designer and App Developer', 'Nagules Gobi is a UK UX/UI designer who designs and builds his own apps, Xpense, Tockbee and FreshBit, and Director of dotXline LTD.', home, True),
             ('work.html', 'Work · Nagules Gobi', 'Product and app case studies, plus logos, identities, campaigns and print design by Nagules Gobi.', work, False),
             ('about.html', 'About · Nagules Gobi', 'About Nagules Gobi: product designer, Director of dotXline LTD, BSc in Computing.', about, False),
             ('contact.html', 'Contact · Nagules Gobi', 'Hire Nagules Gobi for a product design role or project.', contact, False),
             ('dotxline.html', 'dotXline · Nagules Gobi', 'Nagules Gobi is Director of dotXline LTD, a Cardiff product company that makes Xpense, Tockbee and FreshBit.', dx, False)]


def build(out=OUT):
    for f, t, d, b, intro in PAGE_META:
        open(os.path.join(out, f), 'w').write(page(f, t, d, b, intro))


if __name__ == '__main__':
    build()
    print('wrote', [m[0] for m in PAGE_META])

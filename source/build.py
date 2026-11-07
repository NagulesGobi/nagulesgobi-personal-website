#!/usr/bin/env python3
"""Builds the multi-page Nagules Gobi portfolio into ./out from shared partials.
Content comes only from nagulesgobi.com and dotxline.com."""
import json, os, re, html, shutil
import kit

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, '..'))  # the website is published from the repository root
SIZES = json.load(open(os.path.join(HERE, 'img-sizes.json')))
PARTS = open(os.path.join(HERE, 'parts', 'site-parts.txt')).read().split('\n')
LOGO_VB, MARK60, WORD_D, MARK100 = PARTS
WM = open(os.path.join(HERE, 'parts', 'wordmark-big.txt')).read()
WM_W, WM_D = WM.split('|', 1)
STOPS = '<stop offset="0" stop-color="#FF9124"/><stop offset=".3" stop-color="#FF4A2C"/><stop offset=".55" stop-color="#FF2440"/><stop offset="1" stop-color="#FF008E"/>'
EMAIL = 'contact@nagulesgobi.com'
E = html.escape

# Cache-busting version: a short hash of the CSS and JS, so browsers fetch fresh files after every change
import hashlib
ASSET_V = hashlib.sha1(b''.join(open(os.path.join(HERE, 'assets', f), 'rb').read() for f in ('css/base.css', 'css/pages.css', 'js/site.js'))).hexdigest()[:8]

def img(path, alt, root, cls='', lazy=True, extra=''):
    key = path.replace('.webp', '')
    w, h = SIZES.get(key, [1200, 900])
    return (f'<img src="{root}assets/img/{path}" alt="{E(alt)}" width="{w}" height="{h}"'
            f'{" loading=\"lazy\"" if lazy else ""} decoding="async"{f" class=\"{cls}\"" if cls else ""}{extra}>')

# ------------------------------------------------------------------ partials
NAV = [('work.html', 'Work'), ('dotxline.html', 'dotXline'), ('about.html', 'About'), ('contact.html', 'Contact')]

def logo_svg():
    return (f'<svg class="logo-svg" viewBox="{LOGO_VB}" role="img" aria-label="Nagules Gobi"><defs><radialGradient id="ngg" gradientUnits="userSpaceOnUse" cx="0" cy="0" r="87">{STOPS}</radialGradient></defs>'
            f'<path fill="url(#ngg)" d="{MARK60}"/><path class="wm" d="{WORD_D}"/></svg>')

def head(title, desc, root, intro=False, canonical=''):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<script{' data-intro="1"' if intro else ''}>
  (function () {{
    var d = document.documentElement, s = document.currentScript; d.classList.add('js');
    try {{
      var t = localStorage.getItem('ng-theme'); if (t === 'light' || t === 'dark') d.dataset.theme = t;
      var rm = matchMedia('(prefers-reduced-motion: reduce)').matches, nav = sessionStorage.getItem('ng-nav');
      if (nav && !rm) {{ d.classList.add('arriving'); d.dataset.navLabel = nav; sessionStorage.removeItem('ng-nav'); sessionStorage.setItem('ng-intro', '1'); }}
      if (s.dataset.intro && !rm && !sessionStorage.getItem('ng-intro')) d.classList.add('intro');
    }} catch (e) {{}}
  }})();
</script>
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:type" content="website">
<meta property="og:image" content="https://www.nagulesgobi.com/assets/brand/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#F3EFE7" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#12110F" media="(prefers-color-scheme: dark)">
<link rel="canonical" href="https://www.nagulesgobi.com/{canonical}">
<link rel="icon" href="{root}favicon.ico" sizes="48x48">
<link rel="icon" href="{root}favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{root}apple-touch-icon.png">
<link rel="manifest" href="{root}site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Semi+Condensed:wght@500;600;700&family=Barlow:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}assets/css/base.css?v={ASSET_V}">
<link rel="stylesheet" href="{root}assets/css/pages.css?v={ASSET_V}">
<script src="{root}assets/js/site.js?v={ASSET_V}" defer></script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
'''

DOCK_ICONS = {
    'index.html': 'M3 11l9-7 9 7v9a1 1 0 0 1-1 1h-5v-6h-6v6H4a1 1 0 0 1-1-1z',
    'work.html': 'M4 7h16v13H4zM9 7V4h6v3M4 12h16',
    'dotxline.html': 'DXMARK',
    'about.html': 'M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM4 21c1-4 4-6 8-6s7 2 8 6',
    'contact.html': 'M3 6h18v12H3zM3 7l9 6 9-6',
    'search': 'M11 18a7 7 0 1 0 0-14 7 7 0 0 0 0 14zM21 21l-5-5',
}
THEME_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle class="sun" cx="12" cy="12" r="5"/><g class="rays"><path d="M12 1.5v2.2M12 20.3v2.2M1.5 12h2.2M20.3 12h2.2M4.6 4.6l1.6 1.6M17.8 17.8l1.6 1.6M4.6 19.4l1.6-1.6M17.8 6.2l1.6-1.6"/></g><circle class="moon-cut" cx="17" cy="7" r="5"/></svg>'

DX_MARK = ('<svg class="dk-dx" viewBox="0.37 0.37 87.31 87.31" aria-hidden="true"><path transform="translate(0 1.025)" '
           'd="M63.44 36.56 L38.69 61.31 A16 16 0 1 1 38.69 38.69 L61.31 61.31 A9 9 0 0 0 76.68 54.95 L76.68 20.00" '
           'fill="none" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/></svg>')

def dock_icon(key):
    if DOCK_ICONS[key] == 'DXMARK': return DX_MARK  # the real dotXline mark, from the dotXline brand kit
    return f'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="{DOCK_ICONS[key]}"/></svg>'

def finder_items(root):
    items = [('Pages', 'Home', 'Shipped apps, client work and how I build', 'index.html'),
             ('Pages', 'Work', 'Product case studies, brand and print', 'work.html'),
             ('Pages', 'Brand and print', '29 logos, campaigns, print and packaging pieces', 'work.html#brand'),
             ('Pages', 'dotXline', 'My product company in Cardiff', 'dotxline.html'),
             ('Pages', 'About', 'Story, process and capabilities', 'about.html'),
             ('Pages', 'Contact', 'Hire me for a role or a project', 'contact.html')]
    items += [('Case studies', p['title'], p['kind'], f"work/{p['slug']}.html") for p in PROJECTS]
    items += [('On the home page', 'Try Xpense', 'Working demo: tap a tile to log an expense', 'index.html#xpense'),
              ('On the home page', 'Try Tockbee', 'Working demo: a live shift timer', 'index.html#tockbee'),
              ('On the home page', 'How I build', 'Design, develop, refine, launch', 'index.html#build')]
    out, last = '', None
    for g, t, sub, h in items:
        if g != last: out += f'<li class="fd-group" role="presentation">{g}</li>'; last = g
        out += f'<li role="option"><a href="{root}{h}" data-label="{E(t)}" data-text="{E((t + " " + sub + " " + g).lower())}"><b>{E(t)}</b><span>{E(sub)}</span><i aria-hidden="true">↵</i></a></li>'
    out += f'<li class="fd-group" role="presentation">Actions</li><li role="option"><a href="mailto:{EMAIL}" data-text="email contact hire mail {EMAIL}"><b>Email me</b><span>{EMAIL}</span><i aria-hidden="true">↵</i></a></li>'
    out += '<li role="option"><button type="button" data-theme-toggle data-text="theme dark light mode switch"><b>Switch theme</b><span>Light or dark</span><i aria-hidden="true">↵</i></button></li>'
    return out

def chrome(root, active):
    def item(h, t):
        cur = ' aria-current="page"' if h == active else ''
        return f'<a class="dk-item" href="{root}{h}"{cur} data-label="{t}" aria-label="{t}"><span class="dk-tile">{dock_icon(h)}</span><span class="dk-tip">{t}</span></a>'
    items = ''.join(item(h, t) for h, t in NAV)
    return f"""<div class="curtain" aria-hidden="true"><span class="curtain-label"></span></div>
<div class="progress" aria-hidden="true"><i></i></div>
<div class="grain" aria-hidden="true"></div>
<div class="cursor" aria-hidden="true"><div class="cursor-preview"></div><div class="cursor-ring"><span class="cursor-label"></span></div><div class="cursor-dot"></div></div>
<header class="dock-wrap">
  <nav class="dock" aria-label="Main" data-dock>
    <a class="dk-item dk-mark" href="{root}index.html"{' aria-current="page"' if active == 'index.html' else ''} aria-label="Nagules Gobi, home" data-label="Home"><span class="dk-tile"><svg viewBox="0 0 100 100" aria-hidden="true"><defs><radialGradient id="dkg" gradientUnits="userSpaceOnUse" cx="15" cy="8" r="113">{STOPS}</radialGradient></defs><path fill="url(#dkg)" d="{MARK100}"/></svg></span><span class="dk-tip">Home</span></a>
    <i class="dk-sep" aria-hidden="true"></i>
    {items}
    <i class="dk-sep" aria-hidden="true"></i>
    <button class="dk-item" type="button" data-finder-open aria-label="Search the site (Command K)" aria-haspopup="dialog"><span class="dk-tile">{dock_icon('search')}</span><span class="dk-tip">Search <kbd>⌘K</kbd></span></button>
    <button class="dk-item theme-btn" type="button" aria-label="Switch between light and dark theme"><span class="dk-tile">{THEME_SVG}</span><span class="dk-tip">Theme</span></button>
    <a class="dk-hire" href="{root}contact.html" data-label="Contact"><span class="pulse" aria-hidden="true"></span>Hire me</a>
  </nav>
</header>
<div class="finder" role="dialog" aria-modal="true" aria-label="Search the site" hidden>
  <div class="fd-backdrop" data-finder-close></div>
  <div class="fd-panel">
    <label class="fd-field"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="{DOCK_ICONS['search']}"/></svg><input type="text" placeholder="Search pages, case studies and demos" autocomplete="off" spellcheck="false" aria-label="Search" aria-controls="fd-list"><kbd>Esc</kbd></label>
    <ul class="fd-list" id="fd-list" role="listbox">{finder_items(root)}</ul>
    <p class="fd-empty" hidden>Nothing matches. Try “app”, “brand” or “contact”.</p>
    <div class="fd-foot mono"><span>↑ ↓ to move</span><span>↵ to open</span><span>⌘K or / to search</span></div>
  </div>
</div>
"""

def footer(root, cta='Have a product people should love? Let’s build it.'):
    return f'''<section class="foot-cta">
  <div class="wrap">
    <div class="foot-cta-grid">
      <div>
        <p class="kicker" data-reveal>Available for product design roles and freelance projects</p>
        <h2 data-split>{E(cta)}</h2>
        <a class="mail" href="mailto:{EMAIL}" data-reveal><span data-text="{EMAIL}">{EMAIL}</span></a>
      </div>
      <a class="orb" href="{root}contact.html" data-magnetic aria-label="Hire me" data-label="Contact">
        <svg class="orb-ring" viewBox="0 0 200 200" aria-hidden="true"><defs><path id="orb-c" d="M100 100m-78 0a78 78 0 1 1 156 0a78 78 0 1 1-156 0"/></defs><text><textPath href="#orb-c" textLength="488" lengthAdjust="spacing">HIRE ME · LET'S TALK · HIRE ME · LET'S TALK · </textPath></text></svg>
        <span class="orb-core"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17 17 7M8 7h9v9"/></svg></span>
      </a>
    </div>
  </div>
</section>
<footer class="foot">
  <div class="wrap">
    <svg class="giant" viewBox="-4 -4 {int(WM_W) + 8} 112" aria-hidden="true"><defs><linearGradient id="gw" x1="0" x2="1"><stop offset="0" stop-color="#FF9124"/><stop offset=".35" stop-color="#FF4A2C"/><stop offset=".6" stop-color="#FF2440"/><stop offset="1" stop-color="#FF008E"/></linearGradient></defs><path d="{WM_D}"/></svg>
    <div class="foot-cols">
      <div><h4>Pages</h4><ul>{''.join(f'<li><a href="{root}{h}">{t}</a></li>' for h, t in [('index.html', 'Home')] + NAV)}</ul></div>
      <div><h4>Case studies</h4><ul>{''.join(f'<li><a href="{root}work/{p["slug"]}.html">{p["title"]}</a></li>' for p in PROJECTS)}</ul></div>
      <div><h4>Elsewhere</h4><ul><li><a href="https://dotxline.com" target="_blank" rel="noopener">dotxline.com ↗</a></li><li><a href="https://www.behance.net/gallery/224174429/Chatvertiser" target="_blank" rel="noopener">Behance ↗</a></li><li><a href="mailto:{EMAIL}">Email</a></li><li><span>London <time data-clock>--:--</time></span></li></ul></div>
    </div>
    <div class="foot-row">
      <p>© <span data-year>2026</span> Nagules Gobi · Product designer, United Kingdom</p>
      <p><a href="#top">Back to top ↑</a></p>
    </div>
  </div>
</footer>
'''

def page(path, title, desc, active, body, intro=False, lightbox=False, cta=None):
    root = '../' * path.count('/')
    lb = '''<div class="lightbox" role="dialog" aria-modal="true" aria-label="Image viewer" hidden>
  <div class="lb-bar"><span class="lb-count">01 / 01</span><button class="lb-btn lb-close" type="button" aria-label="Close">✕</button></div>
  <div class="lb-stage"><img class="lb-img" alt=""></div>
  <div class="lb-foot"><div class="lb-cap"></div><div class="lb-nav"><button class="lb-btn lb-prev" type="button" aria-label="Previous image">←</button><button class="lb-btn lb-next" type="button" aria-label="Next image">→</button></div></div>
</div>''' if lightbox else ''
    canonical = '' if path == 'index.html' else path
    doc = (head(title, desc, root, intro, canonical) + chrome(root, active) +
           f'<main id="main">\n{body.replace("{root}", root)}\n</main>\n' + footer(root, *( [cta] if cta else [] )) + lb + '\n</body>\n</html>\n')
    dst = os.path.join(OUT, path); os.makedirs(os.path.dirname(dst), exist_ok=True)
    open(dst, 'w').write(doc)

# ------------------------------------------------------------------ content
PROJECTS = [
  dict(slug='xpense', title='Xpense', cat='product apps mobile', kind='iPhone app · dotXline', badge='My product',
       short='A calm, native iPhone expense tracker. Log spending, set budgets and goals, and split costs with friends.',
       scene='code', html=lambda: '<div class="ks-mini">' + xp_phone(False) + '</div>', tone='x-scene', preview=None),
  dict(slug='tockbee', title='Tockbee', cat='product apps mobile', kind='iPhone and Android app · dotXline', badge='My product',
       short='A shift and pay tracker for UK hourly workers. It clocks you in at work, works out your pay and checks your payslip.',
       scene='code', html=lambda: '<div class="ks-mini">' + tb_phone(False) + '</div>', tone='t-scene', preview=None),
  dict(slug='chatvertiser', title='Chatvertiser', cat='product web', kind='Web design · Ad tech UX',
       short='An AI-powered advertising platform that turns conversations into conversion tools.',
       scene='img', image='work/chatvertiser.webp', preview='work/chatvertiser.webp'),
  dict(slug='greenlife', title='Greenlife', cat='product mobile', kind='App design · Retail',
       short='An everyday shopping assistant that makes the trip faster, from building the list to checkout.',
       scene='img', image='work/greenlife.webp', preview='work/greenlife.webp'),
  dict(slug='puff-count', title='Puff Count', cat='product mobile', kind='App design · Health',
       short='A mobile app that tracks nicotine consumption, with daily limits and onboarding that helps people quit vaping.',
       scene='code', html=lambda: kit.pc_card_inner(), tone='pc-stage', preview=None),
  dict(slug='pocket', title='Pocket', cat='product mobile', kind='iOS app design · Personal finance',
       short='A personal wallet app for iPhone: log expenses by category, see weekly statistics and keep your balance under control.',
       scene='code', html=lambda: kit.pw_card_inner(), tone='pw-stage', preview=None),
]
P = {p['slug']: p for p in PROJECTS}

def scene(p, root='{root}', lazy=True):
    s = p['scene']
    if s == 'img':
        return f'<div class="scene img-scene">{img(p["image"], p["title"] + " design preview", root, "cover", lazy)}<span class="scene-title">{p["title"]}</span></div>'
    if s == 'code':
        return f'<div class="scene kit-scene {p["tone"]}">{p["html"]()}<span class="scene-title">{p["title"]}</span></div>'
    if s == 'app':
        shots = ''.join(f'<div class="phone-shot">{img(x, p["title"] + " screen", root, lazy=lazy)}</div>' for x in p['shots'])
        return f'<div class="scene app-scene {p["tone"]}">{shots}<span class="scene-title">{p["title"]}</span></div>'
    if s == 'omni':
        return '''<div class="scene s1"><div class="mock mock-dash"><div class="mock-bar"><i></i><i></i><i></i></div><div class="mock-body"><div class="map"><span class="route"></span><span class="pin p1"></span><span class="pin p2"></span><span class="pin p3"></span></div><div class="side"><b></b><b></b><b></b><b></b></div></div></div><span class="scene-title">OmniGPS</span></div>'''
    return '''<div class="scene s3"><div class="dial"><svg viewBox="0 0 120 120"><circle cx="60" cy="60" r="50"/><circle class="arc" cx="60" cy="60" r="50" pathLength="100"/></svg><span>72<small>%</small></span></div><div class="chips"><b></b><b></b><b></b></div><span class="scene-title">Quantum Vac</span></div>'''

def preview_attr(p, root):
    if p.get('preview'): return f' data-preview="{root}assets/img/{p["preview"]}"'
    return ''

# ---------------------------------------------------------------- home page
# App Store links. Placeholders point at each app's page on dotxline.com until the real
# App Store links are added: replace these two URLs and rebuild.
APP_STORE = {
    'xpense': 'https://dotxline.com/xpense.html',
    'tockbee': 'https://dotxline.com/tockbee.html',
}
APPLE = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M16.37 12.6c-.02-2.2 1.8-3.26 1.88-3.31-1.03-1.5-2.62-1.7-3.18-1.73-1.35-.14-2.64.8-3.33.8-.69 0-1.74-.78-2.87-.76-1.47.02-2.83.86-3.59 2.18-1.53 2.66-.39 6.6 1.1 8.76.73 1.06 1.6 2.25 2.73 2.2 1.1-.04 1.51-.71 2.84-.71 1.32 0 1.7.71 2.86.69 1.18-.02 1.93-1.08 2.65-2.14.84-1.22 1.18-2.41 1.2-2.47-.03-.01-2.3-.88-2.32-3.5zM14.2 6.13c.6-.73 1.01-1.75.9-2.76-.87.04-1.92.58-2.54 1.31-.56.65-1.05 1.68-.92 2.68.97.07 1.96-.49 2.56-1.23z"/></svg>'

def store_btn(slug, name):
    return (f'<a class="store" href="{APP_STORE[slug]}" target="_blank" rel="noopener" aria-label="Download {name} on the App Store">'
            f'{APPLE}<span><small>Download on the</small>App Store</span></a>')

def status_bar(t='9:41'):
    return (f'<div class="ph-status"><span>{t}</span><i class="ph-island"></i><span class="ph-sig">'
            '<svg viewBox="0 0 18 12"><rect x="0" y="8" width="3" height="4" rx="1"/><rect x="5" y="5" width="3" height="7" rx="1"/><rect x="10" y="2" width="3" height="10" rx="1"/><rect x="15" y="0" width="3" height="12" rx="1"/></svg>'
            '<svg viewBox="0 0 26 12"><rect x=".5" y=".5" width="22" height="11" rx="3" fill="none" stroke="currentColor"/><rect x="2" y="2" width="17" height="8" rx="2"/><rect x="23.5" y="4" width="2" height="4" rx="1"/></svg></span></div>')

XP_TILES = [  # name, amount, colour, icon path
    ('Food', 12.40, '#F59E0B', 'M7 3v8M5 3v4a2 2 0 0 0 4 0V3M7 11v10M16 3c-2 0-3 2-3 5s1 4 3 4v9'),
    ('Transport', 8.20, '#3B82F6', 'M4 16V9l2-4h12l2 4v7M4 16h16M4 16v2M20 16v2M7 13h.01M17 13h.01'),
    ('Fuel', 45.00, '#EF4444', 'M5 21V5a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v16M4 21h12M15 9h2l2 2v6a1.5 1.5 0 0 0 3 0V8l-3-3M8 7h4'),
    ('Subs', 10.99, '#A855F7', 'M4 12a8 8 0 0 1 14-5.3M20 12a8 8 0 0 1-14 5.3M18 3v4h-4M6 21v-4h4'),
    ('Shopping', 24.00, '#EC4899', 'M5 8h14l-1 13H6L5 8zM9 8V6a3 3 0 0 1 6 0v2'),
    ('Groceries', 64.15, '#22C55E', 'M3 4h2l2.5 11h10L20 7H6.2M9 20h.01M17 20h.01'),
    ('Bills', 71.00, '#EAB308', 'M13 2 4 14h7l-1 8 9-12h-7l1-8z'),
    ('Fun', 18.50, '#38BDF8', 'M12 3l2.6 5.6 6 .7-4.5 4.1 1.2 6L12 16.4 6.7 19.4l1.2-6L3.4 9.3l6-.7L12 3z'),
]

def xp_phone(interactive=True):
    tiles = ''.join(f'<button type="button" class="xp-tile" data-cat="{n}" data-amt="{a:.2f}" style="--c:{c}"><i><svg viewBox="0 0 24 24" aria-hidden="true"><path d="{d}"/></svg></i><span>{n}</span></button>' for n, a, c, d in XP_TILES)
    h = f'''        <div class="phone xp-app" data-xpense role="group" aria-label="Working demo of the Xpense overview screen">
          {status_bar()}
          <div class="xp-body">
            <p class="xp-h">Overview</p><p class="xp-sub">Good evening</p>
            <div class="xp-card">
              <span class="xp-l">Spent in October</span>
              <b class="xp-total" data-total>£1,248.60</b>
              <span class="xp-left" data-left>£351.40 left of £1,600 budget</span>
              <div class="xp-bar"><i data-bar></i></div>
              <div class="xp-row"><span data-used>78% used</span><span>9 days to go</span></div>
              <button type="button" class="xp-add" tabindex="-1" aria-hidden="true">+ Add Expense</button>
            </div>
            <p class="xp-qh">Quick Add</p>
            <div class="xp-grid">{tiles}</div>
            <p class="xp-qh">Recent</p>
            <ul class="xp-recent" data-recent><li><i style="--c:#F59E0B"></i><span><b>Lunch with Sam</b><small>Food · Today</small></span><em>£12.40</em></li><li><i style="--c:#3B82F6"></i><span><b>Train to work</b><small>Transport · Today</small></span><em>£8.20</em></li></ul>
            <div class="xp-toast" data-toast role="status" aria-live="polite"></div>
          </div>
          <div class="ph-tabs xp-tabs" aria-hidden="true"><span class="on">Home</span><span>History</span><span>Analyze</span><span>Shared</span></div>
        </div>
'''
    if not interactive:
        h = h.replace(' data-xpense', ' aria-hidden="true"').replace('<button', '<span').replace('</button>', '</span>').replace(' tabindex="-1"', '')
    return h

def tb_phone(interactive=True):
    h = f'''        <div class="phone tb-app" data-tockbee role="group" aria-label="Working demo of the Tockbee today screen">
          {status_bar('09:41')}
          <div class="tb-body">
            <div class="tb-top"><b>tockbee</b><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M4.9 19.1 7 17M17 7l2.1-2.1"/></svg></div>
            <span class="tb-chip" data-chip><i></i><span data-chip-text>On shift at Riverside Care Home</span></span>
            <b class="tb-timer" data-timer>1:33:28</b>
            <span class="tb-since" data-since>Clocked in 07:58 by location</span>
            <button type="button" class="tb-btn" data-btn><span data-btn-text>Clock out</span></button>
            <div class="tb-week">
              <span>This week so far</span>
              <b data-week>£458.20</b>
              <div class="xp-row"><span data-hours>36h 03m</span><span data-shifts>5 shifts</span></div>
              <div class="tb-bar"><i data-bar></i></div>
              <span class="tb-goal" data-goal>£41.80 to your £500.00 goal</span>
            </div>
          </div>
          <div class="ph-tabs tb-tabs" aria-hidden="true"><span class="on">Today</span><span>Shifts</span><span>Sites</span><span>Pay</span></div>
        </div>
'''
    if not interactive:
        h = h.replace(' data-tockbee', ' aria-hidden="true"').replace('<button', '<span').replace('</button>', '</span>').replace(' tabindex="-1"', '')
    return h

def release_xpense():
    return f'''<article class="release" style="--acc:var(--xp)" id="xpense">
      <div class="rel-info" data-reveal>
        <p class="rel-tag mono">My product · dotXline</p>
        <div class="rel-name">{img('kit/xp-icon.webp', '', '{root}')}<h3>Xpense</h3></div>
        <p class="rel-sub">Every penny, in plain sight.</p>
        <dl class="rel-meta mono"><div><dt>Platform</dt><dd>iPhone</dd></div><div><dt>Built with</dt><dd>SwiftUI</dd></div><div><dt>Status</dt><dd>On the App Store</dd></div><div><dt>Role</dt><dd>Designed, built, shipped</dd></div></dl>
        <p class="rel-desc">A calm, native expense tracker. Log spending in one tap, set budgets and goals, and split costs with friends.</p>
        <ul class="rel-points"><li>Quick Add tiles log an expense in one tap</li><li>Progress, never shame: it notices when you spend less</li><li>No ads, and receipt photos stay on your iPhone</li></ul>
        <div class="rel-ctas">{store_btn('xpense', 'Xpense')}<a class="link" href="{{root}}work/xpense.html" data-label="Xpense">Read the case study <span aria-hidden="true">→</span></a></div>
      </div>
      <div class="rel-stage xp-stage" data-reveal style="--d:.1s">
        {xp_phone()}
        <p class="demo-hint mono" aria-hidden="true">Tap a tile to log it</p>
      </div>
    </article>'''

def release_tockbee():
    return f'''<article class="release flip" style="--acc:var(--tb)" id="tockbee">
      <div class="rel-info" data-reveal>
        <p class="rel-tag mono">My product · dotXline</p>
        <div class="rel-name">{img('kit/tb-icon.webp', '', '{root}')}<h3>Tockbee</h3></div>
        <p class="rel-sub">Every hour you work, on the record.</p>
        <dl class="rel-meta mono"><div><dt>Platform</dt><dd>iPhone and Android</dd></div><div><dt>Built with</dt><dd>React Native</dd></div><div><dt>Status</dt><dd>On the App Store</dd></div><div><dt>Role</dt><dd>Designed, built, shipped</dd></div></dl>
        <p class="rel-desc">A shift and pay tracker for UK hourly workers. It clocks you in when you arrive, works out your pay and take-home, and checks your payslip against the hours you really worked.</p>
        <ul class="rel-points"><li>Clocks you in by location or your work Wi-Fi</li><li>Overtime, weekend and night rates worked out as you go</li><li>No account and no data collected</li></ul>
        <div class="rel-ctas">{store_btn('tockbee', 'Tockbee')}<a class="link" href="{{root}}work/tockbee.html" data-label="Tockbee">Read the case study <span aria-hidden="true">→</span></a></div>
      </div>
      <div class="rel-stage tb-stage" data-reveal style="--d:.1s">
        {tb_phone()}
        <p class="demo-hint mono" aria-hidden="true">Live timer · tap Clock out</p>
      </div>
    </article>'''


def home():
    logos = ''.join(f'<img class="mono-logo" src="{{root}}assets/img/brand/logo-{k}.webp" alt="{t}" width="{SIZES["logo/" + k][0]}" height="{SIZES["logo/" + k][1]}" loading="lazy">'
                    for k, t in [('hanek', 'Hanek'), ('phinaturals', 'PhiNaturals'), ('nation-insure', 'Nation Insure'), ('mr-physics', 'Mr Physics'), ('chatvertiser-logo', 'Chatvertiser'), ('cupid-theory', 'Cupid Theory')])
    client = [p for p in PROJECTS if 'apps' not in p['cat']]
    ledger = ''.join(f'''
      <li data-reveal style="--d:{i * .06:.2f}s"><a href="{{root}}work/{p['slug']}.html"{preview_attr(p, '{root}')} data-label="{p['title']}">
        <span class="lg-n">{i + 1:02d}</span><span class="lg-t">{p['title']}</span><span class="lg-k">{p['kind']}</span><span class="lg-s">{p['short']}</span><span class="lg-a" aria-hidden="true">→</span></a></li>''' for i, p in enumerate(client))
    body = f'''<div class="intro-screen" aria-hidden="true">
  <svg class="intro-mark" viewBox="0 0 100 100"><defs><radialGradient id="ngi" gradientUnits="userSpaceOnUse" cx="15" cy="8" r="113">{STOPS}</radialGradient></defs><path pathLength="1" d="{MARK100}"/></svg>
  <div class="intro-count"><span data-intro-count>000</span><i>%</i></div>
  <div class="intro-name">Nagules Gobi · Product Designer</div>
</div>
<section class="hero" id="top">
  <canvas class="hero-canvas" aria-hidden="true"></canvas>
  <div class="wrap hero-inner">
    <p class="me-chip" data-reveal data-hero>{img('me/portrait.webp', 'Portrait of Nagules Gobi', '{root}', lazy=False)}<span>Hi, I’m <b>Nagules Gobi</b>. UX/UI designer who builds the apps too. Director of dotXline LTD.</span></p>
    <h1 class="two-tone" data-split data-hero>I design the app. <span class="dim">Then I build it and ship it.</span></h1>
    <p class="lede" data-reveal data-hero style="--d:.35s">I design web and mobile products, then build them myself with SwiftUI, React Native and AI-assisted development. 30+ projects across three countries, and two apps of my own on the App Store.</p>
    <div class="btns" data-reveal data-hero style="--d:.5s">
      <a class="btn" href="#shipped"><span>See what I’ve shipped</span><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5v14M6 13l6 6 6-6"/></svg></a>
      <a class="btn btn-ghost" href="{{root}}contact.html" data-label="Contact"><span>Hire me</span></a>
    </div>
    <div class="hero-mark-slot" data-reveal data-hero style="--d:.6s" aria-hidden="true"><span class="mono">Touch the mark</span></div>
  </div>
  <div class="wrap hero-foot" data-reveal data-hero style="--d:.7s">
    <span class="mono">UX/UI design · App development · Brand identity</span>
    <span class="hint">Move over the mark, or click it</span>
    <span class="clock mono">London <time data-clock>--:--</time></span>
  </div>
</section>

<section class="marquee" aria-label="Disciplines">
  <div class="marquee-row" data-marquee="1" data-skew="off"><div class="marquee-track"><span>UX/UI Design</span><b>✦</b><span>App Development</span><b>✦</b><span>Product Design</span><b>✦</b><span>Web Development</span><b>✦</b><span>Brand Identity</span><b>✦</b></div></div>
  <div class="marquee-row outline" data-marquee="-1" data-skew="off" aria-hidden="true"><div class="marquee-track"><span>iPhone &amp; Android Apps</span><b>✦</b><span>AI-Assisted Development</span><b>✦</b><span>Websites &amp; Web Apps</span><b>✦</b><span>Design Strategy</span><b>✦</b><span>Graphic Design</span><b>✦</b></div></div>
</section>

<section class="glance" aria-label="At a glance">
  <div class="wrap glance-row mono" data-reveal>
    <span><b>30+</b> projects shipped</span><span><b>3</b> countries</span><span><b>4</b> years of experience</span><span><b>2</b> apps on the App Store</span><span>BSc Computing</span>
  </div>
</section>

<section class="shipped" id="shipped">
  <div class="wrap">
    <div class="section-head">
      <p class="kicker" data-reveal>Shipped</p>
      <h2 class="two-tone" data-split>Designed by me. Built by me. <span class="dim">Live on the App Store.</span></h2>
      <p data-reveal>Xpense and Tockbee are the apps of dotXline LTD, my product company in Cardiff. I designed every screen and built both of them. The phones below are working code, not screenshots: try them.</p>
    </div>
    {release_xpense()}
    {release_tockbee()}
    <p class="shipped-foot" data-reveal><a class="link" href="{{root}}dotxline.html" data-label="dotXline">About dotXline LTD <span aria-hidden="true">→</span></a></p>
  </div>
</section>

<section class="section" id="work">
  <div class="wrap">
    <div class="section-head">
      <p class="kicker" data-reveal>Client work</p>
      <h2 class="two-tone" data-split>Products I designed for teams. <span class="dim">Web, mobile and brand.</span></h2>
    </div>
    <ol class="ledger">{ledger}
    </ol>
    <p class="ledger-foot" data-reveal><a class="link" href="{{root}}work.html" data-label="Work">All work <span aria-hidden="true">→</span></a><a class="link" href="{{root}}work.html#brand" data-label="Brand">Brand and print work <span aria-hidden="true">→</span></a></p>
  </div>
</section>

<section class="logos" aria-label="Brands I have designed for">
  <div class="wrap"><p class="kicker">Brands I’ve designed identities for</p><a href="{{root}}work.html#brand">See all brand work →</a></div>
  <div class="logo-row" data-marquee="1" data-speed="0.5" data-skew="off"><div class="logo-track">{logos}</div></div>
</section>

<section class="section" id="services">
  <div class="wrap">
    <div class="section-head">
      <p class="kicker" data-reveal>What I do</p>
      <h2 data-split>Clean interfaces that catch the eye and guide users effortlessly.</h2>
    </div>
    <div class="services" data-spot>
      <div class="service" data-reveal><svg class="ico" viewBox="0 0 48 48" aria-hidden="true"><circle cx="24" cy="24" r="18" pathLength="1"/><circle cx="24" cy="24" r="10" pathLength="1"/><path d="M24 24 40 8M34 8h6v6" pathLength="1"/></svg><span class="num">Strategy</span><h3>Product design strategy</h3><p>Intuitive, user-focused design strategy rooted in research and aligned with business goals.</p></div>
      <div class="service" data-reveal style="--d:.08s"><svg class="ico" viewBox="0 0 48 48" aria-hidden="true"><rect x="5" y="9" width="30" height="24" rx="3" pathLength="1"/><rect x="30" y="18" width="13" height="22" rx="3" pathLength="1"/><path d="M5 15h30" pathLength="1"/></svg><span class="num">Design + build</span><h3>Web &amp; app design and development</h3><p>From first concept to high-fidelity design, then built into working websites and iPhone and Android apps.</p></div>
      <div class="service" data-reveal style="--d:.16s"><svg class="ico" viewBox="0 0 48 48" aria-hidden="true"><path d="M8 14h32M8 24h32M8 34h32" pathLength="1"/><circle cx="17" cy="14" r="4" pathLength="1"/><circle cx="31" cy="24" r="4" pathLength="1"/><circle cx="21" cy="34" r="4" pathLength="1"/></svg><span class="num">Usability</span><h3>UI/UX optimisation</h3><p>Better usability and performance through engaging, accessible interfaces.</p></div>
      <div class="service" data-reveal style="--d:.24s"><svg class="ico" viewBox="0 0 48 48" aria-hidden="true"><path d="M24 5 41 15v18L24 43 7 33V15Z" pathLength="1"/><path d="M24 5v38M7 15l34 18M41 15 7 33" pathLength="1"/></svg><span class="num">Identity</span><h3>Brand identity</h3><p>Helping brands find their visual voice and build a consistent presence that resonates.</p></div>
    </div>
  </div>
</section>

<section class="section alt" id="build">
  <div class="wrap">
    <div class="section-head">
      <p class="kicker" data-reveal>How I build</p>
      <h2 data-split>From a Figma frame to a <em>working</em> product.</h2>
      <p data-reveal>I’m a product designer first. I also build, using AI-assisted development to turn designs into real, working software fast, then reviewing and refining the code myself.</p>
    </div>
    <ol class="build-steps" data-spot>
      <li class="why-card" data-reveal><span class="big">Design</span><h3>Research and design</h3><p>User flows, wireframes and high-fidelity UI in Figma, grounded in what people actually need.</p></li>
      <li class="why-card" data-reveal style="--d:.08s"><span class="big">Develop</span><h3>Real apps, not just prototypes</h3><p>Working iPhone, Android and web apps, built in SwiftUI and React Native from the design, with real screens and real data.</p></li>
      <li class="why-card" data-reveal style="--d:.16s"><span class="big">Refine</span><h3>AI-assisted development</h3><p>I build with AI coding tools, then review the code and check every change against the design and the brief.</p></li>
      <li class="why-card" data-reveal style="--d:.24s"><span class="big">Launch</span><h3>Take it to users</h3><p>At dotXline I take products from idea to launch-ready apps. For teams, I hand over clean code or clean specs.</p></li>
    </ol>
    <p class="build-note" data-reveal>This portfolio is an example: designed and built by me with AI-assisted development, including the particle logo, page transitions and every animation.</p>
  </div>
</section>

<section class="pitch">
  <div class="wrap">
    <p class="kicker" data-reveal>Need a product that looks great and works flawlessly?</p>
    <p class="scrub" data-scrub>With experience across web, mobile and brand design, I help businesses turn ideas into products people love to use. Whether you’re starting from scratch or refining something that already exists, I bring the clarity and creativity to make it stand out.</p>
  </div>
</section>
'''
    page('index.html', 'Nagules Gobi · UX/UI Designer and App Developer', 'Nagules Gobi is a UK UX/UI designer who builds and ships his own apps, Xpense and Tockbee, and Director of dotXline LTD.', 'index.html', body, intro=True)

# ---------------------------------------------------------------- work index
def work_index():
    cards = ''
    for p in PROJECTS:
        badge = f'<span class="badge"><i></i>{p["badge"]}</span>' if p.get('badge') else ''
        cards += f'''
      <a class="wcard" href="{{root}}work/{p['slug']}.html" data-cat="{p['cat']}" data-cursor="View"{preview_attr(p, '{root}')} data-label="{p['title']}">
        <div class="media" data-img>{badge}{scene(p)}</div>
        <div class="wcard-meta"><h3>{p['title']}</h3><span class="tags">{p['kind']}</span></div>
        <p>{p['short']}</p>
      </a>'''
    body = f'''<section class="page-hero">
  <div class="glow" aria-hidden="true"></div>
  <div class="wrap">
    <p class="kicker" data-reveal data-hero>Work · 2019 to now</p>
    <h1 data-split data-hero>Selected <em>work</em></h1>
    <p class="lede" data-reveal data-hero style="--d:.3s">Two kinds of work on one page: the products and apps I design and build, and the brands, campaigns and print I give a visual voice.</p>
    <nav class="jump" data-reveal data-hero style="--d:.45s" aria-label="Sections on this page"><a href="#product"><span class="mono">01</span>Product work<small>{len(PROJECTS)} case studies</small></a><a href="#brand"><span class="mono">02</span>Brand and print<small>{len(GALLERY)} pieces</small></a></nav>
  </div>
</section>
<section class="section work-part" id="product" style="padding-top:0">
  <div class="wrap"><div class="section-head part-head"><p class="kicker" data-reveal>01 · Product work</p><h2 class="two-tone" data-split>Apps and websites. <span class="dim">Case studies from idea to launch.</span></h2></div></div>
  <div class="wrap" id="work-list" data-view="grid">
    <div class="filters" data-reveal>
      <div class="chipset" data-filter-group="work-grid" role="group" aria-label="Filter projects">
        <button class="chip" type="button" data-filter="all" aria-pressed="true">All<sup></sup></button>
        <button class="chip" type="button" data-filter="apps" aria-pressed="false">My apps<sup></sup></button>
        <button class="chip" type="button" data-filter="web" aria-pressed="false">Web<sup></sup></button>
        <button class="chip" type="button" data-filter="mobile" aria-pressed="false">Mobile<sup></sup></button>
      </div>
      <div class="toggle" data-view-toggle="work-list" role="group" aria-label="Layout"><button type="button" data-view="grid" aria-pressed="true">Grid</button><button type="button" data-view="list" aria-pressed="false">List</button></div>
    </div>
    <div class="wgrid" id="work-grid">{cards}
    </div>
  </div>
</section>
{gallery_section()}'''
    page('work.html', 'Work · Nagules Gobi', 'Product and app case studies, plus logos, identities, campaigns and print design by Nagules Gobi.', 'work.html', body, lightbox=True)

# ---------------------------------------------------------------- case pages
def facts(items):
    return '<dl class="case-facts" data-reveal>' + ''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in items) + '</dl>'

def sec(title, inner):
    return f'<section class="wrap"><div class="case-sec"><h2 data-split>{title}</h2><div class="body" data-reveal>{inner}</div></div></section>'

def points(items):
    return '<ul class="points">' + ''.join(f'<li><b>{a}</b>{b}</li>' for a, b in items) + '</ul>'

def flow(items, root='{root}'):
    its = ''.join(f'<figure class="flow-item"><div class="shot">{img(src, cap, root)}</div><b>{cap}</b><span>{note}</span></figure>' for src, cap, note in items)
    return f'<div class="flow-wrap" data-reveal><div class="flow" data-flow tabindex="0" aria-label="App screens, scroll sideways">{its}</div><div class="flow-nav"><button type="button" data-flow-prev aria-label="Previous screen">←</button><button type="button" data-flow-next aria-label="Next screen">→</button></div></div>'

def next_link(slug):
    i = [p['slug'] for p in PROJECTS].index(slug); n = PROJECTS[(i + 1) % len(PROJECTS)]
    pic = img(n['preview'], '', '{root}') if n.get('preview') else f'<div class="case-mock" style="height:100%">{scene(n)}</div>'
    return f'''<a class="next" href="{{root}}work/{n['slug']}.html" data-label="{n['title']}" data-cursor="Next">
  <div class="wrap"><p class="kicker">Next case study</p><h2><span>{n['title']}</span></h2></div>
  <div class="next-img">{pic}</div>
</a>'''

def case(slug, hero_kicker, title_html, lede, fact_items, cover, sections, link=None):
    p = P[slug]
    body = f'''<section class="page-hero case-hero">
  <div class="glow" aria-hidden="true"></div>
  <div class="wrap">
    <p class="kicker" data-reveal data-hero>{hero_kicker}</p>
    <h1 data-split data-hero>{title_html}</h1>
    <p class="lede" data-reveal data-hero style="--d:.3s">{lede}</p>
    {facts(fact_items)}
    {('<p class="case-store" data-reveal>' + store_btn(slug, p['title']) + '</p>') if slug in APP_STORE else ''}
  </div>
</section>
{cover}
{sections}
{next_link(slug)}'''
    page(f'work/{slug}.html', f'{p["title"]} · Nagules Gobi', p['short'], 'work.html', body)

def shots(items, root='{root}'):
    """Full-width, labelled sections from a Behance board: [(label, image, alt), ...]"""
    its = ''.join(f'<figure class="shot-row" data-reveal><figcaption><span class="mono">{i + 1:02d}</span>{label}</figcaption><div class="media" data-img>{img(src, alt, root)}</div></figure>'
                  for i, (label, src, alt) in enumerate(items))
    return f'<section class="case-band shots"><div class="wrap">{its}</div></section>'

def cover_img(path, alt):
    return f'<div class="media case-cover" data-img><div class="plx" data-parallax="0.08">{img(path, alt, "{root}", lazy=False)}</div></div>'

def cover_scene(p):
    return f'<div class="case-cover case-mock" data-img style="aspect-ratio:auto">{scene(p, lazy=False)}</div>'

def cases():
    # Xpense
    case('xpense', 'Case study · My product at dotXline', 'Every penny, in <em>plain</em> sight.',
         'A calm, native expense tracker for iPhone. Log it in one tap, see where it goes, and keep a little more each month.',
         [('Role', 'Founder · designed, built, shipped'), ('Company', 'dotXline LTD'), ('Platform', 'iPhone'), ('Built with', 'SwiftUI'), ('Status', 'On the App Store')],
         kit.XP_FONT + kit.xp_cover(),
         sec('The idea', '<p class="quote">Spending isn’t the problem. Not knowing is.</p><p>Xpense keeps every penny in plain sight, celebrates the months you keep a little more, and never makes you feel bad about the rest.</p>') +
         sec('Design decisions', points([
             ('Logged in one tap', 'Quick Add tiles open a new expense with the category already chosen. Your tiles, in your order.'),
             ('Progress, never shame', 'Spend less than last month and Xpense says so: “Nice, £12 less than September.” Spend more and it stays neutral.'),
             ('Numbers first', 'Built natively for iPhone with the calm design of iOS 26. Nothing in the way of the figure you came for.'),
             ('Private by default', 'No ads, no selling data, and receipt photos stay on your iPhone.')])) +
         kit.xp_sections() +
         sec('Principles', points([('Clear', 'We say the number. “£3.40 logged to Food.” Plain, specific, no guessing.'), ('Calm', 'Quiet interfaces that stay out of your way and respect your attention.'), ('Private', 'No ads. No tracking you across other companies’ apps.'), ('Built to ship', 'Designed and built inside my own company, with every detail owned end to end.')]) +
             '<p><a class="link" href="https://dotxline.com/xpense.html" target="_blank" rel="noopener">See Xpense on dotxline.com ↗</a></p>'))
    # Tockbee
    case('tockbee', 'Case study · My product at dotXline', 'Every hour you work, on the <em>record</em>.',
         'Tockbee keeps your own record of every hour you work, so you can check your payslip and sort out missing pay.',
         [('Role', 'Founder · designed, built, shipped'), ('Company', 'dotXline LTD'), ('Platform', 'iPhone and Android'), ('Built with', 'React Native'), ('Status', 'On the App Store')],
         kit.TB_FONT + kit.tb_cover(),
         sec('The problem', '<p class="quote">Every hour you work should show up on your payslip.</p><p>Tockbee keeps an honest record on your phone and nobody else’s, so checking your pay takes a minute instead of an argument.</p>') +
         sec('How it works', points([
             ('Arrive. You’re clocked in.', 'By location at a work site or by joining your work Wi-Fi. Every automatic clock-in sends a notification with Undo.'),
             ('Every minute counts', 'Overtime, weekend and night rates and unpaid breaks, worked out as you go.'),
             ('Check it against your payslip', 'Copy in what your payslip says and Tockbee shows any hours or pay that went missing.'),
             ('Your timesheet, ready to share', 'A PDF or CSV with every shift and how it was recorded.')])) +
         kit.tb_sections() +
         sec('Honest by design', '<p class="lead">Tax is an estimate, and the app says so.</p><p>Tockbee calls it <strong>estimated take-home</strong>: after PAYE (including Scottish rates), National Insurance, student loan and pension. Your payslip stays the official figure. And Tockbee collects no data at all.</p>' +
             '<p><a class="link" href="https://dotxline.com/tockbee.html" target="_blank" rel="noopener">See Tockbee on dotxline.com ↗</a></p>'))
    # Chatvertiser
    case('chatvertiser', 'Case study · Web app UI · Ad tech UX', 'Advertising that starts with a <em>conversation</em>.',
         'An AI-powered advertising platform that turns conversations into conversion tools, with a customer support chat app that makes business enquiries easier.',
         [('Role', 'Web and UX design, logo'), ('Industry', 'Advertising technology'), ('Tools', 'Figma, Illustrator, Photoshop'), ('Project', '<a href="https://www.behance.net/gallery/224174429/Chatvertiser" target="_blank" rel="noopener">Behance ↗</a>')],
         kit.CV_FONT + kit.cv_cover(),
         sec('Overview', '<p class="lead">One chat, the whole campaign.</p><p>Chatvertiser is a customer support chatting application for any business. The design focused on a fluid, chat-based interface that simplifies campaign creation, audience targeting and performance tracking, all through one conversational flow.</p>') +
         sec('Design focus', points([('Campaigns by chat', 'Creating a campaign feels like describing it, not filling in a long form.'), ('A full support desk', 'Profiles, flows, broadcasts, segments, reports, integrations and agents in one dashboard.'), ('A clear visual system', 'A violet palette (#805AD5, #7678EC, #3C348A), one typeface, a consistent icon set and reusable elements.'), ('A mark to match', 'I also designed the Chatvertiser logo, a speech bubble with a pulse.')])) +
         kit.cv_sections() +
         f'<section class="case-band"><div class="wrap"><div class="duo"><div class="media" data-img>{img("work/chatvertiser-2.webp", "Chatvertiser support system screens", "{root}")}</div><div class="media" data-img style="display:grid;place-items:center;padding:12%;background:var(--card)">{img("brand/logo-chatvertiser-logo.webp", "Chatvertiser logo", "{root}", "mono-logo")}</div></div></div></section>')
    # Greenlife
    case('greenlife', 'Case study · App design · Retail', 'Shopping, from list to <em>checkout</em>.',
         'An everyday shopping assistant app designed to make the trip faster, from building the list to paying at the till.',
         [('Role', 'App design'), ('Industry', 'Retail and grocery'), ('Platform', 'Mobile app'), ('Prototype', '<a href="https://www.behance.net/gallery/109365235/Grocery-Shopping-App" target="_blank" rel="noopener">Behance ↗</a>')],
         cover_img('work/greenlife.webp', 'Greenlife app screens with fresh produce'),
         sec('Overview', '<p class="lead">Built for the shop floor, not the sofa.</p><p>The UI focuses on simplicity, accessibility and visual clarity, so the app stays easy to use with one hand and a full basket.</p>') +
         sec('Design focus', points([('List creation', 'Build the list quickly before you leave home.'), ('In-store efficiency', 'Find what is next without hunting through menus.'), ('Accessible by default', 'Clear contrast, large targets and readable type.'), ('Fresh visual voice', 'A green, produce-led identity that feels like the food it sells.')])))
    # Puff Count
    case('puff-count', 'Case study · App design · Health', 'Every puff, <em>counted</em>.',
         'Puff Count is a mobile app that tracks nicotine consumption, lets people set daily limits and helps them work towards quitting vaping.',
         [('Role', 'UX/UI design and branding'), ('Platform', 'iPhone app'), ('Tools', 'Figma, Illustrator, Photoshop'), ('Project', '<a href="https://www.behance.net/gallery/224174013/Puff-Count" target="_blank" rel="noopener">Behance ↗</a>')],
         kit.PC_FONT + kit.pc_cover(),
         sec('Overview', '<p class="lead">Track it first. Then cut it down.</p><p>Puff Count tracks nicotine consumption, offers unlimited puff logging and lets people set daily limits. Onboarding asks a few short questions, one per screen, so the app starts from the person’s own goal.</p>') +
         sec('Design focus', points([('One question per screen', 'Name, goal, the day you quit smoking, reminders and weekly spend on vaping, each on its own calm screen.'), ('Goals first', 'People choose “I want to quit vaping” or “Just curious”, so the app meets them where they are.'), ('A clear upgrade', 'Puff Count Unlimited is offered monthly or yearly with a free trial, and no ads.'), ('A bright, friendly identity', 'A bold blue palette (#1058FF, #1497FC), Poppins type and a simple P-mark app icon.')])) +
         kit.pc_sections())
    # Pocket (Personal Wallet App)
    case('pocket', 'Case study · iOS app design · Personal finance', 'Your wallet, in your <em>pocket</em>.',
         'Pocket is a personal wallet app for iPhone. Add expenses by category, see extended statistics for any period and keep your balance under control.',
         [('Role', 'UI/UX design and branding'), ('Made for', 'Loofyn Hyper'), ('Team', 'With Muralikrishna Naguleswararajah'), ('Tools', 'Adobe XD, Illustrator, Photoshop'), ('Project', '<a href="https://www.behance.net/gallery/109368407/Personal-Wallet-App" target="_blank" rel="noopener">Behance ↗</a>')],
         kit.PW_FONT + kit.pw_cover(),
         sec('Overview', '<p class="lead">Every expense in a safe place.</p><p>Pocket is an iOS application for keeping a personal wallet. The flow starts with a clear welcome and login, because it is crucial to make the right first impression and to be sure your personal wallet is in a safe place.</p>') +
         sec('Design focus', points([('Welcome, login and sign-up', 'Short, familiar forms with the Pocket mark front and centre.'), ('Statistics that compare', 'Extended statistics of your expenses for any period, compared with your average for that period.'), ('Balance at a glance', 'Add expenses in categories from food to travel, then edit or delete them when you need to.'), ('A calm, clean identity', 'A cyan and blue palette (#00B4D8, #0078B7), Circular Std type and a wallet-shaped app icon.')])) +
         kit.pw_sections())

# ---------------------------------------------------------------- dotXline
def dotxline():
    body = f'''<section class="page-hero dx-hero">
  <div class="wrap">
    <span class="dx-logos" data-reveal data-hero><img class="dx-logo on-dark" src="{{root}}assets/img/apps/dotxline-lockup-dark.svg" alt="dotXline" width="320" height="54"><img class="dx-logo on-light" src="{{root}}assets/img/apps/dotxline-lockup-light.svg" alt="" width="320" height="54"></span>
    <p class="kicker" data-reveal data-hero>My company · Director</p>
    <h1 data-split data-hero>Small, exact apps that just work.</h1>
    <p class="lede" data-reveal data-hero style="--d:.3s">dotXline LTD is a product company in Cardiff. We make everyday money and work feel simple, one carefully built app at a time. As Director, I lead the product and design every screen.</p>
    <div class="hero-meta" data-reveal data-hero style="--d:.4s"><span>Role <b>Director</b></span><span>Based in <b>Cardiff, United Kingdom</b></span><span>Apps <b>Xpense, Tockbee</b></span></div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="section-head"><p class="kicker" data-reveal>The name is the method</p><h2 data-split>We build from zero to one.</h2></div>
    <div class="dx-story" data-spot>
      <div data-reveal><span class="sym">0</span><h3>Who we are.</h3><p>A small product company in Cardiff. Every app starts as a blank page and one small, exact idea.</p></div>
      <div data-reveal style="--d:.1s"><span class="sym">×</span><h3>Where this meets that.</h3><p>We look for the point where an everyday problem meets a simple answer: what you spent, the hours you worked, what you’re owed.</p></div>
      <div data-reveal style="--d:.2s"><span class="sym">1</span><h3>Then we finish it.</h3><p>One app at a time, built natively and kept simple, until it does its job without fuss.</p></div>
    </div>
  </div>
</section>
<section class="wrap app-sec">
  <div>
    <div class="app-id" data-reveal>{img('kit/xp-icon.webp', '', '{root}')}<div><b>Xpense</b><br><span style="color:var(--muted)">by dotXline</span></div></div>
    <h2 data-split>Every penny, in plain sight.</h2>
    <div class="body" data-reveal><p>A calm, native iPhone expense tracker. Log spending, set budgets and goals, and split costs with friends.</p><div class="tags"><span>iPhone</span><span>SwiftUI</span><span>On the App Store</span><span>No ads</span></div><p class="btn-row"><a class="btn" href="{{root}}work/xpense.html" data-magnetic data-label="Xpense"><span>Read the case study</span></a>{store_btn('xpense', 'Xpense')}</p></div>
  </div>
  <div class="stack" data-reveal>{''.join(f'<div class="shot">{img(x, "Xpense screen", "{root}")}</div>' for x in ['apps/xpense-3.webp', 'apps/xpense-1.webp', 'apps/xpense-4.webp'])}</div>
</section>
<section class="wrap app-sec">
  <div>
    <div class="app-id" data-reveal>{img('kit/tb-icon.webp', '', '{root}')}<div><b>Tockbee</b><br><span style="color:var(--muted)">by dotXline</span></div></div>
    <h2 data-split>Every hour you work, on the record.</h2>
    <div class="body" data-reveal><p>Tockbee clocks you in when you arrive at work, works out your pay and take-home, and checks your payslip against the hours you really worked.</p><div class="tags"><span>iPhone and Android</span><span>React Native</span><span>On the App Store</span><span>No account, no tracking</span></div><p class="btn-row"><a class="btn" href="{{root}}work/tockbee.html" data-magnetic data-label="Tockbee"><span>Read the case study</span></a>{store_btn('tockbee', 'Tockbee')}</p></div>
  </div>
  <div class="stack" data-reveal>{''.join(f'<div class="shot">{img(x, "Tockbee screen", "{root}")}</div>' for x in ['apps/tockbee-shifts.webp', 'apps/tockbee-today.webp', 'apps/tockbee-payslip.webp'])}</div>
</section>
<section class="section alt">
  <div class="wrap">
    <div class="section-head"><p class="kicker" data-reveal>How we work</p><h2 data-split>Three habits, in every app.</h2></div>
    <div class="why three" data-spot>
      <div class="why-card" data-reveal><span class="big">Clear.</span><h3>We say the number.</h3><p>“£3.40 logged to Food.” Plain words, specific amounts, no guessing.</p></div>
      <div class="why-card" data-reveal style="--d:.08s"><span class="big">Calm.</span><h3>Quiet interfaces</h3><p>They stay out of your way and respect your attention. No guilt, no alarms.</p></div>
      <div class="why-card" data-reveal style="--d:.16s"><span class="big">Private.</span><h3>As little as possible.</h3><p>No ads. No selling your data. Xpense keeps receipt photos on your iPhone and Tockbee collects no data at all.</p></div>
    </div>
    <p data-reveal style="margin-top:40px"><a class="link" href="https://dotxline.com" target="_blank" rel="noopener">Visit dotxline.com ↗</a></p>
  </div>
</section>'''
    page('dotxline.html', 'dotXline · Nagules Gobi', 'Nagules Gobi is Director of dotXline LTD, a Cardiff product company that makes Xpense and Tockbee.', 'dotxline.html', body)

# ---------------------------------------------------------------- brand
GALLERY = [
  ('logo-hanek', 'Hanek', 'Logo', 'identity', True), ('allura', 'Allura Apparel', 'Brand guide', 'identity', False),
  ('logo-phinaturals', 'PhiNaturals', 'Logo · Nature’s formula', 'identity', True), ('unlucky-ninja', 'Unlucky Ninja', 'Logo and wallpaper', 'identity', False),
  ('turmeric-ad', 'Turmeric Curcumin', 'Social ad · buy one get one', 'campaign', False), ('logo-nation-insure', 'Nation Insure', 'Logo', 'identity', True),
  ('viviendo-del-trade', 'Viviendo del Trade', 'Book cover', 'print', False), ('team-reddin', 'Team Reddin', 'Logo', 'identity', False),
  ('logo-mr-physics', 'Mr Physics', 'Logo', 'identity', True), ('humanity', 'Humanity', 'Logo system', 'identity', False),
  ('fanera', 'Fanera', 'App launch visual', 'campaign', False), ('cheat-court', 'Cheat Court', 'Logo', 'identity', False),
  ('awesom', 'Awesom', 'Brand identity · triple your energy', 'identity', False), ('handicap', 'Handicap', 'Book poster', 'print', False),
  ('logo-cupid-theory', 'Cupid Theory', 'Logo', 'identity', True), ('vacay360', 'Vacay360', 'Logo and colour system', 'identity', False),
  ('growing-together', 'Growing Together', 'School fundraising campaign', 'campaign', False), ('video-game-break', 'Video Game Break', 'Logo and favicon', 'identity', False),
  ('mushroom-formulas', 'Medicinal mushroom formulas', 'Product ad', 'campaign', False), ('fitfables', 'FitFables', 'Logo', 'identity', False),
  ('wappnegocio', 'WappNegocio', 'Logo', 'identity', False), ('ink-calligraphy', 'Brush calligraphy', 'Artwork', 'print', False),
  ('suomen-tulkkauspalvelut', 'Suomen Tulkkauspalvelut', 'Logo', 'identity', False), ('plegables', 'Plegables.org', 'Logo', 'identity', False),
  ('sachet', 'Sachet', 'Packaging design', 'packaging', False), ('tiquipaya', 'Tiquipaya.net', 'Logo', 'identity', False),
  ('whitsunday-kombi', 'Whitsunday Kombi', 'Logo', 'identity', False), ('cupid-theory-rect', 'Cupid Theory', 'Logo on colour', 'identity', False),
  ('logo-chatvertiser-logo', 'Chatvertiser', 'Logo', 'identity', True),
]
def gallery_section():
    items = ''
    for k, title, kind, cat, logo in GALLERY:
        key = ('logo/' + k[5:]) if logo else ('brand/' + k)
        w, h = SIZES[key]; src = f'{{root}}assets/img/brand/{k}.webp'
        pad = ' style="padding:14% 10%;background:var(--card)"' if logo else ''
        cls = ' class="mono-logo"' if logo else ''
        items += f'<button class="gitem" type="button" data-cat="{cat}" data-full="{src}" data-title="{E(title)}" data-kind="{E(kind)}" data-cursor="Open"{pad}><img{cls} src="{src}" alt="{E(title)}, {E(kind.lower())}" width="{w}" height="{h}" loading="lazy" decoding="async"><span class="gcap"><b>{E(title)}</b><span>{E(kind)}</span></span></button>'
    return f'''<section class="section work-part brand-part" id="brand">
  <div class="wrap"><div class="section-head part-head">
    <p class="kicker" data-reveal>02 · Brand and print</p>
    <h2 class="two-tone" data-split>Every pixel shaped with purpose. <span class="dim">Logos, campaigns, print and packaging.</span></h2>
    <p data-reveal>Alongside product work, I create visual identities and campaigns that help businesses stand out. {len(GALLERY)} pieces. Tap any of them to view it full screen.</p>
  </div></div>
  <div class="wrap" id="campaigns">
    <div class="filters" data-reveal>
      <div class="chipset" data-filter-group="gallery" role="group" aria-label="Filter brand work">
        <button class="chip" type="button" data-filter="all" aria-pressed="true">All<sup></sup></button>
        <button class="chip" type="button" data-filter="identity" aria-pressed="false">Logos and identity<sup></sup></button>
        <button class="chip" type="button" data-filter="campaign" aria-pressed="false">Campaigns<sup></sup></button>
        <button class="chip" type="button" data-filter="print" aria-pressed="false">Print<sup></sup></button>
        <button class="chip" type="button" data-filter="packaging" aria-pressed="false">Packaging<sup></sup></button>
      </div>
    </div>
    <div class="masonry" id="gallery">{items}</div>
  </div>
</section>'''

def redirect(path, target, title):
    open(os.path.join(OUT, path), 'w').write(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{title}</title><meta http-equiv="refresh" content="0; url={target}"><link rel="canonical" href="https://www.nagulesgobi.com/{target.split("#")[0].replace("../", "")}"><meta name="robots" content="noindex"></head><body><p><a href="{target}">{title}</a></p><script>location.replace("{target}" + "")</script></body></html>\n')

def brand():
    redirect('brand.html', 'work.html#brand', 'Brand and print work · Nagules Gobi')

# ---------------------------------------------------------------- about
def about():
    body = f'''<section class="page-hero">
  <div class="glow" aria-hidden="true"></div>
  <div class="wrap">
    <p class="kicker" data-reveal data-hero>About</p>
    <h1 data-split data-hero>Designer. Director. <em>Builder.</em></h1>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap about-grid">
    <figure class="portrait" style="margin:0">
      <div class="media" data-img><div class="plx" data-parallax="0.06">{img('me/portrait.webp', 'Nagules Gobi', '{root}', lazy=False)}</div></div>
      <figcaption><span>Gobikrishna Naguleswararajah</span><span>Nagules Gobi</span></figcaption>
    </figure>
    <div class="bio">
      <p class="lead" data-reveal>I design products people actually enjoy using, and I build my own.</p>
      <p data-reveal>I’m <strong>Nagules Gobi</strong>, a product designer in the United Kingdom working across UX/UI, web and app design, and brand identity. Over four years I’ve shipped <strong>30+ projects across 3 countries</strong>, from ad-tech platforms and health apps to shopping apps and logos.</p>
      <p data-reveal>I’m also <strong>Director of dotXline LTD</strong>, a product company in Cardiff. There I design and build Xpense, a calm iPhone expense tracker, and Tockbee, a shift and pay tracker for UK workers. Owning products end to end taught me to design for the people using them and for the team that has to ship them.</p>
      <p data-reveal>I studied for a <strong>BSc in Computing</strong>, and today I also build what I design. I use <strong>AI-assisted development</strong> to turn designs into working products quickly, then review and refine the code myself. It means I can prototype in code, test ideas with real users sooner, and talk to engineering teams in their own language.</p>
      <dl class="facts" data-reveal>
        <div><dt>Role</dt><dd>Product designer who builds</dd></div>
        <div><dt>Company</dt><dd>Director, dotXline LTD</dd></div>
        <div><dt>Builds with</dt><dd>Code and AI-assisted development</dd></div>
        <div><dt>Education</dt><dd>BSc in Computing</dd></div>
        <div><dt>Experience</dt><dd>4 years · 30+ projects</dd></div>
        <div><dt>Open to</dt><dd>Roles and freelance</dd></div>
      </dl>
      <p data-reveal><a class="btn" href="{{root}}contact.html" data-magnetic data-label="Contact"><span>Hire me</span><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></a></p>
    </div>
  </div>
</section>
<section class="section alt">
  <div class="wrap">
    <div class="section-head"><p class="kicker" data-reveal>How I work</p><h2 data-split>From first question to working product.</h2><p data-reveal>The same five steps on every project. Timelines depend on the size of the work, and I share one after our first call.</p></div>
    <ol class="steps" data-reveal>
      <li style="--i:0"><b>Discovery</b><span>Research the people, the goal and the constraints.</span></li>
      <li style="--i:1"><b>Wireframes</b><span>Structure and flow before any polish.</span></li>
      <li style="--i:2"><b>UI design</b><span>High-fidelity screens and a visual system.</span></li>
      <li style="--i:3"><b>Prototype</b><span>An interactive version to test and refine.</span></li>
      <li style="--i:4"><b>Build</b><span>I build it with AI-assisted development, or hand clean specs to your developers.</span></li>
    </ol>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="section-head"><p class="kicker" data-reveal>Capabilities</p><h2 data-split>What you get when you hire me.</h2></div>
    <div class="services six" data-spot>
      <div class="service" data-reveal><span class="num">Strategy</span><h3>Product design strategy</h3><p>User-focused strategy rooted in research and aligned with business goals.</p></div>
      <div class="service" data-reveal style="--d:.06s"><span class="num">Interfaces</span><h3>Web &amp; app design</h3><p>Concept to high-fidelity design for web, iPhone and Android.</p></div>
      <div class="service" data-reveal style="--d:.12s"><span class="num">Usability</span><h3>UI/UX optimisation</h3><p>Engaging, accessible interfaces that perform better.</p></div>
      <div class="service" data-reveal style="--d:.18s"><span class="num">Identity</span><h3>Brand identity</h3><p>Logos and visual systems that give a product its voice.</p></div>
      <div class="service" data-reveal style="--d:.24s"><span class="num">Apps</span><h3>App development</h3><p>iPhone, Android and web apps designed and built end to end, like Xpense and Tockbee.</p></div>
      <div class="service" data-reveal style="--d:.3s"><span class="num">Building</span><h3>AI-assisted development</h3><p>Designs turned into working front ends and apps, reviewed and refined by me.</p></div>
    </div>
  </div>
</section>'''
    page('about.html', 'About · Nagules Gobi', 'About Nagules Gobi: product designer, Director of dotXline LTD, BSc in Computing.', 'about.html', body)

# ---------------------------------------------------------------- contact
def contact():
    body = f'''<section class="page-hero">
  <div class="glow" aria-hidden="true"></div>
  <div class="wrap">
    <p class="kicker" data-reveal data-hero><span class="avail"><span class="pulse" style="width:8px;height:8px;border-radius:50%;background:#22B35E;display:inline-block"></span>Available now</span></p>
    <h1 data-split data-hero>Let’s work <em>together</em>.</h1>
    <p class="lede" data-reveal data-hero style="--d:.3s">Hiring for a product design role, or need a designer for a project? Tell me a little about it and I’ll get back to you.</p>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap contact-wrap">
    <form class="cform" data-compose novalidate data-reveal>
      <fieldset><legend>I’m looking for</legend><div class="chipset">
        <button class="chip" type="button" data-chip aria-pressed="false">Full-time role</button>
        <button class="chip" type="button" data-chip aria-pressed="false">Freelance project</button>
        <button class="chip" type="button" data-chip aria-pressed="false">App design</button>
        <button class="chip" type="button" data-chip aria-pressed="false">Website</button>
        <button class="chip" type="button" data-chip aria-pressed="false">Brand identity</button>
        <button class="chip" type="button" data-chip aria-pressed="false">Design and build</button>
      </div></fieldset>
      <div class="row">
        <div class="field"><label for="f-name">Your name</label><input id="f-name" name="name" autocomplete="name" required></div>
        <div class="field"><label for="f-email">Your email</label><input id="f-email" name="email" type="email" autocomplete="email"></div>
      </div>
      <div class="field"><label for="f-company">Company</label><input id="f-company" name="company" autocomplete="organization"></div>
      <div class="field"><label for="f-msg">Message</label><textarea id="f-msg" name="message" required placeholder="The role or project, the timeline, and anything I should know."></textarea></div>
      <div class="btns"><button class="btn" type="submit" data-magnetic><span>Write the email</span><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></button></div>
      <p class="form-status" data-status role="status"></p>
    </form>
    <aside class="side-card" data-reveal style="--d:.15s">
      <p class="kicker" style="margin:0">Email me directly</p>
      <p class="email">{EMAIL}</p>
      <div class="btns"><button class="btn btn-sm" type="button" data-copy="{EMAIL}"><span data-copy-label>Copy email</span></button><a class="btn btn-sm btn-ghost" href="mailto:{EMAIL}"><span>Open mail app</span></a></div>
      <p style="margin-top:8px;color:var(--muted);font-size:15px">Helpful to include:</p>
      <ul><li>The role or project</li><li>Your timeline</li><li>A link to the product, if there is one</li></ul>
      <p style="color:var(--muted);font-size:15px">London time <b style="color:var(--text)"><time data-clock>--:--</time></b></p>
    </aside>
  </div>
</section>
<section class="section alt" id="faq">
  <div class="wrap faq-grid">
    <div class="section-head"><p class="kicker" data-reveal>FAQ</p><h2 data-split>Questions, answered.</h2></div>
    <div class="faq" data-reveal>
      <details><summary>Can you guarantee improvements in conversions?<i aria-hidden="true"></i></summary><div class="faq-a"><p>No designer can honestly guarantee a number. What I can promise is a process built on research, clear goals and testing, so every design decision is aimed at making your product easier to use and easier to say yes to.</p></div></details>
      <details><summary>How much does it cost to design one web page?<i aria-hidden="true"></i></summary><div class="faq-a"><p>It depends on scope: the content, the number of states and breakpoints, and whether you need a design system behind it. Tell me about your project and I’ll send a clear quote.</p></div></details>
      <details><summary>What’s your process like, and how long does it take?<i aria-hidden="true"></i></summary><div class="faq-a"><p>Discovery and research, then wireframes, UI design, an interactive prototype and a clean handoff to development. Timelines depend on the size of the project, and I’ll share one after our first call.</p></div></details>
      <details><summary>Can you build what you design?<i aria-hidden="true"></i></summary><div class="faq-a"><p>Yes. Alongside design, I build with code and AI-assisted development: interactive prototypes, front ends and full apps like Xpense and Tockbee at dotXline. For larger products I work with your engineers and hand over clean specs.</p></div></details>
      <details><summary>Are you open to full-time roles?<i aria-hidden="true"></i></summary><div class="faq-a"><p>Yes. I’m open to product design roles as well as freelance projects. Send me the details and let’s talk.</p></div></details>
    </div>
  </div>
</section>'''
    page('contact.html', 'Contact · Nagules Gobi', 'Hire Nagules Gobi for a product design role or project.', 'contact.html', body, cta='Prefer a call? Let’s talk it through.')

def extras():
    redirect('graphicdesigner.html', 'work.html#brand', 'Brand and print work · Nagules Gobi')
    redirect('work/omnigps.html', '../work.html#product', 'Work · Nagules Gobi')
    redirect('work/quantum-vac.html', '../work.html#product', 'Work · Nagules Gobi')
    open(os.path.join(OUT, 'CNAME'), 'w').write('www.nagulesgobi.com\n')
    open(os.path.join(OUT, '.nojekyll'), 'w').write('')
    pages = ['', 'work.html', 'dotxline.html', 'about.html', 'contact.html'] + [f'work/{p["slug"]}.html' for p in PROJECTS]
    open(os.path.join(OUT, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>https://www.nagulesgobi.com/{p}</loc></url>\n' for p in pages) + '</urlset>\n')
    open(os.path.join(OUT, 'robots.txt'), 'w').write('User-agent: *\nAllow: /\nSitemap: https://www.nagulesgobi.com/sitemap.xml\n')
    four = head('Page not found · Nagules Gobi', 'This page does not exist.', '/') + chrome('/', '') + '<main id="main"><section class="page-hero" style="min-height:80vh"><div class="glow" aria-hidden="true"></div><div class="wrap"><p class="kicker">404</p><h1 data-split data-hero>This page <em>doesn’t</em> exist.</h1><div class="btns" style="margin-top:40px"><a class="btn" href="/index.html"><span>Back to home</span></a><a class="btn btn-ghost" href="/work.html"><span>See my work</span></a></div></div></section></main></body></html>\n'
    open(os.path.join(OUT, '404.html'), 'w').write(four)

if __name__ == '__main__':
    if os.path.isdir(os.path.join(OUT, 'assets')): shutil.rmtree(os.path.join(OUT, 'assets'))
    os.makedirs(OUT, exist_ok=True)
    shutil.copytree(os.path.join(HERE, 'assets'), os.path.join(OUT, 'assets'))
    js = os.path.join(OUT, 'assets', 'js', 'site.js'); s = open(js).read()
    s = re.sub(r"var MARK_D = '[^']+';", f"var MARK_D = '{MARK100}';", s); open(js, 'w').write(s)
    home(); work_index(); cases(); dotxline(); brand(); about(); contact(); extras()
    print('built', sorted(os.path.relpath(os.path.join(d, f), OUT) for d, _, fs in os.walk(OUT) for f in fs if f.endswith('.html')))

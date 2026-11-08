"""Coded case-study kit: palettes, type specimens, wireframes, phone and browser frames,
and the app screens for Puff Count, Pocket and Chatvertiser, rebuilt from the owner's
Behance boards in the site's own design language (no pasted screenshots).
HTML uses the literal {root} placeholder, which build.page() replaces."""
import html
E = html.escape

# ------------------------------------------------------------------ building blocks
def palette(colors, note=''):
    cards = ''.join(
        f'<div class="kp-sw" data-reveal style="--d:{i * .06:.2f}s"><i style="background:#{hx}"></i>'
        f'<b>{E(name)}</b><span class="mono">#{hx.upper()}</span></div>' for i, (hx, name) in enumerate(colors))
    return f'<div class="kit-block"><p class="kit-label mono">Colour palette</p><div class="kp-grid">{cards}</div>{f"<p class=kit-note>{E(note)}</p>" if note else ""}</div>'

def typeface(family_css, name, shown_as=None, weights='Regular · Medium · Bold', tint='var(--text)'):
    shown = f'<span class="kt-note">Shown here in {E(shown_as)}, a close free match.</span>' if shown_as else ''
    fam = family_css.replace('"', "'")
    return (f'<div class="kit-block"><p class="kit-label mono">Typography</p><div class="kt" style="--kf:{fam}">'
            f'<div class="kt-aa" style="color:{tint}">Aa</div><div class="kt-body"><b>{E(name)}</b><span class="mono">{E(weights)}</span>'
            f'<p class="kt-abc">Aa Bb Cc Dd Ee Ff Gg Hh Ii Jj Kk Ll Mm Nn Oo Pp Qq Rr Ss Tt Uu Vv Ww Xx Yy Zz</p><p class="kt-num">0 1 2 3 4 5 6 7 8 9 £ $ %</p>{shown}</div></div></div>')

def wireframes(screens, label='Wireframes'):
    """screens: list of lists of block tokens. Tokens: bar, title, sub, hero, circle, line, line-s, input, btn, btn-ghost, grid, list, chart, tabs, spacer"""
    def blk(t):
        if t == 'grid': return '<div class="wf-grid"><i></i><i></i><i></i><i></i><i></i><i></i></div>'
        if t == 'list': return '<div class="wf-list"><i></i><i></i><i></i><i></i></div>'
        if t == 'chart': return '<div class="wf-chart"><i style="height:60%"></i><i style="height:35%"></i><i style="height:80%"></i><i style="height:50%"></i><i style="height:70%"></i><i style="height:40%"></i></div>'
        if t == 'tabs': return '<div class="wf-tabs"><i></i><i></i><i></i><i></i></div>'
        return f'<div class="wf-{t}"></div>'
    ph = ''.join(f'<div class="wf-phone" data-reveal style="--d:{i * .07:.2f}s">{"".join(blk(t) for t in s)}</div>' for i, s in enumerate(screens))
    return f'<div class="kit-block"><p class="kit-label mono">{E(label)}</p><div class="wf-row">{ph}</div></div>'

def phone(inner, cls='', label=''):
    cap = f'<figcaption>{E(label)}</figcaption>' if label else ''
    return f'<figure class="kit-phone" data-reveal><div class="phone {cls}">{inner}</div>{cap}</figure>'

def phones(items, label='Screens'):
    return f'<div class="kit-block"><p class="kit-label mono">{E(label)}</p><div class="kit-phones">{"".join(items)}</div></div>'

def status(t='9:41', light=False):
    return (f'<div class="ph-status{" on-dark" if light else ""}"><span>{t}</span><i class="ph-island"></i><span class="ph-sig">'
            '<svg viewBox="0 0 18 12"><rect x="0" y="8" width="3" height="4" rx="1"/><rect x="5" y="5" width="3" height="7" rx="1"/><rect x="10" y="2" width="3" height="10" rx="1"/><rect x="15" y="0" width="3" height="12" rx="1"/></svg>'
            '<svg viewBox="0 0 26 12"><rect x=".5" y=".5" width="22" height="11" rx="3" fill="none" stroke="currentColor"/><rect x="2" y="2" width="17" height="8" rx="2"/></svg></span></div>')

def browser(inner, url, label=''):
    cap = f'<figcaption>{E(label)}</figcaption>' if label else ''
    return (f'<figure class="kit-browser" data-reveal><div class="kb-win"><div class="kb-bar"><i></i><i></i><i></i><span>{E(url)}</span></div>'
            f'<div class="kb-body">{inner}</div></div>{cap}</figure>')

def stage(inner, cls=''):
    return f'<div class="kit-stage {cls}" data-img>{inner}</div>'

def section(title, inner, kicker='', acc=''):
    k = f'<p class="kicker" data-reveal>{E(kicker)}</p>' if kicker else ''
    st = f' style="--kacc:{acc}"' if acc else ''
    return f'<section class="case-band kit"{st}><div class="wrap"><div class="section-head">{k}<h2 data-split>{title}</h2></div>{inner}</div></section>'

# ------------------------------------------------------------------ Puff Count
PC_FONT = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&amp;display=swap">'
PC_ICON = '<img class="pc-icon" src="{root}assets/img/work/pc-icon.webp" alt="" width="240" height="240">'
BACK = '<svg class="pc-back" viewBox="0 0 24 24" aria-hidden="true"><path d="M19 12H5M11 6l-6 6 6 6"/></svg>'

def pc_head(text):
    return f'<div class="pc-head">{BACK}<span>{E(text)}</span></div>' if text else f'<div class="pc-head">{BACK}</div>'

def pc_screens():
    s = []
    s.append(phone(status() + f'<div class="pc-body pc-center"><div class="pc-art">{PC_ICON}<i></i><i></i><i></i><i></i></div><h4>Congratulations!</h4><p class="pc-mute">Welcome to Puff Count</p><span class="pc-btn">Get Started</span><p class="pc-small">Already have an account? <b>Sign in</b></p></div>', 'pc-app', 'Welcome'))
    s.append(phone(status() + pc_head('Hey! Stranger..') + '<div class="pc-body"><h5>What is your name?</h5><div class="pc-input">Steven</div><span class="pc-btn sm">Next</span></div>', 'pc-app', 'Your name'))
    s.append(phone(status() + pc_head('Hello Steven') + '<div class="pc-body pc-center pc-low"><h5>What are your goals?</h5><span class="pc-btn wide">I want to quit vaping</span><span class="pc-btn wide">Just curious</span></div>', 'pc-app', 'Your goal'))
    wheel = ''.join(f'<div class="{c}"><span>{d}</span><span>{h}</span><span>{m}</span></div>' for c, d, h, m in
                    [('f2', 'Mon 7 Sep', '8', '58'), ('f1', 'Tue 8 Sep', '9', '59'), ('on', 'Wed 9 Sep', '10', '00'), ('f1', 'Thu 10 Sep', '11', '01'), ('f2', 'Fri 11 Sep', '12', '02')])
    s.append(phone(status() + pc_head('You are in the right place...') + f'<div class="pc-body"><h5>When did you quit smoking?</h5><div class="pc-input">Now</div><span class="pc-btn sm">Next</span><div class="pc-picker"><div class="pc-pick-bar"><span>‹ ›</span><b>Now</b></div><div class="pc-wheel">{wheel}</div></div></div>', 'pc-app', 'Quit date'))
    s.append(phone(status() + pc_head('') + '<div class="pc-body pc-center pc-low"><h5>Do you want reminders?</h5><span class="pc-btn wide">Yes</span><span class="pc-btn wide">No</span></div>', 'pc-app', 'Reminders'))
    keys = ''.join(f'<span><b>{n}</b><small>{l}</small></span>' for n, l in [('1', ''), ('2', 'ABC'), ('3', 'DEF'), ('4', 'GHI'), ('5', 'JKL'), ('6', 'MNO'), ('7', 'PQRS'), ('8', 'TUV'), ('9', 'WXYZ')]) + '<span class="blank"></span><span><b>0</b></span><span class="blank">⌫</span>'
    s.append(phone(status() + pc_head('Perfect! Way to go..') + f'<div class="pc-body"><h5>How much do you spend on vaping each week?</h5><div class="pc-input">£15</div><span class="pc-btn sm">Next</span><div class="pc-keys">{keys}</div></div>', 'pc-app', 'Weekly spend'))
    perks = ''.join(f'<li>{p}</li>' for p in ['Track nicotine consumption', 'Unlimited puffs', 'Set daily limits', 'No ads, ever'])
    s.append(phone(status() + f'<div class="pc-body">{BACK}<div class="pc-unlock-art">{PC_ICON}</div><h4 class="pc-left">Unlock</h4><p class="pc-blue">Puff Count Unlimited</p><ul class="pc-perks">{perks}</ul><div class="pc-plan"><i></i><b>$8.88</b><span>/ month</span></div><div class="pc-plan on"><i></i><b>$24.99</b><span>/ year</span><em>Free trial</em></div><span class="pc-btn wide">Try Puff Count for free</span></div>', 'pc-app', 'Puff Count Unlimited'))
    return s

def pc_cover():
    sc = pc_screens()
    return stage(f'<div class="ks-brand">{PC_ICON}<b>Puff Count</b><span>Track nicotine · Unlimited puffs · Daily limits</span></div><div class="ks-phones">{sc[0]}{sc[6]}</div>', 'pc-stage')

def pc_card():
    sc = pc_screens()
    return f'<div class="scene kit-scene pc-stage"><div class="ks-mini">{sc[0]}{sc[6]}</div><span class="scene-title">Puff Count</span></div>'

def pc_sections():
    sc = pc_screens()
    return (section('The design system.', palette([('1058FF', 'Puff Blue'), ('1497FC', 'Sky'), ('FFFFFF', 'White'), ('000000', 'Black')]) +
                    typeface('"Poppins", system-ui, sans-serif', 'Poppins', tint='#1058FF') +
                    wireframes([['bar', 'title', 'line', 'line-s', 'grid'], ['spacer', 'hero', 'title', 'line-s', 'btn'], ['circle', 'title', 'line-s', 'input', 'input', 'btn'], ['bar', 'list', 'btn-ghost']]), 'From the Behance board', '#1497FC')
            + section('Onboarding, one question at a time.', phones(sc[:4], 'Welcome to quit date')
                      + phones(sc[4:], 'Reminders, weekly spend and the upgrade')))

# ------------------------------------------------------------------ Pocket
PW_FONT = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&amp;display=swap">'
PW_MARK = ('<svg class="pw-mark" viewBox="0 0 48 56" aria-hidden="true"><rect x="7" y="2" width="34" height="5" rx="2.5" fill="currentColor" opacity=".55"/>'
           '<rect x="5" y="9" width="38" height="5" rx="2.5" fill="currentColor" opacity=".8"/><path d="M3 16h42v26L24 54 3 42z" fill="currentColor"/>'
           '<path d="M24 22v26M29 27c-1-2-3-3-5-3-3 0-5 1.6-5 4s2 3.2 5 4 5 2 5 4.4-2.2 4.2-5 4.2c-2.4 0-4.4-1-5.4-3" fill="none" stroke="var(--pw-on, #00B4D8)" stroke-width="3" stroke-linecap="round"/></svg>')
PW_TABS = ('<div class="pw-tabs"><i></i><i></i><b>+</b><i></i><i></i></div>')

def pw_screens():
    s = []
    s.append(phone(status(light=True) + f'<div class="pw-body pw-splash">{PW_MARK}<b>POCKET</b><span>Your personal<br>mobile wallet</span></div>', 'pw-app pw-cyan', 'Welcome'))
    s.append(phone(status() + f'<div class="pw-body"><p class="pw-title">LOGIN</p><div class="pw-logo">{PW_MARK}</div><div class="pw-in">EMAIL / PHONE<i>👤</i></div><div class="pw-in">PASSWORD<i>⚿</i></div><span class="pw-btn">LOGIN</span><p class="pw-small">FORGOT <b>PASSWORD?</b></p><p class="pw-foot">CREATE ACCOUNT</p></div>', 'pw-app', 'Login'))
    s.append(phone(status() + f'<div class="pw-body"><p class="pw-title">SIGNUP</p><div class="pw-logo">{PW_MARK}</div><div class="pw-in">FULL NAME</div><div class="pw-in">EMAIL / PHONE</div><div class="pw-in">NEW PASSWORD</div><div class="pw-in">CONFIRM PASSWORD</div><span class="pw-btn">SIGNUP</span><p class="pw-foot">LOGIN</p></div>', 'pw-app', 'Sign up'))
    bars = ''.join(f'<span><i style="height:{a}%"></i><i class="dk" style="height:{b}%"></i></span>' for a, b in [(40, 45), (28, 20), (22, 30), (45, 40), (30, 25), (26, 70), (34, 18)])
    rows = ''.join(f'<li><i>{ic}</i><span><small>{c}</small><b>{t}</b><small>{d}</small></span><em>{v}</em></li>' for ic, c, t, d, v in
                   [('▣', 'MOVIE', 'Spend on Fun Mall Cinema', 'Monday', '$23.00'), ('☕', 'COFFEE', 'Spend on Starbucks', 'Monday', '$20.12'), ('🛍', 'SHOP', 'Spend on Super Market', 'Sunday', '$12.45')])
    s.append(phone(status() + f'<div class="pw-body"><p class="pw-title">WEEKLY REPORT</p><div class="pw-bars">{bars}</div><p class="pw-key"><i></i>EXPENSES <i class="dk"></i>DEPOSIT</p><ul class="pw-rows">{rows}</ul></div>{PW_TABS}', 'pw-app', 'Weekly report'))
    mini = ''.join(f'<span><i style="height:{a}%"></i><i class="dk" style="height:{b}%"></i></span>' for a, b in [(50, 20), (40, 25), (25, 30), (55, 20)])
    s.append(phone(status() + f'<div class="pw-body"><div class="pw-hero"><svg class="pw-waves" viewBox="0 0 200 80" preserveAspectRatio="none" aria-hidden="true">{"".join(f"<path d=\'M0 {40 + k * 3} C40 {10 + k * 3},70 {70 + k * 3},110 {40 + k * 3} S170 {10 + k * 3},200 {35 + k * 3}\'/>" for k in range(6))}</svg><span class="pw-avatar"></span><small>WALLET BALANCE</small><b>$1,345.00</b></div><div class="pw-cards"><div class="pw-visa"><b>VISA</b><strong>$234.85</strong><small>**** 1745</small></div><div class="pw-mini"><small>WEEKLY REPORT</small><div class="pw-bars sm">{mini}</div></div></div></div>{PW_TABS}', 'pw-app', 'Wallet balance'))
    return s

def pw_cover():
    sc = pw_screens()
    return stage(f'<div class="ks-brand pw-brand">{PW_MARK}<b>Pocket</b><span>iOS application · personal wallet</span></div><div class="ks-phones">{sc[4]}{sc[3]}</div>', 'pw-stage')

def pw_card():
    sc = pw_screens()
    return f'<div class="scene kit-scene pw-stage"><div class="ks-mini">{sc[0]}{sc[4]}</div><span class="scene-title">Pocket</span></div>'

def pw_sections():
    sc = pw_screens()
    return (section('The design system.', palette([('00B4D8', 'Pocket Cyan'), ('0078B7', 'Deep Blue'), ('B1B1B1', 'Grey'), ('2B2B2B', 'Ink')]) +
                    typeface('"DM Sans", system-ui, sans-serif', 'Circular Std', shown_as='DM Sans', weights='Book · Medium · Bold', tint='#0078B7') +
                    wireframes([['bar', 'hero', 'line', 'line-s', 'list'], ['spacer', 'circle', 'input', 'input', 'btn'], ['bar', 'chart', 'list'], ['title', 'hero', 'grid'], ['bar', 'line', 'list', 'tabs']], 'User experience: wireframes'), 'From the Behance board', '#00B4D8')
            + section('Welcome, login and sign-up.', '<p class="kit-quote" data-reveal>It’s crucial to make the right first impression, and to be sure your personal wallet is in a safe place.</p>' + phones(sc[:3], 'Welcome screens'))
            + section('Statistics and balance.', '<p class="kit-quote" data-reveal>Look at extended statistics of your expenses for any period, compare costs with your average, and keep your balance under control.</p>' + phones(sc[3:], 'Expenses and wallet')))

# ------------------------------------------------------------------ Chatvertiser
CV_FONT = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Exo+2:wght@500;600&amp;family=Roboto:wght@400;500;700&amp;display=swap">'
CV_LOGO = '<span class="cv-logo"><svg viewBox="0 0 32 28" aria-hidden="true"><path d="M4 4h18a4 4 0 0 1 4 4v8a4 4 0 0 1-4 4H12l-6 5v-5H4a4 4 0 0 1-4-4V8a4 4 0 0 1 4-4z"/><circle cx="9" cy="12" r="1.8" fill="#fff"/><circle cx="14" cy="12" r="1.8" fill="#fff"/><circle cx="19" cy="12" r="1.8" fill="#fff"/></svg>chatvertiser</span>'
CV_ICONS = {  # simple line icons in the Chatvertiser style
    'dashboard': 'M4 4h6v6H4zM14 4h6v6h-6zM4 14h6v6H4zM14 14h6v6h-6z', 'offer': 'M13 2 4 14h7l-1 8 9-12h-7l1-8z',
    'broadcast': 'M3 10v4h4l6 4V6L7 10H3zM17 8c1.5 1 1.5 7 0 8M20 5c3 3 3 11 0 14', 'flows': 'M6 6a2 2 0 1 0 0 .01M18 12a2 2 0 1 0 0 .01M6 18a2 2 0 1 0 0 .01M8 7l8 4M8 17l8-4',
    'profile': 'M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM4 21c1-4 4-6 8-6s7 2 8 6', 'segments': 'M8 11a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM16 11a3 3 0 1 0 0-6M2 20c.6-3 3-5 6-5s5.4 2 6 5M16 15c3 0 5 2 6 5',
    'reports': 'M4 4h16v16H4zM8 16v-4M12 16V8M16 16v-6', 'image': 'M4 5h16v14H4zM4 15l5-5 5 5 3-3 3 3M15 9h.01',
    'forms': 'M8 4h8v3H8zM6 6H5v15h14V6h-1M8 12h8M8 16h5', 'code': 'M8 8l-5 4 5 4M16 8l5 4-5 4M14 5l-4 14', 'users': 'M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM4 21a8 8 0 0 1 16 0',
    'search': 'M11 18a7 7 0 1 0 0-14 7 7 0 0 0 0 14zM21 21l-5-5', 'bell': 'M6 16V11a6 6 0 1 1 12 0v5l2 2H4zM10 21h4', 'trash': 'M4 7h16M10 11v6M14 11v6M6 7l1 13h10l1-13M9 7V4h6v3',
    'edit': 'M4 20h4L19 9l-4-4L4 16zM14 6l4 4', 'download': 'M12 4v11M7 10l5 5 5-5M5 20h14', 'share': 'M6 12a2 2 0 1 0 0 .01M18 6a2 2 0 1 0 0 .01M18 18a2 2 0 1 0 0 .01M8 11l8-4M8 13l8 4',
    'external': 'M14 4h6v6M20 4l-9 9M18 14v6H4V6h6', 'plus': 'M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18zM12 8v8M8 12h8', 'x': 'M6 6l12 12M18 6 6 18',
}
def ico(name, cls='cv-ic'):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true"><path d="{CV_ICONS[name]}"/></svg>'

NAV = [('dashboard', 'Dashboard'), ('offer', 'Offer'), ('broadcast', 'Broadcasts'), ('flows', 'Flows'), ('profile', 'Profiles'), ('segments', 'Segments & Lists'),
       ('reports', 'Reports'), ('image', 'Image Library'), ('forms', 'Forms'), ('code', 'Integrations'), ('users', 'Users / Agents')]

def cv_side(active):
    items = ''.join(f'<li class="{"on" if t == active else ""}">{ico(k)}<span>{t}</span></li>' for k, t in NAV)
    return f'<aside class="cv-side">{CV_LOGO}<ul>{items}</ul></aside>'

def cv_profiles():
    people = [('Lavonda Isom', 'ilavonda@gmail.com'), ('Michael Du', 'alohaboy71@hotmail.com'), ('Shadae Basnight', 'williansshadae080@gmail.com'), ('Jeanette Jackson', 'jjeanette1241@gmail.com'),
              ('George Harris', 'koloharris88@gmail.com'), ('Matthew Jenkins', 'matthewjenkinsjr10@gmail.com'), ('Debbie Osborne', 'dosborne0507@gmail.com'), ('Jennifer Hawkins', 'mrsjsh@gmail.com')]
    rows = ''.join(f'<li class="{"on" if n == "Michael Du" else ""}"><i class="cv-check"></i><b>{n}</b><span>{m}</span></li>' for n, m in people)
    acts = ''.join(f'<li><i></i><span><b>{a}</b><small>Details</small></span><em>{t}</em></li>' for a, t in
                   [('Active on website for less than a minute', '20 minutes ago'), ('Received email “Don’t forget…”', '10 hours ago'), ('Checkout started', '10 hours ago'), ('Checkout started', '11 hours ago'), ('Active on website for 42 minutes', '11 hours ago'), ('Viewed product', '12 hours ago')])
    main = (f'<div class="cv-main"><div class="cv-top">{ico("search")}<span>Search profiles</span></div>'
            f'<div class="cv-crumbs"><span>Profiles ›</span><b>Michael Du</b><em><b>17,948</b> active profiles</em></div>'
            f'<div class="cv-filters"><span class="cv-sel">All states ▾</span><span class="cv-sel">All locations ▾</span></div>'
            f'<div class="cv-split"><div class="cv-table"><div class="cv-th"><i class="cv-check"></i><b>Name</b><span>Email</span></div><ul>{rows}</ul><div class="cv-pages"><span>Page</span><i>1</i><b>1</b><i>2</i><i>3</i></div></div>'
            f'<div class="cv-detail"><div class="cv-tabs"><b>{ico("profile")}Profile</b><span>Messages</span><span>Charts</span></div><ul class="cv-acts">{acts}</ul>'
            f'<div class="cv-meta"><small>CONTACT</small><b>Phone</b><span>+1 651 235 4005</span><b>Location</b><span>Minneapolis, Minnesota</span></div></div></div></div>')
    return f'<div class="cv-app">{cv_side("Profiles")}{main}</div>'

def cv_broadcasts():
    rows = [('Abandoned checkout feminex', True, 'Jason', '1 day ago', '23%', '16%'), ('Newsletter blast', True, 'Rafael', 'Jun 12, 2020', '18%', '18%'),
            ('Oct 23, 2019 · The Strat', False, 'Olivia', 'Jun 12, 2020', '19%', '19%'), ('Tropicana Las Vegas', False, 'Krrish', 'Jun 12, 2020', '19%', '19%'),
            ('Abandoned checkout feminex', False, 'Jason', 'Jun 12, 2020', '19%', '19%'), ('Newsletter blast', False, 'Rafael', 'Jun 12, 2020', '18%', '11%')]
    tr = ''.join(f'<li><i class="cv-check"></i><b>{n}</b><span class="cv-tog{" on" if a else ""}"><i></i></span><span class="cv-owner"><i></i>{o}</span><span>{d}</span><span>{op}</span><span>{c}</span></li>' for n, a, o, d, op, c in rows)
    main = (f'<div class="cv-main"><div class="cv-top">{ico("search")}<span>Search broadcasts</span></div>'
            f'<div class="cv-crumbs"><b>Broadcasts</b><em><span class="cv-sel">Options ▾</span><span class="cv-primary">+ Create</span></em></div>'
            f'<div class="cv-filters"><span class="cv-chip">Product Red {ico("x", "cv-ic xs")}</span><span class="cv-sel">Select tags ▾</span><span class="cv-sel">All states ▾</span></div>'
            f'<div class="cv-table cv-wide"><div class="cv-th"><i class="cv-check"></i><b>Name</b><span>Active</span><span>Owner</span><span>Last edited</span><span>Open rate</span><span>Click rate</span></div><ul>{tr}</ul></div></div>')
    return f'<div class="cv-app">{cv_side("Broadcasts")}{main}</div>'

def cv_chat():
    people = [('Jason', 'I have an issue with my order', '', ''), ('Rafael', 'Can you help me with the…', 'on', ''), ('Olivia', 'I can’t figure out how to…', '', '3'),
              ('Krrish', 'Hello, how can I upgrade…', '', '1'), ('Elijah', 'I have sent it to my email', '', ''), ('Emma', 'Hello, how can I upgrade…', '', ''), ('Noah', 'Ok, got it.', '', '2'), ('Roy', 'I couldn’t log in to your…', '', '1')]
    li = ''.join(f'<li class="{c}"><i class="cv-av"></i><b>{n}</b><span>{m}</span>{f"<em>{u}</em>" if u else ""}</li>' for n, m, c, u in people)
    msgs = ('<div class="cv-sys">Signed up</div><div class="cv-sys">Added to cart</div><div class="cv-sys">Initiated checkout</div>'
            '<div class="cv-in">Hi. This is Rafael.</div><div class="cv-out">Hi Rafael, I’m Julia from Shrum Support. How can I help you today?</div>'
            '<div class="cv-in">Can you give me a call?</div><div class="cv-out">Sure</div><div class="cv-sys">Outgoing call · 06:34</div>'
            '<div class="cv-in">I’m having some issues with checkout.</div><div class="cv-in">Can you help me with the product configuration?</div>')
    quick = '<div class="cv-quick"><span>Sure</span><span>Let me check your cart</span><span>Send me the product…</span></div>'
    coupons = ''.join(f'<li><span>{c}</span><em>{p} off</em></li>' for c, p in [('ShrumBF20', '20%'), ('ShrumCM35', '35%'), ('SuperCC', '10%'), ('ShrumFridayDeals', '35%')])
    side = (f'<div class="cv-panel"><small>SETTINGS</small><p><span>Instant reply</span><i class="cv-tog"><i></i></i></p><p><span>Message suggestions</span><i class="cv-tog on"><i></i></i></p>'
            f'<p><span>Dark mode</span><i class="cv-tog on"><i></i></i></p><small>STOREWIDE COUPONS</small><ul class="cv-coupons">{coupons}</ul>'
            f'<small>ACTIONS</small><div class="cv-actions"><span>Opt out</span><span>Close</span><span>Delete</span></div></div>')
    return (f'<div class="cv-app cv-chat"><ul class="cv-inbox">{li}</ul><div class="cv-thread"><div class="cv-msgs">{msgs}</div>{quick}'
            f'<div class="cv-compose"><span>Type a message…</span><b>Send</b></div></div>{side}</div>')

def cv_elements():
    ics = ''.join(ico(k, 'cv-ic big') for k in ['image', 'broadcast', 'segments', 'plus', 'share', 'profile', 'code', 'search', 'x', 'reports', 'edit', 'offer', 'bell', 'trash', 'dashboard', 'forms', 'external', 'download'])
    els = (f'<span class="cv-chip">Product Red {ico("x", "cv-ic xs")}</span><span class="cv-ghost">{ico("trash")}Delete</span><span class="cv-ghost">{ico("edit")}Edit</span>'
           f'<span class="cv-ghost">{ico("download")}Download</span><span class="cv-primary">Save</span><span class="cv-outline">Cancel</span><span class="cv-primary">+ Upload</span>'
           f'<span class="cv-outline">Options ▾</span><span class="cv-pager"><i>‹</i><b>1</b><i>2</i><i>3</i><i>›</i></span><span class="cv-tog on"><i></i></span><span class="cv-check on"></span>')
    return (f'<div class="kit-block"><p class="kit-label mono">Icons</p><div class="cv-icons">{ics}</div></div>'
            f'<div class="kit-block"><p class="kit-label mono">Elements</p><div class="cv-elements">{els}</div></div>')

def cv_cover():
    return stage(browser(cv_chat(), 'app.chatvertiser.com/inbox'), 'cv-stage')

def cv_sections():
    return (section('The design system.', palette([('805AD5', 'Violet'), ('7678EC', 'Periwinkle'), ('3C348A', 'Indigo'), ('000000', 'Black')]) +
                    typeface('"Exo 2", system-ui, sans-serif', 'Display typeface', shown_as='Exo 2', weights='Headings and numbers', tint='#7678EC') +
                    cv_elements(), 'From the Behance board', '#7678EC')
            + section('Main window and broadcasts.', browser(cv_profiles(), 'app.chatvertiser.com/profiles', 'Profiles: every customer with their live activity')
                      + browser(cv_broadcasts(), 'app.chatvertiser.com/broadcasts', 'Broadcasts: campaigns with owners, open and click rates'))
            + section('Chat, with the whole customer in view.', browser(cv_chat(), 'app.chatvertiser.com/inbox', 'Inbox: conversation, quick replies, coupons and actions side by side')))

def pc_card_inner():
    sc = pc_screens()
    return f'<div class="ks-mini">{sc[0]}{sc[6]}</div>'

def pw_card_inner():
    sc = pw_screens()
    return f'<div class="ks-mini">{sc[0]}{sc[4]}</div>'

# ------------------------------------------------------------------ brand-kit media (Xpense, Tockbee)
def device(src, alt, caption='', w=600, h=1304):
    """A real app screenshot in a thin device bezel that matches its exact shape: never cropped."""
    cap = f'<figcaption>{E(caption)}</figcaption>' if caption else ''
    return (f'<figure class="kit-device" data-reveal><div class="kd-bezel"><img src="{{root}}assets/img/kit/{src}" alt="{E(alt)}" '
            f'width="{w}" height="{h}" loading="lazy" decoding="async"></div>{cap}</figure>')

def devices(items, label='Screens'):
    return f'<div class="kit-block"><p class="kit-label mono">{E(label)}</p><div class="kit-phones kit-devices">{"".join(items)}</div></div>'

def video(name, caption, w=540, h=960):
    return (f'<figure class="kit-video" data-reveal><div class="kv-frame" style="aspect-ratio:{w}/{h}"><video controls playsinline preload="none" '
            f'poster="{{root}}assets/img/kit/{name}-poster.webp" width="{w}" height="{h}"><source src="{{root}}assets/video/{name}.mp4" type="video/mp4"></video></div>'
            f'<figcaption>{E(caption)}</figcaption></figure>')

def videos(items, label='In motion'):
    return f'<div class="kit-block"><p class="kit-label mono">{E(label)}</p><div class="kit-videos">{"".join(items)}</div></div>'

def store_strip(n, alt_prefix, label='App Store photos'):
    imgs = ''.join(f'<img src="{{root}}assets/img/kit/xp-store-{i}.webp" alt="{E(alt_prefix)} {i} of {n}" width="640" height="1387" loading="lazy" decoding="async">' for i in range(1, n + 1))
    return f'<div class="kit-block"><p class="kit-label mono">{E(label)}</p><div class="kit-strip" tabindex="0" aria-label="{E(label)}, scroll sideways">{imgs}</div></div>'

def palette_jobs(colors, label='Colour palette'):
    cards = ''.join(f'<div class="kp-sw" data-reveal style="--d:{i * .05:.2f}s"><i style="background:#{hx}"></i><b>{E(name)}</b><span class="mono">#{hx.upper()}</span><small>{E(job)}</small></div>'
                    for i, (hx, name, job) in enumerate(colors))
    return f'<div class="kit-block"><p class="kit-label mono">{E(label)}</p><div class="kp-grid">{cards}</div></div>'

TB_FONT = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fredoka:wght@600;700&amp;display=swap">'
XP_FONT = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Sora:wght@600;700&amp;display=swap">'

def tb_cover():
    phones = (device('tb-today.webp', 'Tockbee Today screen: on shift at Riverside Care Home, 1:33:28, Clock out') +
              device('tb-pay.webp', 'Tockbee Pay screen: £458.20 this week before tax'))
    return stage(f'<div class="ks-brand tb-brand"><img src="{{root}}assets/img/kit/tb-icon.webp" alt="" width="240" height="240"><b>tockbee</b><span>Every hour you work, on the record.</span></div><div class="ks-phones">{phones}</div>', 'tb-stage')

def tb_sections():
    screens = [('tb-today.webp', 'Today', 'Today: the running shift, clocked in by location'), ('tb-shifts.webp', 'Shifts', 'Shifts: every shift, its breaks and how it was recorded'),
               ('tb-sites.webp', 'Sites', 'Sites: work places that clock you in when you arrive'), ('tb-pay.webp', 'Pay', 'Pay: base pay, goal and estimated take-home'),
               ('tb-payslip.webp', 'Payslip check', 'Payslip check: possibly underpaid, £12.71 less than your log'), ('tb-export.webp', 'Export', 'Export: a PDF timesheet or CSV spreadsheet'),
               ('tb-review.webp', 'Year in review', 'Year in review: tax year so far and your busiest month')]
    return (section('From clock-in to payslip check.', devices([device(s, a, c) for s, c, a in screens], 'The app, screen by screen'), 'Real screens', '#FF7A2F')
            + section('In motion.', videos([video('tb-preview', 'App preview'), video('tb-receipt', 'Receipt ad: an itemised shift'), video('tb-onehour', 'Ad: one hour short')]), 'Videos', '#FF7A2F')
            + section('The brand.', palette_jobs([('FF7A2F', 'Tangerine', 'Brand colour, app icon, Clock in'), ('2A1712', 'Cocoa', 'Text and primary buttons'), ('FFF6E8', 'Cream', 'Light backgrounds'),
                                                  ('FFB627', 'Sunshine', 'Highlights, this week’s earnings'), ('FF4F5A', 'Coral', 'Live: you’re on shift now'), ('C2361F', 'Rust', 'Links and overtime figures'),
                                                  ('1F7A44', 'Leaf', 'Functional only: paid, matches payslip')])
                      + typeface('"Fredoka", system-ui, sans-serif', 'Fredoka', weights='SemiBold 600 · wordmark and titles, lowercase', tint='#FF7A2F')
                      + '<p class="kit-note">Text on Tangerine, Sunshine or Coral is always Cocoa. Coral only ever means “on shift right now”. No bees, anywhere.</p>', 'From the brand kit', '#FF7A2F'))

def xp_cover():
    return f'<div class="kit-stage xp-stage" data-img><div class="ks-brand xp-brand"><img src="{{root}}assets/img/kit/xp-icon.webp" alt="" width="240" height="240"><b>Xpense</b><span>Every penny, in plain sight.</span></div><div class="kit-strip on-stage" tabindex="0" aria-label="Xpense App Store photos, scroll sideways">{"".join(f"<img src=\'{{root}}assets/img/kit/xp-store-{i}.webp\' alt=\'Xpense App Store photo {i} of 5\' width=\'640\' height=\'1387\' decoding=\'async\'>" for i in range(1, 6))}</div></div>'

def xp_sections():
    return (section('In motion.', videos([video('xp-preview', 'App preview, 29 seconds', 540, 1170), video('xp-cup', 'Ad: the cup', 540, 1170)]), 'Videos', '#0F9D7A')
            + section('The brand: Mint and Ink.',
                      '<div class="kit-block xp-logo"><p class="kit-label mono">The icon</p><div class="xl-row"><img src="{root}assets/img/kit/xp-icon.webp" alt="Xpense app icon" width="240" height="240"><p>“Less than last month.” Two rounded bars: last month on top, faint; this month below, shorter; and the amber between them is what you kept. Three layers, so iOS gives it Liquid Glass depth.</p></div></div>'
                      + palette_jobs([('0F9D7A', 'Mint', 'Logo, icon, chart fills'), ('0A7D61', 'Mint Dark', 'Buttons and links'), ('E3F5EE', 'Mint Light', 'Tinted wells, selection'),
                                      ('0E1512', 'Ink', 'Text, dark backgrounds'), ('F5A524', 'Amber', 'Celebrations and progress'), ('F4F6F3', 'Paper', 'Light background')])
                      + typeface('"Sora", system-ui, sans-serif', 'Sora', weights='SemiBold · section headings, with SF Pro for the app', tint='#0F9D7A'), 'From the brand kit', '#0F9D7A'))

# ------------------------------------------------------------------ Greenlife (grocery shopping app, Behance 109365235)
GL_FONT = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo+Narrow:wght@500;600;700&amp;family=Open+Sans:wght@400;600&amp;display=swap">'
GL_MARK = ('<svg class="gl-mark" viewBox="0 0 48 64" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round">'
           '<path d="M24 3C36 11 38 25 30 32c-4 3.5-10 3.5-13 0-4-4-2-11 4-11 4 0 6 4 4 7"/><path d="M24 3C12 11 10 25 17 32c-8 6-7 20 3 23 8 2 14-4 11-11-2-4-7-5-9-2"/></svg>')
GL_ICONS = {
    'mail': '<path d="M3 6h18v12H3z"/><path d="M3 7l9 6 9-6"/>',
    'lock': '<rect x="5" y="10" width="14" height="10" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>',
    'user': '<circle cx="12" cy="8" r="4"/><path d="M4 20c1.5-4 4.5-6 8-6s6.5 2 8 6"/>',
    'search': '<circle cx="11" cy="11" r="6"/><path d="M20 20l-4.5-4.5"/>',
    'back': '<path d="M19 12H5M11 6l-6 6 6 6"/>',
    'leaf': '<path d="M5 19c0-9 6-14 14-14 0 8-5 14-14 14z"/><path d="M5 19l8-8"/>',
    'list': '<path d="M8 7h12M8 12h12M8 17h12M4 7h.01M4 12h.01M4 17h.01"/>',
    'cart': '<path d="M3 4h3l2 11h11l2-8H7"/><circle cx="10" cy="19" r="1.4"/><circle cx="18" cy="19" r="1.4"/>',
    'gear': '<circle cx="12" cy="12" r="3"/><path d="M12 3v3M12 18v3M3 12h3M18 12h3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M5.6 18.4l2.1-2.1M16.3 7.7l2.1-2.1"/>',
    'close': '<path d="M6 6l12 12M18 6L6 18"/>',
}
def gl_ic(name, cls='gl-ic'):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true">{GL_ICONS[name]}</svg>'

def gl_tabs(on='leaf', badge=''):
    def t(n):
        b = f'<sup>{badge}</sup>' if (n == 'cart' and badge) else ''
        return f'<span class="{"on" if n == on else ""}">{gl_ic(n)}{b}</span>'
    return f'<div class="gl-tabs">{t("leaf")}{t("list")}<b>+</b>{t("cart")}{t("gear")}</div>'

def gl_screens():
    s = []
    s.append(phone(status() + f'<div class="gl-body gl-splash">{GL_MARK}</div>', 'gl-app', 'Splash'))
    s.append(phone(status() + f'<div class="gl-body gl-auth"><p class="gl-h">Sign In</p><div class="gl-in">{gl_ic("mail")}Email</div><div class="gl-in">{gl_ic("lock")}Password</div>'
                   f'<p class="gl-small">Forgot password?</p><span class="gl-btn">→ SIGN IN</span><p class="gl-foot">CREATE ACCOUNT</p></div>', 'gl-app', 'Sign in'))
    s.append(phone(status() + f'<div class="gl-body gl-auth"><span class="gl-x">{gl_ic("close")}</span><p class="gl-h">Create Account</p><div class="gl-in">{gl_ic("user")}Full Name</div>'
                   f'<div class="gl-in">{gl_ic("mail")}Email</div><div class="gl-in">{gl_ic("lock")}Password</div><span class="gl-btn">→ CREATE ACCOUNT</span><p class="gl-foot">SIGN IN</p></div>', 'gl-app', 'Create account'))
    for i, (emo, text) in enumerate([('🛒', 'Quickly search and add healthy foods to your cart'), ('📋', 'With one click you can add every ingredient for a recipe to your cart')]):
        dots = ''.join(f'<i class="{"on" if k == i else ""}"></i>' for k in range(3))
        s.append(phone(status() + f'<div class="gl-body gl-onb"><div class="gl-blob"><span>{emo}</span><em>+</em><em>○</em></div><p>{text}</p><div class="gl-dots">{dots}</div><p class="gl-foot">SKIP</p></div>', 'gl-app', f'Onboarding {i + 1}'))
    tiles = ''.join(f'<span class="gl-tile" style="background:{bg}"><i>{e}</i>{n}</span>' for e, n, bg in [('🍓', 'Berries', '#E0393E'), ('🍊', 'Citrus', '#FFA200'), ('🍋', 'Lemons', '#FFD43B')])
    s.append(phone(status() + f'<div class="gl-body"><div class="gl-top"><span></span><b>Store</b>{gl_ic("search")}</div><div class="gl-hero">🥦</div>'
                   f'<p class="gl-cat">Vegetables</p><p class="gl-sub">Browse</p><div class="gl-tiles">{tiles}</div></div>{gl_tabs("leaf")}', 'gl-app', 'Store'))
    s.append(phone(status() + f'<div class="gl-body"><div class="gl-top">{gl_ic("back")}<b>Broccoli</b><span></span></div><div class="gl-hero">🥦</div>'
                   '<div class="gl-pick"><small>Broccoli</small><div class="gl-wheel"><span><i>1</i><b>2</b><i>3</i></span><span><i>grams</i><b>lbs</b><i>heads</i><i>packs</i></span></div><em>£0.80</em></div>'
                   '<span class="gl-btn">→ SELECT</span></div>', 'gl-app', 'Product'))
    rows = ''.join(f'<li><i>{e}</i><span><b>{n}</b><small>{q}</small></span><em>{p}</em></li>' for e, n, q, p in
                   [('🥦', 'Broccoli', '2 lbs', '£0.80'), ('🥬', 'Kale', '300g', '£3.00'), ('🫑', 'Red Peppers', '5', '£1.50'), ('🍓', 'Strawberries', '2 punnets', '£4.00')])
    s.append(phone(status() + f'<div class="gl-body"><div class="gl-top"><span></span><b>Cart</b><span></span></div><ul class="gl-rows">{rows}</ul>'
                   '<div class="gl-sum"><p><span>Sub-total</span><span>£9.30</span></p><p><span>Delivery</span><span>Standard (free)</span></p><p class="tot"><span>Total</span><span>£9.30</span></p></div>'
                   f'<span class="gl-btn">→ CHECKOUT</span></div>{gl_tabs("cart", "4")}', 'gl-app', 'Cart'))
    s.append(phone(status() + f'<div class="gl-body"><div class="gl-top">{gl_ic("back")}<b>Live Chat</b><span></span></div><div class="gl-chat">'
                   '<p class="them">Hi! Can I help you?</p><p class="me">Hello, I seem to be having some trouble with my order.</p>'
                   '<p class="them">Thanks for your patience. I’ve fixed it.</p><p class="me">Perfect. Thanks so much!</p><p class="them">You’re welcome!</p></div></div>', 'gl-app', 'Live chat'))
    s.append(phone(status() + f'<div class="gl-body gl-onb"><div class="gl-blob"><span>📦</span><em>+</em><em>○</em></div><p>Order placed.<br>Your order number is</p><strong class="gl-num">#5678</strong></div>{gl_tabs("cart")}', 'gl-app', 'Order placed'))
    return s

def gl_flow():
    def lane(name, steps):
        chips = '<i>→</i>'.join(f'<span class="{c}">{E(t)}</span>' for t, c in steps)
        return f'<div class="gl-lane" data-reveal><p class="mono">{E(name)}</p><div>{chips}</div></div>'
    return ('<div class="kit-block gl-flow"><p class="kit-label mono">User flow</p>'
            + lane('New user', [('Start', 'end'), ('Sign up', ''), ('Recipe preference', ''), ('Store', 'key')])
            + lane('Returning user', [('Start', 'end'), ('Login', ''), ('Store', 'key')])
            + lane('Search', [('Store', 'key'), ('Search', ''), ('Select item', ''), ('Item description', ''), ('Quantity', ''), ('Address & option', ''), ('Payment method', ''), ('Place order', ''), ('End', 'end')])
            + lane('Quick shop', [('Store', 'key'), ('Quick shop', ''), ('Quantity', ''), ('Address & option', ''), ('Payment method', ''), ('Place order', ''), ('End', 'end')])
            + '</div>')

def gl_cover():
    sc = gl_screens()
    return stage(f'<div class="ks-brand gl-brand">{GL_MARK}<b>greenlife</b><span>Grocery shopping app · UX UI design</span></div><div class="ks-phones">{sc[5]}{sc[0]}</div>', 'gl-stage')

def gl_card_inner():
    sc = gl_screens()
    return f'<div class="ks-mini">{sc[5]}{sc[7]}</div>'

def gl_sections():
    sc = gl_screens()
    return (section('The design system.', palette([('09B44D', 'Green'), ('7DAF25', 'Leaf'), ('748A9D', 'Slate'), ('404E5A', 'Ink')]) +
                    typeface('"Archivo Narrow", system-ui, sans-serif', 'Acumin Variable Concept', shown_as='Archivo Narrow', weights='Medium · Semi Bold · Bold', tint='#09B44D') +
                    wireframes([['bar', 'hero', 'line', 'grid', 'tabs'], ['spacer', 'circle', 'btn'], ['bar', 'list', 'btn'], ['bar', 'hero', 'line', 'grid', 'tabs']], 'User experience: wireframes'), 'From the Behance board', '#09B44D')
            + section('From first tap to placed order.', gl_flow())
            + section('Sign in and sign up.', phones(sc[:3], 'Login screens'))
            + section('Onboarding.', '<p class="kit-quote" data-reveal>Welcome screens introduce new users to the main app features.</p>' + phones(sc[3:5], 'Welcome screens'))
            + section('The store, a product and the cart.', '<p class="kit-quote" data-reveal>Choose groceries by category, among popular items or special offers, or use the search button.</p>' + phones(sc[5:8], 'Main screens'))
            + section('Help and confirmation.', phones(sc[8:], 'Live chat and order placed')))

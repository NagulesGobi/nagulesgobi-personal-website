#!/usr/bin/env python3
"""Logo showcase boards for the work page gallery (Logos and identity).

Each brand gets one 1600 x 1200 board on its own ground: the app icon drawn the Apple way (layered
Liquid Glass: each layer lifted off the tile with its own shadow, highlight and glass rim), the
wordmark, the Dark and Tinted appearances and the palette. Every board is a different kind of
showcase: Xpense an exploded layer view, Tockbee a poster, FreshBit a home screen, Mistkite a
landscape and ngxo3 a stream overlay.

The layers, their order and their light and dark colours come from each app's own Icon Composer
setup (Xpense and FreshBit .icon files, the Tockbee layer kit). Mistkite and ngxo3 have no .icon
file, so their layers follow the same rules from their single-layer marks.

Run from the repository root, then rebuild the site:
    python3 source/brandboards/build_boards.py && python3 source/build.py
Needs rsvg-convert, ImageMagick (magick) and cwebp.
"""
import json, math, os, re, subprocess, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'src')
OUT = os.path.join(HERE, '..', 'assets', 'img', 'brand')
SIZES = os.path.join(HERE, '..', 'img-sizes.json')
W, H = 1600, 1200
TMP = tempfile.mkdtemp(prefix='boards-')

def read(name): return open(os.path.join(SRC, name)).read()
def attr(svg, name): return re.search(name + r'="([^"]+)"', svg).group(1)

# ------------------------------------------------------------------ Apple-style layered icon
def squircle(size=1024, n=5.0, steps=160):
    """Superellipse outline: the continuous-corner tile shape of an Apple app icon."""
    a = size / 2; pts = []
    for i in range(steps):
        t = 2 * math.pi * i / steps; c, s = math.cos(t), math.sin(t)
        x = a + a * math.copysign(abs(c) ** (2 / n), c); y = a + a * math.copysign(abs(s) ** (2 / n), s)
        pts.append(f'{x:.1f} {y:.1f}')
    return 'M' + ' L'.join(pts) + 'Z'
TILE_D = squircle()

def icon_svg(spec, look='light'):
    """One app icon as a 1024 x 1024 SVG. look: light, dark or tinted."""
    if look == 'tinted':
        bg = ('#232326', '#0E0E10', (0, 0, 0, 1))
    else:
        bg = spec['bg'][look]
    x1, y1, x2, y2 = bg[2]
    defs = (f'<linearGradient id="bg" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"><stop offset="0" stop-color="{bg[0]}"/><stop offset="1" stop-color="{bg[1]}"/></linearGradient>'
            '<linearGradient id="sheen" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".26"/><stop offset=".42" stop-color="#fff" stop-opacity="0"/>'
            '<stop offset=".85" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".12"/></linearGradient>'
            '<linearGradient id="spec" x1="0" y1="0" x2=".35" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".55"/><stop offset=".3" stop-color="#fff" stop-opacity=".14"/>'
            '<stop offset=".62" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".10"/></linearGradient>'
            '<filter id="ls" x="-30%" y="-30%" width="160%" height="170%"><feGaussianBlur stdDeviation="16"/><feOffset dy="20"/></filter>'
            f'<clipPath id="tile"><path d="{TILE_D}"/></clipPath>')
    body = ''
    n = len(spec['layers'])
    for i, L in enumerate(spec['layers']):
        if look == 'tinted':
            fill = spec['tint']; op = (.42 + .58 * (i + 1) / n) * L.get('op', 1)
        else:
            fill = L[look]; op = L.get('op', 1)
        sh_col = fill if L.get('shadow') == 'color' else '#000'
        sh_op = .42 if L.get('shadow') == 'color' else .30
        shp = L['shape']
        defs += f'<clipPath id="l{i}">{shp("")}</clipPath>'
        body += (f'<g opacity="{op:.3f}">'
                 f'<g filter="url(#ls)" opacity="{sh_op}">{shp(f"fill=\"{sh_col}\"")}</g>'
                 f'{shp(f"fill=\"{fill}\"")}'
                 f'{shp("fill=\"url(#spec)\"")}'
                 f'<g clip-path="url(#l{i})">{shp("fill=\"none\" stroke=\"#fff\" stroke-opacity=\".6\" stroke-width=\"12\"")}</g>'
                 '</g>')
    rim = f'<path d="{TILE_D}" fill="none" stroke="#fff" stroke-opacity=".38" stroke-width="7"/>'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024"><defs>{defs}</defs>'
            f'<g clip-path="url(#tile)"><rect width="1024" height="1024" fill="url(#bg)"/>{body}'
            f'<rect width="1024" height="1024" fill="url(#sheen)"/>{rim}</g></svg>')

def path_layer(d, transform='', evenodd=False):
    t = f' transform="{transform}"' if transform else ''
    r = ' fill-rule="evenodd" clip-rule="evenodd"' if evenodd else ''
    return lambda a: f'<path d="{d}"{r}{t} {a}/>'

# ------------------------------------------------------------------ the five icons
DIAG = (0, 0, 1, 1); DOWN = (0, 0, 0, 1)

XPENSE = dict(tint='#3DD6A8',
    bg={'light': ('#14B08A', '#0A7D61', DIAG), 'dark': ('#0D4D3B', '#05241B', DIAG)},
    layers=[dict(shape=path_layer(attr(read('xpense-layer-last-month.svg'), ' d')), light='#FFFFFF', dark='#FFFFFF', op=.35),
            dict(shape=path_layer(attr(read('xpense-layer-kept.svg'), ' d')), light='#F5A524', dark='#F5A524'),
            dict(shape=path_layer(attr(read('xpense-layer-this-month.svg'), ' d')), light='#FFFFFF', dark='#FFFFFF')])

TB = 'scale(10.24) translate(50 50) scale(.7) translate(-50 -50)'
TOCKBEE = dict(tint='#FFB627',
    bg={'light': ('#FF7A2F', '#FF4F5A', DOWN), 'dark': ('#3A2219', '#1C100C', DOWN)},
    layers=[dict(shape=path_layer(attr(read('tockbee-layer-1-ring.svg'), ' d'), TB, True), light='#FFF6E8', dark='#FFF6E8'),
            dict(shape=lambda a: f'<rect x="45" y="45" width="41" height="10" rx="5" transform="{TB} rotate(-45 50 50)" {a}/>', light='#2A1712', dark='#FFB627'),
            dict(shape=lambda a: f'<circle cx="71.92" cy="28.08" r="11" transform="{TB}" {a}/>', light='#FFB627', dark='#FF4F5A')])

# FreshBit: the bit is a round-capped line in the .icon file; drawn here as the same capsule so it can be clipped
FRESHBIT = dict(tint='#C8F550',
    bg={'light': ('#D9FA79', '#B4EA38', (.2, 0, .8, 1)), 'dark': ('#1A2B1F', '#0B120D', (.2, 0, .8, 1))},
    layers=[dict(shape=path_layer(attr(read('freshbit-layer-leaf.svg'), ' d'), '', True), light='#0E1A12', dark='#C8F550'),
            dict(shape=lambda a: f'<rect x="313.22" y="490" width="407.55" height="54" rx="27" transform="translate(18 -18) rotate(-45 517 517)" {a}/>',
                 light='#FFFFFF', dark='#0E1A12', shadow='color')])

# Mistkite: the kite is cut by a band of mist; the two pieces become two layers
MK = 'translate(512 512) scale(8.4) translate(-48.2 -46.9)'
MISTKITE = dict(tint='#FF8A3D',
    bg={'light': ('#FF8A3D', '#F2436F', (0, 0, .45, 1)), 'dark': ('#2A2230', '#15121A', (0, 0, .45, 1))},
    layers=[dict(shape=path_layer('M42.7 14.9 L67.1 32.0 L61.91 61 L44.67 61 L29.3 41.4 Z', MK), light='#F7F2EC', dark='#FF8A3D'),
            dict(shape=path_layer('M60.56 68.5 L58.7 78.9 L50.55 68.5 Z', MK), light='#F7F2EC', dark='#F2436F')])

# ngxo3: bars measured from the owner's 800 x 800 icon (70 wide, slope 1:3, gaps 40, heights 120 / 220 / 320)
BARS = [((200, 550), (240, 430), (310, 430), (270, 550)),
        ((310, 550), (383.33, 330), (453.33, 330), (380, 550)),
        ((420, 550), (526.67, 230), (596.67, 230), (490, 550))]
def bar_d(b): return 'M' + ' L'.join(f'{x:g} {y:g}' for x, y in b) + 'Z'
NG_S = 1.28 * .92
NG_T = f'translate({512 - 398.33 * NG_S:.2f} {512 - 390 * NG_S:.2f}) scale({NG_S})'
NG_RED, NG_WHITE, NG_INK = '#FF2E3E', '#F2F0EB', '#0B0B0D'
NGXO3 = dict(tint='#FF2E3E',
    bg={'light': ('#2A0D12', '#0B0B0D', (0, 0, .6, 1)), 'dark': ('#141416', '#060607', (0, 0, .6, 1))},
    layers=[dict(shape=path_layer(bar_d(b), NG_T), light=NG_RED, dark=NG_RED, shadow='color') for b in BARS])

# ------------------------------------------------------------------ ngxo3 wordmark, redrawn as vectors
# Letters drawn upright on a 112 x 152 cell (40-unit strokes, chamfered corners), slanted 1:3 like the bars.
LW, LH, K = 112, 152, 1 / 3
def sx(x): return round(x * LW / 120, 2)
def sy(y): return round(y * LH / 150, 2)
def poly(pts): return 'M' + ' L'.join(f'{sx(x)} {sy(y)}' for x, y in pts) + 'Z'
GLYPHS = {
    'N': poly([(0, 150), (0, 0), (46, 0), (80, 104), (80, 0), (120, 0), (120, 150), (74, 150), (40, 46), (40, 150)]),
    'G': poly([(0, 30), (30, 0), (120, 0), (120, 38), (40, 38), (40, 112), (82, 112), (82, 100), (62, 100), (62, 66), (120, 66), (120, 120), (90, 150), (30, 150), (0, 120)]),
    'X': poly([(0, 0), (44, 0), (60, 44), (76, 0), (120, 0), (82, 75), (120, 150), (76, 150), (60, 106), (44, 150), (0, 150), (38, 75)]),
    '0': poly([(28, 0), (120, 0), (120, 122), (92, 150), (0, 150), (0, 28)]) + poly([(52, 38), (80, 38), (80, 100), (68, 112), (40, 112), (40, 50)]),
    '3': poly([(0, 0), (92, 0), (120, 28), (120, 62), (106, 75), (120, 88), (120, 122), (92, 150), (0, 150), (0, 112), (80, 112), (80, 94), (30, 94), (30, 56), (80, 56), (80, 38), (0, 38)]),
}
def ngxo3_wordmark():
    adv = LW + 24; out = ''
    for i, (ch, col) in enumerate(zip('NGX03', [NG_WHITE] * 3 + [NG_RED] * 2)):
        out += f'<path transform="translate({i * adv + K * LH:.2f} 0) skewX(-18.435)" fill="{col}" fill-rule="evenodd" d="{GLYPHS[ch]}"/>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {4 * adv + LW + K * LH:.2f} {LH}"><g id="wordmark">{out}</g></svg>'

def ngxo3_logo():
    """The full lockup (bars + NGX03) as a master file, same proportions as the owner's PNG."""
    s = 190 / 320; gap = 62; x0 = (596.67 - 200) * s + gap
    wm = re.search(r'<g id="wordmark">(.*)</g>', ngxo3_wordmark()).group(1)
    bars = ''.join(bar_d(b) for b in BARS)
    w = x0 + 4 * (LW + 24) + LW + K * LH
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -19 {w:.2f} 190"><title>ngxo3</title>'
            f'<g id="icon"><path transform="translate({-200 * s:.2f} {-19 - 230 * s:.2f}) scale({s:.5f})" fill="{NG_RED}" d="{bars}"/></g>'
            f'<g id="wordmark" transform="translate({x0:.2f} 0)">{wm}</g></svg>')

# ------------------------------------------------------------------ board helpers
_n = [0]
def embed(svg_text, x, y, w, h, crop=True):
    """Place an SVG inside the board, fitted to the box, ids made unique, optionally cropped to its ink."""
    _n[0] += 1; p = f'e{_n[0]}-'
    svg_text = re.sub(r'<\?xml[^>]*>', '', svg_text)
    vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', svg_text).group(1).replace(',', ' ').split()]
    if crop: vb = ink_box(svg_text, vb)
    inner = re.sub(r'^.*?<svg[^>]*>', '', svg_text, count=1, flags=re.S).rsplit('</svg>', 1)[0]
    inner = re.sub(r'<title>.*?</title>', '', inner)
    inner = re.sub(r'\bid="([^"]+)"', lambda m: f'id="{p}{m.group(1)}"', inner)
    inner = re.sub(r'url\(#([^)]+)\)', lambda m: f'url(#{p}{m.group(1)})', inner)
    return f'<svg x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" viewBox="{" ".join(f"{v:.3f}" for v in vb)}" preserveAspectRatio="xMidYMid meet" overflow="visible">{inner}</svg>'

def ink_box(svg_text, vb):
    f = os.path.join(TMP, 'probe.svg'); open(f, 'w').write(svg_text)
    scale = 2000 / max(vb[2], vb[3]); png = os.path.join(TMP, 'probe.png')
    subprocess.run(['rsvg-convert', '-w', str(round(vb[2] * scale)), f, '-o', png], check=True, env=ENV)
    g = subprocess.run(['magick', png, '-alpha', 'extract', '-threshold', '2%', '-format', '%@', 'info:'], capture_output=True, text=True).stdout
    m = re.match(r'(\d+)x(\d+)\+(\d+)\+(\d+)', g)
    if not m: return vb
    bw, bh, bx, by = (int(v) for v in m.groups())
    return [vb[0] + bx / scale, vb[1] + by / scale, bw / scale, bh / scale]

def box(svg_text):
    vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', svg_text).group(1).split()]
    return ink_box(svg_text, vb)

SHADOW = ('<filter id="sh" filterUnits="userSpaceOnUse" x="-400" y="-400" width="2600" height="2000"><feGaussianBlur in="SourceAlpha" stdDeviation="22"/><feOffset dy="26"/>'
          '<feComponentTransfer><feFuncA type="linear" slope=".38"/></feComponentTransfer><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>')

def hero(spec, mark_svg=None, text=None, mark_h=150):
    """Big light-appearance icon, with the wordmark (an SVG, or a text element) to its right."""
    S, gap, cy = 400, 78, 450
    if mark_svg:
        b = box(mark_svg); mw = b[2] * mark_h / b[3]
    elif text:
        mw = text[1]
    else:
        mw = 0; gap = 0
    x0 = 800 - (S + gap + mw) / 2
    out = f'<g filter="url(#sh)">{embed(icon_svg(spec, "light"), x0, cy - S / 2, S, S, crop=False)}</g>'
    if mark_svg:
        out += embed(mark_svg, x0 + S + gap, cy - mark_h / 2, mw, mark_h)
    elif text:
        out += text[0](x0 + S + gap, cy)
    return out

TS, TY = 178, 920
def footer(spec, cols, ring):
    out = ''
    for i, look in enumerate(('dark', 'tinted')):
        x = 120 + i * (TS + 34)
        out += f'<g filter="url(#sh)">{embed(icon_svg(spec, look), x, TY, TS, TS, crop=False)}</g>'
    r, step = 23, 64; x = W - 120 - r - (len(cols) - 1) * step
    for i, c in enumerate(cols):
        out += f'<circle cx="{x + i * step}" cy="{TY + TS / 2}" r="{r}" fill="{c}" stroke="{ring}" stroke-width="1.5"/>'
    return out

BOARD_SIZE = {}
def board(slug, ground, body, w=W, h=H):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {w} {h}" width="{w}" height="{h}"><defs>{SHADOW}</defs>{ground}{body}</svg>')
    f = os.path.join(TMP, slug + '.svg'); open(f, 'w').write(svg)
    png = os.path.join(TMP, slug + '.png')
    BOARD_SIZE[f'brand/board-{slug}'] = [w, h]
    subprocess.run(['rsvg-convert', '-w', str(w), '-h', str(h), f, '-o', png], check=True, env=ENV)
    subprocess.run(['cwebp', '-quiet', '-q', '90', png, '-o', os.path.join(OUT, f'board-{slug}.webp')], check=True)
    return f'brand/board-{slug}'

def glow(c, op, cx=800, cy=450, r=760):
    return (f'<radialGradient id="g-{c[1:]}" cx="{cx}" cy="{cy}" r="{r}" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="{c}" stop-opacity="{op}"/>'
            f'<stop offset="1" stop-color="{c}" stop-opacity="0"/></radialGradient><rect width="{W}" height="{H}" fill="url(#g-{c[1:]})"/>')

FONTCONF = os.path.join(TMP, 'fonts.conf')
open(FONTCONF, 'w').write(f'<?xml version="1.0"?><!DOCTYPE fontconfig SYSTEM "fonts.dtd"><fontconfig><include ignore_missing="yes">/opt/homebrew/etc/fonts/fonts.conf</include>'
                          f'<dir>{os.path.join(HERE, "fonts")}</dir><cachedir>{TMP}/fc</cachedir></fontconfig>')
ENV = dict(os.environ, FONTCONFIG_FILE=FONTCONF)

# ------------------------------------------------------------------ boards: five different showcases
def icon_at(spec, look, x, y, s, shadow=True):
    e = embed(icon_svg(spec, look), x, y, s, s, crop=False)
    return f'<g filter="url(#sh)">{e}</g>' if shadow else e

def dots(cols, x, y, ring, step=58, r=21):
    return ''.join(f'<circle cx="{x + i * step}" cy="{y}" r="{r}" fill="{c}" stroke="{ring}" stroke-width="1.5"/>' for i, c in enumerate(cols))

def label(x, y, txt, fill, size=22, font='Menlo', weight=400, anchor='start', op=1):
    return f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" fill="{fill}" fill-opacity="{op}" text-anchor="{anchor}">{txt}</text>'

def xpense():
    """Exploded view, the way Icon Composer shows a layered icon: the mint tile and the three bars float apart
    in depth. Beside it the wordmark, what each bar means (the brand's own words), the three appearances and
    the icon at 64, 32 and 16 px."""
    w, h = 1600, 1200
    INK, PAPER, AMBER, MINT, MINT_T = '#0E1512', '#F4F6F3', '#F5A524', '#0F9D7A', '#3DD6A8'
    ground = f'<rect width="{w}" height="{h}" fill="{INK}"/>' + glow('#0F9D7A', .3, 420, 640, 700)
    # isometric planes
    cx, cy, S, D = 420, 760, 470, 118
    k = S / 1024
    def plane(i, inner, extra=''):
        t = f'translate({cx} {cy - i * D}) matrix(.7071 .4082 -.7071 .4082 0 0) translate({-512 * k:.2f} {-512 * k:.2f}) scale({k:.5f})'
        return f'<g filter="url(#sh)"><g transform="{t}" {extra}>{inner}</g></g>'
    def pt(i, x, y):
        X, Y = (x - 512) * k, (y - 512) * k
        return cx + .7071 * X - .7071 * Y, cy - i * D + .4082 * X + .4082 * Y
    tile = ('<defs><linearGradient id="xt" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#14B08A"/><stop offset="1" stop-color="#0A7D61"/></linearGradient></defs>'
            f'<path d="{TILE_D}" fill="url(#xt)"/><path d="{TILE_D}" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width="8"/>')
    layers = [(read('xpense-layer-last-month.svg'), '#FFFFFF', .35), (read('xpense-layer-kept.svg'), AMBER, 1), (read('xpense-layer-this-month.svg'), '#FFFFFF', 1)]
    guides = ''
    for (x, y) in ((0, 1024), (1024, 0), (1024, 1024)):
        x1, y1 = pt(0, x, y); x2, y2 = pt(3, x, y)
        guides += f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{MINT_T}" stroke-opacity=".35" stroke-width="1.5" stroke-dasharray="6 8"/>'
    stack = plane(0, tile)
    for i, (svg, fill, op) in enumerate(layers, 1):
        d = attr(svg, ' d')
        ghost = f'<path d="{TILE_D}" fill="#FFFFFF" fill-opacity=".035" stroke="#FFFFFF" stroke-opacity=".16" stroke-width="5"/>'
        stack += plane(i, ghost + f'<path d="{d}" fill="{fill}" fill-opacity="{op}"/><path d="{d}" fill="none" stroke="#fff" stroke-opacity=".55" stroke-width="10"/>')
    # layer numbers beside the stack
    nums = ''
    for i, name in enumerate(('Tile', 'Last month', 'Kept', 'This month')):
        x, y = pt(i, 1024, 512)
        nums += (f'<line x1="{x + 14:.0f}" y1="{y:.0f}" x2="{cx + 360:.0f}" y2="{y:.0f}" stroke="{MINT_T}" stroke-opacity=".45" stroke-width="1.5" stroke-dasharray="2 5"/>'
                 + label(cx + 372, y + 6, f'{i:02d}  {name}', PAPER, 18, op=.75))
    # right column
    rx = 1010
    right = (embed(read('xpense-wordmark-dark.svg'), rx, 150, 420, 110)
             + label(rx, 330, 'The logo is two bars.', PAPER, 40, 'Sora', 600))
    rows = [(f'<rect x="{rx}" y="{{y}}" width="120" height="30" rx="15" fill="{MINT}" fill-opacity=".45"/>', 'Faint: last month.'),
            (f'<rect x="{rx}" y="{{y}}" width="120" height="30" rx="15" fill="#FFFFFF"/>', 'White: this month.'),
            (f'<rect x="{rx}" y="{{y}}" width="120" height="30" rx="15" fill="{AMBER}"/>', 'Amber: what you kept.')]
    for j, (shape, text) in enumerate(rows):
        y = 384 + j * 62
        right += shape.format(y=y) + label(rx + 148, y + 23, text, PAPER, 28, 'Sora', 600, op=.85)
    looks = ''
    for j, look in enumerate(('light', 'dark', 'tinted')):
        x = rx + j * 196
        looks += icon_at(XPENSE, look, x, 640, 160) + label(x + 80, 840, look.capitalize(), PAPER, 20, op=.6, anchor='middle')
    sizes = ''
    x = rx
    for size in (64, 32, 16):
        sizes += embed(icon_svg(XPENSE, 'light'), x, 950 + (64 - size) / 2, size, size, crop=False) + label(x + size / 2, 1046, f'{size} px', PAPER, 18, op=.55, anchor='middle')
        x += size + 64
    rule = f'<line x1="{rx}" y1="900" x2="{rx + 560}" y2="900" stroke="{MINT_T}" stroke-opacity=".25" stroke-width="1.5"/>'
    return board('xpense', ground, guides + stack + nums + right + looks + rule + sizes, w, h)

def tockbee():
    """Warm poster: the mark huge and cropped by the edge, the app icon and wordmark set small beside it."""
    COCOA, CREAM = '#2A1712', '#FFF6E8'
    ground = (f'<rect width="1600" height="1200" fill="{CREAM}"/>' + glow('#FFB627', .45, 1240, 600, 820)
              + '<circle cx="1240" cy="610" r="560" fill="#FFB627" fill-opacity=".14"/>')
    big = embed(read('tockbee-logo.svg'), 760, 120, 1000, 1000, crop=False)
    left = (icon_at(TOCKBEE, 'light', 130, 170, 260)
            + f'<text x="122" y="640" font-family="Fredoka" font-weight="600" font-size="190" letter-spacing="-4" fill="{COCOA}">tockbee</text>'
            + f'<rect x="130" y="700" width="92" height="10" rx="5" fill="#FF7A2F"/>')
    foot = (icon_at(TOCKBEE, 'dark', 130, 900, 150) + icon_at(TOCKBEE, 'tinted', 310, 900, 150)
            + dots(['#FF7A2F', '#FF4F5A', '#FFB627', '#C2361F', COCOA], 530, 975, 'rgba(42,23,18,.15)'))
    return board('tockbee', ground, big + left + foot)

def freshbit():
    """In context: the icon on a home screen, among blank glass placeholders, beside the wordmark."""
    INK, LIME = '#0E1A12', '#C8F550'
    ground = f'<rect width="1600" height="1200" fill="{LIME}"/>' + glow('#F2FFC4', .85, 0, 0, 1500)
    # the phone screen
    px, py, pw, ph = 880, 90, 600, 1020
    screen = (f'<g filter="url(#sh)"><rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="96" fill="#0B120D"/></g>'
              f'<linearGradient id="wall" x1="0" y1="0" x2=".6" y2="1"><stop offset="0" stop-color="#1A2B1F"/><stop offset="1" stop-color="#0B120D"/></linearGradient>'
              f'<rect x="{px + 14}" y="{py + 14}" width="{pw - 28}" height="{ph - 28}" rx="84" fill="url(#wall)"/>'
              f'<rect x="{px + pw / 2 - 70}" y="{py + 34}" width="140" height="40" rx="20" fill="#000"/>')
    s, gx, gy, step = 104, px + 58, py + 170, 128
    apps = ''
    for r in range(4):
        for c in range(4):
            ax, ay = gx + c * step, gy + r * 150
            if (r, c) == (1, 1):
                apps += icon_at(FRESHBIT, 'light', ax, ay, s) + label(ax + s / 2, ay + s + 30, 'FreshBit', '#FFFFFF', 21, 'Helvetica Neue', 500, 'middle')
            else:
                apps += (f'<path transform="translate({ax} {ay}) scale({s / 1024})" d="{TILE_D}" fill="#FFFFFF" fill-opacity=".08" stroke="#FFFFFF" stroke-opacity=".12" stroke-width="10"/>'
                         f'<rect x="{ax + 26}" y="{ay + s + 18}" width="{s - 52}" height="9" rx="4.5" fill="#FFFFFF" fill-opacity=".12"/>')
    dock_y = py + ph - 170
    dock = f'<rect x="{px + 34}" y="{dock_y}" width="{pw - 68}" height="136" rx="44" fill="#FFFFFF" fill-opacity=".10"/>'
    for c in range(4):
        ax = gx + c * step
        dock += f'<path transform="translate({ax} {dock_y + 16}) scale({s / 1024})" d="{TILE_D}" fill="#FFFFFF" fill-opacity=".10"/>'
    wm = embed(re.sub(r'<g id="icon".*?</g>', '', read('freshbit-logo.svg'), flags=re.S), 120, 300, 640, 120)
    left = (wm + label(124, 490, 'Confirmed news for designers and developers.', INK, 26, 'Helvetica Neue', 500, op=.75)
            + icon_at(FRESHBIT, 'light', 120, 620, 170) + icon_at(FRESHBIT, 'dark', 320, 620, 170) + icon_at(FRESHBIT, 'tinted', 520, 620, 170)
            + label(205, 830, 'Default', INK, 20, op=.6, anchor='middle') + label(405, 830, 'Dark', INK, 20, op=.6, anchor='middle') + label(605, 830, 'Tinted', INK, 20, op=.6, anchor='middle')
            + dots(['#D9FA79', LIME, '#B4EA38', INK], 141, 975, 'rgba(14,26,18,.22)'))
    return board('freshbit', ground, screen + apps + dock + left)

def mistkite():
    """Atmosphere: the kite flies over misty ridges at dusk, its string running down to the hills."""
    INK, PAPER, MIST = '#15121A', '#F7F2EC', '#BDB5C6'
    sky = ('<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#15121A"/><stop offset=".45" stop-color="#4A2236"/>'
           '<stop offset=".72" stop-color="#F2436F"/><stop offset=".9" stop-color="#FF8A3D"/></linearGradient><rect width="1600" height="1200" fill="url(#sky)"/>'
           '<circle cx="1120" cy="905" r="120" fill="#FFB27A" fill-opacity=".55"/>')
    ridges = (f'<path d="M0 860 C180 800 300 820 430 760 C560 700 640 760 780 790 C930 820 1040 720 1200 730 C1360 740 1480 800 1600 780 V1200 H0Z" fill="{MIST}" fill-opacity=".55"/>'
              '<rect y="840" width="1600" height="60" fill="#FFFFFF" fill-opacity=".10"/>'
              f'<path d="M0 940 C150 900 280 930 420 880 C560 830 700 900 860 920 C1010 940 1120 860 1290 870 C1440 880 1520 930 1600 920 V1200 H0Z" fill="#5C5068"/>'
              '<rect y="935" width="1600" height="50" fill="#FFFFFF" fill-opacity=".07"/>'
              f'<path d="M0 1030 C200 990 360 1020 520 990 C700 955 820 1010 1000 1020 C1200 1030 1340 980 1600 1000 V1200 H0Z" fill="{INK}"/>')
    s, kx, ky = 300, 650, 230
    string = f'<path d="M{kx + s * .55} {ky + s * .97} C {kx + 260} {ky + 520}, {kx + 120} {ky + 640}, {kx + 360} {ky + 860}" fill="none" stroke="{PAPER}" stroke-opacity=".7" stroke-width="2.5"/>'
    foot = (icon_at(MISTKITE, 'dark', 120, 1040, 120) + icon_at(MISTKITE, 'tinted', 266, 1040, 120)
            + dots(['#FF8A3D', '#F2436F', MIST, PAPER, INK], 1240, 1100, 'rgba(247,242,236,.3)'))
    return board('mistkite', sky + ridges, string + icon_at(MISTKITE, 'light', kx, ky, s) + foot)

def ngxo3():
    """Stream overlay: angled panels, a ghosted 03 and the full lockup, framed like a broadcast."""
    lines = ''.join(f'<line x1="{x}" y1="1200" x2="{x + 400}" y2="0" stroke="#FFFFFF" stroke-opacity=".035" stroke-width="1.5"/>' for x in range(-400, 1700, 30))
    ground = (f'<rect width="1600" height="1200" fill="{NG_INK}"/>{lines}' + glow('#FF2E3E', .2, 820, 520, 700)
              + '<path d="M1210 0 H1330 L930 1200 H810 Z" fill="#FF2E3E" fill-opacity=".08"/>')
    ghost = ''.join(f'<path transform="translate({840 + i * 330 + K * LH * 2.7:.0f} 140) scale(2.7) skewX(-18.435)" fill="none" stroke="#FF2E3E" stroke-opacity=".16" stroke-width="1.2" fill-rule="evenodd" d="{GLYPHS[ch]}"/>'
                    for i, ch in enumerate('03'))
    panel = '<path d="M210 360 H1450 L1360 640 H120 Z" fill="#FFFFFF" fill-opacity=".035"/><path d="M210 360 H1450" stroke="#FF2E3E" stroke-width="4"/>'
    lockup = fit_svg(ngxo3_logo(), 790, 500, 1160, 250)
    br = ''
    for (cx, cy, dx, dy) in ((60, 60, 1, 1), (1540, 60, -1, 1), (60, 1140, 1, -1), (1540, 1140, -1, -1)):
        br += f'<path d="M{cx} {cy + dy * 70} V{cy} H{cx + dx * 70}" fill="none" stroke="{NG_WHITE}" stroke-opacity=".55" stroke-width="4"/>'
    foot = (icon_at(NGXO3, 'light', 140, 880, 190) + icon_at(NGXO3, 'tinted', 360, 880, 190)
            + dots([NG_RED, NG_WHITE, '#2A0D12'], 1300, 975, 'rgba(255,255,255,.3)'))
    return board('ngxo3', ground, ghost + panel + lockup + br + foot)

def fit_svg(svg_text, cx, cy, maxw, maxh):
    b = box(svg_text); s = min(maxw / b[2], maxh / b[3]); w, h = b[2] * s, b[3] * s
    return embed(svg_text, cx - w / 2, cy - h / 2, w, h)

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    # keep the redrawn ngxo3 masters and every layered icon next to the other sources
    open(os.path.join(SRC, 'ngxo3-logo.svg'), 'w').write(ngxo3_logo())
    open(os.path.join(SRC, 'ngxo3-wordmark.svg'), 'w').write(ngxo3_wordmark())
    for name, spec in (('xpense', XPENSE), ('tockbee', TOCKBEE), ('freshbit', FRESHBIT), ('mistkite', MISTKITE), ('ngxo3', NGXO3)):
        for look in ('light', 'dark', 'tinted'):
            open(os.path.join(SRC, f'{name}-layered-{look}.svg'), 'w').write(icon_svg(spec, look))
    sizes = json.load(open(SIZES))
    for fn in (xpense, tockbee, freshbit, mistkite, ngxo3):
        key = fn(); sizes[key] = BOARD_SIZE[key]; print('built', key)
    json.dump(sizes, open(SIZES, 'w'))

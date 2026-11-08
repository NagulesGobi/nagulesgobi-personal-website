# Handoff: nagulesgobi.com redesign

Give this file to a new Claude session to continue the work. Everything below was
decided or built in the first session (7 November 2026).

## 1. Who and what

- **Owner:** Gobikrishna Naguleswararajah, known as **Nagules Gobi**.
- **Title on the site:** **Product designer** (keep this title). He also builds with code and
  **AI-assisted development**. Do not use the phrase "vibe coding" on the site.
- **Company:** Director of **dotXline LTD**, a product company in Cardiff, United Kingdom
  (website dotxline.com, repo `NagulesGobi/dotxline-website`). It makes two apps:
  - **Xpense**: calm, native iPhone expense tracker. "Every penny, in plain sight." Coming soon.
  - **Tockbee**: shift and pay tracker for UK hourly workers, iPhone and Android.
    "Every hour you work, on the record."
- **Education:** BSc in Computing.
- **Experience claim (from his old site):** 30+ projects across 3 countries in 4 years (owner corrected this in Nov 2026).
- **Contact:** contact@nagulesgobi.com. Old site said "Based in London, UK"; dotXline is in
  Cardiff. The new site says "United Kingdom" generally and "Cardiff" for dotXline.
  **Open question:** which city he wants shown.
- **Goal:** a multi-page, highly animated UX/UI portfolio that makes people want to hire him,
  open to full-time product design roles and freelance projects.

## 2. Where everything lives

| What | Where |
|---|---|
| Website source and published files | GitHub `NagulesGobi/nagulesgobi-personal-website`, branch `main` (this repo) |
| Live domain | www.nagulesgobi.com (bought at Namecheap). **DNS not switched yet**, see section 6 |
| Private preview (claude.ai artifact) | https://claude.ai/artifact/SqwoU2FaqW6QFxAMXpC9xu |
| Older backup copy (can be deleted) | `NagulesGobi/dotxline-website`, branch `claude/run-remote-control-h0vg8f`, folder `nagulesgobi-portfolio/`. Do not merge that branch. |
| Old website (being replaced) | Hosted website builder (nginx, images on cloud-1de12d.becdn.net) |

## 3. Repository layout

| Path | Contents |
|---|---|
| `index.html` … `contact.html`, `work/*.html`, `404.html`, `graphicdesigner.html` | Generated pages (do not hand-edit) |
| `assets/` | Generated copy of CSS, JS, images, brand files |
| `source/build.py` | Generator. All page copy, header, menu, footer, project data live here |
| `source/assets/css/base.css` | Core design system: tokens, hero, marquee, horizontal work, services, FAQ, footer |
| `source/assets/css/pages.css` | Multi-page layer: nav, curtain, work index, case studies, gallery, lightbox, about, dotXline, contact |
| `source/assets/js/site.js` | All interactions (see section 5) |
| `source/assets/img/` | Optimised WebP images: `brand/`, `work/`, `apps/`, `me/` |
| `source/parts/` | Logo path data and the large footer wordmark path used by the build |
| `logo-kit/` | Logo masters, PNGs, web icons, `export/USAGE.md`; `mark2.py` holds the exact geometry |
| `CNAME` | `www.nagulesgobi.com` |
| `CLAUDE.md` | Short rules for Claude in this repo |

**Rebuild:** `python3 source/build.py` from the repo root, then commit source and output together.
**Preview:** `python3 -m http.server 8000` and open http://localhost:8000.

## 4. Pages

1. **Home** (`index.html`, redesigned Nov 2026: hero "I design the app. Then I build it myself.", mono facts strip, **My apps** section with working Xpense and Tockbee demos and App Store buttons, client work ledger, logos, services, How I build, pitch). Before that: intro loader (mark draws, 0–100% counter, curtain lifts, once per
   visit), particle N-mark hero with portrait chip, marquee of disciplines, stats (30 / 3 / 6),
   pinned horizontal "Selected work" with six panels, dotXline ventures strip, client logo
   marquee, services with spotlight borders, **How I build** (Design → Develop → Refine →
   Launch), "Why teams hire me", scroll-scrubbed pitch paragraph, footer CTA.
2. **Work** (`work.html`): filter chips (All, My apps, Web, Mobile, Brand) with FLIP animation,
   grid/list toggle, list view shows a cursor-following preview image.
3. **Case studies** (`work/`): `xpense`, `tockbee`, `chatvertiser`, `greenlife`, `puff-count`, `pocket`
   (Nov 2026: Puff Count replaced OmniGPS, Pocket replaced Quantum Vac; their old URLs forward to work.html). Facts row, cover with clip reveal and parallax, sections, 3D phone carousel
   for the apps, "Next case study" link.
4. **dotXline** (`dotxline.html`): company story (0 · × · 1), both apps with stacked screens,
   principles Clear / Calm / Private, link to dotxline.com.
5. **Brand** (merged into `work.html#brand` in Nov 2026; `brand.html` and `graphicdesigner.html` now forward there): 29 real pieces from the old site in a masonry gallery with filters
   (Logos and identity, Campaigns, Print, Packaging) and a full-screen lightbox (keys, swipe).
6. **About** (`about.html`): portrait, bio, facts, five-step process ending in "Build",
   six capability cards.
7. **Contact** (`contact.html`): form that composes a mailto email (chips: Full-time role,
   Freelance project, App design, Website, Brand identity, Design and build), copy-email button,
   FAQ including "Can you build what you design?" and "Are you open to full-time roles?".

## 5. Interactions (all hand-written, no libraries)

Particle logo (about 2,500 particles sampled from the real mark, cursor repulsion, click
shockwave), page curtain transitions, circular theme switch (View Transitions API), custom
cursor with labels and image preview, magnetic buttons, 3D tilt with glare, spotlight borders,
direction-aware hover fills, split-word headline reveals, image clip reveals, parallax, velocity
marquees, count-up stats, scroll-scrubbed text, pinned horizontal scroll, FLIP filters,
lightbox, animated FAQ, live London clock, mobile full-screen menu.
Everything respects `prefers-reduced-motion`; touch devices get no custom cursor and a vertical
work list. Pages were checked in a browser at 1440 px and iPhone width: no errors, no broken
images, no sideways scroll.

## 6. Still to do

1. **Turn on GitHub Pages:** repo Settings → Pages → Deploy from a branch → `main` / `(root)`;
   custom domain `www.nagulesgobi.com`; Enforce HTTPS once available.
2. **Fix Namecheap DNS.** GitHub reported `InvalidCNAMEError` and the domain still serves the old
   builder. In Namecheap:
   - Domain tab → Nameservers → **Namecheap BasicDNS** (if it says Custom DNS, that is the cause).
   - Advanced DNS → delete every `@` and `www` record except email (MX/TXT), then add:
     - `A` `@` → `185.199.108.153`
     - `A` `@` → `185.199.109.153`
     - `A` `@` → `185.199.110.153`
     - `A` `@` → `185.199.111.153`
     - `CNAME` `www` → `nagulesgobi.github.io` (no `https://`, host is just `www`)
   - Save each row with the green tick, wait 15–30 minutes, press "Check again" on GitHub Pages.
   - Best done in the Claude desktop app's built-in browser with the owner signing in himself.
     Never ask for the Namecheap password in chat.
3. Cancel the old website builder plan once www.nagulesgobi.com serves the new site.
4. Optional: delete the backup folder branch in `dotxline-website`.
5. Optional improvements the owner may send: real cover images for OmniGPS and Quantum Vac
   (they use designed CSS mock screens), a booking link (Calendly or similar), his tech stack
   (SwiftUI, React, Cursor, …) to name on the site, which city to show, corrections to brand
   piece names (for example "Sachet", "Humanity").

## 7. Brand system

- **Logo:** his N-mark (square frame with a diagonal, two rounded corners, a point that breaks
  the baseline). Rebuilt exactly as vector from his artwork (97.8% overlap): stroke = gap = 18%
  of the square, corner radius = S/2 − t/2, diagonal on the square's diagonal.
  Wordmark: "NAGULESGOBI" in Barlow Semi Condensed 600, tracking 0.06, near-black or white.
- **Gradient:** radial from the mark's top-left: `#FF9124` 0, `#FF4A2C` .3, `#FF2440` .55,
  `#FF008E` 1 (radius 1.45 × square).
- **Neutrals (Nov 2026 refresh):** warm paper `#F3EFE7`, card `#FBF9F4`, ink `#15130F`; dark theme bg `#12110F`,
  card `#1C1B18`. Mono labels in IBM Plex Mono.
- **Small accent text:** `#D6143A` on light, `#FF5C6E` on dark (WCAG AA). The bright gradient is
  only for large type, graphics and the logo.
- **Type:** display Barlow Semi Condensed 500–700, body Barlow 400–600 (Google Fonts, OFL).
- Logo checks passed with the logo-designer skill from `nkrrish/krrish-skills`: readable at
  16 px, works in one colour, clear of 3,467 known marks (nearest 0.233).

## 8. Content rules

- Use only facts from nagulesgobi.com and dotxline.com. Do not invent clients, metrics,
  testimonials or tools.
- Removed on purpose from the old site: the placeholder testimonial ("Clay … George Morley") and
  the stock curly-haired portrait (`Group45.png`); the old FAQ answers were mismatched and were
  rewritten without promises or prices.
- His real portraits: `source/assets/img/me/portrait.webp` (dotXline director photo) and
  `portrait-suit.webp` (from the old site).

## 9. Image sources

- From the old nagulesgobi.com and its `/graphicdesigner` page: client logos (Hanek, PhiNaturals,
  Nation Insure, Mr Physics, Chatvertiser, Cupid Theory) and brand, campaign and print work
  (Allura, Unlucky Ninja, Turmeric ad, Viviendo del Trade, Team Reddin, Humanity, Fanera,
  Cheat Court, Awesom, Handicap, Vacay360, Growing Together, Video Game Break, mushroom ad,
  FitFables, WappNegocio, calligraphy, Suomen Tulkkauspalvelut, Plegables, sachet, Tiquipaya,
  Whitsunday Kombi), plus Chatvertiser and Greenlife project images.
- From dotxline.com (`NagulesGobi/dotxline-website`): Xpense and Tockbee screens, icons, promo
  images, the dotXline logo and the director portrait.
- OmniGPS and Quantum Vac had no images; their visuals are CSS mock screens.

## 10. Prompt to start a new session

> Read HANDOFF.md and CLAUDE.md in this repository. Then help me finish section 6: turn on
> GitHub Pages and fix the Namecheap DNS for www.nagulesgobi.com using the built-in browser.
> I will sign in to Namecheap myself.

## 11. Behance sources (added Nov 2026)

Chatvertiser, Puff Count and Pocket (Personal Wallet App) case-study images are slices of the owner's
Behance boards: behance.net/gallery/224174429, /224174013 and /109368407. Files: `source/assets/img/work/cv-*`,
`pc-*`, `pw-*`. Pocket is co-owned on Behance with Muralikrishna Naguleswararajah and was made for Loofyn Hyper;
the case study credits both.

## 12. Nov 2026 additions

- **Header** is now a floating dock (`chrome()` in build.py; styles under "Dock header" in pages.css):
  icons magnify on hover like the macOS Dock; on phones it sits at the bottom. The full logo sits top-left.
- **Search**: ⌘K / Ctrl+K or "/" opens a palette of pages, case studies and home-page demos (`finder_items()`).
- **Case-study kit** (`source/kit.py`): Puff Count, Pocket and Chatvertiser use coded palettes, type specimens,
  wireframes and app screens rebuilt from the Behance boards, not pasted screenshots. Only the Puff Count app
  icon (`work/pc-icon.webp`) is an image. Fonts: Poppins (exact), Pocket's Circular Std shown in DM Sans,
  Chatvertiser's unnamed display face shown in Exo 2 (labelled on the page).
- Xpense and Tockbee cards use the coded phones; image hover previews only show in list layouts.
- Copy: 30+ projects, 4 years of experience.
- **Xpense and Tockbee** case studies now use the owner's brand kits (`assets/img/kit/`, `assets/video/`):
  real Tockbee screens in exact-shape device frames, the five Xpense App Store photos as an uncropped strip,
  compressed videos (540 px, H.264) with posters, palettes and fonts from each brand guideline
  (Tockbee: Fredoka, Cocoa text on orange; Xpense: Mint and Ink, Sora). Never crop brand images.
- Dock: the N-mark is the Home button; there is no separate Home icon or corner logo.
- dotXline uses its "Continuum" identity from dotxline-full-brand-kit (the correct kit): the mark in the dock
  (Amber #F5A524 on dark, Ember #D97706 on light), official one-colour-text lockups on the dotXline page,
  Ink #0E1512 / Paper #F4F6F3 hero. Mint belongs to Xpense; dotXline never uses it.
- Phones show no particle mark in the hero.

## 13. Nov 2026 polish round

- Wording: no "ship/shipped" anywhere (owner finds it unnatural). Say "designed and built", "My apps". Project count reads "30+ projects designed", never "shipped".
- Home hero: softer portrait ring; brand gradient sits on "myself." in the headline to balance the coloured mark. On desktop the mark is centred on the text block inside the 1240px column (site.js MarkField build), so wide screens stay aligned.
- Dock: the dotXline mark uses the same colour as the other dock icons.
- dotXline page hero now uses the site's own background, text and kicker colours; only the lockup carries the dotXline brand colours.
- App fans on dotXline stay inside their column on hover. "Read the case study" and the App Store badge are the same height and shape.
- Chatvertiser: the wide logo sits in `.logo-panel`, never cropped.
- Custom cursor: the press scale is part of the JS transform, so the ring no longer jumps away on click.

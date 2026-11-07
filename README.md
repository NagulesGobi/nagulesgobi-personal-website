# nagulesgobi.com

Portfolio website of **Nagules Gobi**, product designer and Director of dotXline LTD.
Published with GitHub Pages at **https://www.nagulesgobi.com**.

## What is where

| Path | What it is |
|---|---|
| `index.html`, `work.html`, `work/…`, `dotxline.html`, `brand.html`, `about.html`, `contact.html` | The published pages (generated, see below) |
| `assets/` | Generated copy of the styles, script and images the pages use |
| `source/build.py` | Generator for every page; shared header, menu, footer and all page copy live here |
| `source/assets/css/base.css`, `source/assets/css/pages.css` | Styles |
| `source/assets/js/site.js` | All interactions: particle logo, transitions, filters, lightbox, cursor |
| `source/assets/img/` | Optimised images (WebP) |
| `logo-kit/` | The N-mark logo: SVG masters, PNGs, web icons and `export/USAGE.md` |
| `CNAME` | Custom domain for GitHub Pages |

## Making changes

Edit files in `source/`, then rebuild from the repository root:

```bash
python3 source/build.py
```

This regenerates the pages and `assets/` at the root. Commit both the source and the
generated files; GitHub Pages serves the root of the `main` branch.

To preview locally: `python3 -m http.server 8000`, then open http://localhost:8000.

## Publishing settings

- GitHub: Settings → Pages → Deploy from a branch → `main` / `(root)`, custom domain
  `www.nagulesgobi.com`, Enforce HTTPS on.
- Namecheap DNS: `A` records for `@` → 185.199.108.153, 185.199.109.153, 185.199.110.153,
  185.199.111.153; `CNAME` for `www` → `nagulesgobi.github.io`. Email records untouched.

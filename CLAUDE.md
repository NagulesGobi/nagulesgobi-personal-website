# Notes for Claude

- This is a static site published by GitHub Pages from the root of `main`.
- Never hand-edit the generated pages at the root or `assets/`. Change `source/` and run
  `python3 source/build.py` from the repository root, then commit source and output together.
- Brand: N-mark radial gradient #FF9124 → #FF4A2C → #FF2440 → #FF008E on warm ink #12110F / #15130F and warm paper #F3EFE7. Gradient only for the logo and key moments.
  Display type Barlow Semi Condensed 600, body Barlow. Small accent text #D6143A (light) and
  #FF5C6E (dark) for contrast. Logo geometry lives in `logo-kit/mark2.py`.
- Copy must stay factual: content comes from nagulesgobi.com and dotxline.com. Do not invent
  clients, results, testimonials or tools. Title stays "Product designer"; building is described
  as "AI-assisted development", not "vibe coding".
- Respect `prefers-reduced-motion`, keep phones free of sideways scrolling, and check pages in
  a browser at desktop and phone width before pushing.
- App Store links (`APP_STORE` in `source/build.py`) point at dotxline.com until the owner sends the real App
  Store URLs. The new main pages link to the case studies instead; add store buttons in `source/motion.py` when the links exist.
- Xpense is built with SwiftUI, Tockbee with React Native; both are presented as live on the App Store.
- Home, work, about, contact and dotXline are built by `source/motion.py` (the dot-motion design: one WebGL dot
  canvas, `source/assets/motion/`, images in `source/assets/img/motion/`). Case studies, redirects and 404 still come
  from `source/build.py`. Its old `home()`, `work_index()`, `about()`, `contact()` and `dotxline()` are no longer
  called; the previous design is kept as the git tag `live-backup-2026-11-17`.
- The About page's "What went wrong" stories come from real fixes (FreshBit case study, Xpense and Tockbee commit
  history). Add new ones only from facts the owner gives.

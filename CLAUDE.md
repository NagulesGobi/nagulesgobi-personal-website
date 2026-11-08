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
- App Store links live in `APP_STORE` near the top of the home section of `source/build.py`. They point at
  dotxline.com until the owner sends the real App Store URLs.
- Xpense is built with SwiftUI, Tockbee with React Native; both are presented as live on the App Store.
- The home page phones in "My apps" are working HTML/CSS/JS demos (`[data-xpense]`, `[data-tockbee]` in site.js).

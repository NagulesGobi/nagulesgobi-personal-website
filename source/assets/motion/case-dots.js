/* Case study pages: the same dot engine as the main pages draws the project's mark in the hero.
   The case pages switch theme through assets/js/site.js, so tell the dots when data-theme changes. */
import { startDots } from './dots.js';
new MutationObserver(() => dispatchEvent(new Event('ng-theme'))).observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme', 'class'] });
startDots({ intro: false });

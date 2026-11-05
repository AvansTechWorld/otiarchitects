# OTI Architects website: quality, security and launch checklist

Last full test run: 6 November 2026 (Chromium, desktop 1366px and phone 390px, 19 pages).

## Results
| Area | Test | Result |
|---|---|---|
| Accessibility | axe-core, WCAG 2.0/2.1/2.2 A and AA plus best practice, every page, desktop and phone | 0 violations (404 page checked over HTTP) |
| Accessibility | Keyboard only: 44 tab stops, visible focus ring on every one, nothing hidden under the header | Pass |
| Accessibility | Colour contrast, page language, one h1 per page, heading order, landmarks, alt text | Pass |
| Accessibility | Reflow at 320px and 640px, text-spacing stress test (WCAG 1.4.12) | No sideways scroll, no clipped text |
| Accessibility | Pause control for moving content (WCAG 2.2.2) | "Pause animation" button on every page; remembers the choice |
| Accessibility | Respects "reduce motion" on the visitor's device | Motion off by default there; "Play animation" turns it on |
| Security | Content Security Policy: injected scripts and styles blocked during testing | Blocked |
| Security | Console errors / policy violations across all 19 pages with the policy ON | None |
| Security | Enquiry email buttons: text typed in the form is URL-encoded, opens with noopener, addressed to the firm | Pass |
| Security | No third-party scripts, fonts, trackers or cookies; no inline scripts or styles; private-text blocklist; photo metadata check | Pass (enforced by build.py) |
| Performance | Largest paint 0.19s locally, layout shift 0; CSS 31 KB, JS 13 KB, all images 1.0 MB for the whole site | Good |
| Usability | Navigation transitions, back button, project filters, enquiry dialog (Escape closes, focus returns), tap targets 44px | Pass |
| SEO | Unique titles, descriptions under 160 characters, one h1, 404 set to noindex, structured data | Pass once the live address is set |

## Before going live
1. Set `"url"` in `content/site.json` to the live address and run `python3 build.py` again (turns on canonical links, sitemap and social preview images).
2. Test the enquiry form from a phone. For direct delivery to the inbox, set `"formEndpoint"` (Formspree or Web3Forms) in `content/site.json`.
3. After publishing, scan the live address with securityheaders.com and Mozilla Observatory, and run Lighthouse in Chrome. Expect A or A+.
4. Check the public pages contain nothing private (the build blocks the words in `content/blocklist.txt`).

## Account and domain security
- Turn on two-step login for Cloudflare, GitHub and the domain registrar. Use a unique password in a password manager.
- Cloudflare: enable "Always Use HTTPS", set minimum TLS to 1.2, turn on DNSSEC, add a CAA record, and lock the domain at the registrar.
- GitHub: protect the `main` branch (require a pull request) and keep Dependabot on so the build actions stay updated.
- Renew `securityExpires` in `content/site.json` before 31 October 2027.
- The email address is public text, so expect some spam. Keep the enquiry form as the main contact route.

## System requirements
- Visitors: any browser from the last 3 years (Chrome, Edge, Firefox, Safari, Samsung Internet). Older browsers still show all content and work; they lose parallax and some animation.
- Hosting: any static host over HTTPS. Cloudflare Pages is recommended because it applies the `_headers` security file.
- To rebuild: Python 3.8 or newer. Nothing else to install. Run `python3 build.py`, then publish the `dist/` folder.

## Known limits
- Tested in Chromium only. Check Safari (iPhone) and Firefox once live.
- Photos total about 1 MB. Converting them to WebP would cut this by about a third for visitors on slow mobile data.
- The security headers only apply on a host that supports them. On GitHub Pages only the in-page policy applies.

# Security

## Reporting a problem
Email otiarchitects@gmail.com. Please do not post details publicly until we have replied.

## What protects this site
| Control | Where |
|---|---|
| Static site, no server code, no database, no forms, no cookies, no analytics | whole site |
| Content Security Policy: only files from this site can load or run | `<meta>` on every page, plus `_headers` and `.htaccess` |
| No inline scripts or styles, no third-party resources, system fonts only | enforced by `build.py` |
| Clickjacking guard | `assets/js/boot.js` (and `frame-ancestors` where the host allows headers) |
| Private-text blocklist (addresses, tax numbers, names to keep out) | `content/blocklist.txt`, enforced by `build.py` |
| Photo metadata (GPS, camera) removed | images re-encoded; `build.py` fails if EXIF returns |
| Broken link and missing alt text checks | `build.py` |
| Only `dist/` is published, never the repository | `.github/workflows/deploy.yml` |
| Least-privilege workflow, no stored credentials, weekly action updates | workflow and `dependabot.yml` |
| `security.txt` for researchers | `/.well-known/security.txt` |

## Limits to know about
- GitHub Pages cannot send HTTP headers, so the policy is delivered through a `<meta>` tag. `frame-ancestors` and `X-Frame-Options` only work on hosts that read `_headers` (Netlify, Cloudflare Pages) or `.htaccess` (cPanel).
- The email address is printed on the site so clients can contact you. Expect some spam.
- Turn on, in the GitHub repository settings: two-factor sign-in for every account with write access, branch protection on `main`, Dependabot alerts and secret scanning.
- Never paste tokens or passwords into files, commits or issues. If one was ever pasted into the old repository history, revoke it and create a new one.

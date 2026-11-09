# Papua New Guinea compliance and website standards

Researched 9 November 2026. This is a practical checklist, **not legal advice**. Laws and draft bills change; have a PNG lawyer confirm anything marked "check".

## What PNG law says about a business website
| Topic | What was found | What the site does |
|---|---|---|
| Personal data | PNG has **no general data protection law and no data protection authority** (DataGuidance, KSandK). Limited protection comes from the Constitution, sector rules and the Cybercrime Code Act 2016. A data protection framework is being considered. | Collects nothing automatically: no cookies, analytics or trackers. Privacy page says exactly what happens to enquiry details. This already meets the stricter standards (GDPR-style) most clients and funders expect. |
| Cybercrime | The **Cybercrime Code Act 2016** (NICTA oversees ICT regulation) criminalises hacking, data interference, spam, computer fraud and similar. PNG has joined the Budapest Convention. A draft **Cybersecurity Act 2026** (fourth consultation draft) and amendments to the Cybercrime Code Act and NICTA Act were published for consultation by the Department of ICT. | Static site, no server code or database to attack; strict Content Security Policy; `security.txt`; legal notice warns against unauthorised access. **Check** again when the new Act is passed. |
| Architects | The **Architects (Registration) Act 1989** set up the PNG Board of Architects, which keeps the lists of registered architects and approved architectural companies. Use of the title "architect" is for registered persons. | About page shows the firm's Board number and the Managing Director's registration number, and the legal notice repeats the title rule. **Check** with the Board whether it has advertising rules to follow. |
| Copyright | Copyright and Neighbouring Rights Act 2000. | Legal notice states ownership of drawings and photos; get written permission from clients and photographers for every project photo. |
| Company details | Companies are registered with the Investment Promotion Authority (IPA). **Check** whether you want the registered company number and registered office printed in the footer or legal notice. The blocklist currently keeps a street address and tax number off the site on purpose. | Name, postal address, phones and email are shown. |
| Domain | `.pg` is run by **PNG DNS Administration at Unitech, Lae**. `.com.pg` needs an application form; the published commercial fee was K300 at the time of checking. | See DEPLOY.md. |

## Standards the site is built to
| Standard | Status |
|---|---|
| WCAG 2.2 level AA (accessibility) | Automated axe-core run is clean on every page; see QA.md. Keyboard, focus, contrast, reduced motion and a pause control for moving content. |
| HTTPS everywhere | HSTS header, `upgrade-insecure-requests`, Cloudflare Always Use HTTPS (DEPLOY.md). |
| Content Security Policy and security headers | In every page and in `_headers` / `.htaccess`: nosniff, frame protection, referrer policy, permissions policy, cross-origin isolation. |
| `security.txt` (RFC 9116) | `/.well-known/security.txt` with an expiry date to renew yearly. |
| Email authentication | SPF, DKIM and DMARC steps in DEPLOY.md and the DNS generator. |
| Search and sharing | Unique titles and descriptions, canonical links, sitemap, robots.txt, structured data, social preview image once `"url"` is set. |
| Privacy by design | No third-party scripts, fonts or images, so no visitor data leaves the site except the optional form service. |
| Performance | Small CSS and JS, only transform and opacity animated, images sized to avoid layout shift. |

## Still to do by a person
1. Written consent for every photo and project name shown (clients, photographers).
2. Decide what registered-company details to print (see "Company details").
3. Renew `securityExpires`, domain and insurance dates shown on the site (insurance text says "current to February 2027").
4. Ask a PNG lawyer to read `legal.html` and `privacy.html` once.

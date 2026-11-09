# Going live: domain, Cloudflare and Gmail

Plain order of work. Nothing here needs a server, and the only paid item is the domain.

## 0. What you need
- The domain. For a Papua New Guinea business address, `.com.pg` is registered through **PNG DNS Administration** (Unitech, Lae); the registry's published fee for a commercial `.com.pg` was K300 when this was checked, so confirm the current fee and form on their site. A global `.com` from any registrar also works and moves faster.
- A free Cloudflare account and a free GitHub account (already used for the site).
- The firm's Gmail inbox (`otiarchitects@gmail.com`).

## 1. Generate the DNS records (one command)
```
python3 tools/dns_plan.py --domain otiarchitects.com.pg --host github --gh-user YOUR-GITHUB-NAME --mail routing
```
This writes `deploy/cloudflare-zone.txt` and prints a numbered checklist for your exact choices.

| Choice | Meaning |
|---|---|
| `--host github` | Site stays on GitHub Pages (current setup). Adds the 4 GitHub IPv4 and 4 IPv6 addresses and a `www` CNAME. |
| `--host cloudflare-pages --project NAME` | Site is served by Cloudflare Pages. Adds CNAMEs to `NAME.pages.dev`. |
| `--mail routing` | **Free.** Mail sent to `info@yourdomain` is forwarded into the Gmail inbox. Cloudflare adds the MX and SPF records itself. |
| `--mail workspace` | **Paid** Google Workspace mailboxes on your own domain. Adds `smtp.google.com` MX, SPF and DMARC. |

## 2. Cloudflare
1. Add the domain to Cloudflare (Free plan). Import `deploy/cloudflare-zone.txt` (DNS, then Import and Export).
2. For GitHub Pages the web records must be **DNS only (grey cloud)** so GitHub can issue the HTTPS certificate. Check the icon after importing.
3. Ask the registry to change the domain's name servers to the two Cloudflare name servers shown in your dashboard. This can take up to 24 to 72 hours.
4. SSL/TLS: mode **Full (strict)**, turn on **Always Use HTTPS**, then turn on **DNSSEC** and add the DS record at the registry.
5. Optional redirect so only one address is used: Rules, Redirect Rules, send `www` to the bare domain (or the reverse) with a 301.

## 3. Publish the site
- **GitHub Pages (current):** Settings, Pages, Custom domain = your domain, then tick Enforce HTTPS when it appears. The workflow in `.github/workflows/deploy.yml` needs no change.
- **Cloudflare Pages (alternative):** Workers & Pages, Create, connect the GitHub repository, build command `python3 build.py`, output folder `dist`. If the build fails on Python, add the variable `PYTHON_VERSION` = `3.12`. Cloudflare Pages applies `_headers`, so the full security headers work there; GitHub Pages cannot send them (the in-page policy still applies).
- In `content/site.json` set `"url"` to `https://yourdomain` (turns on canonical links and the sitemap) and `"cdn"` to `"cloudflare"` when traffic goes through Cloudflare (the privacy page then says so). Run `python3 build.py` and push.

## 4. Gmail
**Free route (Cloudflare Email Routing)**
1. Cloudflare, Email, Email Routing, Enable, press *Add records and enable*.
2. Create `info@yourdomain` forwarding to `otiarchitects@gmail.com`; confirm the verification email in Gmail.
3. Gmail, Settings, Accounts and Import, **Send mail as**: add `info@yourdomain`, keep "Treat as an alias", and finish the confirmation code (it arrives in the same inbox).
4. Keep a single SPF record. If Gmail sends as your domain, make it `v=spf1 include:_spf.mx.cloudflare.net include:_spf.google.com ~all`.
5. When a test mail works both ways, change `"email"` in `content/site.json` to `info@yourdomain` and rebuild. The enquiry form's **Send with Gmail** button already works with any address.

**Paid route (Google Workspace):** use `--mail workspace`, verify the domain in Google Admin, turn on DKIM and publish the TXT record Google gives you, leave DMARC at `p=none` for about two weeks, then move to `p=quarantine`.

## 5. Direct form delivery (optional, recommended)
The form works with no setup: visitors choose Gmail, Outlook, their mail app, or Copy. To receive enquiries without the visitor pressing Send in their own mail, create a free form on Formspree or Web3Forms for the Gmail address and put its https address in `"formEndpoint"` (and `"formKey"` if given) in `content/site.json`. The build adds only that one address to the security policy and the privacy page updates itself.

## 6. Final checks (10 minutes)
- `https://yourdomain` and `https://www.yourdomain` both load over HTTPS with no browser warning.
- Send a test enquiry from a phone using each button, and send a mail to `info@` from another account.
- Scan the live address with securityheaders.com, and mail with a free SPF/DKIM/DMARC checker. Run Lighthouse in Chrome.
- Put a calendar reminder for `securityExpires` in `content/site.json` (renew before 31 October 2027) and for the domain renewal date.

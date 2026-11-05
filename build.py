#!/usr/bin/env python3
"""Builds the OTI Architects site from content/*.json into dist/.
Usage: python3 build.py            build and run all safety checks (exit code 1 if any check fails)
Pure standard library: nothing to install."""
import json, os, re, shutil, sys, html, struct, datetime
from html.parser import HTMLParser
ROOT = os.path.dirname(os.path.abspath(__file__)); C = ROOT + '/content'; S = ROOT + '/src'; DIST = ROOT + '/dist'
E = html.escape; errors = []; warnings = []
def load(n): return json.load(open(f'{C}/{n}.json', encoding='utf-8'))
site, projects, services, team, clients = (load(n) for n in ('site', 'projects', 'services', 'team', 'clients'))
BASE = site.get('base', '/'); URL = site.get('url', '').rstrip('/'); YEAR = datetime.date.today().year
# ---------------- validation (plain-English messages for editors) ----------------
def need(d, keys, where):
    for k in keys:
        if k not in d or d[k] in (None,): errors.append(f'{where}: missing "{k}"')
slugs = set()
for p in projects:
    need(p, ['slug','title','type','location','status','statusLabel','value','image','alt'], f'projects.json ({p.get("slug","?")})')
    if p.get('slug') in slugs: errors.append(f'projects.json: duplicate slug {p.get("slug")}')
    slugs.add(p.get('slug'))
    if p.get('status') not in ('current','completed'): errors.append(f'projects.json ({p.get("slug")}): status must be "current" or "completed"')
    if not os.path.exists(f'{S}/assets/images/{p.get("image")}'): errors.append(f'projects.json ({p.get("slug")}): image {p.get("image")} not found in src/assets/images')
for t in team:
    need(t, ['name','role','img','bio'], f'team.json ({t.get("name","?")})')
    if not os.path.exists(f'{S}/assets/images/{t.get("img")}'): errors.append(f'team.json ({t.get("name")}): image {t.get("img")} not found')
for c in clients:
    if c.get('logo') and not os.path.exists(f'{S}/assets/images/{c["logo"]}'): errors.append(f'clients.json ({c.get("name")}): logo {c["logo"]} not found')
if errors: print('\n'.join('ERROR ' + e for e in errors)); sys.exit(1)
# ---------------- helpers ----------------
def dims(p):
    b = open(p, 'rb').read()
    if b[:8] == b'\x89PNG\r\n\x1a\n': return struct.unpack('>II', b[16:24])
    i = 2
    while i < len(b) - 9:
        if b[i] != 0xFF: i += 1; continue
        m = b[i+1]
        if m in (0xC0, 0xC1, 0xC2): h, w = struct.unpack('>HH', b[i+5:i+9]); return w, h
        if m in (0xFF, 0x00, 0x01) or 0xD0 <= m <= 0xD9: i += 2; continue
        i += 2 + struct.unpack('>H', b[i+2:i+4])[0]
    return None
def img(f, alt, R, cls='', lazy=True):
    d = dims(f'{S}/assets/images/{f}'); wh = f' width="{d[0]}" height="{d[1]}"' if d else ''
    return f'<img{" class=%s" % chr(34)+cls+chr(34) if cls else ""} src="{R}assets/images/{f}" alt="{E(alt)}"{wh}{" loading=%slazy%s decoding=%sasync%s" % ((chr(34),)*4) if lazy else ""}>'
EM = site['email']
from urllib.parse import urlparse
EP = site.get('formEndpoint', '').strip(); KEY = site.get('formKey', '').strip(); EPO = ''; EPH = ''
if EP:
    _u = urlparse(EP)
    if _u.scheme != 'https' or not _u.netloc: errors.append('content/site.json: formEndpoint must be a full https:// address')
    else: EPO = f'{_u.scheme}://{_u.netloc}'; EPH = _u.netloc
MAIL = f'mailto:{EM}?subject=Project%20enquiry&body=Hello%20OTI%20Architects,%0D%0A%0D%0AMy%20name:%0D%0APhone:%0D%0AProject%20type:%0D%0ALocation:%0D%0ADescription:%0D%0A'
CSP = "default-src 'none'; img-src 'self' data:; style-src 'self'; script-src 'self'; connect-src 'none'; font-src 'none'; form-action 'none'; base-uri 'self'; object-src 'none'; upgrade-insecure-requests"
CSP = CSP.replace("connect-src 'none'", 'connect-src ' + (EPO or "'none'"))
FORMNOTE = (f'If you use the enquiry form, the details you type are sent over a secure connection to our form service ({EPH}), which delivers them to our email inbox. They are used only to reply to you.' if EP else 'The enquiry form on this site does not send anything by itself. It prepares a message that you send from your own email service (Gmail, Outlook or your email app), or copy and paste anywhere.')
NAV = [('index.html', 'Home'), ('about.html', 'About'), ('index.html#services', 'Services'), ('projects.html', 'Projects'), ('team.html', 'Team'), ('contact.html', 'Contact')]
pages = []
def head(title, desc, R, path, home=False):
    canon = f'<link rel="canonical" href="{URL}/{path}"><meta property="og:url" content="{URL}/{path}">' if URL else ''
    if URL: canon += f'<meta property="og:image" content="{URL}/assets/images/workers-mutual.jpg"><meta property="og:site_name" content="{E(site["name"])}"><meta name="twitter:card" content="summary_large_image">'
    if path == '404.html': canon += '<meta name="robots" content="noindex">'
    ld = ''
    if home:
        d = {"@context": "https://schema.org", "@type": "Architect", "name": site['name'], "foundingDate": "1996-02-08", "email": EM, "telephone": [p['tel'] for p in site['phones']], "areaServed": "Papua New Guinea", "address": {"@type": "PostalAddress", "addressLocality": site['city'], "addressCountry": "PG"}}
        if URL: d['url'] = URL + '/'
        ld = '<script type="application/ld+json">' + json.dumps(d).replace('<', '\\u003c') + '</script>'
    return (f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta http-equiv="Content-Security-Policy" content="{CSP}">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="referrer" content="strict-origin-when-cross-origin"><meta name="theme-color" content="#0A1560"><meta name="color-scheme" content="light">'
            f'<title>{E(title)}</title><meta name="description" content="{E(desc)}"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:type" content="website">{canon}'
            f'<link rel="icon" href="{R}assets/images/favicon.png" type="image/png"><link rel="stylesheet" href="{R}assets/css/site.css"><script src="{R}assets/js/boot.js"></script>{ld}</head><body><a class="skip" href="#main">Skip to content</a>')
def header(R, cur):
    nav = ''.join(f'<a href="{R}{h}"' + (' aria-current="page"' if h == cur else '') + f'>{l}</a>' for h, l in NAV)
    return (f'<header class="top"><div class="wrap bar"><a class="brand" href="{R}index.html" aria-label="{E(site["name"])}, home">{img("logo.png", site["name"] + ", " + site["tagline"], R, lazy=False)}</a>'
            f'<nav id="nav" class="nav" aria-label="Main">{nav}</nav><a class="btn" href="{MAIL}" data-enquire>Start a project</a><button id="menuBtn" type="button" aria-expanded="false" aria-controls="nav">Menu</button></div></header><main id="main">')
def dlg():
    types = ['Residential', 'Commercial', 'Industrial', 'Institutional', 'Not sure yet']
    opts = ''.join(f'<option>{t}</option>' for t in types)
    ph = ' or '.join(f'<a href="tel:{p["tel"]}">{p["label"]}</a>' for p in site['phones'])
    ways = ('<button class="btn out" type="button" data-way="gmail">Send with Gmail</button><button class="btn out" type="button" data-way="outlook">Send with Outlook</button>'
            '<button class="btn out" type="button" data-way="app">Open my email app</button><button class="btn out" type="button" data-way="copy">Copy message</button>')
    send = (f'<button class="btn" type="submit" id="enqSend">Send enquiry</button><details class="alt"><summary>Prefer to use your own email?</summary><div class="ways">{ways}</div></details>' if EP
            else f'<p class="how">Choose how to send it. Your message is filled in for you.</p><div class="ways">{ways}</div>')
    return (f'<dialog id="enq" class="enq" aria-labelledby="enqT" data-email="{E(EM)}" data-endpoint="{E(EP)}" data-key="{E(KEY)}"><div class="in">'
            f'<button class="x" type="button" id="enqX" aria-label="Close">Close</button><p class="kicker">Start a project</p><h2 id="enqT">Tell us about your project.</h2>'
            f'<p class="lead">A few details are enough. We reply by phone or email.</p>'
            f'<form id="enqForm" novalidate><div id="enqBody"><div class="g2"><div class="f"><label for="q-name">Your name</label><input id="q-name" name="name" type="text" autocomplete="name" required></div>'
            f'<div class="f"><label for="q-phone">Phone</label><input id="q-phone" name="phone" type="tel" autocomplete="tel"></div></div>'
            f'<div class="g2"><div class="f"><label for="q-email">Email</label><input id="q-email" name="email" type="email" autocomplete="email"></div>'
            f'<div class="f"><label for="q-type">Project type</label><select id="q-type" name="type">{opts}</select></div></div>'
            f'<div class="f"><label for="q-loc">Project location</label><input id="q-loc" name="location" type="text" placeholder="Suburb, town or province"></div>'
            f'<div class="f"><label for="q-det">About the project</label><textarea id="q-det" name="details" required placeholder="What do you want to build, roughly how big, and when do you want to start?"></textarea></div>'
            f'<div class="hp" aria-hidden="true"><label>Leave this empty<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>'
            f'{send}</div><p id="enqMsg" class="msg" role="status" aria-live="polite"></p>'
            f'<div id="enqDone" hidden><h3>Thank you.</h3><p>We have your enquiry and will reply by phone or email.</p><button class="btn" type="button" data-close>Close</button></div></form>'
            f'<p class="alt2">Or call {ph}, or email <a href="mailto:{E(EM)}">{E(EM)}</a> <button class="cp" type="button" data-copy="{E(EM)}">Copy address</button></p></div></dialog>')
def footer(R):
    ph = ''.join(f'<a href="tel:{p["tel"]}">{p["label"]}</a>' for p in site['phones'])
    return (f'</main><footer><div class="wrap fg"><div>{img("logo-light.png", site["name"], R, "fl-logo")}<p>Nationally owned architects and project managers, {site["city"]}, Papua New Guinea.</p></div>'
            f'<div><p class="fh">Navigation</p>{"".join("<a href='" + R + h + "'>" + l + "</a>" for h, l in NAV)}</div>'
            f'<div><p class="fh">Contact</p><a href="{MAIL}" data-enquire>{EM}</a>{ph}<p>{E(site["postal"])}</p></div></div>'
            f'<div class="wrap fl"><span>&copy; {YEAR} {E(site["name"])}</span><a href="{R}privacy.html">Privacy and security</a><button class="mt" type="button">Pause motion</button></div></footer>'
            + dlg() + '<div class="curtain" aria-hidden="true"></div><div class="prog" aria-hidden="true"></div><div class="cur" aria-hidden="true"><span></span></div>' + f'<nav class="dock" aria-label="Quick contact"><a href="tel:{site["phones"][0]["tel"]}">Call</a><a href="{MAIL}" data-enquire>Email</a></nav><script src="{R}assets/js/app.js" defer></script></body></html>')
def page(path, title, desc, body, cur=None, home=False):
    R = BASE if path == '404.html' else '../' * path.count('/')
    out = f'{DIST}/{path}'; os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w', encoding='utf-8').write(head(title, desc, R, path, home) + header(R, cur or path) + body(R) + footer(R)); pages.append(path)
def ph(crumb, h1, lead):
    return f'<div class="ph"><div class="wrap"><p class="crumb"><a href="{{R}}index.html">Home</a> / {crumb}</p><h1>{h1}</h1><p class="lead">{lead}</p></div></div>'
def PH(R, crumb, h1, lead): return ph(crumb, h1, lead).replace('{R}', R)
def cta(R, h='Have a project in mind?', t='Email us a short description of your project, its location and your timeline.'):
    return f'<div class="band"><div class="wrap"><h2>{h}</h2><p class="lead">{t}</p><div class="actions"><a class="btn light" href="{MAIL}" data-enquire>Email {E(site["short"])}</a><a class="btn ghost" href="{R}projects.html">View projects</a></div></div></div>'
LEAD = lambda t: '<p class="lead">' + E(t) + '</p>'
ND = '<div class="nd" aria-hidden="true"></div>'
def card(p, i, R):
    live = p['status'] == 'current'; cl = f'<p class="cl">{E(p["client"])}</p>' if p.get('client') else ''
    return (f'<a class="card reveal" href="{R}projects/{p["slug"]}.html" data-c="{p["type"].lower()}{" current" if live else ""}"><div class="im">{img(p["image"], p["alt"], R)}<span class="st{" live" if live else ""}">{E(p["statusLabel"])}</span></div>'
            f'<div class="bd"><p class="meta"><span class="ref">{i+1:02d}</span><span>{E(p["type"])}</span></p><h3>{E(p["title"])}</h3><p class="cl">{E(p["location"])}</p>{cl}</div></a>')
MARK = ('<svg viewBox="0 0 840 590" role="img" aria-labelledby="mkt"><title id="mkt">OTI Architects mark: a triangle above a ring on a base line</title>'
 '<defs><clipPath id="tc"><polygon points="420,50 90,380 750,380"/></clipPath><pattern id="ps" width="14" height="10" patternUnits="userSpaceOnUse"><rect width="2" height="10" fill="#fff" opacity=".16"/></pattern></defs>'
 '<circle class="rip" cx="420" cy="416" r="112"/><circle class="rip b" cx="420" cy="416" r="112"/>'
 '<g clip-path="url(#tc)"><image href="{R}assets/images/workers-mutual.jpg" x="30" y="40" width="780" height="415" preserveAspectRatio="xMidYMid slice"/><rect width="840" height="560" fill="#0459F1" opacity=".5"/><rect width="840" height="560" fill="url(#ps)"/></g>'
 '<path class="tri-l" d="M314 380H90L420 50 750 380H526" fill="none" stroke="#fff" stroke-width="5"/>'
 '<path class="ln" d="M40 416H308" fill="none" stroke="#fff" stroke-width="4"/><path class="ln" d="M800 416H532" fill="none" stroke="#fff" stroke-width="4"/>'
 '<path class="ax" d="M420 12V304" fill="none" stroke="#A9C6FF" stroke-width="1.5" stroke-dasharray="14 4 3 4"/>'
 '<g class="rg"><circle cx="420" cy="416" r="112" fill="#fff"/><circle cx="420" cy="416" r="88" fill="#000191"/><g text-anchor="middle" font-family="ui-monospace,Menlo,Consolas,monospace" fill="#fff"><text x="420" y="388" font-size="15" letter-spacing="5" fill="#A9C6FF">EST.</text><text x="420" y="441" font-size="50" font-weight="700" letter-spacing="-1">1996</text><text x="420" y="467" font-size="11" letter-spacing="2" fill="#A9C6FF">PNG-OWNED</text></g></g>'
 '<g class="dim" fill="none" stroke="#A9C6FF" stroke-width="1.5"><path d="M90 392V568M750 392V568M90 556H322M518 556H750M84 562L96 550M744 562L756 550"/></g>'
 '<text class="dim" x="420" y="561" text-anchor="middle" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="13" letter-spacing="2" fill="#A9C6FF">OTI ARCHITECTS</text></svg>')
def gallery(R):
    fp = [p for p in projects if p.get('featured')]
    sl = ''.join(f'<a class="slide" href="{R}projects/{p["slug"]}.html">{img(p["image"], p["alt"], R, lazy=(i > 0))}<div class="cap"><p class="meta"><span class="ref">{i+1:02d} / {len(fp):02d}</span><span>{E(p["type"])}</span><span>{E(p["statusLabel"])}</span></p><h3>{E(p["title"])}</h3><p class="where">{E(p["location"])}</p></div></a>' for i, p in enumerate(fp))
    return (f'<section class="sec work"><div class="wrap"><div class="sh"><h2>Selected work.</h2><a class="link" href="{R}projects.html">View all projects</a></div></div>'
            f'<div class="gal" id="gal" tabindex="0" role="region" aria-label="Selected projects, scroll sideways">{sl}</div>'
            f'<div class="wrap"><div class="gal-ctl"><button type="button" id="galPrev" aria-label="Previous project">&larr;</button><button type="button" id="galNext" aria-label="Next project">&rarr;</button></div></div></section>')
def placeof(loc):
    for k in ('Port Moresby', 'Lae', 'Daru'):
        if k in loc: return k
    return loc.split(',')[-1].strip()
def places(R):
    g = {}
    for p in projects: g.setdefault(placeof(p['location']), []).append(p)
    order = sorted(g.items(), key=lambda kv: -len(kv[1]))
    cells = ''.join(f'<div class="place reveal"><i>{len(v):02d}</i><b>{E(k)}</b><span>{E(", ".join(sorted({q["type"] for q in v})))}</span></div>' for k, v in order)
    return f'<section class="sec tint"><div class="wrap"><h2>Where we have built.</h2><p class="lead">From the capital to the provinces: projects by place, drawn from the portfolio.</p><div class="places">{cells}</div></div></section>'
def MQ():
    w = list(site['sectors']) + [x['title'] for x in services]
    one = ''.join(f'<span>{E(x)}</span>' for x in w)
    return f'<div class="mq" aria-hidden="true"><div class="mq-t">{one}{one}</div></div>'
def home(R):
    h = site['hero']; svcs = ''.join(f'<div class="svc reveal"><span class="n">{n+1:02d}</span><h3>{E(s["title"])}</h3><p>{E(s["text"])}</p></div>' for n, s in enumerate(services))
    feat = ''.join(card(p, projects.index(p), R) for p in projects if p.get('featured'))
    cl = ''.join(f'<div class="client">{img(c["logo"], c["name"], R) if c.get("logo") else E(c["name"])}</div>' for c in clients)
    facts = ''.join(f'<div class="fact"><b>{E(f["b"])}</b><span>{E(f["s"])}</span></div>' for f in site['facts'])
    fig = f'<figure class="fig">{img("lae-central.jpg", "Lae Central Complex, a yellow market building with sharp pitched roof forms", R)}{img("atrium.jpg", "Glazed barrel-vault atrium in an OTI project", R, "ins")}<figcaption>Lae Central Complex, 1987. Design architect Alama Oti.</figcaption></figure>'
    return (f'<div class="hero"><div class="pat" aria-hidden="true"></div><span class="cue" aria-hidden="true"></span><div class="wrap hero-grid"><div><p class="kicker">{E(h["kicker"])}</p><h1>{E(h["title"])}</h1><p class="sub">{E(h["sub"])}</p><div class="actions"><a class="btn light" href="{MAIL}" data-enquire>Email us about your project</a><a class="btn ghost" href="{R}projects.html">View projects</a></div></div>'
            f'<figure class="mark">{MARK.replace("{R}", R)}<figcaption>Workers Mutual Centre, 2001</figcaption></figure></div></div>'
            f'{MQ()}<div class="facts"><div class="wrap">{facts}</div></div>'
            f'<section class="sec"><div class="wrap split"><div><h2>Working together is how we build.</h2>{"".join(LEAD(t) for t in site["aboutShort"])}<p><a class="link" href="{R}about.html">About OTI Architects</a></p></div>{fig}</div></section>{ND}'
            f'<section id="services" class="sec tint"><div class="wrap"><h2>Our services.</h2><p class="lead">Residential, industrial, commercial and institutional projects, in one or more of the following services.</p><div class="svcs">{svcs}</div></div></section>'
            f'{gallery(R)}{places(R)}'
            f'<section class="sec"><div class="wrap"><h2>Clients we have worked for.</h2><div class="clients">{cl}</div></div></section>' + cta(R))
page('index.html', f'{site["short"]} | Architects in {site["city"]}, PNG', f'Nationally owned architects and project managers in {site["city"]}. Residential, commercial, industrial and institutional buildings across PNG since 1996.', home, home=True)
def about(R):
    tl = ''.join(f'<li class="reveal"><b>{E(t["y"])}</b>{E(t["t"])}</li>' for t in site['timeline']); cr = ''.join(f'<div class="reveal"><b>{E(c["b"])}</b>{E(c["t"])}</div>' for c in site['credentials'])
    fig = f'<figure class="fig">{img("atrium.jpg", "Glazed barrel-vault atrium in an OTI project", R)}{img("workers-mutual.jpg", "Workers Mutual Centre", R, "ins")}</figure>'
    return (PH(R, 'About', 'About OTI Architects.', 'A nationally owned architectural design and project management firm, since 1996.')
            + f'<section class="sec"><div class="wrap"><div class="split"><div><h2>Working together.</h2>{"".join(LEAD(t) for t in site["about"])}<div class="sectors">{"".join(f"<span>{E(s)}</span>" for s in site["sectors"])}</div></div>{fig}</div><ol class="tl" aria-label="Milestones">{tl}</ol></div></section>'
            + f'<div class="band"><div class="wrap"><blockquote>{E(site["quote"])}</blockquote><cite>{E(site["name"])}</cite></div></div>{ND}'
            + f'<section class="sec"><div class="wrap"><h2>Registered and insured.</h2><div class="creds">{cr}</div></div></section>' + cta(R))
page('about.html', f'About | {site["name"]}', f'{site["name"]} is a nationally owned architecture and project management firm founded in {site["city"]} in 1996.', about)
def plist(R):
    types = ['Commercial', 'Residential', 'Institutional', 'Industrial']
    chips = '<button class="chip on" type="button" data-f="all" aria-pressed="true">All</button><button class="chip" type="button" data-f="current" aria-pressed="false">In progress</button>' + ''.join(f'<button class="chip" type="button" data-f="{t.lower()}" aria-pressed="false">{t}</button>' for t in types)
    views = '<div class="vt" role="group" aria-label="View"><button class="chip on" type="button" data-v="grid" aria-pressed="true">Images</button><button class="chip" type="button" data-v="list" aria-pressed="false">Index</button></div>'
    def row(p, i):
        live = p['status'] == 'current'
        return (f'<a class="row" href="{R}projects/{p["slug"]}.html" data-c="{p["type"].lower()}{" current" if live else ""}">{img(p["image"], p["alt"], R, "th")}<span class="ref">{i+1:02d}</span>'
                f'<span class="tt"><h3>{E(p["title"])}</h3><small>{E(p["location"])}</small></span><span class="ty">{E(p["type"])}</span><span class="stx{" live" if live else ""}">{E(p["statusLabel"])}</span></a>')
    return (PH(R, 'Projects', 'Projects.', 'Completed and current work across Port Moresby, Lae and Western Province. Select a project for its details.')
            + f'<section class="sec"><div class="wrap"><div class="bar2"><div class="chips" role="group" aria-label="Filter projects">{chips}</div>{views}</div><p id="count" class="sr" aria-live="polite"></p>'
            + f'<h2 class="sr">All projects</h2><div class="grid" id="vGrid">{"".join(card(p, i, R) for i, p in enumerate(projects))}</div><div class="idx" id="vList" hidden>{"".join(row(p, i) for i, p in enumerate(projects))}</div></div></section>' + cta(R))
page('projects.html', f'Projects | {site["name"]}', f'Completed and current projects by {site["name"]} across Port Moresby, Lae and Western Province.', plist)
for i, p in enumerate(projects):
    def body(R, p=p, i=i):
        rel = [q for q in projects if q['type'] == p['type'] and q is not p][:3]
        cell = lambda k, v: f'<div><small>{k}</small><b>{E(v)}</b></div>'
        tb = cell('Project', p['title']) + cell('Sheet', f'{i+1:02d} / {len(projects):02d}') + cell('Type', p['type']) + cell('Location', p['location']) + (cell('Client', p['client']) if p.get('client') else '') + cell('Status', p['statusLabel']) + cell('Value', p['value'])
        prev = projects[i-1]; nxt = projects[(i+1) % len(projects)]
        return (PH(R, f'<a href="{R}projects.html">Projects</a> / {E(p["title"])}', E(p['title']), f'{E(p["type"])} project in {E(p["location"])}.')
                + f'<section class="sec"><div class="wrap"><div class="sheet">{img(p["image"], p["alt"], R, lazy=False)}</div><div class="tb">{tb}</div>'
                + f'<nav class="pn" aria-label="Other projects"><a class="link" href="{R}projects/{prev["slug"]}.html">Previous: {E(prev["title"])}</a><a class="link" href="{R}projects/{nxt["slug"]}.html">Next: {E(nxt["title"])}</a></nav></div></section>'
                + (f'<section class="sec tint"><div class="wrap"><h2>Related projects.</h2><div class="grid">{"".join(card(q, projects.index(q), R) for q in rel)}</div></div></section>' if rel else '') + cta(R))
    page(f'projects/{p["slug"]}.html', f'{p["title"]} | {site["name"]}', f'{p["title"]}, {p["type"].lower()} project in {p["location"]} by {site["name"]}.', body, cur='projects.html')
def tpage(R):
    ppl = ''.join(f'<div class="person reveal">{img(t["img"], t["name"], R)}<h3>{E(t["name"])}</h3><p class="role">{E(t["role"])}</p><p>{E(t["bio"])}</p></div>' for t in team)
    return PH(R, 'Team', 'Our team.', 'Registered architects and graduates, working together on every project.') + f'<section class="sec"><div class="wrap"><h2 class="sr">Team members</h2><div class="team">{ppl}</div></div></section>' + cta(R)
page('team.html', f'Team | {site["name"]}', f'Meet the architects of {site["name"]}, {site["city"]}.', tpage)
def cpage(R):
    ph_ = ' / '.join(f'<a href="tel:{p["tel"]}">{p["label"]}</a>' for p in site['phones'])
    return (PH(R, 'Contact', 'Contact us.', 'Tell us about your project, its location and your timeline. We reply by phone or email.')
            + f'<section class="sec"><div class="wrap"><p><a class="btn big" href="{MAIL}" data-enquire>Start a project</a></p>'
            + f'<ul class="cd"><li><small>Email</small><a href="{MAIL}" data-enquire>{EM}</a></li><li><small>Phone</small>{ph_}</li><li><small>Postal</small><strong>{E(site["postal"])}</strong></li></ul></div></section>')
page('contact.html', f'Contact | {site["name"]}', f'Contact {site["name"]} in {site["city"]} to discuss your project.', cpage)
def priv(R):
    return (PH(R, 'Privacy', 'Privacy and data security.', f'Last updated {datetime.date.today():%d %B %Y}.')
        + f'''<section class="sec"><div class="wrap prose"><h2>What this website collects</h2><p>Nothing is collected automatically. This website has no accounts, no cookies, no analytics, no advertising and no third-party scripts, fonts or images. Everything you see is served from this site.</p>
<h2>When you contact us</h2><p>{E(FORMNOTE)}</p><p>If you email or phone us we receive the details you choose to send, such as your name, contact details and project information. We use them only to answer your enquiry and to deliver the project, and we do not sell or share them for marketing. To ask us to delete your emails, write to <a href="mailto:{EM}">{EM}</a>.</p>
<p>Email travels through your own email provider, so please do not send passwords or bank details by email.</p>
<h2>Hosting</h2><p>The website is hosted on a static web host. Like most hosts it may keep standard technical logs, such as IP address, time and page requested, for security and reliability.</p>
<h2>How the site is protected</h2><ul><li>A strict content security policy only allows content from this site.</li><li>Pages are checked automatically on every update for scripts, tracking, broken links and private details before they are published.</li><li>Photographs have hidden location and camera data removed.</li></ul>
<h2>Reporting a security problem</h2><p>Please email <a href="mailto:{EM}">{EM}</a>. Details are in our <a href="{R}.well-known/security.txt">security.txt</a> file.</p></div></section>''')
page('privacy.html', f'Privacy and security | {site["name"]}', f'How {site["name"]} handles data and protects this website.', priv)
def nf(R):
    return f'<section class="sec"><div class="wrap"><p class="kicker" style="color:var(--blue)"></p><h1>Page not found.</h1><p class="lead">The page may have moved.</p><p><a class="btn" href="{R}index.html">Back to home</a></p></div></section>'.replace(' style="color:var(--blue)"', '')
page('404.html', f'Page not found | {site["name"]}', 'Page not found.', nf)
# ---------------- static files ----------------
shutil.copytree(S + '/assets', DIST + '/assets', dirs_exist_ok=True)
if os.path.isdir(S + '/static'): shutil.copytree(S + '/static', DIST, dirs_exist_ok=True)
for _f in ('_headers', '.htaccess'):
    _p = f'{DIST}/{_f}'
    if os.path.exists(_p): open(_p, 'w', encoding='utf-8').write(open(_p, encoding='utf-8').read().replace("connect-src 'none'", 'connect-src ' + (EPO or "'none'")))
os.makedirs(DIST + '/.well-known', exist_ok=True)
open(DIST + '/.well-known/security.txt', 'w').write(f'Contact: mailto:{EM}\nExpires: {site["securityExpires"]}T00:00:00.000Z\nPreferred-Languages: en\n' + (f'Canonical: {URL}/.well-known/security.txt\n' if URL else ''))
open(DIST + '/robots.txt', 'w').write('User-agent: *\nAllow: /\n' + (f'Sitemap: {URL}/sitemap.xml\n' if URL else ''))
if URL: open(DIST + '/sitemap.xml', 'w').write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f'<url><loc>{URL}/{p}</loc></url>' for p in pages if p != '404.html') + '</urlset>')
else: warnings.append('content/site.json "url" is empty: canonical links and sitemap.xml were skipped. Set it to your live address.')
# ---------------- safety checks ----------------
VOID = {'meta','link','img','br','hr','input','source','area','base','col','embed','wbr','path','circle','rect','polygon','image','use','stop'}
class Bal(HTMLParser):
    def __init__(s): super().__init__(); s.st = []; s.ids = set(); s.bad = []
    def handle_starttag(s, t, a):
        d = dict(a); 
        if 'id' in d: s.ids.add(d['id'])
        if t not in VOID: s.st.append(t)
    def handle_startendtag(s, t, a):
        d = dict(a)
        if 'id' in d: s.ids.add(d['id'])
    def handle_endtag(s, t):
        if t in VOID: return
        if s.st and s.st[-1] == t: s.st.pop()
        else: s.bad.append(t)
block = [l.strip().lower() for l in open(C + '/blocklist.txt', encoding='utf-8') if l.strip() and not l.startswith('#')]
allids = {}; htmls = {}
for p in pages:
    s = open(f'{DIST}/{p}', encoding='utf-8').read(); htmls[p] = s; b = Bal(); b.feed(s); allids[p] = b.ids
    if b.bad or b.st: errors.append(f'{p}: unbalanced HTML tags {b.bad[:3] or b.st[-3:]}')
for p, s in htmls.items():
    if re.search(r'\sstyle\s*=', s): errors.append(f'{p}: inline style attribute (blocked by security policy)')
    for m in re.finditer(r'<script([^>]*)>', s):
        if 'src=' not in m.group(1) and 'application/ld+json' not in m.group(1): errors.append(f'{p}: inline script (blocked by security policy)')
    if re.search(r'\son[a-z]+\s*=', s): errors.append(f'{p}: inline event handler')
    if re.search(r'(?:href|src|action)="https?://', s): errors.append(f'{p}: external link or resource (use none on this site)')
    for m in re.finditer(r'<img\b[^>]*>', s):
        if ' alt=' not in m.group(0): errors.append(f'{p}: image without alt text')
    low = re.sub(r'<[^>]+>', ' ', s).lower() + s.lower()
    for w in block:
        if w in low: errors.append(f'{p}: contains blocked text "{w}" (content/blocklist.txt)')
    for m in re.finditer(r'(?:href|src)="([^"]+)"', s):
        u = m.group(1)
        if u.startswith(('mailto:', 'tel:', 'data:')) : continue
        path, _, frag = u.partition('#')
        if p == '404.html' and path.startswith(BASE): path = path[len(BASE):]
        tgt = p if path == '' else os.path.normpath(os.path.join(os.path.dirname(p), path)).replace('\\', '/')
        if tgt == '.': tgt = 'index.html'
        if not os.path.exists(f'{DIST}/{tgt}'): errors.append(f'{p}: broken link {u}'); continue
        if frag and tgt in allids and frag not in allids[tgt]: errors.append(f'{p}: missing anchor #{frag} on {tgt}')
for root, _, fs in os.walk(DIST):
    for f in fs:
        if f.lower().endswith(('.jpg', '.jpeg')) and b'Exif' in open(os.path.join(root, f), 'rb').read(4096): errors.append(f'{f}: contains EXIF metadata (may include location)')
for w in warnings: print('WARNING', w)
if errors: print('\n'.join('ERROR ' + e for e in errors)); sys.exit(1)
print(f'OK: {len(pages)} pages built in dist/, all safety checks passed')

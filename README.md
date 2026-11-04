# OTI Architects Ltd website

A static website built from plain content files. Edit the content, push to `main`, and GitHub builds, checks and publishes it.

## How it is organised
| Folder or file | What it controls |
|---|---|
| `content/site.json` | Contact details, hero text, about text, quote, facts, timeline, credentials, **web address** |
| `content/services.json` | The services list on the home page |
| `content/projects.json` | Every project. Each one gets its own page automatically |
| `content/team.json` | Team members |
| `content/clients.json` | Client names. Add a logo by putting the file in `src/assets/images` and setting `"logo": "file.png"` |
| `content/blocklist.txt` | Words and numbers that must never appear publicly. The build stops if one does |
| `src/assets/css/site.css` | The design system. Colours and sizes are at the top |
| `src/assets/images` | Photos and logos (same file name replaces a photo) |
| `build.py` | Builds the site and runs the safety checks. Nothing to install |

## First steps
1. In `content/site.json` set `"url"` to your live address (for example `https://www.example.com.pg`). If the site lives at `username.github.io/otiarchitects`, also set `"base"` to `"/otiarchitects/"`.
2. In GitHub, go to Settings, then Pages, and set the source to **GitHub Actions**.
3. Delete the old files from the repository root (the empty files such as `git`, `store`, `erase`), then upload this folder's contents.

## The "Start a project" form and email buttons
Every "Start a project" and "Email" button opens an enquiry form. It works in two modes:
1. **Default (nothing to set up):** the visitor fills in the form, then picks *Send with Gmail*, *Send with Outlook*, *Open my email app* or *Copy message*. The message is pre-filled and addressed to the firm. Nothing is sent until the visitor presses Send in their own email.
2. **Direct sending (recommended):** the enquiry lands straight in the firm's inbox with no email app involved. A static site cannot send email by itself, so use a free form service (for example Formspree or Web3Forms): create a form there for `otiarchitects@gmail.com`, then put its address in `content/site.json` as `"formEndpoint": "https://..."` (and `"formKey"` if the service gives you an access key). Push. The build adds only that one address to the security policy and the privacy page updates itself.

## Adding a project
Add a block to `content/projects.json`, copy the photo into `src/assets/images`, push. Leave `"client"` empty for private clients. Set `"featured": true` to show it on the home page.

## Test locally
`python3 build.py` then open `dist/index.html`. If a check fails, the message says which file and why.

## Hosting elsewhere
Upload the contents of `dist/` to any static host. `_headers` (Netlify, Cloudflare Pages) and `.htaccess` (cPanel) add extra security headers.

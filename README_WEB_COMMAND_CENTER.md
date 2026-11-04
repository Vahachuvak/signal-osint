# Signal OSINT

Signal contains a public-profile search workspace, a passive website investigation workspace, a Media page, and an update log. Visitors to a deployed site do not need Python. The interface defaults to English and can be switched to Spanish using the control at the top of every page. The choice is saved in the browser when local storage is available; the former Russian preference falls back to English. Search data, JSON and Markdown reports, and material returned by external sources are not automatically translated or rewritten.

## Run locally

Install the dependencies once, then create the first administrator locally. The setup script asks for the username and password without saving the password to a source file. It never resets an existing administrator.

```powershell
python -m pip install -r requirements.txt
python setup_admin.py
python web_command_center.py
```

After setup, on Windows you can also double-click `Start Signal OSINT.bat` (the original launcher is preserved). Open **http://127.0.0.1:8765**. Keep the terminal open; press `Ctrl+C` to stop it. Python 3.10 or newer is required. If the port is busy, stop the other service or set the `PORT` environment variable before starting Signal. Public investigation tools continue to work if account dependencies are missing, but accounts will be unavailable until they are installed.

- `/` and `/people`: public profile search.
- `/app`: website investigation workspace.
- `/sites`: website investigation introduction.
- `/media`: Telegram channel and TON wallet address.
- `/updates`: project update log (edit `updates.html` when publishing a new entry).
- `/account`: optional sign-in, registration, and password change. The administrator link is shown only to an authenticated administrator.

Local accounts are stored in `.signal-data/accounts.sqlite3` (or the path in `SIGNAL_DB_PATH`). **Never upload this directory, a database file, or credentials to GitHub.** Local SQLite is for development and is not the same database as the published site.

## Deploy on Render

The project is not published automatically. A GitHub account and a hosting account are required. A free Render service can provide an `onrender.com` address and HTTPS for a demonstration:

1. Create a GitHub repository and upload these files to its root:
   - `people_dashboard.html`, `people_enhancements.js`, `people_osint.py`
   - `osint_dashboard.html`, `osint_engine.py`, `signal_home.html`
   - `media.html`, `updates.html`, `signal.css`, `signal_i18n.js`
   - `account.html`, `account.js`, `admin.html`, `admin.js`, `auth_store.py`, `auth_web.py`
   - `site_app.py`, `setup_admin.py`, `requirements.txt`, `render.yaml`, `.gitignore`, `THIRD_PARTY_NOTICES.txt`
2. In Render, choose **New → Blueprint**, connect the repository, and deploy it. Render reads `render.yaml`.
3. To create a service manually, use build command `pip install -r requirements.txt` and start command `gunicorn site_app:application --bind 0.0.0.0:$PORT --workers 1 --threads 4 --timeout 120`. Set `SIGNAL_PUBLIC=1` and `SIGNAL_TRUST_PROXY=1` behind Render's trusted proxy.
4. Configure the account database and administrator as described below. After deployment, test `/people`, `/app`, `/media`, `/updates`, `/account`, and the language switch. For an existing deployment, update **all** the files listed above together so that the pages, stylesheet, scripts, and Python dependencies are present. Commit the changes and deploy them.

Do not upload the entire working directory without checking for unrelated or private files. The free hosting plan is for demonstrations, can sleep when inactive, and has resource and outbound traffic limits. Consult [Render's current documentation](https://render.com/docs/free) for terms and pricing. A custom domain is optional; follow Render's [custom domain instructions](https://render.com/docs/custom-domains) and do not remove existing DNS records without checking their consequences.

The demo allows at most two concurrent investigations and 30 investigations per 10 minutes **per process**, shared across users. These in-memory limits reset on restart and are not comprehensive abuse protection. A public production service needs a security review, reliable rate limiting, monitoring, terms of use, and a privacy policy. Optionally set `SIGNAL_ALLOWED_HOSTS` to a comma-separated list of approved hosts. `SIGNAL_TRUST_PROXY=1` must only be used behind a trusted TLS-terminating proxy.

### Configure accounts on Render

The public web service **does not use local SQLite**: Render's filesystem is ephemeral. Create a managed PostgreSQL database in the same Render region, choose its plan deliberately, and set these environment variables in the **web service's Render dashboard**, not in GitHub:

- `DATABASE_URL`: the database's **internal PostgreSQL URL**. Public connections require TLS (`sslmode=require`). Keep this URL secret.
- `SIGNAL_ADMIN_USERNAME`: the initial administrator username.
- `SIGNAL_ADMIN_PASSWORD`: the initial administrator password; use a unique, private password.

Save and redeploy. Open `/account` to trigger first-time setup, then sign in and verify the administrator link. The administrator is created only if no administrator already exists; later changes to the environment variables do not reset an existing password. After confirming the account works, remove `SIGNAL_ADMIN_PASSWORD` from the environment and redeploy. Use the Account page to change a password; this signs out every active session for that account.

If `DATABASE_URL` or administrator setup is missing, public tools remain available but account endpoints return an unavailable message. No public setup endpoint exists. Render's free PostgreSQL offering can expire after 30 days; check the [current free-plan documentation](https://render.com/docs/free) and arrange backups and a suitable plan before relying on it for users. Do not share the database URL or commit credentials. A password shared in chat should be considered exposed: change the administrator password before public use.

Accounts store usernames, roles, account status, creation times, salted Argon2id password hashes, and hashed session tokens. The admin area requires a server-checked administrator session and never displays passwords or password hashes. Cookies are HttpOnly, SameSite=Lax, and Secure on public HTTPS deployments; account mutations check origin and session CSRF tokens. Login attempts are limited in memory per process, so use a proper shared rate limiter/WAF and a security review before operating a public service. Registration has no email verification or automated password recovery. Establish terms, privacy notices, backups, recovery procedures, and monitoring before inviting users.

The TON address on `/media` is a public receiving address. Senders must verify the address and TON mainnet in their wallet; the site does not hold private keys, process transactions, or verify donations. Never share a seed phrase or private key.

## People search

Search by username, full name, or a public ORCID iD. A username can also be extracted locally from supported GitHub, GitLab, DEV, Hacker News, Bluesky handle, Mastodon.social, Instagram, TikTok, and Telegram profile URLs; the supplied URL itself is never fetched. Select individual sources or use the profile and research presets. The source counter shows how many selected sources are applicable to the current input. Results can be filtered by text and status.

Available public sources are GitHub (profile and up to 20 repositories and organizations), GitLab, Hacker News, DEV Community, Bluesky, Mastodon.social, Russian and English Wikipedia, Stack Overflow, Crossref, ORCID, and Wikidata. A plain Bluesky username is checked as `username.bsky.social`; a valid dotted handle is checked directly. Mastodon checks **mastodon.social only**, not the entire network. ORCID looks up the specified iD; the checksum is validated. Name-based results are searches, not exact identity matches.

For a username, select **445 profile sites** to additionally check public profile addresses on 445 platforms, including Instagram, TikTok, Telegram, LinkedIn, Reddit, independent federated servers, and many creative, gaming, and developer communities. This group is off by default; the **All** and **Profiles** presets turn it on. It counts as one group in the source selector, while the results show a separate card and manual profile link for each site. Subdomain-based platforms are skipped when the username cannot form a valid subdomain. Some profile URLs are based on the [Sherlock Project's site catalogue](https://github.com/sherlock-project/sherlock); its licence is in `THIRD_PARTY_NOTICES.txt`.

Selecting the group sends the username to those sites and may take several minutes. The server makes at most one GET per applicable site, uses up to 40 workers and a three-second socket timeout, checks public DNS addresses, limits response sizes, and never follows redirects. DNS resolution and external network conditions can still delay the overall search. Other sites can block requests, demand sign-in, change their URLs, or return generic pages for nonexistent usernames. **Unverified** means the profile's existence could not be established; a generic HTTP 200, redirect, or Telegram's generic contact page is not treated as a match. **No data** means no accessible public profile was found, not proof that an account does not exist. Open each link and verify independently; a username match is not identification. Existing saved searches remain readable.

The optional context is added only to manual Google, Bing, and DuckDuckGo links. The search links themselves are not queried until the user opens them; some of the same services can also receive separate automatic profile checks when selected. Without the optional profile-site group, a fully populated search can make up to 14 bounded requests to the selected APIs; with it, there can be up to 445 additional profile checks. External services receive the relevant username, name, or ORCID; they can be unavailable, incomplete, or rate-limited. The relationship graph connects queries to source results, **not** confirmed identities, and displays up to 35 nodes. Always verify matches independently.

### Reverse image search

The People page includes a separate reverse-image section. Paste a **public image URL**, prepare the links, then open Google Lens or TinEye to search. Preparing the links happens entirely in the browser and makes no request to the image URL or external service. The chosen provider receives the URL only when its link is opened. Alternatively, select a JPG, PNG, WebP, or GIF file up to 10 MB and press **Search photo with Google Lens**: the browser submits it directly to Google, not to Signal's server. The People page permits the Lens upload and its Google Search redirect in its content-security policy; other pages retain their existing same-origin policy. You can also upload files on Google Images, TinEye, or Bing Visual Search yourself. Google Lens uses an undocumented upload endpoint and can change or reject requests. Third-party services may store images or URLs and have their own privacy policies. Never include secrets or private tokens in a URL; use images only with permission. Results show potentially matching or similar images, not verified identities or biometric identification.

History is disabled by default and, when enabled, stays in the current browser. Saved searches can be compared and exported to JSON or Markdown; the graph can be exported to SVG. The separate phone-format checker runs entirely in the browser and checks only a simplified international syntax. It does not establish whether a number exists or find its owner, carrier, or location; phone numbers are not sent in searches or reports. Do not enter addresses, phone numbers, passwords, tokens, or email addresses into the search fields. Signal does not search leaked databases, retrieve hidden information, or identify people biometrically.

Existing saved reports are not rewritten. Comparisons between reports saved before and after the English update can show differences caused only by translated labels; check the underlying source data before drawing conclusions.

## Website investigation

The existing 20 modules cover DNS, HTTP, TLS, security headers, cookies, technology hints, metadata, links, public contacts and social links, forms, external resources, robots.txt, sitemap, security.txt, indexing, database error signatures, basic accessibility indicators, Certificate Transparency, RDAP, and the Wayback archive. The graph, filters, browser history, comparisons, and JSON, Markdown, and SVG exports remain available.

- A target receives at most four GET requests: the entered URL and three standard public files. Redirects and discovered links are not automatically followed. A redirect can be investigated separately.
- Only public IP addresses are permitted. DNS answers are checked and outgoing connections are pinned to validated addresses. Responses are bounded, JavaScript is not executed, and private or dynamically loaded data may be missing.
- Certificate Transparency, RDAP, and Wayback are opt-in. Enabling them sends the domain or homepage address to the selected external service. RDAP can follow up to three validated public redirects to the registry.
- URL query parameters are omitted from reported addresses, but are sent to the target and can be reflected elsewhere in the response. Do not enter secrets. Cookie values and form field values are not collected.
- Website history is stored unencrypted in the current browser (up to 20 reports). Clear it using the history controls. Older reports are kept in their existing browser storage and may contain original-language labels or third-party content.
- Signal is passive. It does not crawl a whole site, scan ports, exploit vulnerabilities, test SQL injection, guess passwords, or submit forms. A missing security header or a database error signature does not prove a vulnerability, and no finding does not prove safety. Investigate only targets you are authorized to examine.

## Tests

```powershell
python -m unittest -v test_osint_engine test_people_osint test_auth
```

`site_app.py` is the WSGI application; `web_command_center.py` is the local development server. `web_command_center.html` is an older unused interface and is retained for reference. The separate load-test scripts and existing report are not part of the deployed website.

"""Bounded, passive website OSINT collection. No third-party dependencies."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from html.parser import HTMLParser
import http.client
import ipaddress
import json
import re
import socket
import ssl
import time
from urllib.parse import quote, urlencode, urljoin, urlsplit, urlunsplit
import xml.etree.ElementTree as ET

TIMEOUT = 7
BODY_LIMIT = 512 * 1024
USER_AGENT = 'SignalOSINT/2.0 (+passive website analysis)'
SOCIAL = ('facebook.com', 'instagram.com', 'linkedin.com', 'youtube.com', 'youtu.be',
          'x.com', 'twitter.com', 't.me', 'telegram.me', 'github.com', 'tiktok.com', 'mastodon.social')
DB_PATTERNS = {
    'MySQL / MariaDB': r'you have an error in your sql syntax|warning: mysql_|mysqli_sql_exception',
    'PostgreSQL': r'postgresql[^\r\n]{0,200}error|pg_query\(\)[^\r\n]{0,200}error|psql:[^\r\n]{0,200}error',
    'Microsoft SQL Server': r'unclosed quotation mark after the character string|microsoft ole db provider for sql server|sqlserverexception',
    'SQLite': r'sqlite_exception|sqlite3\.operationalerror|sqlite error:',
    'Oracle': r'ora-\d{5}|oracle error',
}


def safe_text(value, limit=500):
    return re.sub(r'[\x00-\x1f\x7f]+', ' ', str(value or '')).strip()[:limit]


def parse_target(value):
    if not isinstance(value, str) or not value.strip() or len(value) > 2048:
        raise ValueError('Enter a domain or address up to 2048 characters long.')
    value = value.strip()
    if re.search(r'[\x00-\x20\x7f\\]', value):
        raise ValueError('The address contains invalid characters.')
    try:
        parsed = urlsplit(value if '://' in value else 'https://' + value)
        if parsed.scheme not in ('http', 'https') or not parsed.hostname or parsed.username is not None or parsed.password is not None:
            raise ValueError()
        host = parsed.hostname.rstrip('.').encode('idna').decode('ascii').lower()
        if '%' in host or not host or len(host) > 253:
            raise ValueError()
        try:
            ipaddress.ip_address(host)
        except ValueError:
            if any(not re.fullmatch(r'[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?', part) for part in host.split('.')):
                raise ValueError()
        port = parsed.port if parsed.port is not None else (443 if parsed.scheme == 'https' else 80)
        if port not in (80, 443):
            raise ValueError('Only ports 80 and 443 are allowed.')
    except (UnicodeError, ValueError) as exc:
        if str(exc).startswith('Only ports'):
            raise
        raise ValueError('Enter a valid public HTTP(S) address without credentials.') from exc
    authority = f'[{host}]' if ':' in host else host
    if port != (443 if parsed.scheme == 'https' else 80):
        authority += f':{port}'
    path = quote(parsed.path or '/', safe="/%:@!$&'()*+,;=-._~")
    query = quote(parsed.query, safe="/%?:@!$&'()*+,;=-._~")
    return {'scheme': parsed.scheme, 'host': host, 'port': port, 'authority': authority,
            'path': path + ('?' + query if query else ''),
            'display_url': urlunsplit((parsed.scheme, authority, path, '', '')),
            'has_query': bool(parsed.query)}


def resolve_public(host):
    try:
        addresses = sorted({item[4][0] for item in socket.getaddrinfo(host, None, type=socket.SOCK_STREAM)})
    except socket.gaierror as exc:
        raise ValueError('Could not resolve the domain via DNS: ' + safe_text(exc)) from exc
    if not addresses or any(not ipaddress.ip_address(ip).is_global or ipaddress.ip_address(ip).is_multicast or ipaddress.ip_address(ip).is_reserved for ip in addresses):
        raise ValueError('Only public IP addresses are allowed. Local and mixed DNS responses are blocked.')
    return addresses


class PinnedHTTP(http.client.HTTPConnection):
    def __init__(self, host, port, address):
        super().__init__(host, port, timeout=TIMEOUT)
        self.address = address

    def connect(self):
        self.sock = socket.create_connection((self.address, self.port), self.timeout)


class PinnedHTTPS(http.client.HTTPSConnection):
    def __init__(self, host, port, address):
        super().__init__(host, port, timeout=TIMEOUT, context=ssl.create_default_context())
        self.address = address

    def connect(self):
        raw = socket.create_connection((self.address, self.port), self.timeout)
        try:
            self.sock = self._context.wrap_socket(raw, server_hostname=self.host)
        except Exception:
            raw.close()
            raise


def fetch(target, addresses, path, limit=BODY_LIMIT, accept='*/*'):
    """Single GET, pinned to a validated address; never follows redirects."""
    start = time.monotonic()
    last_error = 'No addresses available'
    for address in addresses[:3]:
        conn = (PinnedHTTPS if target['scheme'] == 'https' else PinnedHTTP)(target['host'], target['port'], address)
        sent = False
        try:
            conn.connect()
            tls = None
            if target['scheme'] == 'https':
                cert = conn.sock.getpeercert()
                issuer = dict(pair for group in cert.get('issuer', ()) for pair in group)
                tls = {'version': conn.sock.version(), 'issuer': issuer.get('organizationName', issuer.get('commonName', 'Unknown')),
                       'expires': cert.get('notAfter', ''), 'subject_alt_names': [value for typ, value in cert.get('subjectAltName', ()) if typ == 'DNS'][:60]}
            sent = True
            conn.request('GET', path, headers={'Host': target['authority'], 'User-Agent': USER_AGENT,
                                              'Accept': accept, 'Accept-Encoding': 'identity', 'Connection': 'close'})
            response = conn.getresponse()
            raw = response.read(limit + 1)
            headers = {}
            cookies = []
            for key, value in response.getheaders():
                key = key.lower()
                if key == 'set-cookie':
                    cookies.append(value)
                else:
                    headers[key] = (headers[key] + ', ' if key in headers else '') + safe_text(value, 3000)
            return {'status': response.status, 'headers': headers, 'cookies': cookies,
                    'body': raw[:limit], 'truncated': len(raw) > limit, 'tls': tls,
                    'duration': round((time.monotonic() - start) * 1000), 'error': None}
        except (OSError, ssl.SSLError, http.client.HTTPException, ValueError) as exc:
            last_error = safe_text(exc, 250)
            if sent:
                break
        finally:
            conn.close()
    return {'status': None, 'headers': {}, 'cookies': [], 'body': b'', 'truncated': False,
            'tls': None, 'duration': None, 'error': last_error}


def decode_body(response):
    content_type = response['headers'].get('content-type', '').lower()
    if response['headers'].get('content-encoding', 'identity').lower() not in ('identity', ''):
        return None
    if not any(v in content_type for v in ('text/', 'html', 'json', 'xml', 'javascript')):
        return None
    charset = re.search(r'charset\s*=\s*["\']?([\w.-]+)', content_type)
    try:
        return response['body'].decode(charset.group(1) if charset else 'utf-8', errors='replace')
    except LookupError:
        return response['body'].decode('utf-8', errors='replace')


def public_link(base, href):
    """Report only HTTP(S) links and omit credentials, queries, and fragments."""
    try:
        parsed = urlsplit(urljoin(base, href.strip()))
        if parsed.scheme not in ('http', 'https') or not parsed.hostname or parsed.username is not None or parsed.password is not None:
            return None
        host = parsed.hostname.encode('idna').decode('ascii').lower()
        port = parsed.port
        authority = f'[{host}]' if ':' in host else host
        if port:
            authority += f':{port}'
        return urlunsplit((parsed.scheme, authority, parsed.path or '/', '', ''))[:500]
    except (ValueError, UnicodeError):
        return None


class PageParser(HTMLParser):
    def __init__(self, base):
        super().__init__(convert_charrefs=True)
        self.base = base
        self.title = ''
        self.in_title = False
        self.lang = ''
        self.meta = {}
        self.links = []
        self.emails = []
        self.resources = []
        self.forms = []
        self.current_form = None
        self.images = 0
        self.missing_alt = 0
        self.h1 = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'html':
            self.lang = safe_text(a.get('lang'), 30)
        if tag == 'title':
            self.in_title = True
        if tag == 'meta':
            key = (a.get('name') or a.get('property') or '').lower()
            if key and len(self.meta) < 100:
                self.meta[key] = safe_text(a.get('content'))
        if tag == 'h1':
            self.h1 += 1
        if tag == 'img':
            self.images += 1
            if 'alt' not in a:
                self.missing_alt += 1
        if tag == 'a' and a.get('href'):
            href = a['href']
            if href.lower().startswith('mailto:'):
                email = safe_text(href[7:].split('?', 1)[0], 200)
                if email and email not in self.emails and len(self.emails) < 30:
                    self.emails.append(email)
            else:
                link = public_link(self.base, href)
                if link and link not in self.links and len(self.links) < 300:
                    self.links.append(link)
        if tag == 'link' and 'canonical' in (a.get('rel') or '').lower():
            self.meta['canonical'] = public_link(self.base, a.get('href') or '') or ''
        if (tag in ('script', 'iframe', 'img') and a.get('src')) or (tag == 'link' and 'stylesheet' in (a.get('rel') or '').lower() and a.get('href')):
            link = public_link(self.base, a.get('src') or a.get('href'))
            if link and len(self.resources) < 300:
                self.resources.append((tag, link))
        if tag == 'form' and len(self.forms) < 30:
            self.current_form = {'method': safe_text(a.get('method') or 'get', 12).upper(),
                                 'action': public_link(self.base, a.get('action') or self.base) or '—', 'fields': []}
            self.forms.append(self.current_form)
        if tag in ('input', 'select', 'textarea') and self.current_form is not None:
            name = safe_text(a.get('name'), 80)
            if name and len(self.current_form['fields']) < 30:
                self.current_form['fields'].append(name)

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False
        if tag == 'form':
            self.current_form = None

    def handle_data(self, data):
        if self.in_title:
            self.title = safe_text(self.title + data, 300)


def module(id, title, status, summary, facts=()):
    return {'id': id, 'title': title, 'status': status, 'summary': safe_text(summary, 400),
            'facts': [{'label': safe_text(label, 100), 'value': safe_text(value, 1200)} for label, value in facts]}


def parse_robots(response):
    text = decode_body(response)
    if response['status'] != 200 or text is None or '<html' in text[:500].lower():
        return None
    directives = []
    for line in text.splitlines():
        line = line.split('#', 1)[0].strip()
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip().lower()
            if key in ('user-agent', 'allow', 'disallow', 'sitemap', 'crawl-delay'):
                directives.append((key, safe_text(value, 250)))
    return directives


def parse_sitemap(response):
    text = decode_body(response)
    if response['status'] != 200 or text is None or '<!DOCTYPE' in text.upper() or response['truncated']:
        return None
    try:
        root = ET.fromstring(text)
        if root.tag.split('}')[-1] not in ('urlset', 'sitemapindex'):
            return None
        return [safe_text(node.text, 500) for node in root.iter() if node.tag.split('}')[-1] == 'loc' and node.text][:100]
    except ET.ParseError:
        return None


def cookie_facts(headers):
    facts = []
    for value in headers[:30]:
        parts = [part.strip() for part in value.split(';')]
        name = safe_text(parts[0].split('=', 1)[0], 100)
        attrs = [part.split('=', 1)[0].lower() for part in parts[1:]]
        same_site = next((part for part in parts[1:] if part.lower().startswith('samesite=')), 'SameSite not specified')
        facts.append((name, ', '.join(['Secure' if 'secure' in attrs else 'no Secure',
                                      'HttpOnly' if 'httponly' in attrs else 'no HttpOnly', same_site])))
    return facts


def collect_ct(host):
    try:
        ipaddress.ip_address(host)
        return {'names': [], 'error': 'Certificate Transparency search is unavailable for IP addresses.'}
    except ValueError:
        pass
    try:
        target = parse_target('https://crt.sh/')
        addresses = resolve_public(target['host'])
        response = fetch(target, addresses, '/?' + urlencode({'q': '%.' + host, 'output': 'json'}), limit=1024 * 1024)
        if response['error'] or response['status'] != 200 or response['truncated']:
            raise ValueError(response['error'] or ('Service returned HTTP ' + str(response['status']) + ('; response too large' if response['truncated'] else '')))
        data = json.loads(response['body'].decode('utf-8'))
        if not isinstance(data, list):
            raise ValueError('Unexpected crt.sh response format')
        names = set()
        for item in data[:5000]:
            if not isinstance(item, dict):
                continue
            for name in str(item.get('name_value', '')).splitlines():
                name = name.strip().lower().removeprefix('*.').rstrip('.')
                if name == host or name.endswith('.' + host):
                    names.add(safe_text(name, 253))
        return {'names': sorted(names)[:100], 'error': None}
    except (ValueError, OSError, UnicodeError, json.JSONDecodeError) as exc:
        return {'names': [], 'error': safe_text(exc, 250)}


def fetch_external_json(url, redirects=0):
    """Fetch a public JSON service with a bounded, validated redirect chain."""
    for attempt in range(redirects + 1):
        target = parse_target(url)
        response = fetch(target, resolve_public(target['host']), target['path'])
        if response['error']:
            raise ValueError(response['error'])
        if response['status'] in (301, 302, 303, 307, 308) and response['headers'].get('location'):
            if attempt == redirects:
                raise ValueError('Too many external service redirects.')
            url = urljoin(url, response['headers']['location'])
            continue
        if response['status'] != 200:
            raise ValueError('External service returned HTTP ' + str(response['status']))
        if response['truncated']:
            raise ValueError('External service response exceeded the size limit.')
        try:
            return json.loads(response['body'].decode('utf-8'))
        except (UnicodeError, json.JSONDecodeError) as exc:
            raise ValueError('External service returned invalid JSON.') from exc
    raise ValueError('Could not get a response from the external service.')


def collect_rdap(host):
    try:
        try:
            ipaddress.ip_address(host)
            return {'facts': [], 'nameservers': [], 'error': 'This module does not perform RDAP searches for IP addresses.'}
        except ValueError:
            pass
        data = fetch_external_json('https://rdap.org/domain/' + quote(host, safe='.'), redirects=3)
        if not isinstance(data, dict) or data.get('objectClassName') != 'domain':
            raise ValueError('No domain record returned; try the root domain for a subdomain.')
        facts = [('Registry domain', data.get('ldhName', host))]
        status = data.get('status', [])
        if isinstance(status, list):
            facts.append(('Status', ', '.join(str(v) for v in status[:15])))
        for event in data.get('events', [])[:30]:
            if isinstance(event, dict) and event.get('eventAction') in ('registration', 'expiration', 'last changed'):
                facts.append(({'registration': 'Registration', 'expiration': 'Expiration', 'last changed': 'Last changed'}[event['eventAction']], event.get('eventDate', '—')))
        for entity in data.get('entities', [])[:30]:
            if not isinstance(entity, dict) or 'registrar' not in entity.get('roles', []):
                continue
            card = entity.get('vcardArray', [])
            entries = card[1] if isinstance(card, list) and len(card) > 1 and isinstance(card[1], list) else []
            name = next((str(row[3]) for row in entries if isinstance(row, list) and len(row) > 3 and row[0] == 'fn'), entity.get('handle', '—'))
            facts.append(('Registrar', name))
        servers = [safe_text(item.get('ldhName', ''), 253).lower() for item in data.get('nameservers', [])[:30] if isinstance(item, dict) and item.get('ldhName')]
        facts.extend(('Nameserver', name) for name in servers)
        return {'facts': facts, 'nameservers': servers, 'error': None}
    except (ValueError, OSError, TypeError) as exc:
        return {'facts': [], 'nameservers': [], 'error': safe_text(exc, 250)}


def collect_archive(host, scheme):
    try:
        authority = '[' + host + ']' if ':' in host else host
        query = urlencode({'url': scheme + '://' + authority + '/'})
        data = fetch_external_json('https://archive.org/wayback/available?' + query)
        if not isinstance(data, dict) or not isinstance(data.get('archived_snapshots', {}), dict):
            raise ValueError('Unexpected Internet Archive response format.')
        closest = data.get('archived_snapshots', {}).get('closest')
        if not isinstance(closest, dict) or not closest.get('available'):
            return {'snapshot': None, 'error': None}
        archive_url = public_link('https://web.archive.org/', str(closest.get('url', '')))
        if not archive_url or urlsplit(archive_url).hostname != 'web.archive.org':
            raise ValueError('Invalid archive snapshot address.')
        return {'snapshot': {'url': archive_url, 'timestamp': safe_text(closest.get('timestamp'), 30),
                             'status': safe_text(closest.get('status'), 20)}, 'error': None}
    except (ValueError, OSError, TypeError) as exc:
        return {'snapshot': None, 'error': safe_text(exc, 250)}


def inspect_target(value, use_ct=False, use_rdap=False, use_archive=False):
    started = time.monotonic()
    target = parse_target(value)
    addresses = resolve_public(target['host'])
    with ThreadPoolExecutor(max_workers=7) as pool:
        jobs = {key: pool.submit(fetch, target, addresses, path) for key, path in (
            ('page', target['path']), ('robots', '/robots.txt'), ('sitemap', '/sitemap.xml'),
            ('security', '/.well-known/security.txt'))}
        ct_job = pool.submit(collect_ct, target['host']) if use_ct else None
        rdap_job = pool.submit(collect_rdap, target['host']) if use_rdap else None
        archive_job = pool.submit(collect_archive, target['host'], target['scheme']) if use_archive else None
        results = {key: job.result() for key, job in jobs.items()}
        ct = ct_job.result() if ct_job else None
        rdap = rdap_job.result() if rdap_job else None
        archive = archive_job.result() if archive_job else None
    page = results['page']
    text = decode_body(page)
    html = PageParser(target['display_url'])
    is_html = text is not None and ('html' in page['headers'].get('content-type', '').lower())
    if is_html:
        html.feed(text)
    headers = page['headers']
    has_page = page['status'] is not None
    mods = []
    mods.append(module('dns', 'DNS and addresses', 'ok', f'System DNS returned {len(addresses)} public addresses.',
                       [('Domain', target['host'])] + [('IPv6' if ':' in ip else 'IPv4', ip) for ip in addresses[:30]]))
    mods.append(module('http', 'HTTP response', 'ok' if has_page else 'error',
                       f'HTTP {page["status"]}; response time {page["duration"]} ms.' if has_page else 'Request failed: ' + (page['error'] or 'error'),
                       [('URL without parameters', target['display_url']), ('Content-Type', headers.get('content-type', '—')),
                        ('Redirect (not followed)', public_link(target['display_url'], headers['location']) or 'Invalid URL' if headers.get('location') else '—'), ('Bytes read', str(len(page['body'])) + ' bytes' + (' (truncated)' if page['truncated'] else ''))]))
    cert = page['tls']
    mods.append(module('tls', 'TLS certificate', 'ok' if cert else ('info' if target['scheme'] == 'http' else 'error'),
                       'Certificate verified by the system.' if cert else ('HTTP does not use a certificate.' if target['scheme'] == 'http' else 'Could not verify the certificate.'),
                       [('Protocol', cert['version']), ('Issuer', cert['issuer']), ('Expires', cert['expires']), ('Certificate names', ', '.join(cert['subject_alt_names'][:20]) or '—')] if cert else []))
    checks = ['strict-transport-security', 'content-security-policy', 'x-content-type-options', 'x-frame-options', 'referrer-policy', 'permissions-policy']
    present = sum(k in headers for k in checks)
    mods.append(module('security_headers', 'Security headers', ('ok' if present == len(checks) else 'warning') if has_page else 'error',
                       f'Found {present} of {len(checks)} headers. Missing headers do not always indicate a vulnerability.' if has_page else 'No HTTP response to analyze.',
                       [(key, headers.get(key, 'Not found')) for key in checks] if has_page else []))
    cookies = cookie_facts(page['cookies'])
    mods.append(module('cookies', 'Cookie settings', 'ok' if has_page else 'error',
                       f'Found {len(cookies)} Set-Cookie headers. Values are not stored.' if has_page else 'No HTTP response to analyze.', cookies))
    tech = [(k, headers[k]) for k in ('server', 'x-powered-by', 'via', 'x-generator') if headers.get(k)]
    if html.meta.get('generator'):
        tech.append(('HTML generator', html.meta['generator']))
    mods.append(module('tech', 'Technologies and server', 'ok' if tech else ('info' if has_page else 'error'),
                       f'Found {len(tech)} clues. Data may be incomplete or misleading.' if has_page else 'No HTTP response to analyze.', tech))
    mods.append(module('metadata', 'Page metadata', 'ok' if is_html else 'info',
                       'Metadata from the requested HTML page.' if is_html else 'No HTML page available for analysis.',
                       [('Title', html.title or '—'), ('Description', html.meta.get('description', '—')), ('Language', html.lang or '—'),
                        ('Canonical', html.meta.get('canonical', '—')), ('Open Graph', html.meta.get('og:title', '—'))] if is_html else []))
    ext_links = [link for link in html.links if urlsplit(link).hostname != target['host']]
    mods.append(module('links', 'Links and external domains', 'ok' if is_html else 'info',
                       f'Links: {len(html.links)}; external: {len(ext_links)}. Additional pages were not visited.' if is_html else 'No HTML page available for analysis.',
                       [('External link', link) for link in ext_links[:30]] + [('Internal links', str(len(html.links) - len(ext_links)))] if is_html else []))
    mods.append(module('contacts', 'Contacts and social links', 'ok' if is_html else 'info',
                       'Public mailto links and links to known platforms from the page.' if is_html else 'No HTML page available for analysis.',
                       [('Email', email) for email in html.emails] + [('Platform', link) for link in ext_links if any((urlsplit(link).hostname or '') == s or (urlsplit(link).hostname or '').endswith('.' + s) for s in SOCIAL)][:30]))
    mods.append(module('forms', 'Forms and fields', 'ok' if is_html else 'info',
                       f'Forms on page: {len(html.forms)}. Forms are not submitted; field values are not saved.' if is_html else 'No HTML page available for analysis.',
                       [(f'Form {i + 1}', f'{form["method"]} {form["action"]} | Fields: {", ".join(form["fields"]) or "no names"}') for i, form in enumerate(html.forms)]))
    resource_domains = sorted({urlsplit(link).hostname for _, link in html.resources if urlsplit(link).hostname and urlsplit(link).hostname != target['host']})
    mods.append(module('resources', 'External resources', 'ok' if is_html else 'info',
                       f'HTML resources: {len(html.resources)}; external domains: {len(resource_domains)}. Resources were not loaded.' if is_html else 'No HTML page available for analysis.',
                       [('Domain', name) for name in resource_domains[:40]]))
    robots = parse_robots(results['robots'])
    mods.append(module('robots', 'robots.txt', 'error' if results['robots']['error'] else ('ok' if robots is not None else 'info'),
                       f'HTTP {results["robots"]["status"] or "no response"}; ' + (f'{len(robots)} directives recognized.' if robots is not None else 'file unavailable or not recognized.'),
                       robots[:40] if robots else []))
    sitemap = parse_sitemap(results['sitemap'])
    mods.append(module('sitemap', 'Sitemap', 'error' if results['sitemap']['error'] else ('ok' if sitemap is not None else 'info'),
                       f'/sitemap.xml: HTTP {results["sitemap"]["status"] or "no response"}; ' + (f'{len(sitemap)} links read (up to 100).' if sitemap is not None else 'XML is unavailable, invalid or exceeds the limit.'),
                       [('Entry', public_link(target['display_url'], link) or 'Invalid URL') for link in sitemap[:30]] if sitemap else []))
    sec = results['security']
    sec_text = decode_body(sec)
    sec_lines = []
    if sec['status'] == 200 and sec_text is not None and '<html' not in sec_text[:500].lower():
        for line in sec_text.splitlines():
            if ':' in line and not line.strip().startswith('#'):
                key, val = line.split(':', 1)
                if key.strip().lower() in ('contact', 'expires', 'policy', 'canonical', 'preferred-languages', 'encryption'):
                    sec_lines.append((safe_text(key, 50), safe_text(val, 400)))
    mods.append(module('securitytxt', 'security.txt', 'error' if sec['error'] else ('ok' if sec_lines else 'info'),
                       f'/.well-known/security.txt: HTTP {sec["status"] or "no response"}; ' + (f'{len(sec_lines)} fields recognized.' if sec_lines else 'file not found or not recognized.'), sec_lines[:30]))
    mods.append(module('indexing', 'Indexing', 'ok' if has_page else 'error',
                       'Indexing directives from the response and metadata; search engines are not queried.' if has_page else 'No HTTP response to analyze.',
                       [('X-Robots-Tag', headers.get('x-robots-tag', 'Not specified')), ('Meta robots', html.meta.get('robots', 'Not specified')),
                        ('Canonical', html.meta.get('canonical', 'Not specified'))] if has_page else []))
    db = [name for name, pattern in DB_PATTERNS.items() if text and re.search(pattern, text, re.I)]
    mods.append(module('database', 'Database errors', ('warning' if db else 'ok') if text is not None else 'info',
                       ('Possible database error messages found.' if db else 'No known error signatures found in the response fragment.') + ' This is not an SQL injection test.' if text is not None else 'Response text unavailable; check not performed.',
                       [('Signature', name) for name in db]))
    mods.append(module('accessibility', 'Basic accessibility indicators', 'ok' if is_html else 'info',
                       'Selected indicators from the source HTML only; not an accessibility audit.' if is_html else 'No HTML page available for analysis.',
                       [('HTML language', html.lang or 'Not specified'), ('Images without alt', f'{html.missing_alt} of {html.images}'),
                        ('H1 headings', str(html.h1)), ('Viewport', html.meta.get('viewport', 'Not specified'))] if is_html else []))
    mods.append(module('ct', 'Certificate Transparency', 'disabled' if not use_ct else ('error' if ct['error'] else 'ok'),
                       'Disabled. When enabled, the domain is sent to crt.sh.' if not use_ct else ('crt.sh error: ' + ct['error'] if ct['error'] else f'Found {len(ct["names"])} names in public certificates (up to 100). Their current existence is not confirmed.'),
                       [('Certificate name', name) for name in ct['names']] if ct and not ct['error'] else []))
    mods.append(module('rdap', 'Domain registration · RDAP', 'disabled' if not use_rdap else ('error' if rdap['error'] else 'ok'),
                       'Disabled. When enabled, the domain is sent to rdap.org and the registry.' if not use_rdap else ('RDAP error: ' + rdap['error'] if rdap['error'] else 'Public RDAP registration data. Some details may be hidden.'),
                       rdap['facts'] if rdap and not rdap['error'] else []))
    mods.append(module('archive', 'Website archive · Wayback', 'disabled' if not use_archive else ('error' if archive['error'] else ('ok' if archive['snapshot'] else 'info')),
                       'Disabled. When enabled, the website address is sent to Internet Archive.' if not use_archive else ('Internet Archive error: ' + archive['error'] if archive['error'] else ('Closest available home-page snapshot.' if archive['snapshot'] else 'No archived home-page snapshot found.')),
                       [('Snapshot URL', archive['snapshot']['url']), ('Snapshot time (UTC)', archive['snapshot']['timestamp']), ('HTTP status', archive['snapshot']['status'])] if archive and archive['snapshot'] else []))
    nodes = [{'id': 'domain:' + target['host'], 'label': target['host'], 'kind': 'domain'}]
    edges = []
    def add_node(kind, label):
        ident = kind + ':' + label
        if not any(node['id'] == ident for node in nodes):
            nodes.append({'id': ident, 'label': safe_text(label, 100), 'kind': kind})
            edges.append({'source': nodes[0]['id'], 'target': ident})
    for ip in addresses[:12]:
        add_node('ip', ip)
    if cert:
        add_node('cert', cert['issuer'])
    if rdap and not rdap['error']:
        for name in rdap['nameservers'][:15]:
            add_node('nameserver', name)
    for name in resource_domains[:20]:
        add_node('resource', name)
    for link in ext_links[:20]:
        name = urlsplit(link).hostname
        if name:
            add_node('link', name)
    if ct and not ct['error']:
        for name in ct['names'][:25]:
            if name != target['host']:
                add_node('ct', name)
    return {'version': 2, 'host': target['host'], 'url': target['display_url'], 'query_omitted': target['has_query'],
            'scanned_at': datetime.now(timezone.utc).isoformat(), 'duration_ms': round((time.monotonic() - started) * 1000),
            'ips': addresses, 'status': page['status'], 'modules': mods, 'graph': {'nodes': nodes, 'edges': edges},
            'request_count': 4, 'external_sources': [name for name, enabled in (('crt.sh', use_ct), ('rdap.org', use_rdap), ('Internet Archive', use_archive)) if enabled]}

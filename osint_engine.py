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
        raise ValueError('Введите домен или адрес длиной до 2048 символов.')
    value = value.strip()
    if re.search(r'[\x00-\x20\x7f\\]', value):
        raise ValueError('Адрес содержит недопустимые символы.')
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
            raise ValueError('Разрешены только порты 80 и 443.')
    except (UnicodeError, ValueError) as exc:
        if str(exc).startswith('Разрешены'):
            raise
        raise ValueError('Укажите корректный публичный HTTP(S)-адрес без логина и пароля.') from exc
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
        raise ValueError('Не удалось разрешить домен через DNS: ' + safe_text(exc)) from exc
    if not addresses or any(not ipaddress.ip_address(ip).is_global or ipaddress.ip_address(ip).is_multicast or ipaddress.ip_address(ip).is_reserved for ip in addresses):
        raise ValueError('Разрешены только публичные IP-адреса. Локальные и смешанные DNS-ответы запрещены.')
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
    last_error = 'Нет доступных адресов'
    for address in addresses[:3]:
        conn = (PinnedHTTPS if target['scheme'] == 'https' else PinnedHTTP)(target['host'], target['port'], address)
        sent = False
        try:
            conn.connect()
            tls = None
            if target['scheme'] == 'https':
                cert = conn.sock.getpeercert()
                issuer = dict(pair for group in cert.get('issuer', ()) for pair in group)
                tls = {'version': conn.sock.version(), 'issuer': issuer.get('organizationName', issuer.get('commonName', 'Неизвестно')),
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
        same_site = next((part for part in parts[1:] if part.lower().startswith('samesite=')), 'SameSite не указан')
        facts.append((name, ', '.join(['Secure' if 'secure' in attrs else 'без Secure',
                                      'HttpOnly' if 'httponly' in attrs else 'без HttpOnly', same_site])))
    return facts


def collect_ct(host):
    try:
        ipaddress.ip_address(host)
        return {'names': [], 'error': 'Для IP-адреса поиск в Certificate Transparency недоступен.'}
    except ValueError:
        pass
    try:
        target = parse_target('https://crt.sh/')
        addresses = resolve_public(target['host'])
        response = fetch(target, addresses, '/?' + urlencode({'q': '%.' + host, 'output': 'json'}), limit=1024 * 1024)
        if response['error'] or response['status'] != 200 or response['truncated']:
            raise ValueError(response['error'] or ('Сервис вернул HTTP ' + str(response['status']) + ('; ответ слишком большой' if response['truncated'] else '')))
        data = json.loads(response['body'].decode('utf-8'))
        if not isinstance(data, list):
            raise ValueError('Неожиданный формат ответа crt.sh')
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
                raise ValueError('Слишком много перенаправлений внешнего сервиса.')
            url = urljoin(url, response['headers']['location'])
            continue
        if response['status'] != 200:
            raise ValueError('Внешний сервис вернул HTTP ' + str(response['status']))
        if response['truncated']:
            raise ValueError('Ответ внешнего сервиса превысил ограничение размера.')
        try:
            return json.loads(response['body'].decode('utf-8'))
        except (UnicodeError, json.JSONDecodeError) as exc:
            raise ValueError('Внешний сервис вернул некорректный JSON.') from exc
    raise ValueError('Не удалось получить ответ внешнего сервиса.')


def collect_rdap(host):
    try:
        try:
            ipaddress.ip_address(host)
            return {'facts': [], 'nameservers': [], 'error': 'Для IP-адресов этот модуль не выполняет RDAP-поиск.'}
        except ValueError:
            pass
        data = fetch_external_json('https://rdap.org/domain/' + quote(host, safe='.'), redirects=3)
        if not isinstance(data, dict) or data.get('objectClassName') != 'domain':
            raise ValueError('Сервис не вернул запись домена; для поддомена попробуйте основной домен.')
        facts = [('Домен в реестре', data.get('ldhName', host))]
        status = data.get('status', [])
        if isinstance(status, list):
            facts.append(('Статус', ', '.join(str(v) for v in status[:15])))
        for event in data.get('events', [])[:30]:
            if isinstance(event, dict) and event.get('eventAction') in ('registration', 'expiration', 'last changed'):
                facts.append(({'registration': 'Регистрация', 'expiration': 'Истечение', 'last changed': 'Изменение'}[event['eventAction']], event.get('eventDate', '—')))
        for entity in data.get('entities', [])[:30]:
            if not isinstance(entity, dict) or 'registrar' not in entity.get('roles', []):
                continue
            card = entity.get('vcardArray', [])
            entries = card[1] if isinstance(card, list) and len(card) > 1 and isinstance(card[1], list) else []
            name = next((str(row[3]) for row in entries if isinstance(row, list) and len(row) > 3 and row[0] == 'fn'), entity.get('handle', '—'))
            facts.append(('Регистратор', name))
        servers = [safe_text(item.get('ldhName', ''), 253).lower() for item in data.get('nameservers', [])[:30] if isinstance(item, dict) and item.get('ldhName')]
        facts.extend(('NS-сервер', name) for name in servers)
        return {'facts': facts, 'nameservers': servers, 'error': None}
    except (ValueError, OSError, TypeError) as exc:
        return {'facts': [], 'nameservers': [], 'error': safe_text(exc, 250)}


def collect_archive(host, scheme):
    try:
        authority = '[' + host + ']' if ':' in host else host
        query = urlencode({'url': scheme + '://' + authority + '/'})
        data = fetch_external_json('https://archive.org/wayback/available?' + query)
        if not isinstance(data, dict) or not isinstance(data.get('archived_snapshots', {}), dict):
            raise ValueError('Неожиданный формат ответа Internet Archive.')
        closest = data.get('archived_snapshots', {}).get('closest')
        if not isinstance(closest, dict) or not closest.get('available'):
            return {'snapshot': None, 'error': None}
        archive_url = public_link('https://web.archive.org/', str(closest.get('url', '')))
        if not archive_url or urlsplit(archive_url).hostname != 'web.archive.org':
            raise ValueError('Некорректный адрес архивной копии.')
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
    mods.append(module('dns', 'DNS и адреса', 'ok', f'Системный DNS вернул {len(addresses)} публичных адресов.',
                       [('Домен', target['host'])] + [('IPv6' if ':' in ip else 'IPv4', ip) for ip in addresses[:30]]))
    mods.append(module('http', 'HTTP-ответ', 'ok' if has_page else 'error',
                       f'HTTP {page["status"]}; время ответа {page["duration"]} мс.' if has_page else 'Запрос не выполнен: ' + (page['error'] or 'ошибка'),
                       [('URL без параметров', target['display_url']), ('Content-Type', headers.get('content-type', '—')),
                        ('Редирект (не переходили)', public_link(target['display_url'], headers['location']) or 'Недопустимый URL' if headers.get('location') else '—'), ('Размер прочитанного фрагмента', str(len(page['body'])) + ' байт' + (' (ограничено)' if page['truncated'] else ''))]))
    cert = page['tls']
    mods.append(module('tls', 'TLS-сертификат', 'ok' if cert else ('info' if target['scheme'] == 'http' else 'error'),
                       'Сертификат проверен системой.' if cert else ('Для HTTP сертификат не используется.' if target['scheme'] == 'http' else 'Не удалось проверить сертификат.'),
                       [('Протокол', cert['version']), ('Издатель', cert['issuer']), ('Действует до', cert['expires']), ('Имена в сертификате', ', '.join(cert['subject_alt_names'][:20]) or '—')] if cert else []))
    checks = ['strict-transport-security', 'content-security-policy', 'x-content-type-options', 'x-frame-options', 'referrer-policy', 'permissions-policy']
    present = sum(k in headers for k in checks)
    mods.append(module('security_headers', 'Защитные заголовки', ('ok' if present == len(checks) else 'warning') if has_page else 'error',
                       f'Найдено {present} из {len(checks)} заголовков. Отсутствие не всегда означает уязвимость.' if has_page else 'Нет HTTP-ответа для анализа.',
                       [(key, headers.get(key, 'Не обнаружен')) for key in checks] if has_page else []))
    cookies = cookie_facts(page['cookies'])
    mods.append(module('cookies', 'Настройки cookies', 'ok' if has_page else 'error',
                       f'Обнаружено Set-Cookie: {len(cookies)}. Значения не сохраняются.' if has_page else 'Нет HTTP-ответа для анализа.', cookies))
    tech = [(k, headers[k]) for k in ('server', 'x-powered-by', 'via', 'x-generator') if headers.get(k)]
    if html.meta.get('generator'):
        tech.append(('HTML generator', html.meta['generator']))
    mods.append(module('tech', 'Технологии и сервер', 'ok' if tech else ('info' if has_page else 'error'),
                       f'Обнаружено подсказок: {len(tech)}. Данные могут быть неполными или подменёнными.' if has_page else 'Нет HTTP-ответа для анализа.', tech))
    mods.append(module('metadata', 'Метаданные страницы', 'ok' if is_html else 'info',
                       'Метаданные из HTML запрошенной страницы.' if is_html else 'HTML-страница недоступна для анализа.',
                       [('Title', html.title or '—'), ('Description', html.meta.get('description', '—')), ('Язык', html.lang or '—'),
                        ('Canonical', html.meta.get('canonical', '—')), ('Open Graph', html.meta.get('og:title', '—'))] if is_html else []))
    ext_links = [link for link in html.links if urlsplit(link).hostname != target['host']]
    mods.append(module('links', 'Ссылки и внешние домены', 'ok' if is_html else 'info',
                       f'Ссылок: {len(html.links)}; внешних: {len(ext_links)}. Дополнительные страницы не посещались.' if is_html else 'HTML-страница недоступна для анализа.',
                       [('Внешняя ссылка', link) for link in ext_links[:30]] + [('Внутренние ссылки', str(len(html.links) - len(ext_links)))] if is_html else []))
    mods.append(module('contacts', 'Контакты и соцсети', 'ok' if is_html else 'info',
                       'Публичные mailto-ссылки и ссылки на известные платформы со страницы.' if is_html else 'HTML-страница недоступна для анализа.',
                       [('Email', email) for email in html.emails] + [('Платформа', link) for link in ext_links if any((urlsplit(link).hostname or '') == s or (urlsplit(link).hostname or '').endswith('.' + s) for s in SOCIAL)][:30]))
    mods.append(module('forms', 'Формы и поля', 'ok' if is_html else 'info',
                       f'Форм на странице: {len(html.forms)}. Формы не отправляются; значения полей не сохраняются.' if is_html else 'HTML-страница недоступна для анализа.',
                       [(f'Форма {i + 1}', f'{form["method"]} {form["action"]} | Поля: {", ".join(form["fields"]) or "нет имён"}') for i, form in enumerate(html.forms)]))
    resource_domains = sorted({urlsplit(link).hostname for _, link in html.resources if urlsplit(link).hostname and urlsplit(link).hostname != target['host']})
    mods.append(module('resources', 'Внешние ресурсы', 'ok' if is_html else 'info',
                       f'Ресурсов в HTML: {len(html.resources)}; внешних доменов: {len(resource_domains)}. Ресурсы не загружались.' if is_html else 'HTML-страница недоступна для анализа.',
                       [('Домен', name) for name in resource_domains[:40]]))
    robots = parse_robots(results['robots'])
    mods.append(module('robots', 'robots.txt', 'error' if results['robots']['error'] else ('ok' if robots is not None else 'info'),
                       f'HTTP {results["robots"]["status"] or "нет ответа"}; ' + (f'распознано директив: {len(robots)}.' if robots is not None else 'файл не распознан или недоступен.'),
                       robots[:40] if robots else []))
    sitemap = parse_sitemap(results['sitemap'])
    mods.append(module('sitemap', 'Sitemap', 'error' if results['sitemap']['error'] else ('ok' if sitemap is not None else 'info'),
                       f'/sitemap.xml: HTTP {results["sitemap"]["status"] or "нет ответа"}; ' + (f'прочитано ссылок: {len(sitemap)} (до 100).' if sitemap is not None else 'XML недоступен, некорректен или превышает лимит.'),
                       [('Запись', public_link(target['display_url'], link) or 'Недопустимый URL') for link in sitemap[:30]] if sitemap else []))
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
                       f'/.well-known/security.txt: HTTP {sec["status"] or "нет ответа"}; ' + (f'распознано полей: {len(sec_lines)}.' if sec_lines else 'файл не обнаружен или не распознан.'), sec_lines[:30]))
    mods.append(module('indexing', 'Индексация', 'ok' if has_page else 'error',
                       'Директивы индексации из ответа и метаданных; индексы поисковых систем не опрашиваются.' if has_page else 'Нет HTTP-ответа для анализа.',
                       [('X-Robots-Tag', headers.get('x-robots-tag', 'Не указан')), ('Meta robots', html.meta.get('robots', 'Не указан')),
                        ('Canonical', html.meta.get('canonical', 'Не указан'))] if has_page else []))
    db = [name for name, pattern in DB_PATTERNS.items() if text and re.search(pattern, text, re.I)]
    mods.append(module('database', 'Ошибки базы данных', ('warning' if db else 'ok') if text is not None else 'info',
                       ('Обнаружены возможные сообщения об ошибках БД.' if db else 'Известные сигнатуры ошибок в прочитанном фрагменте не найдены.') + ' Это не проверка SQL-инъекций.' if text is not None else 'Текст ответа недоступен; проверка не выполнена.',
                       [('Сигнатура', name) for name in db]))
    mods.append(module('accessibility', 'Базовые признаки доступности', 'ok' if is_html else 'info',
                       'Только отдельные признаки из исходного HTML; не является аудитом доступности.' if is_html else 'HTML-страница недоступна для анализа.',
                       [('Язык HTML', html.lang or 'Не указан'), ('Изображений без alt', f'{html.missing_alt} из {html.images}'),
                        ('Заголовков H1', str(html.h1)), ('Viewport', html.meta.get('viewport', 'Не указан'))] if is_html else []))
    mods.append(module('ct', 'Certificate Transparency', 'disabled' if not use_ct else ('error' if ct['error'] else 'ok'),
                       'Отключено. При включении домен будет передан на crt.sh.' if not use_ct else ('Ошибка crt.sh: ' + ct['error'] if ct['error'] else f'Найдено имён в публичных сертификатах: {len(ct["names"])} (до 100). Их существование сейчас не подтверждено.'),
                       [('Имя сертификата', name) for name in ct['names']] if ct and not ct['error'] else []))
    mods.append(module('rdap', 'Регистрация домена · RDAP', 'disabled' if not use_rdap else ('error' if rdap['error'] else 'ok'),
                       'Отключено. При включении домен будет передан на rdap.org и в реестр.' if not use_rdap else ('Ошибка RDAP: ' + rdap['error'] if rdap['error'] else 'Публичные регистрационные данные из RDAP. Некоторые сведения могут быть скрыты.'),
                       rdap['facts'] if rdap and not rdap['error'] else []))
    mods.append(module('archive', 'Архив сайта · Wayback', 'disabled' if not use_archive else ('error' if archive['error'] else ('ok' if archive['snapshot'] else 'info')),
                       'Отключено. При включении адрес сайта будет передан в Internet Archive.' if not use_archive else ('Ошибка Internet Archive: ' + archive['error'] if archive['error'] else ('Ближайший доступный снимок главной страницы.' if archive['snapshot'] else 'Архивная копия главной страницы не найдена.')),
                       [('Адрес снимка', archive['snapshot']['url']), ('Время снимка (UTC)', archive['snapshot']['timestamp']), ('HTTP статус', archive['snapshot']['status'])] if archive and archive['snapshot'] else []))
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

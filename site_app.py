"""WSGI application for Signal's public website and OSINT workspace."""
from collections import deque
import json
import os
from pathlib import Path
import re
import threading
import time
from urllib.parse import urlsplit

import auth_store
import auth_web
from osint_engine import inspect_target
from people_osint import search_people

ROOT = Path(__file__).resolve().parent
MAX_BODY = 8192
SCAN_WINDOW = 600
SCAN_LIMIT = 30
_scan_times = deque()
_rate_lock = threading.Lock()
_scan_slots = threading.BoundedSemaphore(2)


def _json(value):
    return json.dumps(value, ensure_ascii=False).encode('utf-8')


def _respond(start_response, status, content, content_type='text/html; charset=utf-8', extra=()):
    headers = [('Content-Type', content_type), ('Content-Length', str(len(content))),
               ('Cache-Control', 'no-store'), ('X-Content-Type-Options', 'nosniff'),
               ('X-Frame-Options', 'DENY'), ('Referrer-Policy', 'no-referrer'),
               ('Content-Security-Policy', "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'")]
    start_response(status, headers + list(extra))
    return [content]


def _valid_host_and_origin(environ):
    host = environ.get('HTTP_HOST', '').lower()
    if not host or not re.fullmatch(r'[a-z0-9.\-\[\]:]+', host):
        return False
    public = os.environ.get('SIGNAL_PUBLIC') == '1'
    if public:
        configured = {value.strip().lower() for value in os.environ.get('SIGNAL_ALLOWED_HOSTS', '').split(',') if value.strip()}
        if configured and host not in configured:
            return False
    else:
        port = environ.get('SERVER_PORT', '')
        if host not in {f'127.0.0.1:{port}', f'localhost:{port}'}:
            return False
    origin = environ.get('HTTP_ORIGIN')
    if not origin:
        return not (public and environ.get('REQUEST_METHOD') == 'POST')
    try:
        parsed = urlsplit(origin)
        scheme = environ.get('wsgi.url_scheme', 'http')
        # Only enable behind a trusted TLS-terminating reverse proxy (e.g. Render).
        if public and os.environ.get('SIGNAL_TRUST_PROXY') == '1':
            scheme = environ.get('HTTP_X_FORWARDED_PROTO', scheme).split(',')[0].strip().lower()
        return (parsed.scheme == scheme and parsed.netloc.lower() == host and not parsed.path and
                not parsed.query and not parsed.fragment and parsed.username is None and parsed.password is None)
    except ValueError:
        return False


def _reserve_scan():
    """Per-process global limits for a small single-worker public demo."""
    if not _scan_slots.acquire(blocking=False):
        return 'busy'
    with _rate_lock:
        now = time.monotonic()
        while _scan_times and _scan_times[0] <= now - SCAN_WINDOW:
            _scan_times.popleft()
        if len(_scan_times) >= SCAN_LIMIT:
            _scan_slots.release()
            return 'rate'
        _scan_times.append(now)
    return 'ok'


def application(environ, start_response):
    path = environ.get('PATH_INFO', '/')
    method = environ.get('REQUEST_METHOD', 'GET').upper()
    if method == 'GET' and path == '/healthz':
        return _respond(start_response, '200 OK', b'ok', 'text/plain; charset=utf-8')
    if not _valid_host_and_origin(environ):
        return _respond(start_response, '403 Forbidden', _json({'error': 'Invalid host or request origin.'}), 'application/json; charset=utf-8')
    if path.startswith(('/api/auth/', '/api/admin/')):
        return auth_web.handle(path, environ, start_response, _respond, _json)
    if method == 'GET' and path in ('/admin', '/admin/'):
        try:
            allowed = auth_web.admin_allowed(environ)
        except auth_store.AuthUnavailable:
            return _respond(start_response, '503 Service Unavailable', _json({'error': 'Accounts are not configured or temporarily unavailable.'}), 'application/json; charset=utf-8')
        if not allowed:
            return _respond(start_response, '404 Not Found', _json({'error': 'Page not found.'}), 'application/json; charset=utf-8')
        return _respond(start_response, '200 OK', (ROOT / 'admin.html').read_bytes())
    if method == 'GET' and path in ('/', '/people', '/people/', '/sites', '/app', '/app/', '/media', '/media/', '/updates', '/updates/', '/account', '/account/'):
        filename = ('people_dashboard.html' if path in ('/', '/people', '/people/') else
                    'signal_home.html' if path == '/sites' else
                    'media.html' if path in ('/media', '/media/') else
                    'updates.html' if path in ('/updates', '/updates/') else
                    'account.html' if path in ('/account', '/account/') else 'osint_dashboard.html')
        return _respond(start_response, '200 OK', (ROOT / filename).read_bytes())
    if method == 'GET' and path == '/favicon.ico':
        return _respond(start_response, '204 No Content', b'', 'image/x-icon')
    if method == 'GET' and path == '/signal.css':
        return _respond(start_response, '200 OK', (ROOT / 'signal.css').read_bytes(), 'text/css; charset=utf-8')
    if method == 'GET' and path == '/people_enhancements.js':
        return _respond(start_response, '200 OK', (ROOT / 'people_enhancements.js').read_bytes(), 'text/javascript; charset=utf-8')
    if method == 'GET' and path == '/signal_i18n.js':
        return _respond(start_response, '200 OK', (ROOT / 'signal_i18n.js').read_bytes(), 'text/javascript; charset=utf-8')
    if method == 'GET' and path in ('/account.js', '/admin.js'):
        return _respond(start_response, '200 OK', (ROOT / path[1:]).read_bytes(), 'text/javascript; charset=utf-8')
    if method == 'GET' and path == '/robots.txt':
        return _respond(start_response, '200 OK', b'User-agent: *\nAllow: /\nDisallow: /app\n', 'text/plain; charset=utf-8')
    if method != 'POST' or path not in ('/api/inspect', '/api/people'):
        return _respond(start_response, '404 Not Found', _json({'error': 'Page not found.'}), 'application/json; charset=utf-8')
    try:
        if environ.get('CONTENT_TYPE', '').split(';', 1)[0].strip().lower() != 'application/json':
            raise ValueError('Expected an application/json request.')
        length = int(environ.get('CONTENT_LENGTH') or '0')
        if not 0 < length <= MAX_BODY:
            raise ValueError('Invalid request size.')
        request = json.loads(environ['wsgi.input'].read(length))
        if not isinstance(request, dict) or (path == '/api/inspect' and any(not isinstance(request.get(key, False), bool) for key in ('ct', 'rdap', 'archive'))):
            raise ValueError('Invalid request format.')
    except (ValueError, TypeError, UnicodeError):
        return _respond(start_response, '400 Bad Request', _json({'error': 'Check the request format and size.'}), 'application/json; charset=utf-8')
    reservation = _reserve_scan()
    if reservation != 'ok':
        msg = 'The server is busy. Please try again in a few seconds.' if reservation == 'busy' else 'The shared investigation limit has been reached. Please try again later.'
        return _respond(start_response, '429 Too Many Requests', _json({'error': msg}), 'application/json; charset=utf-8', [('Retry-After', '60')])
    try:
        try:
            if path == '/api/people':
                result = search_people(request.get('username', ''), request.get('name', ''), request.get('sources', []),
                                       orcid=request.get('orcid', ''), context=request.get('context', ''))
            else:
                result = inspect_target(request.get('target'), use_ct=request.get('ct', False),
                                        use_rdap=request.get('rdap', False), use_archive=request.get('archive', False))
            status = '200 OK'
        except (ValueError, TypeError) as exc:
            result, status = {'error': str(exc)}, '400 Bad Request'
        except Exception:
            result, status = {'error': 'An internal error occurred. Check your input and try again.'}, '500 Internal Server Error'
    finally:
        _scan_slots.release()
    return _respond(start_response, status, _json(result), 'application/json; charset=utf-8')

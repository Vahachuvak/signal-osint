"""Bounded same-origin account endpoints for the existing WSGI app."""
from collections import deque
from http.cookies import SimpleCookie
import json
import os
import re
import secrets
import threading
import time

import auth_store as store

MAX_BODY = 4096
AUTH_WINDOW = 600
_attempts = {}
_attempts_lock = threading.Lock()
_hash_slots = threading.BoundedSemaphore(2)
COOKIE_NAME = 'signal_session'


def _secure_transport(environ):
    if os.environ.get('SIGNAL_PUBLIC') != '1':
        return True
    scheme = environ.get('wsgi.url_scheme', 'http')
    if os.environ.get('SIGNAL_TRUST_PROXY') == '1':
        scheme = environ.get('HTTP_X_FORWARDED_PROTO', scheme).split(',')[0].strip().lower()
    return scheme == 'https'


def cookie_token(environ):
    raw = environ.get('HTTP_COOKIE', '')
    if len(raw) > 4096:
        return ''
    try:
        cookie = SimpleCookie()
        cookie.load(raw)
        return cookie[COOKIE_NAME].value if COOKIE_NAME in cookie else ''
    except Exception:
        return ''


def _cookie(value, max_age):
    secure = '; Secure' if os.environ.get('SIGNAL_PUBLIC') == '1' else ''
    return f'{COOKIE_NAME}={value}; Path=/; Max-Age={max_age}; HttpOnly; SameSite=Lax{secure}'


def _read_json(environ):
    if environ.get('CONTENT_TYPE', '').split(';', 1)[0].strip().lower() != 'application/json':
        raise store.AuthInvalid('Expected a JSON request.')
    try:
        length = int(environ.get('CONTENT_LENGTH') or '0')
        if not 0 < length <= MAX_BODY:
            raise ValueError()
        data = json.loads(environ['wsgi.input'].read(length))
        if not isinstance(data, dict):
            raise ValueError()
        return data
    except (ValueError, TypeError, UnicodeError, KeyError):
        raise store.AuthInvalid('Check the request format and size.')


def _rate_allowed(environ, name, operation):
    """Small in-memory limits for the existing single-worker demo, not a WAF."""
    now = time.monotonic()
    address = str(environ.get('REMOTE_ADDR', 'unknown'))[:100]
    keys = [('client:' + address, 40)]
    if operation in ('login', 'change-password') and isinstance(name, str):
        keys.append(('account:' + name.strip().lower()[:32], 8))
    with _attempts_lock:
        for key, hits in list(_attempts.items()):
            while hits and hits[0] <= now - AUTH_WINDOW:
                hits.popleft()
            if not hits:
                del _attempts[key]
        if len(_attempts) > 4096:
            return False
        if any(len(_attempts.get(key, ())) >= limit for key, limit in keys):
            return False
        for key, _ in keys:
            _attempts.setdefault(key, deque()).append(now)
    return True


def _session(environ):
    return store.session_user(cookie_token(environ))


def admin_allowed(environ):
    if not _secure_transport(environ):
        return False
    user = _session(environ)
    return bool(user and user['is_admin'])


def _csrf_valid(environ, user):
    supplied = environ.get('HTTP_X_CSRF_TOKEN', '')
    return isinstance(supplied, str) and re.fullmatch(r'[A-Za-z0-9_-]{43}', supplied) is not None and secrets.compare_digest(supplied, user['csrf'])


def handle(path, environ, start_response, respond, encode_json):
    def reply(status, value, extra=()):
        return respond(start_response, status, encode_json(value), 'application/json; charset=utf-8', extra)

    if not _secure_transport(environ):
        return reply('503 Service Unavailable', {'error': 'Account access requires HTTPS.'})
    method = environ.get('REQUEST_METHOD', 'GET').upper()
    try:
        if path == '/api/auth/session' and method == 'GET':
            store.require_setup()
            user = _session(environ)
            return reply('200 OK', {'authenticated': bool(user), 'user': user})
        if path == '/api/admin/users' and method == 'GET':
            user = _session(environ)
            if not user or not user['is_admin']:
                return reply('404 Not Found', {'error': 'Page not found.'})
            return reply('200 OK', store.list_users())
        allowed = {'/api/auth/register', '/api/auth/login', '/api/auth/logout',
                   '/api/auth/change-password', '/api/admin/user-status'}
        if method != 'POST' or path not in allowed:
            return reply('404 Not Found', {'error': 'Page not found.'})
        # site_app has already checked the Origin and Host match. Unlike the
        # existing public scans, account mutations require an Origin even locally.
        if not environ.get('HTTP_ORIGIN'):
            return reply('403 Forbidden', {'error': 'Invalid request origin.'})
        payload = _read_json(environ)
        action = path.rsplit('/', 1)[-1]
        if action in ('login', 'register'):
            if not _rate_allowed(environ, payload.get('username', ''), action):
                return reply('429 Too Many Requests', {'error': 'Too many attempts. Please try again later.'}, [('Retry-After', str(AUTH_WINDOW))])
            if not _hash_slots.acquire(blocking=False):
                return reply('429 Too Many Requests', {'error': 'Account service is busy. Please try again.'}, [('Retry-After', '10')])
            try:
                user = (store.authenticate(payload.get('username', ''), payload.get('password', '')) if action == 'login'
                        else store.register_user(payload.get('username', ''), payload.get('password', '')))
                token = store.new_session(user['id'], user['password_hash'])
            finally:
                _hash_slots.release()
            old_token = cookie_token(environ)
            if old_token and old_token != token:
                store.revoke_session(old_token)
            session = store.session_user(token)
            if not session:
                raise store.AuthInvalid('Account is unavailable.')
            return reply('200 OK' if action == 'login' else '201 Created', {'authenticated': True, 'user': session},
                         [('Set-Cookie', _cookie(token, store.SESSION_TTL))])
        user = _session(environ)
        if not user:
            return reply('401 Unauthorized', {'error': 'Please sign in first.'})
        if path == '/api/admin/user-status' and not user['is_admin']:
            return reply('404 Not Found', {'error': 'Page not found.'})
        if not _csrf_valid(environ, user):
            return reply('403 Forbidden', {'error': 'Your session could not be verified. Refresh and try again.'})
        if action == 'logout':
            store.revoke_session(cookie_token(environ))
            return reply('200 OK', {'authenticated': False}, [('Set-Cookie', _cookie('', 0))])
        if action == 'user-status':
            store.set_user_enabled(payload.get('user_id'), payload.get('enabled'))
            return reply('200 OK', {'updated': True})
        if not _rate_allowed(environ, user['username'], action):
            return reply('429 Too Many Requests', {'error': 'Too many attempts. Please try again later.'}, [('Retry-After', str(AUTH_WINDOW))])
        if not _hash_slots.acquire(blocking=False):
            return reply('429 Too Many Requests', {'error': 'Account service is busy. Please try again.'}, [('Retry-After', '10')])
        try:
            current, new = payload.get('current_password'), payload.get('new_password')
            if isinstance(current, str) and isinstance(new, str) and secrets.compare_digest(current.encode('utf-8'), new.encode('utf-8')):
                raise store.AuthInvalid('Choose a different new password.')
            store.change_password(user['id'], current, new)
        finally:
            _hash_slots.release()
        return reply('200 OK', {'authenticated': False, 'message': 'Password changed. Sign in again.'}, [('Set-Cookie', _cookie('', 0))])
    except store.AuthConflict as exc:
        return reply('409 Conflict', {'error': str(exc)})
    except store.AuthInvalid as exc:
        return reply('400 Bad Request', {'error': str(exc)})
    except store.AuthUnavailable:
        return reply('503 Service Unavailable', {'error': 'Accounts are not configured or temporarily unavailable.'})
    except Exception:
        return reply('500 Internal Server Error', {'error': 'An internal account error occurred.'})

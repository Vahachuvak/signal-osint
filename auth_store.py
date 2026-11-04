"""Account storage with Argon2id passwords and server-side, hashed-token sessions.

SQLite is for local development only. Public deployments must configure a
persistent PostgreSQL DATABASE_URL; they never fall back to an ephemeral file.
"""
from contextlib import contextmanager
import base64
import hashlib
import os
from pathlib import Path
import re
import secrets
import sqlite3
import threading
import time
from urllib.parse import urlsplit
import uuid

try:
    from argon2 import PasswordHasher
    from argon2.exceptions import InvalidHashError, VerificationError
except ImportError:  # Local development can fall back to the standard library.
    PasswordHasher = None
    InvalidHashError = VerificationError = ValueError

ROOT = Path(__file__).resolve().parent
USERNAME_RE = re.compile(r'[A-Za-z0-9][A-Za-z0-9_.-]{2,31}\Z')
SESSION_RE = re.compile(r'[A-Za-z0-9_-]{43}\Z')
SESSION_TTL = 12 * 60 * 60
MAX_USERS = 5000
S_CRYPT_N, S_CRYPT_R, S_CRYPT_P = 2 ** 15, 8, 1
_schema_lock = threading.Lock()
_ready_schemas = set()
_dummy_lock = threading.Lock()
_dummy_hash = None
_argon2 = PasswordHasher(time_cost=2, memory_cost=19456, parallelism=1) if PasswordHasher else None


def hash_password(password):
    """Argon2id when available, otherwise the standard-library scrypt."""
    if _argon2 is not None:
        return _argon2.hash(password)
    salt = secrets.token_bytes(16)
    digest = hashlib.scrypt(password.encode('utf-8'), salt=salt, n=S_CRYPT_N, r=S_CRYPT_R,
                            p=S_CRYPT_P, maxmem=96 * 1024 * 1024, dklen=32)
    encoded = base64.urlsafe_b64encode(salt + digest).decode('ascii').rstrip('=')
    return f'$scrypt${S_CRYPT_N}${S_CRYPT_R}${S_CRYPT_P}${encoded}'


def verify_password(encoded, password):
    """Verify a stored hash; never raise on malformed input."""
    if not isinstance(encoded, str):
        return False
    if encoded.startswith('$argon2'):
        if _argon2 is None:
            raise AuthUnavailable('The password backend for existing accounts is not installed.')
        try:
            return _argon2.verify(encoded, password)
        except (VerificationError, InvalidHashError, ValueError, TypeError):
            return False
    if not encoded.startswith('$scrypt$'):
        return False
    try:
        raw_n, raw_r, raw_p, encoded_digest = encoded.split('$')[2:6]
        n, r, p = int(raw_n), int(raw_r), int(raw_p)
        data = base64.urlsafe_b64decode(encoded_digest + '=' * (-len(encoded_digest) % 4))
        if not (2 <= r <= 8 and 1 <= p <= 2 and 2 ** 14 <= n <= 2 ** 16) or len(data) < 17:
            return False
        salt, expected = data[:16], data[16:]
        actual = hashlib.scrypt(password.encode('utf-8') if isinstance(password, str) else b'',
                                salt=salt, n=n, r=r, p=p, maxmem=96 * 1024 * 1024, dklen=len(expected))
        return secrets.compare_digest(actual, expected)
    except (ValueError, TypeError):
        return False


class AuthUnavailable(Exception):
    """Accounts are not configured or the backing store is unavailable."""


class AuthInvalid(Exception):
    """A request has invalid account input or credentials."""


class AuthConflict(Exception):
    """The requested username is already taken."""


def validate_username(value):
    if not isinstance(value, str):
        raise AuthInvalid('Enter a valid username.')
    value = value.strip()
    if not USERNAME_RE.fullmatch(value):
        raise AuthInvalid('Username must be 3–32 Latin letters, numbers, dots, underscores or hyphens, starting with a letter or number.')
    return value


def validate_password(value):
    if not isinstance(value, str) or not 10 <= len(value) <= 128 or '\x00' in value:
        raise AuthInvalid('Password must be 10–128 characters long.')
    try:
        value.encode('utf-8')
    except UnicodeEncodeError as exc:
        raise AuthInvalid('Password contains invalid characters.') from exc
    return value


def _spec():
    url = os.environ.get('DATABASE_URL', '').strip()
    public = os.environ.get('SIGNAL_PUBLIC') == '1'
    if url:
        try:
            parsed = urlsplit(url)
            if parsed.scheme not in ('postgres', 'postgresql') or not parsed.hostname:
                raise ValueError()
        except ValueError as exc:
            raise AuthUnavailable('DATABASE_URL must be a PostgreSQL URL.') from exc
        return 'postgres', url, public
    if public:
        raise AuthUnavailable('A persistent PostgreSQL database must be configured.')
    path = os.environ.get('SIGNAL_DB_PATH') or str(ROOT / '.signal-data' / 'accounts.sqlite3')
    return 'sqlite', str(Path(path).expanduser().resolve()), False


@contextmanager
def _connect(spec):
    kind, value, public = spec
    conn = None
    try:
        if kind == 'sqlite':
            Path(value).parent.mkdir(parents=True, exist_ok=True)
            conn = sqlite3.connect(value, timeout=10)
            conn.row_factory = sqlite3.Row
            conn.execute('PRAGMA foreign_keys = ON')
        else:
            try:
                import psycopg
                from psycopg.rows import dict_row
            except ImportError as exc:
                raise AuthUnavailable('PostgreSQL dependencies are not installed.') from exc
            options = {'connect_timeout': 5, 'row_factory': dict_row}
            if public:
                options['sslmode'] = 'require'
            conn = psycopg.connect(value, **options)
        yield conn
        conn.commit()
    except (AuthUnavailable, AuthInvalid, AuthConflict):
        if conn:
            conn.rollback()
        raise
    except Exception as exc:
        if conn:
            conn.rollback()
        # Do not expose database URLs, credentials or internal error details.
        raise AuthUnavailable('The account service is temporarily unavailable.') from exc
    finally:
        if conn:
            conn.close()


def _run(conn, sql, params=()):
    return conn.execute(sql.replace('%s', '?') if isinstance(conn, sqlite3.Connection) else sql, params)


def _lock_bootstrap(conn):
    if isinstance(conn, sqlite3.Connection):
        _run(conn, 'BEGIN IMMEDIATE')
    else:
        _run(conn, 'SELECT pg_advisory_xact_lock(%s)', (72811970625,))


def _admin_exists(conn):
    return _run(conn, 'SELECT id FROM users WHERE is_admin = 1 LIMIT 1').fetchone() is not None


def _insert_admin(conn, username, password):
    username = validate_username(username)
    validate_password(password)
    if _admin_exists(conn):
        return False
    if _run(conn, 'SELECT id FROM users WHERE username_key = %s', (username.lower(),)).fetchone():
        raise AuthUnavailable('The administrator username is already in use.')
    _run(conn, 'INSERT INTO users (id, username, username_key, password_hash, is_admin, enabled, created_at) VALUES (%s, %s, %s, %s, 1, 1, %s)',
         (str(uuid.uuid4()), username, username.lower(), hash_password(password), int(time.time())))
    return True


def ensure_schema():
    spec = _spec()
    key = hashlib.sha256(repr(spec).encode('utf-8')).hexdigest()
    if key in _ready_schemas:
        return spec
    with _schema_lock:
        if key in _ready_schemas:
            return spec
        with _connect(spec) as conn:
            _lock_bootstrap(conn)
            _run(conn, '''CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY, username TEXT NOT NULL, username_key TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL, is_admin INTEGER NOT NULL DEFAULT 0 CHECK (is_admin IN (0,1)),
                enabled INTEGER NOT NULL DEFAULT 1 CHECK (enabled IN (0,1)), created_at BIGINT NOT NULL)''')
            _run(conn, '''CREATE TABLE IF NOT EXISTS sessions (
                token_hash TEXT PRIMARY KEY, user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                csrf_token TEXT NOT NULL, created_at BIGINT NOT NULL, expires_at BIGINT NOT NULL)''')
            _run(conn, 'CREATE INDEX IF NOT EXISTS sessions_user_id_idx ON sessions(user_id)')
            username = os.environ.get('SIGNAL_ADMIN_USERNAME', '').strip()
            password = os.environ.get('SIGNAL_ADMIN_PASSWORD', '')
            if not _admin_exists(conn) and username and password:
                try:
                    _insert_admin(conn, username, password)
                except AuthInvalid as exc:
                    raise AuthUnavailable('Administrator setup is invalid.') from exc
        _ready_schemas.add(key)
    return spec


def bootstrap_admin(username, password):
    """Create exactly one initial administrator. Never overwrite an existing account."""
    spec = ensure_schema()
    with _connect(spec) as conn:
        _lock_bootstrap(conn)
        return _insert_admin(conn, username, password)


def require_setup():
    spec = ensure_schema()
    with _connect(spec) as conn:
        if not _admin_exists(conn):
            raise AuthUnavailable('Accounts are not configured yet.')
    return spec


def _user_by_key(conn, key):
    return _run(conn, 'SELECT id, username, username_key, password_hash, is_admin, enabled, created_at FROM users WHERE username_key = %s', (key,)).fetchone()


def _verify(encoded, password):
    return verify_password(encoded, password)


def _get_dummy_hash():
    global _dummy_hash
    if _dummy_hash is None:
        with _dummy_lock:
            if _dummy_hash is None:
                _dummy_hash = hash_password(secrets.token_urlsafe(32))
    return _dummy_hash


def register_user(username, password):
    username = validate_username(username)
    password = validate_password(password)
    spec = require_setup()
    hashed = hash_password(password)
    user_id = str(uuid.uuid4())
    with _connect(spec) as conn:
        if _user_by_key(conn, username.lower()):
            raise AuthConflict('This username is already in use.')
        if _run(conn, 'SELECT COUNT(*) AS count FROM users').fetchone()['count'] >= MAX_USERS:
            raise AuthUnavailable('Registration is temporarily unavailable.')
        try:
            # ON CONFLICT closes the race between two concurrent registrations.
            cursor = _run(conn, 'INSERT INTO users (id, username, username_key, password_hash, is_admin, enabled, created_at) VALUES (%s, %s, %s, %s, 0, 1, %s) ON CONFLICT (username_key) DO NOTHING',
                          (user_id, username, username.lower(), hashed, int(time.time())))
            if cursor.rowcount != 1:
                raise AuthConflict('This username is already in use.')
        except AuthConflict:
            raise
    return {'id': user_id, 'username': username, 'password_hash': hashed}


def authenticate(username, password):
    # Keep a generic response for unknown, disabled, and invalid credentials.
    spec = require_setup()
    key = username.strip().lower() if isinstance(username, str) and len(username) <= 32 else ''
    password = password if isinstance(password, str) and len(password) <= 128 else ''
    with _connect(spec) as conn:
        row = _user_by_key(conn, key) if key else None
    encoded = row['password_hash'] if row else _get_dummy_hash()
    valid = _verify(encoded, password)
    if not row or not valid or not row['enabled']:
        raise AuthInvalid('Invalid username or password.')
    # The hash is used internally to prevent a login racing with a password change;
    # it must never be returned to the browser.
    return {'id': row['id'], 'username': row['username'], 'is_admin': bool(row['is_admin']), 'password_hash': row['password_hash']}


def new_session(user_id, expected_password_hash):
    spec = require_setup()
    token, csrf, now = secrets.token_urlsafe(32), secrets.token_urlsafe(32), int(time.time())
    digest = hashlib.sha256(token.encode('ascii')).hexdigest()
    with _connect(spec) as conn:
        _run(conn, 'DELETE FROM sessions WHERE expires_at <= %s', (now,))
        # Do not create a session for an account disabled after password verification.
        result = _run(conn, 'INSERT INTO sessions (token_hash, user_id, csrf_token, created_at, expires_at) SELECT %s, id, %s, %s, %s FROM users WHERE id = %s AND enabled = 1 AND password_hash = %s',
                      (digest, csrf, now, now + SESSION_TTL, user_id, expected_password_hash))
        if result.rowcount != 1:
            raise AuthInvalid('Invalid username or password.')
    return token


def session_user(token):
    if not isinstance(token, str) or not SESSION_RE.fullmatch(token):
        return None
    spec = require_setup()
    digest = hashlib.sha256(token.encode('ascii')).hexdigest()
    with _connect(spec) as conn:
        row = _run(conn, '''SELECT u.id, u.username, u.is_admin, s.csrf_token, s.expires_at
                            FROM sessions s JOIN users u ON u.id = s.user_id
                            WHERE s.token_hash = %s AND s.expires_at > %s AND u.enabled = 1''',
                   (digest, int(time.time()))).fetchone()
    if not row:
        return None
    return {'id': row['id'], 'username': row['username'], 'is_admin': bool(row['is_admin']),
            'csrf': row['csrf_token'], 'expires_at': row['expires_at']}


def revoke_session(token):
    if not isinstance(token, str) or not SESSION_RE.fullmatch(token):
        return
    spec = require_setup()
    with _connect(spec) as conn:
        _run(conn, 'DELETE FROM sessions WHERE token_hash = %s', (hashlib.sha256(token.encode('ascii')).hexdigest(),))


def change_password(user_id, current_password, new_password):
    validate_password(new_password)
    if not isinstance(current_password, str) or len(current_password) > 128:
        raise AuthInvalid('Current password is incorrect.')
    spec = require_setup()
    with _connect(spec) as conn:
        row = _run(conn, 'SELECT password_hash FROM users WHERE id = %s AND enabled = 1', (user_id,)).fetchone()
    if not row or not _verify(row['password_hash'], current_password):
        raise AuthInvalid('Current password is incorrect.')
    hashed = hash_password(new_password)
    with _connect(spec) as conn:
        changed = _run(conn, 'UPDATE users SET password_hash = %s WHERE id = %s AND enabled = 1 AND password_hash = %s',
                       (hashed, user_id, row['password_hash']))
        if changed.rowcount != 1:
            raise AuthInvalid('Account changed. Please sign in again.')
        _run(conn, 'DELETE FROM sessions WHERE user_id = %s', (user_id,))


def list_users():
    spec = require_setup()
    with _connect(spec) as conn:
        total = _run(conn, 'SELECT COUNT(*) AS count FROM users').fetchone()['count']
        rows = _run(conn, 'SELECT id, username, is_admin, enabled, created_at FROM users ORDER BY created_at DESC, id DESC LIMIT 200').fetchall()
    return {'total': total, 'users': [{'id': row['id'], 'username': row['username'], 'is_admin': bool(row['is_admin']),
                                       'enabled': bool(row['enabled']), 'created_at': row['created_at']} for row in rows]}


def set_user_enabled(user_id, enabled):
    if not isinstance(user_id, str) or not isinstance(enabled, bool):
        raise AuthInvalid('Invalid account request.')
    try:
        if str(uuid.UUID(user_id)) != user_id:
            raise ValueError()
    except (ValueError, AttributeError):
        raise AuthInvalid('Invalid account request.')
    spec = require_setup()
    with _connect(spec) as conn:
        changed = _run(conn, 'UPDATE users SET enabled = %s WHERE id = %s AND is_admin = 0', (1 if enabled else 0, user_id))
        if changed.rowcount != 1:
            raise AuthInvalid('Account not found or cannot be changed.')
        if not enabled:
            _run(conn, 'DELETE FROM sessions WHERE user_id = %s', (user_id,))

import io
from contextlib import closing
import json
import os
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest import mock
from wsgiref.util import setup_testing_defaults

import auth_store
import auth_web
import site_app


class AccountTests(unittest.TestCase):
    def setUp(self):
        temp_root = Path(os.environ.get('LOCALAPPDATA', tempfile.gettempdir())) / 'Temp' / 'opencode' if os.name == 'nt' else Path(tempfile.gettempdir())
        self.temp = tempfile.TemporaryDirectory(prefix='signal-auth-', dir=str(temp_root))
        self.db = str(Path(self.temp.name) / 'accounts.sqlite3')
        self.env = mock.patch.dict(os.environ, {'SIGNAL_DB_PATH': self.db, 'SIGNAL_PUBLIC': '0', 'DATABASE_URL': '',
                                                'SIGNAL_ADMIN_USERNAME': '', 'SIGNAL_ADMIN_PASSWORD': '', 'SIGNAL_TRUST_PROXY': '0'}, clear=False)
        self.env.start()
        with auth_web._attempts_lock:
            auth_web._attempts.clear()
        self.assertTrue(auth_store.bootstrap_admin('TestAdmin', 'demo_admin_password_1'))

    def tearDown(self):
        self.env.stop()
        self.temp.cleanup()

    def request(self, method, path, data=None, cookie='', csrf='', origin=True, extra=None):
        body = b'' if data is None else json.dumps(data).encode('utf-8')
        environ = {}
        setup_testing_defaults(environ)
        environ.update({'REQUEST_METHOD': method, 'PATH_INFO': path, 'SERVER_PORT': '8765',
                        'HTTP_HOST': '127.0.0.1:8765', 'REMOTE_ADDR': '127.0.0.1',
                        'wsgi.url_scheme': 'http', 'wsgi.input': io.BytesIO(body),
                        'CONTENT_LENGTH': str(len(body)), 'CONTENT_TYPE': 'application/json'})
        if origin:
            environ['HTTP_ORIGIN'] = 'http://127.0.0.1:8765'
        if cookie:
            environ['HTTP_COOKIE'] = cookie
        if csrf:
            environ['HTTP_X_CSRF_TOKEN'] = csrf
        environ.update(extra or {})
        result = {}
        def start_response(status, headers, exc_info=None):
            result['status'] = int(status.split()[0]); result['headers'] = dict(headers)
        content = b''.join(site_app.application(environ, start_response))
        result['body'] = content
        if result['headers'].get('Content-Type', '').startswith('application/json'):
            result['json'] = json.loads(content)
        return result

    def login(self, username='TestAdmin', password='demo_admin_password_1'):
        response = self.request('POST', '/api/auth/login', {'username': username, 'password': password})
        self.assertEqual(response['status'], 200, response['body'])
        cookie = response['headers']['Set-Cookie'].split(';', 1)[0]
        return cookie, response['json']['user']['csrf']

    def register(self, username='Alice_01', password='unique_user_password_1'):
        response = self.request('POST', '/api/auth/register', {'username': username, 'password': password, 'is_admin': True})
        self.assertEqual(response['status'], 201, response['body'])
        return response['headers']['Set-Cookie'].split(';', 1)[0], response['json']['user']

    def test_admin_area_requires_server_side_admin_role(self):
        self.assertEqual(self.request('GET', '/admin')['status'], 404)
        self.assertEqual(self.request('GET', '/api/admin/users')['status'], 404)
        regular_cookie, regular = self.register()
        self.assertFalse(regular['is_admin'])
        self.assertEqual(self.request('GET', '/admin', cookie=regular_cookie)['status'], 404)
        self.assertEqual(self.request('GET', '/api/admin/users', cookie=regular_cookie)['status'], 404)
        self.assertEqual(self.request('POST', '/api/admin/user-status', {'user_id': regular['id'], 'enabled': False}, cookie=regular_cookie, csrf=regular['csrf'])['status'], 404)
        admin_cookie, _ = self.login()
        self.assertEqual(self.request('GET', '/admin', cookie=admin_cookie)['status'], 200)
        result = self.request('GET', '/api/admin/users', cookie=admin_cookie)
        self.assertEqual(result['status'], 200)
        self.assertEqual(result['json']['total'], 2)
        self.assertNotIn(b'password_hash', result['body'])
        self.assertNotIn(b'demo_admin_password_1', result['body'])

    def test_passwords_are_argon2id_and_sessions_store_only_hashes(self):
        cookie, _ = self.register()
        token = cookie.split('=', 1)[1]
        with closing(sqlite3.connect(self.db)) as conn:
            hashes = [row[0] for row in conn.execute('SELECT password_hash FROM users ORDER BY username')]
            token_hashes = [row[0] for row in conn.execute('SELECT token_hash FROM sessions')]
        self.assertTrue(all(value.startswith('$argon2id$') for value in hashes))
        self.assertNotIn('unique_user_password_1', repr(hashes))
        self.assertNotIn(token, token_hashes)
        self.assertEqual(len(token_hashes[0]), 64)
        self.assertEqual(self.request('GET', '/api/auth/session', cookie=cookie)['json']['user']['username'], 'Alice_01')

    def test_origin_csrf_cookie_and_admin_protection(self):
        login = self.request('POST', '/api/auth/login', {'username': 'TestAdmin', 'password': 'demo_admin_password_1'})
        cookie_header = login['headers']['Set-Cookie']
        self.assertIn('HttpOnly', cookie_header)
        self.assertIn('SameSite=Lax', cookie_header)
        cookie = cookie_header.split(';', 1)[0]
        csrf = login['json']['user']['csrf']
        target_cookie, target = self.register()
        payload = {'user_id': target['id'], 'enabled': False}
        self.assertEqual(self.request('POST', '/api/admin/user-status', payload, cookie=cookie, csrf=csrf, origin=False)['status'], 403)
        self.assertEqual(self.request('POST', '/api/admin/user-status', payload, cookie=cookie, csrf='not-valid')['status'], 403)
        self.assertEqual(self.request('POST', '/api/admin/user-status', payload, cookie=cookie, csrf=csrf, extra={'HTTP_ORIGIN': 'https://evil.example'})['status'], 403)
        self.assertTrue(self.request('GET', '/api/auth/session', cookie=target_cookie)['json']['authenticated'])
        self.assertEqual(self.request('POST', '/api/admin/user-status', payload, cookie=cookie, csrf=csrf)['status'], 200)
        self.assertFalse(self.request('GET', '/api/auth/session', cookie=target_cookie)['json']['authenticated'])
        self.assertEqual(self.request('POST', '/api/auth/login', {'username': 'Alice_01', 'password': 'unique_user_password_1'})['status'], 400)
        self.assertEqual(self.request('POST', '/api/admin/user-status', {'user_id': target['id'], 'enabled': True}, cookie=cookie, csrf=csrf)['status'], 200)
        self.login('alice_01', 'unique_user_password_1')
        admin_id = login['json']['user']['id']
        self.assertEqual(self.request('POST', '/api/admin/user-status', {'user_id': admin_id, 'enabled': False}, cookie=cookie, csrf=csrf)['status'], 400)

    def test_password_change_revokes_all_sessions_and_old_password(self):
        cookie, user = self.register()
        second, _ = self.login('Alice_01', 'unique_user_password_1')
        denied = self.request('POST', '/api/auth/change-password', {'current_password': 'wrong', 'new_password': 'different_password_2'}, cookie=cookie, csrf=user['csrf'])
        self.assertEqual(denied['status'], 400)
        result = self.request('POST', '/api/auth/change-password', {'current_password': 'unique_user_password_1', 'new_password': 'different_password_2'}, cookie=cookie, csrf=user['csrf'])
        self.assertEqual(result['status'], 200)
        self.assertIn('Max-Age=0', result['headers']['Set-Cookie'])
        self.assertFalse(self.request('GET', '/api/auth/session', cookie=second)['json']['authenticated'])
        self.assertEqual(self.request('POST', '/api/auth/login', {'username': 'Alice_01', 'password': 'unique_user_password_1'})['status'], 400)
        self.login('Alice_01', 'different_password_2')

    def test_old_password_cannot_create_session_after_password_change(self):
        self.register()
        user = auth_store.authenticate('Alice_01', 'unique_user_password_1')
        auth_store.change_password(user['id'], 'unique_user_password_1', 'different_password_2')
        with self.assertRaises(auth_store.AuthInvalid):
            auth_store.new_session(user['id'], user['password_hash'])

    def test_expiration_duplicate_names_and_bootstrap_no_reset(self):
        cookie, _ = self.register()
        duplicate = self.request('POST', '/api/auth/register', {'username': 'alice_01', 'password': 'different_password_2'})
        self.assertEqual(duplicate['status'], 409)
        self.assertFalse(auth_store.bootstrap_admin('OtherAdmin', 'different_password_2'))
        with closing(sqlite3.connect(self.db)) as conn:
            conn.execute('UPDATE sessions SET expires_at = 0')
            conn.commit()
        self.assertFalse(self.request('GET', '/api/auth/session', cookie=cookie)['json']['authenticated'])
        self.assertEqual(self.request('GET', '/admin', cookie=cookie)['status'], 404)

    def test_invalid_login_is_rate_limited(self):
        for _ in range(8):
            self.assertEqual(self.request('POST', '/api/auth/login', {'username': 'Unknown', 'password': 'wrong-password'})['status'], 400)
        self.assertEqual(self.request('POST', '/api/auth/login', {'username': 'Unknown', 'password': 'wrong-password'})['status'], 429)

    def test_public_mode_requires_database_and_never_falls_back_to_sqlite(self):
        missing = str(Path(self.temp.name) / 'missing.sqlite3')
        with mock.patch.dict(os.environ, {'SIGNAL_PUBLIC': '1', 'SIGNAL_DB_PATH': missing, 'DATABASE_URL': ''}, clear=False):
            with self.assertRaises(auth_store.AuthUnavailable):
                auth_store.require_setup()
        self.assertFalse(Path(missing).exists())

    def test_public_cookie_is_secure_and_requires_https(self):
        fake_user = {'id': '1', 'username': 'TestAdmin', 'is_admin': True, 'password_hash': 'not-sent'}
        session = {'id': '1', 'username': 'TestAdmin', 'is_admin': True, 'csrf': 'c' * 43, 'expires_at': 9999999999}
        extra = {'HTTP_HOST': 'app.example', 'HTTP_ORIGIN': 'https://app.example', 'HTTP_X_FORWARDED_PROTO': 'https'}
        with mock.patch.dict(os.environ, {'SIGNAL_PUBLIC': '1', 'SIGNAL_TRUST_PROXY': '1', 'SIGNAL_ALLOWED_HOSTS': 'app.example'}, clear=False), \
             mock.patch.object(auth_store, 'authenticate', return_value=fake_user), \
             mock.patch.object(auth_store, 'new_session', return_value='t' * 43), \
             mock.patch.object(auth_store, 'session_user', return_value=session):
            response = self.request('POST', '/api/auth/login', {'username': 'TestAdmin', 'password': 'anything'}, extra=extra)
            self.assertEqual(response['status'], 200)
            self.assertIn('; Secure', response['headers']['Set-Cookie'])
            self.assertNotIn(b'not-sent', response['body'])
            extra.update({'HTTP_ORIGIN': 'http://app.example', 'HTTP_X_FORWARDED_PROTO': 'http'})
            self.assertEqual(self.request('POST', '/api/auth/login', {'username': 'TestAdmin', 'password': 'anything'}, extra=extra)['status'], 503)


if __name__ == '__main__':
    unittest.main()

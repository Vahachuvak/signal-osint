import http.client
import json
import socket
import threading
import unittest
from unittest import mock
from wsgiref.simple_server import make_server

import osint_engine as engine
import people_osint as people
import site_app
import web_command_center


def response(body=b'', status=200, content_type='text/html; charset=utf-8', **kwargs):
    return {'status': status, 'headers': {'content-type': content_type, **kwargs.get('headers', {})},
            'cookies': kwargs.get('cookies', []), 'body': body, 'truncated': kwargs.get('truncated', False),
            'tls': kwargs.get('tls'), 'duration': 25, 'error': None}


class TargetTests(unittest.TestCase):
    def test_normalization_and_query_not_in_display(self):
        target = engine.parse_target('https://Example.COM/path?q=secret')
        self.assertEqual(target['host'], 'example.com')
        self.assertEqual(target['path'], '/path?q=secret')
        self.assertEqual(target['display_url'], 'https://example.com/path')
        self.assertTrue(target['has_query'])

    def test_rejects_invalid_inputs(self):
        for value in ('', 'ftp://example.com', 'http://a:b@example.com',
                      'https://example.com:0', 'http://example.com:8080', 'https://bad host',
                      'https://example.com\\@127.0.0.1', 'https://-bad.example'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                engine.parse_target(value)

    def test_rejects_private_and_mixed_dns_answers(self):
        def addr(ip):
            return (socket.AF_INET, socket.SOCK_STREAM, 6, '', (ip, 0))
        with mock.patch('socket.getaddrinfo', return_value=[addr('93.184.216.34'), addr('127.0.0.1')]):
            with self.assertRaises(ValueError):
                engine.resolve_public('example.com')
        with mock.patch('socket.getaddrinfo', return_value=[addr('224.0.0.1')]):
            with self.assertRaises(ValueError):
                engine.resolve_public('example.com')

    def test_transport_connects_to_pinned_address(self):
        fake_sock = mock.Mock()
        with mock.patch('socket.create_connection', return_value=fake_sock) as create:
            conn = engine.PinnedHTTP('example.com', 80, '93.184.216.34')
            conn.connect()
            create.assert_called_once_with(('93.184.216.34', 80), engine.TIMEOUT)

    def test_no_retry_after_request_has_started(self):
        conn = mock.Mock()
        conn.request.side_effect = OSError('connection dropped')
        with mock.patch.object(engine, 'PinnedHTTP', return_value=conn) as factory:
            result = engine.fetch(engine.parse_target('http://example.com'), ['1.1.1.1', '8.8.8.8'], '/')
        self.assertEqual(factory.call_count, 1)
        self.assertIsNone(result['status'])


class ParsingTests(unittest.TestCase):
    def test_html_extracts_without_secrets_or_inline_resources(self):
        page = engine.PageParser('https://example.com/page')
        page.feed('''<html lang="ru"><title>Example</title><meta name="description" content="Hello">
          <script>inline()</script><script src="https://cdn.example.org/a.js?token=secret"></script>
          <a href="https://other.example/link?password=secret">A</a><a href="mailto:team@example.com">Mail</a>
          <form method="post" action="/search?token=secret"><input name="query" value="secret"></form>
          <img src="/a.png"><img src="/b.png" alt=""></html>''')
        self.assertEqual(page.title, 'Example')
        self.assertEqual(page.lang, 'ru')
        self.assertEqual(page.links, ['https://other.example/link'])
        self.assertEqual(page.emails, ['team@example.com'])
        self.assertEqual(page.forms[0]['fields'], ['query'])
        self.assertNotIn('secret', str(page.forms))
        self.assertEqual(len(page.resources), 3)
        self.assertEqual(page.missing_alt, 1)

    def test_sitemap_and_robots(self):
        robots = response(b'User-agent: *\nDisallow: /private\nSitemap: https://x.org/sitemap.xml\n', content_type='text/plain')
        self.assertEqual(len(engine.parse_robots(robots)), 3)
        sitemap = response(b'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://x.org/a</loc></url></urlset>', content_type='application/xml')
        self.assertEqual(engine.parse_sitemap(sitemap), ['https://x.org/a'])
        sitemap['truncated'] = True
        self.assertIsNone(engine.parse_sitemap(sitemap))
        self.assertIsNone(engine.parse_sitemap(response(b'<!DOCTYPE foo><urlset/>', content_type='application/xml')))

    def test_cookie_values_never_returned(self):
        result = engine.cookie_facts(['sid=top-secret; Secure; HttpOnly; SameSite=Lax'])
        self.assertNotIn('top-secret', str(result))
        self.assertEqual(result[0][0], 'sid')
        self.assertIn('HttpOnly', result[0][1])


class InspectionTests(unittest.TestCase):
    def test_full_inspection_is_bounded_and_no_ct_without_opt_in(self):
        html = b'''<html lang="en"><title>Example</title><meta name="generator" content="Test">
            <a href="https://external.example/a?token=top-secret">external</a>
            <form action="/search?token=top-secret"><input name="q" value="top-secret"></form>
            <script src="https://cdn.example.net/a.js"></script>sqlite3.OperationalError</html>'''
        tls = {'version': 'TLSv1.3', 'issuer': 'Test CA', 'expires': 'Jan 1 2030', 'subject_alt_names': ['example.org']}
        def fake_fetch(target, addresses, path, limit=engine.BODY_LIMIT):
            if path.startswith('/page'):
                return response(html, tls=tls, cookies=['sid=top-secret; Secure; HttpOnly'],
                                headers={'location': 'https://example.org/next?token=top-secret', 'server': 'Example'})
            if path == '/robots.txt':
                return response(b'User-agent: *\n', content_type='text/plain')
            if path == '/sitemap.xml':
                return response(b'<urlset><url><loc>https://example.org/page</loc></url></urlset>', content_type='application/xml')
            return response(b'Contact: mailto:security@example.org\n', content_type='text/plain')
        with mock.patch.object(engine, 'resolve_public', return_value=['93.184.216.34']), \
             mock.patch.object(engine, 'fetch', side_effect=fake_fetch) as fetch, \
             mock.patch.object(engine, 'collect_ct', side_effect=AssertionError('unexpected external lookup')), \
             mock.patch.object(engine, 'collect_rdap', side_effect=AssertionError('unexpected external lookup')), \
             mock.patch.object(engine, 'collect_archive', side_effect=AssertionError('unexpected external lookup')):
            result = engine.inspect_target('https://example.org/page?token=top-secret')
        self.assertEqual(fetch.call_count, 4)
        self.assertEqual(len(result['modules']), 20)
        self.assertEqual(result['status'], 200)
        self.assertNotIn('top-secret', json.dumps(result))
        self.assertEqual(next(m for m in result['modules'] if m['id'] == 'ct')['status'], 'disabled')
        self.assertEqual(next(m for m in result['modules'] if m['id'] == 'database')['status'], 'warning')
        self.assertIn('cdn.example.net', [n['label'] for n in result['graph']['nodes']])

    def test_ct_opt_in_and_no_out_of_scope_names(self):
        payload = json.dumps([{'name_value': 'a.example.org\n*.b.example.org\noutside.example.net'}]).encode()
        with mock.patch.object(engine, 'resolve_public', return_value=['1.1.1.1']), \
             mock.patch.object(engine, 'fetch', return_value=response(payload, content_type='application/json')):
            result = engine.collect_ct('example.org')
        self.assertEqual(result['names'], ['a.example.org', 'b.example.org'])
        self.assertIsNone(result['error'])

    def test_optional_sources_and_graph(self):
        rdap = {'facts': [('NS-сервер', 'ns.example.org')], 'nameservers': ['ns.example.org'], 'error': None}
        ct = {'names': ['sub.example.org'], 'error': None}
        archive = {'snapshot': {'url': 'https://web.archive.org/web/20200101/https://example.org/', 'timestamp': '20200101', 'status': '200'}, 'error': None}
        with mock.patch.object(engine, 'resolve_public', return_value=['93.184.216.34']), \
             mock.patch.object(engine, 'fetch', return_value=response(b'<html></html>')), \
             mock.patch.object(engine, 'collect_ct', return_value=ct), \
             mock.patch.object(engine, 'collect_rdap', return_value=rdap), \
             mock.patch.object(engine, 'collect_archive', return_value=archive):
            result = engine.inspect_target('example.org', use_ct=True, use_rdap=True, use_archive=True)
        self.assertEqual([m['status'] for m in result['modules'][-3:]], ['ok', 'ok', 'ok'])
        self.assertIn('ns.example.org', [node['label'] for node in result['graph']['nodes']])
        self.assertEqual(len(result['external_sources']), 3)

    def test_rdap_extracts_registration_and_nameservers(self):
        data = {'objectClassName': 'domain', 'ldhName': 'EXAMPLE.ORG', 'status': ['active'],
                'events': [{'eventAction': 'registration', 'eventDate': '2001-01-01'}],
                'nameservers': [{'ldhName': 'NS1.EXAMPLE.ORG'}],
                'entities': [{'roles': ['registrar'], 'vcardArray': ['vcard', [['fn', {}, 'text', 'Example Registrar']]]}]}
        with mock.patch.object(engine, 'fetch_external_json', return_value=data):
            result = engine.collect_rdap('example.org')
        self.assertIsNone(result['error'])
        self.assertEqual(result['nameservers'], ['ns1.example.org'])
        self.assertIn(('Registrar', 'Example Registrar'), result['facts'])

    def test_archive_snapshot_and_invalid_host(self):
        data = {'archived_snapshots': {'closest': {'available': True, 'url': 'https://web.archive.org/web/20200101000000/https://example.org/', 'timestamp': '20200101000000', 'status': '200'}}}
        with mock.patch.object(engine, 'fetch_external_json', return_value=data):
            result = engine.collect_archive('example.org', 'https')
        self.assertEqual(result['snapshot']['timestamp'], '20200101000000')
        data['archived_snapshots']['closest']['url'] = 'https://evil.example/snapshot'
        with mock.patch.object(engine, 'fetch_external_json', return_value=data):
            result = engine.collect_archive('example.org', 'https')
        self.assertIsNotNone(result['error'])

    def test_external_redirect_revalidates_destination(self):
        redirect = response(b'', status=302, headers={'location': 'http://127.0.0.1/private'})
        def resolve(host):
            if host == '127.0.0.1':
                raise ValueError('private address')
            return ['1.1.1.1']
        with mock.patch.object(engine, 'resolve_public', side_effect=resolve), mock.patch.object(engine, 'fetch', return_value=redirect) as fetch:
            with self.assertRaises(ValueError):
                engine.fetch_external_json('https://rdap.org/domain/example.org', redirects=3)
        self.assertEqual(fetch.call_count, 1)


class APITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = make_server('127.0.0.1', 0, site_app.application, server_class=web_command_center.LocalServer)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def request(self, method, path, body=None, headers=None):
        conn = http.client.HTTPConnection('127.0.0.1', self.server.server_port, timeout=5)
        try:
            conn.request(method, path, body=body, headers=headers or {})
            reply = conn.getresponse()
            return reply.status, reply.read()
        finally:
            conn.close()

    def test_page_served(self):
        status, body = self.request('GET', '/')
        self.assertEqual(status, 200)
        self.assertIn(b'SIGNAL', body)
        # The homepage presents the site and links into both workspaces.
        self.assertIn(b'Find the signal', body)
        self.assertIn(b'href="/people"', body)
        self.assertIn(b'href="/app"', body)
        self.assertIn(b'/app', body)
        status, body = self.request('GET', '/people')
        self.assertEqual(status, 200)
        self.assertIn(b'PEOPLE', body)
        status, body = self.request('GET', '/app')
        self.assertEqual(status, 200)
        self.assertIn(b'20', body)
        self.assertEqual(self.request('GET', '/healthz')[0], 200)
        self.assertEqual(self.request('GET', '/people')[0], 200)
        self.assertEqual(self.request('GET', '/sites')[0], 200)
        status, body = self.request('GET', '/media')
        self.assertEqual(status, 200)
        self.assertIn(b'https://t.me/Signal_osint', body)
        self.assertNotIn(b'send.monobank.ua', body)
        self.assertIn(b'UQDUCRzOw8x8DCQ5VOrvt--vr0Se1Y5hUoP4nwg9qQoWjKc0', body)
        self.assertEqual(self.request('GET', '/media/')[0], 200)
        self.assertEqual(self.request('GET', '/signal.css')[0], 200)
        self.assertEqual(self.request('GET', '/people_enhancements.js')[0], 200)
        self.assertEqual(self.request('GET', '/signal_i18n.js')[0], 200)
        self.assertEqual(self.request('GET', '/account.js')[0], 200)
        self.assertEqual(self.request('GET', '/admin.js')[0], 200)
        for path in ('/', '/people', '/sites', '/app', '/media', '/updates', '/updates/', '/account', '/account/'):
            with self.subTest(path=path):
                status, body = self.request('GET', path)
                self.assertEqual(status, 200)
                self.assertIn(b'lang="en"', body)
                self.assertIn(b'/signal_i18n.js', body)
        status, body = self.request('GET', '/updates')
        self.assertIn(b'CURRENT UPDATE', body)
        self.assertIn(b'PREVIOUS UPDATE', body)
        self.assertIn(b'TON', body)
        self.assertIn(b'A new homepage presents the project', body)

    def test_people_platform_group_through_http(self):
        result = ('unverified', people.UNCLEAR_RE, 'https://example.org/profile')
        with mock.patch.object(people, 'check_platform', return_value=result) as checker:
            status, body = self.request('POST', '/api/people',
                                        json.dumps({'username': 'example', 'sources': ['platforms']}),
                                        {'Content-Type': 'application/json'})
        self.assertEqual(status, 200)
        data = json.loads(body)
        self.assertEqual(checker.call_count, len(people.PLATFORMS))
        self.assertEqual(sum(m['id'].startswith('platform_') for m in data['modules']), len(people.PLATFORMS))
        self.assertEqual(next(m for m in data['modules'] if m['id'] == 'platform_telegram')['status'], 'unverified')

    def test_photo_upload_csp_is_limited_to_people_and_google_lens(self):
        for path, allowed in [('/people', True), ('/people/', True), ('/', False), ('/account', False)]:
            with self.subTest(path=path):
                conn = http.client.HTTPConnection('127.0.0.1', self.server.server_port, timeout=5)
                try:
                    conn.request('GET', path)
                    response = conn.getresponse()
                    policy = response.getheader('Content-Security-Policy')
                    response.read()
                finally:
                    conn.close()
                self.assertIn("form-action 'self'", policy)
                self.assertEqual('https://lens.google.com' in policy, allowed)
                self.assertEqual('https://www.google.com' in policy, allowed)
                self.assertIn("connect-src 'self'", policy)
        status, script = self.request('GET', '/people_enhancements.js')
        self.assertEqual(status, 200)
        self.assertIn(b'action="https://lens.google.com/upload"', script)
        self.assertIn(b'name="encoded_image"', script)

    def test_spanish_ui_covers_existing_labels_and_replaces_russian_switch(self):
        import ast
        import re
        source = (site_app.ROOT / 'signal_i18n.js').read_text(encoding='utf-8')
        quoted = r'''(?:'(?:\\.|[^'\\])*'|"(?:\\.|[^"\\])*")'''
        def keys(name):
            block = source.split('const ' + name + ' = {', 1)[1].split('  };', 1)[0]
            return {ast.literal_eval(value) for value in re.findall('(' + quoted + r')\s*:', block)}
        self.assertFalse(keys('ru') - keys('es'))
        self.assertIn("language === 'en' ? 'es' : 'en'", source)
        self.assertNotIn("language === 'en' ? 'ru' : 'en'", source)
        self.assertIn("localStorage.getItem('signal-language') === 'es'", source)

    def test_cross_origin_and_host_rejected(self):
        self.assertEqual(self.request('GET', '/', headers={'Host': 'evil.example'})[0], 403)
        # No body is needed to test origin rejection. Leaving unread POST bytes
        # can reset the local Windows development socket before its 403 arrives.
        self.assertEqual(self.request('POST', '/api/inspect', None, {'Origin': 'https://evil.example', 'Content-Type': 'application/json'})[0], 403)

    def test_api_json_and_boolean_options(self):
        with mock.patch.object(site_app, 'inspect_target', return_value={'version': 2}) as inspect:
            status, body = self.request('POST', '/api/inspect', '{"target":"example.com","ct":true}', {'Content-Type': 'application/json'})
            self.assertEqual(status, 200)
            self.assertEqual(json.loads(body)['version'], 2)
            inspect.assert_called_once_with('example.com', use_ct=True, use_rdap=False, use_archive=False)
        self.assertEqual(self.request('POST', '/api/inspect', '{"ct":"yes"}', {'Content-Type': 'application/json'})[0], 400)
        self.assertEqual(self.request('POST', '/api/inspect', '{}', {'Content-Type': 'text/plain'})[0], 400)

    def test_people_api(self):
        with mock.patch.object(site_app, 'search_people', return_value={'version': 1}) as search:
            status, body = self.request('POST', '/api/people', '{"username":"octocat","name":"","sources":["github"]}', {'Content-Type': 'application/json'})
            self.assertEqual(status, 200)
            self.assertEqual(json.loads(body)['version'], 1)
            search.assert_called_once_with('octocat', '', ['github'], orcid='', context='')
        with mock.patch.object(site_app, 'search_people', return_value={'version': 1}) as search:
            payload = '{"username":"","name":"","sources":["orcid"],"orcid":"0000-0002-1825-0097","context":"Research"}'
            status, _ = self.request('POST', '/api/people', payload, {'Content-Type': 'application/json'})
            self.assertEqual(status, 200)
            search.assert_called_once_with('', '', ['orcid'], orcid='0000-0002-1825-0097', context='Research')

    def test_public_mode_same_origin_and_allowed_hosts(self):
        with mock.patch.dict('os.environ', {'SIGNAL_PUBLIC': '1', 'SIGNAL_TRUST_PROXY': '1', 'SIGNAL_ALLOWED_HOSTS': 'app.example'}, clear=False), \
             mock.patch.object(site_app, 'inspect_target', return_value={'version': 2}):
            valid = {'Host': 'app.example', 'Origin': 'https://app.example', 'X-Forwarded-Proto': 'https', 'Content-Type': 'application/json'}
            self.assertEqual(self.request('POST', '/api/inspect', '{"target":"example.com"}', valid)[0], 200)
            self.assertEqual(self.request('POST', '/api/inspect', None, {**valid, 'Origin': 'https://evil.example'})[0], 403)
            self.assertEqual(self.request('POST', '/api/inspect', None, {'Host': 'app.example', 'Content-Type': 'application/json'})[0], 403)
            self.assertEqual(self.request('GET', '/', headers={'Host': 'evil.example'})[0], 403)

    def test_global_rate_limit(self):
        with site_app._rate_lock:
            site_app._scan_times.clear()
        try:
            with mock.patch.object(site_app, 'SCAN_LIMIT', 1), mock.patch.object(site_app, 'inspect_target', return_value={'version': 2}):
                headers = {'Content-Type': 'application/json'}
                self.assertEqual(self.request('POST', '/api/inspect', '{"target":"example.com"}', headers)[0], 200)
                self.assertEqual(self.request('POST', '/api/inspect', '{"target":"example.com"}', headers)[0], 429)
        finally:
            with site_app._rate_lock:
                site_app._scan_times.clear()


if __name__ == '__main__':
    unittest.main()

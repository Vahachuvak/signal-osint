import json
import unittest
from unittest import mock

import people_osint as people


class PeopleValidationTests(unittest.TestCase):
    def test_rejects_bad_inputs_and_unknown_sources(self):
        cases = [('', '', ['github']), ('person@example.com', '', ['github']),
                 ('http://example.com', '', ['github']), ('name/../admin', '', ['github']),
                 ('valid', '<script>', ['github']), ('valid', '', ['unknown']),
                 ('valid', '', []), ('', 'Ada Lovelace', ['github'])]
        for username, name, sources in cases:
            with self.subTest(username=username, name=name, sources=sources), self.assertRaises(ValueError):
                people.validate(username, name, sources)

    def test_username_normalization_and_name_only(self):
        self.assertEqual(people.validate('@octocat', '', ['github'])[0], 'octocat')
        self.assertEqual(people.validate('', 'Ада  Лавлейс', ['wikipedia'])[1], 'Ада Лавлейс')

    def test_orcid_checksum_and_context_validation(self):
        self.assertEqual(people.normalize_orcid('0000000218250097'), '0000-0002-1825-0097')
        for value in ('0000-0002-1825-0098', 'https://orcid.org/0000-0002-1825-0097', '000000021825009Z'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                people.normalize_orcid(value)
        with self.assertRaises(ValueError):
            people.validate('octocat', '', ['github'], context='person@example.com')


class PeopleSearchTests(unittest.TestCase):
    def test_sources_exact_match_and_no_private_biography(self):
        seen = []
        def fake_get(url):
            seen.append(url)
            if 'api.github.com/users/octocat/repos' in url:
                return ([{'name': 'project', 'owner': {'login': 'octocat'}, 'stargazers_count': 0, 'language': 'Python'},
                         {'name': 'bad<script>', 'owner': {'login': 'octocat'}}], None)
            if 'api.github.com/users/octocat/orgs' in url:
                return ([{'login': 'public-org'}], None)
            if 'api.github.com/users/octocat' in url:
                return ({'login': 'octocat', 'type': 'User', 'name': 'Public Name', 'followers': 0,
                         'bio': 'secret@example.org', 'email': 'secret@example.org'}, None)
            if 'gitlab.com' in url:
                return ([{'username': 'other', 'name': 'Wrong'}, {'username': 'octocat', 'name': 'Name', 'state': 'active'}], None)
            if 'firebaseio.com' in url:
                return ({'id': 'octocat', 'karma': 3, 'created': 1700000000, 'about': 'secret@example.org'}, None)
            if 'dev.to' in url:
                return ({'username': 'octocat', 'name': 'Name', 'summary': 'secret@example.org'}, None)
            if 'wikipedia.org' in url:
                return ({'query': {'search': [{'title': 'Ada Lovelace', 'pageid': 123}]}}, None)
            self.fail('unexpected URL: ' + url)
        with mock.patch.object(people, 'get_json', side_effect=fake_get):
            result = people.search_people('octocat', 'Ada Lovelace', ['github', 'gitlab', 'hackernews', 'devto', 'wikipedia'])
        self.assertEqual(len(seen), 8)
        self.assertEqual(len(result['modules']), 15)
        self.assertEqual(result['modules'][0]['status'], 'ok')
        self.assertIn({'label': 'Followers', 'value': '0'}, result['modules'][0]['facts'])
        self.assertNotIn('secret@example.org', json.dumps(result))
        self.assertNotIn('bad<script>', json.dumps(result))
        self.assertEqual(len(result['manual_links']), 30)
        self.assertEqual(result['modules'][-1]['status'], 'ready')
        self.assertEqual(result['graph']['nodes'][0]['label'], 'Search query')
        self.assertTrue(any(edge['source'] == 'query:name' for edge in result['graph']['edges']))
        self.assertTrue(any(edge['source'] == 'query:username' for edge in result['graph']['edges']))
        node_ids = {node['id'] for node in result['graph']['nodes']}
        self.assertTrue(all(edge['source'] in node_ids and edge['target'] in node_ids for edge in result['graph']['edges']))
        self.assertTrue(any(edge['source'].startswith('profile:GitHub') and edge['target'].startswith('repo:') for edge in result['graph']['edges']))
        self.assertEqual(sum(x['kind'] == 'article' for x in result['graph']['nodes']), 2)

    def test_only_selected_sources_are_called_and_errors_are_visible(self):
        with mock.patch.object(people, 'get_json', return_value=(None, 'HTTP 429')) as getter:
            result = people.search_people('example', '', ['devto'])
        self.assertEqual(getter.call_count, 1)
        modules = {m['id']: m for m in result['modules']}
        self.assertEqual(modules['devto']['status'], 'error')
        self.assertEqual(modules['github']['status'], 'disabled')
        self.assertEqual(modules['wiki_ru']['status'], 'disabled')
        self.assertIn('429', modules['devto']['summary'])

    def test_name_only_and_no_identity_confirmation(self):
        with mock.patch.object(people, 'get_json', return_value=({'query': {'search': []}}, None)) as getter:
            result = people.search_people('', 'Ада Лавлейс', ['wikipedia'])
        self.assertEqual(getter.call_count, 2)
        self.assertEqual(len(result['manual_links']), 15)
        self.assertIn('does not confirm identity', result['notice'])

    def test_stackoverflow_is_a_fuzzy_search_not_identity_verification(self):
        data = {'items': [{'user_id': 123, 'display_name': 'Ada', 'reputation': 42}]}
        with mock.patch.object(people, 'get_json', return_value=(data, None)) as getter:
            result = people.search_people('', 'Ada Lovelace', ['stackoverflow'])
        self.assertIn('inname=Ada+Lovelace', getter.call_args.args[0])
        module = next(m for m in result['modules'] if m['id'] == 'stackoverflow')
        self.assertEqual(module['status'], 'ok')
        self.assertIn('identity is not confirmed', module['items'][0]['detail'])
        self.assertEqual(module['items'][0]['url'], 'https://stackoverflow.com/users/123')

    def test_orcid_record_whitelists_only_public_name(self):
        data = {'name': {'given-names': {'value': 'Josiah'}, 'family-name': {'value': 'Carberry'}},
                'emails': {'email': [{'email': 'private@example.com'}]}}
        with mock.patch.object(people, 'get_json', return_value=(data, None)) as getter:
            result = people.search_people('', '', ['orcid'], orcid='0000-0002-1825-0097')
        getter.assert_called_once_with('https://pub.orcid.org/v3.0/0000-0002-1825-0097/person')
        module = next(m for m in result['modules'] if m['id'] == 'orcid')
        self.assertEqual(module['status'], 'ok')
        self.assertNotIn('private@example.com', json.dumps(result))
        self.assertEqual(result['manual_links'][0]['url'], 'https://orcid.org/0000-0002-1825-0097')
        self.assertTrue(any(edge['source'] == 'query:orcid' for edge in result['graph']['edges']))

    def test_crossref_results_are_not_identity_confirmation(self):
        data = {'message': {'items': [{'title': ['A paper'], 'DOI': '10.1234/example'},
                                     {'title': ['Invalid DOI'], 'DOI': 'https://evil.test'}]}}
        with mock.patch.object(people, 'get_json', return_value=(data, None)):
            result = people.search_people('', 'Ada Lovelace', ['crossref'], context='Mathematics')
        module = next(m for m in result['modules'] if m['id'] == 'crossref')
        self.assertEqual(module['status'], 'ok')
        self.assertEqual(len(module['items']), 1)
        self.assertEqual(module['items'][0]['url'], 'https://doi.org/10.1234/example')
        self.assertIn('authorship is not confirmed', module['items'][0]['detail'])
        self.assertIn('Mathematics', result['manual_links'][0]['url'])

    def test_wikidata_search_reports_results_and_validates_urls(self):
        data = {'search': [{'id': 'Q7259', 'label': 'Ada Lovelace', 'description': 'English mathematician'},
                           {'id': 'https://evil.example/', 'label': 'Invalid'},
                           {'id': 'Q0', 'label': 'Invalid'}]}
        with mock.patch.object(people, 'get_json', return_value=(data, None)) as getter:
            result = people.search_people('', 'Ada Lovelace', ['wikidata'])
        self.assertEqual(getter.call_count, 1)
        self.assertIn('wikidata.org/w/api.php', getter.call_args.args[0])
        module = next(m for m in result['modules'] if m['id'] == 'wikidata')
        self.assertEqual(module['status'], 'ok')
        self.assertEqual(len(module['items']), 1)
        self.assertEqual(module['items'][0]['url'], 'https://www.wikidata.org/wiki/Q7259')
        self.assertIn('identity is not confirmed', module['items'][0]['detail'])
        self.assertTrue(any(edge['source'] == 'query:name' and edge['target'].startswith('article:')
                            for edge in result['graph']['edges']))

    def test_wikidata_unavailable_and_bad_response_are_visible(self):
        for response, status in [((None, 'HTTP 429'), 'error'), (({}, None), 'error'),
                                 (({'search': []}, None), 'none')]:
            with self.subTest(response=response), mock.patch.object(people, 'get_json', return_value=response):
                result = people.search_people('', 'Ada Lovelace', ['wikidata'])
                self.assertEqual(next(m for m in result['modules'] if m['id'] == 'wikidata')['status'], status)

    def test_graph_prioritizes_source_matches_over_github_repositories(self):
        def fake_get(url):
            if '/repos?' in url:
                return [{'name': 'repo' + str(i), 'owner': {'login': 'example'}} for i in range(20)], None
            if '/orgs?' in url:
                return [{'login': 'org' + str(i)} for i in range(20)], None
            if 'api.github.com' in url:
                return {'type': 'User', 'login': 'example'}, None
            if 'wikidata.org' in url:
                return {'search': [{'id': 'Q1', 'label': 'Example'}]}, None
            self.fail('unexpected URL: ' + url)
        with mock.patch.object(people, 'get_json', side_effect=fake_get):
            result = people.search_people('example', 'Example', ['github', 'wikidata'])
        visible = result['graph']['nodes'][:35]
        self.assertTrue(any(node.get('url') == 'https://www.wikidata.org/wiki/Q1' for node in visible))
        ids = {node['id'] for node in visible}
        self.assertTrue(any(edge['source'] == 'query:name' and edge['target'] in ids for edge in result['graph']['edges']))

    def test_bluesky_and_mastodon_require_exact_public_handles(self):
        def fake_get(url):
            if 'bsky.app' in url:
                return {'handle': 'example.bsky.social', 'displayName': 'Example', 'followersCount': 0}, None
            if 'mastodon.social' in url:
                return {'username': 'example', 'acct': 'example', 'display_name': 'Example'}, None
            self.fail('unexpected URL: ' + url)
        with mock.patch.object(people, 'get_json', side_effect=fake_get) as getter:
            result = people.search_people('example', '', ['bluesky', 'mastodon'])
        self.assertEqual(getter.call_count, 2)
        modules = {m['id']: m for m in result['modules']}
        self.assertEqual(modules['bluesky']['status'], 'ok')
        self.assertEqual(modules['mastodon']['status'], 'ok')
        self.assertEqual(modules['bluesky']['links'][0][1], 'https://bsky.app/profile/example.bsky.social')
        self.assertEqual(modules['mastodon']['links'][0][1], 'https://mastodon.social/@example')
        with mock.patch.object(people, 'get_json', return_value=({'username': 'example', 'acct': 'example@elsewhere.social'}, None)):
            result = people.search_people('example', '', ['mastodon'])
        self.assertEqual(next(m for m in result['modules'] if m['id'] == 'mastodon')['status'], 'none')

    def test_all_sources_are_bounded_and_context_stays_in_manual_links(self):
        with mock.patch.object(people, 'get_json', return_value=(None, None)) as getter, \
             mock.patch.object(people, 'check_platform', return_value=('unverified', people.UNCLEAR_RE, 'https://example.org/user')) as checker:
            result = people.search_people('example', 'Ada Lovelace', list(people.SOURCES),
                                          orcid='0000-0002-1825-0097', context='Research')
        self.assertEqual(getter.call_count, 14)
        self.assertEqual(checker.call_count, len(people.PLATFORMS))
        self.assertTrue(all('Research' not in call.args[0] for call in getter.call_args_list))
        self.assertIn('Research', result['manual_links'][0]['url'])
        self.assertEqual(len(result['modules']), 15 + len(people.PLATFORMS))

    def test_json_requests_ask_for_json_and_surface_rate_limits(self):
        response = {'status': 200, 'headers': {'content-encoding': ''}, 'truncated': False,
                    'body': b'{"name": "public"}', 'error': None}
        with mock.patch.object(people, 'resolve_public', return_value=['1.1.1.1']), \
             mock.patch.object(people, 'fetch', return_value=response) as fetch:
            data, error = people.get_json('https://pub.orcid.org/v3.0/0000-0002-1825-0097/person')
        self.assertEqual(data, {'name': 'public'})
        self.assertIsNone(error)
        self.assertEqual(fetch.call_args.kwargs['accept'], 'application/json')
        response['status'] = 429
        with mock.patch.object(people, 'resolve_public', return_value=['1.1.1.1']), \
             mock.patch.object(people, 'fetch', return_value=response):
            data, error = people.get_json('https://pub.orcid.org/v3.0/0000-0002-1825-0097/person')
        self.assertIsNone(data)
        self.assertIn('429', error)


class PlatformSearchTests(unittest.TestCase):
    @staticmethod
    def response(status=200, body=b'', content_type='text/html; charset=utf-8', **kwargs):
        return {'status': status, 'headers': {'content-type': content_type, **kwargs.get('headers', {})},
                'body': body, 'truncated': kwargs.get('truncated', False), 'error': kwargs.get('error')}

    @staticmethod
    def platform(ident):
        return next(platform for platform in people.PLATFORMS if platform[0] == ident)

    def check(self, ident, username, response):
        with mock.patch.object(people, 'resolve_public', return_value=['1.1.1.1']) as resolver, \
             mock.patch.object(people, 'fetch', return_value=response) as fetcher:
            result = people.check_platform(self.platform(ident), username)
        self.assertEqual(fetcher.call_count, 1)
        self.assertEqual(fetcher.call_args.kwargs['timeout'], people.PLATFORM_TIMEOUT)
        self.assertEqual(fetcher.call_args.kwargs['limit'], people.PLATFORM_BODY_LIMIT)
        self.assertEqual(fetcher.call_args.args[1], ['1.1.1.1'])
        self.assertEqual(resolver.call_count, 1)
        return result

    def test_catalogue_is_unique_and_has_safe_https_templates(self):
        from pathlib import Path
        from urllib.parse import urlsplit
        self.assertGreater(len(people.PLATFORMS), 400)
        self.assertEqual(len(people.PLATFORMS), people.MAX_PLATFORMS)
        self.assertEqual(len({p[0] for p in people.PLATFORMS}), len(people.PLATFORMS))
        self.assertEqual(len({p[2] for p in people.PLATFORMS}), len(people.PLATFORMS))
        hosts = {urlsplit(p[2].format(u='example', d='example')).hostname.removeprefix('www.').removeprefix('example.') for p in people.PLATFORMS}
        self.assertGreater(len(hosts), 400)
        for filename in ('people_enhancements.js', 'updates.html', 'README_WEB_COMMAND_CENTER.md'):
            self.assertIn(str(len(people.PLATFORMS)), Path(filename).read_text(encoding='utf-8'))
        for ident, title, template, probe in people.PLATFORMS:
            with self.subTest(platform=ident):
                self.assertRegex(ident, r'^[a-z0-9-]+$')
                self.assertTrue(title)
                self.assertTrue(probe == 'status' or probe.startswith(('missing:', 'found:')))
                for value in (template, people.PROFILE_URLS.get(ident, template),
                              people.API_PROBES.get(ident, (template, ()))[0]):
                    url = value.format(u='example', d='example')
                    parsed = urlsplit(url)
                    self.assertEqual(parsed.scheme, 'https')
                    self.assertIsNone(parsed.username)
                    self.assertIsNone(parsed.password)
                    people.parse_target(url)

    def test_platform_group_alone_is_valid_and_opt_in(self):
        with mock.patch.object(people, 'get_json') as getter, \
             mock.patch.object(people, 'check_platform', return_value=('unverified', people.UNCLEAR_RE, 'https://example.org/user')) as checker:
            result = people.search_people('example', '', ['platforms'])
        getter.assert_not_called()
        self.assertEqual(checker.call_count, len(people.PLATFORMS))
        modules = [m for m in result['modules'] if m['id'].startswith('platform_')]
        self.assertEqual(len(modules), len(people.PLATFORMS))
        self.assertTrue(all(m['status'] == 'unverified' for m in modules))
        self.assertEqual(result['modules'][-1]['id'], 'search_links')
        with mock.patch.object(people, 'get_json', return_value=(None, None)), \
             mock.patch.object(people, 'check_platform') as checker:
            people.search_people('example', '', ['github'])
        checker.assert_not_called()
        with self.assertRaises(ValueError):
            people.search_people('', 'Example Person', ['platforms'])

    def test_json_exact_match_and_public_link(self):
        reply = self.response(body=b'{"username":"Hikaru","email":"private@example.com"}', content_type='application/json')
        status, summary, url = self.check('chess', 'hikaru', reply)
        self.assertEqual((status, url), ('ok', 'https://www.chess.com/member/hikaru'))
        self.assertNotIn('private@example.com', summary)
        reply['body'] = b'{"username":"different"}'
        self.assertEqual(self.check('chess', 'hikaru', reply)[0], 'unverified')
        reply['body'] = b'{"username":"hikaru"}'
        reply['truncated'] = True
        self.assertEqual(self.check('chess', 'hikaru', reply)[0], 'unverified')
        reply['truncated'] = False
        reply['body'] = b'not json'
        self.assertEqual(self.check('chess', 'hikaru', reply)[0], 'unverified')

    def test_nested_api_fields_are_exact_and_empty_duolingo_is_not_found(self):
        codeforces = self.response(body=b'{"status":"OK","result":[{"handle":"Tourist"}]}', content_type='application/json')
        self.assertEqual(self.check('codeforces', 'tourist', codeforces)[0], 'ok')
        codeforces['body'] = b'{"status":"OK","result":[{"handle":"someoneelse"}]}'
        self.assertEqual(self.check('codeforces', 'tourist', codeforces)[0], 'unverified')
        discourse = self.response(body=b'{"user":{"username":"Example"}}', content_type='application/json')
        self.assertEqual(self.check('pythonforum', 'example', discourse)[0], 'ok')
        tetrio = self.response(body=b'{"success":true,"data":{"username":"osk"}}', content_type='application/json')
        self.assertEqual(self.check('tetrio', 'osk', tetrio)[0], 'ok')
        missing = self.response(body=b'{"users":[]}', content_type='application/json')
        self.assertEqual(self.check('duolingo', 'nobody', missing)[0], 'none')
        missing['body'] = b'{"users":null}'
        self.assertEqual(self.check('duolingo', 'nobody', missing)[0], 'unverified')

    def test_federated_lookup_does_not_confuse_remote_and_local_accounts(self):
        reply = self.response(body=b'{"username":"alice","acct":"alice@elsewhere.example"}', content_type='application/json')
        self.assertEqual(self.check('hachyderm', 'alice', reply)[0], 'unverified')
        reply['body'] = b'{"username":"alice","acct":"Alice"}'
        status, _, url = self.check('hachyderm', 'alice', reply)
        self.assertEqual(status, 'ok')
        self.assertEqual(url, 'https://hachyderm.io/@alice')

    def test_telegram_generic_contact_is_not_a_confirmed_profile(self):
        generic = self.response(body=b'<title>Telegram: Contact @nobody</title><div class="tgme_page_description">Contact</div>')
        self.assertEqual(self.check('telegram', 'nobody', generic)[0], 'unverified')
        public = self.response(body=b'<div class="tgme_page_title">Telegram News</div>')
        self.assertEqual(self.check('telegram', 'telegram', public)[0], 'ok')

    def test_generic_pages_redirects_blocks_and_missing_are_distinct(self):
        for status, body, expected in [
            (200, b'<html>Generic page</html>', 'unverified'),
            (200, b'<title>Just a moment...</title>', 'unverified'),
            (301, b'', 'unverified'), (302, b'', 'unverified'),
            (403, b'', 'error'), (429, b'', 'error'), (500, b'', 'error'),
            (404, b'', 'none'), (410, b'', 'none'),
        ]:
            with self.subTest(status=status, body=body):
                state, _, url = self.check('instagram', 'example', self.response(status=status, body=body))
                self.assertEqual(state, expected)
                self.assertEqual(url, 'https://www.instagram.com/example/')
        self.assertEqual(self.check('steam', 'example', self.response(body=b'The specified profile cannot be found'))[0], 'none')
        self.assertEqual(self.check('steam', 'example', self.response(body=b'<html>profile</html>'))[0], 'unverified')

    def test_invalid_subdomain_is_skipped_without_a_request(self):
        with mock.patch.object(people, 'resolve_public') as resolver, mock.patch.object(people, 'fetch') as fetcher:
            status, summary, url = people.check_platform(self.platform('blogger'), 'has_under')
        self.assertEqual((status, summary, url), ('disabled', people.SKIP_RE, ''))
        resolver.assert_not_called()
        fetcher.assert_not_called()
        for bad in ('../admin', 'person@example.com', 'foo/bar', ''):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                people.check_platform(self.platform('telegram'), bad)

    def test_dns_failures_and_mixed_addresses_do_not_become_found(self):
        with mock.patch.object(people, 'resolve_public', side_effect=ValueError('blocked')), \
             mock.patch.object(people, 'fetch') as fetcher:
            self.assertEqual(people.check_platform(self.platform('telegram'), 'example')[0], 'error')
        fetcher.assert_not_called()
        response = self.response(status=None, error='timeout')
        self.assertEqual(self.check('instagram', 'example', response)[0], 'error')

    def test_confirmed_profiles_appear_in_graph_and_reports(self):
        def fake_check(platform, username):
            return ('ok', people.FOUND_RE, 'https://t.me/example') if platform[0] == 'telegram' else ('unverified', people.UNCLEAR_RE, 'https://example.org/example')
        with mock.patch.object(people, 'check_platform', side_effect=fake_check):
            result = people.search_people('example', '', ['platforms'])
        telegram = next(m for m in result['modules'] if m['id'] == 'platform_telegram')
        self.assertEqual(telegram['status'], 'ok')
        self.assertEqual(telegram['links'], [('Open profile', 'https://t.me/example')])
        self.assertTrue(any(node.get('url') == 'https://t.me/example' for node in result['graph']['nodes']))
        self.assertEqual(sum(node['kind'] == 'profile' for node in result['graph']['nodes']), 1)


if __name__ == '__main__':
    unittest.main()

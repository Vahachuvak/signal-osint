"""Bounded searches of public account and encyclopaedia APIs."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
import re
from urllib.parse import quote, urlencode

from osint_engine import fetch, parse_target, resolve_public, safe_text

SOURCES = {'github', 'gitlab', 'hackernews', 'devto', 'wikipedia', 'stackoverflow', 'crossref', 'orcid'}
USERNAME_RE = re.compile(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,38}\Z')
SLUG_RE = re.compile(r'[A-Za-z0-9_.-]{1,100}\Z')
DOI_RE = re.compile(r'10\.[0-9]{4,9}/[-._;()/:+A-Z0-9]+\Z', re.I)


def normalize_orcid(value):
    if not isinstance(value, str):
        raise ValueError('Введите корректный ORCID.')
    value = value.strip()
    if not value:
        return ''
    if not re.fullmatch(r'(?:[0-9]{4}-){3}[0-9]{3}[0-9Xx]|[0-9]{15}[0-9Xx]', value):
        raise ValueError('ORCID должен состоять из 16 символов в формате 0000-0002-1825-0097.')
    digits = value.replace('-', '').upper()
    total = 0
    for digit in digits[:15]:
        total = (total + int(digit)) * 2
    check = (12 - total % 11) % 11
    if digits[-1] != ('X' if check == 10 else str(check)):
        raise ValueError('Контрольная цифра ORCID не совпадает.')
    return '-'.join(digits[i:i + 4] for i in range(0, 16, 4))


def validate(username, name, sources, orcid='', context=''):
    if not isinstance(username, str) or not isinstance(name, str) or not isinstance(context, str):
        raise ValueError('Введите ник, имя или ORCID.')
    username, name, context = username.strip(), name.strip(), ' '.join(context.split())
    if username.startswith('@'):
        username = username[1:]
    if username and not USERNAME_RE.fullmatch(username):
        raise ValueError('Имя пользователя: до 39 латинских букв, цифр, точек, дефисов или подчёркиваний; без URL и электронной почты.')
    if len(name) > 100 or (name and (not any(c.isalpha() for c in name) or any(not (c.isalpha() or c.isspace() or c in "-.'’") for c in name))):
        raise ValueError('Имя может содержать буквы, пробелы, дефис и апостроф, до 100 символов.')
    name = ' '.join(name.split())
    if len(context) > 80 or (context and any(not (c.isalnum() or c.isspace() or c in "-.'’") for c in context)):
        raise ValueError('Контекст может содержать буквы, цифры, пробелы, точки и дефисы, до 80 символов.')
    orcid = normalize_orcid(orcid)
    if not username and not name and not orcid:
        raise ValueError('Введите имя пользователя, имя человека или ORCID.')
    if not isinstance(sources, list) or not all(isinstance(s, str) and s in SOURCES for s in sources):
        raise ValueError('Выбраны неизвестные источники.')
    sources = set(sources)
    account_sources = {'github', 'gitlab', 'hackernews', 'devto'}
    if not ((username and sources.intersection(account_sources)) or (name and sources.intersection({'wikipedia', 'crossref'})) or ((username or name) and 'stackoverflow' in sources) or (orcid and 'orcid' in sources)):
        raise ValueError('Выберите хотя бы один источник, соответствующий введённым данным.')
    return username, name, sources, orcid, context


def get_json(url):
    """URLs are assembled from fixed services; redirects are never followed."""
    try:
        target = parse_target(url)
        response = fetch(target, resolve_public(target['host']), target['path'], limit=512 * 1024, accept='application/json')
        if response['error']:
            return None, 'Не удалось связаться с источником: ' + response['error']
        if response['status'] == 404:
            return None, None
        if response['status'] != 200:
            return None, 'Источник вернул HTTP ' + str(response['status']) + (' (возможно, достигнут лимит запросов)' if response['status'] in (403, 429) else '')
        if response['truncated']:
            return None, 'Ответ источника превышает допустимый размер.'
        if response['headers'].get('content-encoding', '').lower() not in ('', 'identity'):
            return None, 'Источник вернул неподдерживаемое сжатие.'
        return json.loads(response['body'].decode('utf-8')), None
    except (ValueError, OSError, UnicodeError, json.JSONDecodeError) as exc:
        return None, safe_text(exc, 220)


def card(id, title, status, summary, facts=(), links=(), items=()):
    return {'id': id, 'title': title, 'status': status, 'summary': safe_text(summary, 350),
            'facts': [{'label': safe_text(k, 90), 'value': safe_text(str(v), 400)} for k, v in facts if v is not None and v != ''],
            'links': list(links), 'items': list(items)}


def search_people(username='', name='', sources=None, orcid='', context=''):
    username, name, sources, orcid, context = validate(username, name, sources if sources is not None else [], orcid, context)
    q = quote(username, safe='')
    jobs = {}
    with ThreadPoolExecutor(max_workers=8) as pool:
        if username and 'github' in sources:
            jobs['github'] = pool.submit(get_json, 'https://api.github.com/users/' + q)
            jobs['repos'] = pool.submit(get_json, 'https://api.github.com/users/' + q + '/repos?' + urlencode({'per_page': 20, 'sort': 'updated', 'type': 'owner'}))
            jobs['orgs'] = pool.submit(get_json, 'https://api.github.com/users/' + q + '/orgs?' + urlencode({'per_page': 20}))
        if username and 'gitlab' in sources:
            jobs['gitlab'] = pool.submit(get_json, 'https://gitlab.com/api/v4/users?' + urlencode({'username': username}))
        if username and 'hackernews' in sources:
            jobs['hackernews'] = pool.submit(get_json, 'https://hacker-news.firebaseio.com/v0/user/' + q + '.json')
        if username and 'devto' in sources:
            jobs['devto'] = pool.submit(get_json, 'https://dev.to/api/users/by_username?' + urlencode({'url': username}))
        if name and 'wikipedia' in sources:
            params = urlencode({'action': 'query', 'list': 'search', 'srsearch': name, 'format': 'json', 'srlimit': 8, 'srprop': ''})
            for lang in ('ru', 'en'):
                jobs['wiki_' + lang] = pool.submit(get_json, f'https://{lang}.wikipedia.org/w/api.php?' + params)
        if (name or username) and 'stackoverflow' in sources:
            params = urlencode({'site': 'stackoverflow', 'inname': name or username, 'pagesize': 8})
            jobs['stackoverflow'] = pool.submit(get_json, 'https://api.stackexchange.com/2.3/users?' + params)
        if name and 'crossref' in sources:
            params = urlencode({'query.author': name, 'rows': 6, 'select': 'title,DOI,published'})
            jobs['crossref'] = pool.submit(get_json, 'https://api.crossref.org/works?' + params)
        if orcid and 'orcid' in sources:
            jobs['orcid'] = pool.submit(get_json, 'https://pub.orcid.org/v3.0/' + orcid + '/person')
        results = {key: job.result() for key, job in jobs.items()}
    modules = []
    graph = {'nodes': [{'id': 'query', 'label': 'Поисковый запрос', 'kind': 'query'}], 'edges': []}
    for kind, label in (('username', username), ('name', name), ('orcid', orcid)):
        if label:
            ident = 'query:' + kind
            graph['nodes'].append({'id': ident, 'label': safe_text(label, 100), 'kind': 'query'})
            graph['edges'].append({'source': 'query', 'target': ident})

    def add_node(kind, label, url='', parent='query:username'):
        ident = kind + ':' + label + ':' + url
        if not any(n['id'] == ident for n in graph['nodes']):
            graph['nodes'].append({'id': ident, 'kind': kind, 'label': safe_text(label, 100), 'url': url})
            graph['edges'].append({'source': parent, 'target': ident})
        return ident

    def disabled(id, title, needs):
        modules.append(card(id, title, 'disabled', needs))

    def failure(id, title, err):
        modules.append(card(id, title, 'error', 'Источник недоступен: ' + err))

    github_node = 'query:username'
    if 'github' not in jobs:
        disabled('github', 'GitHub · профиль', 'Выберите GitHub и введите имя пользователя.')
    else:
        data, err = results['github']
        if err:
            failure('github', 'GitHub · профиль', err)
        elif isinstance(data, dict) and data.get('type') == 'User' and str(data.get('login', '')).casefold() == username.casefold():
            login = data['login']
            url = 'https://github.com/' + quote(login, safe='')
            modules.append(card('github', 'GitHub · профиль', 'ok', 'Найден публичный профиль с точным именем пользователя. Личность необходимо подтвердить самостоятельно.',
                                [('Имя в профиле', data.get('name')), ('Логин', login), ('Организация', data.get('company')),
                                 ('Публичные репозитории', data.get('public_repos')), ('Подписчики', data.get('followers')),
                                 ('Подписки', data.get('following')), ('Создан', data.get('created_at'))], [('Открыть GitHub', url)]))
            github_node = add_node('profile', 'GitHub / ' + login, url)
        else:
            modules.append(card('github', 'GitHub · профиль', 'none', 'Профиль с точным именем не найден или недоступен.'))

    for key, title, path in [('repos', 'GitHub · репозитории', 'репозиториев'), ('orgs', 'GitHub · организации', 'организаций')]:
        if key not in jobs:
            disabled(key, title, 'Выберите GitHub и введите имя пользователя.')
            continue
        data, err = results[key]
        if err:
            failure(key, title, err)
        elif isinstance(data, list):
            items = []
            for entry in data[:20]:
                if not isinstance(entry, dict):
                    continue
                slug = str(entry.get('name' if key == 'repos' else 'login', ''))
                owner = str((entry.get('owner') or {}).get('login', '')) if key == 'repos' and isinstance(entry.get('owner'), dict) else ''
                if not SLUG_RE.fullmatch(slug) or (key == 'repos' and (not SLUG_RE.fullmatch(owner) or owner.casefold() != username.casefold())):
                    continue
                url = 'https://github.com/' + (quote(owner, safe='') + '/' if key == 'repos' else '') + quote(slug, safe='')
                detail = ('★ ' + str(entry.get('stargazers_count', 0)) + ' · ' + str(entry.get('language') or 'язык не указан')) if key == 'repos' else 'Публичная организация'
                items.append({'title': safe_text(slug, 100), 'url': url, 'detail': safe_text(detail, 120)})
                add_node('repo' if key == 'repos' else 'org', slug, url, github_node)
            modules.append(card(key, title, 'ok' if items else 'none', f'Показано {len(items)} публичных {path}; максимум 20. Список может быть неполным.', items=items))
        else:
            modules.append(card(key, title, 'none', 'Данные не найдены или профиль недоступен.'))

    if 'gitlab' not in jobs:
        disabled('gitlab', 'GitLab · профиль', 'Выберите GitLab и введите имя пользователя.')
    else:
        data, err = results['gitlab']
        match = next((x for x in data if isinstance(x, dict) and str(x.get('username', '')).casefold() == username.casefold()), None) if isinstance(data, list) else None
        if err:
            failure('gitlab', 'GitLab · профиль', err)
        elif match:
            url = 'https://gitlab.com/' + quote(match['username'], safe='')
            modules.append(card('gitlab', 'GitLab · профиль', 'ok', 'Найден публичный профиль с точным именем пользователя. Это не подтверждает совпадение личности с другими профилями.',
                                [('Имя в профиле', match.get('name')), ('Логин', match['username']), ('Статус', match.get('state')), ('Создан', match.get('created_at'))], [('Открыть GitLab', url)]))
            add_node('profile', 'GitLab / ' + match['username'], url)
        else:
            modules.append(card('gitlab', 'GitLab · профиль', 'none', 'Профиль с точным именем не найден или недоступен.'))

    if 'hackernews' not in jobs:
        disabled('hackernews', 'Hacker News · профиль', 'Выберите Hacker News и введите имя пользователя.')
    else:
        data, err = results['hackernews']
        if err:
            failure('hackernews', 'Hacker News · профиль', err)
        elif isinstance(data, dict) and str(data.get('id', '')).casefold() == username.casefold():
            url = 'https://news.ycombinator.com/user?' + urlencode({'id': data['id']})
            created = data.get('created')
            try:
                created = datetime.fromtimestamp(int(created), timezone.utc).date().isoformat() if created else None
            except (ValueError, OverflowError, OSError, TypeError):
                created = None
            modules.append(card('hackernews', 'Hacker News · профиль', 'ok', 'Найден публичный профиль с точным именем пользователя.',
                                [('Логин', data['id']), ('Карма', data.get('karma')), ('Создан', created)], [('Открыть Hacker News', url)]))
            add_node('profile', 'Hacker News / ' + data['id'], url)
        else:
            modules.append(card('hackernews', 'Hacker News · профиль', 'none', 'Профиль с точным именем не найден или недоступен.'))

    if 'devto' not in jobs:
        disabled('devto', 'DEV Community · профиль', 'Выберите DEV Community и введите имя пользователя.')
    else:
        data, err = results['devto']
        if err:
            failure('devto', 'DEV Community · профиль', err)
        elif isinstance(data, dict) and str(data.get('username', '')).casefold() == username.casefold():
            login = data['username']
            url = 'https://dev.to/' + quote(login, safe='')
            modules.append(card('devto', 'DEV Community · профиль', 'ok', 'Найден публичный профиль с точным именем пользователя.',
                                [('Имя в профиле', data.get('name')), ('Логин', login)], [('Открыть DEV', url)]))
            add_node('profile', 'DEV / ' + login, url)
        else:
            modules.append(card('devto', 'DEV Community · профиль', 'none', 'Профиль с точным именем не найден или недоступен.'))

    for lang, title in [('ru', 'Википедия · русский'), ('en', 'Wikipedia · English')]:
        key = 'wiki_' + lang
        if key not in jobs:
            disabled(key, title, 'Выберите Википедию и введите имя человека.')
            continue
        data, err = results[key]
        if err:
            failure(key, title, err)
            continue
        if not isinstance(data, dict) or not isinstance(data.get('query'), dict) or not isinstance(data['query'].get('search'), list):
            modules.append(card(key, title, 'error', 'Источник вернул неожиданный формат ответа.'))
            continue
        items = []
        for item in data['query']['search'][:8]:
            if isinstance(item, dict) and isinstance(item.get('pageid'), int) and isinstance(item.get('title'), str):
                url = f'https://{lang}.wikipedia.org/?curid={item["pageid"]}'
                items.append({'title': safe_text(item['title'], 150), 'url': url, 'detail': 'Результат поиска по имени, не подтверждение личности'})
                add_node('article', item['title'], url, 'query:name')
        modules.append(card(key, title, 'ok' if items else 'none', f'Найдено статей: {len(items)}. Тезки и нерелевантные совпадения возможны.', items=items))

    if 'stackoverflow' not in jobs:
        disabled('stackoverflow', 'Stack Overflow · поиск профилей', 'Выберите Stack Overflow и введите имя или ник.')
    else:
        data, err = results['stackoverflow']
        if err:
            failure('stackoverflow', 'Stack Overflow · поиск профилей', err)
        elif not isinstance(data, dict) or not isinstance(data.get('items'), list):
            modules.append(card('stackoverflow', 'Stack Overflow · поиск профилей', 'error', 'Источник вернул неожиданный формат ответа.'))
        else:
            items = []
            for item in data['items'][:8]:
                if isinstance(item, dict) and isinstance(item.get('user_id'), int) and isinstance(item.get('display_name'), str):
                    url = 'https://stackoverflow.com/users/' + str(item['user_id'])
                    label = safe_text(item['display_name'], 150)
                    items.append({'title': label, 'url': url, 'detail': 'Репутация: ' + safe_text(str(item.get('reputation', '—')), 40) + ' · совпадение имени не подтверждено'})
                    add_node('profile', 'Stack Overflow / ' + label, url, 'query:name' if name else 'query:username')
            modules.append(card('stackoverflow', 'Stack Overflow · поиск профилей', 'ok' if items else 'none', f'Результатов по отображаемому имени: {len(items)}. Это поиск, а не точная идентификация.', items=items))

    if 'crossref' not in jobs:
        disabled('crossref', 'Crossref · публикации', 'Выберите Crossref и введите имя человека.')
    else:
        data, err = results['crossref']
        message = data.get('message') if isinstance(data, dict) else None
        if err:
            failure('crossref', 'Crossref · публикации', err)
        elif not isinstance(message, dict) or not isinstance(message.get('items'), list):
            modules.append(card('crossref', 'Crossref · публикации', 'error', 'Источник вернул неожиданный формат ответа.'))
        else:
            items = []
            for item in message['items'][:6]:
                if not isinstance(item, dict):
                    continue
                doi = item.get('DOI', '')
                title = item.get('title')
                if not isinstance(doi, str) or not DOI_RE.fullmatch(doi) or not isinstance(title, list) or not title or not isinstance(title[0], str):
                    continue
                url = 'https://doi.org/' + quote(doi, safe='/.:;()_-')
                label = safe_text(title[0], 150)
                items.append({'title': label, 'url': url, 'detail': 'DOI: ' + safe_text(doi, 140) + ' · авторство по совпадению имени не подтверждено'})
                add_node('article', label, url, 'query:name')
            modules.append(card('crossref', 'Crossref · публикации', 'ok' if items else 'none', f'Результатов по имени автора: {len(items)}. Возможны нерелевантные совпадения.', items=items))

    if 'orcid' not in jobs:
        disabled('orcid', 'ORCID · исследователь', 'Выберите ORCID и введите публичный ORCID iD.')
    else:
        data, err = results['orcid']
        if err:
            failure('orcid', 'ORCID · исследователь', err)
        elif data is None:
            modules.append(card('orcid', 'ORCID · исследователь', 'none', 'Публичная запись не найдена или недоступна.'))
        elif not isinstance(data, dict):
            modules.append(card('orcid', 'ORCID · исследователь', 'error', 'Источник вернул неожиданный формат ответа.'))
        else:
            person = data.get('name') if isinstance(data.get('name'), dict) else {}
            def field(key):
                entry = person.get(key)
                return entry.get('value') if isinstance(entry, dict) else None
            url = 'https://orcid.org/' + orcid
            modules.append(card('orcid', 'ORCID · исследователь', 'ok', 'Публичная запись по указанному ORCID. Это не подтверждает совпадение с другими результатами.',
                                [('ORCID', orcid), ('Имя', field('given-names')), ('Фамилия', field('family-name')), ('Имя для публикаций', field('credit-name'))], [('Открыть ORCID', url)]))
            add_node('profile', 'ORCID / ' + orcid, url, 'query:orcid')

    manual = []
    for query, tag in ((username, 'ник'), (name, 'имя')):
        if not query:
            continue
        contextual_query = '"' + query + '"' + (' ' + context if context else '')
        manual.extend([
            ('Google · ' + tag, 'https://www.google.com/search?' + urlencode({'q': contextual_query})),
            ('Bing · ' + tag, 'https://www.bing.com/search?' + urlencode({'q': contextual_query})),
            ('DuckDuckGo · ' + tag, 'https://duckduckgo.com/?' + urlencode({'q': contextual_query})),
            ('YouTube · ' + tag, 'https://www.youtube.com/results?' + urlencode({'search_query': query})),
            ('GitHub поиск · ' + tag, 'https://github.com/search?' + urlencode({'q': query, 'type': 'users'})),
            ('Википедия · ' + tag, 'https://ru.wikipedia.org/w/index.php?' + urlencode({'search': query})),
            ('Google Scholar · ' + tag, 'https://scholar.google.com/scholar?' + urlencode({'q': query})),
            ('Reddit · ' + tag, 'https://www.reddit.com/search/?' + urlencode({'q': query})),
            ('GitLab поиск · ' + tag, 'https://gitlab.com/search?' + urlencode({'search': query})),
            ('DEV поиск · ' + tag, 'https://dev.to/search?' + urlencode({'q': query})),
            ('LinkedIn · ' + tag + ' (может потребоваться вход)', 'https://www.linkedin.com/search/results/people/?' + urlencode({'keywords': query})),
            ('ORCID поиск · ' + tag, 'https://orcid.org/orcid-search/search?' + urlencode({'searchQuery': query})),
            ('Crossref поиск · ' + tag, 'https://search.crossref.org/?' + urlencode({'q': query})),
            ('Stack Overflow поиск · ' + tag, 'https://stackoverflow.com/search?' + urlencode({'q': query})),
            ('Internet Archive · ' + tag, 'https://archive.org/search?' + urlencode({'query': query})),
        ])
    if orcid:
        manual.append(('Указанный ORCID', 'https://orcid.org/' + orcid))
    modules.append(card('search_links', 'Поисковые ссылки', 'ready', f'Подготовлено ссылок: {len(manual)}. Поисковые системы не опрашивались; результаты нужно открыть и проверить самостоятельно.'))
    return {'version': 1, 'username': username, 'name': name, 'orcid': orcid, 'context': context, 'scanned_at': datetime.now(timezone.utc).isoformat(),
            'sources': sorted(sources), 'modules': modules, 'graph': graph,
            'manual_links': [{'label': label, 'url': url} for label, url in manual],
            'notice': 'Совпадение имени пользователя или имени не подтверждает личность. Источники могут быть неполными или недоступными.'}

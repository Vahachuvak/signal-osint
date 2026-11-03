/* UI-only translation. Search data, saved reports, URLs and exports are not modified. */
(function () {
  'use strict';

  const ru = {
    'Main navigation': 'Основная навигация', 'Navigation': 'Навигация', 'Workspaces': 'Разделы', 'Signal home': 'Signal — на главную',
    'PEOPLE': 'ЛЮДИ', 'SITES': 'САЙТЫ', 'MEDIA': 'МЕДИА', 'UPDATES': 'ОБНОВЛЕНИЯ',
    'People': 'Люди', 'Media': 'Медиа', 'Updates': 'Обновления', 'LOG': 'ЛОГ',
    '01 / PEOPLE': '01 / ЛЮДИ', '02 / SITES': '02 / САЙТЫ', '03 / MEDIA': '03 / МЕДИА', '04 / UPDATES': '04 / ОБНОВЛЕНИЯ',
    'Public profiles and articles': 'Публичные профили и статьи', 'Domains and connections': 'Домены и связи',
    'Follow and support Signal': 'Подписка и поддержка', "What's new in Signal": 'Что нового в Signal',
    'WORKSPACE / PEOPLE INTELLIGENCE': 'РАБОЧЕЕ ПРОСТРАНСТВО / ПОИСК ЛЮДЕЙ', 'PUBLIC SOURCES ONLY': 'ТОЛЬКО ОТКРЫТЫЕ ИСТОЧНИКИ',
    'OPEN SOURCE INTELLIGENCE': 'РАЗВЕДКА ПО ОТКРЫТЫМ ИСТОЧНИКАМ', 'WEB INTELLIGENCE': 'ИССЛЕДОВАНИЕ САЙТОВ',
    'Find the signal.': 'Найти сигнал.', 'Follow the connections.': 'Увидеть связи.',
    'Explore public profiles and articles. Follow the evidence, verify the source, and never assume a match is an identity.': 'Изучайте публичные профили и статьи. Проверяйте источники и не принимайте совпадение за подтверждение личности.',
    'SIGNAL / 01 ─ PEOPLE': 'SIGNAL / 01 ─ ЛЮДИ', '01 / SEARCH PARAMETERS': '01 / ПАРАМЕТРЫ ПОИСКА',
    'Enter a username, name, or both': 'Введите ник, имя или оба значения', 'Username, name, profile URL, or ORCID iD': 'Ник, имя, ссылка на профиль или ORCID iD',
    'QUERY': 'ЗАПРОС', 'USERNAME': 'ИМЯ ПОЛЬЗОВАТЕЛЯ', 'FULL NAME': 'ИМЯ И ФАМИЛИЯ', 'PUBLIC PROFILE URL': 'ССЫЛКА НА ПУБЛИЧНЫЙ ПРОФИЛЬ',
    'e.g. octocat': 'например, octocat', 'e.g. Ada Lovelace': 'например, Ада Лавлейс', 'e.g. university': 'например, университет',
    'No links or email addresses.': 'Без ссылок и адресов электронной почты.', 'Used for public name searches.': 'Используется для поиска по имени в открытых источниках.',
    'Used for Wikipedia, Wikidata, Stack Overflow, Crossref, and manual searches.': 'Используется для Википедии, Wikidata, Stack Overflow, Crossref и ручного поиска.',
    'Extracts a username from a supported public profile. The URL itself is not visited.': 'Извлекает ник из поддерживаемой ссылки на профиль. Сама ссылка не посещается.',
    'Extracts a username from GitHub, GitLab, DEV, Hacker News, Bluesky, or Mastodon.social. The link is not visited.': 'Извлекает ник из GitHub, GitLab, DEV, Hacker News, Bluesky или Mastodon.social. Сама ссылка не посещается.',
    'EXTRACT USERNAME': 'ИЗВЛЕЧЬ НИК', 'Public researcher identifier, not a phone number.': 'Публичный идентификатор исследователя, не номер телефона.',
    'CONTEXT FOR MANUAL SEARCH': 'КОНТЕКСТ ДЛЯ РУЧНОГО ПОИСКА',
    'Added to Google, Bing, and DuckDuckGo links; does not verify identity.': 'Добавляется к ссылкам Google, Bing и DuckDuckGo; не подтверждает личность.',
    'SOURCES': 'ИСТОЧНИКИ', 'Source selection': 'Выбор источников', 'All': 'Все', 'Profiles': 'Профили', 'Research': 'Исследования', 'Clear': 'Очистить', 'Wikipedia': 'Википедия',
    'Save history in this browser': 'Сохранять историю в этом браузере',
    'Selected sources receive the username, name, or ORCID. History is off by default. Do not enter addresses, phone numbers, passwords, or tokens in search fields.': 'Выбранные источники получат введённый ник, имя или ORCID. История по умолчанию отключена. Не вводите адреса, телефоны, пароли или токены в поля поиска.',
    'Selected sources receive your username or name. History is off by default. Do not enter addresses, phone numbers, passwords, or tokens.': 'Выбранные источники получат ник или имя. История по умолчанию отключена. Не вводите адреса, телефоны, пароли или токены.',
    'START SEARCH': 'НАЧАТЬ ПОИСК', 'SEARCHING...': 'ПОИСК...', '02 / PHONE FORMAT': '02 / ФОРМАТ ТЕЛЕФОНА',
    'Checked only in this browser. The number is not sent to the server, and this does not find an owner or verify the number exists.': 'Проверка выполняется только в браузере. Номер не отправляется на сервер; проверка не ищет владельца и не подтверждает существование номера.',
    'INTERNATIONAL FORMAT': 'МЕЖДУНАРОДНЫЙ ФОРМАТ', '+ and country code': '+ и код страны', 'CHECK FORMAT': 'ПРОВЕРИТЬ ФОРМАТ', 'CLEAR': 'ОЧИСТИТЬ',
    'Enter an international number beginning with +. Spaces, parentheses, and hyphens are allowed.': 'Введите международный номер начиная с +. Допускаются пробелы, скобки и дефисы.',
    'Invalid format: use 7 to 15 digits after +, starting with a non-zero digit.': 'Неверный формат: после + укажите от 7 до 15 цифр, первая не может быть нулём.',
    'The basic format check passed. The number, carrier, and owner are not verified.': 'Упрощённая проверка формата пройдена. Сам номер, оператор и владелец не проверены.',
    'MODULES': 'МОДУЛИ', 'MATCHES': 'СОВПАДЕНИЯ', 'FOUND IN': 'НАЙДЕНО В', 'ERRORS': 'ОШИБКИ',
    'name / username': 'имя / ник', 'username / name / ORCID': 'ник / имя / ORCID', 'sources and sections': 'источники и разделы',
    'not identity verification': 'не подтверждение личности', 'modules; not identification': 'модулях; не идентификация', 'unavailable sources': 'недоступные источники',
    'RESULTS': 'РЕЗУЛЬТАТЫ', 'RELATIONSHIP GRAPH': 'ГРАФ СВЯЗЕЙ', 'SEARCH LINKS': 'ПОИСКОВЫЕ ССЫЛКИ', 'HISTORY': 'ИСТОРИЯ',
    '[ VIEW DETAILS ]': '[ ПОКАЗАТЬ ПОДРОБНОСТИ ]',
    'Waiting for a search': 'Ожидание запроса', 'Filter results...': 'Фильтр результатов...', 'Filter results': 'Фильтр результатов',
    'Status': 'Статус', 'All statuses': 'Все статусы', 'Found': 'Найдено', 'No data': 'Нет данных', 'Error': 'Ошибка', 'Disabled': 'Отключено', 'Ready': 'Готово',
    'FOUND': 'НАЙДЕНО', 'NO DATA': 'НЕТ ДАННЫХ', 'ERROR': 'ОШИБКА', 'DISABLED': 'ОТКЛЮЧЕНО', 'READY': 'ГОТОВО',
    '[ AWAITING DATA ]': '[ ОЖИДАНИЕ ДАННЫХ ]', 'Enter a username or a name.': 'Введите имя пользователя или имя человека.',
    'Results will appear here after your search.': 'Результаты появятся здесь после поиска.', 'No results match the filter.': 'По фильтру ничего не найдено.',
    'No results match this status and text filter.': 'По выбранному статусу и текстовому фильтру ничего не найдено.',
    'The query is connected to results, not a verified identity.': 'Запрос связан с результатами, а не с подтверждённой личностью.',
    'Zoom in': 'Увеличить', 'Zoom out': 'Уменьшить', 'RESET': 'СБРОС', 'Reset': 'Сбросить',
    'Public source graph': 'Граф открытых источников', 'GRAPH IS EMPTY': 'ГРАФ ПОКА ПУСТ',
    'Select a node to view its source. Up to 35 nodes are shown.': 'Выберите узел для просмотра источника. Показано до 35 узлов.',
    'Drag nodes and select them to view their source. Up to 35 nodes are shown.': 'Перетаскивайте узлы и выбирайте их для просмотра источника. Показано до 35 узлов.',
    'OPEN SOURCE': 'ОТКРЫТЬ ИСТОЧНИК', 'Search query': 'Поисковый запрос', 'search query': 'поисковый запрос', 'profile': 'профиль', 'repository': 'репозиторий', 'organization': 'организация', 'article': 'статья',
    'Open these links to verify results yourself. Services open only when selected.': 'Откройте ссылки для самостоятельной проверки. Сервисы открываются только по вашему нажатию.',
    'Search links will appear after a search.': 'Поисковые ссылки появятся после поиска.',
    'The query is sent to the service only when you open the link.': 'Запрос отправляется сервису только при открытии ссылки.',
    'History stays in this browser when saving is enabled.': 'История хранится только в этом браузере, если сохранение включено.',
    'CLEAR HISTORY': 'ОЧИСТИТЬ ИСТОРИЮ', 'History is empty. Enable saving before searching if you need it.': 'История пуста. При необходимости включите сохранение перед поиском.',
    'COMPARE': 'СРАВНИТЬ', 'COMPARE SEARCHES': 'СРАВНЕНИЕ ПОИСКОВ', 'No changes found in available data.': 'Изменений в доступных данных не найдено.',
    '[ IMPORTANT ] Matching names or usernames do not prove profiles belong to the same person. Verify sources independently and use this tool responsibly and lawfully.': '[ ВАЖНО ] Совпадение имени или ника не доказывает, что профили принадлежат одному человеку. Проверяйте источники самостоятельно и используйте инструмент ответственно и законно.',
    'EXPORT JSON': 'ЭКСПОРТ JSON', 'EXPORT MARKDOWN': 'ЭКСПОРТ MARKDOWN', 'AWAITING SEARCH': 'ОЖИДАНИЕ ПОИСКА',
    'Public data · bounded requests': 'Открытые данные · ограниченное число запросов', 'OPEN SITE INVESTIGATION': 'ПЕРЕЙТИ К ИССЛЕДОВАНИЮ САЙТОВ',
    'This is not identity verification or an exhaustive search.': 'Это не проверка личности и не исчерпывающий поиск.', 'OPEN': 'ОТКРЫТЬ',

    'WORKSPACE': 'РАБОЧЕЕ ПРОСТРАНСТВО', 'SIGNAL / WORKSPACE': 'SIGNAL / РАБОЧЕЕ ПРОСТРАНСТВО', 'SIGNAL / PEOPLE INTELLIGENCE': 'SIGNAL / ПОИСК ЛЮДЕЙ', 'INFORMATION': 'ИНФОРМАЦИЯ', 'People search': 'Поиск людей', 'Website overview': 'Обзор сайтов',
    'Search modules': 'Модули поиска', 'Relationship graph': 'Граф связей', 'History and reports': 'История и отчёты', 'Media & support': 'Медиа и поддержка',
    'About': 'О платформе', 'Browser history': 'История в браузере', 'Results are saved in this browser. External sources are enabled separately.': 'Результаты сохраняются в этом браузере. Внешние источники включаются отдельно.',
    'OVERVIEW': 'ОБЗОР', 'SEARCH MODULES': 'МОДУЛИ ПОИСКА', 'HISTORY AND REPORTS': 'ИСТОРИЯ И ОТЧЁТЫ', 'ABOUT': 'О ПЛАТФОРМЕ',
    'Home': 'На главную', '← Home': '← На главную', 'Web platform': 'Веб-платформа', 'PASSIVE OSINT': 'ПАССИВНЫЙ OSINT',
    'WEB INTELLIGENCE WORKSPACE': 'РАБОЧЕЕ ПРОСТРАНСТВО / САЙТЫ', 'See beyond the surface.': 'Смотрите глубже.',
    'Public data, connections, and a website’s technical profile in one workspace.': 'Публичные данные, связи и технический профиль сайта в одном пространстве.',
    'New investigation': 'Новое исследование', 'HTTP(S) · public domains and IPs': 'HTTP(S) · публичные домены и IP',
    'Enter a domain or address, e.g. example.com': 'Введите домен или адрес, например example.com', 'Start investigation': 'НАЧАТЬ ИССЛЕДОВАНИЕ',
    'crt.sh · certificates': 'crt.sh · сертификаты', 'RDAP · registration': 'RDAP · регистрация', 'Wayback · archive': 'Wayback · архив',
    'Optional: the domain is sent to the selected external services': 'Опционально: домен передаётся выбранным внешним сервисам',
    'The site returned a redirect. Automatic redirects are disabled. New address without parameters:': 'Сайт вернул перенаправление. Автоматический переход отключён. Новый адрес без параметров:',
    'Investigate this address': 'Исследовать этот адрес', 'ACTIVE TARGET': 'АКТИВНАЯ ЦЕЛЬ', 'Target domain': 'Домен исследования', 'HTTP STATUS': 'HTTP-СТАТУС',
    'Awaiting investigation': 'Ожидание исследования', 'IP ADDRESSES': 'IP-АДРЕСА', 'System DNS responses': 'Ответы системного DNS', 'Passive sources and analysis': 'Пассивные источники и анализ',
    'Investigation coverage': 'Покрытие исследования', 'Module status for the current target': 'Состояние модулей текущей цели', 'waiting': 'ожидание', 'complete': 'завершено',
    'Module results': 'Результаты модулей', 'Latest investigation': 'Последнее исследование', 'All modules': 'Все модули',
    'Nothing here yet': 'Пока здесь пусто', 'Enter a domain above to collect your first results.': 'Введите домен выше, чтобы собрать первые данные.',
    'Each module shows its source and the limits of its results.': 'Каждый модуль показывает источник и ограничения результата.', 'Search modules...': 'Поиск по модулям...',
    'Warning': 'Внимание', 'Errors': 'Ошибки', 'Information': 'Информация',
    'Select a node for details. Drag nodes and zoom the graph.': 'Выберите узел для подробностей. Перетаскивайте узлы и меняйте масштаб.', 'Download SVG': 'Скачать SVG',
    'Up to 20 investigations in local browser storage. Compare results for the same target.': 'До 20 исследований в хранилище браузера. Сравнивайте результаты одной цели.',
    'Export JSON': 'Экспорт JSON', 'Export Markdown': 'Экспорт Markdown', 'Clear history': 'Очистить историю', 'Transparency about sources and the limits of analysis.': 'Информация об источниках и ограничениях анализа.',
    'What is analyzed': 'Что анализируется', 'External sources': 'Внешние источники', 'What Signal does not do': 'Чего Signal не делает', 'Privacy': 'Конфиденциальность',
    'System DNS, HTTP response, TLS certificate, requested page HTML, and three public files: robots.txt, sitemap.xml, and security.txt. At most four GET requests are made to the site; redirects and discovered links are not followed.': 'Системный DNS, HTTP-ответ, TLS-сертификат, HTML страницы и три публичных файла: robots.txt, sitemap.xml и security.txt. К сайту выполняется не более четырёх GET-запросов; переходы и найденные ссылки не открываются.',
    'crt.sh, RDAP, and Internet Archive are enabled separately. The domain is sent to selected services; RDAP may redirect the request to the appropriate registry. Results may be incomplete or outdated.': 'crt.sh, RDAP и Internet Archive включаются отдельно. Домен передаётся выбранным сервисам; RDAP может перенаправить запрос в реестр. Результаты могут быть неполными или устаревшими.',
    'Signal does not exploit vulnerabilities, test SQL injection, guess passwords, submit forms, or crawl websites. A lack of findings does not mean a site is secure.': 'Signal не эксплуатирует уязвимости, не проверяет SQL-инъекции, не подбирает пароли, не отправляет формы и не обходит сайты. Отсутствие находок не означает безопасность сайта.',
    'History stays in this browser. Cookie and form field values are not collected, and URL parameters are removed from reports. The site may reflect parameters elsewhere; do not enter secrets.': 'История хранится в этом браузере. Значения cookies и полей форм не собираются, параметры URL удаляются из отчётов. Сайт может отразить параметры в других данных; не вводите секреты.',
    'Passive intelligence.': 'Пассивная разведка.', 'Investigate only websites you have permission to examine. Data can be incomplete; results are not a security audit.': 'Исследуйте только сайты, для которых у вас есть разрешение. Данные могут быть неполными; результаты не являются аудитом безопасности.',
    'Visual map of discovered connections · up to 60 nodes': 'Карта обнаруженных связей · до 60 узлов', 'Website relationship graph': 'Граф связей сайта', 'RELATIONSHIP MAP': 'КАРТА СВЯЗЕЙ', 'NETWORK / 01': 'СЕТЬ / 01',
    'Scroll to zoom · drag to move nodes': 'Прокрутка — масштаб · перетаскивание — перемещение узла', 'Domain': 'Домен', 'Certificate': 'Сертификат', 'Resource / link': 'Ресурс / ссылка',
    'Select a node': 'Выберите узел', 'The map is empty': 'Карта пока пуста', 'Run an investigation to see connections': 'Запустите исследование, чтобы увидеть связи',
    'Optional search via crt.sh.': 'Дополнительный поиск через crt.sh.', 'Results appear after an investigation.': 'Результаты появятся после исследования.', 'Details': 'Подробности',
    'No additional data.': 'Дополнительных данных нет.', 'No results match this filter.': 'По выбранному фильтру ничего не найдено.',
    'History is empty': 'История пуста', 'Completed investigations appear here.': 'Завершённые исследования появятся здесь.', 'Compare': 'Сравнить', 'Open': 'Открыть',
    'Before:': 'Было:', 'After:': 'Стало:', 'Showing the first 50 changes.': 'Показаны первые 50 изменений.', 'No differences found in the available data.': 'Различий в доступных данных не найдено.',

    /* Labels and explanations generated by the people and site engines. */
    'GitHub · profile': 'GitHub · профиль', 'GitHub · repositories': 'GitHub · репозитории', 'GitHub · organizations': 'GitHub · организации',
    'GitLab · profile': 'GitLab · профиль', 'Hacker News · profile': 'Hacker News · профиль', 'DEV Community · profile': 'DEV Community · профиль',
    'Bluesky · profile': 'Bluesky · профиль', 'Mastodon.social · profile': 'Mastodon.social · профиль', 'Wikipedia · Russian': 'Википедия · русский', 'Wikipedia · English': 'Википедия · английский',
    'Wikidata · entity search': 'Wikidata · поиск записей', 'Stack Overflow · profile search': 'Stack Overflow · поиск профилей', 'Crossref · publications': 'Crossref · публикации', 'ORCID · researcher': 'ORCID · исследователь', 'Search links': 'Поисковые ссылки',
    'Select GitHub and enter a username.': 'Выберите GitHub и введите ник.', 'Select GitLab and enter a username.': 'Выберите GitLab и введите ник.',
    'Select Hacker News and enter a username.': 'Выберите Hacker News и введите ник.', 'Select DEV Community and enter a username.': 'Выберите DEV Community и введите ник.',
    'Enter a compatible Bluesky handle or username and select Bluesky. A plain username is checked as username.bsky.social.': 'Выберите Bluesky и введите совместимый ник или handle. Обычный ник проверяется как username.bsky.social.',
    'Select Mastodon.social and enter a username. Other Mastodon servers are not checked.': 'Выберите Mastodon.social и введите ник. Другие серверы Mastodon не проверяются.',
    'Select Wikipedia and enter a name.': 'Выберите Википедию и введите имя.', 'Select Wikidata and enter a name.': 'Выберите Wikidata и введите имя.',
    'Select Stack Overflow and enter a name or username.': 'Выберите Stack Overflow и введите имя или ник.', 'Select Crossref and enter a name.': 'Выберите Crossref и введите имя.', 'Select ORCID and enter a public ORCID iD.': 'Выберите ORCID и введите публичный ORCID iD.',
    'A public profile with this exact username was found. Verify its identity independently.': 'Найден публичный профиль с точно таким ником. Проверьте личность самостоятельно.',
    'A public profile with this exact username was found.': 'Найден публичный профиль с точно таким ником.',
    'No accessible public profile with this exact username was found.': 'Доступный публичный профиль с точно таким ником не найден.',
    'An exact public username was found. This does not establish a match with other profiles.': 'Найден точный публичный ник. Это не подтверждает совпадение с другими профилями.',
    'An exact public Bluesky handle was found; verify the identity independently.': 'Найден точный публичный handle Bluesky; проверьте личность самостоятельно.',
    'A public profile with this exact username was found on mastodon.social only.': 'Найден публичный профиль с таким ником только на mastodon.social.',
    'No public profile was found on mastodon.social. Other servers were not checked.': 'Публичный профиль на mastodon.social не найден. Другие серверы не проверялись.',
    'No data found or the profile is unavailable.': 'Данные не найдены или профиль недоступен.', 'The source returned an unexpected response.': 'Источник вернул ответ неожиданного формата.',
    'Name search result; identity is not confirmed.': 'Результат поиска по имени; личность не подтверждена.', 'Search result; identity is not confirmed.': 'Результат поиска; личность не подтверждена.',
    'No accessible public record was found.': 'Доступная публичная запись не найдена.', 'Public record for the supplied ORCID. This does not confirm a match with other results.': 'Публичная запись по указанному ORCID. Она не подтверждает совпадение с другими результатами.',
    'Display name': 'Отображаемое имя', 'Username': 'Ник', 'Company': 'Компания', 'Public repositories': 'Публичные репозитории', 'Followers': 'Подписчики',
    'Following': 'Подписки', 'Created': 'Создан', 'Handle': 'Handle', 'Given name': 'Имя', 'Family name': 'Фамилия', 'Credit name': 'Имя для публикаций',
    'Public organization': 'Публичная организация', 'language not specified': 'язык не указан', 'Open GitHub': 'Открыть GitHub', 'Open GitLab': 'Открыть GitLab',
    'Open Hacker News': 'Открыть Hacker News', 'Open DEV': 'Открыть DEV', 'Open Bluesky': 'Открыть Bluesky', 'Open Mastodon': 'Открыть Mastodon', 'Open ORCID': 'Открыть ORCID',
    'DNS and addresses': 'DNS и адреса', 'HTTP response': 'HTTP-ответ', 'TLS certificate': 'TLS-сертификат', 'Security headers': 'Защитные заголовки', 'Cookie settings': 'Настройки cookies',
    'Technologies and server': 'Технологии и сервер', 'Page metadata': 'Метаданные страницы', 'Links and external domains': 'Ссылки и внешние домены', 'Contacts and social links': 'Контакты и соцсети',
    'Forms and fields': 'Формы и поля', 'External resources': 'Внешние ресурсы', 'Indexing': 'Индексация', 'Database errors': 'Ошибки базы данных', 'Basic accessibility indicators': 'Базовые признаки доступности',
    'Domain registration · RDAP': 'Регистрация домена · RDAP', 'Website archive · Wayback': 'Архив сайта · Wayback', 'URL without parameters': 'URL без параметров',
    'Redirect (not followed)': 'Перенаправление (не переходили)', 'Bytes read': 'Прочитано байт', 'Protocol': 'Протокол', 'Issuer': 'Издатель', 'Expires': 'Действует до', 'Certificate names': 'Имена в сертификате',
    'Language': 'Язык', 'External link': 'Внешняя ссылка', 'Internal links': 'Внутренние ссылки', 'Platform': 'Платформа', 'Entry': 'Запись', 'Signature': 'Сигнатура',
    'HTML language': 'Язык HTML', 'Images without alt': 'Изображения без alt', 'H1 headings': 'Заголовки H1', 'Certificate name': 'Имя сертификата', 'Registry domain': 'Домен в реестре',
    'Registration': 'Регистрация', 'Expiration': 'Истечение', 'Last changed': 'Изменение', 'Registrar': 'Регистратор', 'Nameserver': 'NS-сервер', 'Snapshot URL': 'Адрес снимка', 'Snapshot time (UTC)': 'Время снимка (UTC)', 'HTTP status': 'HTTP-статус',
    'No HTTP response to analyze.': 'Нет HTTP-ответа для анализа.', 'No HTML page available for analysis.': 'HTML-страница недоступна для анализа.',
    'Certificate verified by the system.': 'Сертификат проверен системой.', 'HTTP does not use a certificate.': 'Для HTTP сертификат не используется.', 'Could not verify the certificate.': 'Не удалось проверить сертификат.',
    'Metadata from the requested HTML page.': 'Метаданные из HTML запрошенной страницы.', 'Public mailto links and links to known platforms from the page.': 'Публичные mailto-ссылки и ссылки на известные платформы со страницы.',
    'Indexing directives from the response and metadata; search engines are not queried.': 'Директивы индексации из ответа и метаданных; поисковые системы не опрашиваются.',
    'Response text unavailable; check not performed.': 'Текст ответа недоступен; проверка не выполнена.', 'Selected indicators from the source HTML only; not an accessibility audit.': 'Только отдельные признаки исходного HTML; это не аудит доступности.',
    'Possible database error messages found. This is not an SQL injection test.': 'Найдены возможные сообщения об ошибках базы данных. Это не проверка SQL-инъекций.',
    'No known error signatures found in the response fragment. This is not an SQL injection test.': 'Известные сигнатуры ошибок в фрагменте ответа не найдены. Это не проверка SQL-инъекций.',
    'Disabled. When enabled, the domain is sent to crt.sh.': 'Отключено. При включении домен передаётся на crt.sh.',
    'Disabled. When enabled, the domain is sent to rdap.org and the registry.': 'Отключено. При включении домен передаётся на rdap.org и в реестр.',
    'Disabled. When enabled, the website address is sent to Internet Archive.': 'Отключено. При включении адрес сайта передаётся в Internet Archive.',
    'Public RDAP registration data. Some details may be hidden.': 'Публичные регистрационные данные RDAP. Некоторые сведения могут быть скрыты.', 'Closest available home-page snapshot.': 'Ближайший доступный снимок главной страницы.', 'No archived home-page snapshot found.': 'Архивная копия главной страницы не найдена.',

    /* Media and update log. */
    'SIGNAL / 03 ─ MEDIA & SUPPORT': 'SIGNAL / 03 ─ МЕДИА И ПОДДЕРЖКА', 'Stay in the': 'Оставайтесь', 'loop.': 'на связи.', 'Support the signal.': 'Поддержите Signal.',
    'Follow the project for updates and support the continued development of Signal OSINT.': 'Следите за обновлениями проекта и поддержите дальнейшее развитие Signal OSINT.',
    '01 / CHANNEL': '01 / КАНАЛ', '02 / SUPPORT': '02 / ПОДДЕРЖКА', 'Signal on Telegram': 'Signal в Telegram', 'Keep Signal running.': 'Поддержите работу Signal.',
    'Find project news, updates, and more on the official Signal OSINT channel.': 'Новости проекта, обновления и другие материалы — в официальном Telegram-канале Signal OSINT.',
    'If you find Signal useful, you can support the project through its Monobank donation jar.': 'Если Signal вам полезен, вы можете поддержать проект через банку Monobank.',
    'Open Telegram': 'Открыть Telegram', 'Donation': 'Поддержать проект', 'Public information. Responsible research.': 'Открытые данные. Ответственное исследование.',
    'SIGNAL / 04 ─ CHANGELOG': 'SIGNAL / 04 ─ ИСТОРИЯ ОБНОВЛЕНИЙ', 'Tracking the': 'Развитие', 'signal.': 'Signal.', 'What changed.': 'Что изменилось.',
    'A record of the improvements made to Signal OSINT, from workspace updates to new features.': 'История улучшений Signal OSINT: от изменений интерфейса до новых возможностей.',
    'Project updates': 'Обновления проекта', '01 / CURRENT UPDATE': '01 / ТЕКУЩЕЕ ОБНОВЛЕНИЕ', '02 / PREVIOUS UPDATE': '02 / ПРЕДЫДУЩЕЕ ОБНОВЛЕНИЕ', '03 / FOUNDATION': '03 / ОСНОВА',
    'Choose your language. Explore the dark.': 'Выберите язык. Исследуйте глубже.', 'A more focused interface and a new way to follow the project.': 'Более собранный интерфейс и новый способ следить за проектом.',
    'Switch between English and Russian from the top of the site. Your preference stays in your browser.': 'Переключайтесь между английским и русским вверху сайта. Выбор сохраняется в браузере.',
    'A darker, terminal-inspired visual style across the workspaces.': 'Более тёмное оформление в стиле терминала во всех разделах.', 'This update log keeps the project\'s changes in one place.': 'История обновлений собирает изменения проекта в одном месте.',
    'More sources. More context.': 'Больше источников. Больше контекста.', 'The people-search workspace received clearer controls and additional public sources.': 'В разделе поиска людей появились удобные настройки и дополнительные открытые источники.',
    'Bluesky, Mastodon.social, and Wikidata were added to the source selection.': 'В выбор источников добавлены Bluesky, Mastodon.social и Wikidata.',
    'Source presets, status filtering, and improved graph prioritization make results easier to explore.': 'Наборы источников, фильтр статусов и улучшенная приоритизация графа упрощают изучение результатов.',
    'The Media page now links to the Signal Telegram channel and donation jar.': 'На странице Media доступны ссылки на Telegram-канал Signal и банку для поддержки.',
    'The Signal workspace.': 'Рабочее пространство Signal.', 'Public-source people searches and passive website investigations in one place.': 'Поиск людей в открытых источниках и пассивное исследование сайтов в одном месте.',
    'Explore results using relationship graphs and manual search links.': 'Изучайте результаты с помощью графов связей и ссылок для ручного поиска.',
    'Save and compare browser history, and export reports in supported formats.': 'Сохраняйте и сравнивайте историю в браузере, экспортируйте отчёты в поддерживаемых форматах.',
    'Results are not identity verification or a full security audit. Verify sources independently.': 'Результаты не подтверждают личность и не являются полным аудитом безопасности. Проверяйте источники самостоятельно.',
    'New entries will appear here as the project is updated.': 'Новые записи появятся здесь по мере обновления проекта.',

    /* Website landing page and user-facing errors. */
    'Capabilities': 'Возможности', 'How it works': 'Как это работает', 'Responsible use': 'О данных', 'Open workspace': 'Открыть платформу',
    'WEB INTELLIGENCE STARTS HERE': 'ВЕБ-РАЗВЕДКА НАЧИНАЕТСЯ ЗДЕСЬ', 'Gather the facts.': 'Собирайте факты.', 'See the connections.': 'Находите связи.',
    'Public website data, its digital footprint, and connections in one clear workspace.': 'Публичные данные сайта, его цифровое окружение и связи в одном пространстве.',
    'Enter a domain, e.g. example.org': 'Введите домен, например example.org', 'Website domain': 'Домен сайта', 'Investigate': 'Исследовать',
    'Public data only. Do not include passwords or tokens in the address.': 'Только открытые данные. Не вводите пароли или токены в адрес.',
    '20 analysis modules': '20 модулей анализа', 'Visual graph': 'Визуальный граф', 'Export reports': 'Экспорт отчётов',
    'Example relationship graph': 'Пример графа связей', 'Example relationship map': 'Пример карты связей', 'Example map: domain connected to IP, TLS, DNS, and public sources': 'Пример карты: домен связан с IP, TLS, DNS и открытыми источниками',
    'YOUR DOMAIN': 'ВАШ ДОМЕН', 'IP addresses': 'IP-адреса', 'Sources': 'Источники', 'Connections from public sources': 'Связи из открытых источников', 'EXAMPLE, NOT LIVE DATA': 'ПРИМЕР, НЕ РЕАЛЬНЫЕ ДАННЫЕ',
    'search and analysis modules': 'модулей поиска и анализа', 'workspace for results': 'пространство для результатов', 'public website data': 'открытые данные сайта', 'interactive relationship map': 'интерактивная карта связей',
    'CAPABILITIES / 01': 'ВОЗМОЖНОСТИ / 01', 'The bigger picture,': 'Всё важное —', 'in one place.': 'в одном месте.',
    'From technical profiles to external sources, Signal helps organize data and reveal context.': 'От технического профиля до внешних источников: Signal помогает организовать данные и увидеть контекст.',
    'Website profile': 'Профиль сайта', 'DNS, HTTP, TLS, technologies, headers, links, forms, and other data from the requested page.': 'DNS, HTTP, TLS, технологии, заголовки, ссылки, формы и другие данные запрошенной страницы.',
    '20 MODULES': '20 МОДУЛЕЙ', 'Explore relationships between domains, addresses, resources, and discovered names.': 'Исследуйте связи между доменами, адресами, ресурсами и найденными именами.', 'INTERACTIVE MAP': 'ИНТЕРАКТИВНАЯ КАРТА',
    'Compare investigations of the same domain and save results as JSON, Markdown, or SVG.': 'Сравнивайте исследования одного домена и сохраняйте результаты в JSON, Markdown или SVG.', 'EXPORT RESULTS': 'ЭКСПОРТ РЕЗУЛЬТАТОВ',
    'More public sources': 'Больше открытых источников', 'Optionally add Certificate Transparency, RDAP data, and the Wayback Machine archive. Each external source is enabled separately.': 'По желанию подключайте Certificate Transparency, данные RDAP и архив Wayback Machine. Каждый внешний источник включается отдельно.',
    'Under your control': 'Под вашим контролем', 'History is stored in your browser. Third-party sources are used only when selected.': 'История хранится в браузере. Сторонние источники используются только по выбору.',
    'HOW IT WORKS / 02': 'КАК ЭТО РАБОТАЕТ / 02', 'From domain': 'От домена', 'to understanding.': 'к пониманию.',
    'No complicated setup: enter a target and choose the sources you want to use.': 'Никаких сложных настроек: укажите цель и выберите источники.',
    'Enter an address': 'Введите адрес', 'Enter a public domain or page address you have permission to investigate.': 'Укажите публичный домен или адрес страницы, которую вам разрешено исследовать.',
    'Explore the data': 'Изучите данные', 'Modules collect available information and show missing data or errors.': 'Модули соберут доступную информацию и покажут отсутствие данных или ошибки.',
    'See connections': 'Посмотрите связи', 'Open the graph, compare previous results, and save a report.': 'Откройте граф, сравните предыдущие результаты и сохраните отчёт.',
    'Investigate responsibly.': 'Исследуйте ответственно.', 'Signal uses public data and is not a full security audit. Use it only within your authorization.': 'Signal работает с открытыми данными и не является полным аудитом безопасности. Используйте его только в рамках имеющихся прав.',
    'Passive website analysis': 'Пассивный анализ сайтов', 'Open investigation': 'Перейти к исследованию', 'History is stored in the browser. When enabled, external sources receive the address.': 'История хранится в браузере. При включении внешние источники получают адрес.',
    'Browser storage is unavailable. Open the workspace and enter the address there.': 'Хранилище браузера недоступно. Откройте платформу и введите адрес там.',
    'Run a search first.': 'Сначала выполните поиск.', 'Run an investigation first.': 'Сначала выполните исследование.',
    'Delete saved people-search history in this browser?': 'Удалить сохранённую историю поиска людей в этом браузере?', 'Delete all local investigation history?': 'Удалить всю локальную историю исследований?',
    'Enter a username, name or ORCID iD.': 'Введите ник, имя или ORCID iD.', 'Enter a valid ORCID iD.': 'Введите корректный ORCID iD.',
    'ORCID must have 16 characters, for example 0000-0002-1825-0097.': 'ORCID должен содержать 16 символов, например 0000-0002-1825-0097.', 'The ORCID check digit is invalid.': 'Контрольная цифра ORCID неверна.',
    'Use up to 39 Latin letters, numbers, dots, hyphens or underscores for the username; do not enter a URL or email address.': 'Ник должен содержать до 39 латинских букв, цифр, точек, дефисов или подчёркиваний. Не вводите ссылку или email.',
    'Names may contain letters, spaces, hyphens and apostrophes, up to 100 characters.': 'Имя может содержать буквы, пробелы, дефисы и апострофы, до 100 символов.',
    'Context may contain letters, numbers, spaces, dots and hyphens, up to 80 characters.': 'Контекст может содержать буквы, цифры, пробелы, точки и дефисы, до 80 символов.',
    'An unknown source was selected.': 'Выбран неизвестный источник.', 'Select at least one source that matches the information you entered.': 'Выберите хотя бы один источник, подходящий для введённых данных.',
    'Enter a full HTTPS link to a public profile.': 'Введите полную HTTPS-ссылку на публичный профиль.', 'Use an HTTPS link without credentials or a nonstandard port.': 'Используйте HTTPS-ссылку без логина, пароля и нестандартного порта.',
    'Use a supported GitHub, GitLab, DEV, Hacker News, Bluesky handle, or Mastodon.social profile link.': 'Введите ссылку на поддерживаемый профиль GitHub, GitLab, DEV, Hacker News, Bluesky или Mastodon.social.',
    'Enter a supported public profile link.': 'Введите поддерживаемую ссылку на публичный профиль.', 'Enter a profile link.': 'Введите ссылку на профиль.', 'Enter an ORCID iD or an https://orcid.org/... link.': 'Введите ORCID iD или ссылку https://orcid.org/...',
    'The username and profile URL do not match. Correct one of them.': 'Ник и ссылка указывают на разные имена. Исправьте одно из значений.',
    'Server error': 'Ошибка сервера', 'Unexpected server response': 'Неожиданный ответ сервера', 'Unexpected response format': 'Неожиданный формат ответа',
    'Search completed, but history could not be saved in this browser.': 'Поиск выполнен, но историю не удалось сохранить в браузере.',
    'Investigation completed, but history could not be saved in this browser.': 'Исследование выполнено, но историю не удалось сохранить в браузере.',
    'Invalid host or request origin.': 'Недопустимый адрес или источник запроса.', 'Check the request format and size.': 'Проверьте формат и размер запроса.',
    'The server is busy. Please try again in a few seconds.': 'Сервер занят. Попробуйте снова через несколько секунд.',
    'The shared investigation limit has been reached. Please try again later.': 'Достигнут общий лимит исследований. Попробуйте позже.',
    'An internal error occurred. Check your input and try again.': 'Внутренняя ошибка. Проверьте введённые данные и повторите попытку.',
    'The source response exceeded the size limit.': 'Ответ источника превысил ограничение размера.', 'The source returned an unsupported content encoding.': 'Источник вернул неподдерживаемое кодирование.',
    'Enter a domain or address up to 2048 characters long.': 'Введите домен или адрес длиной до 2048 символов.', 'The address contains invalid characters.': 'Адрес содержит недопустимые символы.',
    'Only ports 80 and 443 are allowed.': 'Разрешены только порты 80 и 443.', 'Enter a valid public HTTP(S) address without credentials.': 'Укажите корректный публичный HTTP(S)-адрес без логина и пароля.',
    'Only public IP addresses are allowed. Local and mixed DNS responses are blocked.': 'Разрешены только публичные IP-адреса. Локальные и смешанные DNS-ответы запрещены.',
    'Collecting data…': 'Сбор данных…',
    'Signal — explore the open web': 'Signal — исследуйте открытый веб', 'Signal OSINT — website intelligence': 'Signal OSINT — исследование сайтов',
    'SIGNAL / People OSINT': 'SIGNAL / Поиск людей', 'Media & Support | Signal OSINT': 'Медиа и поддержка | Signal OSINT', 'Updates | Signal OSINT': 'Обновления | Signal OSINT'
  };

  const patterns = [
    [/^(\d+) sources? selected · (\d+) applicable to the current input$/, (_, a, b) => `Выбрано источников: ${a} · подходят введённым данным: ${b}`],
    [/^MODULES: (\d+) \/ PUBLIC SOURCE DATA$/, (_, n) => `МОДУЛЕЙ: ${n} / ОТКРЫТЫЕ ДАННЫЕ`],
    [/^UPDATED: (.+)$/, (_, date) => `ОБНОВЛЕНО: ${date}`],
    [/^CHANGED: (\d+)$/, (_, n) => `ИЗМЕНЕНО: ${n}`],
    [/^CHANGES: (\d+)$/, (_, n) => `ИЗМЕНЕНИЙ: ${n}`],
    [/^Comparison: (.+)$/, (_, host) => `Сравнение: ${host}`],
    [/^Investigation time: ([\d.]+) s$/, (_, n) => `Время исследования: ${n} с`],
    [/^\/ (\d+) modules$/, (_, n) => `/ ${n} модулей`],
    [/^\+ more (\d+) modules$/, (_, n) => `+ ещё ${n} модулей`],
    [/^Format: (\+\d+)\nThe basic format check passed\. The number, carrier, and owner are not verified\.$/, (_, n) => `Формат: ${n}\nУпрощённая проверка формата пройдена. Сам номер, оператор и владелец не проверены.`],
    [/^Showing (\d+) public (repositories|organizations), up to 20\. The list may be incomplete\.$/, (_, n, type) => `Показано: ${n} публичных ${type === 'repositories' ? 'репозиториев' : 'организаций'} (до 20). Список может быть неполным.`],
    [/^Found (\d+) articles\. Namesakes and unrelated results are possible\.$/, (_, n) => `Найдено статей: ${n}. Возможны тёзки и нерелевантные результаты.`],
    [/^Found (\d+) entities\. Results can include unrelated people or subjects\.$/, (_, n) => `Найдено записей: ${n}. Результаты могут относиться к другим людям или темам.`],
    [/^Found (\d+) display-name results\. This is a search, not identity verification\.$/, (_, n) => `Найдено результатов по отображаемому имени: ${n}. Это поиск, а не проверка личности.`],
    [/^Found (\d+) author-name results\. Unrelated matches are possible\.$/, (_, n) => `Найдено результатов по имени автора: ${n}. Возможны нерелевантные совпадения.`],
    [/^Prepared (\d+) links\. Search engines were not queried; open and verify the results yourself\.$/, (_, n) => `Подготовлено ссылок: ${n}. Поисковые системы не опрашивались; откройте и проверьте результаты самостоятельно.`],
    [/^No public profile was found for (.+)\. Other Bluesky domains were not checked\.$/, (_, handle) => `Публичный профиль ${handle} не найден. Другие домены Bluesky не проверялись.`],
    [/^System DNS returned (\d+) public addresses\.$/, (_, n) => `Системный DNS вернул публичных адресов: ${n}.`],
    [/^HTTP (\d+); response time (\d+) ms\.$/, (_, code, ms) => `HTTP ${code}; время ответа ${ms} мс.`],
    [/^Found (\d+) of (\d+) headers\. Missing headers do not always indicate a vulnerability\.$/, (_, a, b) => `Найдено заголовков: ${a} из ${b}. Их отсутствие не всегда означает уязвимость.`],
    [/^Found (\d+) Set-Cookie headers\. Values are not stored\.$/, (_, n) => `Найдено заголовков Set-Cookie: ${n}. Значения не сохраняются.`],
    [/^Found (\d+) clues\. Data may be incomplete or misleading\.$/, (_, n) => `Найдено подсказок: ${n}. Данные могут быть неполными или подменёнными.`],
    [/^Links: (\d+); external: (\d+)\. Additional pages were not visited\.$/, (_, a, b) => `Ссылок: ${a}; внешних: ${b}. Дополнительные страницы не посещались.`],
    [/^Forms on page: (\d+)\. Forms are not submitted; field values are not saved\.$/, (_, n) => `Форм на странице: ${n}. Формы не отправляются, значения полей не сохраняются.`],
    [/^HTML resources: (\d+); external domains: (\d+)\. Resources were not loaded\.$/, (_, a, b) => `Ресурсов в HTML: ${a}; внешних доменов: ${b}. Ресурсы не загружались.`],
    [/^Found (\d+) names in public certificates \(up to 100\)\. Their current existence is not confirmed\.$/, (_, n) => `Найдено имён в публичных сертификатах: ${n} (до 100). Их текущее существование не подтверждено.`],
    [/^HTTP (\d+|no response); (\d+) directives recognized\.$/, (_, code, n) => `HTTP ${code === 'no response' ? 'нет ответа' : code}; распознано директив: ${n}.`],
    [/^HTTP (\d+|no response); file unavailable or not recognized\.$/, (_, code) => `HTTP ${code === 'no response' ? 'нет ответа' : code}; файл недоступен или не распознан.`],
    [/^\/sitemap\.xml: HTTP (\d+|no response); (\d+) links read \(up to 100\)\.$/, (_, code, n) => `/sitemap.xml: HTTP ${code === 'no response' ? 'нет ответа' : code}; прочитано ссылок: ${n} (до 100).`],
    [/^\/sitemap\.xml: HTTP (\d+|no response); XML is unavailable, invalid or exceeds the limit\.$/, (_, code) => `/sitemap.xml: HTTP ${code === 'no response' ? 'нет ответа' : code}; XML недоступен, некорректен или превышает лимит.`],
    [/^\/\.well-known\/security\.txt: HTTP (\d+|no response); (\d+) fields recognized\.$/, (_, code, n) => `/.well-known/security.txt: HTTP ${code === 'no response' ? 'нет ответа' : code}; распознано полей: ${n}.`],
    [/^\/\.well-known\/security\.txt: HTTP (\d+|no response); file not found or not recognized\.$/, (_, code) => `/.well-known/security.txt: HTTP ${code === 'no response' ? 'нет ответа' : code}; файл не найден или не распознан.`],
    [/^Source returned HTTP (\d+)( \(possibly rate-limited\))?$/, (_, code, limited) => `Источник вернул HTTP ${code}${limited ? ' (возможно, превышен лимит запросов)' : ''}`],
    [/^(.+) · (username|name)( \(sign-in may be required\))?$/, (_, service, tag, login) => `${service.replace(/ search$/, ' поиск')} · ${tag === 'username' ? 'ник' : 'имя'}${login ? ' (может потребоваться вход)' : ''}`],
    [/^Search query · search query$/, () => 'Поисковый запрос · поисковый запрос'],
    [/^(.+) · (search query|profile|repository|organization|article)$/, (_, label, kind) => `${label} · ${ru[kind]}`],
    [/^(ERROR \/ |Investigation failed: |Source unavailable: |Request failed: |Could not resolve the domain via DNS: |Could not reach the source: )([\s\S]+)$/, (_, prefix, detail) => ({'ERROR / ': 'ОШИБКА / ', 'Investigation failed: ': 'Не удалось выполнить исследование: ', 'Source unavailable: ': 'Источник недоступен: ', 'Request failed: ': 'Запрос не выполнен: ', 'Could not resolve the domain via DNS: ': 'Не удалось разрешить домен через DNS: ', 'Could not reach the source: ': 'Не удалось связаться с источником: '}[prefix] + translate(detail))],
    [/^(.*) · Search result; identity is not confirmed\.$/, (_, description) => `${description} · Результат поиска; личность не подтверждена.`],
    [/^Reputation: (.+) · identity is not confirmed$/, (_, n) => `Репутация: ${n} · личность не подтверждена`],
    [/^DOI: (.+) · authorship is not confirmed by a name match$/, (_, doi) => `DOI: ${doi} · авторство по совпадению имени не подтверждено`],
    [/^★ (\d+) · language not specified$/, (_, n) => `★ ${n} · язык не указан`],
    [/^(.+) · status$/, (_, title) => `${translate(title)} · статус`],
    [/^Form (\d+)$/, (_, n) => `Форма ${n}`]
  ];

  function translate(value) {
    const raw = String(value == null ? '' : value);
    const parts = raw.match(/^(\s*)([\s\S]*?)(\s*)$/);
    if (!parts || !parts[2]) return raw;
    const lead = parts[1], trail = parts[3];
    const text = parts[2].replace(/\u00a0/g, ' ').replace(/[ \t]+/g, ' ');
    if (Object.prototype.hasOwnProperty.call(ru, text)) return lead + ru[text] + trail;
    for (const [pattern, render] of patterns) {
      const match = text.match(pattern);
      if (match) return lead + render(...match) + trail;
    }
    // Keep visual icons and arrows while translating their adjacent label.
    const decorated = text.match(/^([◉◈⌘◇◷●◎✧]\s+)?(.+?)(\s*[↗↓→])?$/);
    if (decorated && Object.prototype.hasOwnProperty.call(ru, decorated[2])) {
      return lead + (decorated[1] || '') + ru[decorated[2]] + (decorated[3] || '') + trail;
    }
    return raw;
  }

  // Search filters can match both English labels and their Russian translations
  // without changing the underlying results or stored reports.
  window.signalI18nText = translate;

  let language = 'en';
  try { if (localStorage.getItem('signal-language') === 'ru') language = 'ru'; } catch (e) { /* English remains available without storage. */ }

  function addNavigation() {
    const headerNav = document.querySelector('.header nav');
    if (headerNav && !headerNav.querySelector('a[href="/updates"]')) {
      const link = document.createElement('a');
      link.href = '/updates';
      link.textContent = headerNav.classList.contains('navigation') ? 'Updates' : 'UPDATES';
      headerNav.appendChild(link);
    }
    const sidebar = document.querySelector('.sidebar');
    if (sidebar && !sidebar.querySelector('a[href="/updates"]')) {
      const link = document.createElement('a');
      link.className = 'nav'; link.href = '/updates';
      link.setAttribute('aria-label', 'Updates');
      link.innerHTML = '<span class="icon">≡</span><span class="nav-text">Updates ↗</span>';
      const separator = sidebar.querySelector('.side-separator');
      sidebar.insertBefore(link, separator || null);
    }
    document.querySelectorAll('.section-switch, .workspace-switch').forEach(nav => {
      if (nav.querySelector('a[href="/updates"]')) return;
      const link = document.createElement('a');
      link.href = '/updates';
      link.innerHTML = '<span><strong>04 / UPDATES</strong><small>What\'s new in Signal</small></span><span class="arrow">↗</span>';
      nav.appendChild(link);
    });
    // The landing-page navigation is hidden on narrow screens.
    if (headerNav && headerNav.classList.contains('navigation')) {
      const compact = document.createElement('a');
      compact.className = 'updates-short'; compact.href = '/updates'; compact.textContent = 'LOG';
      headerNav.parentElement.insertBefore(compact, headerNav.nextSibling);
    }
  }
  addNavigation();

  const switcher = document.createElement('button');
  switcher.type = 'button'; switcher.className = 'language-switch';
  const switchContainer = document.querySelector('.header-inner') || document.querySelector('.topright');
  if (switchContainer) switchContainer.appendChild(switcher);

  const originals = new WeakMap();
  const originalAttributes = new WeakMap();
  const trackedAttributes = ['placeholder', 'title', 'aria-label'];
  const originalTitle = document.title;

  function isExternalData(element) {
    if (!element) return false;
    if (element.closest('#stat-query, #stat-target, #redirect-url, .history-row strong, .item a, .gnode')) return true;
    const graphNode = element.closest('.graph-node');
    if (graphNode) {
      // Only the synthetic root label is application text; all other node labels are source data.
      const root = graphNode.parentElement && graphNode.parentElement.firstElementChild === graphNode;
      return !(root && (element === graphNode || element === graphNode.lastElementChild));
    }
    const fact = element.closest('.fact');
    return Boolean(fact && fact.children.length > 1 && fact.children[1].contains(element));
  }

  function shouldSkip(element) {
    return !element || Boolean(element.closest('script, style, textarea, [contenteditable="true"], .language-switch, [data-no-translate]'));
  }

  function applyText(node) {
    const element = node.parentElement;
    if (shouldSkip(element) || isExternalData(element)) return;
    // A plain item may contain a user-supplied title. Only translate its known empty-state message.
    if (element.classList.contains('item') && node.data.trim() !== 'No additional data.') return;
    const current = node.data;
    let state = originals.get(node);
    if (!state) state = { source: current, last: current };
    else if (current !== state.last) state.source = current;
    const rendered = language === 'ru' ? translate(state.source) : state.source;
    state.last = rendered; originals.set(node, state);
    if (current !== rendered) node.data = rendered;
  }

  function applyAttributes(element) {
    if (shouldSkip(element) || isExternalData(element)) return;
    let states = originalAttributes.get(element);
    if (!states) { states = {}; originalAttributes.set(element, states); }
    for (const name of trackedAttributes) {
      if (!element.hasAttribute(name)) continue;
      const current = element.getAttribute(name);
      let state = states[name];
      if (!state) state = states[name] = { source: current, last: current };
      else if (current !== state.last) state.source = current;
      const rendered = language === 'ru' ? translate(state.source) : state.source;
      state.last = rendered;
      if (current !== rendered) element.setAttribute(name, rendered);
    }
  }

  function applyTree(root) {
    if (root.nodeType === Node.TEXT_NODE) { applyText(root); return; }
    if (root.nodeType !== Node.ELEMENT_NODE) return;
    applyAttributes(root);
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_ELEMENT | NodeFilter.SHOW_TEXT);
    while (walker.nextNode()) {
      if (walker.currentNode.nodeType === Node.TEXT_NODE) applyText(walker.currentNode);
      else applyAttributes(walker.currentNode);
    }
  }

  function updateLanguage(save) {
    document.documentElement.lang = language;
    document.title = language === 'ru' ? translate(originalTitle) : originalTitle;
    switcher.textContent = language === 'en' ? 'RU' : 'EN';
    switcher.setAttribute('aria-label', language === 'en' ? 'Switch to Russian' : 'Переключить на английский');
    switcher.title = language === 'en' ? 'Переключить на русский' : 'Switch to English';
    if (save) { try { localStorage.setItem('signal-language', language); } catch (e) { /* Use this page's language only. */ } }
    applyTree(document.body);
  }

  const observer = new MutationObserver(records => {
    for (const record of records) {
      if (record.type === 'characterData') applyText(record.target);
      else if (record.type === 'attributes') applyAttributes(record.target);
      else record.addedNodes.forEach(applyTree);
    }
  });
  observer.observe(document.body, { subtree: true, childList: true, characterData: true, attributes: true, attributeFilter: trackedAttributes });
  switcher.addEventListener('click', () => { language = language === 'en' ? 'ru' : 'en'; updateLanguage(true); });
  window.addEventListener('storage', event => {
    if (event.key === 'signal-language') { language = event.newValue === 'ru' ? 'ru' : 'en'; updateLanguage(false); }
  });
  const nativeAlert = window.alert.bind(window), nativeConfirm = window.confirm.bind(window);
  window.alert = message => nativeAlert(language === 'ru' ? translate(message) : message);
  window.confirm = message => nativeConfirm(language === 'ru' ? translate(message) : message);
  updateLanguage(false);
})();

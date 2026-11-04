/* UI-only translation. Search data, saved reports, URLs and exports are not modified. */
(function () {
  'use strict';

  // Historical UI labels are retained for compatibility and translation
  // coverage checks. Russian is no longer a selectable interface language.
  const ru = {
    'Main navigation': 'Основная навигация', 'Navigation': 'Навигация', 'Workspaces': 'Разделы', 'Signal home': 'Signal — на главную',
    'PEOPLE': 'ЛЮДИ', 'SITES': 'САЙТЫ', 'MEDIA': 'МЕДИА', 'UPDATES': 'ОБНОВЛЕНИЯ', 'ACCOUNT': 'АККАУНТ',
    'People': 'Люди', 'Media': 'Медиа', 'Updates': 'Обновления', 'Account': 'Аккаунт', 'LOG': 'ЛОГ',
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
    'Extracts a username from GitHub, GitLab, DEV, Hacker News, Bluesky, Mastodon.social, Instagram, TikTok, or Telegram. The link is not visited.': 'Извлекает ник из GitHub, GitLab, DEV, Hacker News, Bluesky, Mastodon.social, Instagram, TikTok или Telegram. Сама ссылка не посещается.',
    'EXTRACT USERNAME': 'ИЗВЛЕЧЬ НИК', 'Public researcher identifier, not a phone number.': 'Публичный идентификатор исследователя, не номер телефона.',
    'CONTEXT FOR MANUAL SEARCH': 'КОНТЕКСТ ДЛЯ РУЧНОГО ПОИСКА',
    'Added to Google, Bing, and DuckDuckGo links; does not verify identity.': 'Добавляется к ссылкам Google, Bing и DuckDuckGo; не подтверждает личность.',
    'SOURCES': 'ИСТОЧНИКИ', 'Source selection': 'Выбор источников', 'All': 'Все', 'Profiles': 'Профили', 'Research': 'Исследования', 'Clear': 'Очистить', 'Wikipedia': 'Википедия',
    '198 profile sites': '198 сайтов с профилями', 'OPTIONAL': 'ОПЦИОНАЛЬНО',
    'The optional group sends the username to up to 198 sites and may take a minute. Blocked or uncertain results require manual verification.': 'Дополнительная группа отправляет ник максимум на 198 сайтов; поиск может занять минуту. Заблокированные и неясные результаты нужно проверить вручную.',
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
    'Status': 'Статус', 'All statuses': 'Все статусы', 'Found': 'Найдено', 'Unverified': 'Не проверено', 'No data': 'Нет данных', 'Error': 'Ошибка', 'Disabled': 'Отключено', 'Ready': 'Готово',
    'FOUND': 'НАЙДЕНО', 'UNVERIFIED': 'НЕ ПРОВЕРЕНО', 'NO DATA': 'НЕТ ДАННЫХ', 'ERROR': 'ОШИБКА', 'DISABLED': 'ОТКЛЮЧЕНО', 'READY': 'ГОТОВО',
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
    'Open profile': 'Открыть профиль', 'Profile found; a name match does not confirm identity.': 'Найден профиль; совпадение ника не подтверждает личность.',
    'No accessible public profile was found; a private or unavailable profile is still possible.': 'Доступный публичный профиль не найден; закрытый или недоступный профиль всё ещё возможен.',
    'Could not verify the profile automatically; open the link and check it yourself.': 'Не удалось автоматически проверить профиль; откройте ссылку и проверьте вручную.',
    'The service was unavailable or blocked the request; check the link manually.': 'Сервис недоступен или заблокировал запрос; проверьте ссылку вручную.',
    'Skipped: this username cannot be used as a subdomain for this site.': 'Пропущено: этот ник нельзя использовать как поддомен данного сайта.',
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
    '03 / TON': '03 / TON', 'Donate with TON': 'Поддержать через TON',
    'Send TON directly to this address on the TON mainnet. Verify the address and network in your wallet before sending.': 'Отправьте TON напрямую на этот адрес в основной сети TON. Перед отправкой проверьте адрес и сеть в своём кошельке.',
    'Copy TON address': 'Скопировать адрес TON', 'Address copied.': 'Адрес скопирован.', 'Copy unavailable. Select and copy the address manually.': 'Не удалось скопировать. Выделите адрес и скопируйте его вручную.',
    'SIGNAL / 04 ─ CHANGELOG': 'SIGNAL / 04 ─ ИСТОРИЯ ОБНОВЛЕНИЙ', 'Tracking the': 'Развитие', 'signal.': 'Signal.', 'What changed.': 'Что изменилось.',
    'A record of the improvements made to Signal OSINT, from workspace updates to new features.': 'История улучшений Signal OSINT: от изменений интерфейса до новых возможностей.',
    'Project updates': 'Обновления проекта', '01 / CURRENT UPDATE': '01 / ТЕКУЩЕЕ ОБНОВЛЕНИЕ', '02 / PREVIOUS UPDATE': '02 / ПРЕДЫДУЩЕЕ ОБНОВЛЕНИЕ', '03 / EARLIER UPDATE': '03 / ПРЕЖНЕЕ ОБНОВЛЕНИЕ', '04 / FOUNDATION': '04 / ОСНОВА',
    '04 / EARLIER UPDATE': '04 / ПРЕЖНЕЕ ОБНОВЛЕНИЕ', '05 / FOUNDATION': '05 / ОСНОВА',
    'More places to find a username.': 'Больше сайтов для поиска по нику.',
    'The people workspace can now check 198 public profile sites in one optional search.': 'Раздел поиска людей теперь может проверить 198 сайтов с публичными профилями за один дополнительный поиск.',
    'Search social networks, creator platforms, communities, and developer sites, including Telegram, Instagram, and TikTok.': 'Поиск в соцсетях, на творческих площадках, в сообществах и на сайтах для разработчиков, включая Telegram, Instagram и TikTok.',
    'Unverified, blocked, or unavailable responses are distinguished from confirmed profile indicators; open the links to check them yourself.': 'Непроверенные ответы, блокировки и недоступные сервисы не выдаются за подтверждённые профили; открывайте ссылки для самостоятельной проверки.',
    'The expanded search is optional, and existing sources, history, graph, and exports remain available.': 'Расширенный поиск включается по желанию; прежние источники, история, граф и экспорт остаются доступны.',
    'Matching usernames do not establish that accounts belong to the same person.': 'Совпадение ников не означает, что аккаунты принадлежат одному человеку.',
    'A clearer signal.': 'Чётче и проще.', 'A monochrome workspace with optional accounts and new ways to support the project.': 'Монохромный интерфейс, необязательные аккаунты и новые способы поддержки проекта.',
    'A new homepage presents the project and its workspaces.': 'Новая главная страница представляет проект и его разделы.',
    'A minimal black-and-white design across the site.': 'Минималистичный чёрно-белый дизайн на всём сайте.',
    'Sign in or create an account; registered accounts are stored in a database and managed in an access-controlled administrator area.': 'Вход и регистрация; аккаунты хранятся в базе данных, а управление доступно только в защищённом разделе администратора.',
    'Passwords are stored as salted Argon2id hashes, and administrator access is checked on the server.': 'Пароли хранятся как хеши Argon2id с солью, а доступ администратора проверяется на сервере.',
    'Support Signal directly with TON from the Media page, alongside the existing Monobank donation link.': 'Поддержка Signal через TON на странице Media, наряду с существующей ссылкой Monobank.',
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

    /* Account and administrator UI. Account data itself is never translated. */
    'SIGNAL / ACCOUNT': 'SIGNAL / АККАУНТ', 'Your account.': 'Ваш аккаунт.',
    'Sign in or create an account. The public workspaces remain available without signing in.': 'Войдите или создайте аккаунт. Публичные разделы по-прежнему доступны без входа.',
    'JavaScript is required to use accounts.': 'Для использования аккаунтов необходим JavaScript.', 'Account access': 'Доступ к аккаунту',
    'Sign in': 'Войти', 'Create account': 'Создать аккаунт', 'PASSWORD': 'ПАРОЛЬ', 'CONFIRM PASSWORD': 'ПОДТВЕРДИТЕ ПАРОЛЬ',
    '3–32 Latin letters, numbers, dots, underscores or hyphens.': 'От 3 до 32 латинских букв, цифр, точек, подчёркиваний или дефисов.',
    'Use a unique password of 10–128 characters.': 'Используйте уникальный пароль длиной от 10 до 128 символов.',
    'SIGNED IN': 'ВЫ ВОШЛИ', 'Administrator': 'Администратор', 'Member': 'Пользователь', 'Sign out': 'Выйти', 'Open admin panel': 'Открыть админ-панель',
    'Change password': 'Изменить пароль', 'Changing your password signs you out on all devices.': 'После смены пароля вы выйдете из аккаунта на всех устройствах.',
    'CURRENT PASSWORD': 'ТЕКУЩИЙ ПАРОЛЬ', 'NEW PASSWORD': 'НОВЫЙ ПАРОЛЬ', 'CONFIRM NEW PASSWORD': 'ПОДТВЕРДИТЕ НОВЫЙ ПАРОЛЬ', 'Update password': 'Сохранить пароль',
    'ACCOUNT SECURITY / 01': 'БЕЗОПАСНОСТЬ АККАУНТА / 01', 'Keep your access private.': 'Берегите доступ к аккаунту.',
    'Passwords are stored as salted Argon2id hashes, not as readable text. Do not reuse passwords or share them with anyone.': 'Пароли хранятся как хеши Argon2id с солью, а не открытым текстом. Не используйте один пароль повторно и никому его не сообщайте.',
    'Accounts are optional. Search history still stays in your browser unless you choose to save it.': 'Аккаунты необязательны. История поиска сохраняется только в браузере, если вы включили её сохранение.',
    'There is currently no automated password recovery. Keep your password safe.': 'Автоматического восстановления пароля пока нет. Сохраните пароль в надёжном месте.',
    'SIGNAL / ADMINISTRATION': 'SIGNAL / АДМИНИСТРИРОВАНИЕ', 'Account oversight.': 'Управление аккаунтами.',
    'Review registered accounts and manage access. Passwords and password hashes are never shown here.': 'Просматривайте зарегистрированные аккаунты и управляйте доступом. Пароли и их хеши здесь не отображаются.',
    '← Back to account': '← Назад в аккаунт', 'Registered accounts': 'Зарегистрированные аккаунты', 'Loading accounts…': 'Загрузка аккаунтов…',
    'Refresh': 'Обновить', 'Active': 'Активен', 'Disable': 'Отключить', 'Enable': 'Включить', 'Protected': 'Защищён',
    'Showing up to 200 accounts. Administrator accounts cannot be disabled here.': 'Показано до 200 аккаунтов. Отключить администратора здесь нельзя.',
    'Authorized access only.': 'Доступ только для уполномоченных лиц.',
    'Disable this account? Its sessions will be signed out.': 'Отключить аккаунт? Его активные сеансы будут завершены.', 'Enable this account?': 'Включить этот аккаунт?',
    'Passwords do not match.': 'Пароли не совпадают.', 'Unexpected server response.': 'Неожиданный ответ сервера.', 'Account service is unavailable.': 'Сервис аккаунтов недоступен.',
    'Accounts are not configured or temporarily unavailable.': 'Аккаунты ещё не настроены или временно недоступны.', 'Account access requires HTTPS.': 'Для доступа к аккаунту требуется HTTPS.',
    'Username must be 3–32 Latin letters, numbers, dots, underscores or hyphens, starting with a letter or number.': 'Имя пользователя должно содержать 3–32 латинские буквы, цифры, точки, подчёркивания или дефисы и начинаться с буквы или цифры.',
    'Password must be 10–128 characters long.': 'Пароль должен содержать от 10 до 128 символов.', 'Password contains invalid characters.': 'Пароль содержит недопустимые символы.',
    'Enter a valid username.': 'Введите корректное имя пользователя.', 'This username is already in use.': 'Это имя пользователя уже занято.', 'Invalid username or password.': 'Неверное имя пользователя или пароль.',
    'Too many attempts. Please try again later.': 'Слишком много попыток. Попробуйте позже.', 'Account service is busy. Please try again.': 'Сервис аккаунтов занят. Попробуйте снова.',
    'Please sign in first.': 'Сначала войдите в аккаунт.', 'Your session could not be verified. Refresh and try again.': 'Не удалось проверить сеанс. Обновите страницу и повторите попытку.',
    'Current password is incorrect.': 'Текущий пароль неверен.', 'Choose a different new password.': 'Новый пароль должен отличаться от текущего.',
    'Password changed. Sign in again.': 'Пароль изменён. Войдите снова.', 'Account changed. Please sign in again.': 'Аккаунт изменён. Войдите снова.',
    'Invalid account request.': 'Некорректный запрос к аккаунту.', 'Account not found or cannot be changed.': 'Аккаунт не найден или его нельзя изменить.',
    'Account is unavailable.': 'Аккаунт недоступен.', 'An internal account error occurred.': 'Внутренняя ошибка сервиса аккаунтов.',
    'Expected a JSON request.': 'Ожидается запрос JSON.', 'Invalid request origin.': 'Недопустимый источник запроса.',
    'Account | Signal OSINT': 'Аккаунт | Signal OSINT', 'Administration | Signal OSINT': 'Администрирование | Signal OSINT',

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
    'Use a supported GitHub, GitLab, DEV, Hacker News, Bluesky, Mastodon.social, Instagram, TikTok, or Telegram profile link.': 'Введите поддерживаемую ссылку на профиль GitHub, GitLab, DEV, Hacker News, Bluesky, Mastodon.social, Instagram, TikTok или Telegram.',
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
    'SIGNAL / People OSINT': 'SIGNAL / Поиск людей', 'Media & Support | Signal OSINT': 'Медиа и поддержка | Signal OSINT', 'Updates | Signal OSINT': 'Обновления | Signal OSINT',

    /* Homepage: the presentation copy is static site text, never user data. */
    'Signal OSINT — open-source intelligence': 'Signal OSINT — разведка по открытым данным',
    'HOME': 'ГЛАВНАЯ',
    'Find the signal in': 'Найдите сигнал в', 'public data.': 'открытых данных.',
    'SIGNAL / 00 ─ OVERVIEW': 'SIGNAL / 00 ─ ОБЗОР',
    'Find the signal in public data.': 'Найдите сигнал в открытых данных.',
    'Signal OSINT is a workspace for responsible open-source research. Look up public profiles by username, name, or ORCID iD, investigate websites without touching them, and export structured reports. All results come from public sources.': 'Signal OSINT — рабочее пространство для ответственного исследования открытых источников. Найдите публичные профили по нику, имени или ORCID iD, изучите сайты, не посещая их, и получите структурированные отчёты. Данные берутся только из открытых источников.',
    'Start people search': 'Начать поиск людей', 'Investigate a website': 'Исследовать сайт',
    '03 / PRINCIPLES': '03 / ПРИНЦИПЫ',
    'Find public profiles.': 'Найдите публичные профили.',
    'Search by username, full name, or ORCID iD across more than a dozen public sources, then explore the connections in an interactive graph.': 'Ищите по нику, полному имени или ORCID iD более чем в десятке открытых источников, а затем изучайте связи на интерактивном графе.',
    'GitHub, GitLab, Wikipedia, Bluesky, Mastodon, and more': 'GitHub, GitLab, Wikipedia, Bluesky, Mastodon и другие',
    'Manual search links for search engines': 'Ссылки на поисковые системы для ручной проверки',
    'Local history with JSON and Markdown exports': 'Локальная история, экспорт в JSON и Markdown',
    'Open the workspace': 'Открыть раздел',
    'Investigate websites passively.': 'Пассивное исследование сайтов.',
    'Enter an address and Signal checks DNS, HTTP, TLS, security headers, links, technology hints, and public metadata in a few bounded requests.': 'Введите адрес, и Signal в нескольких ограниченных запросах проверит DNS, HTTP, TLS, заголовки безопасности, ссылки, технологии и публичные метаданные.',
    '20 modules, from DNS to sitemap': '20 модулей: от DNS до sitemap',
    'Relationship graph and saved history': 'Граф связей и сохранённая история',
    'JSON, Markdown, and SVG exports': 'Экспорт в JSON, Markdown и SVG',
    'Public sources only.': 'Только открытые источники.',
    'Signal does not search leaked databases, test passwords, or exploit anything. A result is a hint, never a proof of identity or of safety.': 'Signal не ищет слитые базы, не проверяет пароли и не взламывает ничего. Результат — подсказка, а не доказательство личности или безопасности.',
    'No leaked data, scanning, or exploitation': 'Без слитых данных, сканирования и взлома',
    'Verify every finding independently': 'Проверяйте каждую находку самостоятельно',
    'Respect the law and privacy': 'Уважайте закон и частную жизнь',
    'See what changed': 'Что изменилось',
    'HOW IT WORKS': 'КАК ЭТО РАБОТАЕТ',
    'Choose a workspace': 'Выберите раздел',
    'Open People to search profiles or Sites to inspect an address. No account is required for either.': 'Откройте «Люди» для поиска профилей или «Сайты» для проверки адреса. Аккаунт не требуется ни там, ни там.',
    'Review the evidence': 'Изучите данные',
    'Filter results, open the source links, explore the relationship graph, and compare saved searches.': 'Фильтруйте результаты, открывайте ссылки на источники, изучайте граф связей и сравнивайте сохранённые поиски.',
    'Export and verify': 'Сохраните и проверьте',
    'Download JSON, Markdown, or SVG, then confirm your findings through independent sources. Accounts stay optional.': 'Скачайте JSON, Markdown или SVG и подтвердите находки через независимые источники. Аккаунты остаются необязательными.',
    'Follow and support Signal.': 'Подпишитесь и поддержите Signal.',
    'News, updates, and donations live on the Media page. The public workspaces stay free.': 'Новости, обновления и поддержка — на странице Media. Публичные разделы остаются бесплатными.',
    'Media and support': 'Медиа и поддержка'
  };

  // Spanish UI copy. User-provided values and external source data are never
  // translated or sent to a translation service by the running application.
  const es = {
    'Main navigation': 'Navegación principal', 'Navigation': 'Navegación', 'Workspaces': 'Espacios de trabajo', 'Signal home': 'Inicio de Signal',
    'PEOPLE': 'PERSONAS', 'SITES': 'SITIOS', 'MEDIA': 'MEDIOS', 'UPDATES': 'ACTUALIZACIONES', 'ACCOUNT': 'CUENTA',
    'People': 'Personas', 'Media': 'Medios', 'Updates': 'Actualizaciones', 'Account': 'Cuenta', 'LOG': 'REGISTRO',
    '01 / PEOPLE': '01 / PERSONAS', '02 / SITES': '02 / SITIOS', '03 / MEDIA': '03 / MEDIOS', '04 / UPDATES': '04 / ACTUALIZACIONES',
    'Public profiles and articles': 'Perfiles y artículos públicos', 'Domains and connections': 'Dominios y conexiones',
    'Follow and support Signal': 'Sigue y apoya a Signal', "What's new in Signal": 'Novedades de Signal',
    'WORKSPACE / PEOPLE INTELLIGENCE': 'ESPACIO DE TRABAJO / BÚSQUEDA DE PERSONAS', 'PUBLIC SOURCES ONLY': 'SOLO FUENTES PÚBLICAS',
    'OPEN SOURCE INTELLIGENCE': 'INTELIGENCIA DE FUENTES ABIERTAS', 'WEB INTELLIGENCE': 'INTELIGENCIA WEB',
    'Find the signal.': 'Encuentra la señal.', 'Follow the connections.': 'Sigue las conexiones.',
    'Explore public profiles and articles. Follow the evidence, verify the source, and never assume a match is an identity.': 'Explora perfiles y artículos públicos. Revisa las pruebas, verifica las fuentes y no confundas una coincidencia con una identidad.',
    'SIGNAL / 01 ─ PEOPLE': 'SIGNAL / 01 ─ PERSONAS', '01 / SEARCH PARAMETERS': '01 / PARÁMETROS DE BÚSQUEDA',
    'Enter a username, name, or both': 'Introduce un nombre de usuario, un nombre o ambos', 'Username, name, profile URL, or ORCID iD': 'Usuario, nombre, URL de perfil u ORCID iD',
    'QUERY': 'CONSULTA', 'USERNAME': 'NOMBRE DE USUARIO', 'FULL NAME': 'NOMBRE COMPLETO', 'PUBLIC PROFILE URL': 'URL DEL PERFIL PÚBLICO',
    'e.g. octocat': 'p. ej., octocat', 'e.g. Ada Lovelace': 'p. ej., Ada Lovelace', 'e.g. university': 'p. ej., universidad',
    'No links or email addresses.': 'Sin enlaces ni direcciones de correo.', 'Used for public name searches.': 'Se utiliza para buscar nombres en fuentes públicas.',
    'Used for Wikipedia, Wikidata, Stack Overflow, Crossref, and manual searches.': 'Se utiliza para Wikipedia, Wikidata, Stack Overflow, Crossref y búsquedas manuales.',
    'Extracts a username from a supported public profile. The URL itself is not visited.': 'Extrae el usuario de un perfil público compatible. La URL no se visita.',
    'Extracts a username from GitHub, GitLab, DEV, Hacker News, Bluesky, or Mastodon.social. The link is not visited.': 'Extrae el usuario de GitHub, GitLab, DEV, Hacker News, Bluesky o Mastodon.social. El enlace no se visita.',
    'Extracts a username from GitHub, GitLab, DEV, Hacker News, Bluesky, Mastodon.social, Instagram, TikTok, or Telegram. The link is not visited.': 'Extrae el usuario de GitHub, GitLab, DEV, Hacker News, Bluesky, Mastodon.social, Instagram, TikTok o Telegram. El enlace no se visita.',
    'EXTRACT USERNAME': 'EXTRAER USUARIO', 'Public researcher identifier, not a phone number.': 'Identificador público de investigador, no un número de teléfono.',
    'CONTEXT FOR MANUAL SEARCH': 'CONTEXTO PARA LA BÚSQUEDA MANUAL', 'Added to Google, Bing, and DuckDuckGo links; does not verify identity.': 'Se añade a los enlaces de Google, Bing y DuckDuckGo; no verifica la identidad.',
    'SOURCES': 'FUENTES', 'Source selection': 'Selección de fuentes', 'All': 'Todas', 'Profiles': 'Perfiles', 'Research': 'Investigación', 'Clear': 'Limpiar', 'Wikipedia': 'Wikipedia',
    '445 profile sites': '445 sitios con perfiles', '198 profile sites': '198 sitios con perfiles', 'OPTIONAL': 'OPCIONAL',
    'The optional group sends the username to up to 445 sites and may take several minutes. Blocked or uncertain results require manual verification.': 'El grupo opcional envía el usuario a un máximo de 445 sitios y puede tardar varios minutos. Los resultados bloqueados o inciertos requieren verificación manual.',
    'The optional group sends the username to up to 198 sites and may take a minute. Blocked or uncertain results require manual verification.': 'El grupo opcional envía el usuario a un máximo de 198 sitios y puede tardar un minuto. Los resultados bloqueados o inciertos requieren verificación manual.',
    'Save history in this browser': 'Guardar historial en este navegador',
    'Selected sources receive the username, name, or ORCID. History is off by default. Do not enter addresses, phone numbers, passwords, or tokens in search fields.': 'Las fuentes seleccionadas reciben el usuario, nombre u ORCID. El historial está desactivado por defecto. No introduzcas direcciones, teléfonos, contraseñas ni tokens.',
    'Selected sources receive your username or name. History is off by default. Do not enter addresses, phone numbers, passwords, or tokens.': 'Las fuentes seleccionadas reciben el usuario o nombre. El historial está desactivado por defecto. No introduzcas direcciones, teléfonos, contraseñas ni tokens.',
    'START SEARCH': 'INICIAR BÚSQUEDA', 'SEARCHING...': 'BUSCANDO...', '02 / PHONE FORMAT': '02 / FORMATO DE TELÉFONO',
    'Checked only in this browser. The number is not sent to the server, and this does not find an owner or verify the number exists.': 'Se comprueba solo en este navegador. El número no se envía al servidor; no se busca al propietario ni se verifica que exista.',
    'INTERNATIONAL FORMAT': 'FORMATO INTERNACIONAL', '+ and country code': '+ y código de país', 'CHECK FORMAT': 'COMPROBAR FORMATO', 'CLEAR': 'LIMPIAR',
    'Enter an international number beginning with +. Spaces, parentheses, and hyphens are allowed.': 'Introduce un número internacional que comience con +. Se permiten espacios, paréntesis y guiones.',
    'Invalid format: use 7 to 15 digits after +, starting with a non-zero digit.': 'Formato incorrecto: usa entre 7 y 15 dígitos después de +, comenzando con un dígito distinto de cero.',
    'The basic format check passed. The number, carrier, and owner are not verified.': 'La comprobación básica del formato ha terminado. El número, la operadora y el propietario no están verificados.',
    'MODULES': 'MÓDULOS', 'MATCHES': 'COINCIDENCIAS', 'FOUND IN': 'ENCONTRADO EN', 'ERRORS': 'ERRORES',
    'name / username': 'nombre / usuario', 'username / name / ORCID': 'usuario / nombre / ORCID', 'sources and sections': 'fuentes y secciones',
    'not identity verification': 'no verifica la identidad', 'modules; not identification': 'módulos; no identifica', 'unavailable sources': 'fuentes no disponibles',
    'RESULTS': 'RESULTADOS', 'RELATIONSHIP GRAPH': 'GRAFO DE RELACIONES', 'SEARCH LINKS': 'ENLACES DE BÚSQUEDA', 'HISTORY': 'HISTORIAL',
    '[ VIEW DETAILS ]': '[ VER DETALLES ]', 'Waiting for a search': 'Esperando una búsqueda', 'Filter results...': 'Filtrar resultados...', 'Filter results': 'Filtrar resultados',
    'Status': 'Estado', 'All statuses': 'Todos los estados', 'Found': 'Encontrado', 'Unverified': 'No verificado', 'No data': 'Sin datos', 'Error': 'Error', 'Disabled': 'Desactivado', 'Ready': 'Listo',
    'FOUND': 'ENCONTRADO', 'UNVERIFIED': 'NO VERIFICADO', 'NO DATA': 'SIN DATOS', 'ERROR': 'ERROR', 'DISABLED': 'DESACTIVADO', 'READY': 'LISTO',
    '[ AWAITING DATA ]': '[ ESPERANDO DATOS ]', 'Enter a username or a name.': 'Introduce un usuario o nombre.', 'Results will appear here after your search.': 'Los resultados aparecerán aquí después de la búsqueda.',
    'No results match the filter.': 'No hay resultados para el filtro.', 'No results match this status and text filter.': 'No hay resultados para este estado y filtro de texto.',
    'The query is connected to results, not a verified identity.': 'La consulta se conecta con resultados, no con una identidad verificada.',
    'Zoom in': 'Acercar', 'Zoom out': 'Alejar', 'RESET': 'RESTABLECER', 'Reset': 'Restablecer', 'Public source graph': 'Grafo de fuentes públicas', 'GRAPH IS EMPTY': 'EL GRAFO ESTÁ VACÍO',
    'Select a node to view its source. Up to 35 nodes are shown.': 'Selecciona un nodo para ver su fuente. Se muestran hasta 35 nodos.',
    'Drag nodes and select them to view their source. Up to 35 nodes are shown.': 'Arrastra y selecciona los nodos para ver su fuente. Se muestran hasta 35 nodos.',
    'OPEN SOURCE': 'ABRIR FUENTE', 'Search query': 'Consulta de búsqueda', 'search query': 'consulta de búsqueda', 'profile': 'perfil', 'repository': 'repositorio', 'organization': 'organización', 'article': 'artículo',
    'Open these links to verify results yourself. Services open only when selected.': 'Abre estos enlaces para verificar los resultados. Los servicios se abren solo al seleccionarlos.',
    'Search links will appear after a search.': 'Los enlaces aparecerán después de una búsqueda.', 'The query is sent to the service only when you open the link.': 'La consulta se envía al servicio solo al abrir el enlace.',
    'History stays in this browser when saving is enabled.': 'El historial permanece en este navegador cuando se activa el guardado.', 'CLEAR HISTORY': 'BORRAR HISTORIAL',
    'History is empty. Enable saving before searching if you need it.': 'El historial está vacío. Activa el guardado antes de buscar si lo necesitas.',
    'COMPARE': 'COMPARAR', 'COMPARE SEARCHES': 'COMPARAR BÚSQUEDAS', 'No changes found in available data.': 'No se encontraron cambios en los datos disponibles.',
    '[ IMPORTANT ] Matching names or usernames do not prove profiles belong to the same person. Verify sources independently and use this tool responsibly and lawfully.': '[ IMPORTANTE ] Los nombres o usuarios coincidentes no prueban que los perfiles pertenezcan a la misma persona. Verifica las fuentes y usa esta herramienta de forma responsable y legal.',
    'EXPORT JSON': 'EXPORTAR JSON', 'EXPORT MARKDOWN': 'EXPORTAR MARKDOWN', 'AWAITING SEARCH': 'ESPERANDO BÚSQUEDA',
    'Public data · bounded requests': 'Datos públicos · solicitudes limitadas', 'OPEN SITE INVESTIGATION': 'ABRIR INVESTIGACIÓN DE SITIOS', 'This is not identity verification or an exhaustive search.': 'Esto no verifica la identidad ni es una búsqueda exhaustiva.', 'OPEN': 'ABRIR',
    'WORKSPACE': 'ESPACIO DE TRABAJO', 'SIGNAL / WORKSPACE': 'SIGNAL / ESPACIO DE TRABAJO', 'SIGNAL / PEOPLE INTELLIGENCE': 'SIGNAL / BÚSQUEDA DE PERSONAS',
    'INFORMATION': 'INFORMACIÓN', 'People search': 'Búsqueda de personas', 'Website overview': 'Resumen del sitio web',
    'Search modules': 'Módulos de búsqueda', 'Relationship graph': 'Grafo de relaciones', 'History and reports': 'Historial e informes', 'Media & support': 'Medios y apoyo',
    'About': 'Acerca de', 'Browser history': 'Historial del navegador', 'Results are saved in this browser. External sources are enabled separately.': 'Los resultados se guardan en este navegador. Las fuentes externas se activan por separado.',
    'OVERVIEW': 'RESUMEN', 'SEARCH MODULES': 'MÓDULOS DE BÚSQUEDA', 'HISTORY AND REPORTS': 'HISTORIAL E INFORMES', 'ABOUT': 'ACERCA DE',
    'Home': 'Inicio', '← Home': '← Inicio', 'Web platform': 'Plataforma web', 'PASSIVE OSINT': 'OSINT PASIVO',
    'WEB INTELLIGENCE WORKSPACE': 'ESPACIO DE INTELIGENCIA WEB', 'See beyond the surface.': 'Mira más allá de la superficie.',
    'Public data, connections, and a website’s technical profile in one workspace.': 'Datos públicos, conexiones y el perfil técnico de un sitio en un solo espacio.',
    'New investigation': 'Nueva investigación', 'HTTP(S) · public domains and IPs': 'HTTP(S) · dominios e IP públicas',
    'Enter a domain or address, e.g. example.com': 'Introduce un dominio o dirección, p. ej., example.com', 'Start investigation': 'Iniciar investigación',
    'crt.sh · certificates': 'crt.sh · certificados', 'RDAP · registration': 'RDAP · registro', 'Wayback · archive': 'Wayback · archivo',
    'Optional: the domain is sent to the selected external services': 'Opcional: el dominio se envía a los servicios externos seleccionados',
    'The site returned a redirect. Automatic redirects are disabled. New address without parameters:': 'El sitio devolvió una redirección. Las redirecciones automáticas están desactivadas. Nueva dirección sin parámetros:',
    'Investigate this address': 'Investigar esta dirección', 'ACTIVE TARGET': 'OBJETIVO ACTIVO', 'Target domain': 'Dominio objetivo', 'HTTP STATUS': 'ESTADO HTTP',
    'Awaiting investigation': 'Esperando investigación', 'IP ADDRESSES': 'DIRECCIONES IP', 'System DNS responses': 'Respuestas DNS del sistema', 'Passive sources and analysis': 'Fuentes pasivas y análisis',
    'Investigation coverage': 'Cobertura de la investigación', 'Module status for the current target': 'Estado de los módulos del objetivo actual', 'waiting': 'en espera', 'complete': 'completado',
    'Module results': 'Resultados de módulos', 'Latest investigation': 'Última investigación', 'All modules': 'Todos los módulos',
    'Nothing here yet': 'Todavía no hay datos', 'Enter a domain above to collect your first results.': 'Introduce un dominio para obtener los primeros resultados.',
    'Each module shows its source and the limits of its results.': 'Cada módulo muestra su fuente y los límites de sus resultados.', 'Search modules...': 'Buscar módulos...',
    'Warning': 'Advertencia', 'Errors': 'Errores', 'Information': 'Información',
    'Select a node for details. Drag nodes and zoom the graph.': 'Selecciona un nodo para ver detalles. Arrastra los nodos y amplía el grafo.', 'Download SVG': 'Descargar SVG',
    'Up to 20 investigations in local browser storage. Compare results for the same target.': 'Hasta 20 investigaciones guardadas en el navegador. Compara resultados del mismo objetivo.',
    'Export JSON': 'Exportar JSON', 'Export Markdown': 'Exportar Markdown', 'Clear history': 'Borrar historial', 'Transparency about sources and the limits of analysis.': 'Información sobre las fuentes y los límites del análisis.',
    'What is analyzed': 'Qué se analiza', 'External sources': 'Fuentes externas', 'What Signal does not do': 'Lo que Signal no hace', 'Privacy': 'Privacidad',
    'System DNS, HTTP response, TLS certificate, requested page HTML, and three public files: robots.txt, sitemap.xml, and security.txt. At most four GET requests are made to the site; redirects and discovered links are not followed.': 'DNS del sistema, respuesta HTTP, certificado TLS, HTML de la página y tres archivos públicos: robots.txt, sitemap.xml y security.txt. Se hacen como máximo cuatro solicitudes GET; no se siguen redirecciones ni enlaces.',
    'crt.sh, RDAP, and Internet Archive are enabled separately. The domain is sent to selected services; RDAP may redirect the request to the appropriate registry. Results may be incomplete or outdated.': 'crt.sh, RDAP e Internet Archive se activan por separado. El dominio se envía a los servicios seleccionados; RDAP puede redirigir la solicitud al registro correspondiente. Los resultados pueden estar incompletos o desactualizados.',
    'Signal does not exploit vulnerabilities, test SQL injection, guess passwords, submit forms, or crawl websites. A lack of findings does not mean a site is secure.': 'Signal no explota vulnerabilidades, prueba inyecciones SQL, adivina contraseñas, envía formularios ni rastrea sitios. La ausencia de hallazgos no significa que un sitio sea seguro.',
    'History stays in this browser. Cookie and form field values are not collected, and URL parameters are removed from reports. The site may reflect parameters elsewhere; do not enter secrets.': 'El historial permanece en este navegador. No se recopilan valores de cookies ni formularios y se eliminan los parámetros URL de los informes. El sitio puede reflejarlos en otros datos; no introduzcas secretos.',
    'Passive intelligence.': 'Inteligencia pasiva.', 'Investigate only websites you have permission to examine. Data can be incomplete; results are not a security audit.': 'Investiga solo sitios que estés autorizado a examinar. Los datos pueden estar incompletos y los resultados no son una auditoría de seguridad.',
    'Visual map of discovered connections · up to 60 nodes': 'Mapa visual de conexiones descubiertas · hasta 60 nodos', 'Website relationship graph': 'Grafo de relaciones del sitio', 'RELATIONSHIP MAP': 'MAPA DE RELACIONES', 'NETWORK / 01': 'RED / 01',
    'Scroll to zoom · drag to move nodes': 'Desplázate para ampliar · arrastra para mover nodos', 'Domain': 'Dominio', 'Certificate': 'Certificado', 'Resource / link': 'Recurso / enlace',
    'Select a node': 'Selecciona un nodo', 'The map is empty': 'El mapa está vacío', 'Run an investigation to see connections': 'Ejecuta una investigación para ver conexiones',
    'Optional search via crt.sh.': 'Búsqueda opcional mediante crt.sh.', 'Results appear after an investigation.': 'Los resultados aparecen después de una investigación.', 'Details': 'Detalles',
    'No additional data.': 'No hay datos adicionales.', 'No results match this filter.': 'No hay resultados para este filtro.',
    'History is empty': 'El historial está vacío', 'Completed investigations appear here.': 'Las investigaciones completadas aparecen aquí.', 'Compare': 'Comparar', 'Open': 'Abrir',
    'Before:': 'Antes:', 'After:': 'Después:', 'Showing the first 50 changes.': 'Se muestran los primeros 50 cambios.', 'No differences found in the available data.': 'No se encontraron diferencias en los datos disponibles.',
    'GitHub · profile': 'GitHub · perfil', 'GitHub · repositories': 'GitHub · repositorios', 'GitHub · organizations': 'GitHub · organizaciones',
    'GitLab · profile': 'GitLab · perfil', 'Hacker News · profile': 'Hacker News · perfil', 'DEV Community · profile': 'DEV Community · perfil',
    'Bluesky · profile': 'Bluesky · perfil', 'Mastodon.social · profile': 'Mastodon.social · perfil', 'Wikipedia · Russian': 'Wikipedia · ruso', 'Wikipedia · English': 'Wikipedia · inglés',
    'Wikidata · entity search': 'Wikidata · búsqueda de entidades', 'Stack Overflow · profile search': 'Stack Overflow · búsqueda de perfiles', 'Crossref · publications': 'Crossref · publicaciones', 'ORCID · researcher': 'ORCID · investigador', 'Search links': 'Enlaces de búsqueda',
    'Select GitHub and enter a username.': 'Selecciona GitHub e introduce un usuario.', 'Select GitLab and enter a username.': 'Selecciona GitLab e introduce un usuario.',
    'Select Hacker News and enter a username.': 'Selecciona Hacker News e introduce un usuario.', 'Select DEV Community and enter a username.': 'Selecciona DEV Community e introduce un usuario.',
    'Enter a compatible Bluesky handle or username and select Bluesky. A plain username is checked as username.bsky.social.': 'Introduce un identificador de Bluesky compatible y selecciona Bluesky. Un usuario simple se comprueba como usuario.bsky.social.',
    'Select Mastodon.social and enter a username. Other Mastodon servers are not checked.': 'Selecciona Mastodon.social e introduce un usuario. No se comprueban otros servidores de Mastodon.',
    'Select Wikipedia and enter a name.': 'Selecciona Wikipedia e introduce un nombre.', 'Select Wikidata and enter a name.': 'Selecciona Wikidata e introduce un nombre.',
    'Select Stack Overflow and enter a name or username.': 'Selecciona Stack Overflow e introduce un nombre o usuario.', 'Select Crossref and enter a name.': 'Selecciona Crossref e introduce un nombre.', 'Select ORCID and enter a public ORCID iD.': 'Selecciona ORCID e introduce un ORCID iD público.',
    'A public profile with this exact username was found. Verify its identity independently.': 'Se encontró un perfil público con este usuario exacto. Verifica la identidad de forma independiente.',
    'A public profile with this exact username was found.': 'Se encontró un perfil público con este usuario exacto.', 'No accessible public profile with this exact username was found.': 'No se encontró un perfil público accesible con este usuario exacto.',
    'An exact public username was found. This does not establish a match with other profiles.': 'Se encontró un usuario público exacto. Esto no confirma una relación con otros perfiles.',
    'An exact public Bluesky handle was found; verify the identity independently.': 'Se encontró un identificador público exacto de Bluesky; verifica la identidad de forma independiente.',
    'A public profile with this exact username was found on mastodon.social only.': 'Se encontró un perfil con este usuario únicamente en mastodon.social.', 'No public profile was found on mastodon.social. Other servers were not checked.': 'No se encontró un perfil público en mastodon.social. No se comprobaron otros servidores.',
    'No data found or the profile is unavailable.': 'No hay datos o el perfil no está disponible.', 'The source returned an unexpected response.': 'La fuente devolvió una respuesta inesperada.',
    'Name search result; identity is not confirmed.': 'Resultado de búsqueda por nombre; identidad no confirmada.', 'Search result; identity is not confirmed.': 'Resultado de búsqueda; identidad no confirmada.',
    'No accessible public record was found.': 'No se encontró un registro público accesible.', 'Public record for the supplied ORCID. This does not confirm a match with other results.': 'Registro público del ORCID proporcionado. No confirma una coincidencia con otros resultados.',
    'Display name': 'Nombre visible', 'Username': 'Usuario', 'Company': 'Empresa', 'Public repositories': 'Repositorios públicos', 'Followers': 'Seguidores', 'Following': 'Siguiendo', 'Created': 'Creado',
    'Handle': 'Identificador', 'Given name': 'Nombre', 'Family name': 'Apellido', 'Credit name': 'Nombre publicado', 'Public organization': 'Organización pública', 'language not specified': 'idioma no especificado',
    'Open GitHub': 'Abrir GitHub', 'Open GitLab': 'Abrir GitLab', 'Open Hacker News': 'Abrir Hacker News', 'Open DEV': 'Abrir DEV', 'Open Bluesky': 'Abrir Bluesky', 'Open Mastodon': 'Abrir Mastodon', 'Open ORCID': 'Abrir ORCID',
    'Open profile': 'Abrir perfil', 'Profile found; a name match does not confirm identity.': 'Perfil encontrado; una coincidencia de nombre no confirma la identidad.',
    'No accessible public profile was found; a private or unavailable profile is still possible.': 'No se encontró un perfil público accesible; aún podría existir un perfil privado o no disponible.',
    'Could not verify the profile automatically; open the link and check it yourself.': 'No se pudo verificar el perfil automáticamente; abre el enlace y compruébalo.',
    'The service was unavailable or blocked the request; check the link manually.': 'El servicio no estaba disponible o bloqueó la solicitud; comprueba el enlace manualmente.',
    'Skipped: this username cannot be used as a subdomain for this site.': 'Omitido: este usuario no puede utilizarse como subdominio en este sitio.',
    'DNS and addresses': 'DNS y direcciones', 'HTTP response': 'Respuesta HTTP', 'TLS certificate': 'Certificado TLS', 'Security headers': 'Cabeceras de seguridad', 'Cookie settings': 'Configuración de cookies',
    'Technologies and server': 'Tecnologías y servidor', 'Page metadata': 'Metadatos de la página', 'Links and external domains': 'Enlaces y dominios externos', 'Contacts and social links': 'Contactos y enlaces sociales',
    'Forms and fields': 'Formularios y campos', 'External resources': 'Recursos externos', 'Indexing': 'Indexación', 'Database errors': 'Errores de base de datos', 'Basic accessibility indicators': 'Indicadores básicos de accesibilidad',
    'Domain registration · RDAP': 'Registro de dominio · RDAP', 'Website archive · Wayback': 'Archivo web · Wayback', 'URL without parameters': 'URL sin parámetros', 'Redirect (not followed)': 'Redirección (no seguida)',
    'Bytes read': 'Bytes leídos', 'Protocol': 'Protocolo', 'Issuer': 'Emisor', 'Expires': 'Caduca', 'Certificate names': 'Nombres del certificado', 'Language': 'Idioma', 'External link': 'Enlace externo',
    'Internal links': 'Enlaces internos', 'Platform': 'Plataforma', 'Entry': 'Entrada', 'Signature': 'Firma', 'HTML language': 'Idioma HTML', 'Images without alt': 'Imágenes sin alt', 'H1 headings': 'Encabezados H1',
    'Certificate name': 'Nombre del certificado', 'Registry domain': 'Dominio del registro', 'Registration': 'Registro', 'Expiration': 'Caducidad', 'Last changed': 'Última modificación', 'Registrar': 'Registrador',
    'Nameserver': 'Servidor de nombres', 'Snapshot URL': 'URL de la captura', 'Snapshot time (UTC)': 'Fecha de la captura (UTC)', 'HTTP status': 'Estado HTTP',
    'No HTTP response to analyze.': 'No hay respuesta HTTP para analizar.', 'No HTML page available for analysis.': 'No hay página HTML disponible para analizar.',
    'Certificate verified by the system.': 'Certificado verificado por el sistema.', 'HTTP does not use a certificate.': 'HTTP no utiliza certificado.', 'Could not verify the certificate.': 'No se pudo verificar el certificado.',
    'Metadata from the requested HTML page.': 'Metadatos de la página HTML solicitada.', 'Public mailto links and links to known platforms from the page.': 'Enlaces mailto públicos y enlaces a plataformas conocidas de la página.',
    'Indexing directives from the response and metadata; search engines are not queried.': 'Directivas de indexación de la respuesta y metadatos; no se consultan buscadores.',
    'Response text unavailable; check not performed.': 'Texto de respuesta no disponible; no se realizó la comprobación.', 'Selected indicators from the source HTML only; not an accessibility audit.': 'Solo indicadores del HTML de origen; no es una auditoría de accesibilidad.',
    'Possible database error messages found. This is not an SQL injection test.': 'Se encontraron posibles mensajes de error de base de datos. Esto no es una prueba de inyección SQL.',
    'No known error signatures found in the response fragment. This is not an SQL injection test.': 'No se encontraron firmas de error conocidas en el fragmento de respuesta. Esto no es una prueba de inyección SQL.',
    'Disabled. When enabled, the domain is sent to crt.sh.': 'Desactivado. Al activarlo, el dominio se envía a crt.sh.', 'Disabled. When enabled, the domain is sent to rdap.org and the registry.': 'Desactivado. Al activarlo, el dominio se envía a rdap.org y al registro.',
    'Disabled. When enabled, the website address is sent to Internet Archive.': 'Desactivado. Al activarlo, la dirección se envía a Internet Archive.',
    'Public RDAP registration data. Some details may be hidden.': 'Datos públicos de registro RDAP. Algunos detalles pueden estar ocultos.', 'Closest available home-page snapshot.': 'Captura disponible más cercana de la página inicial.', 'No archived home-page snapshot found.': 'No se encontró una captura archivada de la página inicial.',
    'SIGNAL / 03 ─ MEDIA & SUPPORT': 'SIGNAL / 03 ─ MEDIOS Y APOYO', 'Stay in the': 'Mantente al', 'loop.': 'día.', 'Support the signal.': 'Apoya a Signal.',
    'Follow the project for updates and support the continued development of Signal OSINT.': 'Sigue las novedades y apoya el desarrollo continuo de Signal OSINT.',
    '01 / CHANNEL': '01 / CANAL', '02 / SUPPORT': '02 / APOYO', '02 / TON': '02 / TON', '03 / TON': '03 / TON', 'Signal on Telegram': 'Signal en Telegram', 'Keep Signal running.': 'Apoya a Signal.',
    'Find project news, updates, and more on the official Signal OSINT channel.': 'Encuentra noticias y novedades en el canal oficial de Signal OSINT.',
    'Open Telegram': 'Abrir Telegram', 'Donation': 'Donación', 'Public information. Responsible research.': 'Información pública. Investigación responsable.', 'Donate with TON': 'Donar con TON',
    'If you find Signal useful, you can support the project through its Monobank donation jar.': 'En esa versión se podía apoyar el proyecto mediante Monobank.',
    'Send TON directly to this address on the TON mainnet. Verify the address and network in your wallet before sending.': 'Envía TON directamente a esta dirección en la red principal de TON. Verifica la dirección y la red en tu cartera antes de enviar.',
    'Copy TON address': 'Copiar dirección TON', 'Address copied.': 'Dirección copiada.', 'Copy unavailable. Select and copy the address manually.': 'No se pudo copiar. Selecciona y copia la dirección manualmente.',
    'SIGNAL / 04 ─ CHANGELOG': 'SIGNAL / 04 ─ REGISTRO DE CAMBIOS', 'Tracking the': 'Seguimiento de', 'signal.': 'Signal.', 'What changed.': 'Qué ha cambiado.',
    'A record of the improvements made to Signal OSINT, from workspace updates to new features.': 'Un registro de las mejoras de Signal OSINT, desde cambios en el espacio de trabajo hasta nuevas funciones.',
    'Project updates': 'Actualizaciones del proyecto', '01 / CURRENT UPDATE': '01 / ACTUALIZACIÓN ACTUAL', '02 / PREVIOUS UPDATE': '02 / ACTUALIZACIÓN ANTERIOR', '03 / EARLIER UPDATE': '03 / ACTUALIZACIÓN PREVIA', '04 / EARLIER UPDATE': '04 / ACTUALIZACIÓN PREVIA', '05 / EARLIER UPDATE': '05 / ACTUALIZACIÓN PREVIA', '04 / FOUNDATION': '04 / BASE', '05 / FOUNDATION': '05 / BASE', '06 / FOUNDATION': '06 / BASE',
    'More sources, another perspective.': 'Más fuentes, otra perspectiva.', 'Explore 445 public profile sites and search for similar images.': 'Explora 445 sitios con perfiles públicos y busca imágenes similares.',
    'The optional username search now checks 445 sites and APIs, with clear statuses for uncertain or blocked results.': 'La búsqueda opcional por usuario ahora comprueba 445 sitios y API, con estados claros para respuestas inciertas o bloqueadas.',
    'Search a public image URL using Google Lens or TinEye, or upload a file directly on an external service.': 'Busca una URL pública de imagen con Google Lens o TinEye, o sube un archivo directamente a un servicio externo.',
    'Search a public image URL using Google Lens or TinEye, or send a photo directly to Google Lens.': 'Busca una URL pública de imagen con Google Lens o TinEye, o envía una foto directamente a Google Lens.',
    'The interface now switches between English and Spanish, with the preference saved in your browser.': 'La interfaz ahora permite alternar entre inglés y español y guarda la preferencia en tu navegador.',
    'The Media page now offers TON as the only donation method.': 'La página de medios ahora ofrece TON como único método de donación.', 'Image matches and usernames do not prove identity; verify results independently.': 'Las imágenes o usuarios coincidentes no prueban la identidad; verifica los resultados de forma independiente.',
    'TON donations were added; the former Monobank option was later removed.': 'Se añadieron donaciones con TON; la antigua opción de Monobank se eliminó posteriormente.',
    'More places to find a username.': 'Más lugares para buscar un nombre de usuario.',
    'The people workspace can now check 198 public profile sites in one optional search.': 'El espacio de personas incorporó una búsqueda opcional en 198 sitios con perfiles públicos.',
    'Search social networks, creator platforms, communities, and developer sites, including Telegram, Instagram, and TikTok.': 'Busca en redes sociales, plataformas de creadores, comunidades y sitios de desarrolladores, como Telegram, Instagram y TikTok.',
    'Unverified, blocked, or unavailable responses are distinguished from confirmed profile indicators; open the links to check them yourself.': 'Las respuestas no verificadas, bloqueadas o no disponibles se distinguen de los indicadores de perfil; abre los enlaces para comprobarlos.',
    'The expanded search is optional, and existing sources, history, graph, and exports remain available.': 'La búsqueda ampliada es opcional y las fuentes, el historial, el grafo y las exportaciones existentes siguen disponibles.', 'Matching usernames do not establish that accounts belong to the same person.': 'La coincidencia de usuarios no demuestra que las cuentas pertenezcan a la misma persona.',
    'A clearer signal.': 'Una señal más clara.', 'A monochrome workspace with optional accounts and new ways to support the project.': 'Un espacio monocromo con cuentas opcionales y nuevas formas de apoyar el proyecto.',
    'A new homepage presents the project and its workspaces.': 'Una nueva página de inicio presenta el proyecto y sus espacios.', 'A minimal black-and-white design across the site.': 'Un diseño minimalista en blanco y negro en todo el sitio.',
    'Sign in or create an account; registered accounts are stored in a database and managed in an access-controlled administrator area.': 'Inicia sesión o crea una cuenta; las cuentas se guardan en una base de datos y se gestionan desde un área de administración con control de acceso.',
    'Passwords are stored as salted Argon2id hashes, and administrator access is checked on the server.': 'Las contraseñas se almacenan como hashes Argon2id con sal y el acceso de administrador se comprueba en el servidor.',
    'Support Signal directly with TON from the Media page, alongside the existing Monobank donation link.': 'Se añadió el apoyo con TON desde la página de medios junto a la antigua opción de Monobank.',
    'Choose your language. Explore the dark.': 'Elige tu idioma. Explora la oscuridad.', 'A more focused interface and a new way to follow the project.': 'Una interfaz más enfocada y una nueva forma de seguir el proyecto.',
    'Switch between English and Russian from the top of the site. Your preference stays in your browser.': 'En esa versión se podía cambiar entre inglés y ruso. La preferencia se guardaba en el navegador.',
    'A darker, terminal-inspired visual style across the workspaces.': 'Un estilo visual oscuro inspirado en terminales en los espacios de trabajo.', "This update log keeps the project's changes in one place.": 'Este registro reúne los cambios del proyecto en un solo lugar.',
    'More sources. More context.': 'Más fuentes. Más contexto.', 'The people-search workspace received clearer controls and additional public sources.': 'El espacio de búsqueda de personas recibió controles más claros y fuentes públicas adicionales.',
    'Bluesky, Mastodon.social, and Wikidata were added to the source selection.': 'Se añadieron Bluesky, Mastodon.social y Wikidata a la selección de fuentes.',
    'Source presets, status filtering, and improved graph prioritization make results easier to explore.': 'Los conjuntos de fuentes, el filtro de estado y la prioridad del grafo facilitan la exploración de resultados.',
    'The Media page now links to the Signal Telegram channel and donation jar.': 'La página de medios incorporó enlaces al canal de Telegram y a la antigua opción de donaciones.',
    'The Signal workspace.': 'El espacio de trabajo Signal.', 'Public-source people searches and passive website investigations in one place.': 'Búsqueda de personas en fuentes públicas e investigación pasiva de sitios en un solo lugar.',
    'Explore results using relationship graphs and manual search links.': 'Explora los resultados con grafos de relaciones y enlaces de búsqueda manual.', 'Save and compare browser history, and export reports in supported formats.': 'Guarda y compara el historial del navegador y exporta informes en los formatos compatibles.',
    'Results are not identity verification or a full security audit. Verify sources independently.': 'Los resultados no verifican la identidad ni son una auditoría de seguridad completa. Verifica las fuentes de forma independiente.', 'New entries will appear here as the project is updated.': 'Las nuevas entradas aparecerán aquí conforme se actualice el proyecto.',
    'SIGNAL / ACCOUNT': 'SIGNAL / CUENTA', 'Your account.': 'Tu cuenta.', 'Sign in or create an account. The public workspaces remain available without signing in.': 'Inicia sesión o crea una cuenta. Los espacios públicos siguen disponibles sin iniciar sesión.',
    'JavaScript is required to use accounts.': 'Se necesita JavaScript para usar las cuentas.', 'Account access': 'Acceso a la cuenta', 'Sign in': 'Iniciar sesión', 'Create account': 'Crear cuenta', 'PASSWORD': 'CONTRASEÑA', 'CONFIRM PASSWORD': 'CONFIRMAR CONTRASEÑA',
    '3–32 Latin letters, numbers, dots, underscores or hyphens.': 'De 3 a 32 letras latinas, números, puntos, guiones bajos o guiones.', 'Use a unique password of 10–128 characters.': 'Usa una contraseña única de 10 a 128 caracteres.',
    'SIGNED IN': 'SESIÓN INICIADA', 'Administrator': 'Administrador', 'Member': 'Miembro', 'Sign out': 'Cerrar sesión', 'Open admin panel': 'Abrir panel de administración',
    'Change password': 'Cambiar contraseña', 'Changing your password signs you out on all devices.': 'Al cambiar la contraseña se cerrará la sesión en todos los dispositivos.', 'CURRENT PASSWORD': 'CONTRASEÑA ACTUAL', 'NEW PASSWORD': 'NUEVA CONTRASEÑA', 'CONFIRM NEW PASSWORD': 'CONFIRMAR NUEVA CONTRASEÑA', 'Update password': 'Actualizar contraseña',
    'ACCOUNT SECURITY / 01': 'SEGURIDAD DE LA CUENTA / 01', 'Keep your access private.': 'Mantén privado tu acceso.',
    'Passwords are stored as salted Argon2id hashes, not as readable text. Do not reuse passwords or share them with anyone.': 'Las contraseñas se almacenan como hashes Argon2id con sal, no como texto legible. No reutilices ni compartas contraseñas.',
    'Accounts are optional. Search history still stays in your browser unless you choose to save it.': 'Las cuentas son opcionales. El historial de búsqueda solo se guarda en tu navegador si eliges guardarlo.', 'There is currently no automated password recovery. Keep your password safe.': 'Actualmente no hay recuperación automática de contraseñas. Guárdala de forma segura.',
    'SIGNAL / ADMINISTRATION': 'SIGNAL / ADMINISTRACIÓN', 'Account oversight.': 'Gestión de cuentas.', 'Review registered accounts and manage access. Passwords and password hashes are never shown here.': 'Revisa las cuentas registradas y administra el acceso. Las contraseñas y sus hashes nunca se muestran aquí.',
    '← Back to account': '← Volver a la cuenta', 'Registered accounts': 'Cuentas registradas', 'Loading accounts…': 'Cargando cuentas…', 'Refresh': 'Actualizar', 'Active': 'Activa', 'Disable': 'Desactivar', 'Enable': 'Activar', 'Protected': 'Protegida',
    'Showing up to 200 accounts. Administrator accounts cannot be disabled here.': 'Se muestran hasta 200 cuentas. Las cuentas de administrador no pueden desactivarse aquí.', 'Authorized access only.': 'Solo acceso autorizado.',
    'Disable this account? Its sessions will be signed out.': '¿Desactivar esta cuenta? Sus sesiones se cerrarán.', 'Enable this account?': '¿Activar esta cuenta?',
    'Passwords do not match.': 'Las contraseñas no coinciden.', 'Unexpected server response.': 'Respuesta inesperada del servidor.', 'Account service is unavailable.': 'El servicio de cuentas no está disponible.',
    'Accounts are not configured or temporarily unavailable.': 'Las cuentas no están configuradas o no están disponibles temporalmente.', 'Account access requires HTTPS.': 'El acceso a la cuenta requiere HTTPS.',
    'Username must be 3–32 Latin letters, numbers, dots, underscores or hyphens, starting with a letter or number.': 'El usuario debe tener de 3 a 32 letras latinas, números, puntos, guiones bajos o guiones, y comenzar con una letra o número.',
    'Password must be 10–128 characters long.': 'La contraseña debe tener entre 10 y 128 caracteres.', 'Password contains invalid characters.': 'La contraseña contiene caracteres no válidos.', 'Enter a valid username.': 'Introduce un usuario válido.',
    'This username is already in use.': 'Este usuario ya está en uso.', 'Invalid username or password.': 'Usuario o contraseña incorrectos.', 'Too many attempts. Please try again later.': 'Demasiados intentos. Inténtalo más tarde.',
    'Account service is busy. Please try again.': 'El servicio de cuentas está ocupado. Inténtalo de nuevo.', 'Please sign in first.': 'Inicia sesión primero.', 'Your session could not be verified. Refresh and try again.': 'No se pudo verificar tu sesión. Actualiza e inténtalo de nuevo.',
    'Current password is incorrect.': 'La contraseña actual es incorrecta.', 'Choose a different new password.': 'Elige una nueva contraseña diferente.', 'Password changed. Sign in again.': 'Contraseña cambiada. Vuelve a iniciar sesión.', 'Account changed. Please sign in again.': 'La cuenta cambió. Vuelve a iniciar sesión.',
    'Invalid account request.': 'Solicitud de cuenta no válida.', 'Account not found or cannot be changed.': 'No se encontró la cuenta o no se puede modificar.', 'Account is unavailable.': 'La cuenta no está disponible.', 'An internal account error occurred.': 'Se produjo un error interno de la cuenta.',
    'Expected a JSON request.': 'Se esperaba una solicitud JSON.', 'Invalid request origin.': 'Origen de solicitud no válido.', 'Account | Signal OSINT': 'Cuenta | Signal OSINT', 'Administration | Signal OSINT': 'Administración | Signal OSINT',
    'Capabilities': 'Funciones', 'How it works': 'Cómo funciona', 'Responsible use': 'Uso responsable', 'Open workspace': 'Abrir espacio de trabajo',
    'WEB INTELLIGENCE STARTS HERE': 'LA INTELIGENCIA WEB COMIENZA AQUÍ', 'Gather the facts.': 'Reúne los datos.', 'See the connections.': 'Descubre las conexiones.',
    'Public website data, its digital footprint, and connections in one clear workspace.': 'Datos públicos de sitios web, su huella digital y sus conexiones en un solo espacio.',
    'Enter a domain, e.g. example.org': 'Introduce un dominio, p. ej., example.org', 'Website domain': 'Dominio del sitio web', 'Investigate': 'Investigar', 'Public data only. Do not include passwords or tokens in the address.': 'Solo datos públicos. No incluyas contraseñas ni tokens en la dirección.',
    '20 analysis modules': '20 módulos de análisis', 'Visual graph': 'Grafo visual', 'Export reports': 'Exportar informes', 'Example relationship graph': 'Ejemplo de grafo de relaciones', 'Example relationship map': 'Ejemplo de mapa de relaciones',
    'Example map: domain connected to IP, TLS, DNS, and public sources': 'Mapa de ejemplo: dominio conectado a IP, TLS, DNS y fuentes públicas', 'YOUR DOMAIN': 'TU DOMINIO', 'IP addresses': 'Direcciones IP', 'Sources': 'Fuentes', 'Connections from public sources': 'Conexiones de fuentes públicas', 'EXAMPLE, NOT LIVE DATA': 'EJEMPLO, NO SON DATOS REALES',
    'search and analysis modules': 'módulos de búsqueda y análisis', 'workspace for results': 'espacio para resultados', 'public website data': 'datos públicos de sitios web', 'interactive relationship map': 'mapa interactivo de relaciones',
    'CAPABILITIES / 01': 'FUNCIONES / 01', 'The bigger picture,': 'Todo el contexto,', 'in one place.': 'en un solo lugar.', 'From technical profiles to external sources, Signal helps organize data and reveal context.': 'Desde perfiles técnicos hasta fuentes externas, Signal ayuda a organizar los datos y descubrir el contexto.',
    'Website profile': 'Perfil del sitio web', 'DNS, HTTP, TLS, technologies, headers, links, forms, and other data from the requested page.': 'DNS, HTTP, TLS, tecnologías, cabeceras, enlaces, formularios y otros datos de la página solicitada.',
    '20 MODULES': '20 MÓDULOS', 'Explore relationships between domains, addresses, resources, and discovered names.': 'Explora las relaciones entre dominios, direcciones, recursos y nombres encontrados.', 'INTERACTIVE MAP': 'MAPA INTERACTIVO',
    'Compare investigations of the same domain and save results as JSON, Markdown, or SVG.': 'Compara investigaciones del mismo dominio y guarda resultados en JSON, Markdown o SVG.', 'EXPORT RESULTS': 'EXPORTAR RESULTADOS',
    'More public sources': 'Más fuentes públicas', 'Optionally add Certificate Transparency, RDAP data, and the Wayback Machine archive. Each external source is enabled separately.': 'Añade opcionalmente Certificate Transparency, datos RDAP y Wayback Machine. Cada fuente externa se activa por separado.',
    'Under your control': 'Bajo tu control', 'History is stored in your browser. Third-party sources are used only when selected.': 'El historial se guarda en tu navegador. Las fuentes externas se usan solo al seleccionarlas.',
    'HOW IT WORKS / 02': 'CÓMO FUNCIONA / 02', 'From domain': 'Del dominio', 'to understanding.': 'a la comprensión.', 'No complicated setup: enter a target and choose the sources you want to use.': 'Sin configuraciones complicadas: introduce un objetivo y elige las fuentes.',
    'Enter an address': 'Introduce una dirección', 'Enter a public domain or page address you have permission to investigate.': 'Introduce un dominio público o una dirección que estés autorizado a investigar.', 'Explore the data': 'Explora los datos', 'Modules collect available information and show missing data or errors.': 'Los módulos recopilan información y muestran datos ausentes o errores.',
    'See connections': 'Ver conexiones', 'Open the graph, compare previous results, and save a report.': 'Abre el grafo, compara resultados anteriores y guarda un informe.', 'Investigate responsibly.': 'Investiga con responsabilidad.',
    'Signal uses public data and is not a full security audit. Use it only within your authorization.': 'Signal usa datos públicos y no es una auditoría de seguridad completa. Úsalo solo dentro de tus autorizaciones.', 'Passive website analysis': 'Análisis pasivo de sitios web', 'Open investigation': 'Abrir investigación',
    'History is stored in the browser. When enabled, external sources receive the address.': 'El historial se guarda en el navegador. Al activarlas, las fuentes externas reciben la dirección.',
    'Browser storage is unavailable. Open the workspace and enter the address there.': 'El almacenamiento del navegador no está disponible. Abre el espacio e introduce allí la dirección.',
    'Run a search first.': 'Ejecuta una búsqueda primero.', 'Run an investigation first.': 'Ejecuta una investigación primero.', 'Delete saved people-search history in this browser?': '¿Eliminar el historial de búsqueda de personas de este navegador?', 'Delete all local investigation history?': '¿Eliminar todo el historial local de investigaciones?',
    'Enter a username, name or ORCID iD.': 'Introduce un usuario, nombre u ORCID iD.', 'Enter a valid ORCID iD.': 'Introduce un ORCID iD válido.', 'ORCID must have 16 characters, for example 0000-0002-1825-0097.': 'El ORCID debe tener 16 caracteres, por ejemplo 0000-0002-1825-0097.', 'The ORCID check digit is invalid.': 'El dígito de control del ORCID no es válido.',
    'Use up to 39 Latin letters, numbers, dots, hyphens or underscores for the username; do not enter a URL or email address.': 'Usa hasta 39 letras latinas, números, puntos, guiones o guiones bajos para el usuario; no introduzcas una URL ni correo electrónico.',
    'Names may contain letters, spaces, hyphens and apostrophes, up to 100 characters.': 'Los nombres pueden contener letras, espacios, guiones y apóstrofes, hasta 100 caracteres.', 'Context may contain letters, numbers, spaces, dots and hyphens, up to 80 characters.': 'El contexto puede contener letras, números, espacios, puntos y guiones, hasta 80 caracteres.',
    'An unknown source was selected.': 'Se seleccionó una fuente desconocida.', 'Select at least one source that matches the information you entered.': 'Selecciona al menos una fuente adecuada para los datos introducidos.',
    'Enter a full HTTPS link to a public profile.': 'Introduce un enlace HTTPS completo a un perfil público.', 'Use an HTTPS link without credentials or a nonstandard port.': 'Usa un enlace HTTPS sin credenciales ni puerto no estándar.',
    'Use a supported GitHub, GitLab, DEV, Hacker News, Bluesky handle, or Mastodon.social profile link.': 'Usa un enlace compatible de GitHub, GitLab, DEV, Hacker News, Bluesky o Mastodon.social.',
    'Use a supported GitHub, GitLab, DEV, Hacker News, Bluesky, Mastodon.social, Instagram, TikTok, or Telegram profile link.': 'Usa un enlace compatible de GitHub, GitLab, DEV, Hacker News, Bluesky, Mastodon.social, Instagram, TikTok o Telegram.',
    'Enter a supported public profile link.': 'Introduce un enlace de perfil público compatible.', 'Enter a profile link.': 'Introduce un enlace de perfil.', 'Enter an ORCID iD or an https://orcid.org/... link.': 'Introduce un ORCID iD o un enlace https://orcid.org/...',
    'The username and profile URL do not match. Correct one of them.': 'El usuario y la URL del perfil no coinciden. Corrige uno de ellos.', 'Server error': 'Error del servidor', 'Unexpected server response': 'Respuesta inesperada del servidor', 'Unexpected response format': 'Formato de respuesta inesperado',
    'Search completed, but history could not be saved in this browser.': 'Búsqueda completada, pero no se pudo guardar el historial en este navegador.', 'Investigation completed, but history could not be saved in this browser.': 'Investigación completada, pero no se pudo guardar el historial en este navegador.',
    'Invalid host or request origin.': 'Servidor u origen de solicitud no válido.', 'Check the request format and size.': 'Comprueba el formato y tamaño de la solicitud.', 'The server is busy. Please try again in a few seconds.': 'El servidor está ocupado. Inténtalo de nuevo en unos segundos.',
    'The shared investigation limit has been reached. Please try again later.': 'Se alcanzó el límite compartido de investigaciones. Inténtalo más tarde.', 'An internal error occurred. Check your input and try again.': 'Se produjo un error interno. Comprueba los datos e inténtalo de nuevo.',
    'The source response exceeded the size limit.': 'La respuesta de la fuente superó el límite de tamaño.', 'The source returned an unsupported content encoding.': 'La fuente devolvió una codificación no compatible.',
    'Enter a domain or address up to 2048 characters long.': 'Introduce un dominio o dirección de hasta 2048 caracteres.', 'The address contains invalid characters.': 'La dirección contiene caracteres no válidos.',
    'Only ports 80 and 443 are allowed.': 'Solo se permiten los puertos 80 y 443.', 'Enter a valid public HTTP(S) address without credentials.': 'Introduce una dirección HTTP(S) pública válida sin credenciales.', 'Only public IP addresses are allowed. Local and mixed DNS responses are blocked.': 'Solo se permiten IP públicas. Se bloquean las respuestas DNS locales y mixtas.',
    'Collecting data…': 'Recopilando datos…', 'Signal — explore the open web': 'Signal — explora la web abierta', 'Signal OSINT — website intelligence': 'Signal OSINT — inteligencia web', 'SIGNAL / People OSINT': 'SIGNAL / Búsqueda de personas',
    'Media & Support | Signal OSINT': 'Medios y apoyo | Signal OSINT', 'Updates | Signal OSINT': 'Actualizaciones | Signal OSINT', 'Signal OSINT — open-source intelligence': 'Signal OSINT — inteligencia de fuentes abiertas',
    'HOME': 'INICIO', 'Find the signal in': 'Encuentra la señal en', 'public data.': 'datos públicos.', 'SIGNAL / 00 ─ OVERVIEW': 'SIGNAL / 00 ─ RESUMEN', 'Find the signal in public data.': 'Encuentra la señal en los datos públicos.',
    'Signal OSINT is a workspace for responsible open-source research. Look up public profiles by username, name, or ORCID iD, investigate websites without touching them, and export structured reports. All results come from public sources.': 'Signal OSINT es un espacio para investigar responsablemente fuentes abiertas. Busca perfiles públicos por usuario, nombre u ORCID iD, investiga sitios y exporta informes estructurados. Los resultados proceden de fuentes públicas.',
    'Start people search': 'Iniciar búsqueda de personas', 'Investigate a website': 'Investigar un sitio web', '03 / PRINCIPLES': '03 / PRINCIPIOS', 'Find public profiles.': 'Encuentra perfiles públicos.',
    'Search by username, full name, or ORCID iD across more than a dozen public sources, then explore the connections in an interactive graph.': 'Busca por usuario, nombre completo u ORCID iD en fuentes públicas y explora las conexiones en un grafo interactivo.',
    'GitHub, GitLab, Wikipedia, Bluesky, Mastodon, and more': 'GitHub, GitLab, Wikipedia, Bluesky, Mastodon y más', 'Manual search links for search engines': 'Enlaces manuales para buscadores', 'Local history with JSON and Markdown exports': 'Historial local con exportación JSON y Markdown', 'Open the workspace': 'Abrir el espacio de trabajo',
    'Investigate websites passively.': 'Investiga sitios web de forma pasiva.', 'Enter an address and Signal checks DNS, HTTP, TLS, security headers, links, technology hints, and public metadata in a few bounded requests.': 'Introduce una dirección y Signal comprobará DNS, HTTP, TLS, cabeceras, enlaces, tecnologías y metadatos públicos mediante solicitudes limitadas.',
    '20 modules, from DNS to sitemap': '20 módulos, desde DNS hasta sitemap', 'Relationship graph and saved history': 'Grafo de relaciones e historial guardado', 'JSON, Markdown, and SVG exports': 'Exportación JSON, Markdown y SVG', 'Public sources only.': 'Solo fuentes públicas.',
    'Signal does not search leaked databases, test passwords, or exploit anything. A result is a hint, never a proof of identity or of safety.': 'Signal no busca datos filtrados, prueba contraseñas ni explota vulnerabilidades. Un resultado es una pista, no una prueba de identidad ni seguridad.',
    'No leaked data, scanning, or exploitation': 'Sin datos filtrados, escaneo ni explotación', 'Verify every finding independently': 'Verifica cada hallazgo de forma independiente', 'Respect the law and privacy': 'Respeta la ley y la privacidad', 'See what changed': 'Ver los cambios',
    'HOW IT WORKS': 'CÓMO FUNCIONA', 'Choose a workspace': 'Elige un espacio de trabajo', 'Open People to search profiles or Sites to inspect an address. No account is required for either.': 'Abre Personas para buscar perfiles o Sitios para inspeccionar una dirección. No se necesita cuenta.',
    'Review the evidence': 'Revisa las pruebas', 'Filter results, open the source links, explore the relationship graph, and compare saved searches.': 'Filtra resultados, abre las fuentes, explora el grafo y compara búsquedas guardadas.',
    'Export and verify': 'Exporta y verifica', 'Download JSON, Markdown, or SVG, then confirm your findings through independent sources. Accounts stay optional.': 'Descarga JSON, Markdown o SVG y confirma los hallazgos con fuentes independientes. Las cuentas son opcionales.',
    'Follow and support Signal.': 'Sigue y apoya a Signal.', 'News, updates, and donations live on the Media page. The public workspaces stay free.': 'Noticias, novedades y donaciones en la página de medios. Los espacios públicos siguen siendo gratuitos.', 'Media and support': 'Medios y apoyo',
    '03 / REVERSE IMAGE SEARCH': '03 / BÚSQUEDA INVERSA DE IMÁGENES', 'Find pages with the same or similar image using Google Lens or TinEye. Results do not identify a person.': 'Busca páginas con imágenes iguales o similares usando Google Lens o TinEye. Los resultados no identifican a una persona.',
    'PUBLIC IMAGE URL': 'URL PÚBLICA DE LA IMAGEN', 'Use a public image link without passwords or private tokens. The selected service receives this URL when opened.': 'Usa un enlace público de imagen sin contraseñas ni tokens privados. El servicio seleccionado recibe la URL al abrirlo.',
    'PREPARE IMAGE SEARCH': 'PREPARAR BÚSQUEDA DE IMAGEN', 'PHOTO FROM DEVICE': 'FOTO DEL DISPOSITIVO',
    'When you press the button, the image is sent directly to Google Lens. Signal does not receive or store the file.': 'Al pulsar el botón, la imagen se envía directamente a Google Lens. Signal no recibe ni guarda el archivo.',
    'SEARCH PHOTO WITH GOOGLE LENS': 'BUSCAR FOTO CON GOOGLE LENS', 'Choose a JPG, PNG, WebP, or GIF image up to 10 MB.': 'Elige una imagen JPG, PNG, WebP o GIF de hasta 10 MB.',
    'Opening Google Lens. The selected image is sent directly to Google.': 'Abriendo Google Lens. La imagen seleccionada se envía directamente a Google.',
    'You can also open a service below and upload a photo there yourself.': 'También puedes abrir un servicio y subir allí una foto.',
    'External services have their own privacy policies and may store images or URLs. Search only images you have permission to use.': 'Los servicios externos tienen sus propias políticas de privacidad y pueden guardar imágenes o URL. Busca solo imágenes que estés autorizado a usar.',
    'Links are ready. Open a service to run the search.': 'Los enlaces están listos. Abre un servicio para iniciar la búsqueda.', 'Enter a valid public HTTP or HTTPS image URL without credentials.': 'Introduce una URL pública de imagen HTTP o HTTPS válida, sin credenciales.',
  };

  const patterns = [
    [/^(\d+) sources? selected · (\d+) applicable to the current input$/, (_, a, b) => `${a} fuentes seleccionadas · ${b} aplicables a los datos introducidos`],
    [/^MODULES: (\d+) \/ PUBLIC SOURCE DATA$/, (_, n) => `MÓDULOS: ${n} / DATOS DE FUENTES PÚBLICAS`],
    [/^UPDATED: (.+)$/, (_, date) => `ACTUALIZADO: ${date}`], [/^CHANGED: (\d+)$/, (_, n) => `CAMBIADOS: ${n}`], [/^CHANGES: (\d+)$/, (_, n) => `CAMBIOS: ${n}`],
    [/^Comparison: (.+)$/, (_, host) => `Comparación: ${host}`], [/^Investigation time: ([\d.]+) s$/, (_, n) => `Tiempo de investigación: ${n} s`],
    [/^\/ (\d+) modules$/, (_, n) => `/ ${n} módulos`], [/^\+ more (\d+) modules$/, (_, n) => `+ ${n} módulos más`],
    [/^Format: (\+\d+)\nThe basic format check passed\. The number, carrier, and owner are not verified\.$/, (_, n) => `Formato: ${n}\nLa comprobación básica del formato ha terminado. El número, la operadora y el propietario no están verificados.`],
    [/^Showing (\d+) public (repositories|organizations), up to 20\. The list may be incomplete\.$/, (_, n, type) => `Se muestran ${n} ${type === 'repositories' ? 'repositorios' : 'organizaciones'} públicos, hasta 20. La lista puede estar incompleta.`],
    [/^Found (\d+) articles\. Namesakes and unrelated results are possible\.$/, (_, n) => `Se encontraron ${n} artículos. Puede haber homónimos y resultados no relacionados.`],
    [/^Found (\d+) entities\. Results can include unrelated people or subjects\.$/, (_, n) => `Se encontraron ${n} entidades. Pueden incluir personas o temas no relacionados.`],
    [/^Found (\d+) display-name results\. This is a search, not identity verification\.$/, (_, n) => `Se encontraron ${n} resultados por nombre visible. Es una búsqueda, no una verificación de identidad.`],
    [/^Found (\d+) author-name results\. Unrelated matches are possible\.$/, (_, n) => `Se encontraron ${n} resultados por nombre de autor. Puede haber coincidencias no relacionadas.`],
    [/^Prepared (\d+) links\. Search engines were not queried; open and verify the results yourself\.$/, (_, n) => `Se prepararon ${n} enlaces. No se consultaron buscadores; abre y verifica los resultados.`],
    [/^No public profile was found for (.+)\. Other Bluesky domains were not checked\.$/, (_, handle) => `No se encontró un perfil público para ${handle}. No se comprobaron otros dominios de Bluesky.`],
    [/^System DNS returned (\d+) public addresses\.$/, (_, n) => `El DNS del sistema devolvió ${n} direcciones públicas.`],
    [/^HTTP (\d+); response time (\d+) ms\.$/, (_, code, ms) => `HTTP ${code}; tiempo de respuesta ${ms} ms.`],
    [/^Found (\d+) of (\d+) headers\. Missing headers do not always indicate a vulnerability\.$/, (_, a, b) => `Se encontraron ${a} de ${b} cabeceras. Su ausencia no siempre indica una vulnerabilidad.`],
    [/^Found (\d+) Set-Cookie headers\. Values are not stored\.$/, (_, n) => `Se encontraron ${n} cabeceras Set-Cookie. No se almacenan sus valores.`],
    [/^Found (\d+) clues\. Data may be incomplete or misleading\.$/, (_, n) => `Se encontraron ${n} indicios. Los datos pueden estar incompletos o ser engañosos.`],
    [/^Links: (\d+); external: (\d+)\. Additional pages were not visited\.$/, (_, a, b) => `Enlaces: ${a}; externos: ${b}. No se visitaron otras páginas.`],
    [/^Forms on page: (\d+)\. Forms are not submitted; field values are not saved\.$/, (_, n) => `Formularios en la página: ${n}. No se envían formularios ni se guardan los valores.`],
    [/^HTML resources: (\d+); external domains: (\d+)\. Resources were not loaded\.$/, (_, a, b) => `Recursos HTML: ${a}; dominios externos: ${b}. No se cargaron recursos.`],
    [/^Found (\d+) names in public certificates \(up to 100\)\. Their current existence is not confirmed\.$/, (_, n) => `Se encontraron ${n} nombres en certificados públicos (hasta 100). No se confirma su existencia actual.`],
    [/^HTTP (\d+|no response); (\d+) directives recognized\.$/, (_, code, n) => `HTTP ${code === 'no response' ? 'sin respuesta' : code}; ${n} directivas reconocidas.`],
    [/^HTTP (\d+|no response); file unavailable or not recognized\.$/, (_, code) => `HTTP ${code === 'no response' ? 'sin respuesta' : code}; archivo no disponible o no reconocido.`],
    [/^\/sitemap\.xml: HTTP (\d+|no response); (\d+) links read \(up to 100\)\.$/, (_, code, n) => `/sitemap.xml: HTTP ${code === 'no response' ? 'sin respuesta' : code}; ${n} enlaces leídos (hasta 100).`],
    [/^\/sitemap\.xml: HTTP (\d+|no response); XML is unavailable, invalid or exceeds the limit\.$/, (_, code) => `/sitemap.xml: HTTP ${code === 'no response' ? 'sin respuesta' : code}; XML no disponible, no válido o superior al límite.`],
    [/^\/\.well-known\/security\.txt: HTTP (\d+|no response); (\d+) fields recognized\.$/, (_, code, n) => `/.well-known/security.txt: HTTP ${code === 'no response' ? 'sin respuesta' : code}; ${n} campos reconocidos.`],
    [/^\/\.well-known\/security\.txt: HTTP (\d+|no response); file not found or not recognized\.$/, (_, code) => `/.well-known/security.txt: HTTP ${code === 'no response' ? 'sin respuesta' : code}; archivo no encontrado o no reconocido.`],
    [/^Source returned HTTP (\d+)( \(possibly rate-limited\))?$/, (_, code, limited) => `La fuente devolvió HTTP ${code}${limited ? ' (posible límite de solicitudes)' : ''}`],
    [/^(.+) · (username|name)( \(sign-in may be required\))?$/, (_, service, tag, login) => `${service} · ${tag === 'username' ? 'usuario' : 'nombre'}${login ? ' (puede requerir inicio de sesión)' : ''}`],
    [/^Search query · search query$/, () => 'Consulta de búsqueda · consulta de búsqueda'], [/^(.+) · (search query|profile|repository|organization|article)$/, (_, label, kind) => `${label} · ${es[kind]}`],
    [/^(ERROR \/ |Investigation failed: |Source unavailable: |Request failed: |Could not resolve the domain via DNS: |Could not reach the source: )([\s\S]+)$/, (_, prefix, detail) => ({'ERROR / ': 'ERROR / ', 'Investigation failed: ': 'Falló la investigación: ', 'Source unavailable: ': 'Fuente no disponible: ', 'Request failed: ': 'Falló la solicitud: ', 'Could not resolve the domain via DNS: ': 'No se pudo resolver el dominio mediante DNS: ', 'Could not reach the source: ': 'No se pudo acceder a la fuente: '}[prefix] + translate(detail))],
    [/^(.*) · Search result; identity is not confirmed\.$/, (_, description) => `${description} · Resultado de búsqueda; identidad no confirmada.`],
    [/^Reputation: (.+) · identity is not confirmed$/, (_, n) => `Reputación: ${n} · identidad no confirmada`], [/^DOI: (.+) · authorship is not confirmed by a name match$/, (_, doi) => `DOI: ${doi} · la coincidencia de nombre no confirma la autoría`],
    [/^★ (\d+) · language not specified$/, (_, n) => `★ ${n} · idioma no especificado`], [/^(.+) · status$/, (_, title) => `${translate(title)} · estado`], [/^Form (\d+)$/, (_, n) => `Formulario ${n}`], [/^Total accounts: (\d+)$/, (_, n) => `Cuentas totales: ${n}`]
  ];

  function translate(value) {
    const raw = String(value == null ? '' : value);
    const parts = raw.match(/^(\s*)([\s\S]*?)(\s*)$/);
    if (!parts || !parts[2]) return raw;
    const lead = parts[1], trail = parts[3];
    const text = parts[2].replace(/\u00a0/g, ' ').replace(/[ \t]+/g, ' ');
    if (Object.prototype.hasOwnProperty.call(es, text)) return lead + es[text] + trail;
    for (const [pattern, render] of patterns) {
      const match = text.match(pattern);
      if (match) return lead + render(...match) + trail;
    }
    // Keep visual icons and arrows while translating their adjacent label.
    const decorated = text.match(/^([◉◈⌘◇◷●◎✧]\s+)?(.+?)(\s*[↗↓→])?$/);
    if (decorated && Object.prototype.hasOwnProperty.call(es, decorated[2])) {
      return lead + (decorated[1] || '') + es[decorated[2]] + (decorated[3] || '') + trail;
    }
    return raw;
  }

  // Search filters can match both English labels and their Spanish translations
  // without changing the underlying results or stored reports.
  window.signalI18nText = translate;

  let language = 'en';
  try { if (localStorage.getItem('signal-language') === 'es') language = 'es'; } catch (e) { /* English remains available without storage. */ }

  function addNavigation() {
    const headerNav = document.querySelector('.header nav');
    if (headerNav && !headerNav.querySelector('a[href="/updates"]')) {
      const link = document.createElement('a');
      link.href = '/updates';
      link.textContent = headerNav.classList.contains('navigation') ? 'Updates' : 'UPDATES';
      headerNav.appendChild(link);
    }
    if (headerNav && !headerNav.querySelector('a[href="/account"]')) {
      const link = document.createElement('a');
      link.href = '/account'; link.className = 'account-link';
      link.textContent = headerNav.classList.contains('navigation') ? 'Account' : 'ACCOUNT';
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
    if (sidebar && !sidebar.querySelector('a[href="/account"]')) {
      const link = document.createElement('a');
      link.className = 'nav'; link.href = '/account'; link.setAttribute('aria-label', 'Account');
      link.innerHTML = '<span class="icon">◉</span><span class="nav-text">Account ↗</span>';
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
      const account = document.createElement('a');
      account.className = 'account-short'; account.href = '/account'; account.textContent = 'ACCOUNT';
      headerNav.parentElement.insertBefore(account, compact.nextSibling);
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
    const rendered = language === 'es' ? translate(state.source) : state.source;
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
      const rendered = language === 'es' ? translate(state.source) : state.source;
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
    document.title = language === 'es' ? translate(originalTitle) : originalTitle;
    switcher.textContent = language === 'en' ? 'ES' : 'EN';
    switcher.setAttribute('aria-label', language === 'en' ? 'Switch to Spanish' : 'Switch to English');
    switcher.title = language === 'en' ? 'Cambiar a español' : 'Switch to English';
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
  switcher.addEventListener('click', () => { language = language === 'en' ? 'es' : 'en'; updateLanguage(true); });
  window.addEventListener('storage', event => {
    if (event.key === 'signal-language') { language = event.newValue === 'es' ? 'es' : 'en'; updateLanguage(false); }
  });
  const nativeAlert = window.alert.bind(window), nativeConfirm = window.confirm.bind(window);
  window.alert = message => nativeAlert(language === 'es' ? translate(message) : message);
  window.confirm = message => nativeConfirm(language === 'es' ? translate(message) : message);
  updateLanguage(false);
})();

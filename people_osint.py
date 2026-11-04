"""Bounded searches of public account and encyclopaedia APIs."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
import re
from urllib.parse import quote, urlencode, urlsplit

from osint_engine import decode_body, fetch, parse_target, resolve_public, safe_text

SOURCES = {'github', 'gitlab', 'hackernews', 'devto', 'wikipedia', 'stackoverflow', 'crossref', 'orcid', 'bluesky', 'mastodon', 'wikidata', 'platforms'}
# Profile URLs are fixed templates, not arbitrary user-supplied addresses.
# A generic HTTP 200 alone is never treated as proof of a profile. The
# 'missing:' and 'found:' markers only apply to the named service. Some URL
# templates were checked against Sherlock's catalogue (see THIRD_PARTY_NOTICES).
PLATFORMS = (
    ('lichess', 'Lichess', 'https://lichess.org/api/user/{u}', 'status'),
    ('chess', 'Chess.com', 'https://api.chess.com/pub/player/{u}', 'status'),
    ('dockerhub', 'Docker Hub', 'https://hub.docker.com/v2/users/{u}/', 'status'),
    ('pypi', 'PyPI', 'https://pypi.org/user/{u}/', 'status'),
    ('npm', 'npm', 'https://www.npmjs.com/~{u}', 'status'),
    ('launchpad', 'Launchpad', 'https://api.launchpad.net/devel/~{u}', 'status'),
    ('keybase', 'Keybase', 'https://keybase.io/{u}', 'status'),
    ('codeberg', 'Codeberg', 'https://codeberg.org/api/v1/users/{u}', 'status'),
    ('sourcehut', 'Sourcehut', 'https://sr.ht/~{u}/', 'status'),
    ('reddit', 'Reddit', 'https://www.reddit.com/user/{u}/about.json', 'status'),
    ('steam', 'Steam', 'https://steamcommunity.com/id/{u}/', 'missing:The specified profile cannot be found'),
    ('telegram', 'Telegram', 'https://t.me/{u}', 'found:tgme_page_title'),
    ('instagram', 'Instagram', 'https://www.instagram.com/{u}/', 'status'),
    ('tiktok', 'TikTok', 'https://www.tiktok.com/@{u}', 'status'),
    ('x', 'X (Twitter)', 'https://x.com/{u}', 'status'),
    ('youtube', 'YouTube', 'https://www.youtube.com/@{u}', 'status'),
    ('facebook', 'Facebook', 'https://www.facebook.com/{u}', 'status'),
    ('twitch', 'Twitch', 'https://www.twitch.tv/{u}', 'status'),
    ('soundcloud', 'SoundCloud', 'https://soundcloud.com/{u}', 'status'),
    ('pinterest', 'Pinterest', 'https://www.pinterest.com/{u}/', 'status'),
    ('vk', 'VK', 'https://vk.com/{u}', 'missing:page not found|не найдена'),
    ('medium', 'Medium', 'https://medium.com/@{u}', 'status'),
    ('tumblr', 'Tumblr', 'https://{d}.tumblr.com', 'status'),
    ('deviantart', 'DeviantArt', 'https://www.deviantart.com/{u}', 'missing:Llama Not Found'),
    ('blogger', 'Blogger', 'https://{d}.blogspot.com', 'status'),
    ('wordpress', 'WordPress.com', 'https://{d}.wordpress.com', 'status'),
    ('behance', 'Behance', 'https://www.behance.net/{u}', 'status'),
    ('dribbble', 'Dribbble', 'https://dribbble.com/{u}', 'status'),
    ('flickr', 'Flickr', 'https://www.flickr.com/people/{u}', 'status'),
    ('vimeo', 'Vimeo', 'https://vimeo.com/{u}', 'status'),
    ('ghpages', 'GitHub Pages', 'https://{d}.github.io', 'status'),
    ('fandom', 'Fandom', 'https://www.fandom.com/u/{u}', 'status'),
    ('wattpad', 'Wattpad', 'https://www.wattpad.com/user/{u}', 'status'),
    ('codewars', 'Codewars', 'https://www.codewars.com/users/{u}', 'status'),
    ('leetcode', 'LeetCode', 'https://leetcode.com/{u}/', 'status'),
    ('kaggle', 'Kaggle', 'https://www.kaggle.com/{u}', 'status'),
    ('lastfm', 'Last.fm', 'https://www.last.fm/user/{u}', 'status'),
    ('letterboxd', 'Letterboxd', 'https://letterboxd.com/{u}', 'status'),
    ('myanimelist', 'MyAnimeList', 'https://myanimelist.net/profile/{u}', 'status'),
    ('mixcloud', 'Mixcloud', 'https://www.mixcloud.com/{u}', 'status'),
    ('bandcamp', 'Bandcamp', 'https://{d}.bandcamp.com', 'status'),
    ('itch', 'itch.io', 'https://{d}.itch.io', 'status'),
    ('gumroad', 'Gumroad', 'https://{d}.gumroad.com', 'status'),
    ('kofi', 'Ko-fi', 'https://ko-fi.com/{u}', 'status'),
    ('bmc', 'Buy Me a Coffee', 'https://buymeacoffee.com/{u}', 'status'),
    ('patreon', 'Patreon', 'https://www.patreon.com/{u}', 'status'),
    ('threads', 'Threads', 'https://www.threads.net/@{u}', 'status'),
    ('snapchat', 'Snapchat', 'https://www.snapchat.com/add/{u}', 'status'),
    # Additional social, creative, gaming, educational and developer services.
    ('linkedin', 'LinkedIn', 'https://www.linkedin.com/in/{u}', 'status'),
    ('9gag', '9GAG', 'https://9gag.com/u/{u}', 'status'),
    ('aboutme', 'About.me', 'https://about.me/{u}', 'status'),
    ('allmylinks', 'AllMyLinks', 'https://allmylinks.com/{u}', 'missing:Page not found'),
    ('linktree', 'Linktree', 'https://linktr.ee/{u}', 'status'),
    ('carrd', 'Carrd', 'https://{d}.carrd.co/', 'status'),
    ('clubhouse', 'Clubhouse', 'https://www.clubhouse.com/@{u}', 'status'),
    ('flipboard', 'Flipboard', 'https://flipboard.com/@{u}', 'status'),
    ('fosstodon', 'Fosstodon', 'https://fosstodon.org/@{u}', 'status'),
    ('pixelfed', 'Pixelfed.social', 'https://pixelfed.social/{u}/', 'status'),
    ('lemmyworld', 'Lemmy.world', 'https://lemmy.world/u/{u}', 'status'),
    ('giphy', 'GIPHY', 'https://giphy.com/{u}', 'status'),
    ('imgur', 'Imgur', 'https://imgur.com/user/{u}', 'status'),
    ('livejournal', 'LiveJournal', 'https://{d}.livejournal.com/', 'status'),
    ('myspace', 'Myspace', 'https://myspace.com/{u}', 'status'),
    ('disqus', 'Disqus', 'https://disqus.com/{u}', 'status'),
    ('spacehey', 'SpaceHey', 'https://spacehey.com/{u}', 'status'),
    ('kick', 'Kick', 'https://kick.com/{u}', 'status'),
    ('dailymotion', 'Dailymotion', 'https://www.dailymotion.com/{u}', 'status'),
    ('rumble', 'Rumble', 'https://rumble.com/user/{u}', 'status'),
    ('odysee', 'Odysee', 'https://odysee.com/@{u}', 'status'),
    ('trovo', 'Trovo', 'https://trovo.live/s/{u}/', 'status'),
    ('habr', 'Habr', 'https://habr.com/ru/users/{u}/', 'status'),
    ('habrcareer', 'Habr Career', 'https://career.habr.com/{u}', 'status'),
    ('pikabu', 'Pikabu', 'https://pikabu.ru/@{u}', 'status'),
    ('plurk', 'Plurk', 'https://www.plurk.com/{u}', 'status'),
    ('vero', 'Vero', 'https://vero.co/{u}', 'status'),
    ('vsco', 'VSCO', 'https://vsco.co/{u}', 'status'),
    ('newgrounds', 'Newgrounds', 'https://{d}.newgrounds.com/', 'status'),
    ('artstation', 'ArtStation', 'https://www.artstation.com/{u}', 'status'),
    ('sketchfab', 'Sketchfab', 'https://sketchfab.com/{u}', 'status'),
    ('cgtrader', 'CGTrader', 'https://www.cgtrader.com/{u}', 'status'),
    ('coroflot', 'Coroflot', 'https://www.coroflot.com/{u}', 'status'),
    ('cults3d', 'Cults3D', 'https://cults3d.com/en/users/{u}/creations', 'missing:Oh dear, this page is not working!'),
    ('myminifactory', 'MyMiniFactory', 'https://www.myminifactory.com/users/{u}', 'status'),
    ('redbubble', 'Redbubble', 'https://www.redbubble.com/people/{u}', 'status'),
    ('unsplash', 'Unsplash', 'https://unsplash.com/@{u}', 'status'),
    ('eyeem', 'EyeEm', 'https://www.eyeem.com/u/{u}', 'status'),
    ('youpic', 'YouPic', 'https://youpic.com/photographer/{u}/', 'status'),
    ('blipfoto', 'Blipfoto', 'https://www.blipfoto.com/{u}', 'status'),
    ('colourlovers', 'COLOURlovers', 'https://www.colourlovers.com/lover/{u}', 'status'),
    ('lottiefiles', 'LottieFiles', 'https://lottiefiles.com/{u}', 'status'),
    ('carbonmade', 'Carbonmade', 'https://{d}.carbonmade.com/', 'status'),
    ('crevado', 'Crevado', 'https://{d}.crevado.com/', 'status'),
    ('discogs', 'Discogs', 'https://www.discogs.com/user/{u}', 'status'),
    ('freesound', 'Freesound', 'https://freesound.org/people/{u}/', 'status'),
    ('musescore', 'MuseScore', 'https://musescore.com/{u}', 'status'),
    ('reverbnation', 'ReverbNation', 'https://www.reverbnation.com/{u}', 'status'),
    ('smule', 'Smule', 'https://www.smule.com/{u}', 'status'),
    ('splice', 'Splice', 'https://splice.com/{u}', 'status'),
    ('ultimate-guitar', 'Ultimate Guitar', 'https://ultimate-guitar.com/u/{u}', 'status'),
    ('rateyourmusic', 'Rate Your Music', 'https://rateyourmusic.com/~{u}', 'status'),
    ('airbit', 'Airbit', 'https://airbit.com/{u}', 'status'),
    ('archiveofourown', 'Archive of Our Own', 'https://archiveofourown.org/users/{u}', 'status'),
    ('archiveorg', 'Internet Archive', 'https://archive.org/details/@{u}', 'status'),
    ('bookcrossing', 'BookCrossing', 'https://www.bookcrossing.com/mybookshelf/{u}/', 'status'),
    ('librarything', 'LibraryThing', 'https://www.librarything.com/profile/{u}', "missing:This user doesn't exist"),
    ('goodreads', 'Goodreads', 'https://www.goodreads.com/{u}', 'status'),
    ('scribd', 'Scribd', 'https://www.scribd.com/{u}', 'status'),
    ('issuu', 'Issuu', 'https://issuu.com/{u}', 'status'),
    ('hubpages', 'HubPages', 'https://hubpages.com/@{u}', 'status'),
    ('substack', 'Substack', 'https://{d}.substack.com/', 'status'),
    ('writeas', 'Write.as', 'https://write.as/{u}', 'status'),
    ('note', 'note', 'https://note.com/{u}', 'status'),
    ('velog', 'Velog', 'https://velog.io/@{u}/posts', 'status'),
    ('anilist', 'AniList', 'https://anilist.co/user/{u}/', 'status'),
    ('mydramalist', 'MyDramaList', 'https://mydramalist.com/profile/{u}', 'status'),
    ('themoviedb', 'The Movie Database', 'https://www.themoviedb.org/u/{u}', 'status'),
    ('trakt', 'Trakt', 'https://trakt.tv/users/{u}', 'status'),
    ('boardgamegeek', 'BoardGameGeek', 'https://boardgamegeek.com/user/{u}', 'status'),
    ('gamefaqs', 'GameFAQs', 'https://gamefaqs.gamespot.com/community/{u}', 'status'),
    ('gamespot', 'GameSpot', 'https://www.gamespot.com/profile/{u}/', 'status'),
    ('giantbomb', 'Giant Bomb', 'https://www.giantbomb.com/profile/{u}/', 'status'),
    ('nintendolife', 'Nintendo Life', 'https://www.nintendolife.com/users/{u}', 'status'),
    ('kongregate', 'Kongregate', 'https://www.kongregate.com/accounts/{u}', 'status'),
    ('speedrun', 'Speedrun.com', 'https://www.speedrun.com/users/{u}', 'status'),
    ('psnprofiles', 'PSNProfiles', 'https://psnprofiles.com/{u}', 'status'),
    ('tetrio', 'TETR.IO', 'https://ch.tetr.io/u/{u}', 'status'),
    ('pokemonshowdown', 'Pokémon Showdown', 'https://pokemonshowdown.com/users/{u}', 'status'),
    ('starcitizen', 'Star Citizen', 'https://robertsspaceindustries.com/citizens/{u}', 'status'),
    ('typeracer', 'TypeRacer', 'https://data.typeracer.com/pit/profile?user={u}', 'status'),
    ('nitrotype', 'Nitro Type', 'https://www.nitrotype.com/racer/{u}', 'status'),
    ('openstreetmap', 'OpenStreetMap', 'https://www.openstreetmap.org/user/{u}', 'status'),
    ('duolingo', 'Duolingo', 'https://www.duolingo.com/profile/{u}', 'status'),
    ('memrise', 'Memrise', 'https://www.memrise.com/user/{u}/', 'status'),
    ('clozemaster', 'Clozemaster', 'https://www.clozemaster.com/players/{u}', 'missing:Oh no! Player not found.'),
    ('instructables', 'Instructables', 'https://www.instructables.com/member/{u}', 'status'),
    ('hackster', 'Hackster.io', 'https://www.hackster.io/{u}', 'status'),
    ('hackaday', 'Hackaday.io', 'https://hackaday.io/{u}', 'status'),
    ('scratch', 'Scratch', 'https://scratch.mit.edu/users/{u}/', 'status'),
    ('freecodecamp', 'freeCodeCamp', 'https://www.freecodecamp.org/{u}', 'status'),
    ('codecademy', 'Codecademy', 'https://www.codecademy.com/profiles/{u}', 'missing:This profile could not be found'),
    ('codeforces', 'Codeforces', 'https://codeforces.com/profile/{u}', 'status'),
    ('codechef', 'CodeChef', 'https://www.codechef.com/users/{u}', 'status'),
    ('atcoder', 'AtCoder', 'https://atcoder.jp/users/{u}', 'status'),
    ('dmoj', 'DMOJ', 'https://dmoj.ca/user/{u}', 'missing:No such user'),
    ('vjudge', 'VJudge', 'https://vjudge.net/user/{u}', 'status'),
    ('hackerrank', 'HackerRank', 'https://www.hackerrank.com/{u}', 'status'),
    ('hackerearth', 'HackerEarth', 'https://www.hackerearth.com/@{u}', 'status'),
    ('topcoder', 'Topcoder', 'https://profiles.topcoder.com/{u}/', 'status'),
    ('cssbattle', 'CSSBattle', 'https://cssbattle.dev/player/{u}', 'status'),
    ('replit', 'Replit', 'https://replit.com/@{u}', 'status'),
    ('codepen', 'CodePen', 'https://codepen.io/{u}', 'status'),
    ('codesandbox', 'CodeSandbox', 'https://codesandbox.io/u/{u}', 'status'),
    ('coderwall', 'Coderwall', 'https://coderwall.com/{u}', 'status'),
    ('huggingface', 'Hugging Face', 'https://huggingface.co/{u}', 'status'),
    ('bitbucket', 'Bitbucket', 'https://bitbucket.org/{u}/', 'status'),
    ('gitea', 'Gitea', 'https://gitea.com/{u}', 'status'),
    ('gitee', 'Gitee', 'https://gitee.com/{u}', 'status'),
    ('notabug', 'NotABug', 'https://notabug.org/{u}', 'status'),
    ('sourceforge', 'SourceForge', 'https://sourceforge.net/u/{u}/', 'status'),
    ('rubygems', 'RubyGems', 'https://rubygems.org/profiles/{u}', 'status'),
    ('packagist', 'Packagist', 'https://packagist.org/packages/{u}/', 'status'),
    ('gradle', 'Gradle Plugins', 'https://plugins.gradle.org/u/{u}', 'status'),
    ('wordpressorg', 'WordPress.org', 'https://profiles.wordpress.org/{u}/', 'status'),
    ('weblate', 'Weblate', 'https://hosted.weblate.org/user/{u}/', 'status'),
    ('crowdin', 'Crowdin', 'https://crowdin.com/profile/{u}', 'status'),
    ('asciinema', 'asciinema', 'https://asciinema.org/~{u}', 'status'),
    ('observable', 'Observable', 'https://observablehq.com/@{u}', 'status'),
    ('hackmd', 'HackMD', 'https://hackmd.io/@{u}', 'status'),
    ('hashnode', 'Hashnode', 'https://hashnode.com/@{u}', 'status'),
    ('devrant', 'devRant', 'https://devrant.com/users/{u}', 'status'),
    ('lobsters', 'Lobsters', 'https://lobste.rs/u/{u}', 'status'),
    ('slashdot', 'Slashdot', 'https://slashdot.org/~{u}', 'status'),
    ('laracasts', 'Laracasts', 'https://laracasts.com/@{u}', 'status'),
    ('wakatime', 'WakaTime', 'https://wakatime.com/@{u}', 'status'),
    ('hackerone', 'HackerOne', 'https://hackerone.com/{u}', 'status'),
    ('bugcrowd', 'Bugcrowd', 'https://bugcrowd.com/{u}', 'status'),
    ('tryhackme', 'TryHackMe', 'https://tryhackme.com/p/{u}', 'status'),
    ('cryptohack', 'CryptoHack', 'https://cryptohack.org/user/{u}/', 'status'),
    ('cyberdefenders', 'CyberDefenders', 'https://cyberdefenders.org/p/{u}', 'status'),
    ('freelancer', 'Freelancer', 'https://www.freelancer.com/u/{u}', 'status'),
    ('producthunt', 'Product Hunt', 'https://www.producthunt.com/@{u}', 'status'),
    ('opencollective', 'Open Collective', 'https://opencollective.com/{u}', 'status'),
    ('speakerdeck', 'Speaker Deck', 'https://speakerdeck.com/{u}', 'status'),
    ('slides', 'Slides', 'https://slides.com/{u}', 'status'),
    ('trello', 'Trello', 'https://trello.com/{u}', 'status'),
    ('credly', 'Credly', 'https://www.credly.com/users/{u}', 'status'),
    ('academia', 'Academia.edu', 'https://independent.academia.edu/{u}', 'status'),
    ('researchgate', 'ResearchGate', 'https://www.researchgate.net/profile/{u}', 'status'),
    ('arduino', 'Arduino Forum', 'https://forum.arduino.cc/u/{u}/summary', 'status'),
    ('pythonforum', 'Python.org Discussions', 'https://discuss.python.org/u/{u}/summary', 'status'),
    ('jupyter', 'Jupyter Community', 'https://discourse.jupyter.org/u/{u}/summary', 'status'),
    ('nextcloud', 'Nextcloud Forum', 'https://help.nextcloud.com/u/{u}/summary', 'status'),
    ('fedora', 'Ask Fedora', 'https://ask.fedoraproject.org/u/{u}', 'status'),
    ('bitwarden', 'Bitwarden Forum', 'https://community.bitwarden.com/u/{u}/summary', 'status'),
    ('brave', 'Brave Community', 'https://community.brave.com/u/{u}/', 'status'),
    ('cloudflare', 'Cloudflare Community', 'https://community.cloudflare.com/u/{u}', 'status'),
    ('joplin', 'Joplin Forum', 'https://discourse.joplinapp.org/u/{u}', 'status'),
    ('n8n', 'n8n Community', 'https://community.n8n.io/u/{u}/summary', 'status'),
    # More public profiles, communities, portfolios, and federated services.
    # The same cautious HTTP-200 and redirect handling applies to every site.
    ('appledev', 'Apple Developer Forums', 'https://developer.apple.com/forums/profile/{u}', 'status'),
    ('applecommunity', 'Apple Support Community', 'https://discussions.apple.com/profile/{u}', 'status'),
    ('airliners', 'Airliners.net', 'https://www.airliners.net/user/{u}/profile/photos', 'status'),
    ('aparat', 'Aparat', 'https://www.aparat.com/{u}/', 'status'),
    ('audiojungle', 'AudioJungle', 'https://audiojungle.net/user/{u}', 'status'),
    ('awsskills', 'AWS Skills Profile', 'https://skillsprofile.skillbuilder.aws/user/{u}/', 'status'),
    ('booth', 'BOOTH', 'https://{d}.booth.pm/', 'status'),
    ('biggerpockets', 'BiggerPockets', 'https://www.biggerpockets.com/users/{u}', 'status'),
    ('blitztactics', 'Blitz Tactics', 'https://blitztactics.com/{u}', 'status'),
    ('buzzfeed', 'BuzzFeed', 'https://www.buzzfeed.com/{u}', 'status'),
    ('cfxforum', 'Cfx.re Forum', 'https://forum.cfx.re/u/{u}/summary', 'status'),
    ('cnet', 'CNET', 'https://www.cnet.com/profiles/{u}/', 'status'),
    ('ctan', 'CTAN', 'https://ctan.org/author/{u}', 'status'),
    ('caddy', 'Caddy Community', 'https://caddy.community/u/{u}/summary', 'status'),
    ('cartalk', 'Car Talk Community', 'https://community.cartalk.com/u/{u}/summary', 'status'),
    ('championat', 'Championat', 'https://www.championat.com/user/{u}', 'status'),
    ('clapper', 'Clapper', 'https://clapperapp.com/{u}', 'status'),
    ('codersrank', 'CodersRank', 'https://profile.codersrank.io/user/{u}/', 'status'),
    ('codolio', 'Codolio', 'https://codolio.com/profile/{u}', 'status'),
    ('contently', 'Contently', 'https://{d}.contently.com/', 'status'),
    ('cplusplus', 'cplusplus.com', 'https://cplusplus.com/user/{u}', 'status'),
    ('cracked', 'Cracked', 'https://www.cracked.com/members/{u}/', 'status'),
    ('cryptomator', 'Cryptomator Forum', 'https://community.cryptomator.org/u/{u}', 'status'),
    ('dcinside', 'DCInside', 'https://gallog.dcinside.com/{u}', 'status'),
    ('dealabs', 'Dealabs', 'https://www.dealabs.com/profile/{u}', 'status'),
    ('digitalspy', 'Digital Spy Forum', 'https://forums.digitalspy.com/profile/{u}', 'status'),
    ('elastic', 'Elastic Community', 'https://discuss.elastic.co/u/{u}', 'status'),
    ('envato', 'Envato Forum', 'https://forums.envato.com/u/{u}', 'status'),
    ('exposure', 'Exposure', 'https://{d}.exposure.co/', 'status'),
    ('exophase', 'Exophase', 'https://www.exophase.com/user/{u}/', 'status'),
    ('fanpop', 'Fanpop', 'https://www.fanpop.com/fans/{u}', 'status'),
    ('flightradar', 'Flightradar24', 'https://my.flightradar24.com/{u}', 'status'),
    ('fortnitetracker', 'Fortnite Tracker', 'https://fortnitetracker.com/profile/all/{u}', 'status'),
    ('gnomegitlab', 'GNOME GitLab', 'https://gitlab.gnome.org/{u}', 'status'),
    ('gaiaonline', 'Gaia Online', 'https://www.gaiaonline.com/profiles/{u}', 'status'),
    ('geeksforgeeks', 'GeeksforGeeks', 'https://auth.geeksforgeeks.org/user/{u}', 'status'),
    ('genius', 'Genius', 'https://genius.com/{u}', 'status'),
    ('gitbook', 'GitBook', 'https://{d}.gitbook.io/', 'status'),
    ('warframe', 'Warframe Market', 'https://warframe.market/profile/{u}', 'status'),
    ('googleplay', 'Google Play Developers', 'https://play.google.com/store/apps/developer?id={u}', 'status'),
    ('grailed', 'Grailed', 'https://www.grailed.com/{u}', 'status'),
    ('hacktheboxforum', 'Hack The Box Forum', 'https://forum.hackthebox.com/u/{u}', 'status'),
    ('hackenproof', 'HackenProof', 'https://hackenproof.com/hackers/{u}', 'status'),
    ('hackersploit', 'HackerSploit Forum', 'https://forum.hackersploit.org/u/{u}', 'status'),
    ('harvardscholar', 'Harvard Scholar', 'https://scholar.harvard.edu/{u}', 'status'),
    ('hive', 'Hive Blog', 'https://hive.blog/@{u}', 'status'),
    ('holopin', 'Holopin', 'https://holopin.io/@{u}', 'status'),
    ('houzz', 'Houzz', 'https://houzz.com/user/{u}', 'status'),
    ('hubski', 'Hubski', 'https://hubski.com/user/{u}', 'status'),
    ('ifttt', 'IFTTT', 'https://www.ifttt.com/p/{u}', 'status'),
    ('ifunny', 'iFunny', 'https://ifunny.co/user/{u}', 'status'),
    ('ircgalleria', 'IRC-Galleria', 'https://irc-galleria.net/user/{u}', 'status'),
    ('icons8', 'Icons8 Community', 'https://community.icons8.com/u/{u}/summary', 'status'),
    ('imgup', 'ImgUp', 'https://imgup.cz/{u}', 'status'),
    ('imood', 'iMood', 'https://www.imood.com/users/{u}', 'status'),
    ('instapaper', 'Instapaper', 'https://www.instapaper.com/p/{u}', 'status'),
    ('intigriti', 'Intigriti', 'https://app.intigriti.com/profile/{u}', 'status'),
    ('ionic', 'Ionic Forum', 'https://forum.ionicframework.com/u/{u}', 'status'),
    ('itemfix', 'ItemFix', 'https://www.itemfix.com/c/{u}', 'status'),
    ('jellyfintranslate', 'Jellyfin Weblate', 'https://translate.jellyfin.org/user/{u}/', 'status'),
    ('jimdo', 'Jimdo', 'https://{d}.jimdosite.com/', 'status'),
    ('kaskus', 'Kaskus', 'https://www.kaskus.co.id/@{u}', 'status'),
    ('linuxorgru', 'Linux.org.ru', 'https://www.linux.org.ru/people/{u}/profile', 'status'),
    ('lesswrong', 'LessWrong', 'https://www.lesswrong.com/users/{u}', 'status'),
    ('linuxfr', 'LinuxFr.org', 'https://linuxfr.org/users/{u}', 'status'),
    ('listed', 'Listed', 'https://listed.to/@{u}', 'status'),
    ('mmorpg', 'MMORPG Forum', 'https://forums.mmorpg.com/profile/{u}', 'status'),
    ('monkeytype', 'Monkeytype', 'https://monkeytype.com/profile/{u}', 'status'),
    ('nativeinstruments', 'Native Instruments Community', 'https://community.native-instruments.com/profile/{u}', 'status'),
    ('namuwiki', 'NamuWiki', 'https://namu.wiki/w/%EC%82%AC%EC%9A%A9%EC%9E%90:{u}', 'status'),
    ('nationstates', 'NationStates', 'https://nationstates.net/nation={u}', 'status'),
    ('naver', 'Naver Blog', 'https://blog.naver.com/{u}', 'status'),
    ('needrom', 'Needrom', 'https://www.needrom.com/author/{u}/', 'status'),
    ('ninjakiwi', 'Ninja Kiwi', 'https://ninjakiwi.com/profile/{u}', 'status'),
    ('nothingcommunity', 'Nothing Community', 'https://nothing.community/u/{u}', 'status'),
    ('opengameart', 'OpenGameArt', 'https://opengameart.org/users/{u}', 'status'),
    ('opensourcecom', 'Opensource.com', 'https://opensource.com/users/{u}', 'status'),
    ('pastebin', 'Pastebin', 'https://pastebin.com/u/{u}', 'status'),
    ('pentesterlab', 'PentesterLab', 'https://pentesterlab.com/profile/{u}', 'status'),
    ('hotukdeals', 'HotUKDeals', 'https://www.hotukdeals.com/profile/{u}', 'status'),
    ('mydealz', 'mydealz', 'https://www.mydealz.de/profile/{u}', 'status'),
    ('chollometro', 'Chollometro', 'https://www.chollometro.com/profile/{u}', 'status'),
    ('peppernl', 'Pepper Netherlands', 'https://nl.pepper.com/profile/{u}', 'status'),
    ('pepperpl', 'Pepper Poland', 'https://www.pepper.pl/profile/{u}', 'status'),
    ('preisjaeger', 'Preisjäger', 'https://www.preisjaeger.at/profile/{u}', 'status'),
    ('promodescuentos', 'Promodescuentos', 'https://www.promodescuentos.com/profile/{u}', 'status'),
    ('pinkbike', 'Pinkbike', 'https://www.pinkbike.com/u/{u}/', 'status'),
    ('playstrategy', 'PlayStrategy', 'https://playstrategy.org/@/{u}', 'status'),
    ('polarsteps', 'Polarsteps', 'https://polarsteps.com/{u}', 'status'),
    ('polygon', 'Polygon', 'https://www.polygon.com/users/{u}', 'status'),
    ('polymart', 'Polymart', 'https://polymart.org/user/{u}', 'status'),
    ('pychess', 'PyChess', 'https://www.pychess.org/@/{u}', 'status'),
    ('rajce', 'Rajče', 'https://{d}.rajce.idnes.cz/', 'status'),
    ('rclone', 'Rclone Forum', 'https://forum.rclone.org/u/{u}', 'status'),
    ('realmeye', 'RealmEye', 'https://www.realmeye.com/player/{u}', 'status'),
    ('rubyforum', 'Ruby Forum', 'https://ruby-forum.com/u/{u}/summary', 'status'),
    ('runescape', 'RuneScape', 'https://apps.runescape.com/runemetrics/app/overview/player/{u}', 'status'),
    ('sbazar', 'Sbazar', 'https://www.sbazar.cz/{u}', 'status'),
    ('seoforum', 'SEO Forum', 'https://seoforum.com/@{u}', 'status'),
    ('shelf', 'Shelf', 'https://www.shelf.im/{u}', 'status'),
    ('signalforum', 'Signal Community', 'https://community.signalusers.org/u/{u}', 'status'),
    ('slant', 'Slant', 'https://www.slant.co/users/{u}', 'status'),
    ('slideshare', 'SlideShare', 'https://www.slideshare.net/{u}', 'status'),
    ('smugmug', 'SmugMug', 'https://{d}.smugmug.com/', 'status'),
    ('soop', 'SOOP', 'https://www.sooplive.co.kr/station/{u}', 'status'),
    ('soylentnews', 'SoylentNews', 'https://soylentnews.org/~{u}', 'status'),
    ('splitsio', 'Splits.io', 'https://splits.io/users/{u}', 'status'),
    ('sporcle', 'Sporcle', 'https://www.sporcle.com/user/{u}/people', 'status'),
    ('sportsru', 'Sports.ru', 'https://www.sports.ru/profile/{u}/', 'status'),
    ('spotify', 'Spotify', 'https://open.spotify.com/user/{u}', 'status'),
    ('statuscafe', 'Status Cafe', 'https://status.cafe/users/{u}', 'status'),
    ('sublimeforum', 'Sublime Forum', 'https://forum.sublimetext.com/u/{u}', 'status'),
    ('tiendanube', 'Tiendanube', 'https://{d}.mitiendanube.com/', 'status'),
    ('topmate', 'Topmate', 'https://topmate.io/{u}', 'status'),
    ('traktrain', 'TRAKTRAIN', 'https://traktrain.com/{u}', 'status'),
    ('tenor', 'Tenor', 'https://tenor.com/users/{u}', 'status'),
    ('themeforest', 'ThemeForest', 'https://themeforest.net/user/{u}', 'status'),
    ('tistory', 'Tistory', 'https://{d}.tistory.com/', 'status'),
    ('tradingview', 'TradingView', 'https://www.tradingview.com/u/{u}/', 'status'),
    ('trashbox', 'Trashbox', 'https://trashbox.ru/users/{u}', 'status'),
    ('traewelling', 'Träwelling', 'https://traewelling.de/@{u}', 'status'),
    ('tuna', 'Tuna by Voicemod', 'https://tuna.voicemod.net/user/{u}', 'status'),
    ('untappd', 'Untappd', 'https://untappd.com/user/{u}', 'status'),
    ('virustotal', 'VirusTotal', 'https://www.virustotal.com/gui/user/{u}', 'status'),
    ('vlr', 'VLR.gg', 'https://www.vlr.gg/user/{u}', 'status'),
    ('wicg', 'WICG Forum', 'https://discourse.wicg.io/u/{u}/summary', 'status'),
    ('warriorforum', 'Warrior Forum', 'https://www.warriorforum.com/members/{u}.html', 'status'),
    ('webnode', 'Webnode', 'https://{d}.webnode.cz/', 'status'),
    ('weebly', 'Weebly', 'https://{d}.weebly.com/', 'status'),
    ('windy', 'Windy Community', 'https://community.windy.com/user/{u}', 'status'),
    ('wix', 'Wix', 'https://{d}.wix.com/', 'status'),
    ('wolfram', 'Wolfram Community', 'https://community.wolfram.com/web/{u}/home', 'status'),
    ('wordnik', 'Wordnik', 'https://www.wordnik.com/users/{u}', 'status'),
    ('wykop', 'Wykop', 'https://www.wykop.pl/ludzie/{u}', 'status'),
    ('xboxgamertag', 'Xbox Gamertag', 'https://xboxgamertag.com/search/{u}', 'status'),
    ('younow', 'YouNow', 'https://www.younow.com/{u}/', 'status'),
    ('akniga', 'Akniga', 'https://akniga.org/profile/{u}', 'status'),
    ('dailykos', 'Daily Kos', 'https://www.dailykos.com/user/{u}', 'status'),
    ('drive2', 'Drive2', 'https://www.drive2.ru/users/{u}', 'status'),
    ('egpu', 'eGPU Forum', 'https://egpu.io/forums/profile/{u}/', 'status'),
    ('fixya', 'Fixya', 'https://www.fixya.com/users/{u}', 'status'),
    ('flru', 'FL.ru', 'https://www.fl.ru/users/{u}', 'status'),
    ('geocaching', 'Geocaching', 'https://www.geocaching.com/p/default.aspx?u={u}', 'status'),
    ('irecommend', 'iRecommend', 'https://irecommend.ru/users/{u}', 'status'),
    ('jeuxvideo', 'Jeuxvideo', 'https://www.jeuxvideo.com/profil/{u}', 'status'),
    ('kwork', 'Kwork', 'https://kwork.ru/user/{u}', 'status'),
    ('leasehackr', 'Leasehackr Forum', 'https://forum.leasehackr.com/u/{u}/summary/', 'status'),
    ('livelib', 'LiveLib', 'https://www.livelib.ru/reader/{u}', 'status'),
    ('mercadolivre', 'Mercado Livre', 'https://www.mercadolivre.com.br/perfil/{u}', 'status'),
    ('minds', 'Minds', 'https://www.minds.com/{u}/', 'status'),
    ('nairaland', 'Nairaland', 'https://www.nairaland.com/{u}', 'status'),
    ('omglol', 'omg.lol', 'https://{d}.omg.lol/', 'status'),
    ('opennet', 'OpenNET', 'https://www.opennet.ru/~{u}', 'status'),
    ('osu', 'osu!', 'https://osu.ppy.sh/users/{u}', 'status'),
    ('proghu', 'prog.hu', 'https://prog.hu/azonosito/info/{u}', 'status'),
    ('sessionize', 'Sessionize', 'https://sessionize.com/{u}', 'status'),
    ('toster', 'Q&A Habr', 'https://www.toster.ru/user/{u}/answers', 'status'),
    ('platzi', 'Platzi', 'https://platzi.com/p/{u}/', 'status'),
    ('wowhead', 'Wowhead', 'https://www.wowhead.com/user={u}', 'status'),
    ('wago', 'Wago Addons', 'https://addons.wago.io/user/{u}', 'status'),
    ('curseforge', 'CurseForge', 'https://www.curseforge.com/members/{u}/projects', 'status'),
    # Independent Discourse communities, queried on their own hosts.
    ('obsidianforum', 'Obsidian Forum', 'https://forum.obsidian.md/u/{u}/summary', 'status'),
    ('mozilla', 'Mozilla Discourse', 'https://discourse.mozilla.org/u/{u}/summary', 'status'),
    ('homeassistant', 'Home Assistant Community', 'https://community.home-assistant.io/u/{u}/summary', 'status'),
    ('openaicommunity', 'OpenAI Developer Community', 'https://community.openai.com/u/{u}/summary', 'status'),
    ('manjaro', 'Manjaro Forum', 'https://forum.manjaro.org/u/{u}/summary', 'status'),
    ('pytorch', 'PyTorch Forums', 'https://discuss.pytorch.org/u/{u}/summary', 'status'),
    ('huggingforum', 'Hugging Face Forums', 'https://discuss.huggingface.co/u/{u}/summary', 'status'),
    ('unrealforum', 'Unreal Engine Forums', 'https://forums.unrealengine.com/u/{u}/summary', 'status'),
    ('godotforum', 'Godot Forum', 'https://forum.godotengine.org/u/{u}/summary', 'status'),
    ('letsencrypt', "Let's Encrypt Community", 'https://community.letsencrypt.org/u/{u}/summary', 'status'),
    ('nixos', 'NixOS Discourse', 'https://discourse.nixos.org/u/{u}/summary', 'status'),
    ('kubernetes', 'Kubernetes Discuss', 'https://discuss.kubernetes.io/u/{u}/summary', 'status'),
    ('hashicorp', 'HashiCorp Discuss', 'https://discuss.hashicorp.com/u/{u}/summary', 'status'),
    ('grafana', 'Grafana Community', 'https://community.grafana.com/u/{u}/summary', 'status'),
    ('torforum', 'Tor Project Forum', 'https://forum.torproject.org/u/{u}/summary', 'status'),
    ('pixls', 'PIXLS.US', 'https://discuss.pixls.us/u/{u}/summary', 'status'),
    ('gnomediscourse', 'GNOME Discourse', 'https://discourse.gnome.org/u/{u}/summary', 'status'),
    ('ubuntu', 'Ubuntu Discourse', 'https://discourse.ubuntu.com/u/{u}/summary', 'status'),
    ('rails', 'Ruby on Rails Discussions', 'https://discuss.rubyonrails.org/u/{u}/summary', 'status'),
    ('rustforum', 'Rust Users Forum', 'https://users.rust-lang.org/u/{u}/summary', 'status'),
    ('discoursemeta', 'Discourse Meta', 'https://meta.discourse.org/u/{u}/summary', 'status'),
    ('blenderforum', 'Blender Artists', 'https://blenderartists.org/u/{u}/summary', 'status'),
    ('threejs', 'three.js Forum', 'https://discourse.threejs.org/u/{u}/summary', 'status'),
    ('processing', 'Processing Forum', 'https://discourse.processing.org/u/{u}/summary', 'status'),
    ('juliaforum', 'Julia Discourse', 'https://discourse.julialang.org/u/{u}/summary', 'status'),
    ('inkscape', 'Inkscape Forum', 'https://inkscape.org/forums/user/{u}/', 'status'),
    ('fedoraabout', 'Fedora Discussion', 'https://discussion.fedoraproject.org/u/{u}/summary', 'status'),
    ('matrixforum', 'Matrix Community', 'https://forum.matrix.org/u/{u}/summary', 'status'),
    ('dockerforum', 'Docker Community Forums', 'https://forums.docker.com/u/{u}/summary', 'status'),
    ('ocamlforum', 'OCaml Discuss', 'https://discuss.ocaml.org/u/{u}/summary', 'status'),
    ('elixirforum', 'Elixir Forum', 'https://elixirforum.com/u/{u}/summary', 'status'),
    ('netlifyforum', 'Netlify Support Forums', 'https://answers.netlify.com/u/{u}/summary', 'status'),
    ('flyforum', 'Fly.io Community', 'https://community.fly.io/u/{u}/summary', 'status'),
    ('djangoforum', 'Django Forum', 'https://forum.djangoproject.com/u/{u}/summary', 'status'),
    ('gitlabforum', 'GitLab Forum', 'https://forum.gitlab.com/u/{u}/summary', 'status'),
    ('openwrtforum', 'OpenWrt Forum', 'https://forum.openwrt.org/u/{u}/summary', 'status'),
    ('platformioforum', 'PlatformIO Community', 'https://community.platformio.org/u/{u}/summary', 'status'),
    ('tvmforum', 'Apache TVM Discuss', 'https://discuss.tvm.apache.org/u/{u}/summary', 'status'),
    ('cmakeforum', 'CMake Discourse', 'https://discourse.cmake.org/u/{u}/summary', 'status'),
    ('paraviewforum', 'ParaView Discourse', 'https://discourse.paraview.org/u/{u}/summary', 'status'),
    ('vtkforum', 'VTK Discourse', 'https://discourse.vtk.org/u/{u}/summary', 'status'),
    ('nvidiaforum', 'NVIDIA Developer Forums', 'https://forums.developer.nvidia.com/u/{u}/summary', 'status'),
    ('llvmforum', 'LLVM Discourse', 'https://discourse.llvm.org/u/{u}/summary', 'status'),
    ('osmcommunity', 'OpenStreetMap Community', 'https://community.openstreetmap.org/u/{u}/summary', 'status'),
    ('babylonforum', 'Babylon.js Forum', 'https://forum.babylonjs.com/u/{u}/summary', 'status'),
    ('plotlyforum', 'Plotly Community', 'https://community.plotly.com/u/{u}/summary', 'status'),
    ('streamlitforum', 'Streamlit Community', 'https://discuss.streamlit.io/u/{u}/summary', 'status'),
    ('neo4jforum', 'Neo4j Community', 'https://community.neo4j.com/u/{u}/summary', 'status'),
    ('yunohostforum', 'YunoHost Forum', 'https://forum.yunohost.org/u/{u}/summary', 'status'),
    ('flarumforum', 'Flarum Community', 'https://discuss.flarum.org/u/{u}', 'status'),
    ('mcneelforum', 'McNeel Forum', 'https://discourse.mcneel.com/u/{u}/summary', 'status'),
    ('syncthingforum', 'Syncthing Forum', 'https://forum.syncthing.net/u/{u}/summary', 'status'),
    ('duplicatiforum', 'Duplicati Forum', 'https://forum.duplicati.com/u/{u}/summary', 'status'),
    ('zorinforum', 'Zorin Forum', 'https://forum.zorin.com/u/{u}/summary', 'status'),
    ('endeavourforum', 'EndeavourOS Forum', 'https://forum.endeavouros.com/u/{u}/summary', 'status'),
    ('kdeforum', 'KDE Discuss', 'https://discuss.kde.org/u/{u}/summary', 'status'),
    ('hugoforum', 'Hugo Discourse', 'https://discourse.gohugo.io/u/{u}/summary', 'status'),
    ('rosforum', 'ROS Discourse', 'https://discourse.ros.org/u/{u}/summary', 'status'),
    ('ardourforum', 'Ardour Discourse', 'https://discourse.ardour.org/u/{u}/summary', 'status'),
    ('opensearchforum', 'OpenSearch Forum', 'https://forum.opensearch.org/u/{u}/summary', 'status'),
    ('tiddlywiki', 'TiddlyWiki Talk', 'https://talk.tiddlywiki.org/u/{u}/summary', 'status'),
    ('racketforum', 'Racket Discourse', 'https://racket.discourse.group/u/{u}/summary', 'status'),
    ('ansibleforum', 'Ansible Forum', 'https://forum.ansible.com/u/{u}/summary', 'status'),
    ('zigforum', 'Ziggit', 'https://ziggit.dev/u/{u}/summary', 'status'),
    # Federated servers are separate communities, not a search of all Mastodon.
    ('chaossocial', 'chaos.social', 'https://chaos.social/@{u}', 'status'),
    ('framapiaf', 'Framapiaf', 'https://framapiaf.org/@{u}', 'status'),
    ('mamot', 'Mamot', 'https://mamot.fr/@{u}', 'status'),
    ('programmingdev', 'programming.dev', 'https://programming.dev/u/{u}', 'status'),
    ('mastodoncloud', 'mastodon.cloud', 'https://mastodon.cloud/@{u}', 'status'),
    ('mastodonxyz', 'mastodon.xyz', 'https://mastodon.xyz/@{u}', 'status'),
    ('mstdnsocial', 'mstdn.social', 'https://mstdn.social/@{u}', 'status'),
    ('mstdnio', 'mstdn.io', 'https://mstdn.io/@{u}', 'status'),
    ('tchncs', 'social.tchncs.de', 'https://social.tchncs.de/@{u}', 'status'),
    ('mastodonline', 'mastodon.online', 'https://mastodon.online/@{u}', 'status'),
    ('mastodonworld', 'mastodon.world', 'https://mastodon.world/@{u}', 'status'),
    ('mastodonart', 'mastodon.art', 'https://mastodon.art/@{u}', 'status'),
    ('hachyderm', 'hachyderm.io', 'https://hachyderm.io/@{u}', 'status'),
    ('masto', 'mas.to', 'https://mas.to/@{u}', 'status'),
    ('techhub', 'techhub.social', 'https://techhub.social/@{u}', 'status'),
    ('infosecexchange', 'infosec.exchange', 'https://infosec.exchange/@{u}', 'status'),
    ('vivaldisocial', 'Vivaldi Social', 'https://social.vivaldi.net/@{u}', 'status'),
    ('mastodonuno', 'mastodon.uno', 'https://mastodon.uno/@{u}', 'status'),
    ('gamedevplace', 'Mastodon Gamedev', 'https://mastodon.gamedev.place/@{u}', 'status'),
    ('photogsocial', 'photog.social', 'https://photog.social/@{u}', 'status'),
    ('mastodonnl', 'mastodon.nl', 'https://mastodon.nl/@{u}', 'status'),
    ('mastodonau', 'mastodon.au', 'https://mastodon.au/@{u}', 'status'),
)
MAX_PLATFORMS = len(PLATFORMS)
PLATFORM_WORKERS = 40
PLATFORM_TIMEOUT = 3
PLATFORM_BODY_LIMIT = 128 * 1024
# When a documented public API returns an exact username, link to the human
# profile rather than exposing the API response (which can contain other data).
PROFILE_URLS = {
    'lichess': 'https://lichess.org/@/{u}',
    'chess': 'https://www.chess.com/member/{u}',
    'dockerhub': 'https://hub.docker.com/u/{u}/',
    'launchpad': 'https://launchpad.net/~{u}',
    'codeberg': 'https://codeberg.org/{u}',
    'reddit': 'https://www.reddit.com/user/{u}/',
    'mixcloud': 'https://www.mixcloud.com/{u}/',
}
# Each API must return one of these username fields, case-insensitively.
API_PROBES = {
    'lichess': ('https://lichess.org/api/user/{u}', ('username', 'id')),
    'chess': ('https://api.chess.com/pub/player/{u}', ('username',)),
    'dockerhub': ('https://hub.docker.com/v2/users/{u}/', ('username', 'orgname')),
    'launchpad': ('https://api.launchpad.net/devel/~{u}', ('name',)),
    'codeberg': ('https://codeberg.org/api/v1/users/{u}', ('login', 'username')),
    'reddit': ('https://www.reddit.com/user/{u}/about.json', ('data.name',)),
    'codewars': ('https://www.codewars.com/api/v1/users/{u}', ('username',)),
    'mixcloud': ('https://api.mixcloud.com/{u}/', ('username',)),
    'huggingface': ('https://huggingface.co/api/users/{u}/overview', ('user',)),
    'scratch': ('https://api.scratch.mit.edu/users/{u}', ('username',)),
    'gitea': ('https://gitea.com/api/v1/users/{u}', ('login', 'username')),
    'codeforces': ('https://codeforces.com/api/user.info?handles={u}', ('result.0.handle',)),
    'duolingo': ('https://www.duolingo.com/2017-06-30/users?username={u}', ('users.0.username',)),
    'tetrio': ('https://ch.tetr.io/api/users/{u}', ('data.username',)),
    'fosstodon': ('https://fosstodon.org/api/v1/accounts/lookup?acct={u}', ('acct',)),
    'arduino': ('https://forum.arduino.cc/u/{u}.json', ('user.username',)),
    'pythonforum': ('https://discuss.python.org/u/{u}.json', ('user.username',)),
    'jupyter': ('https://discourse.jupyter.org/u/{u}.json', ('user.username',)),
    'nextcloud': ('https://help.nextcloud.com/u/{u}.json', ('user.username',)),
    'fedora': ('https://ask.fedoraproject.org/u/{u}.json', ('user.username',)),
    'bitwarden': ('https://community.bitwarden.com/u/{u}.json', ('user.username',)),
    'brave': ('https://community.brave.com/u/{u}.json', ('user.username',)),
    'cloudflare': ('https://community.cloudflare.com/u/{u}.json', ('user.username',)),
    'joplin': ('https://discourse.joplinapp.org/u/{u}.json', ('user.username',)),
    'n8n': ('https://community.n8n.io/u/{u}.json', ('user.username',)),
}
# Discourse's public user endpoint provides a stronger signal than a generic
# profile page. Only the fixed, explicitly listed community hosts are used.
DISCOURSE_IDS = {
    'cfxforum', 'caddy', 'cartalk', 'cryptomator', 'elastic', 'envato',
    'hacktheboxforum', 'hackersploit', 'icons8', 'ionic', 'nothingcommunity',
    'rclone', 'rubyforum', 'signalforum', 'sublimeforum', 'wicg', 'leasehackr',
    'obsidianforum', 'mozilla', 'homeassistant', 'openaicommunity', 'manjaro',
    'pytorch', 'huggingforum', 'unrealforum', 'godotforum', 'letsencrypt',
    'nixos', 'kubernetes', 'hashicorp', 'grafana', 'torforum', 'pixls',
    'gnomediscourse', 'ubuntu', 'rails', 'rustforum', 'discoursemeta',
    'blenderforum', 'threejs', 'processing', 'juliaforum', 'fedoraabout',
    'matrixforum', 'dockerforum', 'ocamlforum', 'elixirforum', 'netlifyforum',
    'flyforum', 'djangoforum', 'gitlabforum', 'openwrtforum', 'platformioforum',
    'tvmforum', 'cmakeforum', 'paraviewforum', 'vtkforum', 'nvidiaforum',
    'llvmforum', 'osmcommunity', 'babylonforum', 'plotlyforum', 'streamlitforum',
    'neo4jforum', 'yunohostforum', 'mcneelforum', 'syncthingforum',
    'duplicatiforum', 'zorinforum', 'endeavourforum', 'kdeforum', 'hugoforum',
    'rosforum', 'ardourforum', 'opensearchforum', 'tiddlywiki', 'racketforum',
    'ansibleforum', 'zigforum',
}
MASTODON_IDS = {
    'chaossocial', 'framapiaf', 'mamot', 'mastodoncloud', 'mastodonxyz',
    'mstdnsocial', 'mstdnio', 'tchncs', 'mastodonline', 'mastodonworld',
    'mastodonart', 'hachyderm', 'masto', 'techhub', 'infosecexchange',
    'vivaldisocial', 'mastodonuno', 'gamedevplace', 'photogsocial',
    'mastodonnl', 'mastodonau',
}
for _ident, _title, _template, _probe in PLATFORMS:
    _host = urlsplit(_template).netloc
    if _ident in DISCOURSE_IDS:
        API_PROBES[_ident] = ('https://' + _host + '/u/{u}.json', ('user.username',))
    elif _ident in MASTODON_IDS:
        # Match acct, not just username: remote federated accounts must not be
        # mistaken for a local account on the queried server.
        API_PROBES[_ident] = ('https://' + _host + '/api/v1/accounts/lookup?acct={u}', ('acct',))
SUBDOMAIN_RE = re.compile(r'[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?\Z')
FOUND_RE = 'Profile found; a name match does not confirm identity.'
NONE_RE = 'No accessible public profile was found; a private or unavailable profile is still possible.'
UNCLEAR_RE = 'Could not verify the profile automatically; open the link and check it yourself.'
ERROR_RE = 'The service was unavailable or blocked the request; check the link manually.'
SKIP_RE = 'Skipped: this username cannot be used as a subdomain for this site.'
USERNAME_RE = re.compile(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,38}\Z')
SLUG_RE = re.compile(r'[A-Za-z0-9_.-]{1,100}\Z')
DOI_RE = re.compile(r'10\.[0-9]{4,9}/[-._;()/:+A-Z0-9]+\Z', re.I)


def normalize_orcid(value):
    if not isinstance(value, str):
        raise ValueError('Enter a valid ORCID iD.')
    value = value.strip()
    if not value:
        return ''
    if not re.fullmatch(r'(?:[0-9]{4}-){3}[0-9]{3}[0-9Xx]|[0-9]{15}[0-9Xx]', value):
        raise ValueError('ORCID must have 16 characters, for example 0000-0002-1825-0097.')
    digits = value.replace('-', '').upper()
    total = 0
    for digit in digits[:15]:
        total = (total + int(digit)) * 2
    check = (12 - total % 11) % 11
    if digits[-1] != ('X' if check == 10 else str(check)):
        raise ValueError('The ORCID check digit is invalid.')
    return '-'.join(digits[i:i + 4] for i in range(0, 16, 4))


def validate(username, name, sources, orcid='', context=''):
    if not isinstance(username, str) or not isinstance(name, str) or not isinstance(context, str):
        raise ValueError('Enter a username, name or ORCID iD.')
    username, name, context = username.strip(), name.strip(), ' '.join(context.split())
    if username.startswith('@'):
        username = username[1:]
    if username and not USERNAME_RE.fullmatch(username):
        raise ValueError('Use up to 39 Latin letters, numbers, dots, hyphens or underscores for the username; do not enter a URL or email address.')
    if len(name) > 100 or (name and (not any(c.isalpha() for c in name) or any(not (c.isalpha() or c.isspace() or c in "-.'’") for c in name))):
        raise ValueError('Names may contain letters, spaces, hyphens and apostrophes, up to 100 characters.')
    name = ' '.join(name.split())
    if len(context) > 80 or (context and any(not (c.isalnum() or c.isspace() or c in "-.'’") for c in context)):
        raise ValueError('Context may contain letters, numbers, spaces, dots and hyphens, up to 80 characters.')
    orcid = normalize_orcid(orcid)
    if not username and not name and not orcid:
        raise ValueError('Enter a username, name or ORCID iD.')
    if not isinstance(sources, list) or not all(isinstance(s, str) and s in SOURCES for s in sources):
        raise ValueError('An unknown source was selected.')
    sources = set(sources)
    account_sources = {'github', 'gitlab', 'hackernews', 'devto', 'bluesky', 'mastodon', 'platforms'}
    if not ((username and sources.intersection(account_sources)) or (name and sources.intersection({'wikipedia', 'crossref', 'wikidata'})) or ((username or name) and 'stackoverflow' in sources) or (orcid and 'orcid' in sources)):
        raise ValueError('Select at least one source that matches the information you entered.')
    return username, name, sources, orcid, context


def get_json(url):
    """URLs are assembled from fixed services; redirects are never followed."""
    try:
        target = parse_target(url)
        response = fetch(target, resolve_public(target['host']), target['path'], limit=512 * 1024, accept='application/json')
        if response['error']:
            return None, 'Could not reach the source: ' + response['error']
        if response['status'] == 404:
            return None, None
        if response['status'] == 400 and target['host'] == 'public.api.bsky.app':
            try:
                body = json.loads(response['body'].decode('utf-8'))
                if isinstance(body, dict) and body.get('message') == 'Profile not found':
                    return None, None
            except (ValueError, UnicodeError):
                pass
        if response['status'] != 200:
            return None, 'Source returned HTTP ' + str(response['status']) + (' (possibly rate-limited)' if response['status'] in (403, 429) else '')
        if response['truncated']:
            return None, 'The source response exceeded the size limit.'
        if response['headers'].get('content-encoding', '').lower() not in ('', 'identity'):
            return None, 'The source returned an unsupported content encoding.'
        return json.loads(response['body'].decode('utf-8')), None
    except (ValueError, OSError, UnicodeError, json.JSONDecodeError) as exc:
        return None, safe_text(exc, 220)


def card(id, title, status, summary, facts=(), links=(), items=()):
    return {'id': id, 'title': title, 'status': status, 'summary': safe_text(summary, 350),
            'facts': [{'label': safe_text(k, 90), 'value': safe_text(str(v), 400)} for k, v in facts if v is not None and v != ''],
            'links': list(links), 'items': list(items)}


def check_platform(platform, username):
    """Check one fixed public URL, without redirects or returning source content."""
    ident, _title, template, probe = platform
    if not USERNAME_RE.fullmatch(username):
        raise ValueError('Invalid username.')
    public_template = PROFILE_URLS.get(ident, template)
    api = API_PROBES.get(ident)
    probe_template = api[0] if api else template
    domain = username.lower()
    if ('{d}' in public_template or '{d}' in probe_template) and not SUBDOMAIN_RE.fullmatch(domain):
        return 'disabled', SKIP_RE, ''
    values = {'u': quote(username, safe=''), 'd': domain}
    profile_url = public_template.format(**values)
    try:
        target = parse_target(probe_template.format(**values))
        # Check every DNS answer before pinning the connection, then try at most
        # two addresses. A profile check never follows redirects or user links.
        addresses = resolve_public(target['host'])
        response = fetch(target, addresses[:2], target['path'], limit=PLATFORM_BODY_LIMIT,
                         accept='application/json' if api else 'text/html,application/xhtml+xml',
                         timeout=PLATFORM_TIMEOUT)
        status = response['status']
        if response['error']:
            return 'error', ERROR_RE, profile_url
        if status in (404, 410):
            return 'none', NONE_RE, profile_url
        if status != 200:
            return ('unverified' if status in (301, 302, 303, 307, 308) else 'error'), (
                UNCLEAR_RE if status in (301, 302, 303, 307, 308) else ERROR_RE), profile_url
        text = decode_body(response)
        if text is None:
            return 'unverified', UNCLEAR_RE, profile_url
        # A block page or partial response is not evidence of account existence.
        lowered = text.lower()
        if any(marker in lowered for marker in ('cf-chl-', 'just a moment...', 'access denied', 'verify you are human', 'captcha challenge')):
            return 'unverified', UNCLEAR_RE, profile_url
        if api:
            if response['truncated']:
                return 'unverified', UNCLEAR_RE, profile_url
            try:
                data = json.loads(text)
            except (ValueError, TypeError):
                return 'unverified', UNCLEAR_RE, profile_url
            for field in api[1]:
                value = data
                for part in field.split('.'):
                    if isinstance(value, dict):
                        value = value.get(part)
                    elif isinstance(value, list) and part.isdigit() and int(part) < len(value):
                        value = value[int(part)]
                    else:
                        value = None
                if isinstance(value, str) and value.casefold() == username.casefold():
                    return 'ok', FOUND_RE, profile_url
            if ident == 'duolingo' and isinstance(data, dict) and data.get('users') == []:
                return 'none', NONE_RE, profile_url
            return 'unverified', UNCLEAR_RE, profile_url
        if probe.startswith('found:') and probe[6:].lower() in lowered:
            return 'ok', FOUND_RE, profile_url
        if probe.startswith('missing:') and any(marker.lower() in lowered for marker in probe[8:].split('|')):
            return 'none', NONE_RE, profile_url
        # Many sites return a generic page for any username, including Telegram
        # personal contacts, login pages and JavaScript-only applications.
        return 'unverified', UNCLEAR_RE, profile_url
    except (ValueError, OSError, UnicodeError):
        return 'error', ERROR_RE, profile_url


def search_people(username='', name='', sources=None, orcid='', context=''):
    username, name, sources, orcid, context = validate(username, name, sources if sources is not None else [], orcid, context)
    q = quote(username, safe='')
    jobs = {}
    with ThreadPoolExecutor(max_workers=PLATFORM_WORKERS if username and 'platforms' in sources else 8) as pool:
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
        if username and 'mastodon' in sources:
            jobs['mastodon'] = pool.submit(get_json, 'https://mastodon.social/api/v1/accounts/lookup?' + urlencode({'acct': username}))
        bluesky_handle = (username if '.' in username else username + '.bsky.social').lower() if username else ''
        if username and 'bluesky' in sources and all(re.fullmatch(r'[a-z0-9](?:[a-z0-9-]*[a-z0-9])?', label) for label in bluesky_handle.split('.')):
            jobs['bluesky'] = pool.submit(get_json, 'https://public.api.bsky.app/xrpc/app.bsky.actor.getProfile?' + urlencode({'actor': bluesky_handle}))
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
        if name and 'wikidata' in sources:
            params = urlencode({'action': 'wbsearchentities', 'search': name, 'language': 'en', 'format': 'json', 'limit': 8})
            jobs['wikidata'] = pool.submit(get_json, 'https://www.wikidata.org/w/api.php?' + params)
        if username and 'platforms' in sources:
            for platform in PLATFORMS:
                jobs['platform:' + platform[0]] = pool.submit(check_platform, platform, username)
        results = {key: job.result() for key, job in jobs.items()}
    modules = []
    graph = {'nodes': [{'id': 'query', 'label': 'Search query', 'kind': 'query'}], 'edges': []}
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
        modules.append(card(id, title, 'error', 'Source unavailable: ' + err))

    github_node = 'query:username'
    if 'github' not in jobs:
        disabled('github', 'GitHub · profile', 'Select GitHub and enter a username.')
    else:
        data, err = results['github']
        if err:
            failure('github', 'GitHub · profile', err)
        elif isinstance(data, dict) and data.get('type') == 'User' and str(data.get('login', '')).casefold() == username.casefold():
            login = data['login']
            url = 'https://github.com/' + quote(login, safe='')
            modules.append(card('github', 'GitHub · profile', 'ok', 'A public profile with this exact username was found. Verify its identity independently.',
                                [('Display name', data.get('name')), ('Username', login), ('Company', data.get('company')),
                                 ('Public repositories', data.get('public_repos')), ('Followers', data.get('followers')),
                                 ('Following', data.get('following')), ('Created', data.get('created_at'))], [('Open GitHub', url)]))
            github_node = add_node('profile', 'GitHub / ' + login, url)
        else:
            modules.append(card('github', 'GitHub · profile', 'none', 'No accessible public profile with this exact username was found.'))

    for key, title, path in [('repos', 'GitHub · repositories', 'repositories'), ('orgs', 'GitHub · organizations', 'organizations')]:
        if key not in jobs:
            disabled(key, title, 'Select GitHub and enter a username.')
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
                detail = ('★ ' + str(entry.get('stargazers_count', 0)) + ' · ' + str(entry.get('language') or 'language not specified')) if key == 'repos' else 'Public organization'
                items.append({'title': safe_text(slug, 100), 'url': url, 'detail': safe_text(detail, 120)})
                add_node('repo' if key == 'repos' else 'org', slug, url, github_node)
            modules.append(card(key, title, 'ok' if items else 'none', f'Showing {len(items)} public {path}, up to 20. The list may be incomplete.', items=items))
        else:
            modules.append(card(key, title, 'none', 'No data found or the profile is unavailable.'))

    if 'gitlab' not in jobs:
        disabled('gitlab', 'GitLab · profile', 'Select GitLab and enter a username.')
    else:
        data, err = results['gitlab']
        match = next((x for x in data if isinstance(x, dict) and str(x.get('username', '')).casefold() == username.casefold()), None) if isinstance(data, list) else None
        if err:
            failure('gitlab', 'GitLab · profile', err)
        elif match:
            url = 'https://gitlab.com/' + quote(match['username'], safe='')
            modules.append(card('gitlab', 'GitLab · profile', 'ok', 'An exact public username was found. This does not establish a match with other profiles.',
                                [('Display name', match.get('name')), ('Username', match['username']), ('Status', match.get('state')), ('Created', match.get('created_at'))], [('Open GitLab', url)]))
            add_node('profile', 'GitLab / ' + match['username'], url)
        else:
            modules.append(card('gitlab', 'GitLab · profile', 'none', 'No accessible public profile with this exact username was found.'))

    if 'hackernews' not in jobs:
        disabled('hackernews', 'Hacker News · profile', 'Select Hacker News and enter a username.')
    else:
        data, err = results['hackernews']
        if err:
            failure('hackernews', 'Hacker News · profile', err)
        elif isinstance(data, dict) and str(data.get('id', '')).casefold() == username.casefold():
            url = 'https://news.ycombinator.com/user?' + urlencode({'id': data['id']})
            created = data.get('created')
            try:
                created = datetime.fromtimestamp(int(created), timezone.utc).date().isoformat() if created else None
            except (ValueError, OverflowError, OSError, TypeError):
                created = None
            modules.append(card('hackernews', 'Hacker News · profile', 'ok', 'A public profile with this exact username was found.',
                                [('Username', data['id']), ('Karma', data.get('karma')), ('Created', created)], [('Open Hacker News', url)]))
            add_node('profile', 'Hacker News / ' + data['id'], url)
        else:
            modules.append(card('hackernews', 'Hacker News · profile', 'none', 'No accessible public profile with this exact username was found.'))

    if 'devto' not in jobs:
        disabled('devto', 'DEV Community · profile', 'Select DEV Community and enter a username.')
    else:
        data, err = results['devto']
        if err:
            failure('devto', 'DEV Community · profile', err)
        elif isinstance(data, dict) and str(data.get('username', '')).casefold() == username.casefold():
            login = data['username']
            url = 'https://dev.to/' + quote(login, safe='')
            modules.append(card('devto', 'DEV Community · profile', 'ok', 'A public profile with this exact username was found.',
                                [('Display name', data.get('name')), ('Username', login)], [('Open DEV', url)]))
            add_node('profile', 'DEV / ' + login, url)
        else:
            modules.append(card('devto', 'DEV Community · profile', 'none', 'No accessible public profile with this exact username was found.'))

    if 'bluesky' not in jobs:
        disabled('bluesky', 'Bluesky · profile', 'Enter a compatible Bluesky handle or username and select Bluesky. A plain username is checked as username.bsky.social.')
    else:
        data, err = results['bluesky']
        if err:
            failure('bluesky', 'Bluesky · profile', err)
        elif isinstance(data, dict) and str(data.get('handle', '')).casefold() == bluesky_handle.casefold():
            handle = data['handle']
            url = 'https://bsky.app/profile/' + quote(handle, safe='.')
            modules.append(card('bluesky', 'Bluesky · profile', 'ok', 'An exact public Bluesky handle was found; verify the identity independently.',
                                [('Display name', data.get('displayName')), ('Handle', handle), ('Followers', data.get('followersCount'))], [('Open Bluesky', url)]))
            add_node('profile', 'Bluesky / ' + handle, url)
        else:
            modules.append(card('bluesky', 'Bluesky · profile', 'none', 'No public profile was found for ' + bluesky_handle + '. Other Bluesky domains were not checked.'))

    if 'mastodon' not in jobs:
        disabled('mastodon', 'Mastodon.social · profile', 'Select Mastodon.social and enter a username. Other Mastodon servers are not checked.')
    else:
        data, err = results['mastodon']
        if err:
            failure('mastodon', 'Mastodon.social · profile', err)
        elif isinstance(data, dict) and str(data.get('username', '')).casefold() == username.casefold() and str(data.get('acct', '')).casefold() == username.casefold():
            login = data['username']
            url = 'https://mastodon.social/@' + quote(login, safe='')
            modules.append(card('mastodon', 'Mastodon.social · profile', 'ok', 'A public profile with this exact username was found on mastodon.social only.',
                                [('Display name', data.get('display_name')), ('Username', login), ('Followers', data.get('followers_count'))], [('Open Mastodon', url)]))
            add_node('profile', 'Mastodon.social / ' + login, url)
        else:
            modules.append(card('mastodon', 'Mastodon.social · profile', 'none', 'No public profile was found on mastodon.social. Other servers were not checked.'))

    for lang, title in [('ru', 'Wikipedia · Russian'), ('en', 'Wikipedia · English')]:
        key = 'wiki_' + lang
        if key not in jobs:
            disabled(key, title, 'Select Wikipedia and enter a name.')
            continue
        data, err = results[key]
        if err:
            failure(key, title, err)
            continue
        if not isinstance(data, dict) or not isinstance(data.get('query'), dict) or not isinstance(data['query'].get('search'), list):
            modules.append(card(key, title, 'error', 'The source returned an unexpected response.'))
            continue
        items = []
        for item in data['query']['search'][:8]:
            if isinstance(item, dict) and isinstance(item.get('pageid'), int) and isinstance(item.get('title'), str):
                url = f'https://{lang}.wikipedia.org/?curid={item["pageid"]}'
                items.append({'title': safe_text(item['title'], 150), 'url': url, 'detail': 'Name search result; identity is not confirmed.'})
                add_node('article', item['title'], url, 'query:name')
        modules.append(card(key, title, 'ok' if items else 'none', f'Found {len(items)} articles. Namesakes and unrelated results are possible.', items=items))

    if 'wikidata' not in jobs:
        disabled('wikidata', 'Wikidata · entity search', 'Select Wikidata and enter a name.')
    else:
        data, err = results['wikidata']
        if err:
            failure('wikidata', 'Wikidata · entity search', err)
        elif not isinstance(data, dict) or not isinstance(data.get('search'), list):
            modules.append(card('wikidata', 'Wikidata · entity search', 'error', 'The source returned an unexpected response.'))
        else:
            items = []
            for item in data['search'][:8]:
                if not isinstance(item, dict):
                    continue
                ident, label = item.get('id'), item.get('label')
                if not isinstance(ident, str) or not re.fullmatch(r'Q[1-9][0-9]{0,18}', ident) or not isinstance(label, str):
                    continue
                url = 'https://www.wikidata.org/wiki/' + ident
                description = safe_text(item.get('description', ''), 120)
                items.append({'title': safe_text(label, 150), 'url': url,
                              'detail': (description + ' · ' if description else '') + 'Search result; identity is not confirmed.'})
                add_node('article', label, url, 'query:name')
            modules.append(card('wikidata', 'Wikidata · entity search', 'ok' if items else 'none',
                                f'Found {len(items)} entities. Results can include unrelated people or subjects.', items=items))

    if 'stackoverflow' not in jobs:
        disabled('stackoverflow', 'Stack Overflow · profile search', 'Select Stack Overflow and enter a name or username.')
    else:
        data, err = results['stackoverflow']
        if err:
            failure('stackoverflow', 'Stack Overflow · profile search', err)
        elif not isinstance(data, dict) or not isinstance(data.get('items'), list):
            modules.append(card('stackoverflow', 'Stack Overflow · profile search', 'error', 'The source returned an unexpected response.'))
        else:
            items = []
            for item in data['items'][:8]:
                if isinstance(item, dict) and isinstance(item.get('user_id'), int) and isinstance(item.get('display_name'), str):
                    url = 'https://stackoverflow.com/users/' + str(item['user_id'])
                    label = safe_text(item['display_name'], 150)
                    items.append({'title': label, 'url': url, 'detail': 'Reputation: ' + safe_text(str(item.get('reputation', '—')), 40) + ' · identity is not confirmed'})
                    add_node('profile', 'Stack Overflow / ' + label, url, 'query:name' if name else 'query:username')
            modules.append(card('stackoverflow', 'Stack Overflow · profile search', 'ok' if items else 'none', f'Found {len(items)} display-name results. This is a search, not identity verification.', items=items))

    if 'crossref' not in jobs:
        disabled('crossref', 'Crossref · publications', 'Select Crossref and enter a name.')
    else:
        data, err = results['crossref']
        message = data.get('message') if isinstance(data, dict) else None
        if err:
            failure('crossref', 'Crossref · publications', err)
        elif not isinstance(message, dict) or not isinstance(message.get('items'), list):
            modules.append(card('crossref', 'Crossref · publications', 'error', 'The source returned an unexpected response.'))
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
                items.append({'title': label, 'url': url, 'detail': 'DOI: ' + safe_text(doi, 140) + ' · authorship is not confirmed by a name match'})
                add_node('article', label, url, 'query:name')
            modules.append(card('crossref', 'Crossref · publications', 'ok' if items else 'none', f'Found {len(items)} author-name results. Unrelated matches are possible.', items=items))

    if 'orcid' not in jobs:
        disabled('orcid', 'ORCID · researcher', 'Select ORCID and enter a public ORCID iD.')
    else:
        data, err = results['orcid']
        if err:
            failure('orcid', 'ORCID · researcher', err)
        elif data is None:
            modules.append(card('orcid', 'ORCID · researcher', 'none', 'No accessible public record was found.'))
        elif not isinstance(data, dict):
            modules.append(card('orcid', 'ORCID · researcher', 'error', 'The source returned an unexpected response.'))
        else:
            person = data.get('name') if isinstance(data.get('name'), dict) else {}
            def field(key):
                entry = person.get(key)
                return entry.get('value') if isinstance(entry, dict) else None
            url = 'https://orcid.org/' + orcid
            modules.append(card('orcid', 'ORCID · researcher', 'ok', 'Public record for the supplied ORCID. This does not confirm a match with other results.',
                                [('ORCID', orcid), ('Given name', field('given-names')), ('Family name', field('family-name')), ('Credit name', field('credit-name'))], [('Open ORCID', url)]))
            add_node('profile', 'ORCID / ' + orcid, url, 'query:orcid')

    if username and 'platforms' in sources:
        for ident, title, _template, _probe in PLATFORMS:
            status, summary, url = results['platform:' + ident]
            modules.append(card('platform_' + ident, title, status, summary,
                                links=[('Open profile', url)] if url else ()))
            if status == 'ok':
                add_node('profile', title + ' / ' + username, url)

    manual = []
    for query, tag in ((username, 'username'), (name, 'name')):
        if not query:
            continue
        contextual_query = '"' + query + '"' + (' ' + context if context else '')
        manual.extend([
            ('Google · ' + tag, 'https://www.google.com/search?' + urlencode({'q': contextual_query})),
            ('Bing · ' + tag, 'https://www.bing.com/search?' + urlencode({'q': contextual_query})),
            ('DuckDuckGo · ' + tag, 'https://duckduckgo.com/?' + urlencode({'q': contextual_query})),
            ('YouTube · ' + tag, 'https://www.youtube.com/results?' + urlencode({'search_query': query})),
            ('GitHub search · ' + tag, 'https://github.com/search?' + urlencode({'q': query, 'type': 'users'})),
            ('Wikipedia · ' + tag, 'https://en.wikipedia.org/w/index.php?' + urlencode({'search': query})),
            ('Google Scholar · ' + tag, 'https://scholar.google.com/scholar?' + urlencode({'q': query})),
            ('Reddit · ' + tag, 'https://www.reddit.com/search/?' + urlencode({'q': query})),
            ('GitLab search · ' + tag, 'https://gitlab.com/search?' + urlencode({'search': query})),
            ('DEV search · ' + tag, 'https://dev.to/search?' + urlencode({'q': query})),
            ('LinkedIn · ' + tag + ' (sign-in may be required)', 'https://www.linkedin.com/search/results/people/?' + urlencode({'keywords': query})),
            ('ORCID search · ' + tag, 'https://orcid.org/orcid-search/search?' + urlencode({'searchQuery': query})),
            ('Crossref search · ' + tag, 'https://search.crossref.org/?' + urlencode({'q': query})),
            ('Stack Overflow search · ' + tag, 'https://stackoverflow.com/search?' + urlencode({'q': query})),
            ('Internet Archive · ' + tag, 'https://archive.org/search?' + urlencode({'query': query})),
        ])
    if orcid:
        manual.append(('Provided ORCID', 'https://orcid.org/' + orcid))
    modules.append(card('search_links', 'Search links', 'ready', f'Prepared {len(manual)} links. Search engines were not queried; open and verify the results yourself.'))
    # The UI displays only the first 35 nodes. Show query and source matches
    # before GitHub's potentially large repository/organization lists so that
    # one source does not crowd out every other source in the visible graph.
    node_priority = {'query': 0, 'profile': 1, 'article': 2, 'repo': 3, 'org': 3}
    graph['nodes'].sort(key=lambda node: node_priority.get(node['kind'], 4))
    return {'version': 1, 'username': username, 'name': name, 'orcid': orcid, 'context': context, 'scanned_at': datetime.now(timezone.utc).isoformat(),
            'sources': sorted(sources), 'modules': modules, 'graph': graph,
            'manual_links': [{'label': label, 'url': url} for label, url in manual],
            'notice': 'A matching username or name does not confirm identity. Sources may be incomplete or unavailable.'}

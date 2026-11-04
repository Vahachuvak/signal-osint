'use strict';

// These controls extend the existing workspace rather than replacing its search,
// history, exports, or graph. Only selected sources receive a query.
const sourceList = document.querySelector('.checks');
sourceList.insertAdjacentHTML('beforeend', `
  <label class="check"><input type="checkbox" name="source" value="bluesky" checked> Bluesky <small>API</small></label>
  <label class="check"><input type="checkbox" name="source" value="mastodon" checked> Mastodon.social <small>API</small></label>
  <label class="check"><input type="checkbox" name="source" value="wikidata" checked> Wikidata <small>API</small></label>
  <label class="check"><input type="checkbox" name="source" value="platforms"> 198 profile sites <small>OPTIONAL</small></label>`);
sourceList.insertAdjacentHTML('beforebegin', `
  <div class="source-presets" role="group" aria-label="Source selection">
    <button type="button" class="button" data-source-preset="all">All</button>
    <button type="button" class="button" data-source-preset="accounts">Profiles</button>
    <button type="button" class="button" data-source-preset="research">Research</button>
    <button type="button" class="button" data-source-preset="none">Clear</button>
  </div>`);
sourceList.insertAdjacentHTML('afterend', '<p class="source-count" id="source-count" aria-live="polite"></p><p class="source-count">The optional group sends the username to up to 198 sites and may take a minute. Blocked or uncertain results require manual verification.</p>');

const sourcePresets = {
  accounts: new Set(['github', 'gitlab', 'hackernews', 'devto', 'bluesky', 'mastodon', 'stackoverflow', 'platforms']),
  research: new Set(['wikipedia', 'wikidata', 'stackoverflow', 'crossref', 'orcid'])
};
const usernameSources = new Set(['github', 'gitlab', 'hackernews', 'devto', 'bluesky', 'mastodon', 'stackoverflow', 'platforms']);
const nameSources = new Set(['wikipedia', 'wikidata', 'stackoverflow', 'crossref']);
function updateSourceCount() {
  const selected = [...sourceList.querySelectorAll('input:checked')];
  const hasUsername = Boolean($('username').value.trim() || $('profile-url').value.trim());
  const hasName = Boolean($('person-name').value.trim());
  const hasOrcid = Boolean($('orcid').value.trim());
  const applicable = selected.filter(input =>
    (hasUsername && usernameSources.has(input.value)) ||
    (hasName && nameSources.has(input.value)) ||
    (hasOrcid && input.value === 'orcid'));
  $('source-count').textContent = `${selected.length} source${selected.length === 1 ? '' : 's'} selected · ${applicable.length} applicable to the current input`;
}
document.querySelectorAll('[data-source-preset]').forEach(button => {
  button.addEventListener('click', () => {
    const preset = button.dataset.sourcePreset;
    sourceList.querySelectorAll('input[name="source"]').forEach(input => {
      input.checked = preset === 'all' || (sourcePresets[preset] && sourcePresets[preset].has(input.value)) || false;
    });
    updateSourceCount();
  });
});
sourceList.addEventListener('change', updateSourceCount);
['username', 'person-name', 'orcid', 'profile-url'].forEach(id => $(id).addEventListener('input', updateSourceCount));
$('extract-profile').addEventListener('click', updateSourceCount);
updateSourceCount();
$('stat-modules').textContent = '15';

// Accept only known profile hosts. The supplied URL is parsed locally, never fetched.
profileUsername = function(value) {
  if (!value.trim()) return '';
  let u;
  try { u = new URL(value.trim()); } catch (e) { throw new Error('Enter a full HTTPS link to a public profile.'); }
  if (u.protocol !== 'https:' || u.username || u.password || (u.port && u.port !== '443')) {
    throw new Error('Use an HTTPS link without credentials or a nonstandard port.');
  }
  let name = '';
  const host = u.hostname.toLowerCase();
  const parts = u.pathname.split('/').filter(Boolean);
  if (['github.com', 'www.github.com', 'gitlab.com', 'www.gitlab.com', 'dev.to'].includes(host) && parts.length === 1) {
    name = parts[0];
  } else if (host === 'news.ycombinator.com' && /^\/user\/?$/.test(u.pathname)) {
    name = u.searchParams.get('id') || '';
  } else if (host === 'mastodon.social' && parts.length === 1 && parts[0].startsWith('@')) {
    name = parts[0].slice(1);
  } else if (host === 'bsky.app' && parts.length === 2 && parts[0] === 'profile') {
    name = parts[1];
  } else if (['instagram.com', 'www.instagram.com', 't.me', 'telegram.me'].includes(host) && parts.length === 1) {
    name = parts[0];
  } else if (['tiktok.com', 'www.tiktok.com'].includes(host) && parts.length === 1 && parts[0].startsWith('@')) {
    name = parts[0].slice(1);
  }
  if (!/^[A-Za-z0-9][A-Za-z0-9_.-]{0,38}$/.test(name)) {
    throw new Error('Use a supported GitHub, GitLab, DEV, Hacker News, Bluesky, Mastodon.social, Instagram, TikTok, or Telegram profile link.');
  }
  return name;
};
$('profile-url').parentElement.querySelector('.hint').textContent = 'Extracts a username from GitHub, GitLab, DEV, Hacker News, Bluesky, Mastodon.social, Instagram, TikTok, or Telegram. The link is not visited.';

// Keep the existing text filter and add a status filter without changing results.
statusText.unverified = 'UNVERIFIED';
const resultToolbar = $('filter').parentElement;
resultToolbar.insertAdjacentHTML('beforeend', '<label class="status-filter">Status <select id="result-status"><option value="">All statuses</option><option value="ok">Found</option><option value="unverified">Unverified</option><option value="none">No data</option><option value="error">Error</option><option value="disabled">Disabled</option><option value="ready">Ready</option></select></label>');
const originalDrawResults = drawResults;
drawResults = function() {
  originalDrawResults();
  const status = $('result-status').value;
  const cards = [...$('results').querySelectorAll('.card')];
  let visible = 0;
  for (const card of cards) {
    const show = !status || card.querySelector('.state').classList.contains(status);
    card.hidden = !show;
    if (show) visible++;
  }
  const previous = $('results').querySelector('.status-empty');
  if (previous) previous.remove();
  if (cards.length && !visible) $('results').insertAdjacentHTML('beforeend', '<div class="empty status-empty">No results match this status and text filter.</div>');
};
$('filter').oninput = drawResults;
$('result-status').addEventListener('change', drawResults);

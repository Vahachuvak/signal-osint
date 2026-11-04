'use strict';

// These controls extend the existing workspace rather than replacing its search,
// history, exports, or graph. Only selected sources receive a query.
const sourceList = document.querySelector('.checks');
sourceList.insertAdjacentHTML('beforeend', `
  <label class="check"><input type="checkbox" name="source" value="bluesky" checked> Bluesky <small>API</small></label>
  <label class="check"><input type="checkbox" name="source" value="mastodon" checked> Mastodon.social <small>API</small></label>
  <label class="check"><input type="checkbox" name="source" value="wikidata" checked> Wikidata <small>API</small></label>
  <label class="check"><input type="checkbox" name="source" value="platforms"> 445 profile sites <small>OPTIONAL</small></label>`);
sourceList.insertAdjacentHTML('beforebegin', `
  <div class="source-presets" role="group" aria-label="Source selection">
    <button type="button" class="button" data-source-preset="all">All</button>
    <button type="button" class="button" data-source-preset="accounts">Profiles</button>
    <button type="button" class="button" data-source-preset="research">Research</button>
    <button type="button" class="button" data-source-preset="none">Clear</button>
  </div>`);
sourceList.insertAdjacentHTML('afterend', '<p class="source-count" id="source-count" aria-live="polite"></p><p class="source-count">The optional group sends the username to up to 445 sites and may take several minutes. Blocked or uncertain results require manual verification.</p>');

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

// Reverse image search uses independent services only on an explicit click.
// Neither the entered URL nor any image file is uploaded to Signal.
document.querySelector('.phone-tool').insertAdjacentHTML('afterend', `
  <section class="reverse-image-tool" aria-labelledby="image-search-title">
    <div class="label" id="image-search-title">03 / REVERSE IMAGE SEARCH</div>
    <p class="subtle">Find pages with the same or similar image using Google Lens or TinEye. Results do not identify a person.</p>
    <form id="image-search-form" novalidate>
      <label class="label" for="image-search-url">PUBLIC IMAGE URL</label>
      <input class="field" id="image-search-url" type="url" maxlength="2048" placeholder="https://example.com/image.jpg" autocomplete="off">
      <p class="hint">Use a public image link without passwords or private tokens. The selected service receives this URL when opened.</p>
      <button class="button" type="submit">PREPARE IMAGE SEARCH</button>
    </form>
    <p class="subtle" id="image-search-status" role="status" aria-live="polite"></p>
    <div class="image-search-actions" id="image-search-results" hidden></div>
    <form id="image-file-form" action="https://lens.google.com/upload" method="post" enctype="multipart/form-data" target="_blank" rel="noopener noreferrer" novalidate>
      <label class="label" for="image-search-file">PHOTO FROM DEVICE</label>
      <input class="field image-file" id="image-search-file" type="file" name="encoded_image" accept="image/jpeg,image/png,image/webp,image/gif">
      <p class="hint">When you press the button, the image is sent directly to Google Lens. Signal does not receive or store the file.</p>
      <button class="button" type="submit">SEARCH PHOTO WITH GOOGLE LENS ↗</button>
      <p class="subtle" id="image-file-status" role="status" aria-live="polite"></p>
    </form>
    <p class="subtle">You can also open a service below and upload a photo there yourself.</p>
    <div class="image-search-actions">
      <a class="button" href="https://images.google.com/" target="_blank" rel="noopener noreferrer">Google Images ↗</a>
      <a class="button" href="https://tineye.com/" target="_blank" rel="noopener noreferrer">TinEye ↗</a>
      <a class="button" href="https://www.bing.com/visualsearch" target="_blank" rel="noopener noreferrer">Bing Visual Search ↗</a>
    </div>
    <p class="subtle">External services have their own privacy policies and may store images or URLs. Search only images you have permission to use.</p>
  </section>`);

$('image-search-form').addEventListener('submit', event => {
  event.preventDefault();
  const results = $('image-search-results');
  const status = $('image-search-status');
  results.replaceChildren();
  results.hidden = true;
  try {
    const url = new URL($('image-search-url').value.trim());
    const host = url.hostname.toLowerCase();
    // Do not pass local addresses or credentials to an external service.
    const ip = host.split('.').map(Number);
    const privateIPv4 = ip.length === 4 && ip.every(n => Number.isInteger(n) && n >= 0 && n <= 255) &&
      (ip[0] === 0 || ip[0] === 10 || ip[0] === 127 || ip[0] >= 224 ||
       (ip[0] === 169 && ip[1] === 254) || (ip[0] === 172 && ip[1] >= 16 && ip[1] <= 31) ||
       (ip[0] === 192 && ip[1] === 168) || (ip[0] === 100 && ip[1] >= 64 && ip[1] <= 127));
    if (!['http:', 'https:'].includes(url.protocol) || url.username || url.password ||
        host === 'localhost' || host.endsWith('.localhost') || host.endsWith('.local') ||
        !host.includes('.') || host.startsWith('[') || privateIPv4) throw new Error();
    const services = [
      ['Google Lens', 'https://lens.google.com/uploadbyurl', 'url'],
      ['TinEye', 'https://tineye.com/search', 'url']
    ];
    for (const [label, base, parameter] of services) {
      const destination = new URL(base);
      destination.searchParams.set(parameter, url.href);
      const link = document.createElement('a');
      link.className = 'button';
      link.textContent = label + ' ↗';
      link.href = destination.href;
      link.target = '_blank';
      link.rel = 'noopener noreferrer';
      results.appendChild(link);
    }
    results.hidden = false;
    status.textContent = 'Links are ready. Open a service to run the search.';
  } catch (error) {
    status.textContent = 'Enter a valid public HTTP or HTTPS image URL without credentials.';
  }
});

$('image-file-form').addEventListener('submit', event => {
  const file = $('image-search-file').files[0];
  const allowed = ['image/jpeg', 'image/png', 'image/webp', 'image/gif'];
  if (!file || !allowed.includes(file.type) || file.size === 0 || file.size > 10 * 1024 * 1024) {
    event.preventDefault();
    $('image-file-status').textContent = 'Choose a JPG, PNG, WebP, or GIF image up to 10 MB.';
    return;
  }
  $('image-file-status').textContent = 'Opening Google Lens. The selected image is sent directly to Google.';
});

'use strict';
(function () {
  const el = id => document.getElementById(id);
  let user = null;

  async function request(path, payload) {
    const options = { credentials: 'same-origin', headers: {} };
    if (payload !== undefined) {
      options.method = 'POST'; options.headers['Content-Type'] = 'application/json';
      options.headers['X-CSRF-Token'] = user.csrf; options.body = JSON.stringify(payload);
    }
    const response = await fetch(path, options);
    let data;
    try { data = await response.json(); } catch (e) { throw new Error('Unexpected server response.'); }
    if (!response.ok) throw new Error(data.error || 'Account service is unavailable.');
    return data;
  }

  function node(tag, className, text) {
    const element = document.createElement(tag);
    if (className) element.className = className;
    if (text !== undefined) element.textContent = text;
    return element;
  }

  async function loadUsers() {
    el('refresh-users').disabled = true; el('admin-status').textContent = '';
    try {
      const data = await request('/api/admin/users');
      el('user-count').textContent = 'Total accounts: ' + data.total;
      const list = el('user-list'); list.replaceChildren();
      for (const account of data.users) {
        const row = node('div', 'user-row');
        const name = node('strong', 'user-name', account.username); name.setAttribute('data-no-translate', '');
        const role = node('span', 'small', account.is_admin ? 'Administrator' : 'Member');
        const state = node('span', 'badge', account.enabled ? 'Active' : 'Disabled');
        const date = node('span', 'date', new Date(account.created_at * 1000).toLocaleDateString());
        row.append(name, role, state, date);
        if (!account.is_admin) {
          const button = node('button', 'button', account.enabled ? 'Disable' : 'Enable');
          button.type = 'button';
          button.onclick = async () => {
            if (!confirm(account.enabled ? 'Disable this account? Its sessions will be signed out.' : 'Enable this account?')) return;
            button.disabled = true;
            try { await request('/api/admin/user-status', { user_id: account.id, enabled: !account.enabled }); await loadUsers(); }
            catch (error) { el('admin-status').textContent = error.message; button.disabled = false; }
          };
          row.appendChild(button);
        } else row.appendChild(node('span', 'small', 'Protected'));
        list.appendChild(row);
      }
    } catch (error) { el('admin-status').textContent = error.message; }
    finally { el('refresh-users').disabled = false; }
  }
  el('refresh-users').onclick = () => loadUsers();
  request('/api/auth/session').then(result => {
    if (!result.user || !result.user.is_admin) { location.href = '/account'; return; }
    user = result.user; return loadUsers();
  }).catch(error => { el('admin-status').textContent = error.message; });
})();

'use strict';
(function () {
  const el = id => document.getElementById(id);
  let user = null;
  let adminLink = null;

  async function request(path, payload, csrf) {
    const options = { credentials: 'same-origin', headers: {} };
    if (payload !== undefined) {
      options.method = 'POST';
      options.headers['Content-Type'] = 'application/json';
      if (csrf) options.headers['X-CSRF-Token'] = csrf;
      options.body = JSON.stringify(payload);
    }
    const response = await fetch(path, options);
    let data;
    try { data = await response.json(); } catch (e) { throw new Error('Unexpected server response.'); }
    if (!response.ok) throw new Error(data.error || 'Account service is unavailable.');
    return data;
  }

  function showMode(mode) {
    const login = mode === 'login';
    el('login-form').hidden = !login; el('register-form').hidden = login;
    el('show-login').classList.toggle('active', login); el('show-register').classList.toggle('active', !login);
    el('show-login').setAttribute('aria-selected', String(login)); el('show-register').setAttribute('aria-selected', String(!login));
    el('auth-status').textContent = '';
  }
  el('show-login').onclick = () => showMode('login');
  el('show-register').onclick = () => showMode('register');

  function showUser(value) {
    user = value || null;
    el('auth-panel').hidden = Boolean(user); el('user-panel').hidden = !user;
    if (adminLink) { adminLink.remove(); adminLink = null; }
    if (!user) return;
    el('account-name').textContent = user.username;
    el('account-role').textContent = user.is_admin ? 'Administrator' : 'Member';
    if (user.is_admin) {
      adminLink = document.createElement('a');
      adminLink.className = 'button'; adminLink.href = '/admin'; adminLink.textContent = 'Open admin panel ↗';
      el('account-actions').prepend(adminLink);
    }
  }

  async function submitAuth(event, mode) {
    event.preventDefault();
    const form = event.currentTarget, button = form.querySelector('button[type="submit"]');
    const username = el(mode + '-username').value, password = el(mode + '-password').value;
    el('auth-status').textContent = '';
    if (mode === 'register' && password !== el('register-confirm').value) {
      el('auth-status').textContent = 'Passwords do not match.'; return;
    }
    button.disabled = true;
    try {
      const result = await request('/api/auth/' + mode, { username, password });
      form.reset(); showUser(result.user);
    } catch (error) { el('auth-status').textContent = error.message; }
    finally { el(mode + '-password').value = ''; if (mode === 'register') el('register-confirm').value = ''; button.disabled = false; }
  }
  el('login-form').addEventListener('submit', event => submitAuth(event, 'login'));
  el('register-form').addEventListener('submit', event => submitAuth(event, 'register'));

  el('logout').onclick = async () => {
    if (!user) return;
    try { await request('/api/auth/logout', {}, user.csrf); showUser(null); showMode('login'); }
    catch (error) { el('user-status').textContent = error.message; }
  };
  el('password-form').addEventListener('submit', async event => {
    event.preventDefault();
    if (!user) return;
    const form = event.currentTarget, button = form.querySelector('button[type="submit"]');
    const current = el('current-password').value, next = el('new-password').value;
    el('user-status').textContent = '';
    if (next !== el('new-confirm').value) { el('user-status').textContent = 'Passwords do not match.'; return; }
    button.disabled = true;
    try {
      const result = await request('/api/auth/change-password', { current_password: current, new_password: next }, user.csrf);
      form.reset(); showUser(null); showMode('login'); el('auth-status').textContent = result.message;
    } catch (error) { el('user-status').textContent = error.message; }
    finally { el('current-password').value = ''; el('new-password').value = ''; el('new-confirm').value = ''; button.disabled = false; }
  });

  request('/api/auth/session').then(result => showUser(result.user)).catch(error => { el('auth-status').textContent = error.message; });
})();

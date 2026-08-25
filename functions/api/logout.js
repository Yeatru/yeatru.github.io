// Admin logout: clear the signed HttpOnly session cookie.

import { setCookieHeader, json } from '../_shared/auth.js';

export async function onRequest(context) {
  const { request } = context;
  if (request.method !== 'POST') {
    return json({ ok: false, error: 'method_not_allowed' }, 405, { Allow: 'POST' });
  }
  return json({ ok: true }, 200, {
    'Set-Cookie': setCookieHeader('', 0, true),
  });
}

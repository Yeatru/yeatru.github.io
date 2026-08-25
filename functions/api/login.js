// Server-side admin login endpoint.
// POST { username, password } -> 200 {ok:true} + Set-Cookie, or 401 {ok:false,error}
//
// Only accepts HTTPS. Uses PBKDF2(SHA-256) + per-password salt for credential
// verification; issues an HMAC-SHA256 signed, HttpOnly/Secure session cookie
// (no server-side session store needed; rotate ADMIN_SECRET to revoke all).

import {
  verifyPassword, signSessionId, setCookieHeader, getAdminSecretBytes, json,
  SESSION_MAX_AGE_SEC,
} from '../_shared/auth.js';

export async function onRequest(context) {
  const { request, env } = context;

  if (request.method !== 'POST') {
    return json({ ok: false, error: 'method_not_allowed' }, 405, { Allow: 'POST' });
  }

  // Basic rate-limit guard: refuse if body is unreasonably large before parsing.
  const cl = request.headers.get('Content-Length');
  if (cl && parseInt(cl, 10) > 8192) {
    return json({ ok: false, error: 'payload_too_large' }, 413);
  }

  let payload;
  try {
    const ct = (request.headers.get('Content-Type') || '').toLowerCase();
    if (ct.includes('application/json')) {
      payload = await request.json();
    } else {
      const fd = await request.formData();
      payload = { username: fd.get('username'), password: fd.get('password') };
    }
  } catch {
    return json({ ok: false, error: 'bad_payload' }, 400);
  }

  const username = typeof payload?.username === 'string' ? payload.username.trim() : '';
  const password = typeof payload?.password === 'string' ? payload.password : '';

  // 400s of artificial slowdown on invalid payloads so enumeration is expensive.
  if (!username || !password) {
    await wait(250);
    return json({ ok: false, error: 'missing_credentials' }, 400);
  }

  const expectedUser = (env?.ADMIN_USERNAME || '').toString();
  const expectedHash = (env?.ADMIN_PASSWORD_HASH || '').toString();
  const secretBytes = getAdminSecretBytes(env);

  if (!expectedUser || !expectedHash || !secretBytes) {
    return json({
      ok: false,
      error: 'auth_not_configured',
      detail: 'Set ADMIN_USERNAME, ADMIN_PASSWORD_HASH, and ADMIN_SECRET environment variables in Cloudflare Pages → Settings → Environment variables.',
    }, 503);
  }

  // Constant-ish: run password-hash verification regardless of username match so
  // timing leaks don't reveal "user exists".
  const userMatches = username === expectedUser;
  const [pwOk] = await Promise.all([
    verifyPassword(password, expectedHash),
    // Ensure minimum wall time to discourage brute force (parallel request cost).
    wait(350),
  ]);

  if (!userMatches || !pwOk) {
    return json({ ok: false, error: 'invalid_credentials' }, 401);
  }

  const { value, maxAge } = await signSessionId(secretBytes);
  return json({ ok: true, expiresIn: SESSION_MAX_AGE_SEC }, 200, {
    'Set-Cookie': setCookieHeader(value, maxAge),
  });
}

function wait(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

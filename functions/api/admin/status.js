// Admin session status check. Returns 200 {ok:true,isAdmin:true,exp} or 401.
// Used by the browser UI to re-sync the optimistic localStorage flag with the
// single authoritative source (the signed HttpOnly cookie).

import { verifySessionCookie, getAdminSecretBytes, json } from '../../auth.js';

export async function onRequest(context) {
  const { request, env } = context;
  if (request.method !== 'GET' && request.method !== 'HEAD') {
    return json({ ok: false, error: 'method_not_allowed' }, 405, { Allow: 'GET, HEAD' });
  }
  const raw = env?.ADMIN_SECRET;
  const secretBytes = getAdminSecretBytes(env);
  if (!secretBytes) {
    return json({
      ok: false, isAdmin: false,
      error: 'auth_not_configured',
      debug: {
        hasSecret: !!raw,
        secretLength: raw ? raw.length : 0,
        envKeys: Object.keys(env || {}),
      },
    }, 503);
  }
  const r = await verifySessionCookie(request, secretBytes);
  if (r.ok) {
    return json({ ok: true, isAdmin: true, exp: r.exp });
  }
  return json({ ok: true, isAdmin: false }, 401);
}

// Shared server-side auth primitives for Cloudflare Pages Functions.
// No Node APIs allowed — use only WebCrypto / standard ESM.
//
// Expected Pages environment variables (set via Cloudflare dashboard → Pages → Settings):
//   ADMIN_SECRET         : >= 32 random bytes, base64 encoded (32+ bytes decoded).
//                         Used to sign session cookies. Rotate this value to revoke all sessions.
//   ADMIN_USERNAME       : Admin login name (case-sensitive).
//   ADMIN_PASSWORD_HASH  : Stored PBKDF2 verifier in the format:
//                            pbkdf2_sha256${ITERATIONS}$${B64_SALT}$${B64_DIGEST}
//                          Produce this value with the accompanying
//                          scripts/generate-admin-hash.js helper.

export const COOKIE_NAME = 'admin_sid';
export const SESSION_MAX_AGE_SEC = 8 * 3600; // 8h

// -------------------- helpers --------------------

function b64decode(s) {
  // Accept standard base64 or base64url, tolerate missing padding.
  const std = String(s).replace(/-/g, '+').replace(/_/g, '/').replace(/\s/g, '');
  const pad = std.length % 4 === 0 ? '' : '='.repeat(4 - (std.length % 4));
  const bin = atob(std + pad);
  const out = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
  return out;
}

function b64encode(bytes, urlSafe = false) {
  let s = '';
  const u8 = new Uint8Array(bytes);
  for (let i = 0; i < u8.length; i++) s += String.fromCharCode(u8[i]);
  let out = btoa(s);
  if (urlSafe) out = out.replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/g, '');
  return out;
}

async function hmacSha256(keyBytes, messageBytes) {
  const key = await crypto.subtle.importKey(
    'raw', keyBytes, { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']
  );
  return new Uint8Array(await crypto.subtle.sign('HMAC', key, messageBytes));
}

async function pbkdf2Sha256(password, salt, iterations, dkLenBytes) {
  const pwKey = await crypto.subtle.importKey(
    'raw', new TextEncoder().encode(password), 'PBKDF2', false, ['deriveBits']
  );
  const bits = await crypto.subtle.deriveBits(
    { name: 'PBKDF2', salt, iterations, hash: 'SHA-256' },
    pwKey, dkLenBytes * 8
  );
  return new Uint8Array(bits);
}

function timingSafeEqual(a, b) {
  if (a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i++) diff |= a[i] ^ b[i];
  return diff === 0;
}

function enc(s) { return new TextEncoder().encode(s); }

// -------------------- password verifier --------------------

export async function verifyPassword(password, storedHash) {
  // Format: pbkdf2_sha256${iter}$${b64salt}$${b64digest}
  if (typeof storedHash !== 'string') return false;
  const parts = storedHash.split('$');
  if (parts.length !== 4) return false;
  const [alg, iterStr, b64salt, b64digest] = parts;
  if (alg !== 'pbkdf2_sha256') return false;
  const iterations = parseInt(iterStr, 10);
  if (!Number.isFinite(iterations) || iterations < 1) return false;
  let saltBytes, digestBytes;
  try {
    saltBytes = b64decode(b64salt);
    digestBytes = b64decode(b64digest);
  } catch { return false; }
  if (digestBytes.length === 0 || saltBytes.length < 8) return false;
  const derived = await pbkdf2Sha256(password, saltBytes, iterations, digestBytes.length);
  return timingSafeEqual(derived, digestBytes);
}

// -------------------- session cookie --------------------

// Returns the decoded, unverified "part1.part2.part3" object or null.
function splitCookie(raw) {
  if (!raw) return null;
  const idx = raw.indexOf(COOKIE_NAME + '=');
  if (idx === -1) return null;
  const start = idx + COOKIE_NAME.length + 1;
  let end = raw.indexOf(';', start);
  if (end === -1) end = raw.length;
  return raw.slice(start, end).trim();
}

export async function signSessionId(secretBytes) {
  const idBytes = new Uint8Array(16);
  crypto.getRandomValues(idBytes);
  const exp = Math.floor(Date.now() / 1000) + SESSION_MAX_AGE_SEC;
  const payload = `admin/v1/${b64encode(idBytes, true)}/${exp}`;
  const sig = await hmacSha256(secretBytes, enc(payload));
  const sigB64 = b64encode(sig, true);
  return {
    value: `${b64encode(idBytes, true)}.${exp}.${sigB64}`,
    maxAge: SESSION_MAX_AGE_SEC,
  };
}

export async function verifySessionCookie(request, secretBytes) {
  const cookieHeader = request.headers.get('Cookie') || '';
  const value = splitCookie(cookieHeader);
  if (!value) return { ok: false };
  const parts = value.split('.');
  if (parts.length !== 3) return { ok: false };
  const [idB64, expStr, sigB64] = parts;
  const exp = parseInt(expStr, 10);
  if (!Number.isFinite(exp)) return { ok: false };
  if (exp <= Math.floor(Date.now() / 1000)) return { ok: false };
  const payload = `admin/v1/${idB64}/${exp}`;
  let expectedSig, providedSig;
  try {
    expectedSig = await hmacSha256(secretBytes, enc(payload));
    providedSig = b64decode(sigB64);
  } catch { return { ok: false }; }
  if (!timingSafeEqual(expectedSig, providedSig)) return { ok: false };
  return { ok: true, exp, id: idB64 };
}

export function setCookieHeader(value, maxAgeSec, isLogout = false) {
  // Set-Cookie for HTTPS (HSTS-enabled) site.
  // SameSite=Lax is required so that the cookie travels on top-level navigations
  // (useful for status checks) but not on cross-site POSTs (CSRF defense for /logout).
  const parts = [
    `${COOKIE_NAME}=${isLogout ? '' : value}`,
    `Max-Age=${isLogout ? 0 : maxAgeSec}`,
    'Path=/',
    'HttpOnly',
    'Secure',
    'SameSite=Lax',
  ];
  return parts.join('; ');
}

export function getAdminSecretBytes(env) {
  const raw = env && env.ADMIN_SECRET;
  if (!raw) return null;
  try {
    const bytes = b64decode(raw);
    if (bytes.length < 32) return null;
    return bytes;
  } catch { return null; }
}

export function json(body, status = 200, extraHeaders = {}) {
  const headers = {
    'Content-Type': 'application/json; charset=utf-8',
    'Cache-Control': 'no-store, private',
    'X-Content-Type-Options': 'nosniff',
    ...extraHeaders,
  };
  return new Response(JSON.stringify(body), { status, headers });
}

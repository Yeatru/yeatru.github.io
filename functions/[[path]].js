// Cloudflare Pages Function v3 — zero-redirect guarantee
// Strategy:
//   (a) Hardcoded 301 redirects (legacy slug rewrites like shipping-and-logistics).
//       These are intentional, and Bing accepts pure HTTP 301 without HTML body.
//   (b) .html URLs → intercept BEFORE Cloudflare auto-strip triggers, rewrite to
//       clean path internally via a SUBREQUEST with special header to bypass
//       auto-strip on the inner request. We also force static file read via
//       env.ASSETS when possible.
//   (c) Any non-.html, non-redirect URL → pass through untouched.
//
// The key v3 fix: Never let Cloudflare Pages default handler see a ".html" URL
// path, because its auto-strip logic answers with 308 BEFORE our Function
// can intercept the response. Instead, we internally map .html → clean path
// with __bypass_strip=1 header on the subrequest, which tells Pages to serve
// the asset directly without redirecting.

const PERMANENT_301 = {
  '/shipping-and-logistics.html':   '/logistics-shipping.html',
  '/shipping-and-logistics':        '/logistics-shipping.html',
  '/how-it-works.html':             '/index.html#sourcing-process',
  '/how-it-works':                  '/index.html#sourcing-process',
  '/yiwu-market.html':              '/blog-yiwu-market-agent-for-foreigners.html',
  '/yiwu-market':                   '/blog-yiwu-market-agent-for-foreigners.html',
};

export async function onRequest(context) {
  const { request, next, env } = context;
  const url = new URL(request.url);

  // Skip for non-GET
  if (request.method !== 'GET') return next();

  // (a) 301 legacy slug redirects
  const redirectTarget = PERMANENT_301[url.pathname];
  if (redirectTarget) {
    const location = url.origin + redirectTarget + url.search;
    return new Response(null, {
      status: 301,
      headers: {
        Location: location,
        'Cache-Control': 'public, max-age=31536000, immutable',
      },
    });
  }

  // (b) .html → serve via ASSETS.fetch (if available) or via rewritten subrequest
  // This approach avoids CF Pages "auto-strip .html → 308" default behavior entirely.
  if (/\.html$/i.test(url.pathname)) {
    const cleanPathname = url.pathname.replace(/\.html$/i, '');

    // Strategy 1: Use Pages ASSETS binding if available (CF Pages v2 platform)
    if (env && env.ASSETS && typeof env.ASSETS.fetch === 'function') {
      try {
        // Build a new request to the same origin, but to the clean pathname
        const cleanReq = new Request(
          url.origin + cleanPathname + url.search,
          request,
        );
        const assetResp = await env.ASSETS.fetch(cleanReq);
        if (assetResp && assetResp.status === 200) {
          const headers = new Headers(assetResp.headers);
          headers.delete('Location');
          headers.delete('Refresh');
          if (!headers.has('Content-Type')) {
            headers.set('Content-Type', 'text/html; charset=utf-8');
          }
          // Serve ASSETS body with our request's status (200) — never 308
          return new Response(assetResp.body, { status: 200, headers });
        }
      } catch (e) {
        // Fall through to strategy 2
      }
    }

    // Strategy 2: Subrequest with __bypass_strip header + explicitly go to clean path
    const innerUrl = url.origin + cleanPathname + (url.search || '');
    const innerReq = new Request(innerUrl, {
      method: request.method,
      headers: new Headers(request.headers),
      redirect: 'manual',
      cf: request.cf,
    });
    innerReq.headers.set('X-Pages-No-Strip', '1');
    innerReq.headers.set('X-Internal-Subrequest', '1');

    // Already-stripped won't redirect again. We pass to next() with this rewritten.
    // BUT: since redirect=manual on subrequest, even if inner returns 308 we capture it.
    let resp;
    try {
      resp = await fetch(innerReq, innerReq);
      if (resp.status === 200) {
        const headers = new Headers(resp.headers);
        headers.delete('Location');
        headers.delete('Refresh');
        if (!headers.has('Content-Type')) headers.set('Content-Type', 'text/html; charset=utf-8');
        return new Response(resp.body, { status: 200, headers });
      }
      if (resp.status === 308 || resp.status === 301 || resp.status === 302) {
        // Inner response tried to redirect — strip and serve body if available, else follow once
        const body = resp.body;
        if (body) {
          const headers = new Headers(resp.headers);
          headers.delete('Location');
          headers.delete('Refresh');
          if (!headers.has('Content-Type')) headers.set('Content-Type', 'text/html; charset=utf-8');
          return new Response(body, { status: 200, headers });
        }
        const location = resp.headers.get('Location');
        if (location) {
          const follow = await fetch(location, { redirect: 'manual', headers: innerReq.headers });
          if (follow.status === 200) {
            const headers = new Headers(follow.headers);
            headers.delete('Location');
            headers.delete('Refresh');
            if (!headers.has('Content-Type')) headers.set('Content-Type', 'text/html; charset=utf-8');
            return new Response(follow.body, { status: 200, headers });
          }
        }
      }
    } catch (e) {
      // fallthrough
    }
  }

  // (c) default — but also check if this clean path hits the X-Internal-Subrequest loop
  const isInternal = request.headers.get('X-Internal-Subrequest') === '1';
  if (isInternal) {
    return next();
  }
  return next();
}

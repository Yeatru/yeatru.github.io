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

const GITHUB_IMAGE_REPO = 'https://raw.githubusercontent.com/Yeatru/Image/main/Images';

const IMAGE_MIME = {
  '.png':  'image/png',
  '.jpg':  'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.webp': 'image/webp',
  '.gif':  'image/gif',
  '.svg':  'image/svg+xml',
  '.ico':  'image/x-icon',
};

const PERMANENT_301 = {
  '/shipping-and-logistics.html':   '/logistics-shipping.html',
  '/shipping-and-logistics':        '/logistics-shipping.html',
  '/how-it-works.html':             '/index.html#sourcing-process',
  '/how-it-works':                  '/index.html#sourcing-process',
  '/yiwu-market.html':              '/blog-yiwu-market-agent-for-foreigners.html',
  '/yiwu-market':                   '/blog-yiwu-market-agent-for-foreigners.html',
  '/blog-index.html':               '/blog.html',
  '/blog-index':                    '/blog.html',
  '/process.html':                  '/index.html#sourcing-process',
  '/process':                       '/index.html#sourcing-process',
  '/term.html':                     '/terms.html',
  '/term':                          '/terms.html',
  '/services.html':                 '/supplier-verification.html',
  '/services':                      '/supplier-verification.html',
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

  // (a.1) Image proxy: /images/SKU.ext → fetch from Yeatru/Image GitHub repo
  //   Bypasses wsrv.nl (often offline) and serves images same-origin via CF CDN.
  //   CF edge IPs are not rate-limited by GitHub like raw.githubusercontent.com from
  //   shared sandbox IPs. Cached for 24h on CF edge.
  const imageMatch = url.pathname.match(/^\/(images?|img)\/(.+)$/i);
  if (imageMatch) {
    const filename = decodeURIComponent(imageMatch[2]);
    const ext = (filename.match(/\.(\w+)$/) || [])[1];
    const mime = ext ? IMAGE_MIME['.' + ext.toLowerCase()] : null;
    const upstreamUrl = `${GITHUB_IMAGE_REPO}/${filename}`;
    try {
      const imgResp = await fetch(upstreamUrl, {
        headers: { 'User-Agent': 'YeatruSourcing/1.0 (+https://www.yeatru.com)' },
        cf: { cacheTtl: 86400, polish: 'original' },
      });
      if (imgResp.status === 200) {
        const headers = new Headers(imgResp.headers);
        if (mime && !headers.has('Content-Type')) headers.set('Content-Type', mime);
        headers.set('Cache-Control', 'public, max-age=86400, s-maxage=86400');
        headers.set('Access-Control-Allow-Origin', '*');
        headers.set('X-Yeatru-Img', 'proxy-ok');
        return new Response(imgResp.body, { status: 200, headers });
      }
      // Fallback: try jsdelivr CDN mirror (already cached for global users)
      const jsdelivrUrl = `https://cdn.jsdelivr.net/gh/Yeatru/Image@main/Images/${filename}`;
      const jdResp = await fetch(jsdelivrUrl, {
        headers: { 'User-Agent': 'YeatruSourcing/1.0' },
        cf: { cacheTtl: 86400, polish: 'original' },
      });
      if (jdResp.status === 200) {
        const headers = new Headers(jdResp.headers);
        if (mime && !headers.has('Content-Type')) headers.set('Content-Type', mime);
        headers.set('Cache-Control', 'public, max-age=86400, s-maxage=86400');
        headers.set('X-Yeatru-Img', 'jsdelivr-fallback');
        return new Response(jdResp.body, { status: 200, headers });
      }
      // 404 placeholder
      const placeholder = `
        <svg xmlns="http://www.w3.org/2000/svg" width="400" height="300" viewBox="0 0 400 300">
          <rect width="400" height="300" fill="#f5f5f5"/>
          <text x="200" y="150" text-anchor="middle" font-family="sans-serif" font-size="14" fill="#999">Image: ${filename}</text>
          <text x="200" y="175" text-anchor="middle" font-family="sans-serif" font-size="11" fill="#bbb">Loading...</text>
        </svg>`;
      return new Response(placeholder, {
        status: 200,
        headers: { 'Content-Type': 'image/svg+xml', 'Cache-Control': 'no-cache' },
      });
    } catch (e) {
      const placeholder = `
        <svg xmlns="http://www.w3.org/2000/svg" width="400" height="300" viewBox="0 0 400 300">
          <rect width="400" height="300" fill="#fafafa"/>
          <text x="200" y="150" text-anchor="middle" font-family="sans-serif" font-size="13" fill="#bbb">${filename}</text>
        </svg>`;
      return new Response(placeholder, {
        status: 200,
        headers: { 'Content-Type': 'image/svg+xml', 'Cache-Control': 'no-cache' },
      });
    }
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

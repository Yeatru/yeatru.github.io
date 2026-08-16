// Cloudflare Pages Function — 3-in-1:
//   (a) Hardcoded 301 redirects for legacy/slug-mismatch URLs (shipping-and-logistics → logistics-shipping, etc.)
//       This fixes Google Search Console "Page cannot be indexed: Not found (404)" for slugs
//       the user manually inspected but which don't exist as files.
//   (b) Intercept *.html URLs and serve them as 200 (instead of letting Cloudflare's
//       auto-strip-.html return a 308 Permanent Redirect).
//   (c) Fallback: if the file truly doesn't exist and no redirect matched, let next()
//       return a 404 but still log a short hint to help debugging.
const PERMANENT_301 = {
  '/shipping-and-logistics.html':   '/logistics-shipping.html',
  '/shipping-and-logistics':        '/logistics-shipping.html',
  '/how-it-works.html':             '/index.html#sourcing-process',
  '/how-it-works':                  '/index.html#sourcing-process',
  '/yiwu-market.html':              '/blog-yiwu-market-agent-for-foreigners.html',
  '/yiwu-market':                   '/blog-yiwu-market-agent-for-foreigners.html',
};

export async function onRequest(context) {
  const { request, next } = context;
  const url = new URL(request.url);

  // (a) 301 legacy slug redirects (both with and without .html)
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

  // (b) .html → serve the clean path content as 200
  if (/\.html$/.test(url.pathname)) {
    const cleanUrl = url.origin + url.pathname.replace(/\.html$/, '') + url.search;
    const response = await fetch(cleanUrl);

    if (response && response.status === 200) {
      const headers = new Headers(response.headers);
      if (!headers.has('Content-Type')) {
        headers.set('Content-Type', 'text/html; charset=utf-8');
      }
      headers.delete('Location');
      headers.delete('Refresh');
      return new Response(response.body, { status: 200, headers });
    }
  }

  // (c) default chain
  return next();
}


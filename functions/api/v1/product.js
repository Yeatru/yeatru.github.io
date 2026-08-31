// Yeatru Public Data API — /api/v1/product?sku=YCS-XXX
// Single-product lookup by SKU. Accepts GET and HEAD.

const CACHE_TTL_SEC = 86400;

function json(body, status = 200, extraHeaders = {}) {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, HEAD, OPTIONS',
      'Cache-Control': `public, max-age=3600, s-maxage=${CACHE_TTL_SEC}`,
      'X-Yeatru-API': 'v1',
      ...extraHeaders,
    },
  });
}

export async function onRequest(context) {
  const { request } = context;

  if (request.method === 'OPTIONS') {
    return new Response(null, {
      status: 204,
      headers: { 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': 'GET, HEAD, OPTIONS' },
    });
  }
  if (request.method !== 'GET' && request.method !== 'HEAD') {
    return json({ error: 'method_not_allowed' }, 405);
  }

  const url = new URL(request.url);
  const sku = url.searchParams.get('sku') || (url.pathname.split('/').pop() || '').replace('.json','');

  if (!sku) {
    return json({ error: 'sku_required', hint: 'GET /api/v1/product?sku=YCS-ACC-001' }, 400);
  }

  const cache = caches.default;
  const cacheKey = new Request(`https://yeatru-pages-cache/api/v1/product/${sku}`, request);
  let cached = await cache.match(cacheKey);
  if (cached) return cached;

  let siteData;
  try {
    const resp = await context.env.ASSETS.fetch(
      new Request(new URL('/site-data.json', request.url).toString())
    );
    if (!resp.ok) return json({ error: 'asset_fetch_failed' }, 502);
    siteData = await resp.json();
  } catch (e) {
    return json({ error: 'asset_parse_failed', detail: String(e) }, 500);
  }

  const product = (siteData.products || []).find(
    p => (p.sku || '').toUpperCase() === sku.toUpperCase()
  );

  if (!product) {
    return json({
      error: 'not_found',
      sku,
      hint: 'Check /api/v1/products?q=' + encodeURIComponent(sku) + ' for fuzzy match',
    }, 404);
  }

  const response = json({
    apiVersion: 'v1',
    generatedAt: new Date().toISOString(),
    siteDataVersion: siteData.version,
    siteDataLastUpdated: siteData.lastUpdated,
    product: {
      ...product,
      productUrl: `https://www.yeatru.com/product-${product.sku}.html`,
    },
  });

  context.waitUntil(cache.put(cacheKey, response.clone()));
  return response;
}

// Yeatru Public Data API — /api/v1/categories
// Returns all 17 product categories with counts.

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

  const cache = caches.default;
  const cacheKey = new Request('https://yeatru-pages-cache/api/v1/categories', request);
  let cached = await cache.match(cacheKey);
  if (cached) return cached;

  let siteData;
  try {
    const resp = await context.env.ASSETS.fetch(
      new Request(new URL('/site-data.json', request.url).toString())
    );
    siteData = await resp.json();
  } catch (e) {
    return json({ error: 'asset_parse_failed', detail: String(e) }, 500);
  }

  const products = siteData.products || [];
  const counts = {};
  for (const p of products) {
    const c = p.mainCategory || 'Uncategorized';
    counts[c] = (counts[c] || 0) + 1;
  }

  const response = json({
    apiVersion: 'v1',
    generatedAt: new Date().toISOString(),
    siteDataVersion: siteData.version,
    siteDataLastUpdated: siteData.lastUpdated,
    totalProducts: products.length,
    categories: siteData.categories.map(name => ({
      name,
      count: counts[name] || 0,
      endpoint: `https://www.yeatru.com/api/v1/products?category=${encodeURIComponent(name)}`,
      categoryPage: `https://www.yeatru.com/category-${name.toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'')}.html`,
    })),
    meta: { docs: 'https://www.yeatru.com/data.html' },
  });

  context.waitUntil(cache.put(cacheKey, response.clone()));
  return response;
}

// Yeatru Public Data API — /api/v1/products
//
// Public, CORS-enabled JSON endpoint for AI agents (ChatGPT/Codex/Claude)
// and data tools to fetch Yeatru's entire product catalog with metadata.
//
// Source: site-data.json (656 products, 17 categories)
// Caching: Cloudflare cache 24h; browser cache 1h
// Auth: None — public read-only. No writes.

const CACHE_TTL_SEC = 86400; // 24h Cloudflare cache

function json(body, status = 200, extraHeaders = {}) {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, HEAD, OPTIONS',
      'Access-Control-Allow-Headers': 'Accept, Authorization',
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
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, HEAD, OPTIONS',
        'Access-Control-Allow-Headers': 'Accept, Authorization',
      },
    });
  }
  if (request.method !== 'GET' && request.method !== 'HEAD') {
    return json({ error: 'method_not_allowed', allow: 'GET, HEAD, OPTIONS' }, 405);
  }

  // Try the Cloudflare cache first
  const cacheKey = new Request('https://yeatru-pages-cache/api/v1/products', request);
  const cache = caches.default;
  let cached = await cache.match(cacheKey);
  if (cached) return cached;

  // Fetch site-data.json from the same origin (Cloudflare Pages Functions v5 asset access)
  const assetsReq = new Request(new URL('/site-data.json', request.url).toString());
  let siteData;
  try {
    const resp = await context.env.ASSETS.fetch(assetsReq);
    if (!resp.ok) return json({ error: 'asset_fetch_failed', status: resp.status }, 502);
    siteData = await resp.json();
  } catch (e) {
    return json({ error: 'asset_parse_failed', detail: String(e) }, 500);
  }

  // Parse ?category=, ?q=, ?limit=, ?offset= query params
  const url = new URL(request.url);
  const categoryFilter = url.searchParams.get('category');
  const q = (url.searchParams.get('q') || '').toLowerCase();
  const limit = Math.min(parseInt(url.searchParams.get('limit') || '10000', 10), 10000);
  const offset = Math.max(parseInt(url.searchParams.get('offset') || '0', 10), 0);

  let products = siteData.products || [];

  if (categoryFilter) {
    products = products.filter(p =>
      (p.mainCategory || '').toLowerCase() === categoryFilter.toLowerCase() ||
      (p.category || '').toLowerCase() === categoryFilter.toLowerCase()
    );
  }
  if (q) {
    products = products.filter(p =>
      (p.sku || '').toLowerCase().includes(q) ||
      (p.name || '').toLowerCase().includes(q) ||
      (p.name_cn || '').includes(q)
    );
  }

  const total = products.length;
  const page = products.slice(offset, offset + limit);

  const response = json({
    apiVersion: 'v1',
    generatedAt: new Date().toISOString(),
    source: siteData.source,
    siteDataVersion: siteData.version,
    siteDataLastUpdated: siteData.lastUpdated,
    priceFormula: siteData.priceFormula,
    categories: siteData.categories,
    meta: {
      totalProducts: siteData.productCount,
      returned: page.length,
      totalMatched: total,
      offset,
      limit,
      filters: { category: categoryFilter || null, q: q || null },
      baseUrl: 'https://www.yeatru.com',
      productEndpoint: 'https://www.yeatru.com/api/v1/products?sku={sku}',
      docs: 'https://www.yeatru.com/data.html',
    },
    products: page.map(p => ({
      sku: p.sku,
      id: p.id,
      name: p.name,
      name_cn: p.name_cn,
      mainCategory: p.mainCategory,
      category: p.category,
      priceMin: p.priceMin,
      priceMax: p.priceMax,
      moq: p.moq,
      image: p.image,
      variations: p.variations,
      productUrl: `https://www.yeatru.com/product-${p.sku}.html`,
    })),
  });

  // Store in Cloudflare cache
  context.waitUntil(cache.put(cacheKey, response.clone()));
  return response;
}

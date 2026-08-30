// functions/_middleware.js — Cloudflare Pages Functions (global middleware).
// GEO + SEO:
//   1) Adds security headers to every HTML response,
//   2) If visitor comes from a known country, swaps data-usd-price on the fly
//      to data-geo-price (EUR/GBP/AED) and appends <script> window.__YEATRUGEO__
//      so the product page hero price renders the local currency symbol,
//   3) Adds Vary: Accept-Language, CF-IPCountry to preserve caching.
// Runtime scope is @cloudflare/pages 2.x.

const fx_vs_usd = { EUR: 0.92, GBP: 0.78, AED: 3.67, USD: 1.0 };
const country_to_ccy = {
  // Eurozone (20)
  DE: 'EUR', FR: 'EUR', IT: 'EUR', ES: 'EUR', NL: 'EUR', BE: 'EUR', AT: 'EUR',
  PT: 'EUR', GR: 'EUR', IE: 'EUR', FI: 'EUR', LU: 'EUR', SI: 'EUR', SK: 'EUR',
  EE: 'EUR', LV: 'EUR', LT: 'EUR', CY: 'EUR', MT: 'EUR', HR: 'EUR',
  // UK + overseas territories GBP
  GB: 'GBP', IM: 'GBP', JE: 'GBP', GG: 'GBP',
  // UAE + GCC common invoicing currency AED
  AE: 'AED',
};
const symbol = { USD: '$', EUR: '€', GBP: '£', AED: 'د.إ' };

function addSecurityHeaders(headers, isHtml) {
  headers.set('X-Content-Type-Options', 'nosniff');
  headers.set('Referrer-Policy', 'strict-origin-when-cross-origin');
  headers.set('Permissions-Policy',
    'camera=(), microphone=(), geolocation=(), interest-cohort=(), payment=()');
  headers.set('Strict-Transport-Security',
    'max-age=63072000; includeSubDomains; preload');
  headers.set('X-Frame-Options', 'SAMEORIGIN');
  if (isHtml) {
    headers.set('Content-Security-Policy',
      "default-src 'self'; " +
      "img-src 'self' data: https: blob:; " +
      "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; " +
      "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com " +
      "https://www.googletagmanager.com https://www.clarity.ms https://wsrv.nl; " +
      "font-src 'self' https://cdnjs.cloudflare.com data:; " +
      "connect-src 'self' https:; frame-ancestors 'self'; base-uri 'self'; form-action 'self' https:;");
  }
}

export async function onRequest(context) {
  const { request, next, env } = context;
  const url = new URL(request.url);
  const country = (request.cf && request.cf.country) || (request.headers.get('CF-IPCountry')) || 'US';
  const ccy = country_to_ccy[country] || 'USD';

  // Short-circuit for non-HTML: still pass through but add headers
  const accept = (request.headers.get('Accept') || '').toLowerCase();
  const isHtml = accept.includes('text/html') || url.pathname.endsWith('/') || url.pathname.endsWith('.html');

  const res = await next();

  // Only mutate 200 OK responses that are ours
  if (!res || res.status !== 200) return res;

  const newRes = new Response(res.body, res);
  const ctype = (newRes.headers.get('Content-Type') || '').toLowerCase();
  const html = isHtml || ctype.includes('text/html');
  addSecurityHeaders(newRes.headers, html);
  newRes.headers.set('Vary', (newRes.headers.get('Vary') ? newRes.headers.get('Vary') + ', ' : '') +
    'Accept, Accept-Language, CF-IPCountry');
  newRes.headers.set('X-Yeatru-Geo', country + ':' + ccy);

  if (!html) return newRes;

  // If this is a product page, inject inline <script> that overrides hero price display
  // (HTML Rewriter would be lighter, but we stay portable by text replace).
  let text = await newRes.text();
  let mutated = false;
  if (/<meta\s+(?:name|property)=["']og:type["'][^>]*content=["']product["']/i.test(text) ||
      /data-usd-price=/i.test(text)) {
    const script = `\n<script data-yeatru-geo="1">\n` +
      `window.__YEATRUGEO__ = { country: ${JSON.stringify(country)}, ccy: ${JSON.stringify(ccy)}, ` +
      `symbol: ${JSON.stringify(symbol[ccy] || '$')}, rate: ${fx_vs_usd[ccy].toFixed(4)} };\n` +
      `document.documentElement.setAttribute('data-geo-ccy', ${JSON.stringify(ccy)});\n` +
      `// Swap hero price elements: \$X.XX -> €X.XX (client-side, SEO sees original USD)\n` +
      `document.querySelectorAll('[data-geo-price-swappable="1"]').forEach(el=>{const u=el.getAttribute('data-usd');if(u){const v=(parseFloat(u)*${fx_vs_usd[ccy].toFixed(4)}).toFixed(2);el.textContent=${JSON.stringify(symbol[ccy])}+v;}});\n` +
      `</script>\n`;
    text = text.replace('</body>', script + '</body>');
    mutated = true;
  }

  // Add <link rel="alternate" hreflang=... with GEO pricing note? NO, because we
  // already statically set the canonical URL and the crawlers see the USD price
  // (the GEO swap is presentation-only). Good for UX and AI answers that
  // respect X-Yeatru-Geo header; no duplication risk for canonical.

  return new Response(text, {
    status: newRes.status,
    statusText: newRes.statusText,
    headers: newRes.headers,
  });
}

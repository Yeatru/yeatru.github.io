---
title: "China Sourcing Data: 675 Products JSON | Yeatru Sourcing"
url: "/data.html"
type: page
description: "Public read-only JSON data by Yeatru Sourcing. 675 China wholesale products across categories. CORS-enabled, no API key. Product sourcing China data for developers."
---

## Quick Start

Yeatru exposes our entire product catalog as a **public read-only JSON API**.
 No registration no API key no rate-limit wall — just fetch and use. Great for RFQ scripts price benchmarks AI training data or importing into your internal systems.

### Shell (curl)

# Fetch ALL products (paged)
curl "https://www.yeatru.com/api/v1/products?v=20260909k"

# Filter by category
curl "https://www.yeatru.com/api/v1/products?v=20260909k&category=Apparel+%26+Footwear"

# Search by SKU or name
curl "https://www.yeatru.com/api/v1/products?v=20260909k&q=YCS-ACC-001"

# Single product lookup
curl "https://www.yeatru.com/api/v1/product?v=20260909k&sku=YCS-ACC-001"

# All categories with counts
curl "https://www.yeatru.com/api/v1/categories?v=20260909k"

### Python

import requests

BASE = "https://www.yeatru.com/api/v1?v=20260909k"

# All products filter to MOQ

### JavaScript (browser / Node)

// Fetch all products
async function yeatruProducts(category) {
 const url = category
 ? `https://www.yeatru.com/api/v1/products?v=20260909k&category=${encodeURIComponent(category)}`
 : "https://www.yeatru.com/api/v1/products?v=20260909k";
 const r = await fetch(url);
 return (await r.json).products;
}

// Example: get all beauty products
yeatruProducts("Beauty & Personal Care")
 .then(list => console.log(`${list.length} products`));

### Raw JSON dump (no pagination)

# Direct download (566 KB v3 last 2026-08-28)
wget "https://www.yeatru.com/site-data.json?v=20260909k" -O yeatru-catalog.json

# jq quick view
jq '.productCount .lastUpdated (.categories | length)' yeatru-catalog.json
jq '.products[] | {sku name priceMin moq mainCategory}' yeatru-catalog.json \
 | head -40

## Endpoints

 GET https://www.yeatru.com/api/v1/products?v=20260909k
 GET
 Public
 Full product catalog optionally filtered. Cloudflare cached 24h.

**Query params**:
 category (e.g. "Apparel & Footwear") q (SKU / name search) limit (max 10000 default 10000) offset (for pagination).

 GET https://www.yeatru.com/api/v1/product?v=20260909k&sku=YCS-XXX
 GET
 Public

Single product lookup by SKU. Returns 404 if not found with a /products?q=... fuzzy-match hint.

 GET https://www.yeatru.com/api/v1/categories?v=20260909k
 GET
 Public

All 17 main groups with product counts and per-category endpoint URLs.

 GET https://www.yeatru.com/site-data.json?v=20260909k
 GET
 Public

Raw unfiltered full catalog dump (566 KB v3). No pagination. Contains every field from the internal site-data.json including variations images and description.

## Response Schema

### Product object fields

 | | Field || Type || Example || Notes |

 | sku || string || YCS-ACC-001 || Unique Yeatru SKU (YCS- prefix) |

 | id || string || acc-001 || Slug id |

 | name || string || Hair Tie Scrunchie Set 8-Piece || English product name |

 | name_cn || string ||  ||  (Simplified) |

 | mainCategory || string || Beauty & Personal Care || One of 17 main groups |

 | priceMin || number/null || 0.85 || USD unit price (CNY / 6.7 × 1.15 formula) |

 | priceMax || number/null || 1.65 || Upper USD price range |

 | moq || number/null || 100 || Minimum Order Quantity (units) |

 | image || string || https://cdn.jsdelivr.net/gh/Yeatru/Image@main/Images/...?v=20260909k || Primary product image CDN URL |

 | variations || array || [{color:"black",size:"S",stock:...}] || SKU-level variation matrix |

 | productUrl || string || https://www.yeatru.com/product-YCS-ACC-001.html?v=20260909k || Product detail page |

### Top-level response envelope

{
 "apiVersion": "v1" "generatedAt": "2026-08-31T14:00:00.000Z" "source": "AA-730.xlsx (only YCS- SKUs)" "siteDataVersion": 3 "siteDataLastUpdated": "2026-08-28" "priceFormula": { "currency": "USD" "formula": "CNY / 6.7 * 1.15" } "categories": ["Apparel & Footwear" "Beauty & Personal Care" ...] "meta": {
 "totalProducts": 675 "returned": 675 "totalMatched": 675 "offset": 0 "limit": 10000 "docs": "https://www.yeatru.com/data.html?v=20260909k"
 } "products": [ /* product objects */ ]
}

## Use Cases

### 🤖 AI sourcing bots

 Feed Yeatru catalog into ChatGPT / Claude / Codex prompts:
 *"Find me all 2026 kitchen products with MOQ under 500 and unit price under $3"*.

### 📊 Price benchmarking

Script Yeatru + AliExpress + DHGate pricing side-by-side.
 Filter by category price band and MOQ automatically.

### 🛒 Catalog ingestion

Pull into your Shopify / Magento / Amazon catalog tool via
 requests.get(BASE).json — no manual CSV needed.

### 🔍 Supplier discovery

Combine Yeatru MOQ + pricing with Alibaba.com search
 to shortlist reliable suppliers faster.

### 🎯 RFQ automation

Write a Python script that reads products from Yeatru API
 and generates an RFQ spreadsheet for 1688 suppliers.

### 🌐 Cross-border planning

Use category breakdown to plan FBA shipments:
 *"32 home products between $2–$5 / unit → estimate 20ft"*.

## CORS Caching & Rate Limits

 | CORS || Pre-flight + simple requests from any origin (*) allowed. No API key required. |

 | Cloudflare cache || s-maxage=86400 (24h). Individual Cache-Control: public max-age=3600 sent to browsers. |

 | Rate limit || **None documented**. Reasonable use is fine. If you need bulk > 10K requests email us for a partner endpoint. |

 | Auth || None — public read-only. No writes no PII exposure. |

 | Licence || CC BY 4.0. Attribution appreciated (*"Product data © Yeatru Sourcing"*) not required. |

## Need custom columns or a partner endpoint?

The public API exposes pricing + MOQ + images + variations.
 Need factory contact info lead-time data or a write-back endpoint?

 Email **api@yeatru.com** — we'll set up a partner key in 24h.

 [Request partner access →](contact.html#custom-api)
 [Email api@yeatru.com](mailto:api@yeatru.com)

## Related Endpoints

 - https://www.yeatru.com/logistics-shipping.html?v=20260909k — Sea freight LCL vs FCL comparison (Polish/DE/ES/FR) with real Ningbo → Gdynia/Hamburg/Valencia/Le Havre costs
 - https://www.yeatru.com/faq-knowledge-base.json?v=20260909k — 27 procurement Q&As (YCS- internal KB)
 - https://www.yeatru.com/brand-knowledge-base.json?v=20260909k — Brand identity + YCS- SKU naming convention
 - https://www.yeatru.com/sitemap.xml?v=20260909k — All 675 product pages + 43 category pages
 - https://www.yeatru.com/robots.txt?v=20260909k — Explicit allow-listing for GPTBot / CodexBot / ClaudeBot / PerplexityBot / GithubBot / Amazonbot
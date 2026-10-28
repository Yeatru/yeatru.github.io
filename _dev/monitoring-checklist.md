# Post-Deploy Monitoring Checklist (2–3 weeks)

Deploy commit: `3c83523` — pushed to `main` (GitHub Pages: www.yeatru.com)
IndexNow: 688 URLs pushed (HTTP 200) — 675 product pages + new blogs + core files

---

## Baseline → Target

| Metric | Source | Before | Target |
|---|---|---|---|
| Invalid Product snippets | GSC → Enhancements → Merchant listings / Product snippets | 1,278 | 0 |
| Missing `price`/`priceSpecification`/`offerCount` | GSC Product snippets | 1,278 | 0 |
| `shippingRate = 0` | Rich Results / Merchant listings | flagged | fixed (small-parcel model) |
| Duplicate without user-selected canonical | GSC → Pages | ~40 | ≤ 10 |
| New pages indexed | GSC → Pages | 0 | ≥ 5 indexed |
| Product page impressions | GSC → Performance | — | +upward trend |

---

## Week 1 — Validate crawl & fix flags

- [ ] GSC → **Page indexing**: confirm `?lang=es/fr/ru/ar` URLs drop out of "Duplicate without user-selected canonical". Submit `sitemap-static.xml` + `sitemap.xml` for re-crawl.
- [ ] GSC → **URL Inspection** on 2–3 sample product pages (e.g. `product-YCS-ACC-001.html`): check "Product snippets" = Valid, then click **Test live URL**.
- [ ] GSC → **Merchant listings / Product snippets**: watch valid count climb as Google re-crawls (expect movement in 3–7 days).
- [ ] Bing Webmaster Tools → **IndexNow**: confirm submitted URLs received (Reports → IndexNow, 200 OK).
- [ ] Bing → **URL Inspection** on new pages: `blog-ddu-vs-ddp-china.html`, `blog-eta-vs-etd-china.html`.
- [ ] Confirm the 2 new pages + France/Spain agent pages index within 3–5 days.

## Week 2 — Measure ranking & rich results

- [ ] GSC → **Performance**: filter queries `ddu vs ddp`, `dap vs ddp`, `eta vs etd`, `incoterms china` — note first impressions.
- [ ] GSC → **Rich Results report**: verify FAQPage valid on the incoterms/agent/country pages.
- [ ] Re-run Rich Results Test on one product page and confirm AggregateOffer + OfferShippingDetails parse.
- [ ] Bing AI Performance / Copilot: check whether yeatru.com is cited for "sourcing agent", "DDU vs DDP", "ETA vs ETD".
- [ ] Check GSC "Duplicate without user-selected canonical" trend — should keep falling.

## Week 3 — Consolidate & iterate

- [ ] Compare product-page CTR (was suppressed by snippet errors) vs baseline.
- [ ] Deprecate any remaining parameterised duplicate URLs: if `?product=` or `?lang=` still appear in GSC, tighten `robots.txt` and add `<link rel="canonical">` if missing.
- [ ] Decide next content targets from GSC query gaps (zero-impression high-intent terms).
- [ ] If product snippets still show errors, re-validate JSON-LD with Schema.org validator and adjust `shippingDetails` destinations.

---

## Quick verification commands

```bash
# Live status of new pages
curl -s -o /dev/null -w "%{http_code} %{url_effective}\n" \
  https://www.yeatru.com/blog-ddu-vs-ddp-china.html \
  https://www.yeatru.com/blog-eta-vs-etd-china.html

# Confirm sitemap contains new URLs
curl -s https://www.yeatru.com/sitemap-static.xml | grep -E 'ddu-vs-ddp|eta-vs-etd'

# Confirm product schema field live
curl -s https://www.yeatru.com/product-YCS-ACC-001.html | grep -c offerCount
```

## Key links

- GSC → Page indexing: https://search.google.com/search-console/index
- GSC → Sitemaps: https://search.google.com/search-console/sitemaps
- Rich Results Test: https://search.google.com/test/rich-results
- Schema validator: https://validator.schema.org/
- Bing Webmaster → IndexNow: https://www.bing.com/webmasters
- Bing AI Performance: https://www.bing.com/webmasters/aivisibility

## Escalation triggers (act immediately)

- Product snippet errors **increase** after 7 days → re-audit `offers` block (likely `priceSpecification` shape).
- New pages still not indexed at day 10 → check `robots.txt` + canonical, resubmit via URL Inspection.
- `?lang=` duplicates persist at day 14 → add `Disallow: /*?lang=` to `robots.txt`.

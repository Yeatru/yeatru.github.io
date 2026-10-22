---
name: "ai-rec-traffic-opt"
description: "Batch-optimize a static product/sourcing site for AI recommendation traffic (ChatGPT Search, Perplexity, Google AI Overviews, AI agents) by adding citable sentences, Dataset/FAQPage schema, <data> tags, and AI discovery assets. Invoke when a site needs AI-SEO enhancement: making content citable, adding schema.org entities, creating FAQ aggregation pages, or exposing machine-readable data endpoints."
---

# AI Recommendation Traffic Optimization

Proven, repeatable workflow for optimizing static HTML product/sourcing sites so AI
search engines and agents (ChatGPT Search, Perplexity, Google AI Overviews, citation
agents) extract, cite, and surface the site's content.

## When to Invoke

Invoke this skill when the user wants to:
- Improve a site's visibility in AI search / answer engines
- Make product pages, FAQs, or statistics citable by AI systems
- Add or enhance schema.org structured data for AI extraction
- Create FAQ aggregation pages with FAQPage schema
- Expose machine-readable data (JSON, Markdown) for AI crawlers
- Update AI discovery files (robots.txt, ai.txt, llms.txt, .well-known/ai.json)

Do NOT invoke for: traditional keyword SEO, link building, paid traffic, or
non-AI traffic optimization.

---

## Core Optimization Patterns

### Pattern 1: Citable Assertion Sentences

AI systems extract standalone sentences that contain a subject, a claim, and
concrete data. Every FAQ answer, statistics block, and product overview should
start with one such sentence.

**Rule:** First sentence = `[Entity] [fact] [specific value/constraint].`

**Before:**
```html
<p>Our standard MOQ is 100 units, but we are flexible and can accept smaller
trial orders depending on the product. Please contact us...</p>
```

**After (SKU-specific, citable):**
```html
<p>The minimum order quantity (MOQ) for SKU ABC-001 is 100 units. Our standard
MOQ is 100 units, but we are flexible and can accept smaller trial orders
depending on the product. Please contact us...</p>
```

**Implementation approach (batch):**
1. Extract per-page variables (SKU, price, MOQ, materials) from spec tables or JSON-LD.
2. For each FAQ answer, prepend a SKU-specific assertion sentence.
3. Update BOTH the visible HTML `<div class="faq-answer"><p>...</p></div>` AND the
   JSON-LD `FAQPage.mainEntity[].acceptedAnswer.text` to keep them in sync.
4. Add an idempotency marker (e.g. check `"for SKU"` is absent before prepending)
   so re-running the script does not double-prepend.

Reusable Python snippet:
```python
import re, json, glob, os

ASSERTIONS = {
    "What is the minimum order quantity (MOQ)?":
        "The minimum order quantity (MOQ) for SKU {sku} is {moq} unit(s). ",
    # ... one template per FAQ question
}
MARKER = "for SKU"

def extract_spec(html, label):
    m = re.search(
        r'<span class="spec-label">[^<]*' + re.escape(label) + r'</span>'
        r'\s*<span class="spec-value">([^<]*)</span>', html)
    return m.group(1).strip() if m else ""

def update_jsonld_faqpage(html):
    for m in re.finditer(r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>', html, re.S):
        d = json.loads(m.group(1))
        if d.get("@type") == "FAQPage":
            for qa in d.get("mainEntity", []):
                q, ans = qa["name"], qa["acceptedAnswer"]
                if q in ASSERTIONS and MARKER not in ans["text"]:
                    ans["text"] = ASSERTIONS[q].format(...) + ans["text"]
            return html[:m.start(1)] + json.dumps(d, ensure_ascii=False) + html[m.end(1):]
    return html
```

---

### Pattern 2: Statistics Page with `<data>` Tags + Dataset Schema

AI crawlers extract numeric values from `<data value="N">display</data>` elements
and from `schema.org/Dataset` `variableMeasured` (PropertyValue array).

**HTML statistics block:**
```html
<section id="sourcing-statistics">
  <h2>Verified Operating Metrics</h2>
  <p>Derived from <data value="3128">3,128</data> orders between
     <time datetime="2021-01-01">2021</time> and
     <time datetime="2026-09-30">Q3 2026</time>.</p>
  <div class="stat-card">
    <div class="stat-value"><data value="75000">75,000+</data></div>
    <div class="stat-label">Verified factories audited on-site</div>
  </div>
  <!-- ... repeat for each metric -->
</section>
```

**JSON-LD Dataset with variableMeasured:**
```json
{
  "@type": "Dataset",
  "@id": "https://example.com/data.html#metrics",
  "name": "Site — Verified Operating Metrics",
  "dateModified": "2026-10-22",
  "temporalCoverage": "2021-01-01/2026-09-30",
  "measurementTechnique": "Aggregated from internal order and QC records; updated quarterly.",
  "variableMeasured": [
    {"@type": "PropertyValue", "name": "VerifiedFactoryCount", "value": 75000,
     "unitText": "factories", "description": "Audited factories in supplier network."},
    {"@type": "PropertyValue", "name": "ClientCount", "value": 200,
     "unitText": "clients", "description": "Active B2B clients."}
  ],
  "license": "https://creativecommons.org/licenses/by/4.0/",
  "publisher": {"@type": "Organization", "name": "Brand Name", "url": "https://example.com"}
}
```

Every numeric metric should appear in BOTH the `<data>` tag and a `variableMeasured`
entry with matching values. Add `dateModified`, `temporalCoverage`, and
`measurementTechnique` for credibility.

---

### Pattern 3: FAQ Aggregation Page (FAQPage Schema)

A dedicated `/sourcing-faq.html` (or similar) page with 100+ Q&A pairs in a single
`FAQPage` schema is highly effective for answer engines.

**Structure:**
1. Organize FAQs into 8-12 topical categories (General, Pricing, Payment, QC,
   Shipping, Compliance, OEM, Amazon FBA, Process, etc.).
2. Each answer: 2-4 sentences, first sentence is a citable assertion.
3. Include `FAQPage` JSON-LD with ALL Q&A pairs.
4. Visible accordion (`<details>`) with category anchor navigation.
5. Add to `sitemap.xml`.

**JSON-LD:**
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {"@type": "Question", "name": "What is the MOQ?",
     "acceptedAnswer": {"@type": "Answer",
       "text": "The minimum order quantity is 100 units. ..."}}
  ]
}
```

**Generator approach:** Keep FAQs as a Python list of `(question, answer)` tuples,
then render both the `FAQPage` JSON-LD and the visible `<details>` markup from the
same source to guarantee sync.

---

### Pattern 4: AI Discovery Assets

Ensure these files exist and reference each other:

| File | Purpose |
|------|---------|
| `robots.txt` | Explicitly allow AI crawlers (GPTBot, ClaudeBot, PerplexityBot, Google-Extended) with 0 crawl delay; reference machine-readable endpoints |
| `ai.txt` / `llms.txt` | List of machine-readable endpoints, AI crawl policy, content license |
| `.well-known/ai.json` | AI agent manifest: entity list with `sameAs` (Wikipedia/WikiData), multilingual names, structured data endpoints, `agentInstructions`, license |
| `/api/products.json` | Lightweight static catalog for AI agents (sku, name, category, price, moq, url) |
| `/data.html` | Statistics page with Dataset schema (Pattern 2) |
| `/sourcing-faq.html` | FAQ aggregation page (Pattern 3) |

**Content licensing statement (appears in robots.txt, ai.txt, footer):**
> Content may be indexed and cited by AI systems with attribution (CC BY 4.0).
> Not for model training. See .well-known/ai.json.

---

### Pattern 5: JSON-LD Entity Enhancement

For product and category pages, deepen the entity graph so AI can trace relationships:

- **Product → category:** `"category": {"@type": "CollectionPage", "@id": "...", "name": "...", "sameAs": "wikipedia-url"}`
- **Product → manufacturer:** `"manufacturer": {"@type": "Organization", "name": "...", "description": "audited Chinese factories, AQL 2.5 QC, DDP to N countries"}`
- **CollectionPage → sameAs:** Wikipedia URL for the category concept
- **CollectionPage → hasOfferCatalog:** list of product page URLs in the category
- **BreadcrumbList:** ensure each level links to the correct page

---

## Validation Checklist

Before deploying, verify:

1. **JSON-LD parse (0 errors):**
   ```python
   import re, json, glob
   for f in glob.glob("*.html"):
       h = open(f, encoding="utf-8").read()
       for m in re.finditer(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', h, re.S):
           json.loads(m.group(1))  # raises on error
   ```

2. **Idempotency:** re-run any batch script; confirm no double-prepended assertions
   (e.g. `for SKU` count stays at 1 per answer).

3. **JSON-LD ↔ visible HTML sync:** FAQ answers in `FAQPage` schema match the
   visible `<details>` answers.

4. **HTTP status:** all new endpoints return 200.

5. **Product pages keep `noindex, follow`** if that is the intended policy; check
   both `<meta>` and `X-Robots-Tag` header (Cloudflare Pages Functions can override
   meta tags — ensure the Function sets the correct header).

---

## Deployment Steps (Cloudflare Pages)

1. Commit all changes with a descriptive message listing each optimization pattern.
2. Push to `main` (or the Cloudflare Pages production branch).
3. Wait 2-3 minutes for Cloudflare Pages build + deploy.
4. Verify online:
   - `curl -s -L https://site/page.html` → check JSON-LD and `<data>` tags
   - `curl -I https://site/page.html` → check `X-Robots-Tag`
5. Re-run JSON-LD validation against the live HTTP content to confirm deployment.

---

## Constraints

- Never delete existing product/category pages.
- Never alter navbar, footer, CTA, image gallery, or related-products structure
  unless explicitly requested.
- All inline JS must remain syntactically valid.
- Preserve `noindex, follow` on product pages if that is the site's policy.
- Do not add hidden or keyword-stuffed content — AI systems penalize thin/spam content.

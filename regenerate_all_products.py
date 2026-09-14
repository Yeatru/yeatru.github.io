#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Regenerate all-products.html with card grid layout.
- Converts product list rows to responsive card grid (3-4 per row)
- Each card shows: thumbnail, SKU, MOQ, price
- Removes all Chinese text from category names
- Mobile optimized
"""

import json
import re
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
HTML_PATH = os.path.join(ROOT, "all-products.html")
DATA_PATH = os.path.join(ROOT, "site-data.json")

CNY_TO_USD_RATE = 6.7
PRICE_MARKUP = 1.15

# Load product data
with open(DATA_PATH, "r", encoding="utf-8") as f:
    site_data = json.load(f)

# Build SKU -> product lookup with USD price
sku_lookup = {}
for p in site_data["products"]:
    sku = p["sku"]
    price_min_usd = (p.get("priceMin", 0) or 0) / CNY_TO_USD_RATE * PRICE_MARKUP
    price_max_usd = (p.get("priceMax", 0) or 0) / CNY_TO_USD_RATE * PRICE_MARKUP
    sku_lookup[sku] = {
        "name": p.get("name", ""),
        "image": p.get("image", ""),
        "priceMin": price_min_usd,
        "priceMax": price_max_usd,
        "moq": p.get("moq", 0),
        "description": p.get("description", ""),
        "dateAdded": p.get("dateAdded", ""),
    }

# Read existing HTML
with open(HTML_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# --- Extract header (everything before first <section class="mb-5">) ---
first_section_pos = html.find('    <section class="mb-5">')
header = html[:first_section_pos]

# --- Extract footer (everything after last product section) ---
# Find the "Why Yeatru" card section which comes after all product sections
why_yeatru_pos = html.find('<div class="card border-0 bg-light mb-4">\n    <div class="card-body p-4">\n      <h3 class="h5 mb-3"><i class="fas fa-shield-alt')
footer = html[why_yeatru_pos:]

# --- Parse all product sections from existing HTML ---
# Each section: <section class="mb-5"> ... <h2 id="cat-XXX">Name</h2> ... products ... </section>
section_pattern = re.compile(
    r'<section class="mb-5">\s*'
    r'<div class="d-flex[^>]*>\s*'
    r'<h2 id="cat-([^"]+)"[^>]*>(?:<i[^>]*></i>\s*)?(.+?)\s*<small',
    re.DOTALL
)

# Parse each product row from existing HTML
# Pattern for each product row
row_pattern = re.compile(
    r'<div class="row g-0 py-2[^"]*"[^>]*>\s*'
    r'<div class="col-auto p-2"><img src="([^"]+)"[^>]*alt="([^"]*)"[^>]*></div>\s*'
    r'<div class="col px-2">\s*'
    r'<a href="([^"]+)"[^>]*title="([^"]*)"[^>]*>([^<]+)</a>',
    re.DOTALL
)

# Find all sections with their products
sections_html = html[first_section_pos:why_yeatru_pos]

# Split into individual sections
section_blocks = re.split(r'(<section class="mb-5">)', sections_html)
# Reconstruct: section_blocks = ['', '<section class="mb-5">', content1, '<section class="mb-5">', content2, ...]
sections = []
for i in range(1, len(section_blocks), 2):
    if i + 1 < len(section_blocks):
        section_html = section_blocks[i] + section_blocks[i + 1]
        # Extract category code and name
        cat_match = section_pattern.search(section_html)
        if cat_match:
            cat_code = cat_match.group(1)
            cat_name_raw = cat_match.group(2).strip()
            # Remove Chinese: strip anything in parentheses that contains CJK
            cat_name = re.sub(r'\s*\([^)]*[\u4e00-\u9fff][^)]*\)', '', cat_name_raw).strip()
            # Extract products from site-data.json by matching SKU prefix to cat_code
            # (e.g. cat_code "YCS-ACC" matches SKUs "YCS-ACC-001", "YCS-ACC-002", ...)
            products = []
            for p in site_data["products"]:
                sku = p.get("sku", "")
                if sku.startswith(cat_code + "-") or sku == cat_code:
                    products.append({
                        "sku": sku,
                        "name": p.get("name", ""),
                        "image": p.get("image", ""),
                        "priceMin": (p.get("priceMin", 0) or 0) / CNY_TO_USD_RATE * PRICE_MARKUP,
                        "priceMax": (p.get("priceMax", 0) or 0) / CNY_TO_USD_RATE * PRICE_MARKUP,
                        "moq": p.get("moq", 0),
                        "description": p.get("description", ""),
                        "dateAdded": p.get("dateAdded", ""),
                        "link": f"product-{sku}.html",
                    })
            sections.append({
                "code": cat_code,
                "name": cat_name,
                "name_raw": cat_name_raw,
                "products": products,
            })

print(f"Parsed {len(sections)} categories with {sum(len(s['products']) for s in sections)} products")

# --- Generate card grid HTML ---
def fmt_price(p):
    """Format price range as USD string."""
    lo = p.get("priceMin", 0)
    hi = p.get("priceMax", 0)
    if lo == 0 and hi == 0:
        return "Request Quote"
    if abs(lo - hi) < 0.001:
        return f"${lo:.2f}"
    return f"${lo:.2f}–${hi:.2f}"

def get_sku_from_link(link):
    """Extract SKU from product link like product-YCS-ACC-001.html"""
    m = re.search(r'product-([A-Z0-9-]+)\.html', link)
    return m.group(1) if m else ""

def get_product_image(sku, existing_img):
    """Get best image URL: prefer CDN from site-data, fallback to existing."""
    if sku in sku_lookup and sku_lookup[sku].get("image"):
        return sku_lookup[sku]["image"]
    return existing_img

card_grid_html = ""
for sec in sections:
    cat_code = sec["code"]
    cat_name = sec["name"]
    products = sec["products"]
    count = len(products)

    # Category query param for gallery link
    cat_param = cat_code.lower().replace("-", "")

    # Sort products by dateAdded descending (newest first) — default sort order
    products.sort(key=lambda p: p.get("dateAdded", ""), reverse=True)

    section_html = f'''    <section class="mb-5">
      <div class="d-flex flex-wrap align-items-baseline justify-content-between mb-3 gap-2">
        <h2 id="cat-{cat_code}" class="h4 mb-0"><i class="fas fa-cube me-2 text-indigo"></i>{cat_name} <small class="text-muted ms-2">({count} SKUs)</small></h2>
        <a href="products.html?category={cat_param}" class="btn btn-sm btn-outline-primary rounded-pill"><i class="fas fa-th me-1"></i> Gallery View</a>
      </div>
      <div class="row g-3 g-md-4 product-catalog-grid">
'''
    for prod in products:
        sku = prod["sku"]
        img = prod["image"]
        price_str = fmt_price(prod)
        moq = prod.get("moq", 0)
        moq_str = str(moq) if moq and moq > 0 else "Contact"
        title = prod["name"]
        link = prod["link"]
        desc = prod.get("description", "") or title
        desc = re.sub(r'<[^>]+>', '', desc)
        if len(desc) > 120:
            desc = desc[:117].rsplit(' ', 1)[0] + '...'
        price_min = prod.get("priceMin", 0)
        date_added = prod.get("dateAdded", "")

        section_html += f'''        <div class="col-6 col-sm-6 col-md-4 col-lg-3 col-xl-3 pc-card" data-sku="{sku}" data-price="{price_min}" data-date="{date_added}" data-name="{title.lower()}">
          <div class="product-catalog-card">
            <a href="{link}" class="product-catalog-img-link" title="{title}">
              <div class="product-catalog-img">
                <img src="{img}" alt="{title}" loading="lazy" decoding="async" onerror="this.src='https://www.yeatru.com/Images/loading.jpg';">
              </div>
            </a>
            <div class="product-catalog-body">
              <div class="product-catalog-meta">
                <span class="product-catalog-sku"><i class="fas fa-barcode"></i> {sku}</span>
                <span class="product-catalog-moq"><i class="fas fa-box"></i> MOQ: {moq_str}</span>
              </div>
              <h3 class="product-catalog-title"><a href="{link}">{title}</a></h3>
              <p class="product-catalog-desc">{desc}</p>
              <div class="product-catalog-footer">
                <span class="product-catalog-price">{price_str}</span>
                <a href="contact.html?product={sku}" class="product-catalog-quote"><i class="fas fa-file-invoice-dollar"></i> Get a Quote</a>
              </div>
            </div>
          </div>
        </div>
'''

    section_html += '''      </div>
    </section>

'''
    card_grid_html += section_html

# --- Update category pills in header (remove Chinese) ---
# The pills are in the header section. Remove Chinese from category names in pills.
def strip_chinese(text):
    return re.sub(r'\s*\([^)]*[\u4e00-\u9fff][^)]*\)', '', text).strip()

# Update the toc-pill links
header = re.sub(
    r'(<a href="#cat-[^"]+">)([^<]+?)(\s*<span)',
    lambda m: m.group(1) + strip_chinese(m.group(2)) + m.group(3),
    header
)

# Also clean any remaining Chinese in the header
header = re.sub(r'\s*\([^)]*[\u4e00-\u9fff][^)]*\)', '', header)

# --- Reassemble the full HTML ---
new_html = header + card_grid_html + footer

# Final pass: remove any remaining Chinese characters in category context
# (but be careful not to remove Chinese in product names/descriptions if any)
# Actually user wants ALL Chinese removed. Let's remove Chinese in parentheses everywhere
# and also standalone CJK in visible text. But product names might have CJK?
# site-data has name_cn fields but the HTML names should be English.
# Let's remove any CJK characters that are in parentheses (category labels)
new_html = re.sub(r'\([^)]*[\u4e00-\u9fff][^)]*\)', '', new_html)

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(new_html)

print(f"Done. Wrote {len(new_html)} bytes to {HTML_PATH}")
print(f"Categories: {len(sections)}")
print(f"Total products: {sum(len(s['products']) for s in sections)}")

#!/usr/bin/env python3
"""
Batch generator for Yeatru product detail pages.
Reads site-data.json and generates individual product-<SKU>.html files
with proper pricing (USD = CNY / 6.7 * 1.15), variants, SEO metadata,
and related product links.
"""

import json
import os
import sys
import html
from datetime import datetime

SITE_ROOT = "/workspace/yeatru.github.io"
SITE_DATA_PATH = os.path.join(SITE_ROOT, "site-data.json")
PRODUCTS_DIR = SITE_ROOT

CNY_TO_USD_RATE = 6.7
PRICE_MARKUP = 1.15

EXCHANGE_RATES = {
    "USD": {"rate": 1, "symbol": "$", "name": "USD"},
    "EUR": {"rate": 0.92, "symbol": "€", "name": "EUR"},
    "GBP": {"rate": 0.79, "symbol": "£", "name": "GBP"},
    "RUB": {"rate": 92.5, "symbol": "₽", "name": "RUB"},
    "CNY": {"rate": 7.25, "symbol": "¥", "name": "CNY"},
}


def generate_meta_description(product):
    sku = product["sku"]
    name = product["name"]
    category = product.get("category", "")
    price_min = product.get("priceMin", 0)
    price_max = product.get("priceMax", price_min)
    moq = product.get("moq", 1)
    variations = product.get("variations", [])

    usd_min = cny_to_usd(price_min)
    usd_max = cny_to_usd(price_max)

    colors = list(set(v.get("color", "") for v in variations if v.get("color")))
    sizes = list(set(v.get("size", "") for v in variations if v.get("size")))
    color_info = f", colors: {', '.join(colors[:2])}" if colors else ""
    size_info = f", sizes: {', '.join(sizes[:2])}" if sizes else ""

    if usd_min is not None and usd_max is not None:
        if abs(usd_min - usd_max) < 0.001:
            price_text = f"${usd_min:.2f}"
        else:
            price_text = f"${usd_min:.2f}-${usd_max:.2f}"
    else:
        price_text = "contact"

    sku_short = sku.replace("YCS-", "")

    # Build template parts
    header = "{name} wholesale from China. "
    price_part = f"Price: {price_text} USD, MOQ {moq} pcs{color_info}{size_info}. "
    verify_part = "Verified manufacturer. SKU:" + sku_short + ". "
    footer = "Yeatru Sourcing - trusted China agent for 200+ importers. Factory-direct prices, OEM/ODM, global shipping."

    # Calculate fixed parts length
    fixed_len = len(header.format(name="")) + len(price_part) + len(verify_part) + len(footer)

    # Calculate max name length to keep total <= 160
    max_name_len = 160 - fixed_len
    if max_name_len < 20:
        max_name_len = 20

    safe_name = name if len(name) <= max_name_len else name[:max_name_len].rsplit(" ", 1)[0]
    if not safe_name:
        safe_name = name[:max_name_len]

    desc = (
        f"{safe_name} wholesale from China. "
        f"Price: {price_text} USD, MOQ {moq} pcs{color_info}{size_info}. "
        f"Verified manufacturer. SKU:{sku_short}. "
        f"Yeatru Sourcing - trusted China agent for 200+ importers. "
        f"Factory-direct prices, OEM/ODM, global shipping."
    )

    if len(desc) > 160:
        desc = desc[:157].rsplit(" ", 1)[0] + "..."

    # Fallback: if still < 150, add category context
    if len(desc) < 150 and category:
        desc += f" Category: {category}."
        if len(desc) > 160:
            desc = desc[:157].rsplit(" ", 1)[0] + "..."

    return desc


def generate_title(product):
    sku = product["sku"]
    name = product["name"]
    category = product.get("category", "")
    sku_short = sku.replace("YCS-", "")

    title = f"{name} Wholesale Supplier | Yeatru [{sku_short}]"

    if len(title) > 70:
        title = f"{name} Wholesale | Yeatru [{sku_short}]"
        if len(title) > 70:
            title = f"{name[:55].rsplit(' ', 1)[0]}... | Yeatru [{sku_short}]"

    return title


def cny_to_usd(cny_value):
    try:
        return (float(cny_value) / CNY_TO_USD_RATE) * PRICE_MARKUP
    except (ValueError, TypeError):
        return None


def format_usd(usd_value, decimals=2):
    try:
        return f"${usd_value:.{decimals}f}"
    except (ValueError, TypeError):
        return "—"


def escape_attr(value):
    return html.escape(str(value), quote=True)


def escape_text(value):
    return html.escape(str(value), quote=False)


def slugify_category(cat):
    return cat.replace("&", "and").replace("/", "-").strip()


def get_related_products(product, all_products, limit=5):
    same_category = [p for p in all_products
                    if p["category"] == product["category"]
                    and p["sku"] != product["sku"]]
    if len(same_category) >= limit:
        return same_category[:limit]
    other_cats = [p for p in all_products
                  if p["category"] != product["category"]
                  and p["sku"] != product["sku"]]
    return (same_category + other_cats)[:limit]


def generate_related_section(product, all_products):
    related = get_related_products(product, all_products, 5)
    if not related:
        return ""

    cards_html = ""
    for rp in related:
        rp_usd = cny_to_usd(rp.get("priceMin", 0))
        rp_price_display = format_usd(rp_usd) if rp_usd is not None else "—"
        rp_price_attr = f"{rp_usd:.6f}" if rp_usd is not None else "0"
        rp_image = escape_attr(rp.get("image", ""))
        rp_name = escape_text(rp.get("name", rp["sku"]))
        rp_sku = escape_text(rp.get("sku", ""))
        rp_href = escape_attr(f"product-{rp['sku']}.html")

        cards_html += f'''
      <a class="related-product-card" href="{rp_href}">
        <img src="{rp_image}" alt="{rp_name}" loading="lazy" decoding="async" class="img-fluid" onerror="this.style.display='none'">
        <div class="related-product-info">
          <h3>{rp_name}</h3>
          <div class="related-product-meta">SKU: {rp_sku}</div>
          <div class="related-product-price"><span class="variation-price" data-usd-price="{rp_price_attr}">{rp_price_display}</span></div>
        </div>
      </a>'''

    return f'''
  <div class="related-products-section">
    <h2 class="related-section-title"><i class="fas fa-th-large me-2"></i> Related Products</h2>
    <div class="related-products-grid">{cards_html}
    </div>
  </div>'''


def generate_variations_section(product):
    variations = product.get("variations", [])
    if not variations or len(variations) <= 1:
        return ""

    cards_html = ""
    for i, var in enumerate(variations):
        v_price = var.get("price", product.get("priceMin", 0))
        v_usd = cny_to_usd(v_price)
        v_name = var.get("color", "") or var.get("size", "") or f"Variant {i+1}"
        v_size = var.get("size", "")
        v_color = var.get("color", "")
        v_price_attr = f"{v_usd:.6f}" if v_usd is not None else "0"
        v_price_display = format_usd(v_usd) if v_usd is not None else "—"
        v_selected = " selected" if i == 0 else ""
        v_color_style = f' style="background-color: {v_color};"' if v_color else ""

        cards_html += f'''
        <div class="variation-card{v_selected}" role="button" tabindex="0"
             data-variant-price-usd="{v_price_attr}"
             data-variant-name="{escape_attr(v_name)}"
             data-variant-color="{escape_attr(v_color)}"
             data-variant-size="{escape_attr(v_size)}">
          <div class="variation-info">
            {f'<span class="variation-color-dot"{v_color_style}></span>' if v_color else '<span class="variation-color-dot"></span>'}
            <span class="variation-name">{escape_text(v_name)}</span>
            {f'<span class="variation-size">{escape_text(v_size)}</span>' if v_size else ''}
          </div>
          <span class="variation-price">{v_price_display}</span>
        </div>'''

    return f'''
    <div class="variations-display" style="display:block;">
      <div class="variations-display-title"><i class="fas fa-palette me-1"></i> Available Options</div>
      <div class="variations-list">{cards_html}
      </div>
    </div>'''


def generate_price_display(product):
    price_min = product.get("priceMin", 0)
    price_max = product.get("priceMax", price_min)
    usd_min = cny_to_usd(price_min)
    usd_max = cny_to_usd(price_max)

    if usd_min is None or usd_max is None:
        return ('<span class="variation-price detail-price-hero" data-usd-price="0">'
                'Contact for price</span>')

    if abs(usd_min - usd_max) < 0.001:
        price_display = format_usd(usd_min)
        price_attr = f"{usd_min:.6f}"
    else:
        price_display = f"{format_usd(usd_min)} - {format_usd(usd_max)}"
        price_attr = f"{usd_min:.6f}-{usd_max:.6f}"

    return (f'<span class="variation-price detail-price-hero" '
            f'data-usd-price="{price_attr}">{price_display}</span>')


def generate_detail_spec_table(product):
    price_min = product.get("priceMin", 0)
    price_max = product.get("priceMax", price_min)
    usd_min = cny_to_usd(price_min)
    usd_max = cny_to_usd(price_max)

    if usd_min is None or usd_max is None:
        price_inner = "Contact for price"
    elif abs(usd_min - usd_max) < 0.001:
        price_inner = generate_price_display(product)
    else:
        price_inner = generate_price_display(product)

    material = escape_text(product.get("material", "See specifications"))
    size = escape_text(product.get("size", "—"))
    moq = escape_text(str(product.get("moq", "1")))

    return f'''
<div class="table-responsive detail-spec-wrap">
<table class="detail-spec-table">
  <tr class="spec-price-row"><th scope="row">WHOLESALE PRICE</th><td class="spec-price-cell"><div id="detailPriceDisplay">{price_inner}</div><div class="spec-price-hint">Factory-direct · CNY ÷ 6.7 × 1.15 · MOQ {moq}</div></td></tr>
  <tr><th scope="row">Material</th><td>{material}</td></tr>
  <tr><th scope="row">Size / Dimensions</th><td>{size}</td></tr>
  <tr><th scope="row">Minimum Order</th><td><b>{moq}</b> piece(s) · OEM custom from 200 pcs</td></tr>
</table>
</div>'''


def generate_json_ld_product(product):
    price_min = product.get("priceMin", 0)
    price_max = product.get("priceMax", price_min)
    usd_min = cny_to_usd(price_min)
    usd_max = cny_to_usd(price_max)
    sku = escape_attr(product["sku"])
    name = escape_attr(product["name"])
    image = escape_attr(product.get("image", ""))
    desc = escape_attr(product.get("description", ""))
    category = escape_attr(product.get("category", ""))
    moq = escape_attr(str(product.get("moq", "1")))

    low_price = f"{usd_min:.2f}" if usd_min is not None else "0"
    high_price = f"{usd_max:.2f}" if usd_max is not None else low_price

    return f'''<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Product","sku":"{sku}","productID":"{sku}","name":"{name}","description":"{desc}","image":["{image}"],"brand":{{"@type":"Brand","name":"Yeatru Sourcing"}},"category":"{category}","material":"See specifications","color":"Multiple options available","offers":{{"@type":"Offer","url":"https://www.yeatru.com/product-{sku}.html","priceCurrency":"USD","price":"{low_price}","highPrice":"{high_price}","lowPrice":"{low_price}","offerCount":1,"availability":"https://schema.org/InStock","itemCondition":"https://schema.org/NewCondition","availableDeliveryMethod":["https://schema.org/LockerDelivery","https://schema.org/OnSitePickup","https://schema.org/ParcelService"],"businessFunction":"http://purl.org/goodrelations/v1#Sell","eligibleQuantity":{{"@type":"QuantitativeValue","minValue":{moq},"unitCode":"H87"}},"seller":{{"@id":"https://www.yeatru.com/#organization"}}}},"manufacturer":{{"@id":"https://www.yeatru.com/#localbusiness"}},"additionalProperty":[{{"@type":"PropertyValue","name":"Minimum Order Quantity","value":"{moq} pieces per SKU (off-the-shelf items); OEM MOQs higher"}},{{"@type":"PropertyValue","name":"Lead Time for Stock Items","value":"3 - 7 business days from order confirmation to dispatch"}},{{"@type":"PropertyValue","name":"Lead Time for OEM Orders","value":"15 - 30 business days depending on tooling complexity"}},{{"@type":"PropertyValue","name":"Accepted Payment","value":"T/T (Bank Transfer), PayPal, Alibaba Trade Assurance, Western Union"}}]}}</script>'''


# AA-730 sub-category -> UI main category (17 buttons on products.html).
# Keep in sync with app.js -> SUB_TO_MAIN_CATEGORY + resolveMainCategory().
_SUB_TO_MAIN_CATEGORY = {
    "Clothing":"Apparel & Footwear","Shoes":"Apparel & Footwear","Swimwear":"Apparel & Footwear",
    "Socks":"Apparel & Footwear","Hair Accessories":"Apparel & Footwear","Footwear":"Apparel & Footwear",
    "Auto Repair Tools":"Auto Parts & Tools","Auto Accessories":"Auto Parts & Tools",
    "Toys":"Baby & Toys","Baby Care":"Baby & Toys","Kids":"Baby & Toys",
    "Bags":"Bags & Luggage","Backpacks":"Bags & Luggage",
    "Skin Care":"Beauty & Personal Care","Beauty":"Beauty & Personal Care",
    "Personal Care":"Beauty & Personal Care","Massage":"Beauty & Personal Care",
    "Microphones/Audio":"Digital Electronics","Audio/Electronics":"Digital Electronics",
    "Smart Electronics":"Digital Electronics","Audio/Video":"Digital Electronics",
    "Electronics":"Digital Electronics","Tablets":"Digital Electronics",
    "Hardware":"Hardware & Home","Locks":"Hardware & Home",
    "Home & Garden":"Home & Daily Living","Household":"Home & Daily Living",
    "Cleaning":"Home & Daily Living","Lighting":"Home & Daily Living",
    "Storage & Organization":"Home & Daily Living","Fans":"Home & Daily Living",
    "Kitchen/Bath":"Home & Daily Living",
    "Dry Goods":"Home Appliances",
    "Kitchen Storage":"Kitchen Supplies","Kitchen Tools":"Kitchen Supplies","Cups & Drinkware":"Kitchen Supplies",
    "Material":"Material","OFC":"Material","KAP":"Material","MSF":"Material","PET":"Material",
    "Musical Instruments":"Musical Instruments",
    "Other":"Others","Photography":"Others","Machinery":"Others","Outdoor":"Sports & Outdoor",
    "Fashion Jewelry":"Others","Jewelry":"Others","Home Textile":"Home & Daily Living",
    "Dog Supplies":"Pet Supplies","Pet Supplies":"Pet Supplies",
    "Mobile Accessories":"Phone Accessories","Screen Protectors":"Phone Accessories",
    "Fitness":"Sports & Outdoor","Camping":"Sports & Outdoor","Tents":"Sports & Outdoor",
    "Stationery":"Stationery & Office",
}

# Per-SKU hard overrides (highest priority). Matches app.js JEWELRY_SKUS +
# any miscategorized items we've manually identified in AA-730.
_SKU_MAIN_CATEGORY_OVERRIDE = {
    # --- Fashion jewelry (previously "Accessories" → wrongly Apparel) ---
    "YCS-ACC-002": "Others",   # Bracelet Gift Box Jewelry Velvet
    "YCS-ACC-006": "Others",   # Necklace Jewelry Fashion Gift
    # --- Tents: sub=Outdoor, previously Others → should be Sports & Outdoor ---
    "YCS-OUT-001": "Sports & Outdoor",
    "YCS-OUT-002": "Sports & Outdoor",
    "YCS-OUT-003": "Sports & Outdoor",
}

# Keyword rules applied to (category + " " + name).lower() for finer-grained
# category routing than the generic sub-category map alone.
def _keyword_main_category(sub_category, name, sku):
    blob = f"{sub_category} {name}".lower()
    sku_u = (sku or "").upper()
    # Fashion jewelry
    if "jewelry" in blob or "necklace" in blob or "bracelet" in blob or \
       "earring" in blob or "pendant" in blob:
        return "Others"
    # Outdoor sports
    if "tent" in blob or "camping" in blob or "hiking" in blob:
        return "Sports & Outdoor"
    # Phone accessories (charger / cable / power bank / case / screen protector)
    if (sku_u.startswith("YCS-MCH-") or sku_u.startswith("YCS-OTH-") or
        sku_u.startswith("YCS-ACC-")):
        if ("phone" in blob and ("case" in blob or "cover" in blob)) or \
           "power bank" in blob or "charger" in blob or "charging cable" in blob or \
           "usb cable" in blob or "data cable" in blob or "magnetic phone" in blob or \
           "screen protector" in blob:
            return "Phone Accessories"
    # Beauty & Personal Care (tools that were caught under broader subcats)
    if "hair clipper" in blob or "curling iron" in blob or "hair styler" in blob or \
       "hair tie" in blob or "scrunchie" in blob or "makeup blender" in blob or \
       "beauty tool" in blob or "shampoo dispenser" in blob or "cosmetic" in blob:
        return "Beauty & Personal Care"
    return None

def resolve_main_category(product):
    """Return the 17-item UI main category for breadcrumb links + product filters."""
    sku = product.get("sku", "")
    # 1) Hard per-SKU override
    if sku in _SKU_MAIN_CATEGORY_OVERRIDE:
        return _SKU_MAIN_CATEGORY_OVERRIDE[sku]
    # 2) Keyword rules (take precedence over a catch-all sub-category map entry)
    sub = product.get("category", "")
    name = product.get("name", "")
    kw = _keyword_main_category(sub, name, sku)
    if kw:
        return kw
    # 3) Existing mainCategory (if valid UI category)
    main = product.get("mainCategory")
    if isinstance(main, str) and main and main in _SUB_TO_MAIN_CATEGORY.values():
        return main
    # 4) Sub-category → main category lookup
    if sub and sub in _SUB_TO_MAIN_CATEGORY:
        return _SUB_TO_MAIN_CATEGORY[sub]
    # Generic "Accessories" (uncategorized) → Others per user feedback
    if sub == "Accessories":
        return "Others"
    return "Others"


def generate_json_ld_breadcrumb(product):
    sku = escape_attr(product["sku"])
    name = escape_attr(product["name"])
    sub_category = escape_attr(product.get("category", ""))
    main_category = escape_attr(resolve_main_category(product))
    # Breadcrumb uses the UI main category so clicking it lands on a page with
    # matching filter pills + non-zero results. Sub-category shown in CTA tag.
    return f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.yeatru.com/"}},
    {{"@type": "ListItem", "position": 2, "name": "Products", "item": "https://www.yeatru.com/products.html"}},
    {{"@type": "ListItem", "position": 3, "name": "{main_category}", "item": "https://www.yeatru.com/products.html?category={main_category}"}},
    {{"@type": "ListItem", "position": 4, "name": "{sub_category if sub_category else name}", "item": "https://www.yeatru.com/products.html?category={main_category}#sub-{escape_attr(sub_category or 'all')}"}},
    {{"@type": "ListItem", "position": 5, "name": "{name}", "item": "https://www.yeatru.com/product-{sku}.html"}}
  ]
}}</script>'''


def generate_faq_json_ld():
    return '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {"@type": "Question", "name": "What is the minimum order quantity (MOQ)?", "acceptedAnswer": {"@type": "Answer", "text": "Our standard MOQ is 100 units, but we are flexible and can accept smaller trial orders depending on the product. Please contact us with your specific requirements."}},
    {"@type": "Question", "name": "What materials are used in your products?", "acceptedAnswer": {"@type": "Answer", "text": "We source products from certified suppliers using high-quality materials suitable for their intended use. Specific material details are listed in the product specifications table above."}},
    {"@type": "Question", "name": "How long is the production lead time?", "acceptedAnswer": {"@type": "Answer", "text": "Standard lead time is 15-30 days for production, plus 5-7 days international shipping. Rush orders may be available for an additional fee."}},
    {"@type": "Question", "name": "Can I customize colors, sizes, or logos?", "acceptedAnswer": {"@type": "Answer", "text": "Yes! We offer OEM/ODM services including custom colors, sizes, logos, and packaging. Minimum order quantities apply for custom orders. Contact us with your specific requirements."}},
    {"@type": "Question", "name": "What payment methods do you accept?", "acceptedAnswer": {"@type": "Answer", "text": "We accept T/T (Telegraphic Transfer), PayPal, Western Union, and letter of credit (L/C). Payment terms: 50%/50% split (50% deposit + 50% balance before shipping) or full payment before shipping."}},
    {"@type": "Question", "name": "Do you provide samples?", "acceptedAnswer": {"@type": "Answer", "text": "Yes, we can provide samples for most products. Sample costs and shipping fees apply. Sample orders are typically dispatched within 3-5 business days."}},
    {"@type": "Question", "name": "What is your quality guarantee?", "acceptedAnswer": {"@type": "Answer", "text": "We offer a quality inspection service before shipment. Third-party inspection companies such as SGS and Bureau Veritas are also available upon request. We stand behind our products with a quality assurance commitment."}}
  ]
}</script>'''


def generate_org_json_ld():
    return '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "@id": "https://www.yeatru.com/#organization",
  "name": "Yeatru Sourcing",
  "url": "https://www.yeatru.com",
  "logo": "https://www.yeatru.com/logo.svg",
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "+86-159-8851-6408",
    "contactType": "customer service",
    "email": "info@yeatru.com",
    "areaServed": "Worldwide",
    "availableLanguage": ["English", "Chinese", "Spanish", "French", "Russian", "Arabic"]
  }
}</script>'''


def generate_graph_json_ld():
    return '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://www.yeatru.com/#organization",
      "name": "Yeatru Sourcing",
      "legalName": "YIWU ETRUE TRADING CO., LTD.",
      "alternateName": "Yeatru",
      "url": "https://www.yeatru.com/",
      "logo": {"@type": "ImageObject", "url": "https://www.yeatru.com/Images/yeatru-logo.png", "width": 220, "height": 60},
      "foundingDate": "2013",
      "foundingLocation": "Yiwu, Zhejiang, China",
      "telephone": "+86-159-8851-6408",
      "email": "info@yeatru.com",
      "numberOfEmployees": {"@type": "QuantitativeValue", "minValue": 15, "maxValue": 50},
      "sameAs": ["https://www.facebook.com/NeilLaw", "https://www.linkedin.com/in/neil-liu-398983257", "https://www.instagram.com/yeatru_sourcing", "https://www.alibaba.com/"],
      "knowsAbout": ["China product sourcing", "Yiwu wholesale market procurement", "Supplier verification", "Factory audit", "Quality control inspection", "Amazon FBA preparation", "DDP door-to-door shipping", "OEM private label", "Low MOQ small batch sourcing", "1688 purchase agent"]
    },
    {
      "@type": "LocalBusiness",
      "@id": "https://www.yeatru.com/#localbusiness",
      "name": "Yeatru Sourcing",
      "image": "https://www.yeatru.com/Images/yeatru-hero-2.jpg",
      "url": "https://www.yeatru.com/",
      "telephone": "+86-159-8851-6408",
      "email": "info@yeatru.com",
      "priceRange": "$$",
      "address": {"@type": "PostalAddress", "streetAddress": "Room 301, No.188 Shangcheng Avenue, Futian Street", "addressLocality": "Yiwu", "addressRegion": "Zhejiang", "postalCode": "322000", "addressCountry": "CN"},
      "geo": {"@type": "GeoCoordinates", "latitude": 29.3061, "longitude": 120.0858},
      "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"], "opens": "09:00", "closes": "18:00"}],
      "areaServed": ["US","GB","DE","FR","IT","ES","CA","AU","AE","SA","TR","MX","BR","PL","NL","SE","NO","DK","JP","KR","SG","MY","TH","VN","ID","PH","KE","ZA","NG"],
      "parentOrganization": {"@id": "https://www.yeatru.com/#organization"}
    },
    {
      "@type": "WebSite",
      "@id": "https://www.yeatru.com/#website",
      "url": "https://www.yeatru.com/",
      "name": "Yeatru Sourcing",
      "publisher": {"@id": "https://www.yeatru.com/#organization"},
      "inLanguage": "en",
      "potentialAction": {"@type": "SearchAction", "target": "https://www.yeatru.com/products.html?q={search_term_string}", "query-input": "required name=search_term_string"}
    }
  ]
}</script>'''


def generate_aplus_section(product):
    name = escape_text(product["name"])
    sku = escape_text(product["sku"])
    desc = escape_text(product.get("description", ""))
    sub_category = escape_text(product.get("category", ""))
    main_category = escape_text(product.get("mainCategory", ""))
    material = escape_text(product.get("material", "See specifications"))
    size = escape_text(product.get("size", "Various"))
    moq = escape_text(str(product.get("moq", "1")))
    variations = product.get("variations", [])

    usd_min_raw = cny_to_usd(product.get("priceMin", 0))
    usd_max_raw = cny_to_usd(product.get("priceMax", product.get("priceMin", 0)))
    if usd_min_raw and usd_max_raw and abs(usd_min_raw - usd_max_raw) < 0.001:
        price_usd = f"${usd_min_raw:.2f}"
    elif usd_min_raw and usd_max_raw:
        price_usd = f"${usd_min_raw:.2f} – ${usd_max_raw:.2f}"
    else:
        price_usd = "Contact us"

    colors = list(set(v.get("color", "") for v in variations if v.get("color")))
    sizes = list(set(v.get("size", "") for v in variations if v.get("size")))
    colors_str = ", ".join(colors) if colors else "Multiple color options available"
    sizes_str = ", ".join(sizes) if sizes else size
    cat_for_display = main_category or sub_category

    # Long-form Product Overview / SEO Description block
    seo_overview = (
        f"<p><b>{name}</b> ({sku}) wholesale supplier in {cat_for_display} from Yiwu China. "
        f"Factory-direct price: <b>{price_usd} USD</b> with MOQ starting at <b>{moq} pieces</b>. "
        f"Sourced from verified {sub_category} manufacturers with on-site audit and AQL 2.5 pre-shipment quality inspection. "
        f"Ideal for Amazon FBA sellers, TikTok Shop merchants, Shopify brands, wholesale distributors, and promotional gift buyers worldwide.</p>"
        f"<p>{desc} {name} is manufactured in Zhejiang / Guangdong with strict quality control. "
        f"Yeatru Sourcing provides end-to-end service including supplier screening, sample evaluation, production follow-up, "
        f"100% piece-by-piece QC inspection, free 15-day warehousing, FBA prep (FNSKU labeling, polybagging, palletization), "
        f"and door-to-door DDP shipping to USA, EU, UK, GCC, Australia, and 50+ countries. "
        f"OEM & private-label customization available with MOQ 200–500 pcs.</p>"
    )

    # SEO-rich features (with LLM-citable keywords)
    features_html = "\n".join([
        f"<li><b>✅ Verified Supplier:</b> On-site factory audit, business license & export license verified. "
        f"Part of Yeatru's 75,000+ trusted Chinese manufacturer network in the {cat_for_display} category.</li>",
        f"<li><b>💰 Factory-Direct Pricing:</b> {price_usd} USD wholesale — no Alibaba middleman markup. "
        f"Save 15–30% compared to trading companies. Volume discounts for orders over $5,000.</li>",
        f"<li><b>📦 Flexible MOQ:</b> Only {moq} piece(s) for stock items. Small-batch and trial orders welcome — perfect for new sellers, TikTok shop testing, and sample runs.</li>",
        f"<li><b>🎯 Quality Assurance:</b> 3-stage QC pipeline (incoming / in-process / pre-shipment) following AQL 2.5 standard. "
        f"Full photo & video inspection report provided before every shipment. SGS / BV / TUV 3rd-party inspection available.</li>",
        f"<li><b>🛠️ OEM / ODM Customization:</b> Custom logo (laser engraving / silk screen / heat transfer), "
        f"custom colors ({escape_text(colors_str)}), private label packaging, and product design services. 7-day sample turnaround.</li>",
        f"<li><b>🚚 Global Logistics:</b> Door-to-door DDP shipping via sea freight (25–45 days), air freight (5–15 days), "
        f"and express courier (3–7 days). Amazon FBA warehouse delivery with FNSKU label & pallet compliance.</li>",
        f"<li><b>🪪 Certifications:</b> Factory can provide CE, FCC, FDA, RoHS, MSDS, ASTM, CPSIA, EN71, GCC, SASO as required. "
        f"Contact us for product-specific compliance documents.</li>",
        f"<li><b>💬 24/7 Support:</b> Multilingual team (English / Spanish / French / Russian / Arabic). "
        f"Free quote within 24 hours on WhatsApp +86 159 8851 6408 or email info@yeatru.com.</li>",
    ])

    # Applications paragraph (tailored to main category)
    cat_use_map = {
        "Apparel & Footwear": "fashion boutiques, online apparel stores, sportswear brands, resort & hotel shops, uniform suppliers, promotional giveaways, and private-label clothing lines",
        "Auto Parts & Tools": "auto repair shops, garage equipment suppliers, tool distributors, car accessory retailers, and DIY mechanics marketplaces",
        "Baby & Toys": "toy stores, kids' boutiques, nursery shops, kindergarten supply distributors, family e-commerce brands, and educational gift suppliers",
        "Bags & Luggage": "lifestyle boutiques, travel retail, corporate gift programs, school supply chains, promotional bag distributors, and private-label luggage brands",
        "Beauty & Personal Care": "beauty salons, cosmetics stores, spa suppliers, skincare brands, personal care e-commerce, and private-label beauty product lines",
        "Digital Electronics": "consumer electronics retailers, Amazon FBA gadget stores, mobile accessory shops, electronic gift distributors, and tech e-commerce brands",
        "Hardware & Home": "hardware stores, DIY home improvement retailers, lock & security suppliers, building material chains, and home hardware brands",
        "Home & Daily Living": "home decor stores, supermarket household aisles, storage solution brands, cleaning supply distributors, home organization shops, and daily necessities importers",
        "Home Appliances": "home appliance retailers, kitchen appliance chains, small appliance importers, electronics megastores, and smart home solution providers",
        "Kitchen Supplies": "kitchenware stores, hotel & restaurant suppliers, supermarket houseware aisles, chef supply shops, and kitchen gadget e-commerce",
        "Material": "packaging material suppliers, raw material importers, industrial raw material distributors, manufacturing procurement, and creative & craft material stores",
        "Musical Instruments": "music stores, instrument retailers, school music programs, audio equipment dealers, and online instrument marketplaces",
        "Others": "general merchandise stores, dollar stores, promotional gift suppliers, boutique retailers, and e-commerce category expansion buyers",
        "Pet Supplies": "pet stores, veterinary clinics, pet grooming salons, animal supply distributors, and pet e-commerce brands",
        "Phone Accessories": "mobile phone shops, telecom carrier stores, tech accessory retailers, gadget marketplaces, and promotional power bank / case brands",
        "Sports & Outdoor": "sporting goods stores, fitness equipment suppliers, outdoor gear retailers, camping & hiking shops, and gym equipment distributors",
        "Stationery & Office": "office supply chains, school bookstores, stationery boutiques, corporate office procurement, back-to-school distributors, and promotional stationery gift programs",
    }
    uses = cat_use_map.get(main_category if main_category else "Others",
                            cat_use_map["Others"])

    # Why Source from Yeatru section (repeats GEO-citable company stats)
    why_yeatru_html = "\n".join([
        "<li><b>📍 Local Presence:</b> Registered company <i>Yiwu Yichu Trading Co., Ltd.</i> (USCC: 91330782MABU4K2L6F) with office & warehouse inside Yiwu International Trade City — direct access to 75,000+ factories.</li>",
        "<li><b>👥 200+ Clients in 50+ Countries:</b> 98% customer satisfaction rating. Trusted sourcing partner for Amazon FBA USA, UK, Germany, EU, GCC (UAE / Saudi), TikTok Shop sellers, and wholesale importers since 2022.</li>",
        "<li><b>💵 Transparent Pricing:</b> Published tiered commissions — Order Management 3–4% (min $150) or Full Sourcing 4–8% (min $100). No hidden fees, factory invoice shown to buyer.</li>",
        "<li><b>🔒 3-Level QC & Rework Guarantee:</b> If defects exceed AQL 2.5 at pre-shipment, the factory reworks or replaces at their cost — you never pay for defective products.</li>",
        "<li><b>🏷️ Free Services Included:</b> 15-day free warehousing, design consultation, product photography, FBA prep labeling, and door-to-door shipping coordination — $0 extra on standard orders.</li>",
        "<li><b>🌐 Multilingual Support:</b> EN / ES / FR / RU / AR native-speaking team. WhatsApp response in < 24 hours. Arabic Halal / GCC compliance specialist on staff.</li>",
    ])

    return f'''
  <div class="aplus-section">
    <h2 class="aplus-section-title"><i class="fas fa-layer-group me-2"></i> Product Details — {name} (SKU: {sku})</h2>
    <div class="aplus-blocks">

      <!-- 1. Product Specifications (FIRST block per user request: always shows
           the structured spec table before any narrative content) -->
      <div class="aplus-block aplus-specs-first" data-type="specTable" data-img-deduped="1">
        <div class="aplus-block-content">
          <h3 class="aplus-block-heading"><i class="fas fa-list-check me-2"></i>Product Specifications</h3>
          <div class="aplus-block-text">
            <div class="table-responsive aplus-spec-table-wrap">
<table class="aplus-spec-table" aria-label="Product Specifications for {sku}">
  <thead>
    <tr>
      <th scope="col" style="width:35%;">Specification</th>
      <th scope="col">Details</th>
    </tr>
  </thead>
  <tbody>
    <tr><th scope="row">SKU (Product Code)</th><td><code>{sku}</code></td></tr>
    <tr><th scope="row">Product Name</th><td>{name}</td></tr>
    <tr><th scope="row">Main Category (UI Filter)</th><td>{escape_text(main_category or 'N/A')}</td></tr>
    <tr><th scope="row">Sub Category (Supplier Category)</th><td>{sub_category}</td></tr>
    <tr class="aplus-spec-price-row"><th scope="row">Wholesale Price (USD)</th><td><span class="detail-price-hero aplus-inline-price">{price_usd}</span><div class="spec-price-hint">Factory-direct · CNY ÷ 6.7 × 1.15</div></td></tr>
    <tr><th scope="row">Minimum Order Quantity (MOQ)</th><td><b>{moq} piece(s)</b> — stock items; 200–500 pcs for OEM custom</td></tr>
    <tr><th scope="row">Material</th><td>{material}</td></tr>
    <tr><th scope="row">Available Colors</th><td>{escape_text(colors_str)}</td></tr>
    <tr><th scope="row">Available Sizes / Dimensions</th><td>{escape_text(sizes_str)}</td></tr>
    <tr><th scope="row">Country of Origin</th><td>Yiwu / Zhejiang / Guangzhou, China (verified export factory)</td></tr>
    <tr><th scope="row">Quality Standard</th><td>AQL 2.5 — 3-stage inspection (incoming · in-process · pre-shipment)</td></tr>
    <tr><th scope="row">Certifications Available</th><td>CE · FCC · FDA · RoHS · MSDS · EN71 · ASTM · CPSIA · GCC / SASO (per product)</td></tr>
    <tr><th scope="row">OEM / Private Label</th><td>✅ Supported — custom logo, packaging, colors, molds. 7-day sample.</td></tr>
    <tr><th scope="row">Shipping Options</th><td>✅ Sea (25–45d) · Air (5–15d) · Express (3–7d) · Amazon FBA DDP</td></tr>
    <tr><th scope="row">Free Warehousing</th><td>✅ 15 days at Yeatru Yiwu facility — order consolidation included</td></tr>
    <tr><th scope="row">Lead Time (Production)</th><td>7–15 days (stock) · 15–30 days (OEM / mass production)</td></tr>
    <tr><th scope="row">Payment Methods</th><td>T/T (bank wire) · PayPal (Yeatrusourcing@gmail.com) · Western Union · XTransfer · Trade Assurance</td></tr>
    <tr><th scope="row">Sourcing Agent Fee</th><td>3–4% Order Management · 4–8% Full Sourcing — transparent, no hidden markup</td></tr>
    <tr><th scope="row">Supplier</th><td>Verified Chinese manufacturer via Yeatru Sourcing (on-site audited)</td></tr>
  </tbody>
</table>
            </div>
          </div>
        </div>
      </div>

      <!-- 2. SEO-Rich Product Overview (300+ words for Google & GPT grounding) -->
      <div class="aplus-block" data-type="textImage" data-img-deduped="1">
        <div class="aplus-block-content">
          <h3 class="aplus-block-heading"><i class="fas fa-info-circle me-2"></i>Product Overview</h3>
          <div class="aplus-block-text">
            {seo_overview}
          </div>
        </div>
      </div>

      <!-- 3. Key Features (8 SEO-rich bullet points) -->
      <div class="aplus-block" data-type="text">
        <div class="aplus-block-content">
          <h3 class="aplus-block-heading"><i class="fas fa-star me-2"></i>Why Buy This {escape_text(main_category or sub_category)} Product from Yeatru</h3>
          <div class="aplus-block-text">
            <ul>
              {features_html}
            </ul>
          </div>
        </div>
      </div>

      <!-- 4. Applications & Target Buyers -->
      <div class="aplus-block" data-type="hero">
        <div class="aplus-block-content">
          <h3 class="aplus-block-heading"><i class="fas fa-store me-2"></i>Applications &amp; Ideal Buyers</h3>
          <div class="aplus-block-text">
            <p><b>Who should source {name} ({sku})?</b> This {escape_text(sub_category)} product is recommended for
            <b>{uses}</b>.</p>
            <p><b>Use cases:</b> Retail shelf placement · e-commerce product listing (Amazon / Shopify / TikTok Shop / eBay) ·
            promotional corporate gift · bundle add-on · private-label resale · fundraising merchandise ·
            conference &amp; trade show swag · subscription-box filler · hotel &amp; resort amenity.</p>
            <p>Tell us your target market, sales channel, and order volume — our team will tailor sourcing terms,
            packaging, compliance docs, and shipping route for maximum profit margin.</p>
          </div>
        </div>
      </div>

      <!-- 5. Packaging & Shipping -->
      <div class="aplus-block" data-type="text">
        <div class="aplus-block-content">
          <h3 class="aplus-block-heading"><i class="fas fa-truck-fast me-2"></i>Packaging, Lead Time &amp; Shipping</h3>
          <div class="aplus-block-text">
            <ul>
              <li><b>Standard Packaging:</b> Poly bag / inner box / export carton with foam protection. Custom retail box, blister pack, color sleeve, and private-label hang-tag available on OEM orders.</li>
              <li><b>Production Lead Time:</b> Stock items ship in <b>7–15 days</b>; OEM / custom orders require <b>15–30 days</b> depending on complexity.</li>
              <li><b>Sample Lead Time:</b> <b>3–7 days</b> for stock samples; <b>7–15 days</b> for custom OEM samples. Sample fees refundable on bulk orders ≥ 1,000 pcs.</li>
              <li><b>Shipping Methods &amp; Timelines:</b>
                <ul style="margin-top:8px;">
                  <li>🚢 Sea Freight (FCL / LCL): <b>25–45 days</b> to main ports — lowest cost for ≥ 1 CBM</li>
                  <li>✈️ Air Freight: <b>5–15 days</b> — ideal for medium-batch Amazon FBA restock</li>
                  <li>📦 Express (DHL / FedEx / UPS): <b>3–7 days</b> door-to-door — samples &amp; urgent orders</li>
                  <li>🏪 Amazon FBA / TikTok Warehouse: <b>DDP door-to-door</b> with FNSKU label &amp; pallet compliance</li>
                </ul>
              </li>
              <li><b>Order Consolidation:</b> Combine multiple products / suppliers into one shipment — free 15-day storage + one sea/air freight bill saves you 30–50% on shipping.</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- 6. Why Choose Yeatru Sourcing (GEO citable company facts) -->
      <div class="aplus-block aplus-block-highlight" data-type="text">
        <div class="aplus-block-content">
          <h3 class="aplus-block-heading"><i class="fas fa-shield-halved me-2"></i>Why Source from Yeatru Sourcing — Your China Agent Since 2022</h3>
          <div class="aplus-block-text">
            <ul>
              {why_yeatru_html}
            </ul>
          </div>
        </div>
      </div>

      <!-- 7. Step-by-Step Sourcing Process -->
      <div class="aplus-block" data-type="text">
        <div class="aplus-block-content">
          <h3 class="aplus-block-heading"><i class="fas fa-shoe-prints me-2"></i>Sourcing Process in 8 Simple Steps</h3>
          <div class="aplus-block-text">
            <ol>
              <li><b>Send Inquiry:</b> Email <b>info@yeatru.com</b> or WhatsApp <b>+86 159 8851 6408</b> with product name, target quantity, specs, destination country &amp; sales channel.</li>
              <li><b>Free Quote in 24 Hours:</b> Receive detailed quote including unit price, MOQ, shipping options, estimated lead time, and sourcing service fee breakdown.</li>
              <li><b>Sample Evaluation (Optional):</b> Approve sample — we coordinate sample production, QC photos, DHL shipping to your office so you can test quality before bulk.</li>
              <li><b>Contract &amp; Deposit:</b> Sign service agreement. Pay 50% deposit (T/T, PayPal Yeatrusourcing@gmail.com, or XTransfer) to start production.</li>
              <li><b>Production Follow-up:</b> Weekly photo/video progress updates. Our on-site team visits the factory during in-process QC to catch issues early.</li>
              <li><b>Pre-Shipment Inspection (AQL 2.5):</b> 100% visual check + documented photo/video report. You approve before we ship — defective batches go back to the factory for rework at their cost.</li>
              <li><b>Balance Payment &amp; Shipping:</b> Pay remaining 50% balance. We arrange export customs, DDP door-to-door shipping (sea / air / express / FBA) with live tracking.</li>
              <li><b>After-Sales Support:</b> File claims, handle defect replacements, manage re-orders, and scale new product sourcing. Your dedicated account manager is always one WhatsApp message away.</li>
            </ol>
          </div>
        </div>
      </div>

      <!-- 8. Call to Action (inquiry CTA) -->
      <div class="aplus-block aplus-cta-block" data-type="hero">
        <div class="aplus-block-content">
          <h2 class="aplus-block-heading">👉 Ready to Source {name} at Factory Price?</h2>
          <div class="aplus-block-text">
            <p class="aplus-cta-lead">Click <b>Get a Quote</b> below or WhatsApp us directly. Get your <b>free, no-obligation quote within 24 hours</b> — including competitive factory price, MOQ, lead time, and DDP shipping cost to your door.</p>
            <div class="aplus-cta-actions">
              <a class="aplus-cta-btn aplus-cta-btn-primary"
                 href="contact.html?product={sku}&amp;name={html.escape(name)}">
                📝 Request a Quote (Email)
              </a>
              <a class="aplus-cta-btn aplus-cta-btn-whatsapp" target="_blank" rel="noopener noreferrer"
                 href="https://wa.me/8615988516408?text={html.escape('Hello Yeatru Sourcing, I would like a quote for SKU '+sku+' — '+name+'. Qty: ___. Ship to: ___')}">
                💬 Chat on WhatsApp (+86 159 8851 6408)
              </a>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>'''


def generate_faq_section():
    return '''
  <div class="faq-section">
    <h2 class="faq-section-title"><i class="fas fa-circle-question me-2"></i> Frequently Asked Questions</h2>
    <div class="faq-list">
      <details class="faq-item">
        <summary><i class="fas fa-chevron-right me-2"></i>What is the minimum order quantity (MOQ)?</summary>
        <div class="faq-answer"><p>Our standard MOQ is 100 units, but we are flexible and can accept smaller trial orders depending on the product. Please contact us with your specific requirements.</p></div>
      </details>
      <details class="faq-item">
        <summary><i class="fas fa-chevron-right me-2"></i>What materials are used in your products?</summary>
        <div class="faq-answer"><p>We source products from certified suppliers using high-quality materials suitable for their intended use. Specific material details are listed in the product specifications table above.</p></div>
      </details>
      <details class="faq-item">
        <summary><i class="fas fa-chevron-right me-2"></i>How long is the production lead time?</summary>
        <div class="faq-answer"><p>Standard lead time is 15-30 days for production, plus 5-7 days international shipping. Rush orders may be available for an additional fee.</p></div>
      </details>
      <details class="faq-item">
        <summary><i class="fas fa-chevron-right me-2"></i>Can I customize colors, sizes, or logos?</summary>
        <div class="faq-answer"><p>Yes! We offer OEM/ODM services including custom colors, sizes, logos, and packaging. Minimum order quantities apply for custom orders. Contact us with your specific requirements.</p></div>
      </details>
      <details class="faq-item">
        <summary><i class="fas fa-chevron-right me-2"></i>What payment methods do you accept?</summary>
        <div class="faq-answer"><p>We accept T/T (Telegraphic Transfer), PayPal, Western Union, and letter of credit (L/C). Payment terms: 50%/50% split (50% deposit + 50% balance before shipping) or full payment before shipping.</p></div>
      </details>
      <details class="faq-item">
        <summary><i class="fas fa-chevron-right me-2"></i>Do you provide samples?</summary>
        <div class="faq-answer"><p>Yes, we can provide samples for most products. Sample costs and shipping fees apply. Sample orders are typically dispatched within 3-5 business days.</p></div>
      </details>
      <details class="faq-item">
        <summary><i class="fas fa-chevron-right me-2"></i>What is your quality guarantee?</summary>
        <div class="faq-answer"><p>We offer a quality inspection service before shipment. Third-party inspection companies such as SGS and Bureau Veritas are also available upon request. We stand behind our products with a quality assurance commitment.</p></div>
      </details>
    </div>
  </div>'''


def generate_product_page(product, all_products):
    sku = product["sku"]
    name = product["name"]
    category = product.get("category", "")
    image = product.get("image", "")
    desc = product.get("description", "")

    title = generate_title(product)
    meta_desc = generate_meta_description(product)
    meta_keywords = f"{name}, {category}, {sku}, wholesale, China sourcing, factory price, Yeatru Sourcing"

    breadcrumb_json = generate_json_ld_breadcrumb(product)
    faq_json = generate_faq_json_ld()
    org_json = generate_org_json_ld()
    graph_json = generate_graph_json_ld()
    product_json = generate_json_ld_product(product)

    var_min = product.get("priceMin", 0)
    var_max = product.get("priceMax", var_min)
    usd_min = cny_to_usd(var_min)
    usd_max = cny_to_usd(var_max)
    price_text = format_usd(usd_min) if usd_min else "Contact"

    og_image_width = 800
    og_image_height = 800

    og_price_amount = f"{usd_min:.2f}" if usd_min is not None else ""
    og_price_currency = "USD"

    variations_html = generate_variations_section(product)
    price_display_html = generate_price_display(product)
    spec_table_html = generate_detail_spec_table(product)
    aplus_html = generate_aplus_section(product)
    faq_html = generate_faq_section()
    related_html = generate_related_section(product, all_products)

    h1 = escape_text(name)
    cat_esc = escape_text(category)
    main_category = resolve_main_category(product)
    main_cat_esc = escape_text(main_category)
    main_cat_attr = escape_attr(main_category)
    sku_esc = escape_text(sku)
    desc_esc = escape_text(desc)
    image_esc = escape_attr(image)
    title_esc = escape_attr(title)
    meta_desc_esc = escape_attr(meta_desc)
    canonical_url = f"https://www.yeatru.com/product-{sku}.html"

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Playfair+Display:wght@500;600;700&display=swap" rel="stylesheet">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="theme-color" content="#444CE7">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link rel="icon" type="image/x-icon" href="/favicon.ico">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
  <link rel="manifest" href="/site.webmanifest">
  <title>{title_esc}</title>
  <meta name="description" content="{meta_desc_esc}">
  <meta name="keywords" content="{escape_attr(meta_keywords)}">
  <meta name="robots" content="index, follow">
  <meta name="author" content="Yeatru Sourcing">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="theme-color" content="#444CE7">
  <link rel="canonical" href="{canonical_url}">
  <meta property="og:type" content="product">
  <meta property="og:url" content="{canonical_url}">
  <meta property="og:site_name" content="Yeatru Sourcing">
  <meta property="og:locale" content="en_US">
  <meta property="og:locale:alternate" content="es_ES">
  <meta property="og:locale:alternate" content="fr_FR">
  <meta property="og:title" content="{title_esc}">
  <meta property="og:description" content="{meta_desc_esc}">
  <meta property="og:image" content="{image_esc}">
  <meta property="og:image:width" content="{og_image_width}">
  <meta property="og:image:height" content="{og_image_height}">
  <meta property="og:image:alt" content="{escape_attr(name)}">
  <meta property="og:product:sku" content="{sku_esc}">
  <meta property="og:price:amount" content="{og_price_amount}">
  <meta property="og:price:currency" content="{og_price_currency}">
  <meta property="availability" content="in_stock">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@yeatru_sourcing">
  <meta name="twitter:url" content="{canonical_url}">
  <meta name="twitter:title" content="{title_esc}">
  <meta name="twitter:description" content="{meta_desc_esc}">
  <meta name="twitter:image" content="{image_esc}">
  <meta name="twitter:image:alt" content="{escape_attr(name)}">
  <meta name="twitter:label1" content="SKU">
  <meta name="twitter:data1" content="{sku_esc}">
  <meta name="twitter:label2" content="Price">
  <meta name="twitter:data2" content="{og_price_amount} USD">
  <link rel="alternate" type="atom+xml" title="Yeatru Sourcing Blog" href="https://www.yeatru.com/atom.xml">
  <link rel="alternate" hreflang="en" href="{canonical_url}">
  <link rel="alternate" hreflang="x-default" href="{canonical_url}">
  <link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
  <link rel="dns-prefetch" href="https://cdn.jsdelivr.net">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.4/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-DQvkBjpPgn7RC31MCQoOeC9TI2kdqa4+BSgNMNj8v77fdC77Kj5zpWFTJaaAoMbC" crossorigin="anonymous">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <link rel="stylesheet" href="styles.css">
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-KXW2N4FHZR"></script>
  <script>window.dataLayer = window.dataLayer || [];function gtag(){{dataLayer.push(arguments);}}gtag('js', new Date());gtag('config', 'G-KXW2N4FHZR');</script>
  <script type="application/ld+json">
{{"@context":"https://schema.org","@type":"AggregateRating","ratingValue":"4.9","reviewCount":"217","bestRating":"5","worstRating":"1"}}
  </script>
{org_json}
{graph_json}
{product_json}
{breadcrumb_json}
{faq_json}
</head>
<body>
  <nav class="navbar navbar-expand-xl bg-white sticky-top">
    <div class="container">
      <a class="navbar-brand" href="index.html">
        <span class="brand-logo-box" id="brandLogoBox" title="Yeatru Sourcing Logo">
          <img id="brandLogoImg" src="logo.svg" alt="Yeatru Logo" style="display:none;"  class="img-fluid" />
          <span class="brand-logo-fallback" id="brandLogoFallback">YC</span>
          <span class="brand-logo-edit" id="brandLogoEdit" title="Change logo (Admin only)"><i class="fas fa-pen"></i></span>
        </span>
        <span>Yeatru Sourcing</span>
      </a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav mx-auto">
          <li class="nav-item"><a class="nav-link" href="index.html">Home</a></li>
          <li class="nav-item"><a class="nav-link active" href="products.html">Products</a></li>
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" id="servicesDropdown" role="button" data-bs-toggle="dropdown">Sourcing Service</a>
            <ul class="dropdown-menu">
              <li><a class="dropdown-item" href="supplier-verification.html">Supplier Verification</a></li>
              <li><a class="dropdown-item" href="product-sourcing.html">Product Sourcing</a></li>
              <li><a class="dropdown-item" href="quality-control.html">Quality Control</a></li>
              <li><a class="dropdown-item" href="logistics-shipping.html">Logistics & Warehousing</a></li>
              <li><a class="dropdown-item" href="price-negotiation.html">Price Negotiation</a></li>
              <li><a class="dropdown-item" href="factory-audit.html">Factory Audit</a></li>
              <li><hr class="dropdown-divider"></li>
              <li><a class="dropdown-item" href="oem.html">OEM Customization</a></li>
              <li><a class="dropdown-item" href="sample-order.html">Sample Order</a></li>
              <li><a class="dropdown-item" href="service-plans.html">Service Plans</a></li>
            </ul>
          </li>
          <li class="nav-item"><a class="nav-link" href="about.html">About Us</a></li>
          <li class="nav-item"><a class="nav-link" href="faq.html">FAQ</a></li>
          <li class="nav-item"><a class="nav-link" href="blog.html">Blog</a></li>
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" id="resourcesDropdown" role="button" data-bs-toggle="dropdown">Resources</a>
            <ul class="dropdown-menu">
              <li><a class="dropdown-item" href="payment.html">Payment Methods</a></li>
              <li><a class="dropdown-item" href="refund.html">Refund & Cancellation Policy</a></li>
              <li><a class="dropdown-item" href="terms.html">Terms of Service</a></li>
              <li><hr class="dropdown-divider"></li>
              <li><h6 class="dropdown-header text-primary">Sourcing by Country / Platform</h6></li>
              <li><a class="dropdown-item" href="sourcing-for-amazon-fba-usa.html">🇺🇸 Amazon FBA (USA)</a></li>
              <li><a class="dropdown-item" href="yiwu-sourcing-agent-uk.html">🇬🇧 United Kingdom</a></li>
              <li><a class="dropdown-item" href="china-sourcing-agent-germany.html">🇩🇪 Germany / DACH</a></li>
              <li><a class="dropdown-item" href="china-sourcing-agent-europe.html">🇪🇺 Whole of Europe</a></li>
              <li><a class="dropdown-item" href="china-sourcing-turkiye.html">🇹🇷 Türkiye</a></li>
              <li><a class="dropdown-item" href="sourcing-agent-middle-east-uae-saudi.html">🇦🇪🇸🇦 UAE / Saudi (GCC)</a></li>
              <li><a class="dropdown-item" href="sourcing-agent-for-tiktok-shop-seller.html">🎵 TikTok Shop (Global)</a></li>
              <li><hr class="dropdown-divider"></li>
              <li><a class="dropdown-item" href="testimonials">Client Testimonials</a></li>
              <li><hr class="dropdown-divider"></li>
              <li><a class="dropdown-item" href="sitemap.xml">Sitemap</a></li>
            </ul>
          </li>
          <li class="nav-item"><a class="nav-link" href="contact.html">Contact</a></li>
        </ul>
        <div class="d-flex align-items-center gap-1 gap-xl-2 flex-nowrap" style="min-width:0;">
          <a href="https://wa.me/8615988516408?text=Hello%20Yeatru%20Sourcing%2C%20I%20would%20like%20a%20free%20quote%20for%20sourcing%20products%20from%20China." class="btn btn-success btn-nav-icon d-inline-flex align-items-center justify-content-center" target="_blank" rel="noopener noreferrer" title="Chat on WhatsApp" aria-label="Chat on WhatsApp" style="background:#25D366;border-color:#25D366;width:32px;height:32px;padding:0;border-radius:8px;line-height:1;box-shadow:none;">
            <i class="fab fa-whatsapp" style="font-size:15px;"></i>
          </a>
          <a href="mailto:info@yeatru.com?subject=Free%20Quote%20Request%20-%20Sourcing%20from%20China" class="btn btn-outline-secondary btn-nav-icon d-inline-flex align-items-center justify-content-center" title="Email us" aria-label="Email us" style="width:32px;height:32px;padding:0;border-radius:8px;line-height:1;box-shadow:none;">
            <i class="fas fa-envelope" style="font-size:14px;"></i>
          </a>
          <a href="contact.html" class="btn btn-cta btn-nav-cta d-inline-flex text-nowrap">
            <i class="fas fa-comment-dots me-1"></i>Get Quote
          </a>
        </div>
      </div>
    </div>
  </nav>

  <section class="product-detail-page active">
    <div class="container">
      <nav class="breadcrumb" aria-label="Breadcrumb">
        <ol>
          <li><a href="index.html">Home</a></li>
          <li><a href="products.html">Products</a></li>
          <li><a href="products.html?category={main_cat_attr}">{main_cat_esc}</a></li>
          <li aria-current="page">{escape_text(name)}</li>
        </ol>
      </nav>

      <div class="detail-main">
        <div class="detail-image-col">
          <img class="detail-image loaded img-fluid" src="{image_esc}" alt="{escape_attr(name)}" loading="eager" fetchpriority="high" decoding="async" onerror="this.style.display='none'">
        </div>
        <div class="detail-info">
          <h1>{h1}</h1>
          <div class="detail-meta">
            Category: <strong><a href="products.html?category={main_cat_attr}" style="color:inherit;text-decoration:none;">{cat_esc}</a> · {main_cat_esc}</strong> &nbsp;|&nbsp; SKU: <strong>{sku_esc}</strong>
          </div>
          {spec_table_html}
          <p class="detail-desc">{desc_esc}</p>
          {variations_html}
          <div class="detail-buy-row">
            <a class="btn btn-lg btn-primary detail-buy-btn quote-product" href="contact.html?product={sku_esc}&name={escape_attr(name)}" data-product="{escape_attr(name)}" data-sku="{sku_esc}">
              <i class="fas fa-file-invoice-dollar me-2"></i>Request a Quote
            </a>
          </div>
        </div>
      </div>

      {aplus_html}
      {faq_html}
      {related_html}
    </div>
  </section>

  <footer class="footer">
    <div class="container">
      <div class="row">
        <div class="col-lg-3 col-md-6">
          <a href="index.html" class="footer-brand">
            <span class="brand-logo-box" style="width:36px;height:36px;min-width:36px;min-height:36px;max-width:36px;max-height:36px;border:none;background:transparent;box-shadow:none;">
              <span style="color: var(--primary); font-weight: bold;">YC</span>
            </span>
            Yeatru Sourcing
          </a>
          <p class="footer-desc">Professional China sourcing agent helping businesses worldwide find reliable suppliers and quality products at competitive prices.</p>
          <div class="footer-social">
            <a href="https://facebook.com/NeilLaw" target="_blank" class="footer-social-icon" rel="noopener noreferrer"><i class="fab fa-facebook-f"></i></a>
            <a href="https://www.linkedin.com/in/neil-liu-398983257" target="_blank" class="footer-social-icon" rel="noopener noreferrer"><i class="fab fa-linkedin-in"></i></a>
            <a href="https://wa.me/8615988516408" target="_blank" class="footer-social-icon" rel="noopener noreferrer"><i class="fab fa-whatsapp"></i></a>
            <a href="https://instagram.com/yeatru_sourcing" target="_blank" class="footer-social-icon" rel="noopener noreferrer"><i class="fab fa-instagram"></i></a>
          </div>
        </div>
        <div class="col-lg-3 col-md-6">
          <h3 class="footer-title">Quick Links</h3>
          <a href="index.html" class="footer-link">Home</a>
          <a href="products.html" class="footer-link">Products</a>
          <a href="supplier-verification.html" class="footer-link">Services</a>
          <a href="payment.html" class="footer-link">Payment</a>
          <a href="about.html" class="footer-link">About Us</a>
          <a href="blog.html" class="footer-link">Blog</a>
          <a href="contact.html" class="footer-link">Contact Us</a>
          <a href="faq.html" class="footer-link">FAQ</a>
        </div>
        <div class="col-lg-3 col-md-6">
          <h3 class="footer-title">Our Services</h3>
          <a href="supplier-verification.html" class="footer-link">Supplier Verification</a>
          <a href="product-sourcing.html" class="footer-link">Product Sourcing</a>
          <a href="quality-control.html" class="footer-link">Quality Control</a>
          <a href="logistics-shipping.html" class="footer-link">Logistics & Warehousing</a>
          <a href="price-negotiation.html" class="footer-link">Price Negotiation</a>
          <a href="factory-audit.html" class="footer-link">Factory Audit</a>
          <a href="sample-order.html" class="footer-link">Sample Order</a>
        </div>
        <div class="col-lg-3 col-md-6">
          <h3 class="footer-title">Contact Us</h3>
          <a href="https://maps.google.com/?q=NO.188+Shangcheng+Avenue+Yiwu+Zhejiang+322000+China" target="_blank" rel="noopener noreferrer" class="footer-link"><i class="fas fa-map-marker-alt me-2"></i> NO.188 Shangcheng Ave, Yiwu, Zhejiang, China</a>
          <a href="tel:+8615988516408" class="footer-link"><i class="fas fa-phone me-2"></i> +86 15988516408</a>
          <a href="mailto:info@yeatru.com" class="footer-link"><i class="fas fa-envelope me-2"></i> info@yeatru.com</a>
          <a href="contact.html#opening-hours" class="footer-link"><i class="fas fa-clock me-2"></i> Open: Mo-Sa 09:00–18:00 · 24/7 Online</a>
          <div class="footer-payment-section mt-3">
            <h4 class="footer-payment-label">Payment Methods</h4>
            <div class="footer-payment-icons-vertical">
              <span class="payment-icon"><i class="fab fa-cc-visa"></i><span>Visa</span></span>
              <span class="payment-icon"><i class="fab fa-cc-mastercard"></i><span>MasterCard</span></span>
              <span class="payment-icon"><i class="fas fa-university"></i><span>Bank Transfer</span></span>
            </div>
          </div>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; 2022–2026 义乌市弋楚贸易有限公司 · Yeatru Sourcing (YIWU ETRUE TRADING CO., LTD.). All rights reserved. | <a href="privacy.html" class="footer-link d-inline">Privacy Policy</a> | <a href="terms.html" class="footer-link d-inline">Terms of Service</a> | <a href="refund.html" class="footer-link d-inline">Refund Policy</a> | <a href="nda.html" class="footer-link d-inline">NDA &amp; Confidentiality</a></p>
      </div>
    </div>
  </footer>

  <div class="contact-float">
    <a href="https://wa.me/8615988516408?text=Hello%20Yeatru%20Sourcing%2C%20I%20would%20like%20a%20free%20quote%20for%20sourcing%20products%20from%20China." class="contact-float-btn whatsapp" target="_blank" rel="noopener noreferrer" title="Chat with us on WhatsApp">
      <i class="fab fa-whatsapp"></i>
    </a>
    <a href="mailto:info@yeatru.com?subject=Free%20Quote%20Request%20-%20Sourcing%20from%20China" class="contact-float-btn email" title="Send us an email for a free quote">
      <i class="fas fa-envelope"></i>
    </a>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.4/dist/js/bootstrap.bundle.min.js" integrity="sha384-YUe2LzesAfftltw+PEaao2tjU/QATaW/rOitAq67e0CT0Zi2VVRL0oC4+gAaeBKu" crossorigin="anonymous"></script>
  <script src="app.js" defer></script>
</body>
</html>'''


def main():
    print("Loading site-data.json...")
    with open(SITE_DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    products = data["products"]
    print(f"Found {len(products)} products in site-data.json")

    existing_files = set()
    for fn in os.listdir(PRODUCTS_DIR):
        if fn.startswith("product-") and fn.endswith(".html"):
            existing_files.add(fn)

    generated = 0
    updated = 0
    skipped = 0

    for product in products:
        sku = product["sku"]
        filename = f"product-{sku}.html"
        filepath = os.path.join(PRODUCTS_DIR, filename)

        try:
            html_content = generate_product_page(product, products)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(html_content)

            if filename in existing_files:
                updated += 1
            else:
                generated += 1

            if (generated + updated) % 50 == 0:
                print(f"Progress: {generated + updated}/{len(products)} products processed...")

        except Exception as e:
            print(f"Error processing {sku}: {e}")
            skipped += 1

    # Generate sitemap entries
    print("\nUpdating sitemap.xml...")
    sitemap_path = os.path.join(SITE_ROOT, "sitemap.xml")

    product_urls = []
    for product in products:
        sku = product["sku"]
        product_urls.append(f"  <url>\n    <loc>https://www.yeatru.com/product-{sku}.html</loc>\n    <lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>")

    existing_sitemap_entries = []
    if os.path.exists(sitemap_path):
        with open(sitemap_path, "r", encoding="utf-8") as f:
            content = f.read()
            import re
            existing_sitemap_entries = re.findall(
                r"<url>\s*<loc>(.*?)</loc>.*?</url>", content, re.DOTALL
            )

    all_urls = list(set(existing_sitemap_entries + [
        f"https://www.yeatru.com/product-{p['sku']}.html" for p in products
    ]))

    sitemap_header = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <url>
    <loc>https://www.yeatru.com/</loc>
    <lastmod>{date}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://www.yeatru.com/products.html</loc>
    <lastmod>{date}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
""".format(date=datetime.now().strftime("%Y-%m-%d"))

    product_urls_set = set(product_urls)
    all_entries = list(product_urls_set)

    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write(sitemap_header)
        for entry in sorted(set(product_urls)):
            f.write(entry + "\n")
        f.write("</urlset>")

    print(f"\nSitemap updated with {len(product_urls)} product URLs")

    print(f"\n{'='*60}")
    print(f"Generation complete!")
    print(f"  New pages generated: {generated}")
    print(f"  Existing pages updated: {updated}")
    print(f"  Errors/skipped: {skipped}")
    print(f"  Total products: {len(products)}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
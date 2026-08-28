#!/usr/bin/env python3
"""Rebuild site-data-aplus.json so each product.id entry strictly matches the
product's real SKU, name, category, MOQ, price, origin, and main image.

This fixes the systematic mismatch where e.g. YCS-CLO-028 (tracksuit) was
rendered with YCS-OUT-003 (camping tent) content inside the A+ section, and
YCS-CLO-029 (shorts) was rendered with YCS-TOY-001 (felt ornament) content.
"""
import json
import os
import html

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE_DATA = os.path.join(ROOT, "site-data.json")
APLUS_DATA = os.path.join(ROOT, "site-data-aplus.json")
CNY_TO_USD_RATE = 6.7
PRICE_MARKUP = 1.15


def cny_to_usd(v):
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    return (f / CNY_TO_USD_RATE) * PRICE_MARKUP


def fmt_usd(v):
    if v is None:
        return "—"
    return f"${v:.2f}"


def esc_html(s):
    if s is None:
        return ""
    return html.escape(str(s), quote=False)


CAT_USE = {
    "Toys": "birthday party favors, preschool classrooms, daycare centers, amusement arcades, family game nights, kids gift shops, and promotional toy bundles",
    "Storage & Organization": "retail shelving, kitchen pantries, bathroom cabinets, closet makeovers, garage storage, office organization, and dorm-room essentials",
    "Clothing": "fashion boutiques, online apparel stores, sportswear brands, resort & hotel shops, uniform suppliers, promotional giveaways, and private-label clothing lines",
    "Shoes": "footwear retailers, fashion e-commerce stores, sports shoe outlets, uniform suppliers, resort gift shops, and branded-private-label footwear lines",
    "Household": "housewares retailers, home decor e-commerce stores, hotel amenity suppliers, houseware distributors, and promotional gift programs",
    "Kitchen Storage": "kitchenware retailers, pantry organizers, restaurant supply shops, home organization boutiques, and houseware e-commerce brands",
    "Home & Garden": "home decor brands, garden centers, e-commerce home & living stores, holiday decoration resellers, and landscaping supply shops",
    "Bags": "fashion bag retailers, travel accessory stores, promotional gifts, backpack brands, luggage distributors, and private-label handbag lines",
    "Cleaning": "janitorial supply distributors, hotel & restaurant procurement, household cleaning product retailers, and office cleaning supply stores",
    "Kids": "kids apparel stores, children toy shops, nursery retailers, baby shower gift suppliers, and private-label children lifestyle brands",
    "Lighting": "indoor lighting retailers, home decor stores, hotel & restaurant lighting suppliers, commercial lighting projects, and smart-light e-commerce brands",
    "Microphones/Audio": "podcast studios, content creators, event AV rental companies, live-stream equipment shops, broadcast equipment distributors, and audio gear brands",
    "Cups & Drinkware": "drinkware retailers, coffee shops, promotional merchandise brands, gift shops, cafe & restaurant supply stores, and private-label mugs & tumblers",
    "Kitchen Tools": "kitchenware e-commerce, restaurant supply stores, home chef brands, culinary gift shops, and houseware boutiques",
    "Dog Supplies": "pet stores, vet clinic gift shops, dog grooming salons, online pet DTC brands, pet-supply distributors, and private-label pet product lines",
    "Audio/Electronics": "electronics retailers, gadget e-commerce stores, B2B office equipment buyers, and tech accessory distributors",
    "Fitness": "gym equipment dealers, fitness studios, sports apparel brands, yoga & pilates studios, outdoor athletic retailers, and home gym DTC brands",
    "Smart Electronics": "smart-home retailers, gadget stores, B2B office automation, smart security installers, and tech DTC brands",
    "Personal Care": "personal care stores, beauty e-commerce, hotel amenity suppliers, salon supply distributors, and private-label personal care brands",
    "Machinery": "B2B industrial buyers, factory equipment dealers, workshop equipment suppliers, and construction procurement companies",
    "Baby Care": "baby stores, maternity boutiques, hospital gift shops, baby registry platforms, and private-label baby care brands",
    "Stationery": "office supply retailers, school stationery stores, back-to-school programs, promotional gifts, and stationery DTC brands",
    "Skin Care": "beauty retailers, salon skincare brands, cosmetic e-commerce stores, private-label skincare lines, and spa & hotel amenity suppliers",
    "Auto Repair Tools": "auto repair shops, tool distributors, car accessory retailers, and DIY workshop suppliers",
    "Backpacks": "school backpack retailers, travel gear stores, outdoor hiking brands, corporate gift suppliers, and private-label bag lines",
    "Hardware": "home-improvement retailers, construction procurement, hardware stores, industrial maintenance buyers, and DIY workshops",
    "Photography": "camera accessory retailers, photography studios, content creator gear stores, and rental photography equipment shops",
    "Auto Accessories": "car accessory retailers, auto detailing shops, dealership gift shops, and private-label automotive accessories",
    "Swimwear": "swimwear retailers, resort boutique shops, beachwear brands, swim schools, pool supply stores, and private-label swim lines",
    "Kitchenware": "kitchenware retailers, home chef brands, culinary gift shops, restaurant supply stores, and houseware distributors",
    "Outdoor": "outdoor camping stores, hiking gear retailers, survival equipment brands, picnic & BBQ suppliers, and private-label outdoor product lines",
    "Baby & Toys": "baby stores, toy shops, daycare center procurement, and children gift brands",
    "Hair Accessories": "beauty supply stores, hair salons, fashion accessory retailers, and private-label hair accessory brands",
    "Beauty & Personal Care": "beauty retailers, salons, cosmetic e-commerce stores, spa suppliers, and private-label beauty brands",
    "Apparel & Textile": "apparel retailers, uniform suppliers, textile distributors, fashion e-commerce stores, and promotional apparel programs",
    "Sports & Outdoor": "sporting goods retailers, outdoor activity brands, school athletic programs, and private-label sportswear",
}


def build_use_cases(category):
    if category in CAT_USE:
        return CAT_USE[category]
    return "retail stores, e-commerce sellers, private-label brands, promotional gift programs, hotel & restaurant procurement, and wholesale distributors across 50+ countries"


def parse_variations(p):
    v = p.get("variations") or []
    if isinstance(v, str):
        try:
            v = json.loads(v)
        except Exception:
            v = []
    if not isinstance(v, list):
        v = []
    return v


def collect_images(p):
    img = p.get("image") or ""
    images = []
    if isinstance(p.get("variantImages"), list):
        for u in p["variantImages"]:
            if isinstance(u, str) and u and u not in images and u != img:
                images.append(u)
    raw = p.get("images") or "[]"
    if isinstance(raw, str):
        try:
            raw = json.loads(raw)
        except Exception:
            raw = []
    if isinstance(raw, list):
        for u in raw:
            if isinstance(u, str) and u and u not in images and u != img:
                images.append(u)
    return img, images


def build_overview_text(p, sku, name, category, main_category, description, moq, usd_min, usd_max, variants_cnt):
    custom = (p.get("seoOverview") or "").strip()
    if custom:
        return custom
    cat_display = main_category or category or "general merchandise"
    sub = category or cat_display
    price_part = ""
    if usd_min is not None or usd_max is not None:
        a, b = usd_min, usd_max
        if a is None:
            a = b
        if b is None:
            b = a
        if abs(a - b) < 0.01:
            price_part = f"Factory-direct price: <b>{fmt_usd(a)} USD</b> with MOQ starting at <b>{moq} pieces</b>. "
        else:
            price_part = f"Factory-direct price range: <b>{fmt_usd(a)}–{fmt_usd(b)} USD</b> with MOQ starting at <b>{moq} pieces</b>. "
    p1 = (
        f"<p><b>{esc_html(name)}</b> ({sku}) wholesale supplier in {esc_html(cat_display)} from Yiwu China. "
        f"{price_part}"
        f"Sourced from verified {esc_html(sub)} manufacturers with on-site audit and AQL 2.5 pre-shipment quality inspection. "
        f"Ideal for Amazon FBA sellers, TikTok Shop merchants, Shopify brands, wholesale distributors, and promotional gift buyers worldwide.</p>"
    )
    desc_esc = esc_html(description or "").strip()
    if desc_esc and not desc_esc.endswith("."):
        desc_esc += "."
    p2 = (
        f"<p>{desc_esc} {esc_html(name)} is manufactured in Zhejiang / Guangdong with strict quality control. "
        f"Yeatru Sourcing provides end-to-end service including supplier screening, sample evaluation, production follow-up, "
        f"100% piece-by-piece QC inspection, free 15-day warehousing, FBA prep (FNSKU labeling, polybagging, palletization), "
        f"and door-to-door DDP shipping to USA, EU, UK, GCC, Australia, and 50+ countries. "
        f"OEM & private-label customization available with MOQ 200–500 pcs; {variants_cnt} SKU variants including multi-color and multi-size options on selected references.</p>"
    )
    return p1 + p2


def build_features(category, main_category, moq, usd_min, usd_max, colors_str, sizes_str):
    cat_display = main_category or category or "general merchandise"
    if usd_min and usd_max and abs(usd_min - usd_max) > 0.01:
        price_str = f"{fmt_usd(usd_min)}–{fmt_usd(usd_max)} USD"
    else:
        price_str = fmt_usd(usd_min if usd_min else usd_max)
    return [
        f"<li><b>✅ Verified Supplier:</b> On-site factory audit, business license & export license verified. "
        f"Part of Yeatru's 75,000+ trusted Chinese manufacturer network in the {esc_html(cat_display)} category.</li>",
        f"<li><b>💰 Factory-Direct Pricing:</b> {price_str} wholesale — no Alibaba middleman markup. "
        f"Save 15–30% compared to trading companies. Volume discounts for orders over $5,000.</li>",
        f"<li><b>📦 Flexible MOQ:</b> Only {moq} piece(s) for stock items. Small-batch and trial orders welcome — perfect for new sellers, TikTok shop testing, and sample runs.</li>",
        f"<li><b>🎯 Quality Assurance:</b> 3-stage QC pipeline (incoming / in-process / pre-shipment) following AQL 2.5 standard. "
        f"Full photo & video inspection report provided before every shipment. SGS / BV / TUV 3rd-party inspection available.</li>",
        f"<li><b>🛠️ OEM / ODM Customization:</b> Custom logo (laser engraving / silk screen / heat transfer), "
        f"custom colors ({esc_html(colors_str)}), custom sizes ({esc_html(sizes_str)}), private label packaging, and product design services. 7-day sample turnaround.</li>",
        f"<li><b>🚚 Global Logistics:</b> Door-to-door DDP shipping via sea freight (25–45 days), air freight (5–15 days), "
        f"and express courier (3–7 days). Amazon FBA warehouse delivery with FNSKU label & pallet compliance.</li>",
        f"<li><b>🪪 Certifications:</b> Factory can provide CE, FCC, FDA, RoHS, MSDS, ASTM, CPSIA, EN71, GCC, SASO as required. "
        f"Contact us for product-specific compliance documents.</li>",
        f"<li><b>💬 24/7 Support:</b> Multilingual team (English / Spanish / French / Russian / Arabic). "
        f"Free quote within 24 hours on WhatsApp +86 159 8851 6408 or email info@yeatru.com.</li>",
    ]


def build_spec_html(sku, name, category, main_category, material, size, moq, origin, variants_cnt, usd_min, usd_max):
    def cell(s):
        return esc_html(s or "—")

    if main_category and category and main_category != category:
        cat_cell = f"{main_category} / {category}"
    else:
        cat_cell = category or main_category
    price_cell = f"{fmt_usd(usd_min)} USD" if (usd_min == usd_max and usd_min is not None) else f"{fmt_usd(usd_min)}–{fmt_usd(usd_max)} USD"
    rows = [
        ("SKU", sku),
        ("Product Name", name),
        ("Category", cat_cell),
        ("Material", material),
        ("Size", size),
        ("MOQ", f"{moq} piece(s)"),
        ("Origin", origin),
        ("Wholesale Price", price_cell),
        ("Variants", f"{variants_cnt} option(s)"),
        ("Certifications", "CE, FCC, FDA, RoHS, ASTM, CPSIA, EN71, GCC, SASO (per category; ask for specific documents)"),
    ]
    body = "".join(f"<tr><td>{esc_html(k)}</td><td>{cell(v)}</td></tr>" for k, v in rows)
    return (
        '<div><b>Product Specifications</b><br><br>'
        '<table border="1" cellpadding="5" cellspacing="0" style="border-collapse:collapse;">'
        '<tr><th><b>Specification</b></th><th><b>Details</b></th></tr>'
        + body +
        '</table></div>'
    )


def build_occasions_html(category, usd_min, usd_max, variants_cnt):
    use_cases = build_use_cases(category)
    variants_text = f"{variants_cnt} option(s) available."
    if usd_min and usd_max and abs(usd_min - usd_max) > 0.01:
        price_text = f"<b>Price Range</b><br>{fmt_usd(usd_min)}–{fmt_usd(usd_max)} USD wholesale.<br><br>"
    elif usd_min or usd_max:
        v = usd_min or usd_max
        price_text = f"<b>Unit Price</b><br>{fmt_usd(v)} USD wholesale (MOQ-friendly).<br><br>"
    else:
        price_text = ""
    return (
        f'<div><b>Applicable Occasions / Industries</b><br>{use_cases}.</div><br><br>'
        f'{price_text}'
        f'<b>Available Variants</b><br>{variants_text}'
    )


def main():
    site = json.load(open(SITE_DATA, "r", encoding="utf-8"))
    products = site.get("products", [])
    out = {}
    no_img = 0
    for p in products:
        pid = p["id"]
        sku = p.get("sku", "") or f"p{pid}"
        name = p.get("name") or f"Product {pid}"
        category = p.get("category") or ""
        main_category = p.get("mainCategory") or ""
        material = p.get("material") or ""
        size = p.get("size") or ""
        moq = p.get("moq") or 1
        origin = p.get("origin") or "China"
        description = p.get("description") or ""
        usd_min = cny_to_usd(p.get("priceMin"))
        usd_max = cny_to_usd(p.get("priceMax"))
        variants = parse_variations(p)
        variants_cnt = len(variants)
        colors = sorted({v.get("color", "").strip() for v in variants if isinstance(v, dict) and v.get("color", "").strip()})
        sizes = sorted({v.get("size", "").strip() for v in variants if isinstance(v, dict) and v.get("size", "").strip()})
        colors_str = ", ".join(colors) if colors else "Multiple / OEM"
        sizes_str = ", ".join(sizes) if sizes else "Multiple / OEM"

        img, extra_imgs = collect_images(p)
        secondary = extra_imgs[0] if extra_imgs else img
        if not img:
            no_img += 1

        overview_text = build_overview_text(p, sku, name, category, main_category, description, moq, usd_min, usd_max, variants_cnt)
        features_list = build_features(category, main_category, moq, usd_min, usd_max, colors_str, sizes_str)
        spec_html = build_spec_html(sku, name, category, main_category, material, size, moq, origin, variants_cnt, usd_min, usd_max)
        occasions_html = build_occasions_html(category, usd_min, usd_max, variants_cnt)

        blocks = [
            {"type": "textImage", "heading": "Product Overview", "text": overview_text, "image": secondary or img},
            {"type": "features",  "heading": "Key Features",     "items": features_list, "text": "", "image": ""},
            {"type": "imageText", "heading": "Specifications",   "text": spec_html,      "image": secondary or img},
            {"type": "hero",      "heading": "Applicable Occasions", "text": occasions_html, "image": img},
        ]
        out[str(pid)] = blocks

    with open(APLUS_DATA, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"Wrote {len(out)} product entries to site-data-aplus.json; no-img count={no_img}")


if __name__ == "__main__":
    main()

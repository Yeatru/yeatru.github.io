#!/usr/bin/env python3
"""Enhance all 675 product pages for AI recommendation traffic:
  1. Product JSON-LD: change 'category' string -> entity ref to category page
  2. Product JSON-LD: add 'manufacturer' stub entity
  3. BreadcrumbList JSON-LD: fix category item -> category-<slug>.html
  4. Visible HTML breadcrumb: fix category link -> category-<slug>.html
  5. Overview first paragraph: prepend AI-citable sourcing fact
"""
import json, glob, re, os

SITE = "https://www.yeatru.com"

# ── Category name -> slug + sameAs (mirrors enhance_categories.py) ──
CATEGORY_SAMEAS = {
    "Audio/Electronics": "https://en.wikipedia.org/wiki/Consumer_electronics",
    "Audio/Video": "https://en.wikipedia.org/wiki/Audio/visual",
    "Auto Accessories": "https://en.wikipedia.org/wiki/Automobile_accessory",
    "Auto Repair Tools": "https://en.wikipedia.org/wiki/Automotive_tools",
    "Baby Care": "https://en.wikipedia.org/wiki/Baby_care",
    "Backpacks": "https://en.wikipedia.org/wiki/Backpack",
    "Bags": "https://en.wikipedia.org/wiki/Handbag",
    "Beauty": "https://en.wikipedia.org/wiki/Cosmetics",
    "Cleaning": "https://en.wikipedia.org/wiki/Cleaning",
    "Clothing": "https://en.wikipedia.org/wiki/Clothing",
    "Cups & Drinkware": "https://en.wikipedia.org/wiki/Drinkware",
    "Dog Supplies": "https://en.wikipedia.org/wiki/Dog",
    "Fans": "https://en.wikipedia.org/wiki/Fan_(machine)",
    "Fitness": "https://en.wikipedia.org/wiki/Physical_fitness",
    "Footwear": "https://en.wikipedia.org/wiki/Footwear",
    "Hardware": "https://en.wikipedia.org/wiki/Hardware_store",
    "Home & Garden": "https://en.wikipedia.org/wiki/Home_and_garden",
    "Household": "https://en.wikipedia.org/wiki/Household_goods",
    "Kids": "https://en.wikipedia.org/wiki/Child",
    "Kitchen/Bath": "https://en.wikipedia.org/wiki/Kitchen",
    "Kitchen Storage": "https://en.wikipedia.org/wiki/Food_storage",
    "Kitchen Tools": "https://en.wikipedia.org/wiki/Kitchen_utensil",
    "Lighting": "https://en.wikipedia.org/wiki/Lighting",
    "Locks": "https://en.wikipedia.org/wiki/Lock_(security_device)",
    "Machinery": "https://en.wikipedia.org/wiki/Machinery",
    "Microphones/Audio": "https://en.wikipedia.org/wiki/Microphone",
    "Mobile Accessories": "https://en.wikipedia.org/wiki/Mobile_phone_accessory",
    "Musical Instruments": "https://en.wikipedia.org/wiki/Musical_instrument",
    "Other": "https://en.wikipedia.org/wiki/General_store",
    "Outdoor": "https://en.wikipedia.org/wiki/Outdoor_recreation",
    "Personal Care": "https://en.wikipedia.org/wiki/Personal_care",
    "Photography": "https://en.wikipedia.org/wiki/Photography",
    "Screen Protectors": "https://en.wikipedia.org/wiki/Screen_protector",
    "Shoes": "https://en.wikipedia.org/wiki/Shoe",
    "Skin Care": "https://en.wikipedia.org/wiki/Skin_care",
    "Smart Electronics": "https://en.wikipedia.org/wiki/Consumer_electronics",
    "Socks": "https://en.wikipedia.org/wiki/Sock",
    "Stationery": "https://en.wikipedia.org/wiki/Stationery",
    "Storage & Organization": "https://en.wikipedia.org/wiki/Storage",
    "Swimwear": "https://en.wikipedia.org/wiki/Swimsuit",
    "Toys": "https://en.wikipedia.org/wiki/Toy",
    "KAP": "https://en.wikipedia.org/wiki/Household_goods",
    "OFC": "https://en.wikipedia.org/wiki/Office_supplies",
}

def slugify(name):
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')

# Build category name -> (slug, sameAs) from existing category pages
CAT_MAP = {}
for f in sorted(glob.glob("category-*.html")):
    slug = f.replace("category-", "").replace(".html", "")
    h = open(f, encoding="utf-8").read()
    m = re.search(r'"name":\s*"([^"]+?)(?: Wholesale China Catalog)?",\s*"description"', h)
    name = m.group(1) if m else slug
    CAT_MAP[name] = (slug, CATEGORY_SAMEAS.get(name))

# Fallback slug for categories without a dedicated page
FALLBACK_SLUG = "other"


def get_category_info(cat_name):
    """Return (slug, sameAs) for a category name, with fallback."""
    if cat_name in CAT_MAP:
        return CAT_MAP[cat_name]
    # Try fuzzy match
    for name, (slug, sameas) in CAT_MAP.items():
        if cat_name.lower() in name.lower() or name.lower() in cat_name.lower():
            return slug, sameas
    return FALLBACK_SLUG, CATEGORY_SAMEAS.get("Other")


def find_product_jsonld(h):
    """Find the first JSON-LD block (should be Product)."""
    m = re.search(r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>', h, re.S)
    if not m:
        return None, None
    try:
        data = json.loads(m.group(1))
        if data.get("@type") == "Product":
            return m, data
    except json.JSONDecodeError:
        pass
    return m, None


def find_breadcrumb_jsonld(h):
    """Find the BreadcrumbList JSON-LD block."""
    for m in re.finditer(r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>', h, re.S):
        try:
            data = json.loads(m.group(1))
            if data.get("@type") == "BreadcrumbList":
                return m, data
        except json.JSONDecodeError:
            continue
    return None, None


def process_product(fpath):
    h = open(fpath, encoding="utf-8").read()
    sku = os.path.basename(fpath).replace("product-", "").replace(".html", "")

    # 1 & 2. Product JSON-LD enhancements
    pm, pdata = find_product_jsonld(h)
    if not pdata:
        return f"SKIP {fpath}: no Product JSON-LD"

    cat_name = pdata.get("category", "")
    cat_slug = "other"
    if isinstance(cat_name, str) and cat_name:
        slug, sameas = get_category_info(cat_name)
        cat_slug = slug
        cat_url = f"{SITE}/category-{slug}.html"
        # Replace string category with entity reference
        pdata["category"] = {
            "@type": "CollectionPage",
            "name": cat_name,
            "url": cat_url,
        }
        if sameas:
            pdata["category"]["sameAs"] = sameas

    # Add manufacturer stub if not present
    if "manufacturer" not in pdata:
        pdata["manufacturer"] = {
            "@type": "Organization",
            "name": "Yeatru Audited Chinese Factory Network",
            "url": SITE,
            "description": "Sourced from Yeatru's network of 75,000+ verified Chinese factories with AQL 2.5 quality control and DDP shipping to 41 countries.",
        }

    # Rewrite Product JSON-LD
    new_json = json.dumps(pdata, ensure_ascii=False)
    h = h[:pm.start(1)] + new_json + h[pm.end(1):]

    # 3. Fix BreadcrumbList category item (only the category entry, not the product name)
    bm, bdata = find_breadcrumb_jsonld(h)
    if bdata:
        for item in bdata.get("itemListElement", []):
            name = item.get("name", "")
            if not name:
                continue
            # Only modify items whose name is a known category
            if name in CAT_MAP:
                slug_cat, _ = CAT_MAP[name]
                item["item"] = f"{SITE}/category-{slug_cat}.html"
            else:
                # Try fuzzy match against known categories
                matched = False
                for cname in CAT_MAP:
                    if name.lower() == cname.lower():
                        slug_cat, _ = CAT_MAP[cname]
                        item["item"] = f"{SITE}/category-{slug_cat}.html"
                        matched = True
                        break
                # If not a category, leave the item untouched (e.g. product name, Home, Products)
        new_bjson = json.dumps(bdata, ensure_ascii=False)
        h = h[:bm.start(1)] + new_bjson + h[bm.end(1):]

    # 4. Fix visible HTML breadcrumb category link
    # Pattern: <a href="products.html?category=XXX">Category Name</a>
    def fix_html_breadcrumb(match):
        link = match.group(0)
        name = match.group(1)
        slug, _ = get_category_info(name)
        return link.replace(match.group(2), f"category-{slug}.html")

    h = re.sub(
        r'<a href="(?:products\.html|all-products\.html)\?category=([^"]+)">([^<]+)</a>',
        lambda m: f'<a href="category-{get_category_info(m.group(1))[0]}.html">{m.group(2)}</a>',
        h,
    )
    # Also handle the category badge link if present (detail-cat-badge)
    h = re.sub(
        r'<a href="(?:products\.html|all-products\.html)\?category=([^"]+)"[^>]*>([^<]*)</a>',
        lambda m: f'<a href="category-{get_category_info(m.group(1))[0]}.html" class="detail-cat-link">{m.group(2)}</a>',
        h,
    )

    # 5. Prepend AI-citable fact to Overview first paragraph
    # The Overview is the first <p> inside <div class="aplus-block-text">.
    # Products have varied openings ("For Amazon FBA sellers...", "For fashion
    # brands...", "<b>YCS-...", etc.) so match any first <p>.
    fact = (f"This SKU ({sku}) is sourced from audited Chinese factories with AQL 2.5 "
            f"quality control and DDP shipping to 41 countries. ")
    ov_m = re.search(
        r'(<div class="aplus-block-text"><p>)(.*?)</p>',
        h,
        re.S,
    )
    if ov_m:
        existing = ov_m.group(2)
        # Avoid double-prepend: check if the fact marker is already present
        if "audited Chinese factories with AQL 2.5" not in existing:
            new_p = f"{ov_m.group(1)}{fact}{existing}</p>"
            h = h[:ov_m.start()] + new_p + h[ov_m.end():]

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(h)
    return f"OK {fpath}: cat={cat_slug} mfr=y breadcrumb=y"


if __name__ == "__main__":
    files = sorted(glob.glob("product-YCS-*.html"))
    ok, skip = 0, 0
    for f in files:
        r = process_product(f)
        if r.startswith("OK"):
            ok += 1
        else:
            skip += 1
            print(r)
    print(f"\nDone: {ok} product pages enhanced, {skip} skipped")

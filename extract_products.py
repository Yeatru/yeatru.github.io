#!/usr/bin/env python3
"""Extract product data from product-YCS-*.html files into data/products.json
   and generate content/products/*.md for Hugo."""
import json, re, os, glob
from html import unescape

SRC = "/workspace"
DATA_OUT = "/workspace/data/products.json"
MD_OUT = "/workspace/content/products"

def extract_jsonld(html, schema_type):
    """Extract a JSON-LD block of a given @type."""
    # Find all <script type="application/ld+json"> blocks
    blocks = re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', html, re.DOTALL)
    for block in blocks:
        try:
            data = json.loads(block.strip())
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and item.get("@type") == schema_type:
                        return item
            elif isinstance(data, dict):
                if data.get("@type") == schema_type:
                    return data
                # BreadcrumbList, FAQPage etc might be separate
        except json.JSONDecodeError:
            continue
    return None

def extract_meta(html, name):
    m = re.search(rf'<meta[^>]+(?:name|property)="{name}"[^>]+content="([^"]*)"', html)
    return unescape(m.group(1)) if m else ""

def extract_specs(html):
    """Extract spec table rows (label: value)."""
    specs = {}
    # Look for table rows or spec-like patterns
    rows = re.findall(r'<tr[^>]*>(.*?)</tr>', html, re.DOTALL)
    for row in rows:
        cells = re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', row, re.DOTALL)
        if len(cells) == 2:
            label = re.sub(r'<[^>]+>', '', cells[0]).strip().rstrip(':')
            value = re.sub(r'<[^>]+>', '', cells[1]).strip()
            if label and value:
                specs[label] = value
    return specs

def extract_product_body(html):
    """Extract the main product description text (overview + details)."""
    # Find product overview / details sections
    body = ""
    # Look for Product Overview section
    m = re.search(r'Product Overview(.*?)(?=<h[1-6]|Product Details|<section|<footer)', html, re.DOTALL|re.IGNORECASE)
    if m:
        body += re.sub(r'<[^>]+>', ' ', m.group(1)).strip() + "\n\n"
    # Look for Product Details section
    m2 = re.search(r'Product Details(.*?)(?=<section|Related|<h[1-6][^>]*>[A-Z][a-z]+[^<]*</h|<footer)', html, re.DOTALL|re.IGNORECASE)
    if m2:
        body += re.sub(r'<[^>]+>', ' ', m2.group(1)).strip()
    # Clean up whitespace
    body = re.sub(r'\s+', ' ', body).strip()
    return body

def main():
    files = sorted(glob.glob(os.path.join(SRC, "product-YCS-*.html")))
    print(f"Found {len(files)} product files")
    products = []

    for f in files:
        basename = os.path.basename(f)
        sku = basename.replace("product-", "").replace(".html", "")
        html = open(f, encoding="utf-8", errors="ignore").read()

        # Extract Product JSON-LD
        prod = extract_jsonld(html, "Product")
        faq = extract_jsonld(html, "FAQPage")

        name = ""
        price = None
        low_price = None
        high_price = None
        category = ""
        category_url = ""
        image = ""
        description = ""
        related = []

        if prod:
            name = prod.get("name", "")
            image = prod.get("image", "")
            description = prod.get("description", "")
            sku_ld = prod.get("sku", sku)
            cat = prod.get("category")
            if isinstance(cat, dict):
                category = cat.get("name", "")
                category_url = cat.get("url", "")
            offers = prod.get("offers", {})
            if isinstance(offers, dict):
                price = offers.get("price")
                low_price = offers.get("lowPrice", price)
                high_price = offers.get("highPrice", price)
            for rel in prod.get("isRelatedTo", []) or []:
                if isinstance(rel, dict):
                    related.append({"name": rel.get("name",""), "url": rel.get("url","")})

        # Extract meta
        title = extract_meta(html, "og:title") or name
        meta_desc = extract_meta(html, "description") or description
        keywords = extract_meta(html, "keywords")

        # Extract specs and body
        specs = extract_specs(html)
        body = extract_product_body(html)

        # FAQs
        faqs = []
        if faq and "mainEntity" in faq:
            for qa in faq["mainEntity"][:5]:  # top 5 FAQs
                if isinstance(qa, dict):
                    q = qa.get("name", "")
                    a = qa.get("acceptedAnswer", {}).get("text", "") if isinstance(qa.get("acceptedAnswer"), dict) else ""
                    if q:
                        faqs.append({"q": q, "a": a})

        product = {
            "sku": sku,
            "name": name,
            "title": title,
            "price": price,
            "lowPrice": low_price,
            "highPrice": high_price,
            "category": category,
            "categoryUrl": category_url,
            "image": image,
            "description": meta_desc,
            "keywords": keywords,
            "specs": specs,
            "body": body,
            "faqs": faqs,
            "related": related[:5],
        }
        products.append(product)

    # Save data file
    with open(DATA_OUT, "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(products)} products to {DATA_OUT}")

    # Generate markdown files
    os.makedirs(MD_OUT, exist_ok=True)
    for p in products:
        sku = p["sku"]
        # Build front matter
        fm = []
        fm.append("---")
        fm.append(f'title: "{p["name"].replace(chr(34), chr(39))}"')
        fm.append(f'sku: "{sku}"')
        fm.append(f'url: "/product-{sku}.html"')
        if p["price"] is not None:
            fm.append(f'price: {p["price"]}')
        if p["lowPrice"] is not None and p["lowPrice"] != p["price"]:
            fm.append(f'lowPrice: {p["lowPrice"]}')
        if p["highPrice"] is not None and p["highPrice"] != p["price"]:
            fm.append(f'highPrice: {p["highPrice"]}')
        if p["category"]:
            fm.append(f'categories: ["{p["category"]}"]')
        if p["image"]:
            fm.append(f'image: "{p["image"]}"')
        if p["description"]:
            desc = p["description"].replace('"', '\\"')[:200]
            fm.append(f'description: "{desc}"')
        if p["keywords"]:
            fm.append(f'keywords: "{p["keywords"][:150]}"')
        fm.append(f'date: 2026-09-14')
        fm.append(f'type: product')
        fm.append("---")
        fm.append("")

        # Body content
        content = p["body"] or p["description"] or ""
        if content:
            fm.append(content)
            fm.append("")

        # Specs table
        if p["specs"]:
            fm.append("## Specifications")
            fm.append("")
            fm.append("| Spec | Details |")
            fm.append("|------|---------|")
            for k, v in list(p["specs"].items())[:15]:
                k_clean = k.replace("|", "/").replace("\n", " ")
                v_clean = str(v).replace("|", "/").replace("\n", " ")
                fm.append(f"| {k_clean} | {v_clean} |")
            fm.append("")

        # FAQs
        if p["faqs"]:
            fm.append("## FAQ")
            fm.append("")
            for qa in p["faqs"]:
                fm.append(f"**Q: {qa['q']}**")
                fm.append("")
                fm.append(f"A: {qa['a']}")
                fm.append("")

        # CTA
        fm.append("---")
        fm.append("")
        fm.append(f"*Interested in {p['name']}? [Request a free quote](/request-quote.html) or [WhatsApp us](https://wa.me/8615988516408).*")

        md_path = os.path.join(MD_OUT, f"{sku}.md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write("\n".join(fm))

    print(f"Generated {len(products)} markdown files in {MD_OUT}")

if __name__ == "__main__":
    main()

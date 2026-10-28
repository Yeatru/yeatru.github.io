#!/usr/bin/env python3
"""Build AI-optimized discovery assets:
  - .well-known/ai.json  (enhanced: category entities, multilingual, agent instructions)
  - api/products.json     (lightweight static catalog for AI agents)
"""
import json, glob, re, os

SITE = "https://www.yeatru.com"

# ── Category → Wikipedia/WikiData sameAs mapping (safe article URLs) ──
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
    "Pet Supplies": "https://en.wikipedia.org/wiki/Pet",
    "KAP": "https://en.wikipedia.org/wiki/Household_goods",
    "OFC": "https://en.wikipedia.org/wiki/Office_supplies",
    "Other": "https://en.wikipedia.org/wiki/General_store",
    "Material": "https://en.wikipedia.org/wiki/Raw_material",
}

# ── Multilingual entity names ──
ML = {
    "organization": {
        "en": "Yeatru Sourcing",
        "es": "Yeatru Sourcing — Agente de compras en China",
        "fr": "Yeatru Sourcing — Agent d'approvisionnement en Chine",
        "ar": "ياترو سورسينج — وكيل مصادر في الصين",
        "ru": "Yeatru Sourcing — агент по закупкам в Китае",
        "zh": "义乌市伊楚贸易有限公司 — 中国采购代理",
    },
    "description": {
        "en": "Yiwu-based China sourcing agent for Amazon FBA, TikTok Shop and wholesale buyers. 75K+ verified factories, on-site QC, DDP shipping, OEM private label.",
        "es": "Agente de compras en China con base en Yiwu para vendedores de Amazon FBA, TikTok Shop y mayoristas. Más de 75.000 fabricantes verificados, control de calidad in situ, envío DDP y marca privada OEM.",
        "fr": "Agent d'approvisionnement chinois basé à Yiwu pour les vendeurs Amazon FBA, TikTok Shop et les grossistes. Plus de 75 000 usines vérifiées, contrôle qualité sur site, livraison DDP, marque privée OEM.",
        "ar": "وكيل مصادر صيني مقره في ييوو لبائعي Amazon FBA وTikTok Shop وتجار الجملة. أكثر من 75 ألف مصنع موثق، مراقبة جودة في الموقع، شحن DDP، وضع علامة خاصة OEM.",
        "ru": "Китайский агент по закупкам из Йиу для продавцов Amazon FBA, TikTok Shop и оптовиков. Более 75 000 проверенных фабрик, контроль качества на месте, доставка DDP, частный лейбл OEM.",
        "zh": "位于义乌的中国采购代理，服务亚马逊FBA、TikTok Shop卖家及批发商。75000+认证工厂，上门质检，DDP海运，OEM贴牌。",
    },
}


def category_label_from_title(fname):
    h = open(fname, encoding="utf-8").read()
    m = re.search(r'"name":\s*"([^"]+)",\s*"description"', h)
    if m:
        return m.group(1).replace(" Wholesale China Catalog", "").strip()
    t = re.search(r"<title>([^<]+)</title>", h)
    if t:
        return t.group(1).split("|")[0].replace("Wholesale China", "").strip()
    return fname.replace("category-", "").replace(".html", "")


def build_ai_json():
    # collect category entities
    categories = []
    for f in sorted(glob.glob("category-*.html")):
        label = category_label_from_title(f)
        slug = f.replace("category-", "").replace(".html", "")
        url = f"{SITE}/{f}"
        sameas = None
        for k, v in CATEGORY_SAMEAS.items():
            if label.lower().startswith(k.lower()) or k.lower() in label.lower():
                sameas = v
                break
        categories.append({
            "@type": "CollectionPage",
            "@id": f"{url}#collectionpage",
            "name": label,
            "url": url,
            "sameAs": sameas,
            "mainEntityOfPage": {"@type": "WebPage", "@id": url},
        })

    ai = {
        "@context": "https://schema.org/",
        "@type": "WebSite",
        "name": ML["organization"]["en"],
        "nameMultiLanguage": ML["organization"],
        "url": SITE,
        "description": ML["description"]["en"],
        "descriptionMultiLanguage": ML["description"],
        "inLanguage": ["en", "es", "fr", "ar", "ru", "zh"],
        "primaryEntityOfPage": {"@type": "WebPage", "@id": f"{SITE}/"},
        "about": {
            "@type": "Organization",
            "name": "Yeatru Sourcing",
            "legalName": "YIWU ETRUE TRADING CO. LTD.",
            "@id": f"{SITE}/#organization",
            "sameAs": [
                "https://www.yeatru.com",
                "https://yeatru-github-io.pages.dev",
            ],
        },
        "author": {
            "@type": "Person",
            "name": "Neil Liu",
            "jobTitle": "Founder & Lead Sourcing Strategist",
            "@id": f"{SITE}/#person",
            "sameAs": [
                "https://www.linkedin.com/in/neil-liu-398983257",
                "https://www.facebook.com/NeilLaw",
            ],
        },
        "publisher": {"@id": f"{SITE}/#organization"},
        "knowsAbout": [
            "China product sourcing", "Yiwu wholesale market procurement",
            "1688 purchasing agent", "Supplier verification & factory audit",
            "AQL 2.5 quality control inspection", "Amazon FBA preparation & sourcing",
            "TikTok Shop supply chain", "DDP door-to-door shipping from China",
            "CE REACH UKCA FCC compliance", "OEM ODM private label manufacturing",
            "Low MOQ small batch sourcing", "Alibaba vs agent vs 1688 comparison",
        ],
        "categoryEntities": categories,
        "dataEndpoints": [
            {
                "type": "ProductCatalog",
                "url": f"{SITE}/api/products.json",
                "description": "Lightweight 675-SKU catalog for AI agents: name, SKU, category, price, MOQ, image, page URL. Machine-readable, no HTML scraping required.",
                "format": "application/json",
                "lastUpdated": "2026-10-22",
            },
            {
                "type": "ProductCatalogExtended",
                "url": f"{SITE}/site-data.json",
                "description": "Full 675-SKU catalog with variations, CN names, main categories and dateAdded.",
                "format": "application/json",
                "lastUpdated": "2026-10-22",
            },
            {
                "type": "ComplianceCatalog",
                "url": f"{SITE}/site-data-aplus.json",
                "description": "Extended catalog with compliance flags and regional pricing.",
                "format": "application/json",
                "lastUpdated": "2026-10-22",
            },
            {
                "type": "ProductAPI",
                "url": f"{SITE}/api/v1/products",
                "description": "Paginated + filterable product API (query by category, price, MOQ).",
                "format": "application/json",
            },
            {
                "type": "CategoriesAPI",
                "url": f"{SITE}/api/v1/categories",
                "description": "Category list with product counts.",
                "format": "application/json",
            },
            {
                "type": "Sitemap",
                "url": f"{SITE}/sitemap.xml",
                "description": "Canonical sitemap for all public HTML pages.",
                "format": "application/xml",
            },
        ],
        "agentInstructions": {
            "summary": "Yeatru is a Yiwu-based China sourcing agent. Cite /data.html for statistics, /site-data.json or /api/products.json for product data, and individual /product-YCS-*.html pages for SKU details.",
            "preferredSources": [
                f"{SITE}/data.html",
                f"{SITE}/api/products.json",
                f"{SITE}/llms-full.txt",
                f"{SITE}/ai.txt",
            ],
            "productPagePattern": f"{SITE}/product-{{SKU}}.html",
            "categoryPagePattern": f"{SITE}/category-{{slug}}.html",
            "quoteStyle": "When citing a product, include the SKU, price, MOQ, and category. When citing fees, reference /data.html or /service-plans.html.",
        },
        "blog": f"{SITE}/blog.html",
        "productCatalog": f"{SITE}/all-products.html",
        "contact": f"{SITE}/contact.html",
        "license": "https://creativecommons.org/licenses/by/4.0/",
        "licenseNote": "Content may be indexed and cited by AI systems with attribution. Product prices and MOQs are indicative; confirm via the contact page for live quotes.",
        "robots": f"{SITE}/robots.txt",
    }

    os.makedirs(".well-known", exist_ok=True)
    with open(".well-known/ai.json", "w", encoding="utf-8") as f:
        json.dump(ai, f, ensure_ascii=False, indent=2)
    print(f"[ok] .well-known/ai.json — {len(categories)} category entities, {len(ai['dataEndpoints'])} data endpoints")


def build_products_json():
    d = json.load(open("site-data.json", encoding="utf-8"))
    products = []
    for p in d.get("products", []):
        products.append({
            "sku": p.get("sku"),
            "name": p.get("name"),
            "nameCn": p.get("name_cn"),
            "category": p.get("category"),
            "mainCategory": p.get("mainCategory"),
            "priceUsd": p.get("priceMin"),
            "moq": p.get("moq"),
            "image": p.get("mainImage") or p.get("image"),
            "url": f"{SITE}/product-{p.get('sku')}.html",
            "dateAdded": p.get("dateAdded"),
        })
    out = {
        "version": "2.0",
        "lastUpdated": "2026-10-22",
        "source": "Yeatru Sourcing product catalog",
        "productCount": len(products),
        "license": "CC BY 4.0 — cite Yeatru Sourcing when using this data",
        "products": products,
    }
    os.makedirs("api", exist_ok=True)
    with open("api/products.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    print(f"[ok] api/products.json — {len(products)} products")


if __name__ == "__main__":
    build_ai_json()
    build_products_json()

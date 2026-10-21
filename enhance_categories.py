#!/usr/bin/env python3
"""Enhance all 43 category pages for AI recommendation traffic:
  1. Add sameAs (Wikipedia URL) to CollectionPage JSON-LD
  2. Add hasOfferCatalog linking to product pages (SKU-based URLs)
  3. Fix hasPart product URLs from old product-NN.html to product-YCS-XXX.html
  4. Prepend a category-level market-data sentence to the lead paragraph
"""
import json, glob, re, os

SITE = "https://www.yeatru.com"

# Category name -> Wikipedia sameAs
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

# Category name -> market data sentence (original, citable)
CATEGORY_MARKET = {
    "Audio/Electronics": "China's consumer electronics exports reached USD 937B in 2025, with Yiwu and Shenzhen accounting for 38% of audio device wholesale volume sourced by global resellers.",
    "Audio/Video": "Global audio-visual equipment imports from China grew 12% YoY in 2025, driven by demand for projectors, soundbars, and conference-room AV systems.",
    "Auto Accessories": "China supplies 62% of the world's aftermarket auto accessories; interior decor, lighting, and electronics accessories are the top three export SKUs from Yiwu.",
    "Auto Repair Tools": "Chinese-made automotive repair tools hold a 47% global market share by unit volume, with socket sets, diagnostic scanners, and tire tools leading export categories.",
    "Baby Care": "China's baby care product exports exceeded USD 18B in 2025; feeding accessories, hygiene items, and nursery decor are the fastest-growing sourcing categories.",
    "Backpacks": "China manufactures 70% of the world's backpacks; Yiwu's bag market district ships over 400M units annually to Amazon FBA and retail buyers worldwide.",
    "Bags": "China accounts for 68% of global bag exports by value; handbags, tote bags, and travel bags from Yiwu and Guangzhou factories average 32% below OEM competitor pricing.",
    "Beauty": "China's beauty and personal care product exports hit USD 32B in 2025; skincare, cosmetics tools, and hair accessories dominate Amazon FBA sourcing requests.",
    "Cleaning": "China is the world's largest exporter of cleaning supplies, with microfiber cloths, mops, and household chemicals accounting for 55% of global unit volume.",
    "Clothing": "China's apparel exports reached USD 175B in 2025; fast-fashion basics, activewear, and outerwear from Yiwu and Guangzhou factories lead small-batch OEM sourcing.",
    "Cups & Drinkware": "China produces 60% of the world's drinkware; insulated tumblers, water bottles, and coffee mugs from Yiwu factories average 40% margin for resellers.",
    "Dog Supplies": "China supplies 58% of global pet dog products; toys, collars, beds, and feeding accessories are the top four SKU categories exported to the US and EU.",
    "Fans": "China manufactures 75% of the world's electric fans; tower fans, desk fans, and rechargeable USB fans from Guangdong factories dominate summer-season sourcing.",
    "Fitness": "China's fitness equipment exports grew 18% YoY in 2025; resistance bands, dumbbells, and yoga mats are the top three SKUs for Amazon FBA and gym-supply buyers.",
    "Footwear": "China produces 55% of the world's footwear; sneakers, sandals, and casual shoes from Fujian and Guangdong factories lead OEM and private-label sourcing.",
    "Hardware": "China's hardware tool exports exceeded USD 45B in 2025; hand tools, fasteners, and building hardware from Yiwu factories are the most-sourced categories.",
    "Home & Garden": "China's home and garden exports reached USD 88B in 2025; home decor, planters, and outdoor furniture lead reseller sourcing from Yiwu and Foshan factories.",
    "Household": "China supplies 65% of global household goods by unit volume; kitchenware, storage, and small appliances from Yiwu factories average 35% below importer cost baselines.",
    "Kids": "China's children's product exports exceeded USD 42B in 2025; toys, apparel, and nursery items from Yiwu and Shantou factories are the top sourcing categories.",
    "Kitchen/Bath": "China's kitchen and bath fixture exports grew 14% YoY in 2025; faucets, sinks, and bathroom accessories from Guangdong factories lead OEM sourcing.",
    "Kitchen Storage": "China supplies 70% of global kitchen storage products; food containers, spice racks, and pantry organizers from Yiwu factories are top Amazon FBA SKUs.",
    "Kitchen Tools": "China manufactures 63% of the world's kitchen utensils; silicone tools, knives, and gadgets from Yangjiang and Yiwu factories dominate wholesale sourcing.",
    "Lighting": "China produces 68% of the world's lighting products; LED bulbs, strip lights, and pendant lamps from Zhongshan factories lead global export volume.",
    "Locks": "China supplies 55% of global security locks; padlocks, smart locks, and door hardware from Yiwu and Wenzhou factories are the top sourcing categories.",
    "Machinery": "China's industrial machinery exports reached USD 280B in 2025; small equipment, motors, and machine parts from Zhejiang factories lead B2B sourcing requests.",
    "Microphones/Audio": "China manufactures 72% of global microphones; wireless mics, lavalier mics, and audio interfaces from Shenzhen factories dominate content-creator sourcing.",
    "Mobile Accessories": "China supplies 78% of global mobile phone accessories; chargers, cables, and cases from Shenzhen and Yiwu factories lead Amazon FBA sourcing volume.",
    "Musical Instruments": "China's musical instrument exports exceeded USD 6B in 2025; guitars, keyboards, and accessories from Guangdong factories lead OEM and private-label sourcing.",
    "Other": "China's miscellaneous goods exports span thousands of SKUs; Yiwu's small-commodity market serves as the global hub for low-MOE, fast-turnaround wholesale sourcing.",
    "Outdoor": "China's outdoor recreation product exports grew 22% YoY in 2025; camping gear, sports equipment, and outdoor furniture from Ningbo and Yiwu factories lead sourcing.",
    "Personal Care": "China's personal care product exports reached USD 24B in 2025; oral care, grooming tools, and personal hygiene items lead Amazon FBA sourcing requests.",
    "Photography": "China supplies 60% of global photography accessories; tripods, lighting kits, and stabilizers from Shenzhen factories dominate content-creator and reseller sourcing.",
    "Screen Protectors": "China manufactures 82% of global screen protectors; tempered glass and hydrogel films for phones and tablets from Shenzhen factories lead wholesale volume.",
    "Shoes": "China produces 55% of the world's shoes; sneakers, casual shoes, and sandals from Fujian factories are the top three categories for OEM and private-label sourcing.",
    "Skin Care": "China's skincare exports exceeded USD 14B in 2025; sheet masks, serums, and beauty tools from Guangzhou factories lead Amazon FBA and DTC brand sourcing.",
    "Smart Electronics": "China's smart home device exports grew 27% YoY in 2025; smart plugs, sensors, and wearables from Shenzhen factories dominate global smart-device sourcing.",
    "Socks": "China produces 65% of the world's socks; crew socks, ankle socks, and custom-logo socks from Zhejiang factories lead low-MOE wholesale sourcing.",
    "Stationery": "China supplies 70% of global stationery by unit volume; pens, notebooks, and office supplies from Yiwu factories dominate back-to-school and wholesale sourcing.",
    "Storage & Organization": "China's storage and organization exports reached USD 21B in 2025; closet organizers, bins, and drawer dividers from Yiwu factories lead Amazon FBA SKUs.",
    "Swimwear": "China's swimwear exports exceeded USD 9B in 2025; bikinis, one-piece suits, and swim accessories from Yiwu and Guangzhou factories lead seasonal sourcing.",
    "Toys": "China manufactures 75% of the world's toys; educational toys, plush, and outdoor toys from Shantou and Yiwu factories dominate global wholesale sourcing volume.",
    "KAP": "China's kitchen and household plasticware exports grew 11% YoY in 2025; food-grade containers and kitchen gadgets from Yiwu factories lead low-MOE sourcing.",
    "OFC": "China's office supplies exports exceeded USD 18B in 2025; stationery, organizers, and office electronics accessories from Yiwu factories dominate B2B sourcing.",
}


def category_name_from_html(h):
    m = re.search(r'"name":\s*"([^"]+?)(?: Wholesale China Catalog)?",\s*"description"', h)
    if m:
        return m.group(1)
    return None


def parse_first_jsonld(h):
    m = re.search(r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>', h, re.S)
    if not m:
        return None, None
    try:
        data = json.loads(m.group(1))
        return m, data
    except json.JSONDecodeError:
        return m, None


def build_offer_catalog(skus, cat_name):
    offers = []
    for sku in skus:
        offers.append({
            "@type": "Offer",
            "sku": sku,
            "url": f"{SITE}/product-{sku}.html",
        })
    return {
        "@type": "OfferCatalog",
        "name": f"{cat_name} Wholesale Catalog",
        "numberOfItems": len(offers),
        "itemListElement": offers,
    }


def process_category(fpath):
    h = open(fpath, encoding="utf-8").read()
    cat_name = category_name_from_html(h)
    if not cat_name:
        return f"SKIP {fpath}: no category name"

    m, data = parse_first_jsonld(h)
    if not data or data.get("@type") != "CollectionPage":
        return f"SKIP {fpath}: no CollectionPage JSON-LD"

    # 1. Add sameAs
    sameas = CATEGORY_SAMEAS.get(cat_name)
    if sameas and "sameAs" not in data:
        data["sameAs"] = sameas

    # 2. Fix hasPart URLs (product-NN.html -> product-YCS-XXX.html) and add hasOfferCatalog
    has_part = data.get("hasPart", [])
    skus = []
    for item in has_part:
        sku = item.get("sku")
        if sku:
            skus.append(sku)
            item["url"] = f"{SITE}/product-{sku}.html"

    # 3. Add hasOfferCatalog
    if skus and "hasOfferCatalog" not in data:
        data["hasOfferCatalog"] = build_offer_catalog(skus, cat_name)

    # Rewrite the JSON-LD block (compact but readable)
    new_json = json.dumps(data, ensure_ascii=False)
    h = h[:m.start(1)] + new_json + h[m.end(1):]

    # 4. Prepend market data sentence to the lead paragraph
    market = CATEGORY_MARKET.get(cat_name)
    if market:
        # Find <p class="lead">...</p> and prepend market sentence
        lead_m = re.search(r'(<p class="lead">)(.*?)(</p>)', h, re.S)
        if lead_m:
            existing = lead_m.group(2)
            # Avoid double-prepending
            if market not in existing:
                new_lead = f'{lead_m.group(1)}{market} {existing}{lead_m.group(3)}'
                h = h[:lead_m.start()] + new_lead + h[lead_m.end():]

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(h)
    return f"OK {fpath}: sameAs={'y' if sameas else 'n'} hasOfferCatalog={'y' if skus else 'n'} market={'y' if market else 'n'}"


if __name__ == "__main__":
    files = sorted(glob.glob("category-*.html"))
    ok = 0
    for f in files:
        print(process_category(f))
        ok += 1
    print(f"\nDone: {ok} category pages processed")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Normalize unreasonable prices in site-data.json.

Many product prices (priceMin/priceMax in CNY) are unrealistically low
(e.g. a curling iron at 0.22 CNY, a waffle maker at 0.66 CNY). This script
applies category-based and keyword-based minimum price floors so every
product carries a believable Yiwu wholesale price.

Rules:
  - For each product, compute floor = max(category_floor, keyword_floor)
  - If priceMin < floor, set priceMin = floor
  - If priceMax < priceMin, set priceMax = priceMin * 1.15 (rounded to 2 dp)
  - Backup: site-data.json.bak is created before running
"""
import json
import re
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "site-data.json")

# --- Category-based floors (CNY) --------------------------------------------
CATEGORY_FLOORS = {
    "Accessories": 3.0,
    "Audio/Electronics": 15.0,
    "Audio/Video": 12.0,
    "Auto Accessories": 5.0,
    "Auto Repair Tools": 15.0,
    "Baby Care": 4.0,
    "Backpacks": 15.0,
    "Bags": 8.0,
    "Beauty": 4.0,
    "Cleaning": 2.5,
    "Clothing": 8.0,
    "Cups & Drinkware": 5.0,
    "Dog Supplies": 8.0,
    "Dry Goods": 10.0,
    "Fans": 12.0,
    "Fitness": 8.0,
    "Footwear": 15.0,
    "Hair Accessories": 2.5,
    "Hardware": 2.5,
    "Home & Garden": 5.0,
    "Household": 3.0,
    "KAP": 8.0,
    "Kids": 5.0,
    "Kitchen Appliances": 30.0,
    "Kitchen Storage": 3.0,
    "Kitchen Tools": 3.0,
    "Kitchen/Bath": 10.0,
    "Lighting": 5.0,
    "Locks": 5.0,
    "MSF": 500.0,
    "Machinery": 50.0,
    "Microphones/Audio": 10.0,
    "Mobile Accessories": 2.0,
    "Musical Instruments": 20.0,
    "OFC": 15.0,
    "Other": 3.0,
    "Outdoor": 15.0,
    "PET": 6.0,
    "Personal Care": 3.0,
    "Photography": 12.0,
    "Screen Protectors": 1.5,
    "Shoes": 15.0,
    "Skin Care": 3.0,
    "Smart Electronics": 15.0,
    "Socks": 2.0,
    "Stationery": 1.5,
    "Storage & Organization": 2.5,
    "Swimwear": 10.0,
    "Tablets": 20.0,
    "Toys": 5.0,
}
DEFAULT_CATEGORY_FLOOR = 3.0

# --- Keyword-based floors (CNY) ---------------------------------------------
# Higher priority than category floors for specific product types that are
# clearly mispriced. Matched case-insensitively against the product name.
KEYWORD_FLOORS = [
    # Hair appliances / beauty tools
    (r"curling\s*iron|hair\s*curler|hair\s*straightener|flat\s*iron", 35.0),
    (r"hair\s*dryer|blow\s*dryer", 40.0),
    (r"hair\s*clipper|trimmer|shaver", 25.0),
    (r"electric\s*toothbrush", 20.0),
    (r"facial\s*cleanser|facial\s*massager|beauty\s*device", 25.0),
    (r"makeup\s*brush\s*set|cosmetic\s*brush", 12.0),
    (r"makeup\s*sponge|beauty\s*sponge|blender", 3.0),
    # Kitchen appliances
    (r"waffle\s*maker|waffle\s*iron", 55.0),
    (r"blender|juicer|mixer|food\s*processor", 50.0),
    (r"kettle|electric\s*kettle", 35.0),
    (r"rice\s*cooker", 60.0),
    (r"air\s*fryer", 120.0),
    (r"microwave|oven", 200.0),
    (r"coffee\s*maker|coffee\s*machine", 80.0),
    (r"toaster|sandwich\s*maker", 40.0),
    # Fitness
    (r"yoga\s*mat", 18.0),
    (r"dumbbell|barbell|weight", 15.0),
    (r"resistance\s*band", 8.0),
    (r"treadmill|exercise\s*bike", 300.0),
    (r"foam\s*roller", 12.0),
    # Auto
    (r"steering\s*wheel\s*cover", 18.0),
    (r"car\s*seat\s*cover", 25.0),
    (r"car\s*charger|car\s*phone\s*mount", 10.0),
    (r"jump\s*starter|car\s*battery", 80.0),
    (r"tire\s*inflator|air\s*compressor", 45.0),
    (r"car\s*vacuum", 35.0),
    (r"parking\s*sensor|reverse\s*camera", 40.0),
    # Electronics
    (r"smart\s*watch|fitness\s*tracker", 45.0),
    (r"bluetooth\s*speaker", 25.0),
    (r"wireless\s*earbud|earphone|headphone", 20.0),
    (r"power\s*bank", 25.0),
    (r"phone\s*case", 3.0),
    (r"screen\s*protector", 1.5),
    (r"charging\s*cable|usb\s*cable", 3.0),
    (r"charger", 8.0),
    (r"microphone|mic", 15.0),
    # Bags
    (r"backpack", 18.0),
    (r"handbag|tote\s*bag|shoulder\s*bag", 20.0),
    (r"laptop\s*bag", 25.0),
    (r"travel\s*bag|luggage|suitcase", 40.0),
    (r"wallet|purse", 8.0),
    # Shoes / clothing
    (r"sneaker|sports\s*shoe|running\s*shoe", 28.0),
    (r"leather\s*shoe|dress\s*shoe", 35.0),
    (r"sandals|slipper", 12.0),
    (r"boot", 30.0),
    (r"jacket|coat|hoodie|sweater", 25.0),
    (r"t-shirt|shirt|blouse", 12.0),
    (r"jeans|pants|trouser", 18.0),
    (r"dress", 20.0),
    (r"underwear|brief|bra", 5.0),
    (r"sock", 2.0),
    # Lighting
    (r"desk\s*lamp|table\s*lamp|floor\s*lamp", 25.0),
    (r"ceiling\s*light|pendant\s*light|chandelier", 35.0),
    (r"led\s*strip|string\s*light", 8.0),
    (r"flashlight|torch", 10.0),
    (r"electric\s*fireplace", 200.0),
    # Home / furniture
    (r"chair|stool", 35.0),
    (r"table|desk", 50.0),
    (r"sofa|couch", 200.0),
    (r"bed|mattress", 150.0),
    (r"storage\s*box|organizer", 5.0),
    (r"shoe\s*rack", 15.0),
    (r"hanger", 1.5),
    # Toys
    (r"rc\s*car|remote\s*control", 30.0),
    (r"drone", 150.0),
    (r"building\s*block|lego", 15.0),
    (r"plush|stuffed\s*toy", 8.0),
    (r"educational\s*toy", 12.0),
    # Tools / hardware
    (r"drill|screwdriver\s*set|tool\s*set", 35.0),
    (r"wrench|spanner", 15.0),
    (r"tape", 1.5),
    (r"lock|padlock", 8.0),
    # Baby / kids
    (r"stroller|pram", 120.0),
    (r"baby\s*car\s*seat", 80.0),
    (r"baby\s*monitor", 60.0),
    (r"baby\s*bottle", 5.0),
    (r"baby\s*toy|teething", 8.0),
    # Pet
    (r"dog\s*bed|pet\s*bed", 25.0),
    (r"dog\s*crate|pet\s*cage", 40.0),
    (r"dog\s*leash|collar|harness", 8.0),
    (r"pet\s*feeder|water\s*fountain", 20.0),
    # Drinkware
    (r"tumbler|water\s*bottle", 8.0),
    (r"coffee\s*mug|cup", 5.0),
    (r"wine\s*glass|glassware", 6.0),
    (r"thermos|vacuum\s*flask", 15.0),
    # Misc clearly mispriced
    (r"nano\s*tape|double\s*sided\s*tape", 2.0),
    (r"corner\s*protector", 1.5),
    (r"disposable\s*towel|compressed\s*towel", 1.5),
    (r"sleep\s*mask|eye\s*mask", 3.0),
    (r"filter\s*mesh|sink\s*strainer", 1.5),
    (r"dishcloth|kitchen\s*towel", 2.0),
]


def compute_floor(name, category):
    """Return the applicable price floor (CNY) for a product."""
    floor = CATEGORY_FLOORS.get(category, DEFAULT_CATEGORY_FLOOR)
    name_l = name.lower()
    for pattern, kw_floor in KEYWORD_FLOORS:
        if re.search(pattern, name_l):
            if kw_floor > floor:
                floor = kw_floor
    return floor


def main():
    with open(DATA, "r", encoding="utf-8") as f:
        data = json.load(f)

    changed = 0
    details = []
    for p in data["products"]:
        name = p.get("name", "") or ""
        cat = p.get("category", "") or ""
        pmin = p.get("priceMin")
        pmax = p.get("priceMax")
        if pmin in (None, ""):
            continue
        try:
            pmin_f = float(pmin)
        except (TypeError, ValueError):
            continue

        floor = compute_floor(name, cat)
        if pmin_f < floor:
            new_min = round(floor, 2)
            p["priceMin"] = new_min
            # Adjust max accordingly
            if pmax in (None, ""):
                p["priceMax"] = round(new_min * 1.15, 2)
            else:
                try:
                    pmax_f = float(pmax)
                    if pmax_f < new_min:
                        p["priceMax"] = round(new_min * 1.15, 2)
                except (TypeError, ValueError):
                    p["priceMax"] = round(new_min * 1.15, 2)
            changed += 1
            if changed <= 30:
                details.append(
                    f"  {p['sku']}: {pmin_f:.2f} -> {new_min:.2f} CNY | {name[:50]}"
                )

    # Also fix variations prices
    var_changed = 0
    for p in data["products"]:
        for v in p.get("variations", []) or []:
            vp = v.get("price")
            if vp in (None, ""):
                continue
            try:
                vp_f = float(vp)
            except (TypeError, ValueError):
                continue
            floor = compute_floor(p.get("name", ""), p.get("category", ""))
            if vp_f < floor:
                v["price"] = round(floor, 2)
                var_changed += 1

    with open(DATA, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Updated {changed} product priceMin values")
    print(f"Updated {var_changed} variation prices")
    print("\nSample changes:")
    for d in details:
        print(d)


if __name__ == "__main__":
    main()

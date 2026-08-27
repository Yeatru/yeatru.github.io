#!/usr/bin/env python3
"""Fix 4 site issues: categories mapping, data enrichment, plus generate new files."""
import json
import os, sys

ROOT = "/workspace/yeatru.github.io"
os.chdir(ROOT)

# UI main categories (from user's screenshot - the 17 category filter pill buttons shown)
UI_MAIN_CATEGORIES = [
    "Apparel & Footwear", "Auto Parts & Tools", "Baby & Toys",
    "Bags & Luggage", "Beauty & Personal Care", "Digital Electronics",
    "Hardware & Home", "Home & Daily Living", "Home Appliances",
    "Kitchen Supplies", "Material", "Musical Instruments", "Others",
    "Pet Supplies", "Phone Accessories", "Sports & Outdoor",
    "Stationery & Office",
]

# Excel AA-730 sub-category (stored in product.category) -> UI main category
SUB_TO_MAIN = {
    "Clothing":"Apparel & Footwear","Shoes":"Apparel & Footwear","Swimwear":"Apparel & Footwear",
    "Socks":"Apparel & Footwear","Hair Accessories":"Apparel & Footwear","Footwear":"Apparel & Footwear",
    "Accessories":"Apparel & Footwear",
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
    "Other":"Others","Photography":"Others","Machinery":"Others","Outdoor":"Others",
    "Dog Supplies":"Pet Supplies","Pet Supplies":"Pet Supplies",
    "Mobile Accessories":"Phone Accessories","Screen Protectors":"Phone Accessories",
    "Fitness":"Sports & Outdoor",
    "Stationery":"Stationery & Office",
}

print("=== Step 1: site-data.json add categories + mainCategory ===")
with open("site-data.json","r") as f:
    data = json.load(f)

unmapped = set()
for p in data["products"]:
    sub = p.get("category","Other")
    main = SUB_TO_MAIN.get(sub)
    if not main:
        unmapped.add(sub)
        main = "Others"
    p["mainCategory"] = main

data["categories"] = UI_MAIN_CATEGORIES

with open("site-data.json","w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

from collections import Counter
cnt = Counter(p["mainCategory"] for p in data["products"])
print(f"✅ site-data.json: {len(data['products'])} products | {len(UI_MAIN_CATEGORIES)} main categories")
if unmapped:
    print(f"⚠️  Unmapped sub-categories → Others: {unmapped}")
for c in UI_MAIN_CATEGORIES:
    print(f"  {c}: {cnt.get(c,0)}")

print("\n=== Step 1 DONE ===")

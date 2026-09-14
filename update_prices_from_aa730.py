#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Recalculate product prices from the AA-730 price summary table.

Pricing rules:
  1. Base CNY price = price from AA-730 价格汇总 sheet (with 价格变动汇总 corrections)
  2. 15% wholesale markup is applied by the existing conversion formula:
        USD = (CNY / 6.7) * 1.15
     So priceMin/priceMax in site-data.json store the RAW CNY value.
  3. Category/keyword price floors act as a minimum safety net to catch
     obviously unreasonable prices (e.g. curling iron at 0.22 CNY).

Usage: python3 update_prices_from_aa730.py
"""
import json
import os
import re
import sys

import openpyxl

ROOT = os.path.dirname(os.path.abspath(__file__))
WORKSPACE = os.path.dirname(ROOT)
AA730 = os.path.join(WORKSPACE, "AA-730价格汇总表.xlsx")
DATA = os.path.join(ROOT, "site-data.json")

# Conservative price floors — only catch obviously wrong prices.
# Most AA-730 prices are used directly; floors only apply when the
# AA-730 price is impossibly low for the product type.
CONSERVATIVE_FLOORS = [
    # Appliances / tools clearly mispriced (likely decimal-point errors)
    (r"curling\s*iron|hair\s*curler|hair\s*straightener|flat\s*iron", 25.0),
    (r"hair\s*dryer|blow\s*dryer", 30.0),
    (r"hair\s*clipper|trimmer|shaver", 15.0),
    (r"waffle\s*maker|waffle\s*iron", 40.0),
    (r"blender|juicer|food\s*processor", 35.0),
    (r"kettle|electric\s*kettle", 25.0),
    (r"rice\s*cooker", 45.0),
    (r"air\s*fryer", 80.0),
    (r"coffee\s*maker|coffee\s*machine", 50.0),
    (r"toaster|sandwich\s*maker", 30.0),
    (r"microwave|oven", 150.0),
    (r"yoga.*mat|mat.*yoga", 12.0),
    (r"steering\s*wheel\s*cover", 12.0),
    (r"car\s*seat\s*cover", 18.0),
    (r"smart\s*watch|fitness\s*tracker", 30.0),
    (r"bluetooth\s*speaker", 15.0),
    (r"wireless\s*earbud|earphone|headphone", 12.0),
    (r"backpack", 12.0),
    (r"handbag|tote\s*bag|shoulder\s*bag", 15.0),
    (r"laptop\s*bag", 18.0),
    (r"sneaker|sports\s*shoe|running\s*shoe", 20.0),
    (r"leather\s*shoe|dress\s*shoe", 25.0),
    (r"jacket|coat|hoodie|sweater", 18.0),
    (r"desk\s*lamp|table\s*lamp|floor\s*lamp", 18.0),
    (r"ceiling\s*light|pendant\s*light|chandelier", 25.0),
    (r"electric\s*fireplace", 150.0),
    (r"drill|screwdriver\s*set|tool\s*set", 25.0),
    (r"stroller|pram", 80.0),
    (r"baby\s*car\s*seat", 50.0),
    (r"dog\s*bed|pet\s*bed", 15.0),
    (r"dog\s*crate|pet\s*cage", 25.0),
    (r"tumbler|water\s*bottle", 5.0),
    (r"rc\s*car|remote\s*control", 20.0),
    (r"drone", 100.0),
]
DEFAULT_FLOOR = 0.3  # only catch obvious typos (< 0.3 CNY for non-trivial items)


def compute_floor(name, category):
    """Return a conservative price floor (CNY). Most products return 0.3."""
    floor = DEFAULT_FLOOR
    name_l = name.lower()
    for pattern, kw_floor in CONSERVATIVE_FLOORS:
        if re.search(pattern, name_l):
            if kw_floor > floor:
                floor = kw_floor
    return floor


def load_aa730_prices():
    """Return dict: child_sku (str) -> {'price': float, 'color': str, 'size': str, 'parent': str}."""
    wb = openpyxl.load_workbook(AA730, data_only=True)
    ws = wb["价格汇总"]
    prices = {}
    for row in ws.iter_rows(min_row=2, values_only=True):
        child = row[0]
        parent = row[1]
        price = row[4]
        color = row[5]
        size = row[6]
        if not child or price is None:
            continue
        try:
            p = float(price)
        except (TypeError, ValueError):
            continue
        prices[str(child).strip()] = {
            "price": p,
            "color": str(color) if color else "",
            "size": str(size) if size else "",
            "parent": str(parent).strip() if parent else "",
        }

    # Apply corrections from 价格变动汇总
    ws2 = wb["价格变动汇总"]
    corrected = 0
    for row in ws2.iter_rows(min_row=2, values_only=True):
        sku = row[0]
        actual = row[3]  # 实际单价
        if not sku or actual is None:
            continue
        try:
            p = float(actual)
        except (TypeError, ValueError):
            continue
        sku = str(sku).strip()
        if sku in prices:
            prices[sku]["price"] = p
            corrected += 1
        else:
            # Add as new entry (might be a child SKU not in main sheet)
            prices[sku] = {"price": p, "color": "", "size": "", "parent": ""}
            corrected += 1
    print(f"Loaded {len(prices)} SKU prices from AA-730 ({corrected} corrections applied)")
    return prices


def main():
    aa730 = load_aa730_prices()

    with open(DATA, "r", encoding="utf-8") as f:
        data = json.load(f)

    updated_products = 0
    updated_variations = 0
    floor_applied = 0
    not_found = []

    for p in data["products"]:
        sku = p.get("sku", "")
        name = p.get("name", "")
        cat = p.get("category", "")
        variations = p.get("variations") or []

        # Try to match each variation's child_id to AA-730
        product_prices = []
        for v in variations:
            child_id = v.get("child_id", "")
            matched = None
            if child_id and child_id in aa730:
                matched = aa730[child_id]
            elif sku and sku in aa730:
                matched = aa730[sku]
            if matched:
                cny = matched["price"]
                # Apply floor as minimum safety net
                floor = compute_floor(name, cat)
                if cny < floor:
                    cny = floor
                    floor_applied += 1
                v["price"] = round(cny, 2)
                product_prices.append(cny)
                updated_variations += 1

        if product_prices:
            p["priceMin"] = round(min(product_prices), 2)
            p["priceMax"] = round(max(product_prices), 2)
            updated_products += 1
        else:
            # Product not found in AA-730 — keep existing price but still
            # ensure it meets the floor for reasonableness
            pm = p.get("priceMin")
            if pm is not None and pm != "":
                try:
                    cny = float(pm)
                    floor = compute_floor(name, cat)
                    if cny < floor:
                        p["priceMin"] = round(floor, 2)
                        p["priceMax"] = round(max(float(p.get("priceMax", floor)), floor), 2)
                        floor_applied += 1
                except (TypeError, ValueError):
                    pass
            not_found.append(sku)

    with open(DATA, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Updated {updated_products} products, {updated_variations} variations")
    print(f"Floor applied to {floor_applied} prices (below reasonable minimum)")
    if not_found:
        print(f"Products not in AA-730 (kept existing price): {len(not_found)}")
        for s in not_found[:10]:
            print(f"  {s}")


if __name__ == "__main__":
    main()

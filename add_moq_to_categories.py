#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add MOQ info to every product card on category-*.html pages.
Inserts a MOQ line between the title and the price.
"""

import json
import os
import re
import glob

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(ROOT, "site-data.json")

CNY_TO_USD_RATE = 6.7
PRICE_MARKUP = 1.15

# Build SKU -> MOQ lookup
with open(DATA_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

sku_moq = {}
for p in data["products"]:
    sku_moq[p["sku"]] = p.get("moq", 0)

# Match a card's SKU line and price line to insert MOQ between them.
# Pattern: <p class="small text-muted mb-1">SKU</p> ... <h3 ...>title</h3> ... <p class="mt-auto mb-0 fw-bold text-indigo">PRICE</p>
# We'll operate per-article: find the SKU, find the price, inject MOQ before price.

price_re = re.compile(
    r'(<p class="mt-auto mb-0 fw-bold text-indigo">)([^<]+)(</p>)'
)

sku_re = re.compile(
    r'<p class="small text-muted mb-1">([A-Z0-9-]+)</p>'
)

def process_file(fpath):
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    # Split into articles to associate SKU with price within same card
    # We'll process by finding each SKU and the next price after it.
    articles = re.split(r'(<article class="col-md-4 col-lg-3">)', content)
    out = [articles[0]]
    for i in range(1, len(articles), 2):
        tag = articles[i]
        art = articles[i + 1] if i + 1 < len(articles) else ""
        sku_m = sku_re.search(art)
        if sku_m:
            sku = sku_m.group(1)
            moq = sku_moq.get(sku, 0)
            moq_str = str(moq) if moq and moq > 0 else "Contact"
            # Insert MOQ before the price line, move mt-auto to a wrapper
            def price_repl(m, moq_str=moq_str):
                return (
                    f'<div class="mt-auto d-flex flex-column gap-1">'
                    f'<p class="small text-muted mb-0"><i class="fas fa-box me-1"></i>MOQ: {moq_str}</p>'
                    f'<p class="mb-0 fw-bold text-indigo">{m.group(2)}</p>'
                    f'</div>'
                )
            art = price_re.sub(price_repl, art, count=1)
        out.append(tag + art)

    new_content = "".join(out)
    if new_content != content:
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(new_content)
        return True
    return False

files = glob.glob(os.path.join(ROOT, "category-*.html"))
changed = 0
for fpath in files:
    if process_file(fpath):
        changed += 1

print(f"Processed {len(files)} category files, updated MOQ in {changed} files.")

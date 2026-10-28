#!/usr/bin/env python3
"""Add isRelatedTo to each product page's Product JSON-LD, pointing to the
related products already listed in the page's visible "Related Products" section.
This strengthens the product entity graph for AI crawlers.
"""
import re, json, glob, os

SITE = "https://www.yeatru.com"


def extract_related(h):
    """Extract (url, name) pairs from related-product-card anchors."""
    results = []
    for m in re.finditer(
        r'class="related-product-card"\s+href="(product-[^"]+\.html)"[^>]*>\s*'
        r'<img[^>]*alt="([^"]*)"',
        h,
    ):
        href, name = m.group(1), m.group(2).strip()
        results.append({"url": f"{SITE}/{href}", "name": name})
    return results


def product_jsonld_match(h):
    for m in re.finditer(
        r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>', h, re.S
    ):
        try:
            d = json.loads(m.group(1))
        except json.JSONDecodeError:
            continue
        if d.get("@type") == "Product":
            return m, d
    return None, None


def process(fpath):
    h = open(fpath, encoding="utf-8").read()
    sku = os.path.basename(fpath).replace("product-", "").replace(".html", "")

    # Already has isRelatedTo? skip (idempotent)
    if '"isRelatedTo"' in h:
        return f"SKIP {fpath}"

    related = extract_related(h)
    if not related:
        return f"WARN {fpath}: no related products found"

    m, d = product_jsonld_match(h)
    if not d:
        return f"ERROR {fpath}: no Product JSON-LD"

    d["isRelatedTo"] = [
        {"@type": "Product", "name": r["name"], "url": r["url"]} for r in related
    ]

    new_json = json.dumps(d, ensure_ascii=False)
    h = h[: m.start(1)] + new_json + h[m.end(1) :]
    open(fpath, "w", encoding="utf-8").write(h)
    return f"OK {sku}: {len(related)} related"


if __name__ == "__main__":
    files = sorted(glob.glob("product-YCS-*.html"))
    ok = skip = warn = err = 0
    for f in files:
        r = process(f)
        if r.startswith("OK"):
            ok += 1
        elif r.startswith("SKIP"):
            skip += 1
        elif r.startswith("WARN"):
            warn += 1
        else:
            err += 1
    print(f"Done: OK={ok} SKIP={skip} WARN={warn} ERR={err} (total={len(files)})")

#!/usr/bin/env python3
"""Generate category pages from product data."""
import json, os, re

DATA = "/workspace/data/products.json"
MD_OUT = "/workspace/content/pages"
SRC = "/workspace"

def main():
    products = json.load(open(DATA, encoding="utf-8"))
    cats = {}
    for p in products:
        cat = p.get("category", "")
        if cat:
            if cat not in cats:
                cats[cat] = []
            cats[cat].append(p["sku"])

    # Also read existing category HTML for descriptions
    cat_descs = {}
    for fname in os.listdir(SRC):
        if fname.startswith("category-") and fname.endswith(".html"):
            cat_slug = fname.replace("category-", "").replace(".html", "")
            html = open(os.path.join(SRC, fname), encoding="utf-8", errors="ignore").read()
            m = re.search(r'<meta[^>]+name="description"[^>]+content="([^"]*)"', html)
            if m:
                cat_descs[cat_slug] = m.group(1)

    print(f"Found {len(cats)} categories")
    for cat, skus in sorted(cats.items()):
        slug = cat.lower().replace(" ", "-").replace("&", "and").replace("/", "-")
        slug = re.sub(r'[^a-z0-9-]', '', slug)
        desc = cat_descs.get(slug, f"Source {cat} from verified Chinese factories. Small MOQ, AQL 2.5 QC, DDP shipping to 50+ countries.")

        lines = ["---"]
        lines.append(f'title: "{cat}"')
        lines.append(f'url: "/category-{slug}.html"')
        lines.append(f'type: page')
        lines.append(f'layout: category')
        lines.append(f'categoryName: "{cat}"')
        lines.append(f'description: "{desc[:200].replace(chr(34), chr(39))}"')
        lines.append(f'date: 2026-09-14')
        lines.append("---")
        lines.append("")
        lines.append(f"Browse {len(skus)} {cat} products sourced from verified Chinese factories.")
        lines.append("")
        lines.append("All products include AQL 2.5 quality inspection, OEM/private label support, and DDP shipping to 50+ countries.")

        md_path = os.path.join(MD_OUT, f"category-{slug}.md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

    print(f"Generated {len(cats)} category pages")

if __name__ == "__main__":
    main()

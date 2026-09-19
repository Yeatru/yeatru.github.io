#!/usr/bin/env python3
"""verify_local_images.py

Local verification (no network) that the 19 NEW blog image dedup is complete.

Checks:
  1. For every blog-*.html: extract its own og:image -> resolve to a local file
     -> md5 the content -> group blogs by md5 -> report cross-article duplicates.
  2. Confirm none of the 19 NEW blogs shares its image md5 with any other blog.
  3. Confirm each of the 19 NEW blog HTML files has og:image, twitter:image and
     hero <img> all pointing to its own /Images/blog/blog-{slug}.jpg.
  4. Confirm every image referenced (og:image) across all blogs exists on disk
     (no broken primary image paths).
  5. Confirm blog.html cards + all related-article-cards linking to the 19 NEW
     blogs now point to those blogs' new images.
"""
import os
import re
import glob
import hashlib

ROOT = "/workspace"
IMG_DIR = os.path.join(ROOT, "Images", "blog")
ABS_BASE = "https://www.yeatru.com"

NEW_BLOGS = [
    "blog-verify-chinese-supplier-license",
    "blog-what-is-a-sourcing-agent-2026",
    "blog-agent-vs-trading-company",
    "blog-alibaba-vs-sourcing-agent",
    "blog-custom-product-manufacturing-china",
    "blog-sourcing-agent-vs-direct-factory",
    "blog-china-sourcing-agent-europe",
    "blog-low-moq-sourcing-china",
    "blog-yiwu-market-guide-2026",
    "blog-yiwu-agent-for-foreigners",
    "blog-sourcing-preparation-checklist",
    "blog-import-from-china-step-by-step",
    "blog-yiwu-sourcing-agent-uk",
    "blog-sourcing-agent-vs-buying-office",
    "blog-air-freight-china",
    "blog-fba-product-research-china",
    "blog-amazon-restricted-products-china",
    "blog-tiktok-shop-compliance-2026",
    "blog-first-time-china-sourcing",
]
NEW_SET = set(NEW_BLOGS)


def read(p):
    with open(p, "r", encoding="utf-8") as f:
        return f.read()


def md5_file(path):
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def resolve_local(url):
    """Map an image URL/path to a local absolute file path under /workspace."""
    if url.startswith(ABS_BASE):
        rel = url[len(ABS_BASE):]
    elif url.startswith("https://") or url.startswith("http://"):
        return None  # external image, skip
    else:
        rel = url
    if rel.startswith("/"):
        rel = rel[1:]
    return os.path.join(ROOT, rel)


def og_image(html):
    m = re.search(r'<meta\s+property="og:image"\s+content="([^"]+)"', html)
    return m.group(1) if m else None


# --------------------------------------------------------------------------- #
print("=" * 70)
print("CHECK 1+2: cross-article duplicate og:image groups (local md5)")
print("=" * 70)
blog_files = sorted(glob.glob(os.path.join(ROOT, "blog-*.html")))
groups = {}            # md5 -> list of (slug, og_image_url, local_file)
broken_og = []         # blogs whose og:image file is missing on disk
per_blog_md5 = {}      # slug -> md5
for bf in blog_files:
    slug = os.path.basename(bf)[:-5]  # strip .html
    html = read(bf)
    og = og_image(html)
    if not og:
        continue
    local = resolve_local(og)
    if not local or not os.path.exists(local):
        broken_og.append((slug, og, local))
        continue
    h = md5_file(local)
    per_blog_md5[slug] = h
    groups.setdefault(h, []).append((slug, og, local))

dup_groups = {h: v for h, v in groups.items() if len(v) > 1}
print(f"  Blogs scanned: {len(blog_files)}")
print(f"  Distinct og:image md5 groups: {len(groups)}")
print(f"  Cross-article duplicate groups (size>1): {len(dup_groups)}")
new_in_dup = []
for h, members in sorted(dup_groups.items(), key=lambda kv: -len(kv[1])):
    slugs = [m[0] for m in members]
    new_here = [s for s in slugs if s in NEW_SET]
    flag = "  <-- involves NEW blog" if new_here else ""
    print(f"  md5 {h[:12]}  size={len(members)}  blogs={slugs}{flag}")
    if new_here:
        new_in_dup.extend(new_here)

if new_in_dup:
    print(f"\n  !! {len(set(new_in_dup))} NEW blogs STILL in a duplicate group: {sorted(set(new_in_dup))}")
else:
    print("\n  OK: none of the 19 NEW blogs shares its og:image md5 with any other blog.")

# --------------------------------------------------------------------------- #
print()
print("=" * 70)
print("CHECK 3: each NEW blog HTML points og/twitter/hero to its own image")
print("=" * 70)
problems = []
for slug in NEW_BLOGS:
    bf = os.path.join(ROOT, slug + ".html")
    if not os.path.exists(bf):
        problems.append(f"{slug}: HTML missing")
        continue
    html = read(bf)
    want_abs = ABS_BASE + "/Images/blog/" + slug + ".jpg"
    want_rel = "/Images/blog/" + slug + ".jpg"
    # og:image
    og = og_image(html)
    if og != want_abs:
        problems.append(f"{slug}: og:image={og} (want {want_abs})")
    # twitter:image
    m = re.search(r'<meta\s+name="twitter:image"\s+content="([^"]+)"', html)
    tw = m.group(1) if m else None
    if tw != want_abs:
        problems.append(f"{slug}: twitter:image={tw} (want {want_abs})")
    # hero img: first <img ... class="...img-fluid..."> OR any img with src
    # containing the slug. Check the article-body hero specifically.
    # Look for an <img> whose src references this blog's new image.
    img_srcs = re.findall(r'<img\b[^>]*\bsrc="([^"]+)"', html)
    hero_ok = any(s == want_rel or s == want_abs for s in img_srcs)
    if not hero_ok:
        problems.append(f"{slug}: no hero <img> src points to {want_rel} (found {img_srcs[:3]})")
    # also ensure no leftover reference to a clearly-different OLD shared image
    # is fine -- the hero check above covers the main one.
if problems:
    print("  PROBLEMS:")
    for p in problems:
        print("   -", p)
else:
    print("  OK: all 19 NEW blogs have og:image, twitter:image and a hero <img>")
    print("      pointing to /Images/blog/blog-{slug}.jpg")

# --------------------------------------------------------------------------- #
print()
print("=" * 70)
print("CHECK 4: every og:image referenced by any blog exists on disk")
print("=" * 70)
if broken_og:
    print(f"  BROKEN og:image references ({len(broken_og)}):")
    for slug, og, local in broken_og:
        print(f"   - {slug}: {og} -> {local}")
else:
    print("  OK: every blog's og:image resolves to an existing local file.")

# --------------------------------------------------------------------------- #
print()
print("=" * 70)
print("CHECK 5: blog.html + related-cards linking to NEW blogs use new image")
print("=" * 70)
# blog.html cards
bh = os.path.join(ROOT, "blog.html")
if os.path.exists(bh):
    html = read(bh)
    card_issues = []
    for slug in NEW_BLOGS:
        want_rel = "/Images/blog/" + slug + ".jpg"
        # find all <a href="slug.html" ...> ... <img src="...">
        pat = (r'<a\b[^>]*\bhref="' + re.escape(slug) + r'\.html"[^>]*>'
               r'[\s\S]*?<img\b[^>]*?src="([^"]*)"')
        srcs = re.findall(pat, html)
        if not srcs:
            card_issues.append(f"{slug}: no blog.html card found")
        else:
            bad = [s for s in srcs if s != want_rel]
            if bad:
                card_issues.append(f"{slug}: blog.html card src(s) {bad} (want {want_rel})")
    if card_issues:
        print("  blog.html card issues:")
        for c in card_issues:
            print("   -", c)
    else:
        print("  OK: all blog.html cards for the 19 NEW blogs point to new images.")

# related-article-cards across all blog files
rel_issues = []
for bf in blog_files + ([bh] if os.path.exists(bh) else []):
    slug_host = os.path.basename(bf)[:-5]
    html = read(bf)
    for slug in NEW_BLOGS:
        want_rel = "/Images/blog/" + slug + ".jpg"
        pat = (r'<a\b[^>]*\bhref="' + re.escape(slug) + r'\.html"[^>]*'
               r'class="[^"]*\brelated-article-card\b[^"]*"[^>]*>'
               r'[\s\S]*?<img\b[^>]*?src="([^"]*)"')
        srcs = re.findall(pat, html)
        bad = [s for s in srcs if s != want_rel]
        if bad:
            rel_issues.append(f"{slug_host}: related-card -> {slug} src(s) {bad}")
if rel_issues:
    print(f"  related-article-card issues ({len(rel_issues)}):")
    for c in rel_issues[:20]:
        print("   -", c)
else:
    print("  OK: all related-article-cards linking to the 19 NEW blogs point to new images.")

print()
print("=" * 70)
print("DONE")
print("=" * 70)

#!/usr/bin/env python3
"""fix_image_refs.py

Update HTML image references for the 19 NEW blog posts so they point to the
newly generated unique AI images.

  Step A: each NEW blog's own HTML file -> replace its OLD image (detected from
          og:image) everywhere (og:image, twitter:image, JSON-LD image fields,
          hero <img>, self-referencing related-article card).
  Step B: blog.html index -> for every card linking to one of the 19 NEW blogs,
          set the card <img> src to the new image.
  Step C: all blog HTML files -> for every related-article-card linking to one
          of the 19 NEW blogs, set the card <img> src to the new image.

Only the 19 NEW blogs' images are touched. OLD blogs' own images (og:image /
hero) are never modified.
"""
import os
import re
import glob

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

stats = {
    "A_files_changed": 0,
    "A_string_replacements": 0,
    "A_meta_forced": 0,        # og/twitter:image explicitly set (safety net)
    "B_changes": 0,            # img srcs rewritten in blog.html
    "C_files_changed": 0,
    "C_card_changes": 0,      # related-article-card img srcs rewritten
    "skipped_missing_image": [],
    "skipped_missing_html": [],
}


def read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def new_paths(slug):
    """Return (absolute_url, relative_path) for the new image of a slug."""
    rel = "/Images/blog/" + slug + ".jpg"
    return ABS_BASE + rel, rel


def esc(slug):
    return re.escape(slug)


# --------------------------------------------------------------------------- #
# Step A: each NEW blog's own HTML file
# --------------------------------------------------------------------------- #
print("=" * 70)
print("STEP A: update each NEW blog's own HTML image references")
print("=" * 70)
for slug in NEW_BLOGS:
    html_path = os.path.join(ROOT, slug + ".html")
    local_img = os.path.join(IMG_DIR, slug + ".jpg")
    new_abs, new_rel = new_paths(slug)

    if not os.path.exists(local_img):
        print(f"  [A] SKIP {slug}: new image file missing on disk")
        stats["skipped_missing_image"].append(slug)
        continue
    if not os.path.exists(html_path):
        print(f"  [A] SKIP {slug}: HTML file missing")
        stats["skipped_missing_html"].append(slug)
        continue

    html = read(html_path)
    before = html

    # Detect the blog's OWN old image from its og:image meta tag.
    m = re.search(r'<meta\s+property="og:image"\s+content="([^"]+)"', html)
    if m:
        old_abs = m.group(1)
        # Derive the relative form too (hero img / related cards use relative).
        if old_abs.startswith(ABS_BASE):
            old_rel = old_abs[len(ABS_BASE):]
        elif old_abs.startswith("/"):
            old_rel = old_abs
            old_abs = ABS_BASE + old_abs
        else:
            old_rel = None

        # Replace absolute occurrences everywhere (og:image, twitter:image,
        # JSON-LD Article/BlogPosting image URLs).
        if old_abs and old_abs != new_abs:
            n = html.count(old_abs)
            if n:
                html = html.replace(old_abs, new_abs)
                stats["A_string_replacements"] += n
                print(f"  [A] {slug}: replaced abs old {old_abs} (x{n})")
        # Replace relative occurrences (hero <img>, self-referencing related card).
        if old_rel and old_rel != new_rel:
            n = html.count(old_rel)
            if n:
                html = html.replace(old_rel, new_rel)
                stats["A_string_replacements"] += n
                print(f"  [A] {slug}: replaced rel old {old_rel} (x{n})")

    # Safety nets: explicitly force og:image & twitter:image to the new URL
    # (no-op if the global replace already did it).
    html, n1 = re.subn(
        r'(<meta\s+property="og:image"\s+content=")[^"]*(")',
        lambda mm: mm.group(1) + new_abs + mm.group(2),
        html,
    )
    html, n2 = re.subn(
        r'(<meta\s+name="twitter:image"\s+content=")[^"]*(")',
        lambda mm: mm.group(1) + new_abs + mm.group(2),
        html,
    )
    if n1 or n2:
        stats["A_meta_forced"] += n1 + n2

    if html != before:
        write(html_path, html)
        stats["A_files_changed"] += 1
    else:
        print(f"  [A] {slug}: no changes (already pointing to new image?)")


# --------------------------------------------------------------------------- #
# Step B: blog.html index cards
# --------------------------------------------------------------------------- #
print()
print("=" * 70)
print("STEP B: update blog.html index cards for the 19 NEW blogs")
print("=" * 70)
blog_index = os.path.join(ROOT, "blog.html")
if os.path.exists(blog_index):
    html = read(blog_index)
    before = html
    for slug in NEW_BLOGS:
        new_abs, new_rel = new_paths(slug)
        # Match an <a> opening with href="{slug}.html" up to the first
        # <img ...> tag's src attribute, and rewrite that src. (slug already
        # starts with "blog-", so do NOT prepend another "blog-".)
        pattern = (
            r'(<a\b[^>]*\bhref="' + esc(slug) + r'\.html"[^>]*>'
            r'[\s\S]*?<img\b[^>]*?)src="[^"]*"'
        )
        html, n = re.subn(
            pattern,
            lambda mm, nr=new_rel: mm.group(1) + 'src="' + nr + '"',
            html,
        )
        if n:
            stats["B_changes"] += n
            print(f"  [B] {slug}: rewrote {n} blog.html card image(s) -> {new_rel}")
    if html != before:
        write(blog_index, html)
        print(f"  [B] blog.html updated (total {stats['B_changes']} card img srcs)")
    else:
        print("  [B] blog.html: no card changes needed")
else:
    print("  [B] blog.html not found")


# --------------------------------------------------------------------------- #
# Step C: related-article-card references across all blog HTML files
# --------------------------------------------------------------------------- #
print()
print("=" * 70)
print("STEP C: update related-article-card images across all blog HTML files")
print("=" * 70)
# All blog HTML files + the index.
files = sorted(glob.glob(os.path.join(ROOT, "blog-*.html")))
if os.path.exists(blog_index) and blog_index not in files:
    files.append(blog_index)

for fpath in files:
    try:
        html = read(fpath)
    except Exception as e:
        print(f"  [C] SKIP {os.path.basename(fpath)}: read error {e}")
        continue
    before = html
    changed_here = 0
    for slug in NEW_BLOGS:
        new_abs, new_rel = new_paths(slug)
        # Anchor must have href="{slug}.html" AND class containing
        # "related-article-card"; then rewrite the first <img> src inside it.
        # (slug already starts with "blog-", so do NOT prepend "blog-".)
        pattern = (
            r'(<a\b[^>]*\bhref="' + esc(slug) + r'\.html"[^>]*'
            r'class="[^"]*\brelated-article-card\b[^"]*"[^>]*>'
            r'[\s\S]*?<img\b[^>]*?)src="[^"]*"'
        )
        html, n = re.subn(
            pattern,
            lambda mm, nr=new_rel: mm.group(1) + 'src="' + nr + '"',
            html,
        )
        if n:
            changed_here += n
            stats["C_card_changes"] += n
    if html != before:
        write(fpath, html)
        stats["C_files_changed"] += 1
        print(f"  [C] {os.path.basename(fpath)}: rewrote {changed_here} related-card img(s)")

# --------------------------------------------------------------------------- #
print()
print("=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"  Step A: {stats['A_files_changed']} NEW blog HTML files changed")
print(f"          {stats['A_string_replacements']} string replacements (old->new path)")
print(f"          {stats['A_meta_forced']} og/twitter:image meta values forced")
print(f"  Step B: {stats['B_changes']} blog.html card image srcs rewritten")
print(f"  Step C: {stats['C_files_changed']} files with related-card changes")
print(f"          {stats['C_card_changes']} related-article-card img srcs rewritten")
if stats["skipped_missing_image"]:
    print(f"  SKIPPED (missing image): {stats['skipped_missing_image']}")
if stats["skipped_missing_html"]:
    print(f"  SKIPPED (missing html): {stats['skipped_missing_html']}")

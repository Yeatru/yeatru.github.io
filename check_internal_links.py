#!/usr/bin/env python3
"""Check for broken internal links in blog HTML files (href to non-existent blog-*.html)."""
import os
import re
import glob

WORKSPACE = "/workspace"

# 1. Build set of all existing blog HTML files
all_files = set()
for f in glob.glob(os.path.join(WORKSPACE, "blog-*.html")):
    all_files.add(os.path.basename(f))
print(f"Existing blog HTML files: {len(all_files)}")

# 2. Scan all HTML files for href="blog-*.html" and check existence
broken = []
all_html = glob.glob(os.path.join(WORKSPACE, "*.html"))
for html_file in all_html:
    try:
        with open(html_file, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
    except Exception:
        continue
    # Find all href="blog-*.html" (with optional #anchor or ?query)
    for m in re.finditer(r'href="(blog-[^"#?]+\.html)', content):
        target = m.group(1)
        if target not in all_files:
            broken.append((os.path.basename(html_file), target))

# Deduplicate
broken_unique = sorted(set(broken))
print(f"\n=== BROKEN INTERNAL LINKS (href to non-existent blog-*.html) ===")
print(f"Count: {len(broken_unique)}")
for src, tgt in broken_unique[:50]:
    print(f"  {src} -> {tgt}")
if len(broken_unique) > 50:
    print(f"  ... and {len(broken_unique)-50} more")

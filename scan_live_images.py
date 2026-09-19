#!/usr/bin/env python3
"""Scan live yeatru.com blog.html for broken or duplicate card images."""
import re
import hashlib
import urllib.request
import urllib.error
from html.parser import HTMLParser

BLOG_HTML = "https://www.yeatru.com/blog.html"
UA = "Mozilla/5.0 (compatible; ImageScanner/1.0)"


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


# 1. Fetch blog.html
html = fetch(BLOG_HTML).decode("utf-8", errors="replace")
print(f"blog.html size: {len(html)} bytes")

# 2. Extract all blog cards: href + img src + title
# Pattern: <a href="blog-...html" class="blog-card">...<img src="..." ... alt="...">
card_re = re.compile(
    r'<a\s+href="(blog-[^"#]+\.html)"[^>]*class="blog-card"[^>]*>'
    r'.*?<img[^>]+src="([^"]+)"[^>]*alt="([^"]*)"[^>]*>',
    re.DOTALL,
)

cards = []
seen_urls = set()
for m in card_re.finditer(html):
    blog = m.group(1)
    img = m.group(2)
    alt = m.group(3)
    if blog in seen_urls:
        continue
    seen_urls.add(blog)
    cards.append((blog, img, alt))

print(f"Unique blog cards on blog.html: {len(cards)}")

# 3. For each card image, fetch HEAD then GET to check actual content
results = []
for blog, img, alt in cards:
    if img.startswith("/"):
        full_url = "https://www.yeatru.com" + img
    elif img.startswith("http"):
        full_url = img
    else:
        full_url = "https://www.yeatru.com/" + img

    try:
        req = urllib.request.Request(full_url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read()
        size = len(data)
        # Hash the content
        md5 = hashlib.md5(data).hexdigest() if size > 0 else "EMPTY"
        # Check JPEG/PNG magic
        is_jpeg = data[:3] == b"\xff\xd8\xff" if size >= 3 else False
        is_png = data[:8] == b"\x89PNG\r\n\x1a\n" if size >= 8 else False
        is_webp = data[:4] == b"RIFF" and data[8:12] == b"WEBP" if size >= 12 else False
        ok = is_jpeg or is_png or is_webp
    except urllib.error.HTTPError as e:
        size = -1
        md5 = f"HTTP{e.code}"
        ok = False
    except Exception as e:
        size = -2
        md5 = f"ERR:{type(e).__name__}"
        ok = False
    results.append({
        "blog": blog,
        "img_path": img,
        "img_url": full_url,
        "alt": alt[:60],
        "size": size,
        "md5": md5,
        "ok": ok,
    })

# 4. Print broken images
print("\n=== BROKEN / EMPTY IMAGES (size <= 0 or non-image content) ===")
broken = [r for r in results if not r["ok"]]
print(f"Count: {len(broken)}")
for r in broken:
    print(f"  {r['blog']:50s} | {r['img_path']:60s} | size={r['size']:>7} | md5={r['md5']}")

# 5. Print duplicate images (same md5 across DIFFERENT blogs)
print("\n=== CROSS-ARTICLE DUPLICATE IMAGES (same content) ===")
by_md5 = {}
for r in results:
    if r["ok"]:
        by_md5.setdefault(r["md5"], []).append(r)
dups = {k: v for k, v in by_md5.items() if len(v) > 1}
print(f"Duplicate groups: {len(dups)}")
for md5, items in dups.items():
    if len({i["blog"] for i in items}) > 1:  # different blogs share same img
        print(f"\n  md5={md5}  size={items[0]['size']}")
        for i in items:
            print(f"    {i['blog']:50s} | {i['img_path']:60s} | alt={i['alt']}")

# 6. Also report duplicate image PATHS (different blogs using same image URL path)
print("\n=== CROSS-ARTICLE DUPLICATE IMAGE PATHS (same URL) ===")
by_path = {}
for r in results:
    by_path.setdefault(r["img_path"], []).append(r)
dup_paths = {k: v for k, v in by_path.items() if len({i["blog"] for i in v}) > 1}
print(f"Duplicate path groups: {len(dup_paths)}")
for path, items in dup_paths.items():
    print(f"\n  path={path}")
    for i in items:
        print(f"    {i['blog']:50s} | alt={i['alt']}")

# 7. Save full report
import json
with open("/workspace/scan_results.json", "w") as f:
    json.dump({
        "broken": broken,
        "cross_article_dup_by_content": [
            {"md5": k, "items": v} for k, v in dups.items() if len({i["blog"] for i in v}) > 1
        ],
        "cross_article_dup_by_path": [
            {"path": k, "items": v} for k, v in dup_paths.items()
        ],
    }, f, indent=2, default=str)
print("\nFull report: /workspace/scan_results.json")

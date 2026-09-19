#!/usr/bin/env python3
"""
Fix broken internal links in blog files:
- blog-supplier-verification.html -> blog-verify-chinese-supplier-license.html
- blog-section-301-tariffs-2026.html -> blog-hs-code-lookup-china.html
Also fix card images, titles, and excerpts to match the target blog.
"""
import os, re

WORKSPACE = "/workspace"

# Mapping: broken_link -> (replacement_link, replacement_title, replacement_excerpt)
LINK_MAP = {
    "blog-supplier-verification.html": {
        "replacement": "blog-verify-chinese-supplier-license.html",
        "title": "How to Verify a Chinese Supplier's Business License in 2026",
        "excerpt": "Verify supplier licenses, business scope, and factory authenticity before payment.",
        "category": "Supplier Verification",
    },
    "blog-section-301-tariffs-2026.html": {
        "replacement": "blog-hs-code-lookup-china.html",
        "title": "HS Code Lookup Guide: Find Your China Import Tariff in 5 Minutes",
        "excerpt": "Find your HS code, calculate Section 301 duties, CBP MPF, and total landed cost.",
        "category": "Customs & Tariffs",
    },
}

# Build image map from all blogs' og:image
all_blogs = sorted([f for f in os.listdir(WORKSPACE) 
                    if f.startswith("blog-") and f.endswith(".html") and f != "blog.html"])
final_img = {}
for blog in all_blogs:
    path = os.path.join(WORKSPACE, blog)
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        content = fh.read()
    m = re.search(r'og:image"\s+content="([^"]+)"', content)
    if m:
        img = m.group(1)
        if "yeatru.com" in img:
            img = "/" + img.split("yeatru.com/", 1)[-1]
        final_img[blog] = img

total_fixed = 0
blogs_fixed = 0

for blog in all_blogs:
    path = os.path.join(WORKSPACE, blog)
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        content = fh.read()
    
    original = content
    changes = 0
    
    for broken_link, info in LINK_MAP.items():
        replacement = info["replacement"]
        title = info["title"]
        excerpt = info["excerpt"]
        category = info["category"]
        
        # Get the replacement blog's image
        replacement_img = final_img.get(replacement, "")
        if replacement_img.startswith("https://"):
            replacement_rel = "/" + replacement_img.split("yeatru.com/", 1)[-1]
        else:
            replacement_rel = replacement_img
        
        # 1. Replace href
        old_href = f'href="{broken_link}"'
        new_href = f'href="{replacement}"'
        if old_href in content:
            content = content.replace(old_href, new_href)
            changes += content.count(new_href) - content.count(old_href) if old_href not in content else 1
        
        # 2. Replace the card image if it's in a related card linking to this target
        # Find related-article-card blocks that link to the replacement
        # and fix their image, title, excerpt
        card_pattern = rf'(href="{replacement}"[^>]*class="related-article-card"[^>]*>.*?<img[^>]+src=")([^"]+)(")'
        
        def fix_card_img(match):
            old_img = match.group(2)
            if replacement_rel and old_img != replacement_rel:
                return f'{match.group(1)}{replacement_rel}{match.group(3)}'
            return match.group(0)
        
        content = re.sub(card_pattern, fix_card_img, content, flags=re.DOTALL)
        
        # 3. Fix the card title
        title_pattern = rf'(href="{replacement}"[^>]*class="related-article-card"[^>]*>.*?<h3[^>]*>)[^<]*(</h3>)'
        content = re.sub(title_pattern, rf'\1{title}\2', content, flags=re.DOTALL)
        
        # 4. Fix the card excerpt
        excerpt_pattern = rf'(href="{replacement}"[^>]*class="related-article-card"[^>]*>.*?<p[^>]*class="related-article-excerpt"[^>]*>)[^<]*(</p>)'
        content = re.sub(excerpt_pattern, rf'\1{excerpt}\2', content, flags=re.DOTALL)
        
        # 5. Fix the card category
        cat_pattern = rf'(href="{replacement}"[^>]*class="related-article-card"[^>]*>.*?<span[^>]*class="related-article-category"[^>]*>)[^<]*(</span>)'
        content = re.sub(cat_pattern, rf'\1{category}\2', content, flags=re.DOTALL)
        
        # 6. Also handle simpler card patterns (card-img-top, blog-card-title, blog-card-excerpt)
        # These might use different class names
        simple_title_pattern = rf'(href="{replacement}"[^>]*>.*?<h3[^>]*class="[^"]*card-title[^"]*"[^>]*>)[^<]*(</h3>)'
        content = re.sub(simple_title_pattern, rf'\1{title}\2', content, flags=re.DOTALL)
    
    if content != original:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
        blogs_fixed += 1
        total_fixed += changes
        if changes > 0:
            print(f"  Fixed {changes} broken links in {blog}")

# Also fix blog.html index page
blog_html_path = os.path.join(WORKSPACE, "blog.html")
with open(blog_html_path, "r", encoding="utf-8", errors="replace") as fh:
    content = fh.read()

html_original = content
for broken_link, info in LINK_MAP.items():
    replacement = info["replacement"]
    content = content.replace(f'href="{broken_link}"', f'href="{replacement}"')

if content != html_original:
    with open(blog_html_path, "w", encoding="utf-8") as fh:
        fh.write(content)
    print(f"\n  Fixed broken links in blog.html")

print(f"\n=== Summary ===")
print(f"Fixed broken links in {blogs_fixed} blog files")
print(f"Total link replacements: {total_fixed}")

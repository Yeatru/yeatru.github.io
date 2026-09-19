#!/usr/bin/env python3
"""
Fix blog images Phase 2: Replace AI_GENERATE blogs with their new AI-generated images.
Also rebuild all blog image maps and fix related-card cross-references.
"""
import os, re, csv

WORKSPACE = "/workspace"

# Step 1: Build current image map for ALL blogs (blog_file -> current og:image path)
all_blogs = sorted([f for f in os.listdir(WORKSPACE) if f.startswith("blog-") and f.endswith(".html")])
current_img = {}
for blog in all_blogs:
    path = os.path.join(WORKSPACE, blog)
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        content = fh.read()
    m = re.search(r'og:image"\s+content="([^"]+)"', content)
    if m:
        img = m.group(1)
        if "yeatru.com" in img:
            img = "/" + img.split("yeatru.com/", 1)[-1]
        current_img[blog] = img
    else:
        current_img[blog] = ""

# Step 2: Read final remap CSV
new_img_map = {}
with open(os.path.join(WORKSPACE, "image-remap-final.csv"), "r") as f:
    reader = csv.DictReader(f, delimiter="|")
    for row in reader:
        blog = row["blog_file"]
        new_img = row["new_image"]
        new_img_map[blog] = new_img

# Step 3: Build final image map for all 124 blogs
# Original 34 keep current_img; new 90 get new_img_map
final_img = {}
for blog in all_blogs:
    if blog in new_img_map:
        final_img[blog] = new_img_map[blog]
    else:
        final_img[blog] = current_img.get(blog, "")

# Step 4: Replace images in the 57 AI blogs + rebuild all 90 new blogs' related cards
replaced_count = 0
for blog, new_img in new_img_map.items():
    path = os.path.join(WORKSPACE, blog)
    if not os.path.exists(path):
        print(f"SKIP (not found): {blog}")
        continue
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        content = fh.read()
    
    old_img = current_img.get(blog, "")
    if not old_img:
        print(f"SKIP (no old img): {blog}")
        continue
    
    # Build old image variants to search for
    old_variants = set()
    old_variants.add(old_img)
    if old_img.startswith("/"):
        old_variants.add("https://www.yeatru.com" + old_img)
        old_variants.add("https://yeatru.com" + old_img)
    if "yeatru.com" in old_img:
        rel = "/" + old_img.split("yeatru.com/", 1)[-1]
        old_variants.add(rel)
    
    new_img_rel = new_img
    new_img_full = "https://www.yeatru.com" + new_img_rel
    
    changes = 0
    
    # Replace all old image references with new image
    for old_v in list(old_variants):
        if old_v == new_img_full or old_v == new_img_rel:
            continue
        count = content.count(old_v)
        if count > 0:
            if old_v.startswith("https://"):
                content = content.replace(old_v, new_img_full)
            else:
                content = content.replace(old_v, new_img_rel)
            changes += count
    
    # Now fix related-card cross-references: find cards that link to other blogs
    # and replace self-referencing images with the target blog's correct image
    # Pattern: href="blog-XXX.html" ... <img src="..." 
    related_pattern = r'href="(blog-[^"#]+\.html)"([^>]*)>(.*?)<img[^>]+src="([^"]+)"'
    
    def replace_card_img(match):
        target_blog = match.group(1)
        attrs = match.group(2)
        inner = match.group(3)
        card_img = match.group(4)
        
        if target_blog in final_img and final_img[target_blog]:
            target_img = final_img[target_blog]
            # Normalize to relative path
            if target_img.startswith("https://"):
                target_rel = "/" + target_img.split("yeatru.com/", 1)[-1]
            else:
                target_rel = target_img
            
            # Only replace if card_img is currently our new_img (self-referencing)
            if card_img == new_img_rel or card_img == new_img_full:
                return f'href="{target_blog}"{attrs}>{inner}<img src="{target_rel}"'
        
        return match.group(0)
    
    content = re.sub(related_pattern, replace_card_img, content, flags=re.DOTALL)
    
    if changes > 0:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
        replaced_count += 1
        print(f"OK ({changes} replacements): {blog} -> {new_img}")

print(f"\n=== Summary ===")
print(f"Replaced images in {replaced_count} blogs")
print(f"Total blogs in final_img map: {len(final_img)}")

# Step 5: Also fix the 33 previously-replaced blogs' related cards (they may still self-reference)
# For each blog in new_img_map, re-scan and fix related cards
print("\n=== Fixing related cards in all 90 new blogs ===")
fixed_cards = 0
for blog, new_img in new_img_map.items():
    path = os.path.join(WORKSPACE, blog)
    if not os.path.exists(path):
        continue
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        content = fh.read()
    
    new_img_rel = new_img
    original = content
    
    # Fix related cards
    related_pattern = r'href="(blog-[^"#]+\.html)"([^>]*)>(.*?)<img[^>]+src="([^"]+)"'
    def fix_card(match):
        target_blog = match.group(1)
        attrs = match.group(2)
        inner = match.group(3)
        card_img = match.group(4)
        
        if target_blog in final_img and final_img[target_blog]:
            target_img = final_img[target_blog]
            if target_img.startswith("https://"):
                target_rel = "/" + target_img.split("yeatru.com/", 1)[-1]
            else:
                target_rel = target_img
            
            if card_img == new_img_rel or card_img == "https://www.yeatru.com" + new_img_rel:
                return f'href="{target_blog}"{attrs}>{inner}<img src="{target_rel}"'
        
        return match.group(0)
    
    content = re.sub(related_pattern, fix_card, content, flags=re.DOTALL)
    
    if content != original:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
        fixed_cards += 1

print(f"Fixed related cards in {fixed_cards} blogs")

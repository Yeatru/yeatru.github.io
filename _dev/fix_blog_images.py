#!/usr/bin/env python3
"""
Fix blog images: replace duplicate images with unique ones.
- Original 34 blogs: keep their images untouched
- 90 new blogs: assign unique images (from existing pool or AI-generated)
- Replace og:image, twitter:image, featured image, and related-card images
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
        # Normalize to /Images/... path
        if "yeatru.com" in img:
            img = "/" + img.split("yeatru.com/", 1)[-1]
        current_img[blog] = img
    else:
        current_img[blog] = ""

# Step 2: Read remap CSV for new blog -> new image
new_img_map = {}
ai_generate = []
with open(os.path.join(WORKSPACE, "image-remap.csv"), "r") as f:
    reader = csv.DictReader(f, delimiter="|")
    for row in reader:
        blog = row["blog_file"]
        new_img = row["new_image"]
        if new_img == "AI_GENERATE":
            ai_generate.append(blog)
        else:
            new_img_map[blog] = new_img

# Step 3: Build final image map for all blogs
# Original 34 keep current_img; new blogs get new_img_map or (for AI_GENERATE) keep current for now
final_img = {}
for blog in all_blogs:
    if blog in new_img_map:
        final_img[blog] = new_img_map[blog]
    else:
        final_img[blog] = current_img.get(blog, "")

# Step 4: For each blog in new_img_map (has real image replacement), do the replacement
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
    
    # Normalize old_img for matching (could be full URL or relative)
    old_img_variants = set()
    old_img_variants.add(old_img)
    if old_img.startswith("/"):
        old_img_variants.add("https://www.yeatru.com" + old_img)
        old_img_variants.add("https://yeatru.com" + old_img)
    if "yeatru.com" in old_img:
        rel = "/" + old_img.split("yeatru.com/", 1)[-1]
        old_img_variants.add(rel)
    
    # New image variants (full URL + relative)
    new_img_rel = new_img  # /Images/...
    new_img_full = "https://www.yeatru.com" + new_img_rel
    new_img_variants = [new_img_full, new_img_rel]
    
    changes = 0
    
    # Replace og:image
    for old_v in old_img_variants:
        if old_v in content:
            content = content.replace(old_v, new_img_full)
            changes += 1
            break
    
    # Replace any remaining old image paths (featured img, related cards, twitter:image)
    # These are typically relative paths like /Images/blog/xxx.jpg
    for old_v in old_img_variants:
        if old_v != new_img_full and old_v != new_img_rel:
            count = content.count(old_v)
            if count > 0:
                content = content.replace(old_v, new_img_rel)
                changes += count
    
    # Also handle the case where the blog references ITSELF in related cards
    # (all related cards pointing to the same self-image)
    # Find related article cards and replace their images with the correct target blog's image
    # Pattern: <a href="blog-XXX.html" ...> ... <img src="OLD_IMG" ... alt="...related">
    related_pattern = r'href="(blog-[^"#]+\.html)"[^>]*>.*?<img[^>]+src="([^"]+)"'
    for m in re.finditer(related_pattern, content, re.DOTALL):
        target_blog = m.group(1)
        card_img = m.group(2)
        # If the card image is our new image (self-reference), replace with target blog's image
        if target_blog in final_img and final_img[target_blog]:
            target_img = final_img[target_blog]
            # Normalize target_img to relative path
            if target_img.startswith("https://"):
                target_rel = "/" + target_img.split("yeatru.com/", 1)[-1]
            else:
                target_rel = target_img
            
            # Only replace if card_img is currently our new_img (self-referencing)
            if card_img == new_img_rel or card_img == new_img_full:
                content = content.replace(
                    f'src="{card_img}"',
                    f'src="{target_rel}"',
                    1  # replace first occurrence near this card
                )
    
    if changes > 0:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
        replaced_count += 1
        print(f"OK ({changes} replacements): {blog} -> {new_img}")

print(f"\n=== Summary ===")
print(f"Replaced images in {replaced_count} blogs")
print(f"AI generation needed for {len(ai_generate)} blogs")
for b in ai_generate:
    print(f"  AI: {b}")

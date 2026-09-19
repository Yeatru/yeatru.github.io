#!/usr/bin/env python3
"""
Fix ALL blog files: for each related-article-card, replace the card image
with the correct image of the TARGET blog (from its og:image).
This fixes systematic related-card image mismatches across all 124 blogs.
"""
import os, re

WORKSPACE = "/workspace"

# Step 1: Build final image map for ALL blogs from their og:image
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

print(f"Built image map for {len(final_img)} blogs")

# Step 2: For each blog, fix related-article-card images
# Pattern: <a href="blog-XXX.html" class="related-article-card"> ... <img src="..." ...>
total_fixed = 0
blogs_fixed = 0

for blog in all_blogs:
    path = os.path.join(WORKSPACE, blog)
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        content = fh.read()
    
    original = content
    changes = [0]
    
    # Find all related-article-card blocks and fix their images
    # Pattern captures: href target + the img src inside the card
    card_pattern = r'(href="(blog-[^"#]+\.html)"[^>]*class="related-article-card"[^>]*>.*?<img[^>]+src=")([^"]+)(")'
    
    def fix_card(match):
        prefix = match.group(1)
        target_blog = match.group(2)
        old_img = match.group(3)
        suffix = match.group(4)
        
        if target_blog in final_img and final_img[target_blog]:
            correct_img = final_img[target_blog]
            # Normalize to relative path
            if correct_img.startswith("https://"):
                correct_rel = "/" + correct_img.split("yeatru.com/", 1)[-1]
            else:
                correct_rel = correct_img
            
            if old_img != correct_rel:
                changes[0] += 1
                return f'{prefix}{correct_rel}{suffix}'
        
        return match.group(0)
    
    content = re.sub(card_pattern, fix_card, content, flags=re.DOTALL)
    
    # Also handle a simpler pattern: href="blog-XXX.html" ... <img src="..." class="card-img-top"
    # This catches related cards with slightly different HTML structure
    simple_pattern = r'(href="(blog-[^"#]+\.html)"[^>]*>.*?class="card-img-top[^"]*"[^>]*src=")([^"]+)(")'
    
    def fix_simple(match):
        prefix = match.group(1)
        target_blog = match.group(2)
        old_img = match.group(3)
        suffix = match.group(4)
        
        if target_blog in final_img and final_img[target_blog]:
            correct_img = final_img[target_blog]
            if correct_img.startswith("https://"):
                correct_rel = "/" + correct_img.split("yeatru.com/", 1)[-1]
            else:
                correct_rel = correct_img
            
            if old_img != correct_rel:
                changes[0] += 1
                return f'{prefix}{correct_rel}{suffix}'
        
        return match.group(0)
    
    content = re.sub(simple_pattern, fix_simple, content, flags=re.DOTALL)
    
    if changes[0] > 0:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
        blogs_fixed += 1
        total_fixed += changes[0]
        print(f"  Fixed {changes[0]} cards in {blog}")

# Step 3: Also fix featured images in blogs that still use wrong images
# For each blog, if the featured image (article-featured-image) doesn't match its og:image, fix it
print("\n=== Fixing featured images ===")
featured_fixed = [0]
for blog in all_blogs:
    path = os.path.join(WORKSPACE, blog)
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        content = fh.read()
    
    if blog not in final_img or not final_img[blog]:
        continue
    
    correct_img = final_img[blog]
    if correct_img.startswith("https://"):
        correct_rel = "/" + correct_img.split("yeatru.com/", 1)[-1]
    else:
        correct_rel = correct_img
    
    # Find featured image: <div class="article-featured-image"> <img src="..." ...>
    featured_pattern = r'(class="article-featured-image"[^>]*>\s*<img[^>]+src=")([^"]+)(")'
    
    def fix_featured(match):
        old_img = match.group(2)
        if old_img != correct_rel:
            featured_fixed[0] += 1
            return f'{match.group(1)}{correct_rel}{match.group(3)}'
        return match.group(0)
    
    content = re.sub(featured_pattern, fix_featured, content)
    
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)

print(f"\n=== Summary ===")
print(f"Related cards fixed: {total_fixed} cards across {blogs_fixed} blogs")
print(f"Featured images fixed: {featured_fixed[0]}")

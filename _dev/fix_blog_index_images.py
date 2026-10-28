#!/usr/bin/env python3
"""
Fix blog.html index page: replace all duplicate/broken card images with
each blog's correct unique image (from final_img map).
Also fix the 4 missing image filenames.
"""
import os, re

WORKSPACE = "/workspace"

# Step 1: Build final image map for ALL 124 blogs from their og:image
all_blogs = sorted([f for f in os.listdir(WORKSPACE) if f.startswith("blog-") and f.endswith(".html") and f != "blog.html"])
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
    else:
        final_img[blog] = ""

# Step 2: Fix specific broken images (rename files to match references)
# 1. blog-1688-shopping-agent-english-storage.jpg -> blog-1688-shopping-agent-english.jpg
src = os.path.join(WORKSPACE, "Images/blog/blog-1688-shopping-agent-english-storage.jpg")
dst = os.path.join(WORKSPACE, "Images/blog/blog-1688-shopping-agent-english.jpg")
if os.path.exists(src) and not os.path.exists(dst):
    os.rename(src, dst)
    print(f"Renamed: blog-1688-shopping-agent-english-storage.jpg -> blog-1688-shopping-agent-english.jpg")

# 2. blog-individual-seller-v7.jpg -> blog-individual-seller-china-sourcing.jpg (if missing)
src2 = os.path.join(WORKSPACE, "Images/blog/blog-individual-seller-v7.jpg")
dst2 = os.path.join(WORKSPACE, "Images/blog/blog-individual-seller-china-sourcing.jpg")
if os.path.exists(src2) and not os.path.exists(dst2):
    import shutil
    shutil.copy2(src2, dst2)
    print(f"Copied: blog-individual-seller-v7.jpg -> blog-individual-seller-china-sourcing.jpg")

# 3. blog-tiktok-shop-compliance-2026.jpg - check if blog-3-tiktok-compliance-v2.jpg can be used
dst3 = os.path.join(WORKSPACE, "Images/blog/blog-tiktok-shop-compliance-2026.jpg")
if not os.path.exists(dst3):
    src3 = os.path.join(WORKSPACE, "Images/blog/blog-3-tiktok-compliance-v2.jpg")
    if os.path.exists(src3):
        import shutil
        shutil.copy2(src3, dst3)
        print(f"Copied: blog-3-tiktok-compliance-v2.jpg -> blog-tiktok-shop-compliance-2026.jpg")

# 4. Audit2.jpg.jpg (double extension) -> Audit2.jpg
dst4 = os.path.join(WORKSPACE, "Images/blog/Audit2.jpg")
src4 = os.path.join(WORKSPACE, "Images/Audit2.jpg")  # exists in Images root
if not os.path.exists(dst4) and os.path.exists(src4):
    import shutil
    shutil.copy2(src4, dst4)
    print(f"Copied: Images/Audit2.jpg -> Images/blog/Audit2.jpg")
# Also handle the blog/Audit2.jpg.jpg reference
dst4b = os.path.join(WORKSPACE, "Images/blog/Audit2.jpg.jpg")
if not os.path.exists(dst4b) and os.path.exists(dst4):
    import shutil
    shutil.copy2(dst4, dst4b)
    print(f"Copied: Audit2.jpg -> Audit2.jpg.jpg (to match broken ref)")

# Step 3: Now update blog.html card images
blog_html_path = os.path.join(WORKSPACE, "blog.html")
with open(blog_html_path, "r", encoding="utf-8", errors="replace") as fh:
    content = fh.read()

# Pattern: <a href="blog-XXX.html" ...> <img src="/Images/..." ...>
# We need to find each blog card and replace its image with the correct one
card_pattern = r'(href="(blog-[^"#]+\.html)"[^>]*>.*?<img[^>]+src=")([^"]+)(")'
replacements = 0

def replace_card_img(match):
    global replacements
    prefix = match.group(1)
    blog_file = match.group(2)
    old_img = match.group(3)
    suffix = match.group(4)
    
    if blog_file in final_img and final_img[blog_file]:
        new_img = final_img[blog_file]
        # Normalize to relative path
        if new_img.startswith("https://"):
            new_rel = "/" + new_img.split("yeatru.com/", 1)[-1]
        else:
            new_rel = new_img
        
        if old_img != new_rel:
            replacements += 1
            return f'{prefix}{new_rel}{suffix}'
    
    return match.group(0)

content = re.sub(card_pattern, replace_card_img, content, flags=re.DOTALL)

with open(blog_html_path, "w", encoding="utf-8") as fh:
    fh.write(content)

print(f"\n=== blog.html updated: {replacements} card images replaced ===")

# Step 4: Verify no more duplicates
print("\n=== Verification: image frequency on blog.html ===")
img_freq = {}
for m in re.finditer(r'src="(/Images/[^"]*\.(jpg|png|webp)[^"]*)"', content):
    img = m.group(1)
    img_freq[img] = img_freq.get(img, 0) + 1
for img, count in sorted(img_freq.items(), key=lambda x: -x[1])[:15]:
    print(f"  {count:3d}x  {img}")

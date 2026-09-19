#!/usr/bin/env python3
"""Find unused image files in /workspace/Images/blog/ and /workspace/Images/."""
import os
import re
import glob

WORKSPACE = "/workspace"

# 1. Collect all image references from all HTML files
img_refs = set()
html_files = glob.glob(os.path.join(WORKSPACE, "*.html"))
for html_file in html_files:
    try:
        with open(html_file, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
    except Exception:
        continue
    # Match img src, og:image, twitter:image, data-src
    for m in re.finditer(r'(?:src|content|data-src)="(/Images/[^"]+)"', content):
        img_refs.add(m.group(1))

print(f"Total image references in HTML: {len(img_refs)}")

# 2. List all image files in /Images/blog/ and /Images/
def list_images(folder):
    files = []
    if not os.path.isdir(folder):
        return files
    for ext in ("*.jpg", "*.jpeg", "*.png", "*.webp"):
        files.extend(glob.glob(os.path.join(folder, ext)))
        files.extend(glob.glob(os.path.join(folder, ext.upper())))
    return files

all_image_files = list_images(os.path.join(WORKSPACE, "Images")) + \
                  list_images(os.path.join(WORKSPACE, "Images", "blog"))

print(f"Total image files on disk: {len(all_image_files)}")

# 3. Identify unused images
unused = []
used = []
for f in all_image_files:
    rel_path = "/" + os.path.relpath(f, WORKSPACE)
    if rel_path in img_refs:
        used.append(rel_path)
    else:
        unused.append(rel_path)

print(f"Used images: {len(used)}")
print(f"Unused images: {len(unused)}")
print("\n=== UNUSED IMAGES ===")
for u in sorted(unused):
    size = os.path.getsize(os.path.join(WORKSPACE, u.lstrip("/")))
    print(f"  {u}  ({size} bytes)")

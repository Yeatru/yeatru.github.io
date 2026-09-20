#!/usr/bin/env python3
"""Compress all blog images: resize to web-friendly dimensions, re-encode JPEG.

Rules:
- Max width 1200px (hero images). Card images display at 400px, hero at ~780px
  in col-lg-8, so 1200px is generous for retina.
- JPEG quality 82, progressive=True, optimize=True.
- Only process if result is smaller than original (never upscale).
- Skip images already <= 180KB AND already <= 1280px wide (already web-optimized).
"""
import os
import sys
from PIL import Image

BLOG_DIR = "/workspace/Images/blog"
MAX_WIDTH = 1200
JPEG_QUALITY = 82
SKIP_MAX_SIZE = 180 * 1024  # 180 KB
SKIP_MAX_WIDTH = 1280

total_before = 0
total_after = 0
processed = 0
skipped = 0

files = [f for f in os.listdir(BLOG_DIR) if f.lower().endswith((".jpg", ".jpeg"))]

for fname in files:
    fpath = os.path.join(BLOG_DIR, fname)
    orig_size = os.path.getsize(fpath)
    try:
        im = Image.open(fpath)
    except Exception as e:
        print(f"SKIP (open error) {fname}: {e}")
        skipped += 1
        continue

    w, h = im.size
    # Skip if already web-optimized
    if orig_size <= SKIP_MAX_SIZE and w <= SKIP_MAX_WIDTH:
        skipped += 1
        continue

    # Resize if too wide
    if w > MAX_WIDTH:
        new_w = MAX_WIDTH
        new_h = int(h * MAX_WIDTH / w)
        im = im.resize((new_w, new_h), Image.LANCZOS)
        w, h = new_w, new_h

    # Re-encode
    tmp_path = fpath + ".tmp"
    if im.mode in ("RGBA", "P"):
        im = im.convert("RGB")
    im.save(tmp_path, "JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True)

    new_size = os.path.getsize(tmp_path)
    if new_size < orig_size:
        os.replace(tmp_path, fpath)
        total_before += orig_size
        total_after += new_size
        processed += 1
        saving = (1 - new_size / orig_size) * 100
        print(f"{fname}: {orig_size//1024:4d}KB -> {new_size//1024:4d}KB  ({saving:.0f}% smaller)  {w}x{h}")
    else:
        os.remove(tmp_path)
        skipped += 1

print(f"\n=== Summary ===")
print(f"Processed: {processed}")
print(f"Skipped (already optimized): {skipped}")
print(f"Total before: {total_before/1024:.0f} KB")
print(f"Total after:  {total_after/1024:.0f} KB")
print(f"Saved:        {(total_before-total_after)/1024:.0f} KB  ({(1-total_after/total_before)*100:.0f}%)")

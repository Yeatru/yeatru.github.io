#!/usr/bin/env python3
"""Detect templated NEW blog posts by looking for shared template signatures.

A blog is "templated" if it contains the boilerplate sentences that appear
in every templated post (e.g. "is not an optional step — it directly
determines whether your order lands on time, on spec, and on budget").
"""
import os
import re
import glob

WORKSPACE = "/workspace"

with open("/tmp/new_blogs.txt") as f:
    NEW_BLOGS = sorted(set(line.strip() for line in f if line.strip()))

# Template signatures — these exact phrases appear in EVERY templated blog.
SIGNATURES = [
    "is not an optional step — it directly determines whether your order lands on time, on spec, and on budget",
    "This guide covers everything you need to know, with actionable checklists, cost tables, and red flags based on Yeatru's 14+ years handling sourcing from Yiwu",
    "The process typically follows these stages. First, define your requirement clearly. Second, identify qualified suppliers or service providers.",
    "Most first-time buyers make the same mistakes in",
    "Understanding the real cost structure helps you negotiate from a position of knowledge.",
    "Focusing only on the lowest unit price.",
    "Skipping supplier verification.",
    "Yeatru Sourcing specializes in",
    "For standard products, 5-15 days from RFQ to confirmed supplier.",
    "MOQ varies by product: off-the-shelf Yiwu goods accept 10-100 pieces; OEM private label typically requires 300-1,000 pieces per SKU.",
    "Use AQL 2.5 pre-shipment inspection with photo and video documentation.",
    "Standard terms are 50% deposit to start production and 50% balance after pre-shipment QC approval.",
]

templated = []
not_templated = []
for blog in NEW_BLOGS:
    path = os.path.join(WORKSPACE, blog + ".html")
    if not os.path.exists(path):
        continue
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()
    hits = sum(1 for sig in SIGNATURES if sig in content)
    # Require at least 8 of 12 signatures to count as templated
    if hits >= 8:
        templated.append((blog, hits))
    else:
        not_templated.append((blog, hits))

print(f"NEW blogs scanned: {len(templated) + len(not_templated)}")
print(f"TEMPLATED (≥8/12 signatures): {len(templated)}")
print(f"NOT templated (<8 signatures): {len(not_templated)}")

print("\n=== NOT TEMPLATED (might already have unique content) ===")
for b, h in not_templated:
    print(f"  {b}  (hits={h}/12)")

print("\n=== TEMPLATED blogs (need rewrite) ===")
with open("/tmp/templated_blogs.txt", "w") as f:
    for b, h in templated:
        f.write(b + "\n")
print(f"Saved to /tmp/templated_blogs.txt ({len(templated)} blogs)")
print("\nFirst 10 templated:")
for b, h in templated[:10]:
    print(f"  {b}  (hits={h}/12)")

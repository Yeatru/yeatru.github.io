#!/usr/bin/env python3
"""Detect templated (duplicate body) NEW blog posts.

For each NEW blog (added in commit c12fc44), extract the article body,
normalize by masking the topic word, then group by identical normalized body.
Blogs sharing the same normalized body are templated duplicates.
"""
import os
import re
import glob
import hashlib

WORKSPACE = "/workspace"

# NEW blogs (added in c12fc44 commit) — read from /tmp/new_blogs.txt
with open("/tmp/new_blogs.txt") as f:
    NEW_BLOGS = set(line.strip() for line in f if line.strip())
print(f"NEW blogs to scan: {len(NEW_BLOGS)}")


def extract_body(html_path):
    """Extract the article body content between <article ...> and </article>."""
    try:
        with open(html_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
    except Exception:
        return ""

    # Extract from <article class="article-content"> to </article>
    m = re.search(r'<article class="article-content">(.*?)</article>', content, re.DOTALL)
    if not m:
        return ""
    body = m.group(1)
    # Remove the featured image div and author bio aside (those are common/legit)
    body = re.sub(r'<div class="article-featured-image">.*?</div>', '', body, flags=re.DOTALL)
    body = re.sub(r'<aside class="author-bio.*?</aside>', '', body, flags=re.DOTALL)
    # Strip all HTML tags
    text = re.sub(r'<[^>]+>', ' ', body)
    # Collapse whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def normalize(text, slug):
    """Mask the topic word (derived from slug) so templated bodies collapse."""
    # Derive topic words from slug, e.g. blog-air-freight-china -> ["air freight", "air", "freight", "china"]
    parts = slug.replace("blog-", "").replace("-china", "").replace("-2026", "").split("-")
    topic_words = set()
    # individual words
    for p in parts:
        if len(p) > 2:
            topic_words.add(p.lower())
            topic_words.add(p.capitalize())
            topic_words.add(p.upper())
    # joined phrase
    phrase = " ".join(parts)
    topic_words.add(phrase)
    topic_words.add(phrase.lower())
    topic_words.add(phrase.capitalize())

    norm = text
    for w in topic_words:
        norm = norm.replace(w, "TOPIC")
    # Also mask the H1 title which appears at start
    return norm


# Collect normalized bodies for all NEW blogs
results = {}
for blog in sorted(NEW_BLOGS):
    path = os.path.join(WORKSPACE, blog + ".html")
    if not os.path.exists(path):
        continue
    body = extract_body(path)
    norm = normalize(body, blog)
    md5 = hashlib.md5(norm.encode("utf-8", errors="replace")).hexdigest()
    results[blog] = {"md5": md5, "body_len": len(body), "norm_len": len(norm)}

# Group by md5
by_md5 = {}
for blog, info in results.items():
    by_md5.setdefault(info["md5"], []).append(blog)

templated_groups = {k: v for k, v in by_md5.items() if len(v) > 1}
unique_groups = {k: v for k, v in by_md5.items() if len(v) == 1}

print(f"\n=== TEMPLATED BODY GROUPS (identical after topic-word masking) ===")
print(f"Groups: {len(templated_groups)}")
print(f"Total templated blogs: {sum(len(v) for v in templated_groups.values())}")
print(f"Unique-body blogs: {len(unique_groups)}")

for md5, blogs in sorted(templated_groups.items(), key=lambda x: -len(x[1])):
    print(f"\n  md5={md5[:12]}  count={len(blogs)}  body_len={results[blogs[0]]['body_len']}")
    # show first 3
    for b in blogs[:5]:
        print(f"    {b}")
    if len(blogs) > 5:
        print(f"    ... and {len(blogs)-5} more")

# Save full list of templated blogs to a file for the rewrite phase
all_templated = []
for blogs in templated_groups.values():
    all_templated.extend(blogs)
with open("/tmp/templated_blogs.txt", "w") as f:
    for b in sorted(all_templated):
        f.write(b + "\n")
print(f"\nTemplated blog list saved to /tmp/templated_blogs.txt ({len(all_templated)} blogs)")

# Also show a sample normalized body to confirm it's really templated
if templated_groups:
    sample_md5 = list(templated_groups.keys())[0]
    sample_blog = templated_groups[sample_md5][0]
    sample_body = extract_body(os.path.join(WORKSPACE, sample_blog + ".html"))
    print(f"\n=== SAMPLE normalized body (blog: {sample_blog}) ===")
    print(sample_body[:800] + "...")

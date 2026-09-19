#!/usr/bin/env python3
"""Insert 100 new blog cards into blog.html and update sitemap-static.xml."""
import os, re

REPO = '/workspace'
from blog_topics import TOPICS

# --- 1. Build blog cards for all new topics ---
cards = ''
for t in TOPICS:
    slug = t['slug']
    title = t['title']
    desc = t['desc']
    cat = t['cat']
    img = t['img']
    cards += f'''<a href="{slug}.html" class="blog-card">
 <div class="blog-card-image">
 <img src="{img}" alt="{title}" loading="lazy" decoding="async" width="400" height="225">
 <span class="blog-card-category">{cat}</span>
 </div>
 <div class="blog-card-content">
 <div class="blog-card-meta">
 <span><i class="far fa-calendar"></i> Sep 19 2026</span>
 <span><i class="far fa-clock"></i> 8 min</span>
 </div>
 <h3 class="blog-card-title">{title}</h3>
 <p class="blog-card-excerpt">{desc}</p>
 <span class="blog-card-link">Read Article <i class="fas fa-arrow-right"></i></span>
 </div>
 </a>
'''

# Insert cards right after the opening blog-grid div
blog_path = os.path.join(REPO, 'blog.html')
with open(blog_path, encoding='utf-8') as f:
    content = f.read()

marker = '<div class="blog-grid mb-5">'
assert marker in content, 'blog-grid marker not found'
content = content.replace(marker, marker + '\n' + cards, 1)
with open(blog_path, 'w', encoding='utf-8') as f:
    f.write(content)
print(f"Inserted {len(TOPICS)} blog cards into blog.html")

# --- 2. Update sitemap-static.xml ---
sitemap_path = os.path.join(REPO, 'sitemap-static.xml')
with open(sitemap_path, encoding='utf-8') as f:
    sm = f.read()

new_urls = ''
for t in TOPICS:
    new_urls += f'  <url><loc>https://www.yeatru.com/{t["slug"]}.html</loc><lastmod>2026-09-19</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>\n'

# Insert before closing </urlset>
sm = sm.replace('</urlset>', new_urls + '</urlset>')
with open(sitemap_path, 'w', encoding='utf-8') as f:
    f.write(sm)
print(f"Added {len(TOPICS)} URLs to sitemap-static.xml")

# --- 3. Update sitemap.xml (main sitemap index points to static) ---
print("Done.")

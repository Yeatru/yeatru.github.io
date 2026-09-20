#!/usr/bin/env python3
import sys

path = sys.argv[1]
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

start_marker = '<div class="article-featured-image">'
end_marker = '<aside class="author-bio'

start_idx = content.index(start_marker)
# find the end of the featured-image div
after_featured = content.index('</div>', start_idx) + len('</div>')
end_idx = content.index(end_marker, after_featured)

with open("/workspace/_new_body.html", "r", encoding="utf-8") as f:
    new_body = f.read()

new_content = content[:after_featured] + "\n" + new_body + content[end_idx:]
with open(path, "w", encoding="utf-8") as f:
    f.write(new_content)

print(f"Replaced body in {path}; chars: {len(new_body)}")

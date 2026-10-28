#!/usr/bin/env python3
"""De-stuff repetitive internal links in a blog article body.

For each href that appears more than once inside the <article class="article-content">
block, keep only the first occurrence as an <a> tag and convert the rest to plain
text (the link's visible text). This removes SEO link-spam while preserving the
first, most relevant link to each target.
"""
import re
import sys

A_TAG_RE = re.compile(r'<a\b[^>]*\bhref="([^"]*)"[^>]*>(.*?)</a>', re.DOTALL | re.IGNORECASE)

def strip_tags(s):
    """Convert any nested tags inside link text to nothing (plain text)."""
    return re.sub(r'<[^>]+>', '', s)

def destuff(html, start_marker='<article class="article-content">', end_marker='</article>'):
    s = html.find(start_marker)
    if s == -1:
        return html, 0
    # find matching </article> after start
    e = html.find(end_marker, s)
    if e == -1:
        e = len(html)
    else:
        e += len(end_marker)
    body = html[s:e]
    seen = set()
    removed = 0
    def repl(m):
        nonlocal removed
        href = m.group(1)
        text = m.group(2)
        if href in seen:
            removed += 1
            return strip_tags(text)
        seen.add(href)
        return m.group(0)
    new_body = A_TAG_RE.sub(repl, body)
    return html[:s] + new_body + html[e:], removed

def main():
    files = sys.argv[1:]
    for f in files:
        with open(f, 'r', encoding='utf-8') as fh:
            html = fh.read()
        new_html, removed = destuff(html)
        if removed:
            with open(f, 'w', encoding='utf-8') as fh:
                fh.write(new_html)
            print(f"{f}: removed {removed} duplicate link(s)")
        else:
            print(f"{f}: no duplicates")

if __name__ == '__main__':
    main()

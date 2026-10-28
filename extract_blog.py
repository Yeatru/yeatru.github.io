#!/usr/bin/env python3
"""Convert blog-*.html to Hugo markdown."""
import re, os, glob
from html import unescape

SRC = "/workspace"
MD_OUT = "/workspace/content/blog"

def extract_meta(html, name):
    m = re.search(rf'<meta[^>]+(?:name|property)="{name}"[^>]+content="([^"]*)"', html)
    return unescape(m.group(1)) if m else ""

def html_to_markdown(html_text):
    """Basic HTML to Markdown conversion for article content."""
    t = html_text
    # Remove scripts, styles, nav, footer, etc.
    t = re.sub(r'<script[^>]*>.*?</script>', '', t, flags=re.DOTALL)
    t = re.sub(r'<style[^>]*>.*?</style>', '', t, flags=re.DOTALL)
    # Headers
    t = re.sub(r'<h1[^>]*>(.*?)</h1>', r'\n# \1\n', t, flags=re.DOTALL)
    t = re.sub(r'<h2[^>]*>(.*?)</h2>', r'\n## \1\n', t, flags=re.DOTALL)
    t = re.sub(r'<h3[^>]*>(.*?)</h3>', r'\n### \1\n', t, flags=re.DOTALL)
    t = re.sub(r'<h4[^>]*>(.*?)</h4>', r'\n#### \1\n', t, flags=re.DOTALL)
    # Paragraphs
    t = re.sub(r'<p[^>]*>(.*?)</p>', r'\n\1\n', t, flags=re.DOTALL)
    # Line breaks
    t = re.sub(r'<br\s*/?>', '\n', t)
    # Bold/italic
    t = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', t, flags=re.DOTALL)
    t = re.sub(r'<b[^>]*>(.*?)</b>', r'**\1**', t, flags=re.DOTALL)
    t = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', t, flags=re.DOTALL)
    t = re.sub(r'<i[^>]*>(.*?)</i>', r'*\1*', t, flags=re.DOTALL)
    # Links
    t = re.sub(r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', r'[\2](\1)', t, flags=re.DOTALL)
    # Images
    t = re.sub(r'<img[^>]*src="([^"]*)"[^>]*alt="([^"]*)"[^>]*>', r'![\2](\1)', t)
    t = re.sub(r'<img[^>]*src="([^"]*)"[^>]*>', r'![](\1)', t)
    # Lists
    t = re.sub(r'<ul[^>]*>', '\n', t)
    t = re.sub(r'<ol[^>]*>', '\n', t)
    t = re.sub(r'</ul>', '\n', t)
    t = re.sub(r'</ol>', '\n', t)
    t = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1', t, flags=re.DOTALL)
    # Blockquote
    t = re.sub(r'<blockquote[^>]*>(.*?)</blockquote>', r'> \1', t, flags=re.DOTALL)
    # Tables - keep simple
    t = re.sub(r'<table[^>]*>', '\n', t)
    t = re.sub(r'</table>', '\n', t)
    t = re.sub(r'<tr[^>]*>', '', t)
    t = re.sub(r'</tr>', '\n', t)
    t = re.sub(r'<t[dh][^>]*>', '| ', t)
    t = re.sub(r'</t[dh]>', ' |', t)
    # Remove remaining tags
    t = re.sub(r'<[^>]+>', '', t)
    # Unescape HTML entities
    t = unescape(t)
    # Clean whitespace
    t = re.sub(r'[ \t]+\n', '\n', t)
    t = re.sub(r'\n{3,}', '\n\n', t)
    return t.strip()

def extract_article_body(html):
    """Extract the main article content from a blog page."""
    # Try to find the article content area
    # Look for common patterns
    patterns = [
        r'<article[^>]*>(.*?)</article>',
        r'<main[^>]*>(.*?)</main>',
        r'<div[^>]*class="[^"]*article-content[^"]*"[^>]*>(.*?)</div>',
        r'<div[^>]*class="[^"]*post-content[^"]*"[^>]*>(.*?)</div>',
        r'<div[^>]*class="[^"]*blog-content[^"]*"[^>]*>(.*?)</div>',
        r'<div[^>]*id="[^"]*content[^"]*"[^>]*>(.*?)</div>',
    ]
    for pat in patterns:
        m = re.search(pat, html, re.DOTALL|re.IGNORECASE)
        if m:
            content = m.group(1)
            # Remove nav, sidebar, comments, forms
            content = re.sub(r'<nav[^>]*>.*?</nav>', '', content, flags=re.DOTALL)
            content = re.sub(r'<aside[^>]*>.*?</aside>', '', content, flags=re.DOTALL)
            content = re.sub(r'<form[^>]*>.*?</form>', '', content, flags=re.DOTALL)
            content = re.sub(r'<footer[^>]*>.*?</footer>', '', content, flags=re.DOTALL)
            content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
            if len(content.strip()) > 200:
                return content
    # Fallback: take everything between h1 and the contact/cta section
    h1 = re.search(r'<h1[^>]*>', html)
    if h1:
        start = h1.start()
        # Find a good end point
        end_markers = ['<section', '<footer', 'id="contact"', 'id="faq"', 'Request a Quote']
        end = len(html)
        for marker in end_markers:
            idx = html.find(marker, start + 500)
            if idx > 0 and idx < end:
                end = idx
        return html[start:end]
    return ""

def main():
    files = sorted(glob.glob(os.path.join(SRC, "blog-*.html")))
    print(f"Found {len(files)} blog files")
    os.makedirs(MD_OUT, exist_ok=True)
    count = 0

    for f in files:
        basename = os.path.basename(f)
        slug = basename.replace(".html", "")
        html = open(f, encoding="utf-8", errors="ignore").read()

        title = extract_meta(html, "og:title") or extract_meta(html, "title")
        description = extract_meta(html, "description")
        keywords = extract_meta(html, "keywords")
        # Try to extract date
        date_m = re.search(r'"datePublished"\s*:\s*"([^"]+)"', html)
        date = date_m.group(1)[:10] if date_m else "2026-01-01"

        body_html = extract_article_body(html)
        body_md = html_to_markdown(body_html)

        if not title:
            # fallback to h1
            h1 = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
            title = re.sub(r'<[^>]+>', '', h1.group(1)).strip() if h1 else slug

        # Build markdown
        lines = ["---"]
        lines.append(f'title: "{title.replace(chr(34), chr(39))}"')
        lines.append(f'url: "/{basename}"')
        lines.append(f'date: {date}')
        lines.append(f'type: blog')
        if description:
            desc = description[:300].replace('"', '\\"')
            lines.append(f'description: "{desc}"')
        if keywords:
            lines.append(f'keywords: "{keywords[:200]}"')
        lines.append("---")
        lines.append("")
        lines.append(body_md)

        md_path = os.path.join(MD_OUT, f"{slug}.md")
        with open(md_path, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines))
        count += 1

    print(f"Generated {count} blog markdown files")

if __name__ == "__main__":
    main()

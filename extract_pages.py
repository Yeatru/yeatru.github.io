#!/usr/bin/env python3
"""Convert remaining service/landing pages to Hugo markdown.
   Skips product-*, blog-*, and already-migrated pages."""
import re, os, glob
from html import unescape

SRC = "/workspace"
MD_OUT = "/workspace/content/pages"

SKIP_PREFIXES = ("product-YCS-", "blog-", "index.html", "404.html", "blog.html", "all-products.html")
# Pages that need custom layouts or are handled separately
SPECIAL = {"categories.html", "contact.html", "request-quote.html", "faq.html"}

def extract_meta(html, name):
    m = re.search(rf'<meta[^>]+(?:name|property)="{name}"[^>]+content="([^"]*)"', html)
    return unescape(m.group(1)) if m else ""

def html_to_markdown(html_text):
    t = html_text
    t = re.sub(r'<script[^>]*>.*?</script>', '', t, flags=re.DOTALL)
    t = re.sub(r'<style[^>]*>.*?</style>', '', t, flags=re.DOTALL)
    t = re.sub(r'<h1[^>]*>(.*?)</h1>', r'\n# \1\n', t, flags=re.DOTALL)
    t = re.sub(r'<h2[^>]*>(.*?)</h2>', r'\n## \1\n', t, flags=re.DOTALL)
    t = re.sub(r'<h3[^>]*>(.*?)</h3>', r'\n### \1\n', t, flags=re.DOTALL)
    t = re.sub(r'<h4[^>]*>(.*?)</h4>', r'\n#### \1\n', t, flags=re.DOTALL)
    t = re.sub(r'<p[^>]*>(.*?)</p>', r'\n\1\n', t, flags=re.DOTALL)
    t = re.sub(r'<br\s*/?>', '\n', t)
    t = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', t, flags=re.DOTALL)
    t = re.sub(r'<b[^>]*>(.*?)</b>', r'**\1**', t, flags=re.DOTALL)
    t = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', t, flags=re.DOTALL)
    t = re.sub(r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', r'[\2](\1)', t, flags=re.DOTALL)
    t = re.sub(r'<img[^>]*src="([^"]*)"[^>]*alt="([^"]*)"[^>]*>', r'![\2](\1)', t)
    t = re.sub(r'<img[^>]*src="([^"]*)"[^>]*>', r'![](\1)', t)
    t = re.sub(r'<ul[^>]*>', '\n', t)
    t = re.sub(r'<ol[^>]*>', '\n', t)
    t = re.sub(r'</ul>', '\n', t)
    t = re.sub(r'</ol>', '\n', t)
    t = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1', t, flags=re.DOTALL)
    t = re.sub(r'<blockquote[^>]*>(.*?)</blockquote>', r'> \1', t, flags=re.DOTALL)
    t = re.sub(r'<table[^>]*>', '\n', t)
    t = re.sub(r'</table>', '\n', t)
    t = re.sub(r'<tr[^>]*>', '', t)
    t = re.sub(r'</tr>', '\n', t)
    t = re.sub(r'<t[dh][^>]*>', '| ', t)
    t = re.sub(r'</t[dh]>', ' |', t)
    t = re.sub(r'<[^>]+>', '', t)
    t = unescape(t)
    t = re.sub(r'[ \t]+\n', '\n', t)
    t = re.sub(r'\n{3,}', '\n\n', t)
    return t.strip()

def extract_body(html):
    patterns = [
        r'<main[^>]*>(.*?)</main>',
        r'<article[^>]*>(.*?)</article>',
        r'<div[^>]*class="[^"]*page-content[^"]*"[^>]*>(.*?)</div>',
        r'<div[^>]*class="[^"]*section-content[^"]*"[^>]*>(.*?)</div>',
    ]
    for pat in patterns:
        m = re.search(pat, html, re.DOTALL|re.IGNORECASE)
        if m:
            content = m.group(1)
            content = re.sub(r'<nav[^>]*>.*?</nav>', '', content, flags=re.DOTALL)
            content = re.sub(r'<form[^>]*>.*?</form>', '', content, flags=re.DOTALL)
            content = re.sub(r'<footer[^>]*>.*?</footer>', '', content, flags=re.DOTALL)
            content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
            if len(content.strip()) > 100:
                return content
    # Fallback: body minus header/footer
    body = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL)
    if body:
        content = body.group(1)
        content = re.sub(r'<header[^>]*>.*?</header>', '', content, flags=re.DOTALL)
        content = re.sub(r'<nav[^>]*>.*?</nav>', '', content, flags=re.DOTALL)
        content = re.sub(r'<footer[^>]*>.*?</footer>', '', content, flags=re.DOTALL)
        content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
        content = re.sub(r'<form[^>]*>.*?</form>', '', content, flags=re.DOTALL)
        return content
    return ""

def main():
    files = sorted(glob.glob(os.path.join(SRC, "*.html")))
    os.makedirs(MD_OUT, exist_ok=True)
    count = 0

    for f in files:
        basename = os.path.basename(f)
        if basename.startswith(SKIP_PREFIXES):
            continue
        slug = basename.replace(".html", "")

        html = open(f, encoding="utf-8", errors="ignore").read()
        title = extract_meta(html, "og:title") or extract_meta(html, "title")
        description = extract_meta(html, "description")

        body_html = extract_body(html)
        body_md = html_to_markdown(body_html)

        if not title:
            h1 = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
            title = re.sub(r'<[^>]+>', '', h1.group(1)).strip() if h1 else slug

        layout = ""
        if basename in SPECIAL:
            layout = f'layout: {slug}\n'

        lines = ["---"]
        lines.append(f'title: "{title.replace(chr(34), chr(39))[:120]}"')
        lines.append(f'url: "/{basename}"')
        lines.append(f'type: page')
        if layout:
            lines.append(layout.strip())
        if description:
            desc = description[:300].replace('"', '\\"')
            lines.append(f'description: "{desc}"')
        lines.append("---")
        lines.append("")
        lines.append(body_md)

        md_path = os.path.join(MD_OUT, f"{slug}.md")
        with open(md_path, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines))
        count += 1

    print(f"Generated {count} page markdown files")

if __name__ == "__main__":
    main()

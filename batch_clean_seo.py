#!/usr/bin/env python3
"""
批量清理所有博客的 SEO 机械性问题：
1. H1 / breadcrumb-current / article-category 中的内嵌链接 → 纯文本
2. article-content 体内重复内链 → 去堆砌（每 href 仅保留首次）
3. author-bio 内部链接堆砌 → 纯文本（保留 LinkedIn/Facebook 外链）
4. publisher.logo 误指向博客图片 → 修正为 logo.svg 220x60
5. JSON-LD Article image 尺寸 1200x630 → 2560x1440 + URL 相对转绝对
6. og:image / twitter:image / thumbnailUrl 相对路径 → 绝对
7. og:image:width/height 1200/630 → 2560/1440
"""
import os
import re
import sys

ROOT = "/workspace"
SITE = "https://www.yeatru.com"

A_TAG_RE = re.compile(r'<a\b[^>]*\bhref="([^"]+)"[^>]*>(.*?)</a>', re.IGNORECASE | re.DOTALL)


def strip_tags(s):
    return re.sub(r'<[^>]+>', '', s)


def strip_inner_links(text):
    """把一段 HTML 中的所有 <a> 标签替换为其纯文本内容。"""
    return A_TAG_RE.sub(lambda m: strip_tags(m.group(2)), text)


def fix_h1_breadcrumb(html):
    """移除 H1 / breadcrumb-current / article-category 中的内嵌链接。"""
    count = 0
    # H1
    def repl_h1(m):
        nonlocal count
        inner = strip_inner_links(m.group(2))
        if inner != m.group(2):
            count += 1
        return m.group(1) + inner + m.group(3)
    html = re.sub(r'(<h1\b[^>]*>)(.*?)(</h1>)', repl_h1, html, flags=re.DOTALL)
    # breadcrumb-current span
    def repl_bc(m):
        nonlocal count
        inner = strip_inner_links(m.group(2))
        if inner != m.group(2):
            count += 1
        return m.group(1) + inner + m.group(3)
    html = re.sub(r'(<span\b[^>]*class="[^"]*breadcrumb-current[^"]*"[^>]*>)(.*?)(</span>)', repl_bc, html, flags=re.DOTALL)
    # article-category span
    def repl_cat(m):
        nonlocal count
        inner = strip_inner_links(m.group(2))
        if inner != m.group(2):
            count += 1
        return m.group(1) + inner + m.group(3)
    html = re.sub(r'(<span\b[^>]*class="[^"]*article-category[^"]*"[^>]*>)(.*?)(</span>)', repl_cat, html, flags=re.DOTALL)
    return html, count


def destuff_body(html):
    """article-content 体内重复内链去堆砌。"""
    start_marker = '<article class="article-content">'
    end_marker = '</article>'
    s = html.find(start_marker)
    if s == -1:
        return html, 0
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


def clean_author_bio(html):
    """author-bio 块内的内部链接 → 纯文本，保留外部 LinkedIn/Facebook 链接。"""
    start_marker = '<aside class="author-bio'
    end_marker = '</aside>'
    s = html.find(start_marker)
    if s == -1:
        return html, 0
    e = html.find(end_marker, s)
    if e == -1:
        return html, 0
    e += len(end_marker)
    bio = html[s:e]
    count = 0

    def repl(m):
        nonlocal count
        href = m.group(1)
        text = m.group(2)
        # 保留外部链接（http 开头）
        if href.startswith('http'):
            return m.group(0)
        count += 1
        return strip_tags(text)
    new_bio = A_TAG_RE.sub(repl, bio)
    return html[:s] + new_bio + html[e:], count


def fix_publisher_logo(html):
    """publisher.logo 误指向博客图片 → logo.svg 220x60。"""
    pattern = re.compile(
        r'("logo":\s*\{\s*"@type":\s*"ImageObject",\s*"url":\s*")([^"]*Images/blog/[^"]+\.jpg)("\s*,\s*"width":\s*)1200(\s*,\s*"height":\s*)630(\s*\})',
        re.IGNORECASE,
    )
    def repl(m):
        return m.group(1) + SITE + "/logo.svg" + m.group(3) + "220" + m.group(4) + "60" + m.group(5)
    new_html, n = pattern.subn(repl, html)
    return new_html, n


def fix_article_image(html):
    """JSON-LD Article image 尺寸 1200x630 → 2560x1440，URL 相对转绝对。"""
    pattern = re.compile(
        r'("image":\s*\{\s*"@type":\s*"ImageObject",\s*"url":\s*")([^"]*Images/blog/[^"]+\.jpg)("\s*,\s*"width":\s*)1200(\s*,\s*"height":\s*)630(\s*\})',
        re.IGNORECASE,
    )
    def repl(m):
        url = m.group(2)
        if not url.startswith("http"):
            url = SITE + url
        return m.group(1) + url + m.group(3) + "2560" + m.group(4) + "1440" + m.group(5)
    new_html, n = pattern.subn(repl, html)
    return new_html, n


def fix_thumbnail(html):
    pattern = re.compile(r'("thumbnailUrl":\s*")(/Images/[^"]+)(")')
    new_html, n = pattern.subn(lambda m: m.group(1) + SITE + m.group(2) + m.group(3), html)
    return new_html, n


def fix_og_twitter(html):
    pattern = re.compile(
        r'(<meta\s+(?:property|name)="(?:og:image|twitter:image)"\s+content=")(/Images/[^"]+)(")',
        re.IGNORECASE,
    )
    new_html, n = pattern.subn(lambda m: m.group(1) + SITE + m.group(2) + m.group(3), html)
    return new_html, n


def fix_og_dim(html):
    p1 = re.compile(r'(<meta\s+property="og:image:width"\s+content=")1200(")', re.IGNORECASE)
    p2 = re.compile(r'(<meta\s+property="og:image:height"\s+content=")630(")', re.IGNORECASE)
    h1, n1 = p1.subn(lambda m: m.group(1) + "2560" + m.group(2), html)
    h2, n2 = p2.subn(lambda m: m.group(1) + "1440" + m.group(2), h1)
    return h2, n1 + n2


def main():
    files = sorted(
        os.path.join(ROOT, n)
        for n in os.listdir(ROOT)
        if n.startswith("blog-") and n.endswith(".html") and os.path.isfile(os.path.join(ROOT, n))
    )
    total = {"h1": 0, "destuff": 0, "bio": 0, "logo": 0, "img": 0, "thumb": 0, "ogtw": 0, "ogdim": 0}
    touched = 0
    for path in files:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            html = f.read()
        orig = html
        c = {}
        html, c["h1"] = fix_h1_breadcrumb(html)
        html, c["destuff"] = destuff_body(html)
        html, c["bio"] = clean_author_bio(html)
        html, c["logo"] = fix_publisher_logo(html)
        html, c["img"] = fix_article_image(html)
        html, c["thumb"] = fix_thumbnail(html)
        html, c["ogtw"] = fix_og_twitter(html)
        html, c["ogdim"] = fix_og_dim(html)
        if html == orig:
            continue
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        touched += 1
        for k, v in c.items():
            total[k] += v
        name = os.path.basename(path)
        parts = [f"{k}+{v}" for k, v in c.items() if v]
        print(f"  {name}: {', '.join(parts)}")

    print(f"\n汇总: 处理 {touched}/{len(files)} 篇博客")
    for k, v in total.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()

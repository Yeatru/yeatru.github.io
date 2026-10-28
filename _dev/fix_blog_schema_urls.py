#!/usr/bin/env python3
"""
修复 blog-what-is-sourcing-agent.html 中被批量错误替换的 schema URL 和文本。

错误模式：
- "yeatru.com sourcing agent firm.com" -> "yeatru.com"
- "yeatru.com buyer's advocate firm.com" -> "yeatru.com"
- "info@Yeatru ground-sourcing.com" -> "info@yeatru.com"
- "info@Yeatru sourcing agent firm.com" -> "info@yeatru.com"
- "Yeatru ground-sourcing-logo.png" -> "Yeatru-logo.png"
- "Yeatru mainland-fiduciary-hero-2.jpg" -> "yeatru-hero-2.jpg"
- "blog-what-is-sourcing-agent's sourcing-sourcing agent.jpg" -> "blog-what-is-sourcing-agent.jpg"
- "blog-what-is-sourcing-on-ground representative.jpg" -> "blog-what-is-sourcing-agent.jpg"
- "blog-what-is-sourcing-agent's sourcing-on-ground representative.jpg" -> "blog-what-is-sourcing-agent.jpg"
- "blog-what-is-sourcing-sourcing agent.html" -> "blog-what-is-sourcing-agent.html"
- "blog-what-is-sourcing-agent's sourcing-on-ground representative.html" -> "blog-what-is-sourcing-agent.html"
- "https://www.yeatru.com sourcing agent firm.com/" -> "https://www.yeatru.com/"
- "Yeatru?v=20260909k ground-sourcing_sourcing" -> "Yeatru?v=20260909k"
- 字面 "P…" -> 完整内容
"""
import re

FILE = '/workspace/blog-what-is-sourcing-agent.html'

# (regex_pattern, replacement)
REPLACEMENTS = [
    # 主域替换 - 必须最先做（最长前缀优先）
    (r'yeatru\.com [a-z\']+ [a-z]+ firm\.com', 'yeatru.com'),
    (r'yeatru\.com buyer\'s advocate firm\.com', 'yeatru.com'),
    # 邮箱
    (r'info@Yeatru ground-sourcing\.com', 'info@yeatru.com'),
    (r'info@Yeatru sourcing agent firm\.com', 'info@yeatru.com'),
    # Logo / 图片路径
    (r'Yeatru ground-sourcing-logo\.png', 'Yeatru-logo.png'),
    (r'Yeatru mainland-fiduciary-hero-2\.jpg', 'yeatru-hero-2.jpg'),
    # Blog 图片路径修复
    (r"blog-what-is-sourcing-agent's sourcing-sourcing agent\.jpg", 'blog-what-is-sourcing-agent.jpg'),
    (r'blog-what-is-sourcing-on-ground representative\.jpg', 'blog-what-is-sourcing-agent.jpg'),
    (r"blog-what-is-sourcing-agent's sourcing-on-ground representative\.jpg", 'blog-what-is-sourcing-agent.jpg'),
    # Blog URL 修复
    (r"blog-what-is-sourcing-sourcing agent\.html", 'blog-what-is-sourcing-agent.html'),
    (r"blog-what-is-sourcing-agent's sourcing-on-ground representative\.html", 'blog-what-is-sourcing-agent.html'),
    (r"blog-what-is-sourcing-agent's-sourcing agent\.html", 'blog-what-is-sourcing-agent.html'),
    # Instagram URL 修复
    (r'Yeatru\?v=20260909k ground-sourcing_sourcing', 'Yeatru?v=20260909k'),
    # 修复字面 "P…" 省略号到完整内容
    (r'hidden total landed costs when to use one vs direct local factory\. P…',
     'hidden costs when to use one vs direct factory. Free quote from Yeatru.'),
    (r'hidden acquisition aggregate outlays when to use one vs direct local factory\. P…',
     'hidden costs when to use one vs direct factory. Free quote from Yeatru.'),
    # 描述开头被截断 " does a China China sourcing agent" -> "What does a China sourcing agent"
    (r'"description": " does a China China sourcing agent',
     '"description": "What does a China sourcing agent'),
]

def main():
    with open(FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content
    changes = []
    for pat, repl in REPLACEMENTS:
        new_content, n = re.subn(pat, repl, content)
        if n > 0:
            changes.append(f"  ✓ Pattern {pat!r} -> {repl!r} : {n} 处")
            content = new_content
    if content != original:
        with open(FILE, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"修复完成，共 {len(changes)} 类模式：")
        for c in changes:
            print(c)
    else:
        print("无需修改")

if __name__ == '__main__':
    main()

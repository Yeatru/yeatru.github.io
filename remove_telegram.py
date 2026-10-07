#!/usr/bin/env python3
"""
批量移除网站中所有 Telegram 相关元素（footer social-icon + contact-float-btn）。
用户反馈：Telegram 没什么人用，需要从网站上移除。
"""
import re
import os
import glob

# 模式 1: footer 中的 Telegram social-icon (单行)
# 形如: <a aria-label="Telegram Yeatru Sourcing" class="footer-social-icon" href="https://t.me/..." ...><i class="fab fa-telegram"></i></a>
# 形如: <a href="https://t.me/YeatruSourcing" ... class="footer-social-icon" ...><i class="fab fa-telegram"></i></a>
FOOTER_PATTERN = re.compile(
    r'\s*<a\b[^>]*\bfooter-social-icon\b[^>]*\bhref="https://t\.me/[^"]*"[^>]*>[\s]*<i\b[^>]*\bfa-telegram\b[^>]*></i>\s*</a>\s*',
    re.IGNORECASE | re.DOTALL
)

# 模式 2: contact-float-btn Telegram (多行)
# 形如: <a class="contact-float-btn telegram" ... href="https://t.me/..." ...>...</a>
FLOAT_PATTERN = re.compile(
    r'\s*<a\b[^>]*\bcontact-float-btn\b[^>]*\btelegram\b[^>]*>.*?</a>\s*',
    re.IGNORECASE | re.DOTALL
)

# 模式 3: 任何残留的 t.me/ 链接
RESIDUAL_PATTERN = re.compile(
    r'\s*<a\b[^>]*\bhref="https://t\.me/[^"]*"[^>]*>.*?</a>\s*',
    re.IGNORECASE | re.DOTALL
)

def remove_telegram(html):
    """返回 (new_html, removed_count)"""
    n = 0
    # 第一轮：footer social-icon (单行最严格)
    new_html, count = FOOTER_PATTERN.subn('', html)
    n += count
    # 第二轮：contact-float-btn telegram (多行)
    new_html, count = FLOAT_PATTERN.subn('', new_html)
    n += count
    # 第三轮：残留的 t.me/ 链接
    new_html, count = RESIDUAL_PATTERN.subn('', new_html)
    n += count
    return new_html, n

def main():
    # 扫描所有 .html 文件
    patterns = [
        '/workspace/*.html',
        '/workspace/blog-*.html',
        '/workspace/product-*.html',
        '/workspace/category-*.html',
    ]
    files = set()
    for p in patterns:
        files.update(glob.glob(p))
    files = sorted(files)

    total_files = 0
    total_removed = 0
    files_modified = []

    for f in files:
        try:
            with open(f, 'r', encoding='utf-8') as fh:
                content = fh.read()
        except Exception as e:
            continue
        new_content, count = remove_telegram(content)
        if count > 0:
            with open(f, 'w', encoding='utf-8') as fh:
                fh.write(new_content)
            files_modified.append((os.path.basename(f), count))
            total_files += 1
            total_removed += count

    print(f"扫描 {len(files)} 个 HTML 文件")
    print(f"修改 {total_files} 个文件")
    print(f"共移除 {total_removed} 处 Telegram 元素")
    # 显示前 10 个修改的文件
    print("\n前 10 个修改的文件：")
    for name, count in files_modified[:10]:
        print(f"  ✓ {name}: {count} 处")
    if len(files_modified) > 10:
        print(f"  ... 共 {len(files_modified)} 个文件被修改")

if __name__ == '__main__':
    main()

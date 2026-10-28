#!/usr/bin/env python3
"""
第二轮清理：移除 JSON-LD schema 中 sameAs 数组的 Telegram 链接 + FAQ 文本中的 Telegram 引用。
"""
import re
import os
import glob

# 模式 1: sameAs 数组中的 t.me 链接 (形如 "https://t.me/yeatrusourcing", 或 "https://t.me/yeatru",)
# 需要匹配整个字符串 + 可能的后置逗号
SAMEAS_PATTERN = re.compile(
    r'"https://t\.me/[A-Za-z0-9_]+"\s*,?\s*',
)

# 模式 2: FAQ 文本中的 "or Telegram" / "or Telegram at" / "WhatsApp or Telegram at +86..."
# 替换为 "WhatsApp" only
TELEGRAM_TEXT_PATTERN = re.compile(
    r'\s*\b(?:or\s+)?Telegram\s+at\s*\+86\s*\d[\d\s]*',
    re.IGNORECASE
)
TELEGRAM_TEXT_PATTERN_2 = re.compile(
    r'\s+or\s+Telegram\b',
    re.IGNORECASE
)
# "WhatsApp or Telegram" -> "WhatsApp"
WHATSAPP_TELEGRAM_PATTERN = re.compile(
    r'(WhatsApp)\s+or\s+Telegram',
    re.IGNORECASE
)
# "Contact us on WhatsApp or Telegram at +86 159 8851 6408."
CONTACT_PATTERN = re.compile(
    r'Contact us on (?:WhatsApp|Telegram)(?:\s+or\s+(?:WhatsApp|Telegram))?\s+at\s*\+?[\d\s\-]+\.?',
    re.IGNORECASE
)

def clean_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content
    n = 0
    # 1. sameAs 数组中的 Telegram URL
    new, count = SAMEAS_PATTERN.subn('', content)
    n += count
    content = new
    # 2. "Contact us on WhatsApp or Telegram at +86..." -> "Contact us on WhatsApp at +86..."
    new, count = WHATSAPP_TELEGRAM_PATTERN.subn(r'\1', content)
    n += count
    content = new
    # 3. "or Telegram at +86 159 8851 6408" -> ""
    new, count = TELEGRAM_TEXT_PATTERN.subn('', content)
    n += count
    content = new
    # 4. 残留的 "or Telegram"
    new, count = TELEGRAM_TEXT_PATTERN_2.subn('', content)
    n += count
    content = new

    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return n
    return 0

def main():
    files = sorted(glob.glob('/workspace/*.html'))
    total_files = 0
    total_changes = 0
    modified = []
    for f in files:
        n = clean_file(f)
        if n > 0:
            total_files += 1
            total_changes += n
            modified.append((os.path.basename(f), n))
    print(f"扫描 {len(files)} 个 HTML 文件")
    print(f"修改 {total_files} 个文件，共 {total_changes} 处变更")
    if modified:
        print("\n前 10 个修改：")
        for name, n in modified[:10]:
            print(f"  ✓ {name}: {n} 处")

if __name__ == '__main__':
    main()

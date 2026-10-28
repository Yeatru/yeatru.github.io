#!/usr/bin/env python3
"""
批量修复 19 个 category 页面的 description 截断问题。
模式：description 末尾被截断成 "Free qu..." / "Free q..." / "US. ..." 等，
脚本将其替换为完整的 "Free quote." 结尾。
"""
import re
import glob
import os

# 匹配末尾被截断的 description，捕获前面的主体内容
# 模式: ...content... Free qu... / Free q... / Fre... / Free... / U... / to... / DDP to... 等
PATTERNS = [
    # "Free qu..." / "Free q..." / "Fre..." / "Free..." -> "Free quote."
    (r'Free qu\.\.\."', 'Free quote."'),
    (r'Free q\.\.\."', 'Free quote."'),
    (r'Fr\.\.\."', 'Free quote."'),
    (r'Free \.\.\."', 'Free quote."'),
    (r'Free\.\.\."', 'Free quote."'),
    # "US. ..." -> "US. Free quote."
    (r'US\. \.\.\."', 'US. Free quote."'),
    # "DDP to ..." / "DDP to..." -> "DDP to US. Free quote."
    (r'DDP to \.\.\."', 'DDP to US. Free quote."'),
    (r'DDP to\.\.\."', 'DDP to US. Free quote."'),
    # "DDP to US..." (no period) -> "DDP to US. Free quote."
    (r'DDP to US\.\.\."', 'DDP to US. Free quote."'),
    # "any US ..." -> "any US. Free quote."
    (r'any US \.\.\."', 'any US. Free quote."'),
    # "to..." -> "to US. Free quote."
    (r'\bto\.\.\."', 'to US. Free quote."'),
    # "U..." 单独 -> "US. Free quote."
    (r'\bU\.\.\."', 'US. Free quote."'),
]

def fix_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content
    for pat, repl in PATTERNS:
        content = re.sub(pat, repl, content)
    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    files = sorted(glob.glob('/workspace/category-*.html'))
    fixed = []
    for f in files:
        if fix_file(f):
            fixed.append(os.path.basename(f))
    print(f"Total files scanned: {len(files)}")
    print(f"Files fixed: {len(fixed)}")
    for f in fixed:
        print(f"  ✓ {f}")

if __name__ == '__main__':
    main()

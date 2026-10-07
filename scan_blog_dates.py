#!/usr/bin/env python3
"""
扫描 /workspace 下所有 blog-*.html 文件，
按发布日期排序，筛选 2026-09-19 及之后发布的博客。
"""
import re
import glob
import os
from datetime import date

# 匹配 datePublished 和 dateModified
DATE_PUB_RE = re.compile(
    r'"datePublished"\s*:\s*"([^"]+)"',
    re.IGNORECASE
)
DATE_MOD_RE = re.compile(
    r'"dateModified"\s*:\s*"([^"]+)"',
    re.IGNORECASE
)

def scan_file(path):
    """返回 (date_published, date_modified) 或 (None, None)"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return (None, None)
    pub_m = DATE_PUB_RE.search(content)
    mod_m = DATE_MOD_RE.search(content)
    pub = pub_m.group(1)[:10] if pub_m else None
    mod = mod_m.group(1)[:10] if mod_m else None
    return (pub, mod)

def main():
    files = sorted(glob.glob('/workspace/blog-*.html'))
    print(f"扫描 {len(files)} 个博客文件\n")
    
    cutoff = date(2026, 9, 19)
    after_cutoff = []
    
    for f in files:
        pub, mod = scan_file(f)
        if not pub:
            continue
        try:
            pub_date = date.fromisoformat(pub[:10])
        except Exception:
            continue
        if pub_date >= cutoff:
            after_cutoff.append((pub, mod, os.path.basename(f)))
    
    after_cutoff.sort(key=lambda x: x[0], reverse=True)
    
    print(f"=== {cutoff} 及之后发布的博客 ({len(after_cutoff)} 篇) ===")
    print(f"{'发布日期':<12} {'修改日期':<12} 文件名")
    print("-" * 80)
    for pub, mod, name in after_cutoff:
        print(f"{pub:<12} {mod or '-':<12} {name}")
    
    print(f"\n=== 按月统计 ===")
    by_month = {}
    for pub, mod, name in after_cutoff:
        m = pub[:7]
        by_month.setdefault(m, []).append(name)
    for m in sorted(by_month, reverse=True):
        print(f"  {m}: {len(by_month[m])} 篇")

if __name__ == '__main__':
    main()

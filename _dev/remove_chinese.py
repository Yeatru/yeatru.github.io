#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Remove all Chinese (CJK) characters from every .html file in the repo.
Also cleans up artifacts: empty parentheses, doubled spaces, orphaned
commas/slashes left after stripping CJK, etc.
"""

import os
import re
import glob

ROOT = os.path.dirname(os.path.abspath(__file__))

# CJK Unified Ideographs + Extension A + common CJK punctuation
CJK_RE = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf\u3000-\u303f\uff00-\uffef]+')

def clean_html(text):
    # 1. Remove CJK character runs
    text = CJK_RE.sub('', text)
    # 2. Remove empty parentheses (English) left behind, e.g. "Accessories ()"
    text = re.sub(r'\s*\(\s*\)', '', text)
    # 3. Remove parentheses that only contain whitespace/punctuation after CJK removal
    text = re.sub(r'\s*\([\s,，。、；：""''\-—/]*\)', '', text)
    # 4. Clean up orphaned separators: " , " ", " " / " etc.
    text = re.sub(r'\s+[,，。、；：]\s+', ' ', text)
    text = re.sub(r'[,，。、；：]\s+', ' ', text)
    text = re.sub(r'\s+[,，。、；：]', ' ', text)
    # 5. Collapse multiple spaces
    text = re.sub(r'[ \t]{2,}', ' ', text)
    # 6. Fix "  " before closing tags
    text = re.sub(r' +<', ' <', text)
    text = re.sub(r'> +', '> ', text)
    text = re.sub(r'>  +', '> ', text)
    return text

files = glob.glob(os.path.join(ROOT, "*.html"))
changed = 0
for fpath in files:
    with open(fpath, "r", encoding="utf-8") as f:
        original = f.read()
    if not CJK_RE.search(original):
        continue
    cleaned = clean_html(original)
    if cleaned != original:
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(cleaned)
        changed += 1

print(f"Processed {len(files)} HTML files, cleaned {changed} files with Chinese text.")

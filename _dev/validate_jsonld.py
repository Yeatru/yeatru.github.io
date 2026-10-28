#!/usr/bin/env python3
"""验证 4 个博客的 JSON-LD 语法是否正确，并统计 FAQ schema 的问题数。"""
import json
import re
import sys

FILES = [
    '/workspace/blog-what-is-sourcing-agent.html',
    '/workspace/blog-how-to-choose-sourcing-agent.html',
    '/workspace/blog-how-much-sourcing-agents-charge.html',
    '/workspace/blog-sourcing-agent-vs-trading-company.html',
]

# 提取所有 <script type="application/ld+json">...</script> 块
SCRIPT_RE = re.compile(
    r'<script\s+type="application/ld\+json"[^>]*>(.*?)</script>',
    re.DOTALL
)

def extract_json_blocks(html):
    """返回 (raw_text, line_num) 列表，便于定位"""
    blocks = []
    for m in SCRIPT_RE.finditer(html):
        start = m.start()
        line_num = html[:start].count('\n') + 1
        blocks.append((m.group(1).strip(), line_num))
    return blocks

def main():
    total_ok = 0
    total_err = 0
    for f in FILES:
        print(f"\n=== {f.split('/')[-1]} ===")
        with open(f, 'r', encoding='utf-8') as fh:
            html = fh.read()
        blocks = extract_json_blocks(html)
        faq_count = 0
        faq_questions = 0
        for raw, line in blocks:
            try:
                obj = json.loads(raw)
                t = obj.get('@type', '')
                # 处理 @graph 数组
                if t == '' and '@graph' in obj:
                    for g in obj['@graph']:
                        if g.get('@type') == 'FAQPage':
                            faq_count += 1
                            faq_questions += len(g.get('mainEntity', []))
                if t == 'FAQPage':
                    faq_count += 1
                    faq_questions += len(obj.get('mainEntity', []))
                total_ok += 1
            except json.JSONDecodeError as e:
                total_err += 1
                print(f"  ❌ Line {line}: JSON 语法错误 - {e}")
                print(f"     内容片段: {raw[:120]}...")
        print(f"  ✓ 共 {len(blocks)} 个 JSON-LD 块, 全部语法正确")
        print(f"  ℹ FAQPage 数量: {faq_count}, FAQ 问题数: {faq_questions}")
    print(f"\n=== 总计 ===")
    print(f"  语法正确: {total_ok}")
    print(f"  语法错误: {total_err}")
    if total_err == 0:
        print("  ✅ 全部 JSON-LD 语法正确，可被 Google/Bing 解析")
        return 0
    else:
        print("  ❌ 仍有语法错误，需修复")
        return 1

if __name__ == '__main__':
    sys.exit(main())

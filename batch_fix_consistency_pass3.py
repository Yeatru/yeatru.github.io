#!/usr/bin/env python3
"""Pass 3: Fix remaining site-wide consistency issues.

Fixes:
1. product-sourcing.html: footer dead links (#), old copyright, missing refund/nda, clock link
2. product-sourcing.html: schema address "Yiwu International Trade City" → "NO.188 Shangcheng Ave, Yiwu, Zhejiang, China"
3. brand-knowledge-base.json: vague address → specific
4. faq-knowledge-base.json: check & fix
5. llms-full.txt: registered address alignment
6. page-data.json: vague address → specific
7. payment.html: add postal code 322000 to address
8. Any other pages with schema address still using "Yiwu International Trade City"
"""
import re
from pathlib import Path

ROOT = Path('/workspace')

HTML_FILES = list(ROOT.glob('*.html'))
JSON_FILES = list(ROOT.glob('*.json'))
TXT_FILES = list(ROOT.glob('*.txt'))

# ---------- 1. Fix product-sourcing.html footer + schema ----------
def fix_product_sourcing():
    p = ROOT / 'product-sourcing.html'
    if not p.exists():
        return
    t = p.read_text(encoding='utf-8')

    # 1a. Schema address fix
    t = t.replace(
        '"streetAddress": "Yiwu International Trade City"',
        '"streetAddress": "NO.188 Shangcheng Ave, Yiwu, Zhejiang, China"'
    )

    # 1b. Clock href="#" → Google Maps + address
    t = t.replace(
        '<a href="#" class="footer-link"><i class="fas fa-clock me-2"></i> 24/7 Available</a>',
        '<a href="https://maps.google.com/?q=NO.188+Shangcheng+Avenue+Yiwu+Zhejiang+322000+China" target="_blank" rel="noopener noreferrer" class="footer-link"><i class="fas fa-map-marker-alt me-2"></i> NO.188 Shangcheng Ave, Yiwu, Zhejiang, China</a>'
    )

    # 1c. Copyright + legal links (old block to new block)
    old_copyright_block = '''<p>&copy; 2026 Yeatru Sourcing. <span data-i18n="footer.allRightsReserved">All rights reserved.</span> |
                    <a href="#" class="footer-link d-inline" data-i18n="footer.privacyPolicy">Privacy Policy</a> |
                    <a href="#" class="footer-link d-inline" data-i18n="footer.termsOfService">Terms of Service</a>
                </p>'''
    new_copyright_block = '''<p>&copy; 2022–2026 义乌市弋楚贸易有限公司 · Yeatru Sourcing (YIWU ETRUE TRADING CO., LTD.). All rights reserved. |
                    <a href="privacy.html" class="footer-link d-inline" data-i18n="footer.privacyPolicy">Privacy Policy</a> |
                    <a href="terms.html" class="footer-link d-inline" data-i18n="footer.termsOfService">Terms of Service</a> |
                    <a href="refund.html" class="footer-link d-inline">Refund Policy</a> |
                    <a href="nda.html" class="footer-link d-inline">NDA</a>
                </p>'''
    if old_copyright_block in t:
        t = t.replace(old_copyright_block, new_copyright_block)
    else:
        # Try simpler replacements if full block doesn't match
        t = t.replace(
            '&copy; 2026 Yeatru Sourcing.',
            '&copy; 2022–2026 义乌市弋楚贸易有限公司 · Yeatru Sourcing (YIWU ETRUE TRADING CO., LTD.).'
        )
        t = t.replace(
            '<a href="#" class="footer-link d-inline" data-i18n="footer.privacyPolicy">Privacy Policy</a>',
            '<a href="privacy.html" class="footer-link d-inline" data-i18n="footer.privacyPolicy">Privacy Policy</a>'
        )
        t = t.replace(
            '<a href="#" class="footer-link d-inline" data-i18n="footer.termsOfService">Terms of Service</a>',
            '<a href="terms.html" class="footer-link d-inline" data-i18n="footer.termsOfService">Terms of Service</a> |\n                    <a href="refund.html" class="footer-link d-inline">Refund Policy</a> |\n                    <a href="nda.html" class="footer-link d-inline">NDA</a>'
        )

    p.write_text(t, encoding='utf-8')
    print(f"[FIXED] product-sourcing.html: footer + schema")


# ---------- 2. Fix all HTML pages with schema address "Yiwu International Trade City" ----------
def fix_all_schema_addresses():
    for f in HTML_FILES:
        t = f.read_text(encoding='utf-8')
        if '"streetAddress": "Yiwu International Trade City"' in t:
            t = t.replace(
                '"streetAddress": "Yiwu International Trade City"',
                '"streetAddress": "NO.188 Shangcheng Ave, Yiwu, Zhejiang, China"'
            )
            f.write_text(t, encoding='utf-8')
            print(f"[FIXED] {f.name}: schema streetAddress")


# ---------- 3. Fix brand-knowledge-base.json ----------
def fix_brand_kb():
    p = ROOT / 'brand-knowledge-base.json'
    if not p.exists():
        return
    t = p.read_text(encoding='utf-8')
    # Replace vague address with specific
    old_addr = '"address": "浙江省义乌市"'
    new_addr = '"address": "浙江省义乌市商城大道188号 邮编322000 (NO.188 Shangcheng Ave, Yiwu, Zhejiang 322000, China)"'
    if old_addr in t:
        t = t.replace(old_addr, new_addr)
        p.write_text(t, encoding='utf-8')
        print(f"[FIXED] brand-knowledge-base.json: address")
    else:
        print(f"[SKIP ] brand-knowledge-base.json: address already updated or pattern mismatch")


# ---------- 4. Fix faq-knowledge-base.json ----------
def fix_faq_kb():
    p = ROOT / 'faq-knowledge-base.json'
    if not p.exists():
        return
    t = p.read_text(encoding='utf-8')
    changed = False
    # Check for vague address patterns
    if '"浙江省义乌市"' in t and '商城大道' not in t:
        t = t.replace(
            '"浙江省义乌市"',
            '"浙江省义乌市商城大道188号 邮编322000 (NO.188 Shangcheng Ave, Yiwu, Zhejiang 322000, China)"'
        )
        changed = True
    if changed:
        p.write_text(t, encoding='utf-8')
        print(f"[FIXED] faq-knowledge-base.json: address")
    else:
        print(f"[SKIP ] faq-knowledge-base.json: no changes needed")


# ---------- 5. Fix llms-full.txt registered address ----------
def fix_llms_full():
    p = ROOT / 'llms-full.txt'
    if not p.exists():
        return
    t = p.read_text(encoding='utf-8')
    old = 'Registered address: Yiwu International Trade City, Yiwu, Zhejiang Province 322000, China'
    new = 'Registered address: NO.188 Shangcheng Ave, Yiwu, Zhejiang 322000, China'
    if old in t:
        t = t.replace(old, new)
        p.write_text(t, encoding='utf-8')
        print(f"[FIXED] llms-full.txt: registered address")
    else:
        print(f"[SKIP ] llms-full.txt: address already updated")


# ---------- 6. Fix page-data.json ----------
def fix_page_data():
    p = ROOT / 'page-data.json'
    if not p.exists():
        return
    t = p.read_text(encoding='utf-8')
    old = '"address": "Yiwu City, Zhejiang Province, China"'
    new = '"address": "NO.188 Shangcheng Ave, Yiwu, Zhejiang 322000, China"'
    if old in t:
        t = t.replace(old, new)
        p.write_text(t, encoding='utf-8')
        print(f"[FIXED] page-data.json: address")
    else:
        print(f"[SKIP ] page-data.json: address pattern not found, checking alternatives...")
        # Try Chinese
        old2 = '"Yiwu City, Zhejiang Province, China"'
        if old2 in t:
            t = t.replace(old2, new)
            p.write_text(t, encoding='utf-8')
            print(f"[FIXED] page-data.json: address (alt)")


# ---------- 7. Fix payment.html address (add postal code) ----------
def fix_payment_address():
    p = ROOT / 'payment.html'
    if not p.exists():
        return
    t = p.read_text(encoding='utf-8')
    old = '<td>NO.188, Shangcheng Avenue, Yiwu, Zhejiang Province</td>'
    new = '<td>NO.188 Shangcheng Ave, Yiwu, Zhejiang 322000, China</td>'
    if old in t:
        t = t.replace(old, new)
        p.write_text(t, encoding='utf-8')
        print(f"[FIXED] payment.html: address postal code")
    else:
        print(f"[SKIP ] payment.html: address pattern not found")


# ---------- 8. Check ALL pages for remaining copyright "© 2026 Yeatru Sourcing" without full legal name ----------
def fix_remaining_copyright():
    for f in HTML_FILES:
        t = f.read_text(encoding='utf-8')
        orig = t
        # Pattern 1: plain "© 2026 Yeatru Sourcing"
        t = t.replace(
            '&copy; 2026 Yeatru Sourcing.',
            '&copy; 2022–2026 义乌市弋楚贸易有限公司 · Yeatru Sourcing (YIWU ETRUE TRADING CO., LTD.).'
        )
        # Pattern 2: "Copyright 2026 Yeatru Sourcing" or similar
        t = re.sub(
            r'&copy;\s*2026\s+Yeatru\s+Sourcing\b',
            '&copy; 2022–2026 义乌市弋楚贸易有限公司 · Yeatru Sourcing (YIWU ETRUE TRADING CO., LTD.)',
            t
        )
        if t != orig:
            f.write_text(t, encoding='utf-8')
            print(f"[FIXED] {f.name}: copyright")


# ---------- Main ----------
def main():
    print("=" * 60)
    print("Site Consistency Fix - Pass 3")
    print("=" * 60)
    fix_product_sourcing()
    fix_all_schema_addresses()
    fix_brand_kb()
    fix_faq_kb()
    fix_llms_full()
    fix_page_data()
    fix_payment_address()
    fix_remaining_copyright()
    print("=" * 60)
    print("Pass 3 complete.")
    print("=" * 60)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Pass 4: Fix remaining footer consistency issues.

Fixes:
1. product-sourcing.html: "NDA</a>" → "NDA & Confidentiality</a>"
2. 404.html, data.html, monitor.html: add legal links (Privacy/Terms/Refund/NDA) to copyright line
3. Process any other pages with similar "lightweight footer" patterns
"""
from pathlib import Path

ROOT = Path('/workspace')


def fix_product_sourcing_nda_name():
    p = ROOT / 'product-sourcing.html'
    if not p.exists():
        return
    t = p.read_text(encoding='utf-8')
    old = '<a href="nda.html" class="footer-link d-inline">NDA</a>'
    new = '<a href="nda.html" class="footer-link d-inline">NDA &amp; Confidentiality</a>'
    if old in t:
        t = t.replace(old, new)
        p.write_text(t, encoding='utf-8')
        print(f"[FIXED] product-sourcing.html: NDA → NDA & Confidentiality")
    else:
        print(f"[SKIP ] product-sourcing.html: NDA naming pattern not found")


def fix_lightweight_footer(page_name: str):
    """For pages that have copyright line but NO legal links after it."""
    p = ROOT / f'{page_name}.html'
    if not p.exists():
        print(f"[SKIP ] {page_name}.html: file not found")
        return
    t = p.read_text(encoding='utf-8')
    orig = t

    # Pattern: the standard copyright sentence ending with "All rights reserved.</p>"
    # but missing the | Privacy | Terms | Refund | NDA part after it
    old_copyright = (
        '<p>&copy; 2022–2026 义乌市弋楚贸易有限公司 · Yeatru Sourcing '
        '(YIWU ETRUE TRADING CO., LTD.). All rights reserved.</p>'
    )
    new_copyright = (
        '<p>&copy; 2022–2026 义乌市弋楚贸易有限公司 · Yeatru Sourcing '
        '(YIWU ETRUE TRADING CO., LTD.). All rights reserved. |\n'
        '                    <a href="privacy.html" class="footer-link d-inline" style="color: #ccc; text-decoration: none;">Privacy Policy</a> |\n'
        '                    <a href="terms.html" class="footer-link d-inline" style="color: #ccc; text-decoration: none;">Terms of Service</a> |\n'
        '                    <a href="refund.html" class="footer-link d-inline" style="color: #ccc; text-decoration: none;">Refund Policy</a> |\n'
        '                    <a href="nda.html" class="footer-link d-inline" style="color: #ccc; text-decoration: none;">NDA &amp; Confidentiality</a>\n'
        '                </p>'
    )

    if old_copyright in t:
        t = t.replace(old_copyright, new_copyright)
        changed = True
    else:
        changed = False
        # Try monitor.html style (simpler footer)
        if page_name == 'monitor':
            old_monitor = '<p>Yeatru Sourcing SEO Monitor &mdash; <a href="https://www.yeatru.com/">yeatru.com</a></p>'
            new_monitor = (
                '<p>Yeatru Sourcing SEO Monitor &mdash; <a href="https://www.yeatru.com/">yeatru.com</a></p>\n'
                '            <p style="margin-top:6px; font-size: 0.85rem; opacity: 0.85;">'
                '&copy; 2022–2026 义乌市弋楚贸易有限公司 · Yeatru Sourcing (YIWU ETRUE TRADING CO., LTD.). All rights reserved. | '
                '<a href="privacy.html" style="color: #ccc; text-decoration: none;">Privacy</a> | '
                '<a href="terms.html" style="color: #ccc; text-decoration: none;">Terms</a> | '
                '<a href="refund.html" style="color: #ccc; text-decoration: none;">Refund</a> | '
                '<a href="nda.html" style="color: #ccc; text-decoration: none;">NDA</a>'
                '</p>'
            )
            if old_monitor in t:
                t = t.replace(old_monitor, new_monitor)
                changed = True

    if changed:
        p.write_text(t, encoding='utf-8')
        print(f"[FIXED] {page_name}.html: added legal links to footer")
    else:
        print(f"[SKIP ] {page_name}.html: footer pattern not matched")


def main():
    print("=" * 60)
    print("Site Consistency Fix - Pass 4")
    print("=" * 60)
    fix_product_sourcing_nda_name()
    for page in ['404', 'data', 'monitor']:
        fix_lightweight_footer(page)
    print("=" * 60)
    print("Pass 4 complete.")
    print("=" * 60)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Pass 5: Fix remaining footer legal links warnings.

Fixes:
1. testimonials.html: Add Privacy/Terms/Refund/NDA links to copyright line
2. process.html / services.html (redirect pages): Add simple legal links
3. googlec23c18b1ca57e814.html is a Google verification file, skip
"""
from pathlib import Path

ROOT = Path('/workspace')


def fix_testimonials():
    p = ROOT / 'testimonials.html'
    if not p.exists():
        return
    t = p.read_text(encoding='utf-8')
    old = (
        '<p class="mb-0 small text-muted">&copy; 2022–2026 义乌市弋楚贸易有限公司 · Yeatru Sourcing '
        '(YIWU ETRUE TRADING CO., LTD.). All rights reserved.</p>'
    )
    new = (
        '<p class="mb-0 small text-muted">&copy; 2022–2026 义乌市弋楚贸易有限公司 · Yeatru Sourcing '
        '(YIWU ETRUE TRADING CO., LTD.). All rights reserved. |\n'
        '                    <a href="privacy.html" style="color: #ccc; text-decoration: none;">Privacy</a> |\n'
        '                    <a href="terms.html" style="color: #ccc; text-decoration: none;">Terms</a> |\n'
        '                    <a href="refund.html" style="color: #ccc; text-decoration: none;">Refund</a> |\n'
        '                    <a href="nda.html" style="color: #ccc; text-decoration: none;">NDA</a>\n'
        '                </p>'
    )
    if old in t:
        t = t.replace(old, new)
        p.write_text(t, encoding='utf-8')
        print(f"[FIXED] testimonials.html: added legal links to copyright line")
    else:
        print(f"[SKIP ] testimonials.html: copyright pattern not found (already fixed?)")


def fix_redirect_page(name: str):
    """Add simple legal links footer to redirect/noindex pages."""
    p = ROOT / f'{name}.html'
    if not p.exists():
        print(f"[SKIP ] {name}.html: file not found")
        return
    t = p.read_text(encoding='utf-8')
    orig = t

    # Insert a simple footer with legal links before </body>
    legal_footer = '''
    <footer style="margin-top: 40px; padding: 20px; text-align: center; font-size: 0.8rem; color: #888;">
        <p>&copy; 2022–2026 义乌市弋楚贸易有限公司 · Yeatru Sourcing (YIWU ETRUE TRADING CO., LTD.). All rights reserved.<br>
        <a href="privacy.html" style="color: #888; margin: 0 5px;">Privacy</a> |
        <a href="terms.html" style="color: #888; margin: 0 5px;">Terms</a> |
        <a href="refund.html" style="color: #888; margin: 0 5px;">Refund</a> |
        <a href="nda.html" style="color: #888; margin: 0 5px;">NDA</a></p>
    </footer>
'''
    if '</body>' in t and legal_footer.strip().split('\n')[1].strip() not in t:
        t = t.replace('</body>', legal_footer + '</body>')
        p.write_text(t, encoding='utf-8')
        print(f"[FIXED] {name}.html: added legal footer")
    elif orig == t:
        print(f"[SKIP ] {name}.html: already has legal footer or </body> not found")
    else:
        p.write_text(t, encoding='utf-8')


def main():
    print("=" * 60)
    print("Site Consistency Fix - Pass 5")
    print("=" * 60)
    fix_testimonials()
    for page in ['process', 'services']:
        fix_redirect_page(page)
    print("=" * 60)
    print("Pass 5 complete.")
    print("=" * 60)


if __name__ == '__main__':
    main()

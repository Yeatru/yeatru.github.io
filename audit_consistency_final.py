#!/usr/bin/env python3
"""Final site-wide consistency validation audit.

Checks ALL core fields for contradictions across all files.
Prints a PASS/FAIL report with detailed findings.
"""
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path('/workspace')

# ---------- STANDARD / TRUTH VALUES ----------
STANDARD = {
    "founder_name": ["Neil Liu"],  # ONLY this is allowed
    "founder_banned": ["Megan Mei", "Neil Wang", "megan mei", "neil wang"],
    "company_zh": "义乌市弋楚贸易有限公司",
    "company_en_legal": "YIWU ETRUE TRADING CO., LTD.",
    "company_en_alt": "Yiwu Yichu Trading Co., Ltd.",
    "brand_name": "Yeatru Sourcing",
    "founded_year": 2022,  # Company registration year
    "banned_founded": ["since 2012", "founded in 2012", "established 2012"],
    "address_full": "NO.188 Shangcheng Ave",  # must appear in all schema/footer addresses
    "address_banned_vague": ["Yiwu International Trade City"],  # in schema streetAddress
    "copyright_full_regex": r"&copy;\s*2022–2026\s*义乌市弋楚贸易有限公司",
    "copyright_banned_old": [r"&copy;\s*2026\s+Yeatru\s+Sourcing\b(?!.*义乌市弋楚贸易)"],
    "phone": ["+86 159 8851 6408", "+8615988516408"],
    "email": "info@yeatru.com",
    "legal_links": ["privacy.html", "terms.html", "refund.html", "nda.html"],
}

# Pages that are INTERNAL / TOOLS and don't need strict full compliance (but still checked)
TOOL_PAGES = {"monitor.html"}

HTML_FILES = sorted([p for p in ROOT.glob('*.html')])
JSON_FILES = sorted([p for p in ROOT.glob('*.json')])
TXT_FILES = sorted([p for p in ROOT.glob('*.txt')])
JS_FILES = sorted([p for p in ROOT.glob('*.js')])


def check_banned_patterns(file_path: Path, text: str, findings: dict):
    """Check for banned patterns like wrong founder names, wrong founding year."""
    fname = file_path.name

    # Wrong founder names
    for banned in STANDARD["founder_banned"]:
        if banned.lower() in text.lower():
            # Case-insensitive search, report exact line
            for i, line in enumerate(text.splitlines(), 1):
                if banned.lower() in line.lower():
                    findings["errors"].append(f"❌ {fname}:{i} — BANNED founder name '{banned}' found: {line.strip()[:120]}")
                    break

    # Wrong founding year (since 2012 etc.)
    for banned in STANDARD["banned_founded"]:
        if banned.lower() in text.lower():
            for i, line in enumerate(text.splitlines(), 1):
                if banned.lower() in line.lower():
                    findings["warnings"].append(f"⚠️ {fname}:{i} — POSSIBLE wrong founding year phrase '{banned}': {line.strip()[:120]}")
                    break


def check_html_footer(file_path: Path, text: str, findings: dict):
    """Check HTML footer: copyright, legal links."""
    fname = file_path.name
    if fname in TOOL_PAGES:
        strict = False
    else:
        strict = True

    # Copyright regex check
    if not re.search(STANDARD["copyright_full_regex"], text):
        # Check if there's any copyright at all
        if re.search(r"&copy;", text):
            msg = f"⚠️ {fname} — Copyright does not match full legal format (2022–2026 + 义乌市弋楚贸易有限公司)"
            if strict:
                findings["warnings"].append(msg + " (strict page)")
            else:
                findings["info"].append(msg + " (tool/light page)")

    # Legal links check (only for non-tooling strict pages)
    if strict:
        footer_match = re.search(r'<footer[\s\S]*?</footer>', text, re.IGNORECASE)
        footer_text = footer_match.group(0) if footer_match else text
        missing_links = []
        for link in STANDARD["legal_links"]:
            # Look for href="link" in footer
            if not re.search(r'href\s*=\s*["\']' + re.escape(link) + r'["\']', footer_text):
                missing_links.append(link)
        if missing_links and fname != 'monitor.html':
            # For pages like privacy/terms/refund/nda, self-links are OK
            findings["warnings"].append(f"⚠️ {fname} — Footer MISSING legal links: {', '.join(missing_links)}")


def check_schema_address(file_path: Path, text: str, findings: dict):
    """Check schema.org PostalAddress streetAddress."""
    fname = file_path.name
    # Find all schema streetAddress values
    schema_matches = re.findall(r'"streetAddress"\s*:\s*"([^"]+)"', text)
    for addr in schema_matches:
        for banned in STANDARD["address_banned_vague"]:
            if banned.lower() in addr.lower():
                findings["errors"].append(f"❌ {fname} — Schema streetAddress is VAGUE: \"{addr}\" should include NO.188 Shangcheng Ave")


def check_company_names(file_path: Path, text: str, findings: dict):
    """Check for wrong company name variants."""
    fname = file_path.name
    # Check for any GUOCHU references (old wrong name)
    if re.search(r'GUOCHU|Guochu|guochu|国楚', text):
        for i, line in enumerate(text.splitlines(), 1):
            if re.search(r'GUOCHU|Guochu|guochu|国楚', line):
                findings["errors"].append(f"❌ {fname}:{i} — BANNED company name variant: {line.strip()[:120]}")
                break


def run_audit():
    findings = {
        "errors": [],
        "warnings": [],
        "info": [],
    }
    all_files = HTML_FILES + JSON_FILES + TXT_FILES + JS_FILES

    for fp in all_files:
        try:
            text = fp.read_text(encoding='utf-8')
        except Exception:
            continue

        check_banned_patterns(fp, text, findings)
        check_company_names(fp, text, findings)
        if fp.suffix == '.html':
            check_html_footer(fp, text, findings)
            check_schema_address(fp, text, findings)

    return findings


def print_report(findings):
    print()
    print("=" * 72)
    print("         YEATRU SITE CONSISTENCY AUDIT — FINAL REPORT")
    print("=" * 72)

    errors = findings["errors"]
    warnings = findings["warnings"]
    info = findings["info"]

    # Summary
    total_issues = len(errors) + len(warnings)
    status = "✅ PASS (minor info only)" if total_issues == 0 else "⚠️ PASS WITH ISSUES" if len(errors) == 0 else "❌ FAIL"
    print(f"\n  STATUS:  {status}")
    print(f"  ERRORS:  {len(errors)}  (contradictions / must fix)")
    print(f"  WARNING: {len(warnings)}  (inconsistencies / recommended)")
    print(f"  INFO:    {len(info)}  (notes)")
    print()

    if errors:
        print("-" * 72)
        print("  ERRORS (must fix):")
        print("-" * 72)
        for e in errors:
            print(f"  {e}")
        print()

    if warnings:
        print("-" * 72)
        print("  WARNINGS (recommended fixes):")
        print("-" * 72)
        for w in warnings:
            print(f"  {w}")
        print()

    if info:
        print("-" * 72)
        print("  INFO:")
        print("-" * 72)
        for i in info:
            print(f"  {i}")
        print()

    # Standard reference
    print("=" * 72)
    print("  STANDARD REFERENCE VALUES (single source of truth):")
    print("=" * 72)
    print(f"  🏢 中文名:     {STANDARD['company_zh']}")
    print(f"  🏢 英文法定名: {STANDARD['company_en_legal']}")
    print(f"  🏢 英文拼音名: {STANDARD['company_en_alt']}")
    print(f"  🏷️ 品牌名:      {STANDARD['brand_name']}")
    print(f"  👤 创始人:      {STANDARD['founder_name'][0]}")
    print(f"  📅 公司注册:    {STANDARD['founded_year']}年")
    print(f"  📅 团队经验:    14+ years combined team experience")
    print(f"  📍 地址:        NO.188 Shangcheng Ave, Yiwu, Zhejiang 322000, China")
    print(f"  📞 电话:        +86 159 8851 6408")
    print(f"  📧 邮箱:        {STANDARD['email']}")
    print(f"  ⚖️  法律页:      privacy.html / terms.html / refund.html / nda.html")
    print(f"  ©️ 版权:         © 2022–2026 义乌市弋楚贸易有限公司 · Yeatru Sourcing (YIWU ETRUE TRADING CO., LTD.)")
    print("=" * 72)

    return len(errors) == 0


if __name__ == '__main__':
    findings = run_audit()
    ok = print_report(findings)
    exit(0 if ok else 1)

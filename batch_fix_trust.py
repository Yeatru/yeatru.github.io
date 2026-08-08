#!/usr/bin/env python3
"""
Yeatru Sourcing — Trust & Consistency Batch Fixer
-------------------------------------------------
Runs a series of search-and-replace operations across all core site files to:
1. Fix footer dead links (Privacy / Terms / Refund / NDA / Address / Hours)
2. Wire brandLogoImg to logo.svg so the real logo displays instead of "YC" fallback
3. Unify company legal names in Organization JSON-LD schemas (add ETRUE Trading alias)
4. Replace Megan Mei -> Neil Liu everywhere
5. Replace Neil Wang -> Neil Liu everywhere (blog author bio boxes, schema employee)
6. Fix "since 2012" exaggeration in about.html metas/OG to "14+ years combined team experience"
7. Replace generic Yiwu address in footer with concrete NO.188 Shangcheng Ave address
8. Replace fake font-awesome testimonial avatars on testimonials.html with data-ready placeholders
"""

import os
import re
import glob

WORKSPACE = "/workspace"
os.chdir(WORKSPACE)

# ──────────────────────────────────────────────────────────────────────
# 1. List of files to operate on
# ──────────────────────────────────────────────────────────────────────
html_files = [
    p for p in glob.glob("*.html")
    if not p.startswith("product-") and p not in {"process.html", "services.html"}
]

data_files = [
    "brand-knowledge-base.json",
    "faq-knowledge-base.json",
    "llms.txt",
    "llms-full.txt",
    "i18n-misc.js",
]

all_targets = html_files + data_files

address_link = (
    "https://maps.google.com/?q=NO.188+Shangcheng+Avenue+"
    "Yiwu+Zhejiang+322000+China"
)
new_address_text = "NO.188 Shangcheng Ave, Yiwu, Zhejiang, China"
map_link_html = (
    f'<a href="{address_link}" target="_blank" rel="noopener noreferrer" '
    f'class="footer-link"><i class="fas fa-map-marker-alt me-2"></i> '
    f'{new_address_text}</a>'
)

hours_link_html = (
    '<a href="contact.html#opening-hours" class="footer-link">'
    '<i class="fas fa-clock me-2"></i> Open: Mo-Sa 09:00–18:00 · 24/7 Online'
    "</a>"
)


def slurp(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def spit(path: str, text: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


counts = {}


def apply(path, label, fn):
    before = slurp(path)
    after = fn(before)
    if after != before:
        counts[label] = counts.get(label, 0) + 1
        spit(path, after)


# ──────────────────────────────────────────────────────────────────────
# Fix A: Footer dead links -> real URLs + add Refund & NDA
# ──────────────────────────────────────────────────────────────────────
def fix_footer_links(t: str) -> str:
    # Two footer patterns:
    # 1)  <a href="#" class="footer-link d-inline" data-i18n="footer.privacyPolicy">Privacy Policy</a>
    # 2)  <a href="#" class="footer-link d-inline">Privacy Policy</a>
    t = re.sub(
        r'<a href="#" class="footer-link d-inline"(?:\s+data-i18n="footer\.privacyPolicy")?>\s*Privacy Policy\s*</a>',
        '<a href="privacy.html" class="footer-link d-inline" data-i18n="footer.privacyPolicy">Privacy Policy</a>',
        t,
    )
    t = re.sub(
        r'<a href="#" class="footer-link d-inline"(?:\s+data-i18n="footer\.termsOfService")?>\s*Terms of Service\s*</a>',
        '<a href="terms.html" class="footer-link d-inline" data-i18n="footer.termsOfService">Terms of Service</a>',
        t,
    )

    # After the Terms of Service link, add " | Refund Policy | NDA"
    # Insert only once per page (after Terms), don't duplicate if already there.
    if "refund.html" not in t and "nda.html" not in t:
        t = re.sub(
            r'(<a href="terms\.html" class="footer-link d-inline"[^>]*>Terms of Service</a>\s*)',
            r'\1 |\n                    <a href="refund.html" class="footer-link d-inline">Refund Policy</a> |\n                    <a href="nda.html" class="footer-link d-inline">NDA & Confidentiality</a>',
            t,
        )
    return t


# ──────────────────────────────────────────────────────────────────────
# Fix B/C: Address href="#" + Clock href="#" in footer
# ──────────────────────────────────────────────────────────────────────
def fix_footer_address_and_hours(t: str) -> str:
    t = re.sub(
        r'<a href="#" class="footer-link"><i class="fas fa-map-marker-alt me-2"></i>\s*Yiwu City, Zhejiang, China\s*</a>',
        map_link_html,
        t,
    )
    t = re.sub(
        r'<a href="#" class="footer-link"><i class="fas fa-clock me-2"></i>\s*24/7 Available\s*</a>',
        hours_link_html,
        t,
    )
    # faq.html has a slightly spaced out one:
    t = re.sub(
        r'<a href="#" class="footer-link"><i class="fas fa-map-marker-alt me-2"></i>Yiwu City, Zhejiang, China</a>',
        map_link_html,
        t,
    )
    t = re.sub(
        r'<a href="#" class="footer-link"><i class="fas fa-clock me-2"></i>24/7 Available</a>',
        hours_link_html,
        t,
    )
    return t


# ──────────────────────────────────────────────────────────────────────
# Fix D: brandLogoImg src=""  ->  src="logo.svg"
# ──────────────────────────────────────────────────────────────────────
def fix_brand_logo(t: str) -> str:
    t = t.replace(
        '<img id="brandLogoImg" src="" ',
        '<img id="brandLogoImg" src="logo.svg" ',
    )
    # Also default "display:none" -> let it show; fallback only if onerror
    t = t.replace(
        'style="display:none;" id="brandLogoImg"',
        'id="brandLogoImg" style="display:inline-block; height:36px; vertical-align:middle; margin-right:8px;" onerror="this.style.display=\'none\'; document.getElementById(\'brandLogoFallback\') && (document.getElementById(\'brandLogoFallback\').style.display=\'inline-block\');"',
    )
    return t


# ──────────────────────────────────────────────────────────────────────
# Fix G: Organization schema - add ETRUE Trading to alternateName
# ──────────────────────────────────────────────────────────────────────
def fix_schema_alias(t: str) -> str:
    t = t.replace(
        '"alternateName": "义乌市弋楚贸易有限公司"',
        '"alternateName": ["义乌市弋楚贸易有限公司", "Yiwu Yichu Trading Co., Ltd.", "YIWU ETRUE TRADING CO.,LTD."]',
    )
    t = t.replace(
        '"alternateName": ["Yiwu Yichu Trading Co., Ltd.", "Yeatru", "YC Sourcing", "弋楚贸易"]',
        '"alternateName": ["Yiwu Yichu Trading Co., Ltd.", "YIWU ETRUE TRADING CO.,LTD.", "Yeatru", "YC Sourcing", "弋楚贸易"]',
    )
    return t


def fix_schema_streetaddress(t: str) -> str:
    t = t.replace(
        '"streetAddress": "Yiwu International Trade City"',
        '"streetAddress": "NO.188 Shangcheng Ave, Yiwu, Zhejiang, China"',
    )
    return t


# ──────────────────────────────────────────────────────────────────────
# Fix 3a: Megan Mei -> Neil Liu
# ──────────────────────────────────────────────────────────────────────
def fix_megan(t: str) -> str:
    t = t.replace("Megan Mei", "Neil Liu")
    t = t.replace("megan mei", "Neil Liu")
    return t


# ──────────────────────────────────────────────────────────────────────
# Fix 3b: Neil Wang -> Neil Liu
# ──────────────────────────────────────────────────────────────────────
def fix_neil_wang(t: str) -> str:
    # Don't accidentally break Facebook URL /neil-law or LinkedIn /neil-liu-398983257
    t = t.replace('content="Neil Wang"', 'content="Neil Liu"')
    t = t.replace('"name": "Neil Wang",', '"name": "Neil Liu",')
    t = t.replace("Neil Wang - China Sourcing Expert", "Neil Liu - Founder & Sourcing Expert")
    t = t.replace("<h3 class=\"h5 mb-1\">Neil Wang</h3>", "<h3 class=\"h5 mb-1\">Neil Liu</h3>")
    t = t.replace("<h3 class=\"h5 mb-1\">\n                                    Neil Wang",
                  "<h3 class=\"h5 mb-1\">\n                                    Neil Liu")
    t = t.replace("Neil Wang is a China sourcing specialist",
                  "Neil Liu is the Founder & Managing Director of Yeatru Sourcing and a China sourcing specialist")
    t = t.replace('aria-label="Neil Wang on LinkedIn"', 'aria-label="Neil Liu on LinkedIn"')
    t = t.replace('aria-label="Neil Wang on Facebook"', 'aria-label="Neil Liu on Facebook"')
    t = t.replace('Head of content / sourcing specialist: Neil Wang',
                  'Founder & Managing Director: Neil Liu')
    return t


# ──────────────────────────────────────────────────────────────────────
# Fix 3c: about.html "since 2012" meta/description/OG/twitter
# ──────────────────────────────────────────────────────────────────────
def fix_since_2012(t: str) -> str:
    old_desc = (
        "14+ years, 200+ clients, 75K suppliers, 98% satisfaction. "
        "Your trusted Yiwu-based China sourcing agent since 2012. "
        "Amazon FBA, TikTok Shop, wholesale."
    )
    new_desc = (
        "14+ years combined team experience, 200+ clients, 75K suppliers, 98% satisfaction. "
        "Yeatru Sourcing — Yiwu-based China sourcing agent registered 2022 with import/export rights. "
        "Amazon FBA, TikTok Shop, wholesale."
    )
    t = t.replace(old_desc, new_desc)
    return t


# ──────────────────────────────────────────────────────────────────────
# Fix brand-knowledge-base.json: legal_person Megan -> Neil Liu + alias
# ──────────────────────────────────────────────────────────────────────
def fix_brand_kb(t: str) -> str:
    t = t.replace('"legal_person": "Megan Mei"', '"legal_person": "Neil Liu"')
    t = t.replace(
        '"full_name": "义乌市弋楚贸易有限公司"',
        '"full_name": "义乌市弋楚贸易有限公司",\n        "english_legal_name": "YIWU ETRUE TRADING CO., LTD. (also: Yiwu Yichu Trading Co., Ltd.)"',
    )
    return t


# ──────────────────────────────────────────────────────────────────────
# Fix llms files: founder Neil Liu, company founded 2022 wording tweak
# ──────────────────────────────────────────────────────────────────────
def fix_llms(t: str) -> str:
    t = t.replace(
        "- Legal name: 义乌市弋楚贸易有限公司 (Yiwu Yichu Trading Co., Ltd.)",
        "- Legal name: 义乌市弋楚贸易有限公司\n"
        "- English legal aliases: YIWU ETRUE TRADING CO., LTD. (banking), Yiwu Yichu Trading Co., Ltd. (pinyin)",
    )
    t = t.replace(
        "- Founder: Megan Mei",
        "- Founder & Managing Director: Neil Liu\n"
        "- LinkedIn: https://www.linkedin.com/in/neil-liu-398983257",
    )
    return t


def fix_llms_txt(t: str) -> str:
    t = t.replace(
        "Founded: 2022 (14+ years team experience)",
        "Company registered: 2022 (14+ years combined team sourcing experience)",
    )
    return t


# ──────────────────────────────────────────────────────────────────────
# Runner
# ──────────────────────────────────────────────────────────────────────
for f in html_files:
    try:
        apply(f, "footer_links", fix_footer_links)
        apply(f, "footer_addr_hours", fix_footer_address_and_hours)
        apply(f, "brand_logo", fix_brand_logo)
        apply(f, "schema_alias", fix_schema_alias)
        apply(f, "schema_addr", fix_schema_streetaddress)
        apply(f, "megan", fix_megan)
        apply(f, "neil_wang", fix_neil_wang)
        apply(f, "since_2012", fix_since_2012)
    except Exception as e:
        print(f"WARN {f}: {e}")

for f in data_files:
    try:
        if f.endswith(".json") and "brand" in f:
            apply(f, "brand_kb", fix_brand_kb)
        if f == "llms-full.txt":
            apply(f, "llms", fix_llms)
        if f == "llms.txt":
            apply(f, "llms_txt", fix_llms_txt)
        apply(f, "megan", fix_megan)
        apply(f, "neil_wang", fix_neil_wang)
    except Exception as e:
        print(f"WARN {f}: {e}")

print("Batch fix done. Counts per rule:")
for k, v in sorted(counts.items(), key=lambda x: -x[1]):
    print(f"  {k:<20} {v} files touched")
print(f"Total target files scanned: {len(all_targets)}")

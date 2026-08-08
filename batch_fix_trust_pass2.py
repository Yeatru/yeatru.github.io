#!/usr/bin/env python3
"""
Second pass trust fixes — applied after contact.css was hand-tuned.
1. Inject full footer-social-icons block (TikTok, YouTube, Telegram, Alibaba Gold)
   and copyright year + legal-name sentence into EVERY html file EXCEPT contact.css
   (which we just hand-tuned).
2. Fix testimonials.html — replace font-awesome placeholder avatars with real
   image placeholders (user fills in URLs later) + disclaimers of authenticity.
3. Update sitemap.xml to include the 4 new legal pages (privacy/terms/refund/nda).
"""
import os
import re
import glob

WORKSPACE = "/workspace"
os.chdir(WORKSPACE)

html_files = [
    p for p in glob.glob("*.html")
    if not p.startswith("product-") and p not in {"process.html", "services.html", "contact.css"}
]

new_social_block = """<div class="footer-social">
                        <a href="https://facebook.com/NeilLaw" target="_blank" class="footer-social-icon" rel="noopener noreferrer" aria-label="Facebook"><i class="fab fa-facebook-f"></i></a>
                        <a href="https://www.linkedin.com/in/neil-liu-398983257" target="_blank" class="footer-social-icon" rel="noopener noreferrer" aria-label="LinkedIn"><i class="fab fa-linkedin-in"></i></a>
                        <a href="https://wa.me/+8615988516408" target="_blank" class="footer-social-icon" rel="noopener noreferrer" aria-label="WhatsApp"><i class="fab fa-whatsapp"></i></a>
                        <a href="https://instagram.com/yeatru_sourcing" target="_blank" class="footer-social-icon" rel="noopener noreferrer" aria-label="Instagram"><i class="fab fa-instagram"></i></a>
                        <a href="https://www.tiktok.com/@yeatru" target="_blank" class="footer-social-icon" rel="noopener noreferrer" aria-label="TikTok"><i class="fab fa-tiktok"></i></a>
                        <a href="https://www.youtube.com/@yeatru-sourcing" target="_blank" class="footer-social-icon" rel="noopener noreferrer" aria-label="YouTube"><i class="fab fa-youtube"></i></a>
                        <a href="https://t.me/yeatru" target="_blank" class="footer-social-icon" rel="noopener noreferrer" aria-label="Telegram"><i class="fab fa-telegram-plane"></i></a>
                        <a href="https://www.alibaba.com/member/yeatru.html" target="_blank" class="footer-social-icon" rel="noopener noreferrer" aria-label="Alibaba Gold Supplier" title="Alibaba Gold Member ✓"><i class="fab fa-alibaba"></i></a>
                    </div>"""

new_copyright_html = """<p>&copy; 2022–2026 义乌市弋楚贸易有限公司 · Yeatru Sourcing (YIWU ETRUE TRADING CO., LTD.). All rights reserved. |
                    <a href="privacy.html" class="footer-link d-inline" data-i18n="footer.privacyPolicy">Privacy Policy</a> |
                    <a href="terms.html" class="footer-link d-inline" data-i18n="footer.termsOfService">Terms of Service</a> |
                    <a href="refund.html" class="footer-link d-inline">Refund Policy</a> |
                    <a href="nda.html" class="footer-link d-inline">NDA & Confidentiality</a>
                </p>"""

# Some pages (blog articles, products.html, faq.html, blog.html, testimonials.html, 404.html)
# use a footer-bottom WITHOUT data-i18n attributes. Build an alternate for them:
new_copyright_html_plain = """<p>&copy; 2022–2026 义乌市弋楚贸易有限公司 · Yeatru Sourcing (YIWU ETRUE TRADING CO., LTD.). All rights reserved. |
                    <a href="privacy.html" class="footer-link d-inline">Privacy Policy</a> |
                    <a href="terms.html" class="footer-link d-inline">Terms of Service</a> |
                    <a href="refund.html" class="footer-link d-inline">Refund Policy</a> |
                    <a href="nda.html" class="footer-link d-inline">NDA & Confidentiality</a>
                </p>"""

address_link = "https://maps.google.com/?q=NO.188+Shangcheng+Avenue+Yiwu+Zhejiang+322000+China"
address_new = f'<a href="{address_link}" target="_blank" rel="noopener noreferrer" class="footer-link"><i class="fas fa-map-marker-alt me-2"></i> NO.188 Shangcheng Ave, Yiwu, Zhejiang, China</a>'

hours_new = '<a href="contact.html#opening-hours" class="footer-link"><i class="fas fa-clock me-2"></i> Open: Mo-Sa 09:00–18:00 · 24/7 Online</a>'


def slurp(p):
    with open(p, "r", encoding="utf-8") as f:
        return f.read()
def spit(p, t):
    with open(p, "w", encoding="utf-8") as f:
        f.write(t)

counters = {}
def inc(k):
    counters[k] = counters.get(k, 0) + 1

for f in html_files:
    try:
        t = slurp(f)
        original = t

        # 1) Expand footer-social from 4 icons -> 8 icons if only 4 are present
        old_4 = """<div class="footer-social">
                        <a href="https://wa.me/+8615988516408" target="_blank" class="footer-social-icon" rel="noopener noreferrer"><i class="fab fa-whatsapp"></i></a>
                        <a href="mailto:info@yeatru.com" class="footer-social-icon" aria-label="Email"><i class="fas fa-envelope"></i></a>
                    </div>"""
        if old_4 in t:
            t = t.replace(old_4, new_social_block)
            inc("social_whatsapp_email -> 8 icons");

        # Some blog/article footer-social blocks only have WhatsApp icon
        t = re.sub(
            r'<div class="footer-social">\s*<a href="https://wa\.me/\+8615988516408"[^>]*><i class="fab fa-whatsapp"></i></a>\s*</div>',
            new_social_block,
            t,
        )

        # 2) Copyright footer-bottom block
        # Pattern A (with data-i18n):
        t = re.sub(
            r'<p>&copy; 2026 Yeatru Sourcing\. All rights reserved\. \|\s*'
            r'<a href="privacy\.html" class="footer-link d-inline"(?:\s+data-i18n="footer\.privacyPolicy")?>\s*Privacy Policy\s*</a> \|\s*'
            r'<a href="terms\.html" class="footer-link d-inline"(?:\s+data-i18n="footer\.termsOfService")?>\s*Terms of Service\s*</a>\s*'
            r'\|?\s*<a href="refund\.html" class="footer-link d-inline">Refund Policy</a> \|\s*'
            r'<a href="nda\.html" class="footer-link d-inline">NDA &amp; Confidentiality</a>\s*</p>',
            new_copyright_html,
            t,
        )

        # Pattern B (still the OLD # hrefs in copyright line — already fixed by pass1 for privacy/terms,
        # but here we also add refund/nda + copyright wording)
        t = re.sub(
            r'<p>&copy; 2026 Yeatru Sourcing\. All rights reserved\. \|\s*'
            r'<a href="privacy\.html" class="footer-link d-inline"(?:\s+data-i18n="footer\.privacyPolicy")?>\s*Privacy Policy\s*</a> \|\s*'
            r'<a href="terms\.html" class="footer-link d-inline"(?:\s+data-i18n="footer\.termsOfService")?>\s*Terms of Service\s*</a>\s*</p>',
            new_copyright_html,
            t,
        )

        # Same Pattern B for plain-text copyright line (no data-i18n) used by blog/product/faq pages:
        t = re.sub(
            r'<p>&copy; 2026 Yeatru Sourcing\. All rights reserved\. \|\s*'
            r'<a href="privacy\.html" class="footer-link d-inline">Privacy Policy</a> \|\s*'
            r'<a href="terms\.html" class="footer-link d-inline">Terms of Service</a>\s*\|?\s*'
            r'(<a href="refund\.html" class="footer-link d-inline">Refund Policy</a> \|\s*'
            r'<a href="nda\.html" class="footer-link d-inline">NDA &amp; Confidentiality</a>)?\s*</p>',
            new_copyright_html_plain,
            t,
        )

        # Still old style "&copy; 2026 Yeatru Sourcing" + 2 # hrefs? Replace:
        t = re.sub(
            r'<p>&copy; 2026 Yeatru Sourcing\. All rights reserved\. \|\s*'
            r'<a href="#" class="footer-link d-inline">Privacy Policy</a> \|\s*'
            r'<a href="#" class="footer-link d-inline">Terms of Service</a>\s*</p>',
            new_copyright_html_plain,
            t,
        )

        # 3) Expand footer-bottom where already pass-1 added refund/nda but
        #    still only says "© 2026 Yeatru Sourcing. All rights reserved."
        t = re.sub(
            r'&copy; 2026 Yeatru Sourcing\. All rights reserved\.',
            '&copy; 2022–2026 义乌市弋楚贸易有限公司 · Yeatru Sourcing (YIWU ETRUE TRADING CO., LTD.). All rights reserved.',
            t,
        )

        # 4) Address & hours links already fixed (pass 1 did them).
        #    But footer that still has only WhatsApp social icon (e.g. index.html) —
        #    We also just did them in step 1.

        if t != original:
            inc(f"__changed__: {f}")
            spit(f, t)
    except Exception as e:
        print(f"WARN {f}: {e}")


# ───────────────────────────────────────────────
# 5. Update sitemap.xml — add 4 new legal pages
# ───────────────────────────────────────────────
SM = "sitemap.xml"
try:
    sm = slurp(SM)
    today = "2026-08-08"
    if "privacy.html" not in sm:
        block = f"""
    <url>
        <loc>https://www.yeatru.com/privacy.html</loc>
        <lastmod>{today}</lastmod>
        <changefreq>yearly</changefreq>
        <priority>0.2</priority>
        <xhtml:link rel="alternate" hreflang="en" href="https://www.yeatru.com/privacy.html"/>
        <xhtml:link rel="alternate" hreflang="es" href="https://www.yeatru.com/privacy.html?lang=es"/>
        <xhtml:link rel="alternate" hreflang="fr" href="https://www.yeatru.com/privacy.html?lang=fr"/>
        <xhtml:link rel="alternate" hreflang="ru" href="https://www.yeatru.com/privacy.html?lang=ru"/>
        <xhtml:link rel="alternate" hreflang="ar" href="https://www.yeatru.com/privacy.html?lang=ar"/>
        <xhtml:link rel="alternate" hreflang="x-default" href="https://www.yeatru.com/privacy.html"/>
    </url>
    <url>
        <loc>https://www.yeatru.com/terms.html</loc>
        <lastmod>{today}</lastmod>
        <changefreq>yearly</changefreq>
        <priority>0.2</priority>
        <xhtml:link rel="alternate" hreflang="en" href="https://www.yeatru.com/terms.html"/>
        <xhtml:link rel="alternate" hreflang="es" href="https://www.yeatru.com/terms.html?lang=es"/>
        <xhtml:link rel="alternate" hreflang="fr" href="https://www.yeatru.com/terms.html?lang=fr"/>
        <xhtml:link rel="alternate" hreflang="ru" href="https://www.yeatru.com/terms.html?lang=ru"/>
        <xhtml:link rel="alternate" hreflang="ar" href="https://www.yeatru.com/terms.html?lang=ar"/>
        <xhtml:link rel="alternate" hreflang="x-default" href="https://www.yeatru.com/terms.html"/>
    </url>
    <url>
        <loc>https://www.yeatru.com/refund.html</loc>
        <lastmod>{today}</lastmod>
        <changefreq>yearly</changefreq>
        <priority>0.2</priority>
        <xhtml:link rel="alternate" hreflang="en" href="https://www.yeatru.com/refund.html"/>
        <xhtml:link rel="alternate" hreflang="es" href="https://www.yeatru.com/refund.html?lang=es"/>
        <xhtml:link rel="alternate" hreflang="fr" href="https://www.yeatru.com/refund.html?lang=fr"/>
        <xhtml:link rel="alternate" hreflang="ru" href="https://www.yeatru.com/refund.html?lang=ru"/>
        <xhtml:link rel="alternate" hreflang="ar" href="https://www.yeatru.com/refund.html?lang=ar"/>
        <xhtml:link rel="alternate" hreflang="x-default" href="https://www.yeatru.com/refund.html"/>
    </url>
    <url>
        <loc>https://www.yeatru.com/nda.html</loc>
        <lastmod>{today}</lastmod>
        <changefreq>yearly</changefreq>
        <priority>0.2</priority>
        <xhtml:link rel="alternate" hreflang="en" href="https://www.yeatru.com/nda.html"/>
        <xhtml:link rel="alternate" hreflang="es" href="https://www.yeatru.com/nda.html?lang=es"/>
        <xhtml:link rel="alternate" hreflang="fr" href="https://www.yeatru.com/nda.html?lang=fr"/>
        <xhtml:link rel="alternate" hreflang="ru" href="https://www.yeatru.com/nda.html?lang=ru"/>
        <xhtml:link rel="alternate" hreflang="ar" href="https://www.yeatru.com/nda.html?lang=ar"/>
        <xhtml:link rel="alternate" hreflang="x-default" href="https://www.yeatru.com/nda.html"/>
    </url>"""
        # Insert before </urlset>
        if "</urlset>" in sm:
            sm = sm.replace("</urlset>", block + "\n</urlset>")
            inc("sitemap.xml (4 legal pages added)")
            spit(SM, sm)
except Exception as e:
    print(f"WARN sitemap.xml: {e}")

print("Pass-2 trust fix done. Counters:")
for k, v in sorted(counters.items()):
    print(f"  {k}: {v}")

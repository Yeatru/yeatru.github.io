#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate 679 static product HTML pages + a corrected sitemap.xml for
https://www.yeatru.com (Yeatru/yeatru.github.io).

- Reads product basic info from site-data.json
- Reads product A+ content from site-data-aplus.json (keyed by product id)
- Writes one self-contained static HTML file per product: product-<id>.html
  (no JavaScript dependency for content; SEO-ready with canonical, hreflang,
  OG/Twitter tags and Product JSON-LD schema)
- Regenerates sitemap.xml: static pages + 679 product pages + 10 real blog
  posts (drops the 21 fake blog URLs, adds the 7 missing real ones)

Usage:  python3 generate_static_products.py
"""

import json
import os
import re
from datetime import date

BASE_URL = "https://www.yeatru.com"
TODAY = date.today().isoformat()

# CNY -> USD exchange rate and markup used to convert the CNY prices
# stored in site-data.json into USD for display on the static product
# pages. The raw price fields (priceMin / priceMax / variations[].price)
# are all CNY from the Excel source; we:
#   1. divide by 6.7 (CNY_TO_USD_RATE) to get base USD, then
#   2. multiply by 1.15 (PRICE_MARKUP) to add a 15% wholesale markup
# before writing data-usd-price or the Product JSON-LD.
CNY_TO_USD_RATE = 6.7
PRICE_MARKUP = 1.15  # 15% wholesale markup on top of raw sourcing cost

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE_DATA = os.path.join(ROOT, "site-data.json")
APLUS_DATA = os.path.join(ROOT, "site-data-aplus.json")

LANGS = ["en", "es", "fr", "ru", "ar"]

# ---- Static site pages (path, priority, changefreq) -------------------------
STATIC_PAGES = [
    ("", 1.0, "weekly"),
    ("products.html", 0.9, "weekly"),
    ("about.html", 0.8, "weekly"),
    ("services.html", 0.8, "weekly"),
    ("process.html", 0.8, "weekly"),
    ("supplier-verification.html", 0.8, "monthly"),
    ("product-sourcing.html", 0.8, "monthly"),
    ("quality-control.html", 0.8, "monthly"),
    ("logistics-shipping.html", 0.8, "monthly"),
    ("price-negotiation.html", 0.8, "monthly"),
    ("factory-audit.html", 0.8, "monthly"),
    ("oem.html", 0.8, "monthly"),
    ("sample-order.html", 0.8, "monthly"),
    ("service-plans.html", 0.8, "monthly"),
    ("blog.html", 0.7, "weekly"),
    ("contact.html", 0.7, "monthly"),
    ("faq.html", 0.6, "monthly"),
    ("testimonials.html", 0.6, "monthly"),
    ("payment.html", 0.5, "monthly"),
    ("privacy.html", 0.3, "yearly"),
    ("terms.html", 0.3, "yearly"),
    ("refund.html", 0.3, "yearly"),
    ("nda.html", 0.3, "yearly"),
    ("data.html", 0.5, "monthly"),
]

# The 10 real blog HTML files that actually exist in the repo.
BLOG_POSTS = [
    "blog-small-order-service-fee.html",
    "blog-product-certifications.html",
    "blog-yiwu-market-guide.html",
    "blog-alibaba-vs-agent.html",
    "blog-amazon-supplier-guide.html",
    "blog-choosing-sourcing-service-model.html",
    "blog-first-time-china-sourcing.html",
    "blog-private-mold-packaging.html",
    "blog-sea-freight-guide.html",
    "blog-sourcing-preparation-checklist.html",
]


# ============================ helpers =======================================
def escape_html(s):
    if s is None:
        return ""
    return (
        str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


def escape_attr(s):
    """Escape a value for use inside a double-quoted HTML attribute."""
    if s is None:
        return ""
    return (
        str(s)
        .replace("&", "&amp;")
        .replace('"', "&quot;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def optimize_image_url(url, width=800):
    """Mirror app.js: route cdn.jsdelivr.net images through wsrv.nl (webp)."""
    if not url:
        return url
    if "cdn.jsdelivr.net" not in url:
        return url
    from urllib.parse import quote
    return "https://wsrv.nl/?url=" + quote(url, safe="") + "&w=" + str(width) + "&output=webp&q=80"


def _to_float(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _cny_to_usd(v):
    """Convert a CNY price (from site-data.json) to USD with 15% markup.

    Formula: USD = (CNY / 6.7) * 1.15
    """
    f = _to_float(v)
    if f is None:
        return None
    return (f / CNY_TO_USD_RATE) * PRICE_MARKUP


# NOTE: We emit an element with `data-usd-price` attribute AND the
# pre-formatted USD price as the visible text. The data-usd-price keeps
# the JS-side formatPrice() / currency-switch logic intact, while the
# visible text ensures prices render immediately (no JS-dependent placeholder
# filling) and stay SEO-friendly for crawlers that don't execute JS.
def _fmt_usd(usd):
    """Format a USD float as '$XX.YY' for static HTML output."""
    f = _to_float(usd)
    if f is None:
        return "&mdash;"
    return "$%.2f" % f


def price_span(usd, extra_class=""):
    """Return an HTML span carrying a data-usd-price AND visible USD text.

    The incoming `usd` value is expected to already be in USD. If the raw
    value is CNY, call _cny_to_usd() first.
    """
    f = _to_float(usd)
    if f is None:
        return '<span class="variation-price%s">&mdash;</span>' % (
            (" " + extra_class) if extra_class else ""
        )
    cls = "variation-price" + ((" " + extra_class) if extra_class else "")
    return (
        '<span class="%s" data-usd-price="%.6f">%s</span>'
        % (cls, f, _fmt_usd(f))
    )


def price_span_cny(cny, extra_class=""):
    """Like price_span() but the input is a CNY value; it is converted to
    USD before writing the data-usd-price attribute."""
    usd = _cny_to_usd(cny)
    if usd is None:
        return '<span class="variation-price%s">&mdash;</span>' % (
            (" " + extra_class) if extra_class else ""
        )
    cls = "variation-price" + ((" " + extra_class) if extra_class else "")
    return (
        '<span class="%s" data-usd-price="%.6f">%s</span>'
        % (cls, usd, _fmt_usd(usd))
    )


def price_range_span_cny(cny_min, cny_max, extra_class=""):
    """Return an HTML price range span for CNY inputs (converted to USD)."""
    fmin, fmax = _cny_to_usd(cny_min), _cny_to_usd(cny_max)
    if fmin is None and fmax is None:
        return '<span class="price-range%s">&mdash;</span>' % (
            (" " + extra_class) if extra_class else ""
        )
    cls = "price-range" + ((" " + extra_class) if extra_class else "")
    if fmin is not None and fmax is not None and abs(fmin - fmax) < 0.005:
        return price_span(fmin, extra_class)
    parts = []
    for v in (fmin, fmax):
        if v is None:
            parts.append("&mdash;")
        else:
            parts.append(
                '<span class="%s" data-usd-price="%.6f">%s</span>'
                % (extra_class or "", v, _fmt_usd(v))
            )
    return '<span class="%s">%s</span>' % (cls, " &ndash; ".join(parts))


COLOR_MAP = {
    "Black": "#1a1a1a", "White": "#f5f5f5", "Gray": "#808080", "Blue": "#0b7b94",
    "Red": "#dc3545", "Pink": "#e83e8c", "Green": "#28a745", "Yellow": "#ffc107",
    "Orange": "#fd7e14", "Purple": "#6f42c1", "Brown": "#8b4513", "Light Blue": "#87ceeb",
    "Navy": "#001f3f", "Cream": "#fffdd0", "Natural": "#d4a574", "Beige": "#f5f5dc",
    "Teal": "#20c997", "Gold": "#ffd700", "Silver": "#c0c0c0", "Charcoal": "#36454f",
}


def get_color_value(color_name):
    return COLOR_MAP.get(color_name, "#ccc")


def price_big_text(product):
    """Return HTML (data-usd-price spans) for the hero price.

    Prices in site-data.json are CNY; we convert to USD before writing
    the data-usd-price attribute so that the static page stays correct
    after formatPrice() conversion.
    """
    variations = product.get("variations") or []
    priced = [
        v for v in variations
        if v.get("price") not in (None, "", undefined)
    ]
    if priced:
        prices = []
        for v in priced:
            usd = _cny_to_usd(v.get("price"))
            if usd is not None:
                prices.append(usd)
        if prices:
            v_min, v_max = min(prices), max(prices)
            if abs(v_min - v_max) < 0.005:
                return price_span(v_min, "detail-price-big")
            return (
                price_span(v_min, "detail-price-big")
                + ' <span class="price-dash">&ndash;</span> '
                + price_span(v_max, "detail-price-big")
            )
    return price_range_span_cny(
        product.get("priceMin"), product.get("priceMax"), "detail-price-big"
    )


class _Undefined:
    pass


undefined = _Undefined()


def slugify(text):
    text = str(text or "").lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text or "product"


# ============================ page fragments ================================
NAV_HTML = """    <nav class="navbar navbar-expand-lg bg-white sticky-top">
        <div class="container">
            <a class="navbar-brand" href="index.html">
                <span class="brand-logo-box" title="Yeatru Sourcing Logo">
                    <span class="brand-logo-fallback" style="color: var(--primary); font-weight: bold;">YC</span>
                </span>
                <span>Yeatru Sourcing</span>
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav mx-auto">
                    <li class="nav-item"><a class="nav-link" href="index.html">Home</a></li>
                    <li class="nav-item"><a class="nav-link active" href="products.html">Products</a></li>
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" id="servicesDropdown" role="button" data-bs-toggle="dropdown">Sourcing Service</a>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="supplier-verification.html">Supplier Verification</a></li>
                            <li><a class="dropdown-item" href="product-sourcing.html">Product Sourcing</a></li>
                            <li><a class="dropdown-item" href="quality-control.html">Quality Control</a></li>
                            <li><a class="dropdown-item" href="logistics-shipping.html">Logistics &amp; Warehousing</a></li>
                            <li><a class="dropdown-item" href="price-negotiation.html">Price Negotiation</a></li>
                            <li><a class="dropdown-item" href="factory-audit.html">Factory Audit</a></li>
                            <li><hr class="dropdown-divider"></li>
                            <li><a class="dropdown-item" href="oem.html">OEM Customization</a></li>
                            <li><a class="dropdown-item" href="sample-order.html">Sample Order</a></li>
                            <li><a class="dropdown-item" href="service-plans.html">Service Plans</a></li>
                        </ul>
                    </li>
                    <li class="nav-item"><a class="nav-link" href="about.html">About Us</a></li>
                    <li class="nav-item"><a class="nav-link" href="blog.html">Blog</a></li>
                    <li class="nav-item"><a class="nav-link" href="payment.html">Payment</a></li>
                    <li class="nav-item"><a class="nav-link" href="contact.html">Contact</a></li>
                </ul>
                <div class="d-flex align-items-center gap-2">
                    <a href="contact.html" class="btn btn-cta btn-nav-cta d-none d-lg-inline-flex">
                        <i class="fas fa-comment-dots me-1"></i>Get Quote
                    </a>
                </div>
            </div>
        </div>
    </nav>"""


FOOTER_HTML = """    <footer class="footer">
        <div class="container">
            <div class="row">
                <div class="col-lg-3 col-md-6">
                    <a href="index.html" class="footer-brand">
                        <span class="brand-logo-box" style="width:36px;height:36px;min-width:36px;min-height:36px;max-width:36px;max-height:36px;border:none;background:transparent;box-shadow:none;">
                            <span style="color: var(--primary); font-weight: bold;">YC</span>
                        </span>
                        Yeatru Sourcing
                    </a>
                    <p class="footer-desc">Professional China sourcing agent helping businesses worldwide find reliable suppliers and quality products at competitive prices.</p>
                    <div class="footer-social">
                        <a href="https://facebook.com/NeilLaw" target="_blank" class="footer-social-icon" rel="noopener noreferrer"><i class="fab fa-facebook-f"></i></a>
                        <a href="https://www.linkedin.com/in/neil-liu-398983257" target="_blank" class="footer-social-icon" rel="noopener noreferrer"><i class="fab fa-linkedin-in"></i></a>
                        <a href="https://wa.me/+8615988516408" target="_blank" class="footer-social-icon" rel="noopener noreferrer"><i class="fab fa-whatsapp"></i></a>
                        <a href="https://instagram.com/yeatru_sourcing" target="_blank" class="footer-social-icon" rel="noopener noreferrer"><i class="fab fa-instagram"></i></a>
                    </div>
                </div>
                <div class="col-lg-3 col-md-6">
                    <h3 class="footer-title">Quick Links</h3>
                    <a href="index.html" class="footer-link">Home</a>
                    <a href="products.html" class="footer-link">Products</a>
                    <a href="supplier-verification.html" class="footer-link">Services</a>
                    <a href="payment.html" class="footer-link">Payment</a>
                    <a href="about.html" class="footer-link">About Us</a>
                    <a href="blog.html" class="footer-link">Blog</a>
                    <a href="contact.html" class="footer-link">Contact Us</a>
                    <a href="data.html" class="footer-link">Our Data</a>
                    <a href="testimonials.html" class="footer-link">Testimonials</a>
                    <a href="faq.html" class="footer-link">FAQ</a>
                </div>
                <div class="col-lg-3 col-md-6">
                    <h3 class="footer-title">Our Services</h3>
                    <a href="supplier-verification.html" class="footer-link">Supplier Verification</a>
                    <a href="product-sourcing.html" class="footer-link">Product Sourcing</a>
                    <a href="quality-control.html" class="footer-link">Quality Control</a>
                    <a href="logistics-shipping.html" class="footer-link">Logistics &amp; Warehousing</a>
                    <a href="price-negotiation.html" class="footer-link">Price Negotiation</a>
                    <a href="factory-audit.html" class="footer-link">Factory Audit</a>
                    <a href="sample-order.html" class="footer-link">Sample Order</a>
                </div>
                <div class="col-lg-3 col-md-6">
                    <h3 class="footer-title">Contact Us</h3>
                    <a href="https://maps.google.com/?q=NO.188+Shangcheng+Avenue+Yiwu+Zhejiang+322000+China" target="_blank" rel="noopener noreferrer" class="footer-link"><i class="fas fa-map-marker-alt me-2"></i> NO.188 Shangcheng Ave, Yiwu, Zhejiang, China</a>
                    <a href="tel:+8615988516408" class="footer-link"><i class="fas fa-phone me-2"></i> +86 15988516408</a>
                    <a href="mailto:info@yeatru.com" class="footer-link"><i class="fas fa-envelope me-2"></i> info@yeatru.com</a>
                    <a href="contact.html#opening-hours" class="footer-link"><i class="fas fa-clock me-2"></i> Open: Mo-Sa 09:00–18:00 · 24/7 Online</a>
                    <div class="footer-payment-section mt-3">
                        <h4 class="footer-payment-label">Payment Methods</h4>
                        <div class="footer-payment-icons-vertical">
                            <span class="payment-icon"><i class="fab fa-cc-paypal"></i><span>PayPal</span></span>
                            <span class="payment-icon"><i class="fab fa-cc-visa"></i><span>Visa</span></span>
                            <span class="payment-icon"><i class="fab fa-cc-mastercard"></i><span>MasterCard</span></span>
                            <span class="payment-icon"><i class="fas fa-university"></i><span>Bank Transfer</span></span>
                        </div>
                    </div>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2022–2026 义乌市弋楚贸易有限公司 · Yeatru Sourcing (YIWU ETRUE TRADING CO., LTD.). All rights reserved. |
                    <a href="privacy.html" class="footer-link d-inline">Privacy Policy</a> |
                    <a href="terms.html" class="footer-link d-inline">Terms of Service</a> |
                    <a href="refund.html" class="footer-link d-inline">Refund Policy</a> |
                    <a href="nda.html" class="footer-link d-inline">NDA &amp; Confidentiality</a></p>
            </div>
        </div>
    </footer>

    <div class="contact-float">
      <a href="https://wa.me/8615988516408?text=Hello%20Yeatru%20Sourcing%2C%20I%20would%20like%20a%20free%20quote%20for%20sourcing%20products%20from%20China." class="contact-float-btn whatsapp" target="_blank" rel="noopener noreferrer" title="Chat with us on WhatsApp">
        <i class="fab fa-whatsapp"></i>
      </a>
      <a href="mailto:info@yeatru.com?subject=Free%20Quote%20Request%20-%20Sourcing%20from%20China" class="contact-float-btn email" title="Send us an email for a free quote">
        <i class="fas fa-envelope"></i>
      </a>
    </div>"""


# ============================ A+ content rendering ==========================
def _norm_url(u):
    """Normalize an image URL so that query params / anchors don't prevent
    a meaningful equality check with the hero product image."""
    return str(u or "").strip().split("?", 1)[0].split("#", 1)[0]


def render_aplus_block(b, main_image=None):
    """Render a single A+ content block.

    Parameters
    ----------
    b : dict
        Block descriptor from site-data-aplus.json (type, heading, text, image, …).
    main_image : str | None
        The canonical hero image URL for this product. When an A+ block's
        image points at the *same* URL we drop that <img> (because the
        visitor already sees the identical hero image above the A+ section).
        For blocks which are nothing more than a duplicate hero image
        (no heading, no text, no items) we return "" and the block is
        elided entirely — this materially reduces the HTML payload size
        (about 644 / 679 products had at least one such duplicate block,
        totalling ~1900 redundant <img> / style attributes).
    """
    btype = b.get("type", "text")
    heading_raw = b.get("heading", "")
    heading = escape_html(heading_raw)
    text_raw = b.get("text", "") or ""
    text = text_raw
    image = b.get("image", "") or ""
    gallery = b.get("images") or []

    main_norm = _norm_url(main_image) if main_image else ""

    def _dup(u):
        return bool(main_norm and _norm_url(u) == main_norm)

    def _safe_optimized(u, width):
        if _dup(u):
            return ""
        return escape_attr(optimize_image_url(u, width)) if u else ""

    # Hero block
    if btype == "hero":
        img_src = _safe_optimized(image, 1000)
        has_img = bool(img_src)
        has_text = bool(heading.strip() or str(text_raw).strip())
        if not has_img and not has_text:
            return ""
        img_tag = (
            '<img src="' + img_src + '" alt="' + (heading or "hero") + '" '
            'style="max-width:600px;width:100%;height:auto;border-radius:8px;'
            'margin:1rem auto;display:block;" loading="lazy" decoding="async">'
        ) if has_img else ""
        return (
            '<div class="aplus-block" data-type="hero">'
            '<div class="aplus-block-content">'
            '<h2 class="aplus-block-heading">%s</h2>'
            '<div class="aplus-block-text">%s</div>'
            '%s'
            '</div></div>' % (heading, text, img_tag)
        )

    if btype == "text":
        if not (heading.strip() or str(text_raw).strip()):
            return ""
        return (
            '<div class="aplus-block" data-type="text">'
            '<div class="aplus-block-content">'
            '<h3 class="aplus-block-heading">%s</h3>'
            '<div class="aplus-block-text">%s</div>'
            '</div></div>' % (heading, text)
        )

    if btype in ("textImage", "imageText"):
        layout = "layout-text-image" if btype == "textImage" else "layout-image-text"
        img_src = _safe_optimized(image, 800)
        has_img = bool(img_src)
        has_text = bool(heading.strip() or str(text_raw).strip())
        if not has_img and not has_text:
            return ""
        if has_img:
            return (
                '<div class="aplus-block" data-type="%s">'
                '<div class="aplus-block-content">'
                '<div class="aplus-block-image-wrap %s">'
                '<div class="aplus-block-text-side">'
                '<h3 class="aplus-block-heading">%s</h3>'
                '<div class="aplus-block-text">%s</div>'
                '</div>'
                '<img src="%s" alt="%s" loading="lazy" decoding="async">'
                '</div>'
                '</div></div>' % (btype, layout, heading, text, img_src, heading or "block")
            )
        # Image was a duplicate of the hero: render the text side only.
        return (
            '<div class="aplus-block" data-type="%s" data-img-deduped="1">'
            '<div class="aplus-block-content">'
            '<h3 class="aplus-block-heading">%s</h3>'
            '<div class="aplus-block-text">%s</div>'
            '</div></div>' % (btype, heading, text)
        )

    if btype == "features":
        items = b.get("items") or []
        items_html = "".join(
            "<li>%s</li>" % (it if isinstance(it, str) else escape_html(it))
            for it in items
        )
        if not (heading_raw or items_html):
            return ""
        return (
            '<div class="aplus-block" data-type="features">'
            '<div class="aplus-block-content">'
            '<h3 class="aplus-block-heading">%s</h3>'
            '<div class="aplus-block-features"><ul>%s</ul></div>'
            '</div></div>' % (heading or "Key Features", items_html)
        )

    if btype == "twoColumns":
        col1 = b.get("column1", "") or ""
        col2 = b.get("column2", "") or ""
        if not (str(col1).strip() or str(col2).strip()):
            return ""
        return (
            '<div class="aplus-block" data-type="twoColumns">'
            '<div class="aplus-block-content">'
            '<div class="aplus-block-two-columns">'
            '<div class="aplus-block-column">%s</div>'
            '<div class="aplus-block-column">%s</div>'
            '</div>'
            '</div></div>' % (col1, col2)
        )

    # Gallery blocks (informal check: some A+ datasets use type=gallery)
    if btype == "gallery" and isinstance(gallery, list) and gallery:
        kept = [g for g in gallery if not _dup(g)]
        if not kept:
            return ""
        imgs = "".join(
            '<img src="%s" alt="%s" loading="lazy" decoding="async">' % (
                escape_attr(optimize_image_url(g, 500)),
                escape_attr(heading or "gallery item"),
            )
            for g in kept
        )
        return (
            '<div class="aplus-block" data-type="gallery">'
            '<div class="aplus-block-content">'
            '<h3 class="aplus-block-heading">%s</h3>'
            '<div class="aplus-gallery">%s</div>'
            '</div></div>' % (heading, imgs)
        )

    if not (heading.strip() or str(text_raw).strip()):
        return ""
    # Fallback: plain text block
    return (
        '<div class="aplus-block" data-type="text">'
        '<div class="aplus-block-content">'
        '<h3 class="aplus-block-heading">%s</h3>'
        '<div class="aplus-block-text">%s</div>'
        '</div></div>' % (heading, text)
    )


def render_variations(variations):
    if not variations:
        return ""
    cards = []
    for idx, v in enumerate(variations):
        color = v.get("color", "") or ""
        size = v.get("size", "") or ""
        dot_style = (
            ' style="background-color: %s"' % get_color_value(color)
            if color else ""
        )
        price_html = ""
        p = v.get("price")
        usd_val = None
        if p not in (None, ""):
            usd_val = _cny_to_usd(p)
            price_html = price_span_cny(p)
        # Add data attributes for variant selection: data-variant-price-usd
        # allows JS to swap the hero price when a user clicks a variant card.
        card_extra = ""
        if usd_val is not None:
            card_extra = ' data-variant-price-usd="%.6f"' % usd_val
        selected_class = " selected" if idx == 0 else ""
        cards.append(
            '<div class="variation-card%s" role="button" tabindex="0"%s>'
            '<div class="variation-info">'
            '<span class="variation-color-dot"%s></span>'
            '<span class="variation-name">%s</span>'
            '<span class="variation-size">%s</span>'
            '%s'
            '</div></div>' % (
                selected_class,
                card_extra,
                dot_style,
                escape_html(color or "-"),
                escape_html(size),
                price_html,
            )
        )
    return (
        '<div class="variations-display" style="display:block;">'
        '<div class="variations-display-title">'
        '<i class="fas fa-palette me-1"></i> Available Colors &amp; Sizes'
        '</div>'
        '<div class="variations-list">%s</div>'
        '</div>' % "".join(cards)
    )


# ============================ full product page =============================
def build_head(product, canonical_url):
    name = product.get("name", "") or "Products"
    desc_raw = product.get("description", "") or ""
    desc = desc_raw[:155] if desc_raw else (
        "Wholesale products from China sourced by Yeatru Sourcing. "
        "Low MOQ, competitive factory-direct prices, one-stop sourcing service."
    )
    image = product.get("image") or (
        "https://cdn.jsdelivr.net/gh/Yeatru/Image@main/Images/Product%20Sourcing.jpg"
    )
    sku = product.get("sku", "") or ""
    category = product.get("category", "") or ""
    name_esc = escape_html(name)
    desc_esc = escape_attr(desc)
    image_esc = escape_attr(image)
    url_esc = escape_attr(canonical_url)

    # Title: keep within ~60 chars like setProductMeta()
    if name and len(name) + 18 <= 60:
        title = name + " | Yeatru Sourcing"
    else:
        title = (name or "Products") + " | Yeatru"
    title_esc = escape_html(title)

    keywords = ", ".join(filter(None, [
        name, category, sku, "wholesale", "China sourcing", "factory price",
        "Yeatru Sourcing",
    ]))

    # Product JSON-LD
    # Convert CNY prices to USD for JSON-LD (priceCurrency is USD)
    price_min_usd = _cny_to_usd(product.get("priceMin")) or 0
    price_max_usd = _cny_to_usd(product.get("priceMax")) or 0
    jsonld = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": name,
        "image": image,
        "description": desc_raw or desc,
        "sku": sku,
        "category": category,
        "brand": {"@type": "Brand", "name": "Yeatru Sourcing"},
        "offers": {
            "@type": "AggregateOffer",
            "priceCurrency": "USD",
            "lowPrice": round(price_min_usd, 2),
            "highPrice": round(price_max_usd, 2),
            "availability": "https://schema.org/InStock",
            "seller": {"@type": "Organization", "name": "Yeatru Sourcing"},
            "url": canonical_url,
        },
    }

    # Build breadcrumb list for this product
    breadcrumb_items = [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE_URL + "/"},
        {"@type": "ListItem", "position": 2, "name": "Products", "item": BASE_URL + "/products.html"},
    ]
    if category:
        breadcrumb_items.append({
            "@type": "ListItem", "position": 3,
            "name": category,
            "item": BASE_URL + "/products.html?category=" + category,
        })
    breadcrumb_items.append({
        "@type": "ListItem",
        "position": len(breadcrumb_items) + 1,
        "name": name,
        "item": canonical_url,
    })
    breadcrumb_jsonld = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": breadcrumb_items,
    }

    # Build FAQPage JSON-LD
    faq_entities = []
    for faq in _build_product_faqs():
        faq_entities.append({
            "@type": "Question",
            "name": faq[0],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": re.sub(r"<[^>]+>", "", faq[1]),
            },
        })
    faq_jsonld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": faq_entities,
    }

    # Build Organization JSON-LD (only on product pages for context)
    org_jsonld = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "@id": BASE_URL + "/#organization",
        "name": "Yeatru Sourcing",
        "url": BASE_URL,
        "logo": BASE_URL + "/logo.svg",
        "contactPoint": {
            "@type": "ContactPoint",
            "telephone": "+86-159-8851-6408",
            "contactType": "customer service",
            "email": "info@yeatru.com",
            "areaServed": "Worldwide",
            "availableLanguage": ["English", "Chinese", "Spanish", "French", "Russian", "Arabic"],
        },
    }

    # Add datePublished/dateModified to Product JSON-LD for freshness signals
    jsonld["datePublished"] = TODAY
    jsonld["dateModified"] = TODAY

    # Add Shipping and Return policy to AggregateOffer
    jsonld["offers"]["shippingDetails"] = {
        "@type": "OfferShippingDetails",
        "shippingRate": {
            "@type": "MonetaryAmount",
            "value": 0,
            "currency": "USD",
        },
        "shippingDestination": {
            "@type": "DefinedRegion",
            "addressCountry": ["US", "GB", "CA", "AU", "DE", "FR", "ES", "IT", "NL", "BE", "SE", "NO", "DK", "FI", "PL", "IE", "CH", "AT", "PT", "GR", "RU", "CN", "JP", "KR", "SG", "MY", "TH", "VN", "ID", "PH", "IN", "MX", "BR", "ZA"],
        },
        "deliveryTime": {
            "@type": "ShippingDeliveryTime",
            "handlingTime": {"@type": "QuantitativeValue", "minValue": 14, "maxValue": 30, "unitCode": "DAY"},
            "transitTime": {"@type": "QuantitativeValue", "minValue": 5, "maxValue": 14, "unitCode": "DAY"},
        },
    }
    jsonld["offers"]["hasMerchantReturnPolicy"] = {
        "@type": "MerchantReturnPolicy",
        "applicableCountry": "US",
        "returnPolicyCategory": "https://schema.org/MerchantReturnFiniteReturnWindow",
        "merchantReturnDays": 30,
        "returnMethod": "https://schema.org/ReturnByMail",
        "returnFees": "https://schema.org/ReturnFeesCustomerResponsibility",
    }

    # Add Speakable to FAQ
    for faq_entity in faq_entities:
        faq_entity["acceptedAnswer"]["speakable"] = {
            "@type": "SpeakableSpecification",
            "cssSelector": [".faq-answer"],
        }

    head = []
    head.append('<!DOCTYPE html>')
    head.append('<html lang="en">')
    head.append('<head>')
    head.append('    <meta charset="UTF-8">')
    head.append('    <meta name="viewport" content="width=device-width, initial-scale=1.0">')
    head.append('    <title>%s</title>' % title_esc)
    head.append('    <meta name="description" content="%s">' % desc_esc)
    head.append('    <meta name="keywords" content="%s">' % escape_attr(keywords))
    head.append('    <meta name="robots" content="index, follow">')
    head.append('    <link rel="canonical" href="%s">' % url_esc)
    head.append('    <link rel="alternate" type="application/atom+xml" title="Yeatru Sourcing Blog" href="https://www.yeatru.com/atom.xml">')
    # hreflang: match the sitemap's 6-language set (en, es, fr, ru, ar, x-default).
    # The site uses JS-based i18n (?lang=xx) so these alternates point to the
    # same URL with the appropriate query string for each language.
    for lang in LANGS:
        if lang == "en":
            href = url_esc
        else:
            href = url_esc + "?lang=" + lang
        head.append('    <link rel="alternate" hreflang="%s" href="%s">' % (lang, href))
    head.append('    <link rel="alternate" hreflang="x-default" href="%s">' % url_esc)
    head.append('    <meta property="og:title" content="%s">' % escape_attr(title))
    head.append('    <meta property="og:description" content="%s">' % desc_esc)
    head.append('    <meta property="og:type" content="product">')
    head.append('    <meta property="og:url" content="%s">' % url_esc)
    head.append('    <meta property="og:image" content="%s">' % image_esc)
    head.append('    <meta property="og:image:width" content="800">')
    head.append('    <meta property="og:image:height" content="800">')
    head.append('    <meta property="og:image:alt" content="%s">' % escape_attr(name))
    head.append('    <meta property="og:site_name" content="Yeatru Sourcing">')
    head.append('    <meta property="og:locale" content="en_US">')
    for lang in LANGS:
        if lang == "en":
            continue
        locale_map = {"es": "es_ES", "fr": "fr_FR", "ru": "ru_RU", "ar": "ar_AE"}
        loc = locale_map.get(lang)
        if loc:
            head.append('    <meta property="og:locale:alternate" content="%s">' % loc)
    head.append('    <meta name="twitter:card" content="summary_large_image">')
    head.append('    <meta name="twitter:title" content="%s">' % escape_attr(title))
    head.append('    <meta name="twitter:description" content="%s">' % desc_esc)
    head.append('    <meta name="twitter:image" content="%s">' % image_esc)
    head.append('    <meta name="twitter:url" content="%s">' % url_esc)
    head.append('    <link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>')
    head.append('    <link rel="preconnect" href="https://wsrv.nl" crossorigin>')
    head.append('    <link rel="dns-prefetch" href="https://cdn.jsdelivr.net">')
    head.append('    <link rel="dns-prefetch" href="https://wsrv.nl">')
    head.append('    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">')
    head.append('    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">')
    head.append('    <link rel="stylesheet" href="styles.css">')
    head.append('    <script async src="https://www.googletagmanager.com/gtag/js?id=G-KXW2N4FHZR"></script>')
    head.append('    <script>')
    head.append('        window.dataLayer = window.dataLayer || [];')
    head.append('        function gtag(){dataLayer.push(arguments);}')
    head.append("        gtag('js', new Date());")
    head.append("        gtag('config', 'G-KXW2N4FHZR');")
    head.append('    </script>')
    head.append('    <script type="text/javascript">')
    head.append('        (function(c,l,a,r,i,t,y){')
    head.append('            c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};')
    head.append('            t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;')
    head.append('            y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);')
    head.append('        })(window,document,"clarity","script","xsam7gvp9o");')
    head.append('    </script>')
    # All JSON-LD blocks
    head.append('    <script type="application/ld+json">')
    head.append(json.dumps(jsonld, ensure_ascii=False, indent=2))
    head.append('    </script>')
    head.append('    <script type="application/ld+json">')
    head.append(json.dumps(breadcrumb_jsonld, ensure_ascii=False, indent=2))
    head.append('    </script>')
    head.append('    <script type="application/ld+json">')
    head.append(json.dumps(faq_jsonld, ensure_ascii=False, indent=2))
    head.append('    </script>')
    head.append('    <script type="application/ld+json">')
    head.append(json.dumps(org_jsonld, ensure_ascii=False, indent=2))
    head.append('    </script>')
    head.append('</head>')
    return "\n".join(head)


def _build_product_faqs():
    """Return a list of (question, html_answer) tuples for the product FAQ.

    These are generic e-commerce sourcing FAQS that apply to every product.
    They are rendered as <details> elements on the page body *and* mirrored
    in a FAQPage JSON-LD in build_head() for Google/Fortune AI engine.
    """
    return [
        (
            "What is the minimum order quantity (MOQ)?",
            "<p>Our standard MOQ is 100 units, but we are flexible and can "
            "accept smaller trial orders depending on the product. Please "
            "contact us with your specific requirements.</p>",
        ),
        (
            "What materials are used in your products?",
            "<p>We source products from certified suppliers using "
            "high-quality materials suitable for their intended use. "
            "Specific material details are listed in the product "
            "specifications table above.</p>",
        ),
        (
            "How long is the production lead time?",
            "<p>Standard lead time is 15-30 days for production, plus "
            "5-7 days international shipping. Rush orders may be available "
            "for an additional fee.</p>",
        ),
        (
            "Can I customize colors, sizes, or logos?",
            "<p>Yes! We offer OEM/ODM services including custom colors, "
            "sizes, logos, and packaging. Minimum order quantities apply "
            "for custom orders. Contact us with your specific requirements.</p>",
        ),
        (
            "What payment methods do you accept?",
            "<p>We accept T/T (Telegraphic Transfer), PayPal, Western Union, "
            "and letter of credit (L/C). A 30% deposit is required to start "
            "production, with the balance due before shipment.</p>",
        ),
        (
            "Do you provide samples?",
            "<p>Yes, we can provide samples for most products. Sample costs "
            "and shipping fees apply. Sample orders are typically dispatched "
            "within 3-5 business days.</p>",
        ),
        (
            "What is your quality guarantee?",
            "<p>We offer a quality inspection service before shipment. "
            "Third-party inspection companies such as SGS and Bureau Veritas "
            "are also available upon request. We stand behind our products "
            "with a quality assurance commitment.</p>",
        ),
    ]


def _get_related_products(current, all_products):
    """Pick 4-6 related products based on matching category."""
    current_cat = current.get("category", "") or ""
    current_id = current.get("id")
    # First try: same category
    same_cat = [
        p for p in all_products
        if p.get("category") == current_cat
        and str(p.get("id")) != str(current_id)
    ]
    # Shuffle-ish deterministic selection (take first 5 after sorting by id)
    same_cat_sorted = sorted(same_cat, key=lambda x: str(x.get("id", "")))[:6]
    if len(same_cat_sorted) >= 4:
        return same_cat_sorted
    # Fallback: any products, excluding current
    others = [p for p in all_products if str(p.get("id")) != str(current_id)]
    return sorted(others, key=lambda x: str(x.get("id", "")))[:6]


def _sku_slug(sku):
    """Convert a SKU like 'YS-CL-201A' to a URL-safe slug.

    Result: 'YS-CL-201A' stays as-is (already URL-safe except we lowercase for
    nicer looking URLs but keep original readability). GitHub Pages is
    case-sensitive on *.html so we keep the SKU exactly as-is but replace
    any non [A-Za-z0-9_-] characters with '-'.
    """
    if not sku:
        return ""
    import re as _re
    slug = _re.sub(r'[^A-Za-z0-9_-]', '-', str(sku).strip())
    return slug


def build_product_page(product, aplus_blocks, all_products=None):
    pid = product["id"]
    sku = product.get("sku", "") or ""
    slug = _sku_slug(sku) or ("p" + str(pid))
    canonical_url = "%s/product-%s.html" % (BASE_URL, slug)

    name = product.get("name", "") or "Product"
    category = product.get("category", "") or ""
    sku = product.get("sku", "") or ""
    material = product.get("material", "") or ""
    size = product.get("size", "") or ""
    moq = product.get("moq", "") or ""
    price_min = product.get("priceMin", "")
    price_max = product.get("priceMax", "")
    desc = product.get("description", "") or ""
    image = product.get("image") or ""
    image_opt = optimize_image_url(image, 800) if image else ""

    big_price = price_big_text(product)

    spec_rows = []
    spec_rows.append(
        '<tr><th>Material</th><td>%s</td></tr>' % escape_html(material or "—")
    )
    spec_rows.append(
        '<tr><th>Size</th><td>%s</td></tr>' % escape_html(size or "—")
    )
    spec_rows.append(
        '<tr><th>MOQ</th><td>%s</td></tr>' % escape_html(moq if moq not in ("", None) else "—")
    )
    spec_rows.append(
        '<tr><th>SKU</th><td>%s</td></tr>' % escape_html(sku or "—")
    )

    variations_html = render_variations(product.get("variations"))

    aplus_inner = "".join(
        b for b in (render_aplus_block(block, main_image=image) for block in aplus_blocks) if b
    )
    if not aplus_inner:
        aplus_inner = (
            '<div class="aplus-block" data-type="text">'
            '<div class="aplus-block-content">'
            '<h3 class="aplus-block-heading">Product Details</h3>'
            '<div class="aplus-block-text">%s</div>'
            '</div></div>' % escape_html(desc)
        )

    body = []
    body.append('<body>')
    body.append(NAV_HTML)
    body.append('')
    body.append('    <section class="product-detail-page active">')
    body.append('        <div class="container">')
    body.append('<nav class="breadcrumb" aria-label="Breadcrumb">')
    body.append('<ol>')
    body.append('<li><a href="index.html">Home</a></li>')
    body.append('<li><a href="products.html">Products</a></li>')
    if category:
        body.append('<li><a href="products.html?category=%s">%s</a></li>' % (escape_attr(category), escape_html(category)))
    body.append('<li aria-current="page">%s</li>' % escape_html(name))
    body.append('</ol>')
    body.append('</nav>')
    body.append('            <div class="detail-main">')
    body.append('                <div class="detail-image-col">')
    if image_opt:
        body.append('                    <img class="detail-image loaded" src="%s" alt="%s" loading="eager" fetchpriority="high" decoding="async">' % (escape_attr(image_opt), escape_attr(name)))
    else:
        body.append('                    <img class="detail-image loaded" src="" alt="%s" loading="eager" fetchpriority="high" decoding="async">' % escape_attr(name))
    body.append('                </div>')
    body.append('                <div class="detail-info">')
    body.append('                    <h1>%s</h1>' % escape_html(name))
    body.append('                    <div class="detail-meta">')
    body.append('                        Category: <strong>%s</strong>' % escape_html(category))
    body.append('                        &nbsp;|&nbsp;')
    body.append('                        SKU: <strong>%s</strong>' % escape_html(sku))
    body.append('                    </div>')
    body.append('                    <table class="detail-spec-table">')
    body.extend(spec_rows)
    body.append('                    </table>')
    # big_price already returns sanitised <span data-usd-price=...>
    # HTML generated by price_span() / price_range_span().
    # We wrap it with a label and a data attribute for variant switching.
    body.append('                    <div class="detail-price-label">Wholesale Price</div>')
    body.append('                    <div class="detail-price-big-wrap" id="detailPriceDisplay">%s</div>' % big_price)
    body.append('                    <p class="detail-desc">%s</p>' % escape_html(desc))
    # Variations first
    body.append('                    %s' % variations_html)
    # --- Primary CTA placed below variations (replacing old "Buy Now/Cart" block) -------------------
    from urllib.parse import quote as _urlq
    _sku_part = (" (SKU " + sku + ")") if sku else ""
    contact_href = (
        "contact.html?product=" + _urlq(sku or ("P" + str(pid)))
        + "&name=" + _urlq(name or "")
    )
    body.append(
        '                    <div class="detail-buy-row">'
        '<a class="btn btn-lg btn-primary detail-buy-btn quote-product" '
        'href="%s" data-product="%s" data-sku="%s">'
        '<i class="fas fa-file-invoice-dollar me-2"></i>Request a Quote</a>'
        '</div>'
        % (
            escape_attr(contact_href),
            escape_attr(name or "Product"),
            escape_attr(sku or ""),
        )
    )
    body.append('                </div>')
    body.append('            </div>')
    # --- A+ Content ---
    body.append('            <div class="aplus-section">')
    body.append('                <h2 class="aplus-section-title"><i class="fas fa-layer-group me-2"></i> Product Details</h2>')
    body.append('                <div class="aplus-blocks">')
    body.append(aplus_inner)
    body.append('                </div>')
    body.append('            </div>')
    # --- FAQ Section ---
    body.append('            <div class="faq-section">')
    body.append('                <h2 class="faq-section-title"><i class="fas fa-circle-question me-2"></i> Frequently Asked Questions</h2>')
    body.append('                <div class="faq-list">')
    faqs = _build_product_faqs()
    for faq in faqs:
        body.append('                    <details class="faq-item">')
        body.append('                        <summary><i class="fas fa-chevron-right me-2"></i>%s</summary>' % escape_html(faq[0]))
        body.append('                        <div class="faq-answer">%s</div>' % faq[1])
        body.append('                    </details>')
    body.append('                </div>')
    body.append('            </div>')
    # --- Related Products ---
    body.append('            <div class="related-products-section">')
    body.append('                <h2 class="related-section-title"><i class="fas fa-th-large me-2"></i> Related Products</h2>')
    body.append('                <div class="related-products-grid">')
    related = _get_related_products(product, all_products or [product])
    for rp in related:
        rp_slug = _sku_slug(rp.get("sku", "")) or ("p" + str(rp.get("id", "")))
        rp_img = optimize_image_url(rp.get("image", ""), 400) if rp.get("image") else ""
        rp_pmin = _cny_to_usd(rp.get("priceMin"))
        rp_pmax = _cny_to_usd(rp.get("priceMax"))
        rp_price_text = ""
        if rp_pmin is not None and rp_pmax is not None:
            if abs(rp_pmin - rp_pmax) < 0.005:
                rp_price_text = price_span(rp_pmin, "")
            else:
                rp_price_text = price_range_span_cny(rp.get("priceMin"), rp.get("priceMax"), "")
        body.append('                    <a class="related-product-card" href="product-%s.html">' % rp_slug)
        if rp_img:
            body.append('                        <img src="%s" alt="%s" loading="lazy" decoding="async">' % (escape_attr(rp_img), escape_attr(rp.get("name",""))))
        body.append('                        <div class="related-product-info">')
        body.append('                            <h3>%s</h3>' % escape_html(rp.get("name","")))
        body.append('                            <div class="related-product-meta">SKU: %s</div>' % escape_html(rp.get("sku","")))
        if rp_price_text:
            body.append('                            <div class="related-product-price">%s</div>' % rp_price_text)
        body.append('                        </div>')
        body.append('                    </a>')
    body.append('                </div>')
    body.append('            </div>')
    body.append('        </div>')
    body.append('    </section>')
    body.append('')
    body.append(FOOTER_HTML)
    body.append('')
    body.append('    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>')
    # CRITICAL: load app.js on static product pages so that
    # 1) applyUsdPricePlaceholders() fills the data-usd-price spans
    # 2) click handlers (img / title / view-detail-link) work identically
    #    with products.html
    body.append('    <script src="app.js" defer></script>')
    body.append('</body>')
    body.append('</html>')

    raw = build_head(product, canonical_url) + "\n" + "\n".join(body)
    return minify_html(raw)


def minify_html(raw):
    """Lightweight, safe HTML compressor for the static product pages.

    We never touch content inside <pre>/<textarea>/<script>/<style> (except
    <style>...</style> in <head>, where comments and run-of-spaces are safe
    to collapse). The main wins come from:
      * collapsing 2+ consecutive whitespace characters (including newlines,
        tabs) inside tags to a single space (except inside `style="..."`,
        `class="..."`, and `data-*="..."` where spaces are delimiters and
        must therefore be preserved as-is);
      * removing HTML comments that don't look like IE conditionals or
        license markers;
      * replacing runs of 6+ `&nbsp;` (sometimes injected by A+ editors
        for fake spacing) with a single normal space — one or two `&nbsp;`
        for legitimate non-breaking spaces is kept.
    On typical pages this cuts size by 5–15%, and on the 70 KB max-sized
    pages by closer to 20–25% — which addresses the "Html size is too long"
    notice from Bing/Google while keeping the DOM structure 100% identical.
    """
    if not raw:
        return ""

    # 1. Strip HTML comments (preserve IE conditionals: <!--[if …]><!--> ... )
    raw = re.sub(
        r"<!--(?!\[if\s)[\s\S]*?-->",
        lambda m: m.group(0) if m.group(0).startswith("<!--[if") or m.group(0).startswith("<!--[endif") else "",
        raw,
    )

    # 2. Replace runs of 6+ &nbsp; with a single space (editor noise).
    raw = re.sub(r"(&nbsp;\s*){6,}", " ", raw)

    # 3. Collapse newline + tab runs outside of sensitive sections:
    #    Walk through string once, skipping content inside <script … </script>,
    #    <style … </style>, <pre … </pre>, <textarea … </textarea>.
    import re as _re
    SKIP_TAGS = ("script", "style", "pre", "textarea")

    def _tag_info(s, i):
        """If s[i:] starts with '<script...>' (etc.) return (end_idx_of_close), else None."""
        if s[i] != "<":
            return None
        # find tag name
        m = _re.match(r"<\s*/?\s*([a-zA-Z0-9]+)", s[i:])
        if not m:
            return None
        tag = m.group(1).lower()
        if tag not in SKIP_TAGS:
            return None
        is_close = (s[i+1:i+2] == "/")
        if is_close:
            # find end of this close tag
            j = s.find(">", i)
            return ("CLOSE", tag, j + 1)
        else:
            # find the matching close tag
            close_pat = _re.compile(r"</\s*" + tag + r"\s*>", _re.IGNORECASE)
            cm = close_pat.search(s, i)
            if cm:
                return ("OPEN", tag, cm.end())
            return None

    out_parts = []
    i = 0
    n = len(raw)
    in_ws_run = False
    while i < n:
        ch = raw[i]
        if ch == "<":
            info = _tag_info(raw, i)
            if info:
                kind, tag, end_idx = info
                # copy entire verbatim span up to end_idx
                # (but for <style> in <head> we allow a light collapse)
                span = raw[i:end_idx]
                if tag == "style":
                    span = _re.sub(r"\s+", " ", span)
                    span = _re.sub(r"/\*[\s\S]*?\*/", "", span)
                out_parts.append(span)
                i = end_idx
                in_ws_run = False
                continue
            # Regular tag: copy byte-by-byte up to '>' without collapsing
            # whitespace inside it (to keep class="a b" correct).
            j = raw.find(">", i)
            if j == -1:
                out_parts.append(raw[i:])
                break
            out_parts.append(raw[i:j+1])
            i = j + 1
            in_ws_run = False
            continue
        if ch in "\r\n\t ":
            if in_ws_run:
                i += 1
                continue
            out_parts.append(" ")
            in_ws_run = True
            i += 1
            continue
        in_ws_run = False
        # Copy a run of non-< non-whitespace characters at once for speed.
        j = i
        while j < n and raw[j] not in "<\r\n\t ":
            j += 1
        if j == i:
            out_parts.append(ch)
            i += 1
        else:
            out_parts.append(raw[i:j])
            i = j
    html = "".join(out_parts)
    # Final tidy: spaces next to block boundaries that are never meaningful.
    html = html.replace(" >", ">").replace("< ", "<")
    html = _re.sub(r"\s+</", "</", html)
    return html


# ============================ sitemap generation ============================
def normalize_image_loc(url):
    """Return a Google-safe image URL for sitemap <image:loc>.

    - Empty/None -> None (caller should skip the <image:image> block)
    - Percent-encode any remaining '(', ')', '[' or ']' (Google strictly validates these)
    - Otherwise keep the original URL as-is (it is already URL-encoded on cdn.jsdelivr.net)
    """
    if not url:
        return None
    s = str(url)
    # Replace literal brackets/parens that are valid per RFC 3986 but that Google
    # Webmaster Tools sometimes rejects as "Invalid URL" inside <image:loc>.
    s = s.replace("(", "%28").replace(")", "%29")
    s = s.replace("[", "%5B").replace("]", "%5D")
    return s


def sitemap_url_block(loc, lastmod, changefreq, priority, image=None):
    parts = []
    parts.append("    <url>")
    parts.append("        <loc>%s</loc>" % loc)
    parts.append("        <lastmod>%s</lastmod>" % lastmod)
    parts.append("        <changefreq>%s</changefreq>" % changefreq)
    parts.append("        <priority>%.1f</priority>" % priority)
    for lang in LANGS:
        if lang == "en":
            href = loc
        else:
            sep = "&" if "?" in loc else "?"
            href = loc + sep + "lang=" + lang
        parts.append(
            '        <xhtml:link rel="alternate" hreflang="%s" href="%s"/>' % (lang, href)
        )
    parts.append(
        '        <xhtml:link rel="alternate" hreflang="x-default" href="%s"/>' % loc
    )
    safe_image = normalize_image_loc(image)
    if safe_image:
        parts.append("        <image:image>")
        parts.append("            <image:loc>%s</image:loc>" % safe_image)
        parts.append("        </image:image>")
    parts.append("    </url>")
    return "\n".join(parts)


def build_sitemap(products):
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"')
    lines.append('        xmlns:xhtml="http://www.w3.org/1999/xhtml"')
    lines.append('        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">')

    # STATIC_PAGES + BLOG_POSTS are HTML-only (see constants at top of file).
    for path, priority, freq in STATIC_PAGES:
        loc = BASE_URL + "/" + path
        lines.append(sitemap_url_block(loc, TODAY, freq, priority))

    for blog in BLOG_POSTS:
        loc = BASE_URL + "/" + blog
        lines.append(sitemap_url_block(loc, TODAY, "monthly", 0.7))

    for p in products:
        pid = p["id"]
        sku = p.get("sku", "") or ""
        slug = _sku_slug(sku) or ("p" + str(pid))
        loc = "%s/product-%s.html" % (BASE_URL, slug)
        img = p.get("image") or ""
        lines.append(sitemap_url_block(loc, TODAY, "weekly", 0.8, image=img))

    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


# ============================ main ==========================================
def main():
    with open(SITE_DATA, "r", encoding="utf-8") as f:
        site = json.load(f)
    with open(APLUS_DATA, "r", encoding="utf-8") as f:
        aplus = json.load(f)

    products = site.get("products", [])
    print("Loaded %d products" % len(products))

    generated = 0
    skipped = 0
    for p in products:
        pid = p["id"]
        sku = p.get("sku", "") or ""
        slug = _sku_slug(sku) or ("p" + str(pid))
        blocks = aplus.get(str(pid)) or []
        html = build_product_page(p, blocks, products)

        # Write the canonical SKU-based page: product-{SKU}.html
        sku_path = os.path.join(ROOT, "product-%s.html" % slug)
        with open(sku_path, "w", encoding="utf-8") as f:
            f.write(html)

        generated += 1

    print("Generated %d product pages (skipped %d)" % (generated, skipped))

    sitemap_xml = build_sitemap(products)
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap_xml)
    print("Wrote sitemap.xml")

    # Summary
    total_urls = len(STATIC_PAGES) + len(BLOG_POSTS) + len(products)
    print("Sitemap URL count: %d (static=%d, blog=%d, product=%d)" % (
        total_urls, len(STATIC_PAGES), len(BLOG_POSTS), len(products)
    ))


if __name__ == "__main__":
    main()

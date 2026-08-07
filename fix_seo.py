#!/usr/bin/env python3
"""Batch fix SEO issues across all HTML pages for Bing Webmaster compliance.

Rules:
- <title>: 30-60 chars
- <meta name="description">: 140-160 chars
- og:title / twitter:title: <= 60 chars
"""

import re
import os

os.chdir('/workspace')

# ── Per-file overrides ──
# Each entry: file -> dict of {field: new_value}
# Fields: title, description, og_title, twitter_title

fixes = {
    'index.html': {
        'description': 'Trusted China sourcing agent for Amazon FBA, TikTok Shop and e-commerce brands. Factory-direct prices, strict QC, end-to-end logistics. Free 24h quote, MOQ from 50 pcs.',
        'og_title': 'China Sourcing Agent | Yeatru Sourcing',
        'twitter_title': 'China Sourcing Agent | Yeatru Sourcing',
    },
    'about.html': {
        'title': 'About Yeatru Sourcing | China Sourcing Agent',
        'og_title': 'About Yeatru Sourcing | China Sourcing Agent',
    },
    'testimonials.html': {
        'title': 'Client Testimonials | Yeatru Sourcing',
        'description': '200+ happy clients, 50+ countries, 98% satisfaction. Real stories from Amazon sellers, TikTok shop owners, and wholesalers who saved 15-30% on sourcing with us.',
    },
    'blog.html': {
        'og_title': 'China Sourcing Blog | Yeatru Sourcing',
    },
    'contact.html': {
        'description': 'Get a free sourcing quote in 24 hours. 200+ clients, 50+ countries. WhatsApp/Email response within 4 hours. Start saving 15-30% on China sourcing today.',
    },
    'products.html': {
        'description': 'Browse 75,000+ wholesale products from Yiwu — kitchenware, home goods, electronics, toys at factory prices. MOQ 50 pcs. Free 24h quote.',
    },
    'services.html': {
        'description': 'Complete China sourcing services: product sourcing, supplier verification, quality control, logistics, OEM customization. For Amazon FBA and wholesale buyers.',
        'og_title': 'China Sourcing Services | Yeatru Sourcing',
    },
    'process.html': {
        'description': '4-step sourcing process: requirements to supplier matching, sample confirmation, production oversight, delivery to your door. Transparent and straightforward.',
        'og_title': 'China Sourcing Process | Yeatru Sourcing',
        'twitter_title': 'China Sourcing Process | Yeatru Sourcing',
    },
    'data.html': {
        'description': 'Yeatru Sourcing data: 200+ clients, 75K suppliers, 50+ countries, 98% satisfaction, 14+ yrs experience. Citable facts for sourcing research.',
        'og_title': 'Yeatru Sourcing Key Data & Statistics',
        'twitter_title': 'Yeatru Sourcing Key Data & Statistics',
    },
    'faq.html': {
        'og_title': 'China Sourcing FAQ | Yeatru Sourcing',
    },
    '404.html': {
        'description': 'The page you are looking for could not be found. Browse our China sourcing services, products, blog, FAQ, or contact us for help.',
    },
    'monitor.html': {
        'description': 'SEO monitor and analytics dashboard for Yeatru Sourcing. Track keyword rankings, backlinks, and page performance.',
    },
    'blog-alibaba-vs-agent.html': {
        'og_title': 'Sourcing Agent vs Alibaba | Yeatru Sourcing',
        'twitter_title': 'Sourcing Agent vs Alibaba | Yeatru Sourcing',
    },
    'blog-amazon-supplier-guide.html': {
        'og_title': 'Find Amazon FBA Suppliers | Yeatru Sourcing',
        'twitter_title': 'Find Amazon FBA Suppliers | Yeatru Sourcing',
    },
    'blog-choosing-sourcing-service-model.html': {
        'og_title': 'Choose Sourcing Service Model | Yeatru Sourcing',
        'twitter_title': 'Choose Sourcing Service Model | Yeatru Sourcing',
    },
    'blog-first-time-china-sourcing.html': {
        'og_title': 'First Time China Sourcing | Yeatru Sourcing',
        'twitter_title': 'First Time China Sourcing | Yeatru Sourcing',
    },
    'blog-private-mold-packaging.html': {
        'og_title': 'Private Mold vs Logo Printing | Yeatru Sourcing',
        'twitter_title': 'Private Mold vs Logo Printing | Yeatru Sourcing',
    },
    'blog-product-certifications.html': {
        'description': 'Plain-English guide to EU and US product compliance marks: CE, FCC, CPC, FDA. What you actually need and what you can skip for Amazon FBA.',
        'og_title': 'EU US Product Certifications | Yeatru Sourcing',
        'twitter_title': 'EU US Product Certifications | Yeatru Sourcing',
    },
    'blog-sea-freight-guide.html': {
        'og_title': 'Sea Freight from China | Yeatru Sourcing',
        'twitter_title': 'Sea Freight from China | Yeatru Sourcing',
    },
    'blog-small-order-service-fee.html': {
        'title': 'Why Agents Charge 7-8% on Small Orders | Yeatru',
        'og_title': 'Why Agents Charge 7-8% on Small Orders',
        'twitter_title': 'Why Agents Charge 7-8% on Small Orders',
    },
    'blog-sourcing-preparation-checklist.html': {
        'description': 'Complete sourcing prep checklist: product specs, MOQ, target price, design files, and market research before contacting a China sourcing agent.',
        'og_title': 'Sourcing Preparation Checklist | Yeatru Sourcing',
        'twitter_title': 'Sourcing Preparation Checklist | Yeatru Sourcing',
    },
    'blog-yiwu-market-guide.html': {
        'description': 'Navigate the world\'s largest small commodity market with 75,000+ booths. Tips on hours, transportation, negotiation tactics, and working with a local agent.',
        'og_title': 'Yiwu Market Buyer Guide | Yeatru Sourcing',
        'twitter_title': 'Yiwu Market Buyer Guide | Yeatru Sourcing',
    },
    'design-photography.html': {
        'description': 'E-commerce product photography & packaging design in China. Amazon-ready visuals boosting CTR 20%+. Logo, box, label design. From $50/project.',
        'og_title': 'Product Design & Photography | Yeatru Sourcing',
    },
    'factory-audit.html': {
        'og_title': 'Factory Audit Service | Yeatru Sourcing',
        'twitter_title': 'Factory Audit Service | Yeatru Sourcing',
    },
    'logistics-shipping.html': {
        'og_title': 'China Logistics & Warehousing | Yeatru Sourcing',
        'twitter_title': 'China Logistics & Warehousing | Yeatru Sourcing',
    },
    'oem.html': {
        'og_title': 'OEM & ODM Service | Yeatru Sourcing',
        'twitter_title': 'OEM & ODM Service | Yeatru Sourcing',
    },
    'payment.html': {
        'og_title': 'Payment Methods | Yeatru Sourcing',
    },
    'price-negotiation.html': {
        'og_title': 'Price Negotiation Service | Yeatru Sourcing',
        'twitter_title': 'Price Negotiation Service | Yeatru Sourcing',
    },
    'product-sourcing.html': {
        'og_title': 'Product Sourcing Service | Yeatru Sourcing',
        'twitter_title': 'Product Sourcing Service | Yeatru Sourcing',
    },
    'quality-control.html': {
        'og_title': 'Quality Control Inspection | Yeatru Sourcing',
        'twitter_title': 'Quality Control Inspection | Yeatru Sourcing',
    },
    'sample-order.html': {
        'description': 'Order samples from China factories risk-free. 100% refundable fees, 3-7 day production, express delivery, sample consolidation, free consultation.',
        'og_title': 'Sample Order Service | Yeatru Sourcing',
        'twitter_title': 'Sample Order Service | Yeatru Sourcing',
    },
    'service-plans.html': {
        'og_title': 'Sourcing Plans & Pricing | Yeatru Sourcing',
        'twitter_title': 'Sourcing Plans & Pricing | Yeatru Sourcing',
    },
    'supplier-verification.html': {
        'og_title': 'Supplier Verification | Yeatru Sourcing',
        'twitter_title': 'Supplier Verification | Yeatru Sourcing',
    },
}


def fix_file(filepath, changes):
    """Apply SEO fixes to a single HTML file."""
    if not os.path.exists(filepath):
        print(f"  SKIP (not found): {filepath}")
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    changed = False

    # --- title tag ---
    if 'title' in changes:
        new_title = changes['title']
        if len(new_title) > 60:
            print(f"  WARN: title still > 60 chars ({len(new_title)}): {new_title}")
        content, n = re.subn(r'<title>[^<]*</title>', f'<title>{new_title}</title>', content, count=1)
        if n:
            print(f"  title: → {new_title} [{len(new_title)} chars]")
            changed = True

    # --- meta description ---
    if 'description' in changes:
        new_desc = changes['description']
        if len(new_desc) > 160:
            print(f"  WARN: description > 160 chars ({len(new_desc)}): {new_desc}")
        elif len(new_desc) < 140:
            print(f"  WARN: description < 140 chars ({len(new_desc)}): {new_desc}")
        content, n = re.subn(
            r'<meta\s+name="description"\s+content="[^"]*"',
            f'<meta name="description" content="{new_desc}"',
            content, count=1
        )
        if n:
            changed = True

    # Also update og:description and twitter:description when meta description changes
    if 'description' in changes:
        new_desc = changes['description']
        # og:description
        content, n1 = re.subn(
            r'<meta\s+property="og:description"\s+content="[^"]*"',
            f'<meta property="og:description" content="{new_desc}"',
            content
        )
        # twitter:description
        content, n2 = re.subn(
            r'<meta\s+name="twitter:description"\s+content="[^"]*"',
            f'<meta name="twitter:description" content="{new_desc}"',
            content
        )
        if n1 or n2:
            changed = True

    # --- og:title ---
    if 'og_title' in changes:
        new_og = changes['og_title']
        if len(new_og) > 60:
            print(f"  WARN: og:title > 60 chars ({len(new_og)}): {new_og}")
        content, n = re.subn(
            r'<meta\s+property="og:title"\s+content="[^"]*"',
            f'<meta property="og:title" content="{new_og}"',
            content
        )
        if n:
            changed = True
        else:
            # Try to insert og:title after og:url or before </head>
            print(f"  INFO: og:title tag not found, searching insertion point...")
            # Insert before </head>
            if '<meta property="og:type"' in content:
                insert_after = '<meta property="og:type"'
                idx = content.find(insert_after)
                end_tag = content.find('>', idx) + 1
                og_line = f'\n    <meta property="og:title" content="{new_og}">'
                content = content[:end_tag] + og_line + content[end_tag:]
                print(f"  og:title: inserted after og:type → {new_og}")
                changed = True

    # --- twitter:title ---
    if 'twitter_title' in changes:
        new_tw = changes['twitter_title']
        if len(new_tw) > 60:
            print(f"  WARN: twitter:title > 60 chars ({len(new_tw)}): {new_tw}")
        content, n = re.subn(
            r'<meta\s+name="twitter:title"\s+content="[^"]*"',
            f'<meta name="twitter:title" content="{new_tw}"',
            content
        )
        if n:
            changed = True
        else:
            # Try to insert before </head>
            if '<meta name="twitter:card"' in content:
                idx = content.find('<meta name="twitter:card"')
                end_tag = content.find('>', idx) + 1
                tw_line = f'\n    <meta name="twitter:title" content="{new_tw}">'
                content = content[:end_tag] + tw_line + content[end_tag:]
                print(f"  twitter:title: inserted after twitter:card → {new_tw}")
                changed = True

    # --- og:type and og:url for pages missing them ---
    og_type_present = 'og:type' in content
    og_url_present = 'og:url' in content
    twitter_card_present = 'twitter:card' in content

    if changed and content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


# Process all files
total = len(fixes)
done = 0
errors = 0

for filename, changes in fixes.items():
    filepath = os.path.join('/workspace', filename)
    print(f"\n{'='*50}")
    print(f"Processing: {filename}")
    if fix_file(filepath, changes):
        print(f"  ✓ FIXED")
        done += 1
    else:
        print(f"  — No changes needed or file not found")

        # Still check if file exists and validate current state
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                c = f.read()
            title = re.search(r'<title>([^<]*)</title>', c)
            desc = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', c)
            if title and len(title.group(1)) > 60:
                print(f"  ⚠️  Title still too long: {title.group(1)} ({len(title.group(1))} chars)")
                errors += 1
            if desc:
                dl = len(desc.group(1))
                if dl > 160:
                    print(f"  ⚠️  Description too long ({dl} chars)")
                    errors += 1
                elif dl < 140:
                    print(f"  ⚠️  Description too short ({dl} chars)")
                    errors += 1

print(f"\n{'='*50}")
print(f"Done: {done}/{total} files fixed, {errors} issues remain")

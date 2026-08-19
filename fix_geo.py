#!/usr/bin/env python3
"""
GEO (Generative Engine Optimization) Fix Script for Yeatru Sourcing Website.

Fixes:
1. Add Speakable JSON-LD to all 25 blog pages
2. Fix Author schema (Neil Liu) on all blog pages - Article and BlogPosting
3. Add FAQPage schema to pages missing it
4. Ensure BreadcrumbList uses absolute URLs
"""

import re
import json
import os
import glob

BASE_DIR = "/workspace/repo"
BLOG_PAGES = sorted(glob.glob(os.path.join(BASE_DIR, "blog-*.html")))
SERVICE_PAGES = [
    "supplier-verification.html",
    "product-sourcing.html",
    "quality-control.html",
    "logistics-shipping.html",
    "price-negotiation.html",
    "factory-audit.html",
    "sample-order.html",
]

NEIL_PERSON = {
    "@type": "Person",
    "name": "Neil Liu",
    "jobTitle": "Founder & Managing Director",
    "url": "https://www.yeatru.com/about.html",
    "sameAs": ["https://www.linkedin.com/in/neil-liu-398983257"]
}

SPEAKABLE_TEMPLATE = '''    <!-- Speakable JSON-LD -->
    <script type="application/ld+json">{"@context":"https://schema.org","@type":"Speakable","name":"__TITLE__ - Audio Version","description":"Audio narration of __TITLE__","duration":"PT5M","transcript":"Full text content available on page"}</script>
'''

DEFAULT_FAQ = '''    <!-- FAQPage JSON-LD -->
    <script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"What does Yeatru Sourcing do?","acceptedAnswer":{"@type":"Answer","text":"Yeatru Sourcing is a professional China sourcing agent that helps international buyers find reliable suppliers, negotiate prices, verify product quality, manage logistics, and handle the entire procurement process from China efficiently."}},{"@type":"Question","name":"How much does a sourcing agent cost?","acceptedAnswer":{"@type":"Answer","text":"Our service fees are transparent and competitive: Order Management service costs 3-4% commission with a minimum of USD 150 per order. Full Sourcing service is tiered: 7-8% below USD 5,000, 5-6% for USD 5,000-20,000, and 4% over USD 20,000, with a minimum of USD 300 per order."}},{"@type":"Question","name":"How do you ensure product quality?","acceptedAnswer":{"@type":"Answer","text":"We ensure quality through a three-level inspection process: incoming material inspection, in-process sampling, and pre-shipment full inspection using AQL 2.5 standard. For Amazon FBA sellers, we offer 100% piece-by-piece inspection and FBA label compliance checks."}},{"@type":"Question","name":"What payment methods do you accept?","acceptedAnswer":{"@type":"Answer","text":"We accept bank transfer (T/T) to our OCBC Hong Kong Branch Global Account, Western Union for urgent payments and smaller amounts, and XTransfer for cross-border transfers. All transactions are secure with import/export license documentation provided."}},{"@type":"Question","name":"How long does shipping take from China?","acceptedAnswer":{"@type":"Answer","text":"Shipping time depends on destination and method: express courier takes 3-7 days door-to-door, air freight takes 5-15 days including customs, and sea freight takes 25-45 days to main ports. We provide all three channels with real-time tracking and DDP options."}}]}</script>
'''

SERVICE_SPECIFIC_FAQS = {
    "supplier-verification.html": '''    <!-- FAQPage JSON-LD -->
    <script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"What is supplier verification?","acceptedAnswer":{"@type":"Answer","text":"Supplier verification is the process of vetting Chinese factories to confirm they are legitimate, have proper business licenses, possess export rights, have claimed production capacity, and meet quality standards before you place an order."}},{"@type":"Question","name":"Why is on-site factory verification important?","acceptedAnswer":{"@type":"Answer","text":"On-site verification confirms the factory actually exists, has real production lines, employs the claimed number of workers, and operates in a proper facility. This eliminates 60% of potential scams and trading companies masquerading as factories."}},{"@type":"Question","name":"How much does supplier verification cost?","acceptedAnswer":{"@type":"Answer","text":"Our Supplier Verification service starts at USD 150 per factory visit. This includes on-site inspection, business license verification, production capacity assessment, quality system check, and a detailed written report with photos."}},{"@type":"Question","name":"How long does verification take?","acceptedAnswer":{"@type":"Answer","text":"A standard supplier verification takes 3-5 business days from request to report. Urgent verification can be completed in 1-2 business days for an additional rush fee."}}]}</script>
''',
    "product-sourcing.html": '''    <!-- FAQPage JSON-LD -->
    <script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"What is the minimum order quantity (MOQ)?","acceptedAnswer":{"@type":"Answer","text":"MOQ varies by product. We work with suppliers that offer flexible MOQ options - regular products start from 50 pieces, suitable for small businesses and startups. Custom OEM products typically require MOQ of 200-500 pieces."}},{"@type":"Question","name":"How long does it take to source a product?","acceptedAnswer":{"@type":"Answer","text":"A typical sourcing cycle runs 4-8 weeks: 1-2 weeks for supplier shortlisting and quotes, 1-2 weeks for samples, 2-4 weeks for bulk production, plus pre-shipment inspection and shipping."}},{"@type":"Question","name":"Can you source any product?","acceptedAnswer":{"@type":"Answer","text":"With 75,000+ verified suppliers, we can source almost any manufactured product - home goods, kitchenware, electronics, toys, apparel, beauty products, pet supplies, and industrial parts."}},{"@type":"Question","name":"Do you handle OEM/ODM customization?","acceptedAnswer":{"@type":"Answer","text":"Yes. We provide full OEM/ODM customization services including product design, logo printing, custom packaging, and private label manufacturing. Customization cycle is typically 20-30 days with MOQ starting from 200 pieces."}}]}</script>
''',
    "quality-control.html": '''    <!-- FAQPage JSON-LD -->
    <script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"What is AQL 2.5 quality control?","acceptedAnswer":{"@type":"Answer","text":"AQL 2.5 is the international Acceptance Quality Limit standard used in pre-shipment inspection. It defines how many units an inspector randomly samples from a batch and how many defects are allowed before the batch is rejected."}},{"@type":"Question","name":"How many inspections do you perform?","acceptedAnswer":{"@type":"Answer","text":"We perform a three-level inspection: incoming material inspection, in-process sampling during production, and pre-shipment full inspection. For Amazon FBA sellers, we offer 100% piece-by-piece inspection."}},{"@type":"Question","name":"What happens if a batch fails inspection?","acceptedAnswer":{"@type":"Answer","text":"If a batch fails AQL 2.5 inspection, we issue a detailed defect report, the factory reworks or replaces defective units, and a re-inspection is scheduled. You do not pay the balance until the batch passes."}},{"@type":"Question","name":"Do you provide inspection reports?","acceptedAnswer":{"@type":"Answer","text":"Yes. Every shipment comes with a detailed quality inspection report including photos, measurements, test results, and AQL findings. Reports are provided in PDF format within 24 hours of inspection completion."}}]}</script>
''',
    "logistics-shipping.html": '''    <!-- FAQPage JSON-LD -->
    <script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"What are my shipping options from China?","acceptedAnswer":{"@type":"Answer","text":"We offer three main shipping channels: express courier (DHL/FedEx/UPS) for 3-7 days door-to-door, air freight for 5-15 days, and sea freight for 25-45 days to main ports. We also offer DDP door-to-door options."}},{"@type":"Question","name":"What is the difference between LCL and FCL?","acceptedAnswer":{"@type":"Answer","text":"LCL (Less Than Container Load) shares a container with other shipments, making it economical for small orders. FCL (Full Container Load) gives you exclusive use of a 20ft or 40ft container, ideal for large orders over 15 cubic meters."}},{"@type":"Question","name":"Do you handle customs clearance?","acceptedAnswer":{"@type":"Answer","text":"We handle export customs clearance from China and provide all necessary documentation (commercial invoice, packing list, bill of lading, certificates of origin). For import clearance, we partner with destination brokers."}},{"@type":"Question","name":"How much does shipping cost?","acceptedAnswer":{"@type":"Answer","text":"Shipping costs depend on weight, volume, destination, and method. Express courier starts at around $5-8 per kg, air freight at $3-5 per kg, and sea freight at $200-400 per cubic meter. Contact us for a personalized quote."}}]}</script>
''',
    "price-negotiation.html": '''    <!-- FAQPage JSON-LD -->
    <script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"How much can I save with price negotiation?","acceptedAnswer":{"@type":"Answer","text":"Our professional negotiation team can help you save an average of 15-30% compared to buying directly on Alibaba. We leverage our established supplier relationships and volume commitments to secure factory-direct prices."}},{"@type":"Question","name":"Why do agents get better prices than direct buyers?","acceptedAnswer":{"@type":"Answer","text":"Chinese suppliers give 15-30% better prices to local buying agents than to direct international buyers. This is because agents bring repeat business, can communicate in Chinese, and understand local negotiation dynamics."}},{"@type":"Question","name":"What negotiation tactics do you use?","acceptedAnswer":{"@type":"Answer","text":"We use bulk purchase discounts, long-term cooperation commitments, payment term negotiations, product specification adjustments, and multi-supplier competition to drive down prices."}},{"@type":"Question","name":"Will the price negotiation service delay my order?","acceptedAnswer":{"@type":"Answer","text":"No. Price negotiation is integrated into our standard sourcing process. We handle negotiation alongside supplier verification and sampling, adding no extra delay to your timeline."}}]}</script>
''',
    "factory-audit.html": '''    <!-- FAQPage JSON-LD -->
    <script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"What does a factory audit include?","acceptedAnswer":{"@type":"Answer","text":"A factory audit includes: on-site facility inspection, production line assessment, quality management system evaluation, worker interview, machinery and equipment check, raw material sourcing verification, and a comprehensive written report with photos."}},{"@type":"Question","name":"How much does a factory audit cost?","acceptedAnswer":{"@type":"Answer","text":"Factory audits start at USD 200 per site visit. This includes a full day's on-site inspection, photo documentation, and a detailed report. Multiple factory audits are available at a discounted rate."}},{"@type":"Question","name":"How long does a factory audit take?","acceptedAnswer":{"@type":"Answer","text":"A standard factory audit takes one full day on-site plus 1-2 days for report compilation. Urgent audits can be completed within 24-48 hours of request."}},{"@type":"Question","name":"Can I visit the factories personally?","acceptedAnswer":{"@type":"Answer","text":"Yes! We organize factory tours in Yiwu, Guangzhou, Shenzhen, and other manufacturing hubs. We arrange transportation, translation, and meeting agendas for visiting buyers."}}]}</script>
''',
    "sample-order.html": '''    <!-- FAQPage JSON-LD -->
    <script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"How long does it take to get samples?","acceptedAnswer":{"@type":"Answer","text":"Standard samples take 3-7 days, custom samples take 7-15 days. Sample fees vary by product, typically 50-500 RMB. Sample fees are fully refundable for bulk orders over 1,000 pieces."}},{"@type":"Question","name":"Can I get free samples?","acceptedAnswer":{"@type":"Answer","text":"Most suppliers charge a sample fee to cover material and labor costs. However, sample fees are fully refundable when you place a bulk order. We also provide free sample consultation to help select the best suppliers."}},{"@type":"Question","name":"How many samples should I order?","acceptedAnswer":{"@type":"Answer","text":"We recommend ordering 2-3 samples from different suppliers for comparison. This allows you to evaluate quality, weight, material, and packaging side by side before committing to a bulk order."}},{"@type":"Question","name":"Can you consolidate samples from multiple suppliers?","acceptedAnswer":{"@type":"Answer","text":"Yes. We can consolidate samples from multiple suppliers into one shipment to save on shipping costs. This is especially useful when comparing products across different factories."}}]}</script>
''',
}


def extract_blog_title(content):
    """Extract blog title from the title tag."""
    title_match = re.search(r'<title>(.*?)</title>', content, re.DOTALL)
    if title_match:
        raw = title_match.group(1).strip()
        # Split on | and take first part
        if '|' in raw:
            return raw.split('|')[0].strip()
        return raw.strip()
    return "This Article"


def find_jsonld_blocks(content):
    """Find all JSON-LD script blocks and return (start, end, json_str) tuples."""
    blocks = []
    pattern = r'<script\s+type="application/ld\+json">(.*?)</script>'
    for m in re.finditer(pattern, content, re.DOTALL):
        json_str = m.group(1).strip()
        blocks.append((m.start(), m.end(), json_str, m.group(0)))
    return blocks


def fix_jsonld_authors(content):
    """Fix Article and BlogPosting author fields in all JSON-LD blocks."""
    blocks = find_jsonld_blocks(content)
    if not blocks:
        return content

    # Process blocks in reverse to preserve positions
    new_content = content
    for start, end, json_str, full_match in reversed(blocks):
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError:
            continue

        if not isinstance(data, dict):
            continue

        changed = False

        # Fix Article author
        if data.get("@type") == "Article":
            author = data.get("author", {})
            if isinstance(author, dict):
                old_name = author.get("name", "")
                if old_name and old_name != "Neil Liu":
                    data["author"] = NEIL_PERSON
                    changed = True

        # Fix BlogPosting author
        if data.get("@type") == "BlogPosting":
            author = data.get("author", {})
            if isinstance(author, dict):
                old_type = author.get("@type", "")
                old_name = author.get("name", "")
                if old_type != "Person" or old_name != "Neil Liu":
                    data["author"] = NEIL_PERSON
                    changed = True

        if changed:
            new_json = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
            new_block = f'<script type="application/ld+json">{new_json}</script>'
            new_content = new_content[:start] + new_block + new_content[end:]

    return new_content


def has_speakable(content):
    """Check if content already has a Speakable schema."""
    blocks = find_jsonld_blocks(content)
    for start, end, json_str, full_match in blocks:
        try:
            data = json.loads(json_str)
            if isinstance(data, dict) and data.get("@type") == "Speakable":
                return True
        except json.JSONDecodeError:
            pass
    return False


def has_faqpage(content):
    """Check if content already has a FAQPage schema."""
    blocks = find_jsonld_blocks(content)
    for start, end, json_str, full_match in blocks:
        try:
            data = json.loads(json_str)
            if isinstance(data, dict) and data.get("@type") == "FAQPage":
                return True
            if isinstance(data, dict) and "@graph" in data:
                for item in data.get("@graph", []):
                    if isinstance(item, dict) and item.get("@type") == "FAQPage":
                        return True
        except json.JSONDecodeError:
            pass
    return False


def add_speakable(content, blog_title):
    """Add Speakable JSON-LD after the BreadcrumbList block."""
    if has_speakable(content):
        return content

    speakable = SPEAKABLE_TEMPLATE.replace("__TITLE__", blog_title)

    # Find the BreadcrumbList block
    blocks = find_jsonld_blocks(content)
    last_bc_end = None
    for start, end, json_str, full_match in blocks:
        try:
            data = json.loads(json_str)
            if isinstance(data, dict) and data.get("@type") == "BreadcrumbList":
                last_bc_end = end
        except json.JSONDecodeError:
            pass

    if last_bc_end:
        insert_pos = last_bc_end
        return content[:insert_pos] + '\n' + speakable + content[insert_pos:]

    # Fallback: insert before Yeatru Site Schema
    site_schema_start = content.find('<!-- Yeatru Site Schema')
    if site_schema_start == -1:
        site_schema_start = content.find('<!-- Yeatru Site Schema START')
    if site_schema_start != -1:
        last_script = content.rfind('</script>', 0, site_schema_start)
        if last_script != -1:
            insert_pos = last_script + len('</script>')
            return content[:insert_pos] + '\n' + speakable + content[insert_pos:]

    # Fallback: before </head>
    head_end = content.find('</head>')
    if head_end != -1:
        return content[:head_end] + '\n' + speakable + '\n' + content[head_end:]
    return content


def add_faqpage(content, faq_text):
    """Add FAQPage JSON-LD after the BreadcrumbList block."""
    if has_faqpage(content):
        return content

    # Find the best insertion point - after BreadcrumbList or after last JSON-LD before site schema
    blocks = find_jsonld_blocks(content)
    last_jsonld_end = None

    # Look for the last block before the Yeatru Site Schema
    site_schema_start = content.find('<!-- Yeatru Site Schema')
    if site_schema_start == -1:
        site_schema_start = content.find('<!-- Yeatru Site Schema START')

    for start, end, json_str, full_match in blocks:
        if site_schema_start != -1 and start > site_schema_start:
            break
        last_jsonld_end = end

    if last_jsonld_end:
        insert_pos = last_jsonld_end
        return content[:insert_pos] + '\n' + faq_text + content[insert_pos:]

    # Fallback: before </head>
    head_end = content.find('</head>')
    if head_end != -1:
        return content[:head_end] + '\n' + faq_text + '\n' + content[head_end:]
    return content


def fix_breadcrumb_urls(content):
    """Ensure BreadcrumbList uses absolute URLs."""
    blocks = find_jsonld_blocks(content)
    new_content = content
    for start, end, json_str, full_match in reversed(blocks):
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError:
            continue

        if not isinstance(data, dict) or data.get("@type") != "BreadcrumbList":
            continue

        changed = False
        items = data.get("itemListElement", [])
        for item in items:
            if isinstance(item, dict):
                item_url = item.get("item", "")
                if item_url and not item_url.startswith("http"):
                    item["item"] = "https://www.yeatru.com/" + item_url.lstrip("/")
                    changed = True

        if changed:
            new_json = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
            new_block = f'<script type="application/ld+json">{new_json}</script>'
            new_content = new_content[:start] + new_block + new_content[end:]

    return new_content


def process_blog_pages():
    """Process all 25 blog pages."""
    updated_count = 0
    for filepath in BLOG_PAGES:
        filename = os.path.basename(filepath)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content
        blog_title = extract_blog_title(content)

        # Fix Article and BlogPosting authors
        content = fix_jsonld_authors(content)

        # Add Speakable
        content = add_speakable(content, blog_title)

        # Add FAQPage if missing
        faq_text = SERVICE_SPECIFIC_FAQS.get(filename, DEFAULT_FAQ)
        content = add_faqpage(content, faq_text)

        # Fix BreadcrumbList URLs
        content = fix_breadcrumb_urls(content)

        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  Updated: {filename}")
            updated_count += 1
        else:
            print(f"  No changes needed: {filename}")

    return updated_count


def process_service_pages():
    """Process service pages to add FAQPage."""
    updated_count = 0
    for page_name in SERVICE_PAGES:
        filepath = os.path.join(BASE_DIR, page_name)
        if not os.path.exists(filepath):
            print(f"  Not found: {page_name}")
            continue

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content

        # Add FAQPage if missing
        faq_text = SERVICE_SPECIFIC_FAQS.get(page_name, DEFAULT_FAQ)
        content = add_faqpage(content, faq_text)

        # Fix BreadcrumbList URLs
        content = fix_breadcrumb_urls(content)

        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  Updated: {page_name}")
            updated_count += 1
        else:
            print(f"  No changes needed: {page_name}")

    return updated_count


def validate_json_ld(filepath):
    """Validate JSON-LD blocks in a file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    issues = []
    blocks = find_jsonld_blocks(content)

    for i, (start, end, json_str, full_match) in enumerate(blocks):
        if not json_str:
            issues.append(f"Empty JSON-LD block #{i+1}")
            continue
        try:
            json.loads(json_str)
        except json.JSONDecodeError as e:
            snippet_start = max(0, e.pos - 30)
            snippet_end = min(len(json_str), e.pos + 30)
            snippet = repr(json_str[snippet_start:snippet_end])
            issues.append(f"Invalid JSON in block #{i+1} (pos {start}): {str(e)[:80]} | around: {snippet}")

    return issues


def validate_all():
    """Validate JSON-LD in all processed files."""
    print("\n" + "=" * 60)
    print("Validating JSON-LD...")
    print("=" * 60)

    files_to_check = BLOG_PAGES + [
        os.path.join(BASE_DIR, p) for p in SERVICE_PAGES
    ]

    error_count = 0
    for filepath in files_to_check:
        if not os.path.exists(filepath):
            continue
        issues = validate_json_ld(filepath)
        filename = os.path.basename(filepath)
        if issues:
            print(f"  ERROR {filename}:")
            for issue in issues:
                print(f"    - {issue}")
            error_count += 1
        else:
            print(f"  OK: {filename}")

    print(f"\nValidation complete: {error_count} files with issues")
    return error_count == 0


if __name__ == "__main__":
    print("=" * 60)
    print("GEO Fix Script for Yeatru Sourcing")
    print("=" * 60)

    print(f"\nBlog pages found: {len(BLOG_PAGES)}")
    print(f"Service pages to process: {len(SERVICE_PAGES)}")

    print("\n--- Processing Blog Pages ---")
    blog_updated = process_blog_pages()
    print(f"\nBlog pages updated: {blog_updated}")

    print("\n--- Processing Service Pages ---")
    svc_updated = process_service_pages()
    print(f"\nService pages updated: {svc_updated}")

    print(f"\nTotal pages updated: {blog_updated + svc_updated}")

    # Validate
    all_valid = validate_all()
    if all_valid:
        print("\nAll JSON-LD blocks are valid!")
    else:
        print("\nSome JSON-LD blocks have issues - see above.")
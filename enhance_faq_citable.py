#!/usr/bin/env python3
"""Enhance product page FAQ answers with SKU-specific citable first sentences.

For each of the 7 FAQs, prepend a standalone, AI-citable assertion sentence
that includes the SKU and (where relevant) the MOQ/materials. Updates both the
visible <details> FAQ answers and the JSON-LD FAQPage to keep them in sync.
"""
import glob, re, json, os

SITE = "https://www.yeatru.com"

# FAQ question -> citable first-sentence template (uses {sku}, {moq}, {materials})
FAQ_ASSERTIONS = {
    "What is the minimum order quantity (MOQ)?":
        "The minimum order quantity (MOQ) for SKU {sku} is {moq} unit(s). ",
    "What materials are used in your products?":
        "SKU {sku} is manufactured using {materials} sourced from certified Chinese suppliers. ",
    "How long is the production lead time?":
        "The production lead time for SKU {sku} is 15–30 days, plus 5–7 days for international shipping. ",
    "Can I customize colors, sizes, or logos?":
        "Yes, SKU {sku} supports OEM/ODM customization including colors, sizes, logos, and packaging. ",
    "What payment methods do you accept?":
        "Yeatru accepts XTransfer, LianLian, Airwallex, T/T, and PayPal for SKU {sku} orders. ",
    "Do you provide samples?":
        "Yes, samples are available for SKU {sku} and typically ship within 3–5 business days. ",
    "What is your quality guarantee?":
        "SKU {sku} undergoes AQL 2.5 quality inspection before shipment, with optional SGS or Bureau Veritas third-party inspection. ",
}

# Idempotency marker: if the answer already contains this phrase, skip.
IDEMPOTENCY_MARKER = "for SKU"


def extract_spec(h, label):
    """Extract the value of a spec card by its label text (e.g. 'MOQ', 'Material')."""
    m = re.search(
        r'<span class="spec-label"><i class="fas [^"]+"></i>\s*' + re.escape(label) + r'</span>\s*<span class="spec-value">([^<]*)</span>',
        h,
    )
    return m.group(1).strip() if m else ""


def extract_faqpage_jsonld(h):
    for m in re.finditer(r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>', h, re.S):
        try:
            d = json.loads(m.group(1))
            if d.get("@type") == "FAQPage":
                return m, d
        except json.JSONDecodeError:
            continue
    return None, None


def process_product(fpath):
    h = open(fpath, encoding="utf-8").read()
    sku = os.path.basename(fpath).replace("product-", "").replace(".html", "")
    moq = extract_spec(h, "MOQ") or "100"
    materials = extract_spec(h, "Material") or "high-quality certified materials"

    # Build assertion map for this SKU
    assertions = {}
    for q, tmpl in FAQ_ASSERTIONS.items():
        assertions[q] = tmpl.format(sku=sku, moq=moq, materials=materials)

    modified = False

    # 1. Update JSON-LD FAQPage answers
    fm, fdata = extract_faqpage_jsonld(h)
    if fdata:
        for qa in fdata.get("mainEntity", []):
            q = qa.get("name", "")
            ans = qa.get("acceptedAnswer", {})
            text = ans.get("text", "")
            if q in assertions and IDEMPOTENCY_MARKER not in text:
                ans["text"] = assertions[q] + text
                modified = True
        if modified:
            new_json = json.dumps(fdata, ensure_ascii=False)
            h = h[:fm.start(1)] + new_json + h[fm.end(1):]

    # 2. Update visible HTML FAQ answers
    # Pattern: <details class="faq-item"> <summary>...Q...</summary> <div class="faq-answer"><p>...A...</p></div> </details>
    # We match each details block and update the <p> inside faq-answer
    def replace_faq_answer(match):
        block = match.group(0)
        summary_m = re.search(r"<summary>[^<]*(?:<i[^>]*></i>)?\s*([^<]+)</summary>", block)
        if not summary_m:
            return block
        q = summary_m.group(1).strip()
        if q not in assertions:
            return block
        # Find the <p>...</p> inside faq-answer
        p_m = re.search(r'(<div class="faq-answer"><p>)(.*?)(</p>)', block, re.S)
        if not p_m:
            return block
        existing = p_m.group(2)
        if IDEMPOTENCY_MARKER in existing:
            return block
        new_p = f'{p_m.group(1)}{assertions[q]}{existing}{p_m.group(3)}'
        return block[:p_m.start()] + new_p + block[p_m.end():]

    h = re.sub(
        r'<details class="faq-item">.*?</details>',
        replace_faq_answer,
        h,
        flags=re.S,
    )

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(h)
    return f"OK {fpath}: moq={moq}, materials={materials[:30]}"


if __name__ == "__main__":
    files = sorted(glob.glob("product-YCS-*.html"))
    ok = 0
    for f in files:
        r = process_product(f)
        ok += 1
    print(f"Done: {ok} product pages FAQ-enhanced")

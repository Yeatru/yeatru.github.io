#!/usr/bin/env python3
"""
为所有博客添加：
1. "Common Pitfalls to Avoid" 节（如果没有）—— 按博客主题分类，内容准确且与主题相关
2. 在 Conclusion 中添加到相关支柱文章的内链（Incoterms / DDP / Warehousing / Customs Clearance）

只在 article-content 体内、Conclusion 之前插入 Common Pitfalls。
"""
import os
import re
import sys

ROOT = "/workspace"
SITE = "https://www.yeatru.com"

# 主题分类：关键词 → 对应的 Common Pitfalls 内容
CATEGORIES = {
    "payment": {
        "keywords": ["pay", "payment", "bank", "transfer", "deposit", "t/t", "tt", "paypal", "xtransfer", "trade assurance", "codex", "50-50"],
        "pitfalls": [
            "<strong>Wiring to a personal account instead of the company account.</strong> Always confirm the PI beneficiary name matches the supplier's business license. A personal account = red flag for fraud or tax evasion, and you lose all payment protection.",
            "<strong>No bank-detail re-verification before the balance transfer.</strong> Hackers infiltrate supplier email and send a 'new account' notice mid-order. Re-confirm bank details by phone or WeChat call before every wire over $5,000.",
            "<strong>Paying 100% upfront without a QC gate.</strong> Structure 50/50 with an AQL 2.5 pre-shipment inspection before the balance. Once the full amount is paid, you have zero leverage over defects.",
            "<strong>Ignoring SWIFT cost-sharing (SHA vs OUR).</strong> SHA splits fees ($25–$45 total) but the supplier receives $15–$25 less. OUR costs you ~$55–$60 upfront but guarantees the full amount arrives. For deposits over $10k, OUR avoids short-payment disputes.",
            "<strong>No written payment terms in the contract.</strong> Specify due dates, currency, bank charges, and late-payment penalties. Verbal agreements are unenforceable in Chinese courts.",
        ],
    },
    "qc": {
        "keywords": ["qc", "quality", "inspection", "aql", "defect", "rework"],
        "pitfalls": [
            "<strong>Skipping pre-shipment inspection.</strong> Once the container is sealed and at sea, defects cannot be returned to the factory. A $150 AQL 2.5 inspection catches $1,000+ in defects before they cross the Pacific.",
            "<strong>Using the wrong AQL level.</strong> AQL 2.5/4.0 is standard for consumer goods; 0.65 for medical/safety products, 4.0 for low-value commodities. The wrong level either over-inspects (wasting money) or under-inspects (missing defects).",
            "<strong>Inspecting at the factory without photo/video evidence.</strong> A verbal 'pass' report is worthless when you receive 200 broken units. Demand dated photos of every defect category and a sealed sample retained at the factory.",
            "<strong>No defect rework timeline in the contract.</strong> Specify that defects must be reworked within 3–5 days at the factory's cost, with a re-inspection before shipment. Without this, factories delay rework indefinitely.",
            "<strong>Confusing 'passed QC' with 'guaranteed quality'.</strong> AQL sampling statistically estimates defect rate — it does not guarantee zero defects. Budget 1–3% for post-shipment defects and include a defect-credit clause in the contract.",
        ],
    },
    "shipping": {
        "keywords": ["shipping", "freight", "sea", "air", "ddp", "fob", "exw", "incoterm", "express", "courier", "tracking", "warehous", "consolidat", "customs", "clearance", "duty", "tariff"],
        "pitfalls": [
            "<strong>Accepting a flat DDP rate without line items.</strong> A real DDP quote breaks out freight, duty, VAT, clearance, and last-mile. A single per-kg number hides costs that surface as surprise invoices or low-quality service.",
            "<strong>Choosing CIF for control of freight.</strong> Under CIF the supplier picks the carrier and inflates freight by 15–25%. Choose FOB (you control the line) or DDP (all-in, your forwarder) — never CIF unless you have no other option.",
            "<strong>No transit-time buffer for FBA restocks.</strong> Sea freight from China runs 25–40 days + 5–7 days FBA receiving. Order 45–60 days before you need stock in FBA, not 30. Running out of stock kills your Amazon ranking.",
            "<strong>Ignoring ISPM-15 for wooden pallets.</strong> EU and US customs require heat-treated pallets with the IPPC stamp. Missing stamps = container detained, €400–$600 fumigation, 3–7 day delay.",
            "<strong>No cargo insurance.</strong> Freight forwarders' liability is limited to ~$2/kg by convention. For high-value cargo, buy separate all-risks insurance (0.3–0.5% of value) — it costs $50 and pays out $10,000.",
        ],
    },
    "certification": {
        "keywords": ["certif", "ce", "fcc", "cpc", "rohs", "fda", "ukca", "reach", "compliance", "phytosanitary", "ciq"],
        "pitfalls": [
            "<strong>Using the supplier's test report without verification.</strong> Many factories provide fake or expired CE/FCC reports. Verify the report number on the certification body's website before placing a bulk order.",
            "<strong>Applying the wrong certification for the destination market.</strong> CE for EU, FCC/CPC for US, UKCA for UK, RCM for Australia. Shipping CE-marked goods to the US = customs seizure and $10k+ fines.",
            "<strong>No test report for the exact product variant.</strong> A CE report for a red 220V version does not cover a blue 110V version. Each variant needs its own test or a report covering all variants.",
            "<strong>Forgetting ongoing compliance.</strong> Regulations change (e.g., EU GPSR replacing GPSD, US CPSC updates). A cert valid today may be invalid in 12 months. Track renewal dates and budget for re-testing.",
            "<strong>Under-declaring product category to skip certification.</strong> Listing a children's toy as 'home decoration' to avoid CPC is customs fraud. The buyer of record (you) carries the liability.",
        ],
    },
    "oem": {
        "keywords": ["oem", "odm", "private label", "mold", "packaging", "custom", "product design", "apparel", "electronics", "beauty", "skin"],
        "pitfalls": [
            "<strong>No written mold/drawing ownership contract.</strong> By default Chinese law treats the factory as the mold owner. Your contract must state you own the mold, drawings, and tooling upon full payment, with retrieval rights.",
            "<strong>Signing no NDA before sharing designs.</strong> A factory can legally sell your custom design to competitors if there's no NDA. Sign before sending any CAD files, samples, or spec sheets.",
            "<strong>Approving production without a signed golden sample.</strong> A verbal 'looks good' leads to 5,000 units that don't match your expectation. Sign and retain a golden sample; production must match it exactly.",
            "<strong>No MOQ flexibility in the contract.</strong> A 5,000-unit MOQ for your first order is risky. Negotiate a 1,000–2,000 trial MOQ at a slightly higher unit price, then scale up after quality is confirmed.",
            "<strong>Skipping IP registration in China.</strong> Register your trademark and design patent in China (not just your home country). Chinese trademark law is first-to-file — a factory or competitor can squat your brand if you don't register first.",
        ],
    },
    "sourcing_agent": {
        "keywords": ["sourcing agent", "buying office", "trading company", "agent vs", "how to choose", "how much", "what is a sourcing", "low-moq", "first-time"],
        "pitfalls": [
            "<strong>Choosing the cheapest agent without due diligence.</strong> Commission below 2% is usually subsidized by factory kickbacks or hidden markups — you pay more in inflated goods cost. A real 3–8% fee with transparency costs less.",
            "<strong>Not verifying the business license.</strong> Look up the agent on gsxt.gov.cn (National Enterprise Credit Information). Confirm the business scope lists 代理 (agency), registered capital $50k+, and no abnormal operation status.",
            "<strong>No 3 client references in your category.</strong> Ask for 3 buyers who sourced a similar product in the last 6 months and actually call them. Verify delivery, defect rate, and fee transparency.",
            "<strong>Refusing to share the factory name.</strong> A reputable agent discloses the factory and lets you pay the factory directly. An agent that hides the factory is marking up the goods price, not just charging a fee.",
            "<strong>No contract with QC and defect-liability terms.</strong> Sign an agreement covering NDA, IP protection, QC pass criteria (AQL level), and who pays for rework. A handshake deal leaves you with no recourse.",
        ],
    },
    "yiwu_market": {
        "keywords": ["yiwu", "market", "1688", "wholesale"],
        "pitfalls": [
            "<strong>Visiting Yiwu without a pre-trip product list.</strong> The market has 75,000+ booths across 5 districts. Without a targeted list, you waste days walking and buy on impulse. Research products and target districts before you go.",
            "<strong>Buying from the first booth you see.</strong> The same product is often sold by 20+ booths at different prices and quality. Walk at least 3 booths in the same district before committing.",
            "<strong>No consolidation plan.</strong> Buying from 10 booths means 10 separate shipments. Arrange a consolidation warehouse before you go — it saves 30–50% on international freight.",
            "<strong>Accepting 'sample price' as the bulk price.</strong> Booth prices are sample prices (1–5 pcs). Always negotiate the bulk (MOQ) price, packaging, and lead time in writing before leaving the booth.",
            "<strong>Ignoring minimum order quantities.</strong> Many Yiwu booths have MOQs of 1–2 cartons. If you need smaller quantities, ask about mixed-carton or sample-box pricing before negotiating.",
        ],
    },
    "amazon_fba": {
        "keywords": ["fba", "amazon", "restock", "tiktok shop"],
        "pitfalls": [
            "<strong>Shipping without FBA prep in China.</strong> FBA charges $0.50–$1.50/unit for polybagging and labeling in the US. Doing it in China costs $0.05–$0.15/unit — a 90% saving on 1,000 units = $500–$1,000.",
            "<strong>Wrong FNSKU labels or case-pack rules.</strong> Mislabeled units = FBA receiving delays, $0.15/unit relabeling fee, and potential account flags. Verify label placement and case-pack quantities before shipping.",
            "<strong>No compliance documentation for restricted categories.</strong> Children's products need CPC, electronics need FCC, food-contact needs FDA. Missing docs = FBA inventory destroyed, not returned.",
            "<strong>Underestimating FBA receiving time.</strong> FBA takes 3–7 days to check in inventory after arrival. Factor this into your restock timeline alongside the 25–40 day sea freight.",
            "<strong>Running out of stock.</strong> A stockout drops your Amazon BSR and you lose ranking to competitors. Maintain a 30-day safety stock and order 45–60 days before depletion.",
        ],
    },
    "compliance_ethical": {
        "keywords": ["ethical", "csddd", "uflpa", "forced labor", "sustainable", "social", "audit", "sa8000"],
        "pitfalls": [
            "<strong>No tier-2 supplier traceability.</strong> EU CSDDD and US UFLPA require tracing raw materials to the mine/farm level. A factory audit alone is insufficient — you must map the entire supply chain.",
            "<strong>Relying on the factory's self-declared audit.</strong> SA8000/BSCI audits paid by the factory are often stage-managed. Use an independent auditor and unannounced visits for high-risk categories.",
            "<strong>No written code of conduct with suppliers.</strong> A signed supplier code of conduct (covering wages, hours, child labor, safety) is the first document CSDDD auditors request. Without it, you cannot demonstrate due diligence.",
            "<strong>Ignoring forced-labor risk indicators.</strong> Excessive overtime, wage deductions, restricted movement, and no labor contracts are red flags. Even one high-risk supplier can expose your entire import to UFLPA detention.",
            "<strong>No ongoing monitoring.</strong> An audit is a snapshot, not a guarantee. Re-audit high-risk suppliers every 6 months and include a right-to-audit clause in every supply contract.",
        ],
    },
    "default": {
        "keywords": [],
        "pitfalls": [
            "<strong>No written contract.</strong> A PO or email exchange is not a contract. Sign a detailed agreement covering price, MOQ, lead time, QC standards, defect liability, payment terms, and IP protection before placing any order.",
            "<strong>Paying 100% upfront.</strong> Structure payments as 50% deposit + 50% balance after pre-shipment QC. Paying everything upfront removes your leverage over quality and delivery.",
            "<strong>Skipping pre-shipment inspection.</strong> Once cargo is at sea, you cannot return defects. An AQL 2.5 inspection ($150–$300) catches $1,000+ in defects before shipping.",
            "<strong>No clear product specification sheet.</strong> A verbal description leads to 5,000 units that don't match your expectation. Provide written specs: dimensions, materials, tolerances, labeling, packaging, and a signed golden sample.",
            "<strong>Ignoring destination compliance.</strong> Confirm required certifications (CE, FCC, CPC, RoHS) and labeling rules before production. Fixing non-compliance after arrival costs 5–10x more than getting it right in China.",
        ],
    },
}

# 支柱文章内链（按主题匹配）
PILLAR_LINKS = {
    "shipping": ['<a href="blog-incoterms-china-sourcing.html">Incoterms EXW/FOB/DDP comparison</a>', '<a href="blog-china-ddp-shipping-agent.html">DDP door-to-door shipping guide</a>', '<a href="blog-warehousing-consolidation.html">China warehousing &amp; consolidation</a>'],
    "certification": ['<a href="blog-product-certifications-china.html">China product certifications guide</a>'],
    "payment": ['<a href="blog-50-50-deposit-china.html">50/50 deposit payment terms</a>'],
    "qc": ['<a href="blog-china-quality-control-inspection.html">China quality control inspection guide</a>'],
    "oem": ['<a href="blog-private-mold-packaging.html">private mold vs logo printing</a>'],
    "sourcing_agent": ['<a href="blog-how-to-choose-sourcing-agent.html">how to choose a sourcing agent</a>', '<a href="blog-how-much-sourcing-agents-charge.html">sourcing agent fees</a>'],
    "default": ['<a href="blog-how-to-choose-sourcing-agent.html">how to choose a sourcing agent</a>', '<a href="blog-incoterms-china-sourcing.html">Incoterms comparison</a>'],
}


def categorize(filename, html):
    """根据文件名和 HTML 内容（标题）分类。"""
    text = filename.lower() + " "
    # 取 H1 标题文本
    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
    if h1:
        text += re.sub(r'<[^>]+>', '', h1.group(1)).lower() + " "
    # 取 description
    desc = re.search(r'<meta name="description" content="([^"]*)"', html, re.IGNORECASE)
    if desc:
        text += desc.group(1).lower()

    scores = {}
    for cat, info in CATEGORIES.items():
        if cat == "default":
            continue
        score = sum(1 for kw in info["keywords"] if kw in text)
        scores[cat] = score
    best = max(scores, key=scores.get)
    if scores[best] >= 1:
        return best
    return "default"


def add_common_pitfalls(html, category):
    """在 Conclusion 之前插入 Common Pitfalls 节（如果不存在）。"""
    if re.search(r'<h2[^>]*>Common Pitfalls', html, re.IGNORECASE):
        return html, False

    info = CATEGORIES[category]
    items = "".join(f"<li>{p}</li>\n" for p in info["pitfalls"])
    section = (
        '<h2>Common Pitfalls to Avoid</h2>\n'
        f'<ul>\n{items}</ul>\n'
    )
    # 在 Conclusion 之前插入
    pattern = re.compile(r'(<h2[^>]*>Conclusion</h2>)', re.IGNORECASE)
    new_html, n = pattern.subn(section + r'\1', html, count=1)
    if n == 0:
        # 没有 Conclusion，在 author-bio 之前插入
        pattern = re.compile(r'(<aside class="author-bio)')
        new_html, n = pattern.subn(section + r'\1', html, count=1)
    return new_html, n > 0


def add_pillar_links(html, category):
    """在 Conclusion 段落末尾添加支柱文章内链（如果已有则跳过）。"""
    links = PILLAR_LINKS.get(category, PILLAR_LINKS["default"])
    # 检查 Conclusion 段落后是否已有内链到这些文章
    conclusion_match = re.search(r'(<h2[^>]*>Conclusion</h2>.*?)(?=<h2|<aside class="author-bio|</article>)', html, re.DOTALL | re.IGNORECASE)
    if not conclusion_match:
        return html, False
    conclusion_text = conclusion_match.group(1)
    # 检查是否已包含任何支柱链接
    for link in links:
        href = re.search(r'href="([^"]+)"', link).group(1)
        if href in conclusion_text:
            return html, False  # 已有内链，跳过

    # 在 Conclusion 最后一个 </p> 前插入
    insert_text = ' Related: ' + ', '.join(links) + '.'
    # 找到 Conclusion 块中最后一个 </p>
    last_p = conclusion_text.rfind('</p>')
    if last_p == -1:
        return html, False
    new_conclusion = conclusion_text[:last_p] + insert_text + conclusion_text[last_p:]
    new_html = html[:conclusion_match.start()] + new_conclusion + html[conclusion_match.end():]
    return new_html, True


def main():
    files = sorted(
        os.path.join(ROOT, n)
        for n in os.listdir(ROOT)
        if n.startswith("blog-") and n.endswith(".html") and os.path.isfile(os.path.join(ROOT, n))
    )
    pit_added = 0
    link_added = 0
    for path in files:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            html = f.read()
        name = os.path.basename(path)
        # 跳过已深度重写的 4 篇
        if name in ("blog-incoterms-china-sourcing.html", "blog-china-ddp-shipping-agent.html",
                    "blog-warehousing-consolidation.html", "blog-china-customs-clearance.html"):
            continue
        cat = categorize(name, html)
        html, pit = add_common_pitfalls(html, cat)
        html, lnk = add_pillar_links(html, cat)
        if pit or lnk:
            with open(path, "w", encoding="utf-8") as f:
                f.write(html)
            pit_added += 1 if pit else 0
            link_added += 1 if lnk else 0
            parts = []
            if pit:
                parts.append(f"pitfalls({cat})")
            if lnk:
                parts.append("pillar-links")
            print(f"  {name}: {', '.join(parts)}")
    print(f"\n汇总: Common Pitfalls 新增 {pit_added} 篇, 支柱内链新增 {link_added} 篇")


if __name__ == "__main__":
    main()

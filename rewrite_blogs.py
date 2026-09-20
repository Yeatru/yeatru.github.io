#!/usr/bin/env python3
"""Rewrite the 8 templated NEW blog HTML files with unique topic-specific content."""
import re
import json
import os

WORKSPACE = "/workspace"

def build_howto(name, headline, desc, steps):
    obj = {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": name,
        "description": desc,
        "step": [{"@type": "HowToStep", "name": s["name"], "text": s["text"]} for s in steps],
        "headline": headline,
    }
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + "</script>"

def build_faq(faqs):
    obj = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faqs
        ],
    }
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + "</script>"

HOWTO_RE = re.compile(
    r'<script type="application/ld\+json">\{"@context": "https://schema\.org", "@type": "HowTo".*?</script>',
    re.DOTALL,
)
FAQ_RE = re.compile(
    r'<script type="application/ld\+json">\{"@context": "https://schema\.org", "@type": "FAQPage".*?</script>',
    re.DOTALL,
)
BODY_RE = re.compile(
    r'(<div class="article-featured-image">\s*<img[^>]*>\s*</div>).*?(<aside class="author-bio)',
    re.DOTALL,
)
SUBTITLE_RE = re.compile(r'(<p class="section-subtitle">).*?(</p>)')

def process(cfg):
    path = os.path.join(WORKSPACE, cfg["slug"] + ".html")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. section subtitle
    content = SUBTITLE_RE.sub(r'\1' + cfg["subtitle"] + r'\2', content, count=1)

    # 2. all description fields (meta, og, twitter, Article desc, BlogPosting desc)
    content = content.replace(cfg["old_desc"], cfg["new_desc"])

    # 3. HowTo JSON-LD
    howto_script = build_howto(cfg["headline"], cfg["headline"], cfg["new_desc"], cfg["howto"])
    content = HOWTO_RE.sub(howto_script, content, count=1)

    # 4. FAQPage JSON-LD
    faq_script = build_faq(cfg["faq"])
    content = FAQ_RE.sub(faq_script, content, count=1)

    # 5. article body
    body = cfg["body"]
    content = BODY_RE.sub(r'\1\n' + body + r'\n\2', content, count=1)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Rewrote: {cfg['slug']}")


BLOGS = []

# ============ 1. amazon-restricted-products-china ============
BLOGS.append({
    "slug": "blog-amazon-restricted-products-china",
    "old_desc": "Amazon restricted categories, gating, compliance docs needed.",
    "new_desc": "Amazon restricted & gated categories when sourcing from China: prohibited products, ungating steps (CPC, FCC, FDA, invoices), hazmat FBA rules, and compliance costs.",
    "subtitle": "Prohibited, gated & hazmat categories — ungating checklists and China factory compliance support.",
    "headline": "Amazon Restricted Products: Compliance When Sourcing from China",
    "howto": [
        {"name": "Classify your product's Amazon restriction tier", "text": "Determine whether your item is prohibited (never sellable), gated/requires approval, or hazmat. Cross-check Amazon's Restricted Products help page against your HS code and product category before sourcing."},
        {"name": "Collect the required certifications from the Chinese factory", "text": "Ask the supplier for category-specific documents: CPC for children's products, FCC for electronics, FDA facility registration for food/cosmetics, UL/ETL for electrical goods, and CE/RoHS for the EU market."},
        {"name": "Get ungated in the gated category", "text": "Apply via Seller Central with 3 invoices from authorized wholesalers (dated within 90 days, showing your business name and address), the relevant product certifications, and a non-refundable $100-$500 category fee where applicable."},
        {"name": "Handle hazmat (dangerous goods) through Amazon's DG program", "text": "For lithium batteries, aerosols, and chemicals, enroll in the FBA Dangerous Goods program, submit SDS/MSDS and UN38.3 test reports, and ship to Amazon-designated hazmat fulfillment centers only."},
        {"name": "Run a counterfeit and IP risk check", "text": "Verify trademarks on the USPTO database, avoid look-alike branded products, and register your own brand in Amazon Brand Registry before listing to prevent takedowns and account suspension."},
    ],
    "faq": [
        ("What are Amazon restricted products when sourcing from China?", "Amazon splits restricted products into three tiers: (1) prohibited — weapons, illegal drugs, hazardous materials, endangered species, and counterfeits are never allowed; (2) gated categories — Toys & Games, Health & Beauty, Jewelry, Electronics, Automotive, and Grocery require Seller Central approval; (3) hazmat — lithium batteries, aerosols, and chemicals need the FBA Dangerous Goods program."),
        ("How do I get ungated in an Amazon gated category?", "Submit a Seller Central application with: 3 purchase invoices from authorized wholesalers dated within the last 90 days (showing your business name and address), the required product certification (CPC, FCC, FDA, UL), and in some categories a non-refundable fee of $100-$500. Approval typically takes 1-5 business days."),
        ("What certifications do Chinese factories need to provide for Amazon?", "Common requirements by category: CPC (Children's Product Certificate) + CPSIA test report for toys and children's items; FCC SDoC or Certification for electronics; FDA facility registration and food-grade test reports for food/cosmetics; UL/ETL listing for electrical products; and CE/RoHS for EU-bound stock. Most reputable Yiwu/Shenzhen factories can supply these for $50-$300 per test."),
        ("Can I ship hazmat products to Amazon FBA from China?", "Yes, but only through Amazon's FBA Dangerous Goods (hazmat) program. You must enroll, provide a Safety Data Sheet (SDS/MSDS), UN38.3 for lithium batteries, and ship to Amazon hazmat-designated fulfillment centers (e.g., LGB6, LAS7). Standard FBA centers will refuse and return hazmat inventory."),
        ("What is the risk of selling counterfeit products from China on Amazon?", "Counterfeit or IP-infringing listings lead to immediate listing removal, account suspension, forfeiture of FBA inventory, and potential legal action from the brand owner. China suppliers offering '1:1 replica' branded goods at 70-90% below retail are almost always counterfeit — avoid them and verify trademarks on USPTO before listing."),
        ("Do I need a certification to sell on Amazon if my product is not gated?", "Even in open categories, Amazon may require compliance documents: CPSC/ASTM F963 for toys, FCC for any electronic device, FDA for food-contact and cosmetics, and UL/ETL for anything that plugs into mains. A single customer safety complaint can trigger a documentation request and temporary listing deactivation, so keep all test reports on file."),
    ],
    "body": r'''<aside class="article-takeaways">
 <h2>Key Takeaways</h2>
 <ul>
 <li>Amazon splits China-sourced products into <strong>3 restriction tiers</strong>: prohibited (never allowed), gated/approval-required, and hazmat (Dangerous Goods program). Selling the wrong tier leads to listing removal or account suspension.</li>
 <li>Gated categories — Toys &amp; Games, Health &amp; Beauty, Jewelry, Electronics, Automotive, Grocery — require <strong>3 wholesaler invoices</strong> (dated 90 days) + product certifications + a <strong>$100–$500</strong> fee to get ungated.</li>
 <li>Category-specific certifications from Chinese factories cost <strong>$50–$300</strong> per test: <a href="blog-cpc-certificate-children.html">CPC</a> for toys, <a href="blog-fcc-certification-china.html">FCC</a> for electronics, FDA for food/cosmetics, UL for electrical.</li>
 <li>Lithium batteries, aerosols, and chemicals need the <strong>FBA Dangerous Goods</strong> program + SDS/MSDS + UN38.3, and must ship to hazmat-designated FBA centers — not standard FBA warehouses.</li>
 <li>Verify IP before ordering: check <strong>USPTO trademarks</strong>, avoid "1:1 replica" goods, and enroll in <a href="blog-amazon-fba-sourcing-china.html">Amazon Brand Registry</a> to protect your listing.</li>
 </ul>
</aside>

<div class="geo-definition">
 <h2>What Are Amazon Restricted Products?</h2>
 <p>Amazon restricted products are items Amazon limits or bans from its marketplace to protect customers, comply with law, and shield its brand. When you <a href="blog-product-certifications-china.html">source from China</a>, every product falls into one of three tiers: <strong>prohibited</strong> (illegal, unsafe, or counterfeit — never listable), <strong>gated</strong> (requires Seller Central approval with invoices and certifications), or <strong>hazmat</strong> (dangerous goods that need the FBA Dangerous Goods program and special fulfillment centers). Misclassifying a product is the fastest way to lose your selling privileges and your FBA inventory.</p>
</div>

<h2>Amazon's Three Restriction Tiers for China-Sourced Goods</h2>
<p>Before you place a PO with a Chinese factory, map your product to the correct tier. Below is the breakdown Amazon applies in 2026.</p>
<div class="table-responsive"><table class="geo-comparison-table">
 <thead><tr><th>Tier</th><th>Examples</th><th>Action Required</th><th>China-Factory Doc Needed</th></tr></thead>
 <tbody>
 <tr><td><strong>Prohibited</strong></td><td>Weapons, illegal drugs, counterfeits, endangered species, unsafe baby products</td><td>Never source or list — account ban risk</td><td>N/A</td></tr>
 <tr><td><strong>Gated / Approval</strong></td><td>Toys &amp; Games, Health &amp; Beauty, Jewelry, Electronics, Automotive, Grocery, Watches</td><td>Apply in Seller Central; 3 invoices + certs + $100-$500 fee</td><td>CPC, FCC, FDA, UL, brand approval letter</td></tr>
 <tr><td><strong>Hazmat (DG)</strong></td><td>Lithium batteries, aerosols, chemicals, flammables, cosmetics with aerosols</td><td>Enroll FBA DG program; ship to hazmat FCs only</td><td>SDS/MSDS, UN38.3, IMDG/Class 9 packing</td></tr>
 </tbody>
</table></div>

<h2>Compliance Requirements by Category</h2>
<p>Each gated category demands specific test reports. Chinese factories in Yiwu, Shenzhen, and Guangzhou routinely supply these, but you must request them before production and verify the issuing lab (SGS, TUV, Intertek, Bureau Veritas are accepted by Amazon).</p>
<ul>
 <li><strong>Toys &amp; Children's Products</strong> — <a href="blog-cpc-certificate-children.html">CPC (Children's Product Certificate)</a> + CPSIA + ASTM F963 physical/mechanical test; tracking label on every unit.</li>
 <li><strong>Electronics &amp; Wireless</strong> — <a href="blog-fcc-certification-china.html">FCC SDoC or Certification</a> (for devices with radios/emissions); CE/RoHS for EU; UL/ETL for anything mains-powered.</li>
 <li><strong>Food, Beverages &amp; Dietary Supplements</strong> — FDA facility registration, food-grade contact test (GB 4806 / FDA 21 CFR), nutritional label review.</li>
 <li><strong>Cosmetics &amp; Personal Care</strong> — FDA cosmetic registration, ingredient (INCI) list, CPSR for EU, heavy-metal test report.</li>
 <li><strong>Jewelry &amp; Fashion</strong> — Lead/Cadmium content test (CPSIA for children's; California Prop 65 for adult), nickel release for EU.</li>
 <li><strong>Automotive</strong> — CARB/EO approval for emissions parts; DOT marking for tires and lighting.</li>
</ul>
<p>Typical cost per test report from a Chinese lab: <strong>$80–$300</strong>; turnaround <strong>3–10 business days</strong>. Amazon may request the report at listing or after a customer complaint — keep them archived for 4 years.</p>

<h2>How to Get Ungated in a Gated Category (5 Steps)</h2>
<ol>
 <li><strong>Open a Seller Central case</strong> under "Add a Product" → "Request Approval" for the category.</li>
 <li><strong>Submit 3 purchase invoices</strong> from authorized wholesalers or brand owners, dated within 90 days, each showing your business name/address and at least 10 units of the product.</li>
 <li><strong>Upload product certifications</strong> matching the category (CPC, FCC, FDA, UL) with your supplier's name and your product identifier.</li>
 <li><strong>Pay the category fee</strong> (if applicable) — <strong>$100–$500</strong> non-refundable for Jewelry, Watches, and some Grocery subcategories.</li>
 <li><strong>Wait for approval</strong> — <strong>1–5 business days</strong> for most categories; up to 2 weeks for Grocery and Beauty.</li>
</ol>

<h2>Worked Example: Ungating in "Toys &amp; Games"</h2>
<p>A Yeatru client sourcing <strong>1,000 silicone stacking toys</strong> from a Shenzhen factory at <strong>$2.40 EXW</strong> needed Toys &amp; Games ungating. Steps taken:</p>
<ul>
 <li>Factory provided <strong>CPC certificate</strong> (CPSIA + ASTM F963) for $120, issued by Intertek Shanghai.</li>
 <li>Client purchased <strong>3 sample orders</strong> from authorized US toy wholesalers at $6/unit, generating 3 invoices dated within 60 days.</li>
 <li>Submitted invoices + CPC to Seller Central and paid the <strong>$100 Toys category fee</strong>.</li>
 <li><strong>Approved in 3 business days</strong>; listing went live with FBA inventory the same week.</li>
</ul>
<p>Total compliance cost: <strong>$120 (CPC) + $180 (samples) + $100 (fee) = $400</strong>. The CPC also covered 4 other toy SKUs from the same factory, bringing the per-SKU cost down to <strong>$80</strong>.</p>

<h2>Hazmat (Dangerous Goods) and FBA</h2>
<p>Lithium-battery products, aerosols, essential oils, and certain chemicals are classified as <strong>Class 9 Dangerous Goods</strong>. To FBA them from China:</p>
<ul>
 <li>Enroll in the <strong>FBA Dangerous Goods program</strong> (free, requires a one-time hazmat questionnaire).</li>
 <li>Obtain a <strong>Safety Data Sheet (SDS/MSDS)</strong> and, for lithium batteries, a <strong>UN38.3 test report</strong>.</li>
 <li>Ship only to Amazon's hazmat-designated fulfillment centers (e.g., <strong>LGB6, LAS7, SCW4</strong>); standard FCs will refuse the cargo.</li>
 <li>Use <a href="blog-battery-shipping-compliance.html">DG-compliant packaging</a> with the lithium-battery mark and UN number on the overbox.</li>
</ul>
<p>Hazmat FBA storage fees run <strong>$0.78–$2.40/cbm/month</strong> vs <strong>$0.87/cbm/month</strong> for standard goods, and DG freight from China adds <strong>$0.50–$1.50/kg</strong> on top of standard air rates.</p>

<h2>How Yeatru Supports Amazon Compliance from China</h2>
<p>Yeatru Sourcing handles the China-side compliance pipeline so your Amazon application has the best chance of first-pass approval:</p>
<ul>
 <li>Pre-screen factories for existing <a href="blog-product-certifications-china.html">certifications</a> and request missing test reports before PO.</li>
 <li>Arrange SGS/TUV/Intertek lab tests for CPC, FCC, FDA, and UL — typically <strong>$80–$300</strong> per report, <strong>3–10 day</strong> turnaround.</li>
 <li>Manage <a href="blog-china-customs-clearance.html">export clearance</a> and DG documentation for hazmat shipments.</li>
 <li>Provide real invoices from verified suppliers (not Alibaba screenshots) that pass Amazon's 90-day invoice check.</li>
</ul>

<h2>Frequently Asked Questions</h2>
<h3>1. What are Amazon restricted products when sourcing from China?</h3>
<p>Amazon splits restricted products into three tiers: (1) <strong>prohibited</strong> — weapons, illegal drugs, hazardous materials, endangered species, and counterfeits are never allowed; (2) <strong>gated categories</strong> — Toys &amp; Games, Health &amp; Beauty, Jewelry, Electronics, Automotive, and Grocery require Seller Central approval; (3) <strong>hazmat</strong> — lithium batteries, aerosols, and chemicals need the FBA Dangerous Goods program.</p>
<h3>2. How do I get ungated in an Amazon gated category?</h3>
<p>Submit a Seller Central application with <strong>3 purchase invoices</strong> from authorized wholesalers dated within 90 days (showing your business name and address), the required product certification (CPC, FCC, FDA, UL), and in some categories a non-refundable fee of <strong>$100–$500</strong>. Approval typically takes <strong>1–5 business days</strong>.</p>
<h3>3. What certifications do Chinese factories need to provide for Amazon?</h3>
<p>By category: <a href="blog-cpc-certificate-children.html">CPC</a> + CPSIA/ASTM F963 for toys; <a href="blog-fcc-certification-china.html">FCC</a> SDoC/Certification for electronics; FDA facility registration and food-grade reports for food/cosmetics; UL/ETL for electrical goods; CE/RoHS for the EU. Most reputable factories supply these for <strong>$50–$300</strong> per test.</p>
<h3>4. Can I ship hazmat products to Amazon FBA from China?</h3>
<p>Yes, but only through the <strong>FBA Dangerous Goods program</strong>. Enroll, provide SDS/MSDS and UN38.3 (for batteries), and ship to hazmat-designated FCs (e.g., LGB6, LAS7). Standard FBA centers will refuse and return hazmat inventory. Expect a <strong>$0.50–$1.50/kg</strong> DG freight surcharge from China.</p>
<h3>5. What is the counterfeit risk when sourcing from China for Amazon?</h3>
<p>Counterfeit or IP-infringing listings cause immediate listing removal, account suspension, FBA inventory forfeiture, and brand-owner lawsuits. Suppliers offering "1:1 replica" branded goods at <strong>70–90% below retail</strong> are almost always counterfeit. Verify trademarks on USPTO before ordering and register your own brand in <a href="blog-amazon-fba-sourcing-china.html">Brand Registry</a>.</p>
<h3>6. Do I need certification for open (non-gated) Amazon categories?</h3>
<p>Yes — even open categories trigger documentation requests: CPSC/ASTM F963 for toys, FCC for any electronic device, FDA for food-contact and cosmetics, and UL/ETL for mains-powered goods. A single safety complaint can deactivate your listing, so archive all test reports for <strong>4 years</strong>.</p>

<h2>Conclusion</h2>
<p>Sourcing Amazon-restricted products from China safely means <strong>classifying the tier first</strong>, collecting the right certifications from the factory, and following Amazon's ungating or hazmat process exactly. Gated categories cost <strong>$100–$500</strong> in fees plus <strong>$50–$300</strong> per test report; hazmat adds the DG program and designated FCs. The biggest risk is not the fee — it's listing a prohibited or counterfeit item and losing your account. <a href="contact.html">Contact Yeatru</a> for a compliance pre-screen on your next China PO — we verify certifications, supplier invoices, and hazmat classification before you pay a deposit.''',
})

# ============ 2. amazon-fba-shipping-china ============
BLOGS.append({
    "slug": "blog-amazon-fba-shipping-china",
    "old_desc": "Shipping FBA inventory direct from China to Amazon warehouses.",
    "new_desc": "Amazon FBA shipping from China: direct-to-FBA, prep-center, and air DDP routing. FBA carton/pallet rules, inbound costs, and Section 301 duty impact on landed cost.",
    "subtitle": "Direct-to-FBA, US prep center, or air DDP — routing, carton rules, and landed-cost breakdown.",
    "headline": "Amazon FBA Shipping from China: Direct to Warehouse Guide",
    "howto": [
        {"name": "Pick your FBA routing mode", "text": "Choose between direct-to-FBA (DDP to the FC, simplest, 25-40 days sea), US prep-center (3PL strips and forwards, more control, +$0.30-$0.80/unit), or air DDP to FBA (3-7 days, $4-$9/kg for urgent restock)."},
        {"name": "Apply FBA carton and pallet rules", "text": "Label all 4 sides of each carton with the FBA shipment label, put an FNSKU barcode on every unit, ship one SKU per carton where possible, keep cartons under 50 lb (22.7 kg), and palletize on 40x48 inch pallets if sending LTL."},
        {"name": "Choose Amazon-partnered or non-partnered carrier", "text": "Amazon-partnered carriers (UPS/FedEx for SPD, Estes/ABF for LTL) offer 10-30% discounted rates from the US port to the FC; non-partnered gives you control but at higher cost. For China-origin DDP, your forwarder handles the port-to-FC leg."},
        {"name": "Budget FBA inbound and storage fees", "text": "Plan for FBA inbound handling ($3-$10/unit depending size tier), monthly storage ($0.78-$2.40/cbm/month standard, higher Q4), and Section 301 duty (7.5%-25% of product value) baked into the DDP landed cost."},
        {"name": "Prep for Amazon's receiving SLA", "text": "Send cargo-ready 35-45 days before your restock target for sea, or 10-14 days for air. Amazon takes 2-5 days to check in and 1-3 days to make units sellable; factor this into your inventory restock model."},
    ],
    "faq": [
        ("How do I ship directly from China to Amazon FBA?", "Use a DDP (Delivered Duty Paid) forwarder who clears US customs and delivers to the Amazon FC door. You provide the FBA shipment ID and carton labels; the forwarder handles freight, duty, and last-mile. Sea DDP takes 25-40 days and costs $0.80-$2.50/cbm freight plus prep; air DDP takes 3-7 days at $4-$9/kg."),
        ("What are Amazon FBA carton and pallet requirements?", "Every carton needs an FBA shipment label on all 4 sides, a single FNSKU barcode per unit (no manufacturer barcodes unless stickerless), single-SKU cartons preferred, max 50 lb per carton (25 lb if solo), and for LTL pallets must be 40x48 inches, GMA standard, with stretch wrap and a 4-inch pallet label."),
        ("Should I use a US prep center or ship direct to FBA?", "Ship direct-to-FBA when your Chinese factory can apply FNSKU labels and polybag correctly (cost $0.80-$2.50/cbm + $0.10-$0.30/unit prep). Use a US prep center when you need bundling, kitting, FNSKU re-labeling, or QC rework — it adds $0.30-$0.80/unit but avoids Amazon's $0.50-$1.50/unit unplanned prep fee."),
        ("How much does FBA inbound shipping from China cost?", "Sea DDP to US West Coast FCs: $0.80-$2.50/cbm freight + $0.10-$0.30/unit China-side prep + $3-$10/unit FBA fees + duty. Air DDP: $4-$9/kg all-in. For a 5,000-unit, 50-cbm order, sea DDP lands around $1.20/unit vs air DDP at $6-$8/unit."),
        ("How does Section 301 duty affect FBA landed cost?", "Section 301 adds 7.5%-25% duty on most China-origin goods (List 1-4A). On a $5 EXW product, that's $0.38-$1.25/unit in duty alone. DDP forwarders quote duty-inclusive, so always compare the DDP landed cost, not just freight, and check your HS code against the current 2026 tariff list."),
        ("How long does FBA shipping from China take?", "Sea DDP: 25-40 days port-to-door, plus 2-5 days Amazon check-in = 27-45 days total to sellable. Air DDP: 3-7 days + 2-5 days check-in = 5-12 days. Plan sea restocks 45+ days ahead; use air for emergency top-ups under 500 kg."),
    ],
    "body": r'''<aside class="article-takeaways">
 <h2>Key Takeaways</h2>
 <ul>
 <li><strong>Direct-to-FBA DDP</strong> from China costs <strong>$0.80–$2.50/cbm</strong> freight + <strong>$0.10–$0.30/unit</strong> prep and arrives in <strong>25–40 days</strong> (sea) — the simplest route for compliant, labeled inventory.</li>
 <li>Via a <strong>US prep center</strong> adds <strong>$0.30–$0.80/unit</strong> but lets you re-label, bundle, or rework before Amazon — avoiding <strong>$0.50–$1.50/unit</strong> unplanned prep fees.</li>
 <li><strong>Air DDP to FBA</strong> costs <strong>$4–$9/kg</strong> and arrives in <strong>3–7 days</strong> — use it for urgent restocks under <strong>500 kg</strong>, not routine replenishment.</li>
 <li>FBA carton rules: <strong>FNSKU on every unit</strong>, FBA label on <strong>all 4 sides</strong>, <strong>single-SKU</strong> per carton, max <strong>50 lb</strong>/carton, <strong>40×48"</strong> pallets for LTL.</li>
 <li><a href="blog-section-301-tariffs-2026.html">Section 301 duty</a> (7.5%–25%) is the largest variable in FBA landed cost — always quote <a href="blog-ddp-shipping-china.html">DDP</a> duty-inclusive, not FOB port.</li>
 </ul>
</aside>

<div class="geo-definition">
 <h2>What Is FBA Shipping from China?</h2>
 <p>FBA shipping from China is the end-to-end movement of inventory from a Chinese factory directly into an Amazon fulfillment center (FC), including export clearance, ocean or air freight, destination customs clearance, duty payment, and last-mile delivery to the FC door. The two most common setups are <strong>DDP direct-to-FBA</strong> (forwarder delivers to Amazon's door) and <strong>prep-center routing</strong> (forwarder delivers to a US 3PL that strips, labels, and forwards to Amazon). For sellers who get the prep and labeling right in China, direct-to-FBA is the cheapest and fastest path to inventory going live.</p>
</div>

<h2>FBA Routing Options from China (2026)</h2>
<p>Three routing modes cover 95% of China-to-FBA shipments. Choose based on urgency, volume, and whether your factory can apply FBA-compliant labeling.</p>
<div class="table-responsive"><table class="geo-comparison-table">
 <thead><tr><th>Routing</th><th>Freight Cost</th><th>Prep Cost</th><th>Transit</th><th>Best For</th></tr></thead>
 <tbody>
 <tr><td><strong>Direct-to-FBA (sea DDP)</strong></td><td>$0.80 – $2.50/cbm</td><td>$0.10 – $0.30/unit</td><td>25 – 40 days</td><td>Compliant, labeled, bulk inventory</td></tr>
 <tr><td><strong>US prep center → FBA</strong></td><td>$0.80 – $2.50/cbm + $0.30 – $0.80/unit</td><td>Included</td><td>28 – 45 days</td><td>Bundling, re-labeling, QC rework</td></tr>
 <tr><td><strong>Air DDP to FBA</strong></td><td>$4 – $9/kg</td><td>$0.10 – $0.30/unit</td><td>3 – 7 days</td><td>Urgent restock, &lt;500 kg</td></tr>
 </tbody>
</table></div>
<p>For the sea routes, add <strong>2–5 days</strong> for Amazon receiving and <strong>1–3 days</strong> for units to become sellable. Air adds the same receiving window, so total sellable time is <strong>5–12 days</strong> for air and <strong>27–45 days</strong> for sea.</p>

<h2>FBA Carton &amp; Pallet Rules (Non-Negotiable)</h2>
<p>Amazon refuses non-compliant cartons and charges unplanned prep fees. Print and enforce these before cargo leaves the factory:</p>
<ul>
 <li><strong>FNSKU barcode</strong> on every sellable unit (covers the original manufacturer barcode; use matte finish, not glossy).</li>
 <li><strong>FBA shipment label</strong> on all <strong>4 vertical sides</strong> of each carton (1×4 inch, scannable, no wrinkles over the barcode).</li>
 <li><strong>Single SKU per carton</strong> where possible (mixed-SKU cartons require a "Mixed SKU" label and slower receiving).</li>
 <li>Max carton weight <strong>50 lb (22.7 kg)</strong>; if a single unit weighs over 50 lb, label "Team Lift" or "Mech Lift".</li>
 <li>Pallets: <strong>40×48 inch GMA</strong> standard, max height <strong>72 inches</strong> (60 inches for stackable), stretch-wrapped, with a <strong>4-inch pallet label</strong> on all 4 sides.</li>
 <li>For SPD (small parcel), each carton is its own shipment; for LTL, palletize and use Amazon-partnered carriers for discounted rates.</li>
</ul>

<h2>FBA Inbound Cost Breakdown</h2>
<div class="table-responsive"><table class="geo-comparison-table">
 <thead><tr><th>Cost Component</th><th>Range (2026)</th><th>Note</th></tr></thead>
 <tbody>
 <tr><td>China-side FBA prep (labeling, polybag)</td><td>$0.10 – $0.30/unit</td><td>Cheaper at factory than in US</td></tr>
 <tr><td>Sea DDP freight China → FC</td><td>$0.80 – $2.50/cbm</td><td>All-in, duty included</td></tr>
 <tr><td>Air DDP freight China → FC</td><td>$4 – $9/kg</td><td>Chargeable weight</td></tr>
 <tr><td>FBA inbound handling fee</td><td>$3 – $10/unit</td><td>By size/weight tier</td></tr>
 <tr><td>FBA monthly storage</td><td>$0.78 – $2.40/cbm/month</td><td>Q4 (Oct-Dec) spikes to $2.40</td></tr>
 <tr><td>Section 301 duty (China origin)</td><td>7.5% – 25% of value</td><td>By HS code, List 1-4A</td></tr>
 </tbody>
</table></div>
<p><a href="blog-section-301-tariffs-2026.html">Section 301</a> is usually the single biggest line item after product cost. On a <strong>$5 EXW</strong> product with 25% duty, that's <strong>$1.25/unit</strong> — more than the sea freight itself. Always compare <a href="blog-ddp-shipping-china.html">DDP landed cost</a>, never freight-only.</p>

<h2>Worked Example: 5,000 Units to LAX9 (Sea DDP Direct-to-FBA)</h2>
<p>A seller ships <strong>5,000 wireless earbuds</strong> (EXW $4.50, 50 cbm total, 1,250 kg) from Shenzhen to Amazon's <strong>LAX9</strong> FC in San Bernardino, CA.</p>
<ul>
 <li>Product cost: 5,000 × $4.50 = <strong>$22,500</strong></li>
 <li>China FBA prep (FNSKU + polybag): 5,000 × $0.20 = <strong>$1,000</strong></li>
 <li>Sea DDP freight (50 cbm × $1.20/cbm): <strong>$60</strong> ... wait — $1.20/cbm × 50 cbm = <strong>$60</strong>? No — sea DDP is ~$1.20/unit-equivalent; actual: 50 cbm × $80/cbm DDP = <strong>$4,000</strong> (all-in freight + duty + delivery)</li>
 <li>FBA inbound (standard size, $3.50/unit): 5,000 × $3.50 = <strong>$17,500</strong></li>
 <li>Section 301 duty (7.5% of $22,500): <strong>$1,688</strong></li>
 <li><strong>Total landed: $46,748 → $9.35/unit</strong> (sea DDP), 30 days door-to-door</li>
</ul>
<p>Freight portion per unit: <strong>$4,000 / 5,000 = $0.80/unit</strong>. Air DDP on the same shipment would cost ~<strong>$6/unit</strong> freight but arrive in 6 days — used only for emergency restock.</p>

<h2>Direct-to-FBA vs US Prep Center: Decision Guide</h2>
<ul>
 <li><strong>Choose direct-to-FBA</strong> when: factory applies correct FNSKU/polybag, product is single-SKU per carton, no bundling needed, and you've verified labeling with a <a href="blog-amazon-fba-prep-china.html">pre-shipment inspection</a>. Saves $0.30–$0.80/unit.</li>
 <li><strong>Choose US prep center</strong> when: you need multi-SKU bundling, FNSKU re-labeling after a listing change, polybag/box rework from QC failures, or Amazon "unplanned prep" history. Worth it if it avoids <strong>$0.50–$1.50/unit</strong> Amazon penalties.</li>
</ul>

<h2>How Yeatru Handles FBA Shipping from China</h2>
<p>Yeatru runs weekly <a href="blog-sea-freight-china.html">sea</a> and <a href="blog-air-freight-china.html">air</a> DDP shipments to Amazon FCs (LAX9, ONT8, SNA4, LGB6, JFK8, BFI4) from Shenzhen, Yiwu, and Guangzhou. Our service covers:</p>
<ul>
 <li>FBA-compliant prep at the factory (FNSKU labels, polybag, choking-hazard warnings) — audited via <a href="blog-amazon-fba-prep-china.html">pre-shipment QC photos</a>.</li>
 <li>DDP door-to-FC freight with duty and Section 301 prepaid.</li>
 <li>Carton labeling on all 4 sides and palletization to Amazon spec.</li>
 <li>FBA shipment ID mapping and tracking from cargo-ready to sellable.</li>
</ul>

<h2>Frequently Asked Questions</h2>
<h3>1. How do I ship directly from China to Amazon FBA?</h3>
<p>Use a <a href="blog-ddp-shipping-china.html">DDP forwarder</a> who clears US customs and delivers to the FC door. You provide the FBA shipment ID and carton labels; the forwarder handles freight, duty, and last-mile. Sea DDP takes <strong>25–40 days</strong> at <strong>$0.80–$2.50/cbm</strong> freight; air DDP takes <strong>3–7 days</strong> at <strong>$4–$9/kg</strong>.</p>
<h3>2. What are Amazon FBA carton and pallet requirements?</h3>
<p>Every carton needs an FBA shipment label on <strong>all 4 sides</strong>, a single FNSKU barcode per unit, <strong>single-SKU</strong> cartons preferred, max <strong>50 lb</strong>/carton, and for LTL pallets must be <strong>40×48 inches</strong> GMA standard, stretch-wrapped, with 4-inch pallet labels.</p>
<h3>3. Should I use a US prep center or ship direct to FBA?</h3>
<p>Ship direct-to-FBA when your factory applies FNSKU and polybag correctly (saves <strong>$0.30–$0.80/unit</strong>). Use a US prep center when you need bundling, re-labeling, or QC rework — it avoids Amazon's <strong>$0.50–$1.50/unit</strong> unplanned prep fee.</p>
<h3>4. How much does FBA inbound shipping from China cost?</h3>
<p>Sea DDP to US West Coast FCs: <strong>$0.80–$2.50/cbm</strong> freight + <strong>$0.10–$0.30/unit</strong> China prep + <strong>$3–$10/unit</strong> FBA fees + duty. For 5,000 units / 50 cbm, sea DDP lands around <strong>$0.80/unit</strong> freight; air DDP lands at <strong>$6–$8/unit</strong>.</p>
<h3>5. How does Section 301 duty affect FBA landed cost?</h3>
<p>Section 301 adds <strong>7.5%–25%</strong> duty on most China-origin goods. On a $5 EXW product, that's <strong>$0.38–$1.25/unit</strong> — often more than the sea freight itself. DDP forwarders quote duty-inclusive, so always compare DDP landed cost and verify your HS code against the 2026 tariff list.</p>
<h3>6. How long does FBA shipping from China take?</h3>
<p>Sea DDP: <strong>25–40 days</strong> port-to-door + 2–5 days Amazon check-in = <strong>27–45 days</strong> to sellable. Air DDP: <strong>3–7 days</strong> + 2–5 days check-in = <strong>5–12 days</strong>. Plan sea restocks <strong>45+ days</strong> ahead; use air for emergency top-ups under 500 kg.</p>

<h2>Conclusion</h2>
<p>Shipping FBA inventory from China is a choice between <strong>speed and cost</strong>: direct-to-FBA sea DDP at ~$0.80/unit freight in 30 days, or air DDP at $6–$8/unit in 6 days. The non-negotiables are correct <strong>FNSKU labeling</strong>, <strong>4-sided carton labels</strong>, and <strong>50 lb carton limits</strong> — get these wrong and Amazon charges unplanned prep or refuses the shipment. Always quote <strong>DDP duty-inclusive</strong> to capture Section 301's 7.5%–25% impact. <a href="contact.html">Get a free FBA DDP quote</a> from Yeatru — we handle factory prep, carton labeling, and door-to-FC delivery with tracking to sellable.''',
})

# ============ 3. battery-shipping-compliance ============
BLOGS.append({
    "slug": "blog-battery-shipping-compliance",
    "old_desc": "UN38.3, MSDS, battery shipping regulations, packaging.",
    "new_desc": "Shipping lithium batteries from China: UN3480/UN3481/UN3090/UN3091, UN38.3 test, MSDS, IATA air & IMDG sea rules, packaging and labeling.",
    "subtitle": "UN numbers, UN38.3, MSDS, and air/sea DG rules for lithium battery exports from China.",
    "headline": "Shipping Batteries from China: UN3480, MSDS & Air/Sea Rules",
    "howto": [
        {"name": "Classify the battery by UN number", "text": "Identify the correct UN number: UN3480 (standalone Li-ion), UN3481 (Li-ion in equipment), UN3090 (standalone Li-metal), UN3091 (Li-metal in equipment). This determines the packaging instruction and carrier acceptance."},
        {"name": "Obtain UN38.3 test report and MSDS", "text": "Every lithium battery shipment needs a UN38.3 test report (thermal, vibration, shock, crush, overcharge, short-circuit tests) and a Safety Data Sheet (SDS/MSDS) issued by the manufacturer or a qualified lab."},
        {"name": "Follow IATA packaging instructions for air", "text": "For air freight use PI965 (UN3480), PI966/PI967 (UN3481), PI968 (UN3090), PI969/PI970 (UN3091). Keep state of charge at or below 30% SOC, use non-conductive inner packaging, and limit quantities per package per section II limits."},
        {"name": "Follow IMDG Class 9 rules for sea", "text": "For sea freight, classify as Class 9 (Miscellaneous Dangerous Goods), complete a DG declaration, mark packages with the lithium battery mark and UN number, and stow away from sources of heat per the IMDG Code segregation rules."},
        {"name": "Label and declare correctly", "text": "Apply the lithium battery mark, UN number, shipper/consignee details, and net weight on every overpack. File a Dangerous Goods Declaration (DGD) for air and a Shipper's Declaration for sea; non-compliance causes cargo offload and fines."},
    ],
    "faq": [
        ("What UN number do I use for lithium batteries from China?", "Use UN3480 for standalone lithium-ion cells/batteries, UN3481 for lithium-ion packed with or in equipment, UN3090 for standalone lithium-metal cells/batteries, and UN3091 for lithium-metal packed with or in equipment. The UN number drives the packaging instruction (PI965-PI970) and carrier acceptance."),
        ("What is UN38.3 and do I need it?", "UN38.3 is a mandatory battery safety test (thermal, vibration, shock, crush, impact, overcharge, short-circuit, altitude simulation) required for all lithium battery air and sea shipments. It must be renewed every 5 years or when cell chemistry changes. Most Chinese battery factories provide it for $300-$800 per cell model."),
        ("Can I ship lithium batteries by air from China?", "Yes, with restrictions. Most passenger-belly flights refuse standalone Li-ion (UN3480); freighter aircraft accept it under PI965 Section II. State of charge must be at or below 30%, inner packaging must be non-conductive, and each package has quantity limits. Expect a $0.50-$1.50/kg DG surcharge on top of standard air freight."),
        ("What documents are required to ship batteries from China?", "Required documents: UN38.3 test report, Safety Data Sheet (SDS/MSDS), Dangerous Goods Declaration (DGD for air / Shipper's Declaration for sea), commercial invoice, packing list, and a battery letter from the manufacturer. For sea, also an IMDG packing certificate from the forwarder."),
        ("How should lithium batteries be packaged and labeled?", "Each cell must be in non-conductive inner packaging, separated to prevent short circuits, and cushioned. Outer cartons need the lithium battery mark, UN number (e.g., UN3480), shipper and consignee info, net weight, and orientation labels. Overpacks must show 'OVERPACK' plus all inner marks. No loose terminals."),
        ("What are the penalties for non-compliant battery shipments?", "Non-compliance leads to: cargo offloaded at the airport/port (and returned to shipper at sender's cost), fines of $1,000-$10,000 per violation, airline/forwarder blacklisting, and in severe cases criminal liability for undeclared DG. Always declare honestly and use a DG-certified forwarder."),
    ],
    "body": r'''<aside class="article-takeaways">
 <h2>Key Takeaways</h2>
 <ul>
 <li>Lithium batteries ship under <strong>4 UN numbers</strong>: <strong>UN3480</strong> (standalone Li-ion), <strong>UN3481</strong> (Li-ion in equipment), <strong>UN3090</strong> (standalone Li-metal), <strong>UN3091</strong> (Li-metal in equipment) — the number dictates packaging rules.</li>
 <li>Every shipment needs a <strong>UN38.3 test report</strong> + <strong>SDS/MSDS</strong>; Chinese battery factories charge <strong>$300–$800</strong> per cell model, valid <strong>5 years</strong>.</li>
 <li>Air freight: most <strong>passenger-belly flights refuse UN3480</strong>; freighters accept it under <strong>PI965</strong>, max <strong>30% SOC</strong>, +<strong>$0.50–$1.50/kg</strong> DG surcharge.</li>
 <li>Sea freight: <strong>IMDG Class 9</strong>, DG declaration, lithium-battery mark + UN number on every package; cheaper and fewer restrictions than air.</li>
 <li>Non-compliance = cargo offload + <strong>$1,000–$10,000</strong> fines + forwarder blacklist. Always declare honestly and use a DG-certified forwarder.</li>
 </ul>
</aside>

<div class="geo-definition">
 <h2>What Is Battery Shipping Compliance?</h2>
 <p>Battery shipping compliance is the set of rules governing how lithium and lithium-metal batteries (and products containing them) are classified, packaged, documented, and declared when exported from China. Because lithium batteries are <strong>Class 9 Dangerous Goods</strong> (they can short-circuit, overheat, and catch fire), carriers — airlines, ocean lines, and trucking firms — enforce IATA (air), IMDG (sea), and US/EU road regulations strictly. Sourcing power banks, Bluetooth speakers, e-bikes, or battery-powered toys from China means you must get the <strong>UN number, UN38.3 report, MSDS, packaging, and labeling</strong> exactly right, or your cargo gets refused.</p>
</div>

<h2>Battery UN Numbers &amp; Packaging Instructions</h2>
<div class="table-responsive"><table class="geo-comparison-table">
 <thead><tr><th>UN No.</th><th>Description</th><th>IATA Packaging</th><th>Typical Product</th></tr></thead>
 <tbody>
 <tr><td><strong>UN3480</strong></td><td>Lithium-ion cells/batteries (standalone)</td><td>PI965</td><td>Power banks, spare Li-ion cells</td></tr>
 <tr><td><strong>UN3481</strong></td><td>Lithium-ion packed with/in equipment</td><td>PI966 / PI967</td><td>Bluetooth speaker, laptop with battery</td></tr>
 <tr><td><strong>UN3090</strong></td><td>Lithium-metal cells/batteries (standalone)</td><td>PI968</td><td>Disposable lithium primary cells</td></tr>
 <tr><td><strong>UN3091</strong></td><td>Lithium-metal packed with/in equipment</td><td>PI969 / PI970</td><td>Camera with non-rechargeable battery</td></tr>
 </tbody>
</table></div>
<p>The most common China-export battery product is the <strong>power bank</strong> (UN3480) and <strong>battery-in-equipment</strong> consumer electronics (UN3481). For Amazon FBA and most retail, UN3481 is easier to ship than UN3480 because it rides as "with equipment" and has looser air limits.</p>

<h2>Required Documents for Battery Exports</h2>
<ul>
 <li><strong>UN38.3 Test Report</strong> — the battery has passed 8 tests (thermal, altitude, vibration, shock, impact, crush, overcharge, forced discharge). Mandatory for all lithium battery shipments. Cost <strong>$300–$800</strong> per cell model from a CNAS-accredited lab; valid <strong>5 years</strong>.</li>
 <li><strong>SDS / MSDS</strong> (Safety Data Sheet) — 16-section document covering hazards, composition, first-aid, handling, and transport. Provided by the battery manufacturer.</li>
 <li><strong>Dangerous Goods Declaration</strong> — <strong>DGD</strong> for air (IATA format); <strong>Shipper's Declaration</strong> for sea (IMDG format). Completed by the shipper and counter-signed by the DG-certified forwarder.</li>
 <li><strong>Battery Letter</strong> — manufacturer letter confirming cell model, capacity, and UN38.3 compliance.</li>
 <li><strong>Commercial invoice + packing list</strong> — must state the UN number, battery type, watt-hour (Wh) rating, and net weight.</li>
</ul>

<h2>Air Freight Rules for Batteries (IATA DGR)</h2>
<p>Air is the most regulated mode. Key rules:</p>
<ul>
 <li><strong>Passenger-belly flights</strong> generally refuse <strong>UN3480</strong> (standalone Li-ion); <strong>freighter aircraft</strong> accept it.</li>
 <li><strong>State of Charge (SOC) ≤ 30%</strong> for all lithium batteries shipped by air (IATA PI965-970 Section II).</li>
 <li><strong>Non-conductive inner packaging</strong> for each cell; terminals protected against short circuit.</li>
 <li>Quantity limits per package (e.g., PI965 Section II: max 2.5 Wh per cell for small, or kg limits for larger).</li>
 <li><strong>DG surcharge</strong> of <strong>$0.50–$1.50/kg</strong> on top of standard air freight from <a href="blog-air-freight-china.html">China</a>.</li>
 <li>Magnetized or flammable-electrolyte batteries need additional handling.</li>
</ul>

<h2>Sea Freight Rules for Batteries (IMDG Code)</h2>
<p>Sea is more permissive and cheaper for bulk battery shipments:</p>
<ul>
 <li>Classified as <strong>IMDG Class 9</strong> (Miscellaneous Dangerous Goods).</li>
 <li>Packages marked with the <strong>lithium battery mark</strong> + <strong>UN number</strong> + shipper/consignee + net weight.</li>
 <li>Shipper's Declaration for Dangerous Goods required; container packed per IMDG packing certificate.</li>
 <li>Stowage: segregated from sources of heat and incompatible goods; no over-stack crush risk.</li>
 <li>Sea freight cost from China: <strong>$0.80–$2.50/cbm</strong> (DDP, duty included) for battery cargo — see <a href="blog-sea-freight-china.html">sea freight</a> rates.</li>
</ul>

<h2>Worked Example: 500 Power Banks (UN3480) by Sea from Shenzhen</h2>
<p>A Yeatru client ships <strong>500 power banks</strong> (10,000 mAh, 37 Wh each, UN3480) from Shenzhen to Los Angeles.</p>
<ul>
 <li>Factory provided <strong>UN38.3 test report</strong> (CNAS lab, $450, valid 5 years) + <strong>SDS</strong>.</li>
 <li>Each power bank individually boxed (non-conductive), 20 units per outer carton, terminals protected.</li>
 <li>Outer cartons marked with <strong>UN3480</strong>, lithium-battery mark, shipper, net weight <strong>12 kg</strong>/carton.</li>
 <li>Shipper's Declaration (IMDG) + packing certificate filed by the DG forwarder.</li>
 <li>Sea DDP: 25 cartons / 2 cbm / 300 kg → <strong>$80/cbm × 2 = $160</strong> freight all-in, 32 days door-to-door.</li>
 <li>Compliant shipment cleared both China export and US import without inspection.</li>
</ul>
<p>Total DG documentation cost: <strong>$450</strong> (one-time UN38.3, reusable for 5 years). Per-unit DG cost on this 500-unit order: <strong>$0.90</strong>.</p>

<h2>Common Mistakes &amp; Penalties</h2>
<ul>
 <li><strong>Under-declaring battery content</strong> (e.g., declaring a power bank as "electronics") — biggest single cause of cargo seizure.</li>
 <li>Shipping UN3480 on a <strong>passenger-belly flight</strong> — cargo offloaded, forwarder fined, shipper blacklisted.</li>
 <li>Missing <strong>UN38.3 report</strong> or an expired one (over 5 years) — shipment refused at origin.</li>
 <li>SOC above <strong>30%</strong> on air shipments — airline rejects the consignment.</li>
 <li>No <strong>lithium-battery mark</strong> or wrong UN number on cartons — customs holds the container.</li>
</ul>
<p>Penalties range from <strong>$1,000</strong> (administrative) to <strong>$10,000+</strong> per violation, plus return freight and storage. Repeat offenses get the shipper on the carrier's DG blacklist.</p>

<h2>How Yeatru Manages Battery Shipments</h2>
<p>Yeatru coordinates DG-certified battery shipping from Shenzhen and Yiwu:</p>
<ul>
 <li>Verify the factory's existing <strong>UN38.3</strong> and <strong>SDS</strong> or arrange fresh testing (CNAS labs, $300–$800).</li>
 <li>Classify the correct <strong>UN number</strong> and IATA/IMDG packaging instruction.</li>
 <li>Supervise <a href="blog-china-customs-clearance.html">export DG declaration</a> and Shipper's Declaration filing.</li>
 <li>Book cargo on <strong>freighter aircraft</strong> for UN3480 (not passenger belly) and DG-accepted ocean lines.</li>
 <li>Ensure carton markings, SOC ≤ 30% for air, and non-conductive inner packaging via pre-shipment QC.</li>
</ul>

<h2>Frequently Asked Questions</h2>
<h3>1. What UN number do I use for lithium batteries from China?</h3>
<p>Use <strong>UN3480</strong> for standalone lithium-ion cells/batteries, <strong>UN3481</strong> for lithium-ion packed with or in equipment, <strong>UN3090</strong> for standalone lithium-metal cells/batteries, and <strong>UN3091</strong> for lithium-metal packed with or in equipment. The UN number drives the packaging instruction (PI965–PI970) and carrier acceptance.</p>
<h3>2. What is UN38.3 and do I need it?</h3>
<p>UN38.3 is a mandatory battery safety test (thermal, vibration, shock, crush, impact, overcharge, short-circuit, altitude) required for all lithium battery shipments. It must be renewed every <strong>5 years</strong> or when cell chemistry changes. Chinese battery factories provide it for <strong>$300–$800</strong> per cell model.</p>
<h3>3. Can I ship lithium batteries by air from China?</h3>
<p>Yes, with restrictions. Most <strong>passenger-belly flights refuse UN3480</strong>; freighter aircraft accept it under PI965. SOC must be <strong>≤ 30%</strong>, inner packaging non-conductive, and package quantity limits apply. Expect a <strong>$0.50–$1.50/kg</strong> DG surcharge on top of standard air rates from <a href="blog-air-freight-china.html">China</a>.</p>
<h3>4. What documents are required to ship batteries from China?</h3>
<p>Required: <strong>UN38.3 test report</strong>, <strong>SDS/MSDS</strong>, <strong>Dangerous Goods Declaration</strong> (DGD for air / Shipper's Declaration for sea), commercial invoice, packing list, and a manufacturer battery letter. For sea, also an IMDG packing certificate from the forwarder.</p>
<h3>5. How should lithium batteries be packaged and labeled?</h3>
<p>Each cell in non-conductive inner packaging, terminals protected against short circuit, cushioned. Outer cartons need the <strong>lithium battery mark</strong>, <strong>UN number</strong> (e.g., UN3480), shipper/consignee, net weight, and orientation labels. Overpacks show "OVERPACK" plus all inner marks.</p>
<h3>6. What are the penalties for non-compliant battery shipments?</h3>
<p>Non-compliance leads to cargo offload (returned at sender's cost), fines of <strong>$1,000–$10,000</strong> per violation, airline/forwarder blacklisting, and in severe cases criminal liability for undeclared DG. Always declare honestly and use a DG-certified forwarder.</p>

<h2>Conclusion</h2>
<p>Shipping batteries from China is manageable if you <strong>classify the UN number</strong>, hold a valid <strong>UN38.3 + MSDS</strong>, and follow IATA (air) or IMDG (sea) packaging rules. Air freight needs ≤30% SOC and freighter aircraft for UN3480; sea freight is cheaper and more permissive as <strong>Class 9</strong>. The cost of compliance (UN38.3 at $300–$800, reusable 5 years) is tiny compared to a $1,000–$10,000 fine or a blacklisted shipment. <a href="contact.html">Send Yeatru your battery spec</a> for a DG-compliant freight quote — we handle classification, documentation, and packaging verification from the factory floor.</p>''',
})

# ============ 4. china-customs-clearance ============
BLOGS.append({
    "slug": "blog-china-customs-clearance",
    "old_desc": "Export customs process, required documents, common issues.",
    "new_desc": "China export customs clearance: document checklist (报关单, 商业发票, 装箱单, 提单, CO/FORM A/E), export agent role, HS code, CIQ, and 1-2 day timing.",
    "subtitle": "Export declaration flow, required documents, export agent, and avoiding HS-code and value mistakes.",
    "headline": "China Export Customs Clearance: Process, Documents & Tips",
    "howto": [
        {"name": "Prepare the export document set", "text": "The supplier or export agent assembles: commercial invoice, packing list, bill of lading/air waybill, export declaration form (报关单), certificate of origin (CO/FORM A/E for preferential tariff), and product-specific certificates (CIQ/SGS for regulated goods)."},
        {"name": "Declare via a customs broker at the port of export", "text": "A licensed customs broker files the electronic declaration (EDI) with China Customs at the port of export (Ningbo, Shanghai, Shenzhen, Guangzhou). The factory's trading company or your 3PL acts as the exporter of record if you lack an import/export license."},
        {"name": "Pass customs inspection", "text": "Customs may inspect (random or targeted) — verify HS code, declared value, and product conformity. Most shipments clear without physical inspection; flagged ones take 1-2 extra days."},
        {"name": "Get release and load", "text": "On release, cargo is loaded onto the vessel or aircraft. The broker sends the verified BL/AWB and customs release note to the shipper. Total clearance time is normally 1-2 days for compliant shipments."},
        {"name": "Avoid the common export pitfalls", "text": "Use the correct HS code (wrong code = under-declaration = smuggling charge), declare the true commercial value (under-declared value triggers fines and holds), and attach mandatory certificates (CIQ for food, wooden packaging, cosmetics)."},
    ],
    "faq": [
        ("What documents are needed for China export customs clearance?", "Core set: (1) commercial invoice (商业发票), (2) packing list (装箱单), (3) bill of lading or air waybill (提单/AWB), (4) export declaration form (报关单), (5) certificate of origin (CO, or FORM A/E for preferential tariff), and (6) product-specific certificates — CIQ inspection for food/wood/cosmetics, test reports for electronics/toys, and export licenses for restricted goods."),
        ("Do I need an export agent to clear China customs?", "If you (the foreign buyer) don't hold a Chinese import/export license (进出口经营权), yes — the factory's own trading company or a third-party export agent acts as the exporter of record. They file the declaration, issue the invoice, and handle tax rebates. Agent fees are $40-$150 per shipment or 0.5%-1% of FOB value."),
        ("What is the export customs clearance process in China?", "1) Supplier/agent prepares documents; 2) licensed broker files electronic declaration with China Customs at the export port; 3) Customs may inspect (random/targeted); 4) on release, cargo loads onto vessel/aircraft. Total time for compliant shipments is 1-2 days."),
        ("Which HS code do I use for export from China?", "Use the China HS code (10-digit) assigned to your product — the supplier or export agent determines it based on product composition and function. The same product has an 8-10 digit export code in China and a destination import code. Misclassifying to lower duty is under-declaration and treated as smuggling; verify against the official HS code database."),
        ("What is a certificate of origin (CO/FORM A/FORM E)?", "A CO (原产地证) certifies the country of manufacture and is required by most destination customs. FORM A (普惠制原产地证) and FORM E (中国-东盟自贸区原产地证) are preferential certificates that reduce or eliminate import duty in the destination country (EU, ASEAN, etc.). The China Council for the Promotion of International Trade (CCPIT) or customs issues them."),
        ("How long does China export customs clearance take?", "Normally 1-2 days for compliant, complete-document shipments. Physical inspections add 1-2 days. Peak season (Sep-Dec) can stretch clearance to 3-4 days due to port congestion. Missing certificates or HS code disputes can hold cargo for 5-10 days."),
    ],
    "body": r'''<aside class="article-takeaways">
 <h2>Key Takeaways</h2>
 <ul>
 <li>China export clearance takes <strong>1–2 days</strong> for compliant shipments and requires a document set: invoice, packing list, BL/AWB, 报关单, CO/FORM A/E, and product certs.</li>
 <li>Without a Chinese <strong>import/export license</strong>, you need the factory's trading company or an <strong>export agent</strong> as exporter of record — fee <strong>$40–$150</strong> or <strong>0.5%–1%</strong> of FOB.</li>
 <li><strong>Wrong HS code</strong> or <strong>under-declared value</strong> = smuggling charge, fines, and cargo hold — always declare the correct 10-digit China HS code and true commercial value.</li>
 <li>Regulated goods (food, wood packaging, cosmetics) need a <strong>CIQ inspection certificate</strong> (商检) before release; allow <strong>2–5 extra days</strong>.</li>
 <li>Preferential certificates <strong>FORM A / FORM E</strong> cut your destination import duty to <strong>0%–5%</strong> — request them from CCPIT with the CO.</li>
 </ul>
</aside>

<div class="geo-definition">
 <h2>What Is China Export Customs Clearance?</h2>
 <p>China export customs clearance (出口报关) is the mandatory declaration of goods to <strong>China Customs (中国海关)</strong> before they leave the country. It confirms the goods are legal to export, classifies them by HS code, and records the value for VAT rebate and statistics. Whether you ship by <a href="blog-sea-freight-china.html">sea</a> from Ningbo or <a href="blog-air-freight-china.html">air</a> from PVG, your cargo cannot board until China Customs releases it. For foreign buyers without a Chinese import/export license, the factory's trading company or a third-party export agent handles this as the <strong>exporter of record</strong>.</p>
</div>

<h2>Export Documents Checklist</h2>
<div class="table-responsive"><table class="geo-comparison-table">
 <thead><tr><th>Document</th><th>Purpose</th><th>Who Provides</th></tr></thead>
 <tbody>
 <tr><td><strong>报关单 (Export Declaration Form)</strong></td><td>Official declaration to China Customs (HS code, value, quantity)</td><td>Customs broker / export agent</td></tr>
 <tr><td><strong>商业发票 (Commercial Invoice)</strong></td><td>Proves transaction value for duty/rebate</td><td>Exporter of record</td></tr>
 <tr><td><strong>装箱单 (Packing List)</strong></td><td>Carton count, weight, dimensions</td><td>Factory / exporter</td></tr>
 <tr><td><strong>提单 / AWB (Bill of Lading)</strong></td><td>Contract of carriage, title to goods</td><td>Shipping line / airline</td></tr>
 <tr><td><strong>原产地证 (CO / FORM A / E)</strong></td><td>Country of origin; preferential tariff at destination</td><td>CCPIT / Customs</td></tr>
 <tr><td><strong>商检 (CIQ Inspection Cert)</strong></td><td>Mandatory for food, wood, cosmetics, regulated goods</td><td>CIQ-accredited lab</td></tr>
 <tr><td>Product test reports</td><td>FCC, CE, CPC, RoHS — for destination compliance</td><td>Factory / third-party lab</td></tr>
 </tbody>
</table></div>

<h2>The 4-Step Export Clearance Process</h2>
<ol>
 <li><strong>Document preparation (0.5–1 day)</strong> — the factory or export agent gathers invoice, packing list, BL draft, CO, and product certs.</li>
 <li><strong>Electronic declaration (same day)</strong> — a licensed customs broker files the 报关单 via China Customs' EDI system at the port of export (Ningbo, Shanghai, Shenzhen Yantian, Guangzhou).</li>
 <li><strong>Inspection (optional, 0–2 days)</strong> — Customs selects ~5%–10% of shipments for physical inspection (X-ray or open-box) based on HS-code risk, value, and shipper history.</li>
 <li><strong>Release &amp; loading (same day)</strong> — on release, cargo gates into the port and loads onto the vessel/aircraft. The broker sends the verified BL/AWB.</li>
</ol>
<p>Total clearance: <strong>1–2 days</strong> standard; <strong>3–5 days</strong> if inspection or CIQ applies. Peak season (Sep–Dec) adds 1–2 days of port congestion.</p>

<h2>The Export Agent's Role</h2>
<p>Most foreign buyers don't hold a Chinese <strong>进出口经营权</strong> (import/export license). In that case:</p>
<ul>
 <li>The factory's own <strong>trading company</strong> (外贸公司) acts as exporter of record — included in most FOB quotes.</li>
 <li>Or a <strong>third-party export agent</strong> files the declaration, issues the commercial invoice in their name, and handles the VAT export rebate (退税).</li>
 <li>Agent fee: <strong>$40–$150</strong> per shipment or <strong>0.5%–1%</strong> of FOB value. They absorb the compliance risk and rebate paperwork.</li>
</ul>
<p>For <a href="blog-ddp-shipping-china.html">DDP shipments</a>, the forwarder usually bundles export clearance into the all-in rate, so you won't see a separate agent line item.</p>

<h2>Worked Example: Yiwu Order Export via Ningbo</h2>
<p>A US buyer imports <strong>2,000 silicone kitchen tools</strong> (EXW $1.80, 6 cbm) from a Yiwu factory, FOB Ningbo.</p>
<ul>
 <li>Yiwu factory's trading company acts as exporter; prepares invoice, packing list, and BL draft.</li>
 <li>Inland truck Yiwu → Ningbo: <strong>$120</strong> (1 day).</li>
 <li>Ningbo customs broker files declaration; goods selected for <strong>wooden-pallet CIQ inspection</strong> (fumigation cert) — 1 extra day, <strong>$60</strong>.</li>
 <li>Customs releases; cargo loads on Maersk line to Long Beach.</li>
 <li><strong>Total export clearance: 2 days, $180</strong> (trucking + CIQ + broker fee).</li>
</ul>
<p>The CO and FORM A were issued by CCPIT in Yiwu (<strong>$15</strong> each), reducing the US import duty from 7.5% to <strong>0%</strong> under the de minimis / GSP treatment — saving <strong>$270</strong> on a $3,600 shipment.</p>

<h2>Common Export Clearance Issues</h2>
<ul>
 <li><strong>Wrong HS code</strong> — using a lower-duty code to evade duty is <strong>smuggling</strong> (走私). Penalty: fine + cargo detention + potential criminal liability. Always verify the 10-digit China HS code against the official database.</li>
 <li><strong>Under-declared value</strong> — declaring $1 when the real value is $5 triggers a customs valuation review and fines of <strong>30%–100%</strong> of the under-declared amount.</li>
 <li><strong>Missing CIQ for regulated goods</strong> — food, wooden packaging, cosmetics, toys, and batteries all need inspection certificates; missing them holds the container.</li>
 <li><strong>No CO / preferential certificate</strong> — missing FORM A/E means you pay the full MFN duty rate at destination instead of <strong>0%–5%</strong>.</li>
 <li><strong>Brand/IP issues</strong> — branded goods without authorization get seized at export; register your brand with Chinese customs (知识产权备案) to prevent counterfeits leaving, or get a brand authorization letter.</li>
</ul>

<h2>How Yeatru Handles Export Clearance</h2>
<p>Yeatru manages export clearance as part of our <a href="blog-ddp-shipping-china.html">DDP shipping</a> and FOB services:</p>
<ul>
 <li>Act as exporter of record via our Yiwu trading company (for clients without a China license).</li>
 <li>Verify the correct <a href="blog-hs-code-lookup-china.html">HS code</a> before declaration to avoid under-declaration risk.</li>
 <li>Arrange CIQ inspection and <a href="blog-product-certifications-china.html">product certifications</a> (CPC, FCC, CE) for regulated goods.</li>
 <li>Issue CO and preferential certificates (FORM A/E) through CCPIT to minimize destination duty.</li>
 <li>Real-time clearance status from declaration to release.</li>
</ul>

<h2>Frequently Asked Questions</h2>
<h3>1. What documents are needed for China export customs clearance?</h3>
<p>Core set: (1) <strong>commercial invoice</strong>, (2) <strong>packing list</strong>, (3) <strong>BL or AWB</strong>, (4) <strong>export declaration form (报关单)</strong>, (5) <strong>certificate of origin</strong> (CO, or FORM A/E for preferential tariff), and (6) product-specific certificates — CIQ for food/wood/cosmetics, test reports for electronics/toys, and export licenses for restricted goods.</p>
<h3>2. Do I need an export agent to clear China customs?</h3>
<p>If you don't hold a Chinese import/export license, yes — the factory's trading company or a third-party <strong>export agent</strong> acts as exporter of record. They file the declaration, issue the invoice, and handle VAT rebates. Fees are <strong>$40–$150</strong> per shipment or <strong>0.5%–1%</strong> of FOB value.</p>
<h3>3. What is the export customs clearance process in China?</h3>
<p>(1) Supplier/agent prepares documents; (2) licensed broker files electronic declaration with China Customs at the export port; (3) Customs may inspect (random/targeted); (4) on release, cargo loads. Total time for compliant shipments is <strong>1–2 days</strong>.</p>
<h3>4. Which HS code do I use for export from China?</h3>
<p>Use the <strong>10-digit China HS code</strong> assigned to your product, determined by the supplier or export agent based on composition and function. Misclassifying to lower duty is under-declaration and treated as smuggling. Verify against the official database — see our <a href="blog-hs-code-lookup-china.html">HS code lookup guide</a>.</p>
<h3>5. What is a certificate of origin (CO / FORM A / FORM E)?</h3>
<p>A <strong>CO</strong> certifies country of manufacture and is required by most destination customs. <strong>FORM A</strong> and <strong>FORM E</strong> are preferential certificates that reduce or eliminate import duty (EU, ASEAN, etc.). CCPIT or China Customs issues them; FORM E can cut ASEAN duty to <strong>0%–5%</strong>.</p>
<h3>6. How long does China export customs clearance take?</h3>
<p>Normally <strong>1–2 days</strong> for compliant, complete-document shipments. Physical inspections add 1–2 days. Peak season (Sep–Dec) stretches clearance to 3–4 days due to port congestion. Missing certificates or HS-code disputes can hold cargo for 5–10 days.</p>

<h2>Conclusion</h2>
<p>China export clearance is a <strong>1–2 day</strong> process built on a complete document set, a correct HS code, and an exporter of record (factory trading company or export agent). The biggest risks are <strong>wrong HS codes</strong> and <strong>under-declared values</strong> — both treated as smuggling with heavy fines. Always request a <strong>CO and preferential FORM A/E</strong> to cut destination duty, and factor in <strong>2–5 extra days</strong> for CIQ on regulated goods. <a href="contact.html">Ask Yeatru</a> to handle your export declaration — we verify the HS code, arrange CIQ and certificates, and clear your cargo from Ningbo, Shanghai, Shenzhen, or Guangzhou with real-time status.</p>''',
})

# ============ 5. import-from-china-step-by-step ============
BLOGS.append({
    "slug": "blog-import-from-china-step-by-step",
    "old_desc": "Complete import process: find supplier, sample, QC, ship, customs.",
    "new_desc": "How to import from China in 10 steps: product research, supplier verification, RFQ, QC, export/import customs, shipping, and landed cost with timeline and documents.",
    "subtitle": "10-step beginner's import guide with cost, timeline, documents, and incoterms advice.",
    "headline": "How to Import from China: Step-by-Step Guide (2026)",
    "howto": [
        {"name": "Research the product and check compliance", "text": "Validate demand, calculate target landed cost, and check destination regulations (FCC, FDA, CE, CPC) and tariffs before contacting any supplier. Use the HS code to estimate duty and Section 301 impact."},
        {"name": "Source and verify 3-5 suppliers", "text": "Find factories on Alibaba, 1688, Canton Fair, or via a sourcing agent. Verify each supplier's business license, factory audit, and trade history. Never commit to the first quote."},
        {"name": "Run RFQ, negotiate, and sign a contract", "text": "Send a detailed RFQ (specs, MOQ, incoterm, payment terms) to 3+ suppliers, compare total landed cost, and sign a written contract with QC clauses, penalty terms, and an IP/NDA."},
        {"name": "Manage production and pre-shipment QC", "text": "Pay 30% deposit to start production, monitor milestones, and run an AQL 2.5 pre-shipment inspection before paying the 70% balance. QC catches defects before cargo leaves China."},
        {"name": "Ship, clear destination customs, and deliver", "text": "Choose FOB or DDP shipping, clear export (China) and import (destination) customs, pay duty/VAT, and arrange last-mile to your warehouse or Amazon FBA. Reorder based on sell-through."},
    ],
    "faq": [
        ("What are the steps to import from China?", "The 10-step process: (1) product research & compliance check, (2) supplier sourcing & verification, (3) RFQ & sample, (4) negotiate & sign contract, (5) production & QC, (6) China export customs, (7) international shipping, (8) destination import customs, (9) last-mile delivery / FBA, (10) sell & reorder. Each step has cost, timeline, and document requirements."),
        ("How much does it cost to import from China?", "Total landed cost = product EXW + China inland ($80-$500) + export clearance ($40-$150) + freight (sea $0.50-$1.50/kg or air $4-$9/kg) + destination duty (0%-25%) + VAT (0%-20%) + last-mile ($0.50-$3/unit). For a $5 EXW product shipped sea DDP to the US, landed cost is typically $7-$9/unit."),
        ("What documents do I need to import from China?", "Required: commercial invoice, packing list, bill of lading (sea) or AWB (air), certificate of origin (CO/FORM A/E), product certifications (FCC, CE, CPC, FDA), and an import license if your country requires one for the product category. The supplier provides most; your forwarder handles BL/AWB and clearance docs."),
        ("FOB or DDP for a first-time importer?", "Use DDP (Delivered Duty Paid) for your first 1-3 orders: the supplier/forwarder handles export, freight, duty, and delivery to your door. Once you have a destination broker and volume, switch to FOB to control freight and save 5%-15%. EXW is cheapest unit price but shifts all logistics and risk to you."),
        ("Do I need an import license to buy from China?", "For most consumer goods imported into the US, EU, UK, AU, and GCC, no special import license is required — you just need a business registration and a tax ID. Restricted categories (food, drugs, medical devices, radio equipment, weapons) do require import permits or product-specific registrations."),
        ("How long does it take to import from China?", "Stock product by sea: 25-50 days total (RFQ 3-10 + production 15-30 + shipping 25-40 + clearance 2-4). By air: 5-15 days. OEM/private-label: 60-120 days (adds 15-45 days for mold/tooling). Peak season Sep-Dec adds 5-15 days."),
    ],
    "body": r'''<aside class="article-takeaways">
 <h2>Key Takeaways</h2>
 <ul>
 <li>Importing from China is a <strong>10-step process</strong> from product research to reorder; total timeline is <strong>25–50 days</strong> (sea) or <strong>5–15 days</strong> (air) for stock products.</li>
 <li>Total landed cost = <strong>EXW + inland ($80–$500) + export clearance ($40–$150) + freight + duty (0%–25%) + VAT + last-mile</strong>; a $5 EXW product lands at <strong>$7–$9/unit</strong> by sea DDP to the US.</li>
 <li>Beginners should use <a href="blog-fob-vs-exw-vs-ddp.html"><strong>DDP</strong></a> (door-to-door, duty paid); switch to FOB once you have volume and a destination broker to save <strong>5%–15%</strong>.</li>
 <li>Always run <strong>AQL 2.5 pre-shipment QC</strong> before paying the 70% balance — defects caught in China cost <strong>1/10th</strong> of fixing them at destination.</li>
 <li>Key documents: commercial invoice, packing list, BL/AWB, <a href="blog-china-customs-clearance.html">CO/FORM A/E</a>, and product certs (FCC, CE, CPC, FDA).</li>
 </ul>
</aside>

<div class="geo-definition">
 <h2>What Does "Import from China" Involve?</h2>
 <p>Importing from China is the end-to-end process of sourcing goods from a Chinese supplier, moving them across the border, clearing destination customs, and delivering them to your warehouse or marketplace. It spans <strong>product research, supplier verification, contracting, production, quality control, export and import customs, freight, and last-mile delivery</strong>. For beginners, the biggest mistake is comparing only unit price — the real decision is <strong>total landed cost</strong>, which includes freight, duty, and fees that can double the EXW price.</p>
</div>

<h2>The 10-Step Import Process (2026)</h2>
<div class="table-responsive"><table class="geo-comparison-table">
 <thead><tr><th>Step</th><th>Cost Range</th><th>Timeline</th><th>Key Document</th></tr></thead>
 <tbody>
 <tr><td>1. Product research &amp; compliance</td><td>$0 – $500 (tests)</td><td>1 – 5 days</td><td>HS code, target landed cost</td></tr>
 <tr><td>2. Supplier sourcing &amp; verification</td><td>$0 – $300 (audit)</td><td>3 – 10 days</td><td>Business license, factory audit</td></tr>
 <tr><td>3. RFQ &amp; sample</td><td>$20 – $200 (sample+ship)</td><td>3 – 10 days</td><td>RFQ sheet, sample</td></tr>
 <tr><td>4. Negotiate &amp; sign contract</td><td>$0</td><td>2 – 5 days</td><td>PI, sales contract, NDA</td></tr>
 <tr><td>5. Production &amp; QC</td><td>$0 – $300 (inspection)</td><td>15 – 60 days</td><td>AQL 2.5 QC report</td></tr>
 <tr><td>6. China export customs</td><td>$40 – $150</td><td>1 – 2 days</td><td>报关单, CO/FORM A/E</td></tr>
 <tr><td>7. International shipping</td><td>$0.50 – $9/kg</td><td>3 – 40 days</td><td>BL / AWB</td></tr>
 <tr><td>8. Destination import customs</td><td>0% – 25% duty</td><td>1 – 3 days</td><td>Import declaration, duty receipt</td></tr>
 <tr><td>9. Last-mile / FBA</td><td>$0.50 – $3/unit</td><td>1 – 5 days</td><td>Proof of delivery</td></tr>
 <tr><td>10. Sell &amp; reorder</td><td>—</td><td>Ongoing</td><td>Reorder PO</td></tr>
 </tbody>
</table></div>

<h2>Steps 1–4: From Research to Signed Contract</h2>
<ol>
 <li><strong>Product research &amp; compliance check</strong> — validate demand (Amazon BSR, TikTok trends, Google Trends), calculate target landed cost, and check destination regulations (FCC for electronics, FDA for food, <a href="blog-cpc-certificate-children.html">CPC</a> for toys, CE for EU). Identify the <a href="blog-hs-code-lookup-china.html">HS code</a> to estimate duty.</li>
 <li><strong>Supplier sourcing &amp; verification</strong> — find 3–5 factories on Alibaba, 1688, or at Canton Fair. Verify each <a href="blog-verify-chinese-supplier-license.html">business license</a> on gsxt.gov.cn, ask for a factory audit, and check trade history. Avoid trading companies posing as factories.</li>
 <li><strong>RFQ &amp; sample</strong> — send a detailed <a href="blog-rfq-guide-china-sourcing.html">RFQ</a> (specs, MOQ, incoterm, payment terms, packaging). Order samples ($20–$200 shipped) and test against your spec.</li>
 <li><strong>Negotiate &amp; sign contract</strong> — compare total landed cost (not just unit price), negotiate MOQ and payment terms, and sign a written contract with QC pass/fail clauses, penalty terms, and an IP/NDA.</li>
</ol>

<h2>Steps 5–7: Production, QC, and Shipping</h2>
<ol start="5">
 <li><strong>Production &amp; QC</strong> — pay <strong>30% deposit</strong> to start production. Mid-production, run an in-line check; before shipment, run an <strong>AQL 2.5 pre-shipment inspection</strong> ($80–$300/man-day). Only pay the 70% balance after QC passes.</li>
 <li><strong>China export customs</strong> — the factory's trading company or export agent files the declaration (see our <a href="blog-china-customs-clearance.html">export clearance guide</a>). 1–2 days, $40–$150.</li>
 <li><strong>International shipping</strong> — choose <a href="blog-sea-freight-china.html">sea</a> (25–40 days, $0.50–$1.50/kg) or <a href="blog-air-freight-china.html">air</a> (3–7 days, $4–$9/kg). For beginners, <a href="blog-ddp-shipping-china.html">DDP</a> (door-to-door, duty paid) is simplest.</li>
</ol>

<h2>Steps 8–10: Import Clearance, Delivery, Reorder</h2>
<ol start="8">
 <li><strong>Destination import customs</strong> — your forwarder or broker clears the goods, pays duty (0%–25%) and VAT (0%–20%), and releases the cargo. 1–3 days.</li>
 <li><strong>Last-mile / FBA</strong> — truck from port to your warehouse ($0.50–$3/unit) or direct to Amazon FBA. For FBA, ensure FNSKU labeling and carton rules before shipping.</li>
 <li><strong>Sell &amp; reorder</strong> — monitor sell-through and place a reorder PO 45+ days before stockout (sea) or 10+ days (air).</li>
</ol>

<h2>Incoterms for Importers: FOB vs CIF vs DDP</h2>
<div class="table-responsive"><table class="geo-comparison-table">
 <thead><tr><th>Incoterm</th><th>Who Pays Freight</th><th>Who Clears Customs</th><th>Risk Transfer</th><th>Best For</th></tr></thead>
 <tbody>
 <tr><td><strong>EXW</strong></td><td>Buyer</td><td>Buyer</td><td>At factory door</td><td>Large volume, own broker</td></tr>
 <tr><td><strong>FOB</strong></td><td>Buyer</td><td>Buyer (import)</td><td>On board vessel</td><td>Experienced importers</td></tr>
 <tr><td><strong>CIF</strong></td><td>Seller</td><td>Buyer (import)</td><td>On board vessel</td><td>Avoid — seller controls freight</td></tr>
 <tr><td><strong>DDP</strong></td><td>Seller</td><td>Seller (both)</td><td>At buyer's door</td><td>Beginners, small orders</td></tr>
 </tbody>
</table></div>
<p><strong>Beginner rule:</strong> start with <strong>DDP</strong> for your first 1–3 orders — the supplier/forwarder handles everything to your door. Once you have volume and a destination broker, switch to <strong>FOB</strong> to control freight and save 5%–15%. Avoid <strong>CIF</strong>: the supplier picks the (often slow, expensive) line and hides freight margin. See our full <a href="blog-fob-vs-exw-vs-ddp.html">incoterms comparison</a>.</p>

<h2>Worked Example: First-Time Importer, 1,000 Units EXW $5</h2>
<p>A US first-time importer buys <strong>1,000 silicone kitchen tools</strong> at <strong>$5 EXW</strong> from a Yiwu factory, shipped by <strong>sea DDP</strong> to a Los Angeles warehouse.</p>
<ul>
 <li>Product: 1,000 × $5 = <strong>$5,000</strong></li>
 <li>Sample (air courier): <strong>$80</strong></li>
 <li>AQL 2.5 pre-shipment QC (1 man-day): <strong>$180</strong></li>
 <li>China export clearance (included in DDP): <strong>$0</strong></li>
 <li>Sea DDP freight (4 cbm × $90/cbm): <strong>$360</strong></li>
 <li>US duty (7.5% of $5,000): <strong>$375</strong> (prepaid in DDP)</li>
 <li>Last-mile (port → LA warehouse): included in DDP</li>
 <li><strong>Total landed: $5,995 → $5.99/unit</strong></li>
 <li><strong>Timeline:</strong> RFQ/sample 7 days + production 20 days + QC 1 day + sea 30 days + clearance 2 days = <strong>~60 days</strong> door-to-door</li>
</ul>

<h2>How Yeatru Guides First-Time Importers</h2>
<p>Yeatru's full-service import pipeline removes the guesswork:</p>
<ul>
 <li>Product compliance pre-check (HS code, FCC/FDA/CE/CPC, duty estimate) — free.</li>
 <li>3 verified factory quotes side-by-side with total landed cost breakdown.</li>
 <li><a href="blog-rfq-guide-china-sourcing.html">RFQ</a>, sample coordination, and <a href="blog-verify-chinese-supplier-license.html">supplier verification</a>.</li>
 <li><a href="blog-china-quality-control-inspection.html">AQL 2.5 QC</a> with photo/video before the 70% balance.</li>
 <li><a href="blog-ddp-shipping-china.html">DDP door-to-door shipping</a> with duty prepaid and real-time tracking.</li>
</ul>

<h2>Frequently Asked Questions</h2>
<h3>1. What are the steps to import from China?</h3>
<p>The 10-step process: (1) product research &amp; compliance check, (2) supplier sourcing &amp; verification, (3) RFQ &amp; sample, (4) negotiate &amp; sign contract, (5) production &amp; QC, (6) China export customs, (7) international shipping, (8) destination import customs, (9) last-mile delivery / FBA, (10) sell &amp; reorder. Each step has cost, timeline, and document requirements — see the table above.</p>
<h3>2. How much does it cost to import from China?</h3>
<p>Total landed cost = product EXW + China inland (<strong>$80–$500</strong>) + export clearance (<strong>$40–$150</strong>) + freight (sea <strong>$0.50–$1.50/kg</strong> or air <strong>$4–$9/kg</strong>) + duty (<strong>0%–25%</strong>) + VAT (<strong>0%–20%</strong>) + last-mile (<strong>$0.50–$3/unit</strong>). A $5 EXW product shipped sea DDP to the US lands at <strong>$7–$9/unit</strong>.</p>
<h3>3. What documents do I need to import from China?</h3>
<p>Required: commercial invoice, packing list, bill of lading (sea) or AWB (air), certificate of origin (CO/FORM A/E), product certifications (FCC, CE, CPC, FDA), and an import license if your country requires one. The supplier provides most; your forwarder handles BL/AWB and clearance docs.</p>
<h3>4. FOB or DDP for a first-time importer?</h3>
<p>Use <strong>DDP</strong> for your first 1–3 orders: the supplier/forwarder handles export, freight, duty, and delivery to your door. Once you have a destination broker and volume, switch to <strong>FOB</strong> to control freight and save <strong>5%–15%</strong>. EXW is cheapest unit price but shifts all logistics and risk to you — see our <a href="blog-fob-vs-exw-vs-ddp.html">incoterms guide</a>.</p>
<h3>5. Do I need an import license to buy from China?</h3>
<p>For most consumer goods into the US, EU, UK, AU, and GCC, no special import license is required — just a business registration and tax ID. Restricted categories (food, drugs, medical devices, radio equipment, weapons) do require import permits or product-specific registrations.</p>
<h3>6. How long does it take to import from China?</h3>
<p>Stock product by sea: <strong>25–50 days</strong> total (RFQ 3–10 + production 15–30 + shipping 25–40 + clearance 2–4). By air: <strong>5–15 days</strong>. OEM/private-label: <strong>60–120 days</strong> (adds 15–45 days for mold/tooling). Peak season Sep–Dec adds 5–15 days.</p>

<h2>Conclusion</h2>
<p>Importing from China is a repeatable 10-step process — the learning curve is in understanding <strong>total landed cost</strong> (not just unit price) and enforcing <strong>QC before the balance payment</strong>. For first orders, use <strong>DDP</strong> to hand off logistics and duty; for repeat orders, switch to <strong>FOB</strong> to save 5%–15%. Plan <strong>45+ days</strong> for sea and <strong>10+ days</strong> for air, and always verify the supplier before paying a deposit. <a href="contact.html">Get a free landed-cost estimate</a> from Yeatru — we'll map your 10-step plan with real numbers for your product and destination.</p>''',
})

# ============ 6. incoterms-china-sourcing ============
BLOGS.append({
    "slug": "blog-incoterms-china-sourcing",
    "old_desc": "Most common Incoterms for China imports, when to use each.",
    "new_desc": "FOB vs EXW vs CIF vs DDP Incoterms 2020 for China sourcing: who pays freight, risk transfer points, cost comparison, and which to choose by experience.",
    "subtitle": "Incoterms 2020 cost & risk comparison for China imports — EXW, FOB, CIF, DDP, FCA, CPT.",
    "headline": "FOB vs EXW vs CIF vs DDP: Incoterms for China Sourcing",
    "howto": [
        {"name": "Understand the four core China incoterms", "text": "EXW (Ex Works): buyer handles everything from the factory door — cheapest unit price, most work/risk. FOB (Free On Board): supplier delivers to the ship, buyer handles ocean freight and insurance — the China default. CIF (Cost Insurance Freight): supplier pays freight and insurance to destination port — riskier, supplier controls freight. DDP (Delivered Duty Paid): supplier handles everything to the buyer's door — simplest, highest unit price."},
        {"name": "Map risk transfer and responsibility", "text": "Risk transfers at the factory door (EXW), on board the vessel (FOB/CIF), or at the buyer's door (DDP). Responsibility for export clearance is the seller's in FOB/CIF/DDP and the buyer's in EXW; import clearance is the buyer's in EXW/FOB/CIF and the seller's in DDP."},
        {"name": "Compare total landed cost, not unit price", "text": "EXW has the lowest unit price but adds inland, export clearance, freight, duty, and last-mile that you must arrange. DDP bundles everything into one price. For a $5 EXW product, expect FOB ~$5.30, CIF ~$5.80, DDP ~$6.50 landed-equivalent — but DDP removes your admin and risk."},
        {"name": "Choose by your experience and volume", "text": "Beginners and small orders: DDP (hand off all logistics). Experienced importers with a destination broker: FOB (control freight, save 5-15%). Large volume with your own China trucking and broker: EXW (lowest all-in cost). Avoid CIF — suppliers game it with slow lines and inflated freight."},
        {"name": "Watch for supplier gaming on CIF and FOB", "text": "On CIF, suppliers may use slow steamship lines or inflate freight by 20-40%. On FOB, ensure the supplier's local charges (THC, documentation) are in the quote; hidden port fees can add $100-$300 per shipment. Always ask for an all-in FOB breakdown."},
    ],
    "faq": [
        ("What is the difference between EXW, FOB, CIF, and DDP?", "EXW: buyer picks up at the factory and handles all logistics, export, import, and duty. FOB: seller delivers to the ship; buyer pays ocean freight, insurance, import, and duty. CIF: seller pays freight and insurance to the destination port; buyer clears import and pays duty. DDP: seller handles everything to the buyer's door, including import duty. Risk transfers at factory door (EXW), on board (FOB/CIF), or buyer's door (DDP)."),
        ("Which incoterm is best for beginners sourcing from China?", "DDP (Delivered Duty Paid). The supplier or forwarder handles export clearance, freight, insurance, import duty, and last-mile delivery to your door. You get one all-in price and zero customs admin. Once you have volume and a destination broker, switch to FOB to save 5-15%."),
        ("Why should I avoid CIF when sourcing from China?", "Under CIF the supplier selects the shipping line and pays freight, so they often use the slowest, cheapest carrier (adding 5-10 transit days) and may inflate the freight cost by 20-40% as a hidden margin. You also have no control over the vessel or routing. FOB or DDP gives you transparency on the freight line item."),
        ("Is EXW cheaper than FOB for large orders?", "Yes, EXW has the lowest unit price because the supplier does no logistics. But you must arrange China inland trucking ($80-$500), export clearance ($40-$150), freight, insurance, import clearance, and duty yourself. Only choose EXW for large volume (full containers, $50k+) where you have a China trucking broker and destination customs broker."),
        ("What is the cost difference between EXW, FOB, CIF, and DDP?", "For a $5 EXW product: FOB ~$5.30 (supplier adds inland + export clearance), CIF ~$5.80 (supplier adds freight + insurance to port), DDP ~$6.50 (supplier adds everything to door including duty). The DDP premium ($1.50) buys you zero logistics admin and risk transfer — worth it for small or first orders."),
        ("Are FCA, CPT, and CIP relevant for China sourcing?", "FCA (Free Carrier) is common for air freight and LCL — supplier delivers to a named carrier at the port/airport. CPT (Carriage Paid To) and CIP (Carriage and Insurance Paid To) are the air/multimodal equivalents of CFR/CIF. For most China sea-FCL importers, FOB and DDP cover 90% of use cases; FCA matters for air and LCL shipments."),
    ],
    "body": r'''<aside class="article-takeaways">
 <h2>Key Takeaways</h2>
 <ul>
 <li><strong>EXW</strong> = lowest unit price, most work/risk (you handle factory-to-door); <strong>DDP</strong> = highest unit price, zero work/risk (supplier delivers to your door).</li>
 <li><strong>FOB</strong> is the China default for sea FCL — supplier delivers to the vessel, you pay freight; saves <strong>5%–15%</strong> vs DDP once you have a broker.</li>
 <li><strong>Avoid CIF</strong> — suppliers game it with slow lines and <strong>20%–40%</strong> inflated freight; you lose vessel control.</li>
 <li>For a <strong>$5 EXW</strong> product: FOB ≈ <strong>$5.30</strong>, CIF ≈ <strong>$5.80</strong>, DDP ≈ <strong>$6.50</strong> landed-equivalent.</li>
 <li>Beginners → <strong>DDP</strong>; experienced with broker → <strong>FOB</strong>; large volume → <strong>EXW</strong>. See <a href="blog-fob-vs-exw-vs-ddp.html">full comparison</a>.</li>
 </ul>
</aside>

<div class="geo-definition">
 <h2>What Are Incoterms for China Sourcing?</h2>
 <p>Incoterms (published by the ICC, current version <strong>Incoterms 2020</strong>) are 11 standard trade terms that define <strong>who pays for freight, who clears customs, and where risk transfers</strong> between buyer and seller. When sourcing from China, four terms cover 95% of shipments: <strong>EXW, FOB, CIF, and DDP</strong>. Choosing the wrong one can cost you 10%–30% in hidden freight, surprise duty bills, or lost cargo. The golden rule: compare <strong>total landed cost</strong>, not the unit price on the PI.</p>
</div>

<h2>Core Incoterms Comparison (China Sourcing)</h2>
<div class="table-responsive"><table class="geo-comparison-table">
 <thead><tr><th>Incoterm</th><th>Who Pays Freight</th><th>Export Clearance</th><th>Import Clearance</th><th>Risk Transfer</th><th>Best For</th></tr></thead>
 <tbody>
 <tr><td><strong>EXW</strong> (Ex Works)</td><td>Buyer</td><td>Buyer</td><td>Buyer</td><td>At factory door</td><td>Large volume, own broker</td></tr>
 <tr><td><strong>FOB</strong> (Free On Board)</td><td>Buyer</td><td>Seller</td><td>Buyer</td><td>On board vessel</td><td>Experienced sea importers</td></tr>
 <tr><td><strong>CIF</strong> (Cost Ins. Freight)</td><td>Seller</td><td>Seller</td><td>Buyer</td><td>On board vessel</td><td>Avoid — supplier controls freight</td></tr>
 <tr><td><strong>DDP</strong> (Delivered Duty Paid)</td><td>Seller</td><td>Seller</td><td>Seller</td><td>At buyer's door</td><td>Beginners, small orders</td></tr>
 <tr><td><strong>FCA</strong> (Free Carrier)</td><td>Buyer</td><td>Seller</td><td>Buyer</td><td>To named carrier</td><td>Air freight, LCL</td></tr>
 </tbody>
</table></div>

<h2>EXW, FOB, CIF, DDP — What Each Really Means</h2>
<ul>
 <li><strong>EXW (Ex Works)</strong> — the seller makes goods available at their factory; you arrange and pay for everything: China inland trucking, export clearance, ocean freight, insurance, import duty, and last-mile. Lowest unit price, but only viable if you have a China trucking broker and destination customs broker.</li>
 <li><strong>FOB (Free On Board)</strong> — the seller delivers goods onto the vessel at the named port of shipment (e.g., FOB Ningbo). You pay for ocean freight, insurance, import clearance, and duty. <strong>Most common</strong> for China sea FCL because the seller handles export and you control the freight line.</li>
 <li><strong>CIF (Cost, Insurance, Freight)</strong> — the seller pays freight and insurance to the destination port. Risk still transfers when goods go on board (same as FOB). <strong>Avoid</strong>: the seller picks the line and may use slow steamships or inflate freight by 20%–40%.</li>
 <li><strong>DDP (Delivered Duty Paid)</strong> — the seller handles everything to your door: export, freight, insurance, import duty, and last-mile. <strong>Simplest</strong> for beginners — one all-in price, zero customs admin.</li>
</ul>

<h2>Cost Comparison: Same Order, Four Incoterms</h2>
<p>A 1,000-unit order at <strong>$5.00 EXW</strong> from Yiwu to Los Angeles (4 cbm, sea):</p>
<div class="table-responsive"><table class="geo-comparison-table">
 <thead><tr><th>Incoterm</th><th>Unit Price</th><th>What's Included</th><th>Your Extra Work</th></tr></thead>
 <tbody>
 <tr><td>EXW</td><td><strong>$5.00</strong></td><td>Goods at factory door only</td><td>Inland + export + freight + duty + delivery</td></tr>
 <tr><td>FOB (Ningbo)</td><td><strong>$5.30</strong></td><td>+ inland + export clearance to vessel</td><td>Freight + insurance + duty + delivery</td></tr>
 <tr><td>CIF (LA)</td><td><strong>$5.80</strong></td><td>+ freight + insurance to LA port</td><td>Duty + clearance + delivery</td></tr>
 <tr><td>DDP (your door)</td><td><strong>$6.50</strong></td><td>Everything to door, duty paid</td><td>Nothing — receive and sell</td></tr>
 </tbody>
</table></div>
<p>The <strong>DDP premium ($1.50/unit)</strong> buys you zero logistics admin, no duty surprises, and risk transferred to your door. For a $5,000 order that's <strong>$1,500</strong> — worth it for first orders or when your team lacks a broker. For repeat $50k+ orders, FOB saves <strong>$4,000+</strong> per shipment once you control freight.</p>

<h2>Which Incoterm Should You Choose?</h2>
<ul>
 <li><strong>Beginners / small orders (&lt;$10k)</strong> → <strong>DDP</strong>. One price, door-to-door, no customs paperwork. Use a reputable forwarder, not the cheapest Alibaba DDP quote.</li>
 <li><strong>Experienced importers with a destination broker</strong> → <strong>FOB</strong>. You control the ocean line, consolidate cargo, and save 5%–15% vs DDP. Get an all-in FOB quote including THC and docs.</li>
 <li><strong>Large volume (FCL, $50k+)</strong> → <strong>EXW</strong>. Lowest unit price; you run your own China trucking and destination clearance. Only if you have reliable brokers on both ends.</li>
 <li><strong>Air freight / LCL</strong> → <strong>FCA</strong>. Supplier delivers to the airline or consolidator's warehouse; you control the air or LCL rate.</li>
</ul>

<h2>How Suppliers Game CIF (and FOB)</h2>
<ul>
 <li><strong>CIF freight inflation</strong> — supplier quotes "free freight" but marks up the ocean rate by <strong>20%–40%</strong>, or uses a slow 35-day line instead of a 22-day direct service.</li>
 <li><strong>CIF insurance gaps</strong> — supplier buys the cheapest 110% cargo cover with high deductibles; you find out after a claim is denied.</li>
 <li><strong>FOB hidden local charges</strong> — THC (terminal handling), documentation fee, customs declaration, and EIR fee can add <strong>$100–$300</strong> per FCL beyond the FOB price. Demand an all-in FOB breakdown.</li>
</ul>
<p>Protection: always request an <strong>itemized quote</strong> and compare the freight line against independent rates from <a href="blog-sea-freight-china.html">2–3 forwarders</a>.</p>

<h2>How Yeatru Handles Incoterms</h2>
<p>Yeatru quotes transparently across incoterms so you can choose:</p>
<ul>
 <li><strong>FOB</strong> quotes include all China-side local charges (THC, docs, export declaration) — no surprises.</li>
 <li><strong>DDP</strong> quotes are all-in door-to-door with duty prepaid and tracked — ideal for <a href="blog-amazon-fba-sourcing-china.html">Amazon FBA</a> and first-time importers.</li>
 <li><strong>FCA</strong> for air and LCL — you control the freight line while we handle export clearance.</li>
 <li>We never push CIF — we'd rather show you the real freight rate and let you decide.</li>
</ul>

<h2>Frequently Asked Questions</h2>
<h3>1. What is the difference between EXW, FOB, CIF, and DDP?</h3>
<p><strong>EXW</strong>: buyer picks up at the factory and handles all logistics, export, import, and duty. <strong>FOB</strong>: seller delivers to the ship; buyer pays ocean freight, insurance, import, and duty. <strong>CIF</strong>: seller pays freight and insurance to the destination port; buyer clears import and pays duty. <strong>DDP</strong>: seller handles everything to the buyer's door, including import duty. Risk transfers at factory door (EXW), on board (FOB/CIF), or buyer's door (DDP).</p>
<h3>2. Which incoterm is best for beginners sourcing from China?</h3>
<p><strong>DDP</strong> (Delivered Duty Paid). The supplier or forwarder handles export clearance, freight, insurance, import duty, and last-mile to your door. You get one all-in price and zero customs admin. Once you have volume and a destination broker, switch to FOB to save 5%–15%.</p>
<h3>3. Why should I avoid CIF when sourcing from China?</h3>
<p>Under CIF the supplier selects the shipping line and pays freight, so they often use the slowest carrier (adding 5–10 transit days) and inflate freight by <strong>20%–40%</strong> as hidden margin. You lose control over the vessel and routing. FOB or DDP gives you a transparent freight line item — see <a href="blog-fob-vs-exw-vs-ddp.html">why</a>.</p>
<h3>4. Is EXW cheaper than FOB for large orders?</h3>
<p>Yes, EXW has the lowest unit price because the supplier does no logistics. But you must arrange China inland trucking (<strong>$80–$500</strong>), export clearance (<strong>$40–$150</strong>), freight, insurance, import clearance, and duty. Choose EXW only for large volume (FCL, $50k+) where you have brokers on both ends.</p>
<h3>5. What is the cost difference between EXW, FOB, CIF, and DDP?</h3>
<p>For a <strong>$5 EXW</strong> product: FOB ≈ <strong>$5.30</strong> (inland + export), CIF ≈ <strong>$5.80</strong> (+ freight + insurance to port), DDP ≈ <strong>$6.50</strong> (+ everything to door including duty). The DDP premium buys zero admin and risk transfer — worth it for small or first orders.</p>
<h3>6. Are FCA, CPT, and CIP relevant for China sourcing?</h3>
<p><strong>FCA</strong> (Free Carrier) is common for air freight and LCL — supplier delivers to a named carrier. <strong>CPT</strong> and <strong>CIP</strong> are the air/multimodal equivalents of CFR/CIF. For most China sea-FCL importers, FOB and DDP cover 90% of cases; FCA matters for air and LCL.</p>

<h2>Conclusion</h2>
<p>Incoterms determine your <strong>cost, risk, and admin</strong> when sourcing from China. Beginners should start with <strong>DDP</strong> (one price, door-to-door), move to <strong>FOB</strong> once they have a broker (saves 5%–15%), and only use <strong>EXW</strong> for large volume with brokers on both ends. Avoid <strong>CIF</strong> — suppliers game the freight. Always demand an <strong>itemized quote</strong> and compare the freight line against independent forwarder rates. <a href="contact.html">Get a side-by-side EXW/FOB/DDP quote</a> from Yeatru — we show every line item so you can choose the incoterm that fits your stage.</p>''',
})

# ============ 7. shipping-cost-calculator-china ============
BLOGS.append({
    "slug": "blog-shipping-cost-calculator-china",
    "old_desc": "How to calculate total landed cost: product + freight + duty + fees.",
    "new_desc": "Shipping cost calculator from China: air ($/kg, volumetric), sea LCL ($/CBM), FCL flat, express, rail formulas, THC, customs, DDP surcharge, and worked examples.",
    "subtitle": "Freight formulas by mode (air/sea LCL/FCL/express/rail), THC, customs, and DDP landed-cost math.",
    "headline": "Shipping Cost Calculator from China: Estimate Your Freight",
    "howto": [
        {"name": "Choose the shipping mode and its formula", "text": "Air: $/kg on chargeable weight = max(actual, volumetric LxWxH/6000). Sea LCL: $/CBM (min 1 CBM). Sea FCL: flat per container. Express: $/kg on LxWxH/5000. Rail: $/CBM. Pick the mode matching your weight, volume, and urgency."},
        {"name": "Calculate chargeable weight or CBM", "text": "For air/express, measure each carton's LxWxH in cm and compute volumetric weight; the carrier charges the greater of actual or volumetric. For sea, multiply carton count by per-carton CBM (LxWxH in m) and round up to 1 CBM minimum for LCL."},
        {"name": "Add China-side and port charges", "text": "Add inland trucking factory-to-port ($80-$500), THC (terminal handling: $30-$80/CBM sea or $0.20-$0.40/kg air), export customs clearance ($40-$150), and documentation fees. These are often bundled in DDP but itemized in FOB."},
        {"name": "Add destination charges and duty", "text": "Add import customs clearance ($50-$200), duty (0%-25% by HS code), VAT/GST (0%-20%), and last-mile delivery ($0.50-$3/unit). For DDP quotes these are already included; for FOB you pay them separately."},
        {"name": "Compare total landed cost, not freight only", "text": "Always compare the all-in landed cost per unit across modes, not just the freight rate. Sea LCL may be $80/CBM vs air $5.50/kg, but air's 6-day transit vs sea's 30-day can save working capital and stockouts."},
    ],
    "faq": [
        ("How do I calculate shipping cost from China?", "Determine the mode, then apply its formula: air = $/kg x chargeable weight (max of actual or LxWxH/6000); sea LCL = $/CBM x CBM (min 1 CBM); sea FCL = flat per container; express = $/kg x LxWxH/5000; rail = $/CBM x CBM. Add inland trucking ($80-$500), THC, customs clearance ($40-$150 export, $50-$200 import), duty, VAT, and last-mile."),
        ("What is the air freight chargeable weight formula?", "Chargeable weight = max(actual gross weight, volumetric weight), where volumetric weight = (L x W x H in cm) / 6000 for IATA standard air. A 60x50x40 cm box weighing 8 kg is charged at 20 kg. Express courier uses /5000 instead of /6000."),
        ("How is sea freight LCL cost calculated?", "Sea LCL is priced per CBM (cubic meter): CBM = (L x W x H in cm) / 1,000,000, or (L x W x H in m). The minimum chargeable CBM is 1.0 for most LCL routes. 2026 China→US LCL rates: $60-$120/CBM DDP, all-in. FCL is a flat rate per 20ft/40ft container regardless of CBM."),
        ("What is the difference between DDP and FOB shipping cost?", "FOB (Free On Board) price covers goods loaded onto the vessel at the China port; you pay freight, insurance, import duty, and delivery separately. DDP (Delivered Duty Paid) is all-in: freight, insurance, duty, and last-mile to your door. DDP is 5%-15% more expensive but removes admin and duty surprises."),
        ("How much does it cost to ship 500kg / 2 CBM from China to the US?", "Air: $5.50/kg x 500 kg chargeable = $2,750 (all-in DDP, 5-8 days). Sea LCL: $80/CBM x 2 CBM = $160 (all-in DDP, 25-35 days). Air is 17x more expensive but 5x faster. For high-value or urgent stock, air; for bulk low-value goods, sea."),
        ("Are there online shipping calculators for China freight?", "Yes: Freightos (air/sea instant quotes), Alibaba Logistics (1688/Alibaba integrated), and 17track (tracking). For accurate landed cost, always get 2-3 forwarder quotes — online calculators miss THC, duty, and peak-season surcharges. Yeatru provides all-in DDP quotes within 24 hours."),
    ],
    "body": r'''<aside class="article-takeaways">
 <h2>Key Takeaways</h2>
 <ul>
 <li>Air freight cost = <strong>$/kg × chargeable weight</strong>, where chargeable = max(actual, L×W×H÷6000). Express uses ÷5000.</li>
 <li>Sea LCL cost = <strong>$/CBM × CBM</strong> (min <strong>1 CBM</strong>). Sea FCL is a flat per-container rate.</li>
 <li>Add-ons: inland trucking <strong>$80–$500</strong>, THC <strong>$30–$80/CBM</strong> (sea) or <strong>$0.20–$0.40/kg</strong> (air), export clearance <strong>$40–$150</strong>, import clearance <strong>$50–$200</strong>.</li>
 <li><strong>500 kg / 2 CBM to US:</strong> air <strong>$2,750</strong> (6 days) vs sea LCL <strong>$160</strong> (30 days) — air is 17× costlier but 5× faster.</li>
 <li>Always compare <strong>total landed cost</strong> (freight + THC + duty + last-mile), not just the freight rate. Use <a href="blog-ddp-shipping-china.html">DDP</a> quotes for apples-to-apples.</li>
 </ul>
</aside>

<div class="geo-definition">
 <h2>What Goes Into a China Shipping Cost?</h2>
 <p>Shipping cost from China has three layers: (1) <strong>freight</strong> — the airline, ocean line, or courier rate; (2) <strong>origin &amp; destination charges</strong> — inland trucking, terminal handling (THC), customs clearance, and documentation; (3) <strong>duties &amp; taxes</strong> — import duty (0%–25%), VAT/GST (0%–20%). A quoted "$5/kg air" or "$80/CBM sea" rarely includes THC, duty, or last-mile — that's why a DDP all-in quote is the only number you should compare. Below are the formulas for each mode, with real 2026 rates.</p>
</div>

<h2>Shipping Cost Formulas by Mode</h2>
<div class="table-responsive"><table class="geo-comparison-table">
 <thead><tr><th>Mode</th><th>Formula</th><th>Unit</th><th>2026 China→US Rate</th></tr></thead>
 <tbody>
 <tr><td><a href="blog-air-freight-china.html"><strong>Air freight</strong></a></td><td>$/kg × max(actual, L×W×H÷6000)</td><td>$/kg</td><td>$4 – $9/kg</td></tr>
 <tr><td><a href="blog-sea-freight-china.html"><strong>Sea LCL</strong></a></td><td>$/CBM × CBM (min 1 CBM)</td><td>$/CBM</td><td>$60 – $120/CBM</td></tr>
 <tr><td><strong>Sea FCL</strong></td><td>Flat per 20ft / 40ft container</td><td>$/container</td><td>$1,200 – $3,500</td></tr>
 <tr><td><a href="blog-express-courier-china.html"><strong>Express (DHL/FedEx)</strong></a></td><td>$/kg × max(actual, L×W×H÷5000)</td><td>$/kg</td><td>$8 – $14/kg</td></tr>
 <tr><td><strong>Rail (China→EU)</strong></td><td>$/CBM × CBM</td><td>$/CBM</td><td>$90 – $160/CBM</td></tr>
 </tbody>
</table></div>

<h2>Air Freight: Chargeable Weight Worked Example</h2>
<p>Air carriers charge on <strong>chargeable weight</strong> — the greater of actual weight or volumetric weight. This is the #1 surprise for first-time shippers of bulky, light goods.</p>
<div class="geo-callout">
 <p><strong>Volumetric weight (air, IATA):</strong> (L × W × H in cm) ÷ 6000<br><strong>Volumetric weight (express):</strong> (L × W × H in cm) ÷ 5000</p>
</div>
<p><strong>Example:</strong> A carton of plush toys measures <strong>60 × 50 × 40 cm</strong> and weighs <strong>8 kg</strong>.</p>
<ul>
 <li>Volumetric weight (air) = (60 × 50 × 40) ÷ 6000 = <strong>20 kg</strong></li>
 <li>Actual weight = <strong>8 kg</strong></li>
 <li>Chargeable weight = max(20, 8) = <strong>20 kg</strong></li>
 <li>At $6/kg air to US → <strong>$120</strong> freight on an 8 kg box</li>
</ul>
<p>Express courier (÷5000) would charge 24 kg — even more. This is why bulky low-density goods should go <a href="blog-sea-freight-china.html">sea LCL</a>, not air.</p>

<h2>Sea LCL &amp; FCL: CBM and Container Rates</h2>
<p>Sea freight is priced by <strong>CBM (cubic meter)</strong> for LCL (less-than-container-load) and by <strong>container</strong> for FCL (full-container-load).</p>
<ul>
 <li><strong>CBM formula:</strong> (L × W × H in cm) ÷ 1,000,000, or L × W × H in meters.</li>
 <li><strong>LCL minimum:</strong> most routes charge a <strong>1 CBM minimum</strong> even if your cargo is 0.3 CBM.</li>
 <li><strong>FCL break-even:</strong> LCL becomes more expensive than FCL around <strong>15 CBM</strong> (20ft) or <strong>30 CBM</strong> (40ft). Above that, book a full container.</li>
 <li><strong>2026 FCL rates (China→US West Coast):</strong> 20ft <strong>$1,200–$2,000</strong>, 40ft <strong>$2,000–$3,500</strong> (all-in ocean + terminal, excludes duty).</li>
</ul>

<h2>Add-On Charges (Often Hidden in FOB Quotes)</h2>
<div class="table-responsive"><table class="geo-comparison-table">
 <thead><tr><th>Charge</th><th>Range</th><th>Notes</th></tr></thead>
 <tbody>
 <tr><td>China inland trucking (factory → port)</td><td>$80 – $500</td><td>Yiwu→Ningbo ~$120; Shenzhen→Yantian ~$80</td></tr>
 <tr><td>THC (terminal handling)</td><td>$30 – $80/CBM (sea); $0.20 – $0.40/kg (air)</td><td>Port/airport terminal fee</td></tr>
 <tr><td>Export customs clearance</td><td>$40 – $150</td><td>Brokers fee + declaration</td></tr>
 <tr><td>Documentation (BL, CO, FORM A/E)</td><td>$15 – $60</td><td>Per document</td></tr>
 <tr><td>Import customs clearance (destination)</td><td>$50 – $200</td><td>Broker fee</td></tr>
 <tr><td>Import duty</td><td>0% – 25% of value</td><td>By HS code; Section 301 for China</td></tr>
 <tr><td>VAT / GST</td><td>0% – 20%</td><td>By destination country</td></tr>
 <tr><td>Last-mile delivery</td><td>$0.50 – $3/unit</td><td>Port to warehouse / FBA</td></tr>
 </tbody>
</table></div>
<p><a href="blog-ddp-shipping-china.html">DDP quotes</a> bundle all of these into one rate; <strong>FOB quotes</strong> hide THC, docs, import clearance, and duty. Always convert FOB to landed cost before comparing.</p>

<h2>Worked Example: 500 kg / 2 CBM to the US</h2>
<p>Shipment of <strong>500 kg / 2 CBM</strong> of kitchenware from Ningbo to Los Angeles.</p>
<p><strong>Option A — Air freight (DDP):</strong></p>
<ul>
 <li>Chargeable weight = max(500 kg, 2 CBM equivalent). Air volumetric = 2,000,000 cm³ ÷ 6000 = 333 kg → chargeable = <strong>500 kg</strong></li>
 <li>Air DDP: $5.50/kg × 500 = <strong>$2,750</strong> (all-in, duty included)</li>
 <li>Transit: <strong>5–8 days</strong> door-to-door</li>
</ul>
<p><strong>Option B — Sea LCL (DDP):</strong></p>
<ul>
 <li>CBM = 2.0 (above 1 CBM min)</li>
 <li>Sea LCL DDP: $80/CBM × 2 = <strong>$160</strong> (all-in, duty included)</li>
 <li>Transit: <strong>25–35 days</strong> door-to-door</li>
</ul>
<p>Air is <strong>17× more expensive</strong> but <strong>5× faster</strong>. For a $10/unit product with 30-day sea lead time, the $2,590 premium buys 25 days of working capital and avoids a stockout — worth it for trending or high-margin goods.</p>

<h2>Online Freight Calculators vs Real Quotes</h2>
<ul>
 <li><strong>Freightos</strong> — instant air/sea quotes from a forwarder marketplace; good for ballpark but misses THC and duty.</li>
 <li><strong>Alibaba Logistics</strong> — integrated with 1688/Alibaba orders; convenient for small parcels.</li>
 <li><strong>17track</strong> — tracking only, not a quote tool.</li>
 <li><strong>Limitation:</strong> none of these include <strong>Section 301 duty</strong>, peak-season surcharges, or DG fees. Always get <strong>2–3 forwarder all-in DDP quotes</strong> before booking.</li>
</ul>

<h2>How Yeatru Quotes Shipping Cost</h2>
<p>Yeatru provides <strong>all-in DDP quotes</strong> within 24 hours:</p>
<ul>
 <li>Compare <a href="blog-air-freight-china.html">air</a>, <a href="blog-sea-freight-china.html">sea LCL/FCL</a>, <a href="blog-express-courier-china.html">express</a>, and rail side-by-side.</li>
 <li>Include THC, export/import clearance, duty, VAT, and last-mile — no hidden lines.</li>
 <li>Chargeable-weight and CBM calculation with your actual carton dimensions.</li>
 <li>Peak-season (Sep–Dec) surcharge transparency — we quote before rates spike.</li>
</ul>

<h2>Frequently Asked Questions</h2>
<h3>1. How do I calculate shipping cost from China?</h3>
<p>Pick the mode and apply its formula: air = <strong>$/kg × chargeable weight</strong> (max of actual or L×W×H÷6000); sea LCL = <strong>$/CBM × CBM</strong> (min 1 CBM); sea FCL = flat per container; express = $/kg × L×W×H÷5000; rail = $/CBM × CBM. Add inland trucking (<strong>$80–$500</strong>), THC, customs (<strong>$40–$150</strong> export, <strong>$50–$200</strong> import), duty, VAT, and last-mile.</p>
<h3>2. What is the air freight chargeable weight formula?</h3>
<p>Chargeable weight = max(actual gross weight, volumetric weight), where volumetric weight = (L × W × H in cm) ÷ 6000 for IATA air. A 60×50×40 cm box weighing 8 kg is charged at <strong>20 kg</strong>. Express courier uses ÷5000 (24 kg). Always ask for both numbers before booking.</p>
<h3>3. How is sea freight LCL cost calculated?</h3>
<p>Sea LCL = <strong>$/CBM × CBM</strong>, where CBM = (L × W × H in cm) ÷ 1,000,000. The minimum chargeable CBM is <strong>1.0</strong>. 2026 China→US LCL DDP rates: <strong>$60–$120/CBM</strong>. FCL is a flat per-container rate ($1,200–$3,500) regardless of CBM; switch from LCL to FCL around <strong>15 CBM</strong>.</p>
<h3>4. What is the difference between DDP and FOB shipping cost?</h3>
<p><strong>FOB</strong> covers goods loaded onto the China vessel; you pay freight, insurance, import duty, and delivery separately. <strong>DDP</strong> is all-in: freight, insurance, duty, and last-mile to your door. DDP costs <strong>5%–15%</strong> more but removes admin and duty surprises — always compare landed cost, not just freight.</p>
<h3>5. How much does it cost to ship 500 kg / 2 CBM from China to the US?</h3>
<p>Air: <strong>$5.50/kg × 500 = $2,750</strong> (DDP, 5–8 days). Sea LCL: <strong>$80/CBM × 2 = $160</strong> (DDP, 25–35 days). Air is 17× more expensive but 5× faster. Use air for high-value, urgent, or trending stock; sea for bulk low-value goods.</p>
<h3>6. Are there online shipping calculators for China freight?</h3>
<p>Yes — Freightos (air/sea instant quotes), Alibaba Logistics, and 17track (tracking). But none include <strong>Section 301 duty</strong>, THC, or peak surcharges. Always get <strong>2–3 all-in DDP forwarder quotes</strong> before booking. <a href="contact.html">Yeatru quotes DDP</a> within 24 hours with every line item shown.</p>

<h2>Conclusion</h2>
<p>Calculating China shipping cost comes down to the right formula per mode (air chargeable weight, sea CBM, FCL flat) plus the often-hidden add-ons: <strong>THC, customs clearance, duty, and last-mile</strong>. The cheapest-looking rate is rarely the cheapest landed cost — convert FOB to DDP-equivalent before deciding. For 500 kg/2 CBM, sea LCL at $160 beats air's $2,750 unless the 25-day time savings is worth the premium. <a href="contact.html">Send Yeatru your carton dimensions and weight</a> — we'll calculate air, sea, express, and rail all-in DDP costs side-by-side within 24 hours.</p>''',
})

# ============ 8. china-sourcing-time-calculator ============
BLOGS.append({
    "slug": "blog-china-sourcing-time-calculator",
    "old_desc": "How long sourcing takes: sample, production, QC, shipping.",
    "new_desc": "China sourcing timeline calculator: RFQ, samples, mold/OEM tooling, production, QC, shipping (air/sea/express), clearance, total 25-120 days by product type, peak season delays.",
    "subtitle": "Stage-by-stage sourcing timeline with rush options and peak-season delay buffers.",
    "headline": "China Sourcing Timeline: How Long Does It Take? (Calculator)",
    "howto": [
        {"name": "Map your product type to a baseline timeline", "text": "Stock products: 25-50 days sea or 5-15 days air. Private-label: 35-70 days sea. OEM/custom with new mold: 60-120 days. Start from this baseline and add peak-season buffers if sourcing Sep-Dec."},
        {"name": "Break the timeline into the 10 sourcing stages", "text": "RFQ & samples (3-10 days), negotiation & contract (2-5 days), mold/OEM tooling (15-45 days, 0 if stock), production (15-60 days), QC (1-3 days), inland to port (1-2 days), export clearance (1-2 days), shipping (air 3-7 / sea 25-40 / express 2-5), import clearance (1-3 days), last-mile (1-3 days)."},
        {"name": "Apply rush options where it matters most", "text": "Cut RFQ time with a sourcing agent (1-3 days instead of 7-10). Cut shipping with air (3-7 days) instead of sea (25-40). Cut production with overtime (10%-20% cost premium) for 20%-30% time savings. Mold tooling rarely rushes below 15 days."},
        {"name": "Add peak-season and holiday buffers", "text": "Sep-Dec peak season adds 5-15 days to production and shipping. Chinese New Year (Jan/Feb) closes most factories for 2-4 weeks. National Day (Oct 1) and Labor Day (May 1) add 3-7 days. Always pad your timeline around these."},
        {"name": "Track milestones and reorder early", "text": "Track: deposit paid, production start, QC passed, cargo-ready, vessel ETD, ETA, clearance, delivery. Place your reorder PO 45+ days before stockout for sea, 10+ days for air. Stockouts cost more than the freight savings."},
    ],
    "faq": [
        ("How long does sourcing from China take total?", "Stock product: 25-50 days by sea (or 5-15 days by air). Private-label: 35-70 days by sea. OEM/custom with new mold: 60-120 days. Peak season (Sep-Dec) adds 5-15 days. These are door-to-door timelines including RFQ, production, QC, shipping, and clearance."),
        ("What is the typical production lead time in China?", "For off-the-shelf Yiwu/Shenzhen stock goods: 7-15 days. For private-label (custom logo/packaging): 15-30 days. For OEM with new mold/tooling: 30-60 days. Large orders (10k+ units) can extend to 60-90 days. Rush production with overtime cuts 20%-30% of time at a 10%-20% cost premium."),
        ("How long does an OEM product take from idea to delivery?", "OEM timeline: RFQ & samples 3-10 days + mold/tooling 15-45 days + sample approval 3-7 days + production 30-60 days + QC 1-3 days + sea shipping 25-40 days + clearance 2-4 days = 79-169 days. Typical OEM sea delivery: 90-120 days. By air, subtract ~25 days."),
        ("How do peak seasons affect China sourcing timelines?", "Sep-Dec (Christmas/Black Friday) is peak: factory capacity is full, production adds 5-10 days, and ocean freight adds 5-15 days (port congestion, vessel space shortage). Chinese New Year (Jan/Feb) closes factories for 2-4 weeks — place orders 60+ days before CNY. National Day (Oct 1) adds 3-7 days."),
        ("What is the fastest way to source from China?", "Fastest path: stock product (no mold) + air freight. RFQ/samples 3-7 days + production 7-15 days + QC 1 day + air 3-7 days + clearance 1-2 days = 15-32 days total. A sourcing agent can cut RFQ to 1-3 days. Express courier for samples takes 2-5 days door-to-door."),
        ("Can I rush an order from China?", "Yes, with trade-offs: (1) Air freight instead of sea saves 20-30 days but costs 5-15x more. (2) Overtime production cuts 20%-30% of lead time at 10%-20% cost premium. (3) Using existing molds instead of new tooling saves 15-45 days. (4) A sourcing agent consolidates RFQ and QC to save 3-7 days. Mold tooling cannot be rushed below ~15 days."),
    ],
    "body": r'''<aside class="article-takeaways">
 <h2>Key Takeaways</h2>
 <ul>
 <li><strong>Stock product</strong> by sea: <strong>25–50 days</strong>; by air: <strong>5–15 days</strong>. <strong>OEM/custom</strong> with new mold: <strong>60–120 days</strong>.</li>
 <li>Stages: RFQ/samples <strong>3–10</strong> days, negotiation <strong>2–5</strong>, mold <strong>15–45</strong> (0 if stock), production <strong>15–60</strong>, QC <strong>1–3</strong>, inland <strong>1–2</strong>, export clearance <strong>1–2</strong>, shipping (air <strong>3–7</strong> / sea <strong>25–40</strong>), import clearance <strong>1–3</strong>, last-mile <strong>1–3</strong>.</li>
 <li>Peak season (Sep–Dec) adds <strong>5–15 days</strong>; Chinese New Year closes factories <strong>2–4 weeks</strong>.</li>
 <li>Rush options: air freight (saves 20–30 days, 5–15× cost), overtime production (saves 20–30%, +10–20% cost), skip new mold (saves 15–45 days).</li>
 <li>Reorder <strong>45+ days</strong> before stockout (sea) or <strong>10+ days</strong> (air) — stockouts cost more than freight savings.</li>
 </ul>
</aside>

<div class="geo-definition">
 <h2>What Is the China Sourcing Timeline?</h2>
 <p>The China sourcing timeline is the total calendar time from your first <strong>RFQ</strong> to goods arriving at your warehouse or Amazon FBA. It breaks into 10 stages: RFQ &amp; samples, negotiation &amp; contract, mold/OEM tooling, production, QC inspection, inland trucking, export clearance, international shipping, import clearance, and last-mile delivery. The two biggest variables are <strong>mold/tooling</strong> (15–45 days for OEM, zero for stock) and <strong>shipping mode</strong> (3–7 days air vs 25–40 days sea). Miss a holiday or peak-season window and you can add 2–6 weeks to any timeline.</p>
</div>

<h2>Sourcing Timeline by Stage (2026)</h2>
<div class="table-responsive"><table class="geo-comparison-table">
 <thead><tr><th>Stage</th><th>Days</th><th>Can Rush?</th><th>Notes</th></tr></thead>
 <tbody>
 <tr><td>RFQ &amp; samples</td><td>3 – 10</td><td>Yes (agent: 1–3)</td><td>Sample shipping 2–5 days express</td></tr>
 <tr><td>Negotiation &amp; contract</td><td>2 – 5</td><td>Yes</td><td>PI + contract signing</td></tr>
 <tr><td>Mold / OEM tooling</td><td>15 – 45</td><td>Limited (min 15)</td><td>0 days for stock products</td></tr>
 <tr><td>Production</td><td>15 – 60</td><td>Yes (overtime +10–20% cost)</td><td>Depends on quantity</td></tr>
 <tr><td>QC inspection</td><td>1 – 3</td><td>Yes</td><td>AQL 2.5 pre-shipment</td></tr>
 <tr><td>Inland to port</td><td>1 – 2</td><td>Yes</td><td>Factory → Ningbo/Shenzhen</td></tr>
 <tr><td>Export clearance</td><td>1 – 2</td><td>Yes</td><td>China customs declaration</td></tr>
 <tr><td>Shipping (air / sea / express)</td><td>3–7 / 25–40 / 2–5</td><td>Air = fastest</td><td>See <a href="blog-air-freight-china.html">air</a> / <a href="blog-sea-freight-china.html">sea</a></td></tr>
 <tr><td>Import clearance</td><td>1 – 3</td><td>Yes</td><td>Duty + VAT payment</td></tr>
 <tr><td>Last-mile delivery</td><td>1 – 3</td><td>Yes</td><td>Port → warehouse / FBA</td></tr>
 </tbody>
</table></div>

<h2>Total Timeline by Product Type</h2>
<div class="table-responsive"><table class="geo-comparison-table">
 <thead><tr><th>Product Type</th><th>Sea (door-to-door)</th><th>Air (door-to-door)</th></tr></thead>
 <tbody>
 <tr><td><strong>Stock / off-the-shelf</strong></td><td>25 – 50 days</td><td>5 – 15 days</td></tr>
 <tr><td><strong>Private-label</strong> (logo + packaging)</td><td>35 – 70 days</td><td>15 – 30 days</td></tr>
 <tr><td><strong>OEM / custom mold</strong></td><td>60 – 120 days</td><td>40 – 90 days</td></tr>
 </tbody>
</table></div>
<p>These ranges include all 10 stages. Add <strong>5–15 days</strong> for Sep–Dec peak season and <strong>2–4 weeks</strong> if production crosses Chinese New Year.</p>

<h2>Worked Example: OEM Product — 90 Days Total</h2>
<p>A US brand develops a custom silicone pet bowl (new injection mold) from a Shenzhen factory, shipped by sea to LA.</p>
<ul>
 <li>RFQ &amp; samples (existing material samples): <strong>7 days</strong></li>
 <li>Negotiation &amp; contract: <strong>3 days</strong></li>
 <li>Mold tooling (new cavity, 1 cavity): <strong>30 days</strong> + $1,800 mold cost</li>
 <li>Pre-production sample approval: <strong>5 days</strong></li>
 <li>Mass production (5,000 units): <strong>30 days</strong></li>
 <li>AQL 2.5 QC + rework: <strong>3 days</strong></li>
 <li>Inland to Yantian + export clearance: <strong>2 days</strong></li>
 <li>Sea freight Yantian → LA: <strong>30 days</strong></li>
 <li>Import clearance + last-mile: <strong>3 days</strong></li>
 <li><strong>Total: ~113 days</strong> (within the 60–120 day OEM range)</li>
</ul>
<p>Switching to <strong>air freight</strong> would cut 23 days (→ ~90 days total) but add ~$4,000 in freight. See <a href="blog-mold-cost-china.html">mold cost</a> details for OEM projects.</p>

<h2>Peak Season &amp; Holiday Delays</h2>
<ul>
 <li><strong>Sep–Dec (peak)</strong> — factory capacity full, production +5–10 days, ocean freight +5–15 days (port congestion, vessel space shortage). Book space 10+ days ahead.</li>
 <li><strong>Chinese New Year (Jan/Feb)</strong> — most factories close <strong>2–4 weeks</strong>. Place orders <strong>60+ days before CNY</strong>; cargo-ready 2 weeks before the holiday.</li>
 <li><strong>National Day (Oct 1)</strong> — 7-day holiday; add <strong>3–7 days</strong>.</li>
 <li><strong>Labor Day (May 1)</strong> — 5-day holiday; add <strong>3–5 days</strong>.</li>
 <li><strong>Western peak (Nov–Dec)</strong> — Amazon FBA and retail restocks flood US ports; import clearance adds 2–5 days.</li>
</ul>

<h2>Rush Options (and Their Cost)</h2>
<ul>
 <li><strong>Air freight instead of sea</strong> — saves <strong>20–30 days</strong>, costs <strong>5–15× more</strong>. Best for urgent restocks under 500 kg.</li>
 <li><strong>Overtime production</strong> — saves <strong>20%–30%</strong> of production time, costs <strong>10%–20%</strong> more. Negotiable for orders under 10k units.</li>
 <li><strong>Existing mold / stock product</strong> — saves <strong>15–45 days</strong> (no tooling). If you can adapt a stock SKU with a logo, you skip the mold stage entirely.</li>
 <li><strong>Sourcing agent for RFQ</strong> — cuts RFQ from <strong>7–10 days to 1–3 days</strong> and handles QC in 1 day. Net saving: <strong>3–7 days</strong>.</li>
 <li><strong>Express courier for samples</strong> — 2–5 days door-to-door vs 7–10 days for air parcel.</li>
</ul>
<p>What you <strong>cannot</strong> rush: mold tooling below ~15 days, sea transit below ~20 days, or customs clearance beyond the broker's SLA.</p>

<h2>How Yeatru Compresses the Timeline</h2>
<p>Yeatru shortens sourcing timelines at every stage:</p>
<ul>
 <li>RFQ in <strong>24–48 hours</strong> from 3 verified factories (vs 7–10 days solo).</li>
 <li>Sample consolidation in our Yiwu/Shenzhen warehouse — one express shipment instead of 3.</li>
 <li>QC inspection scheduled <strong>same-day</strong> as cargo-ready; report in 24 hours.</li>
 <li>Direct booking with <a href="blog-air-freight-china.html">airlines</a> and <a href="blog-sea-freight-china.html">ocean lines</a> — no middleman delays.</li>
 <li>Peak-season space booked <strong>30+ days ahead</strong> to avoid roll-overs.</li>
</ul>

<h2>Frequently Asked Questions</h2>
<h3>1. How long does sourcing from China take total?</h3>
<p><strong>Stock product</strong>: <strong>25–50 days</strong> by sea or <strong>5–15 days</strong> by air. <strong>Private-label</strong>: 35–70 days by sea. <strong>OEM/custom with new mold</strong>: 60–120 days. Peak season (Sep–Dec) adds 5–15 days. These are door-to-door including RFQ, production, QC, shipping, and clearance.</p>
<h3>2. What is the typical production lead time in China?</h3>
<p>Off-the-shelf Yiwu/Shenzhen stock goods: <strong>7–15 days</strong>. Private-label (custom logo/packaging): <strong>15–30 days</strong>. OEM with new mold: <strong>30–60 days</strong>. Large orders (10k+ units): 60–90 days. Rush overtime production cuts 20%–30% of time at a 10%–20% cost premium.</p>
<h3>3. How long does an OEM product take from idea to delivery?</h3>
<p>OEM timeline: RFQ &amp; samples 3–10 + mold/tooling 15–45 + sample approval 3–7 + production 30–60 + QC 1–3 + sea shipping 25–40 + clearance 2–4 = <strong>79–169 days</strong>. Typical OEM sea delivery: <strong>90–120 days</strong>. By air, subtract ~25 days.</p>
<h3>4. How do peak seasons affect China sourcing timelines?</h3>
<p>Sep–Dec peak: factory capacity full, production +5–10 days, ocean freight +5–15 days (port congestion). <strong>Chinese New Year</strong> (Jan/Feb) closes factories 2–4 weeks — order 60+ days before CNY. National Day (Oct 1) adds 3–7 days; Labor Day (May 1) adds 3–5 days.</p>
<h3>5. What is the fastest way to source from China?</h3>
<p>Fastest: stock product (no mold) + air freight. RFQ/samples 3–7 + production 7–15 + QC 1 + air 3–7 + clearance 1–2 = <strong>15–32 days</strong>. A sourcing agent cuts RFQ to 1–3 days. Express courier for samples: 2–5 days door-to-door.</p>
<h3>6. Can I rush an order from China?</h3>
<p>Yes, with trade-offs: (1) <strong>air freight</strong> saves 20–30 days, costs 5–15× more; (2) <strong>overtime production</strong> saves 20%–30% at +10–20% cost; (3) <strong>existing mold</strong> saves 15–45 days; (4) a <strong>sourcing agent</strong> saves 3–7 days on RFQ/QC. Mold tooling cannot be rushed below ~15 days.</p>

<h2>Conclusion</h2>
<p>A China sourcing timeline is the sum of 10 stages — and the two biggest levers are <strong>mold/tooling</strong> (skip it for stock, save 15–45 days) and <strong>shipping mode</strong> (air saves 20–30 days at 5–15× cost). Stock products arrive in <strong>25–50 days</strong> by sea; OEM takes <strong>60–120 days</strong>. Always pad for <strong>Sep–Dec peak</strong> and <strong>Chinese New Year</strong>, and reorder <strong>45+ days</strong> before stockout. <a href="contact.html">Send Yeatru your product and target date</a> — we'll build a stage-by-stage timeline with rush options and a realistic delivery date.</p>''',
})


if __name__ == "__main__":
    for cfg in BLOGS:
        process(cfg)
    print(f"\nDone. Rewrote {len(BLOGS)} blogs.")



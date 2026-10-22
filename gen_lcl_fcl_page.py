#!/usr/bin/env python3
"""Generate /lcl-vs-fcl-china-import.html by reusing the site's existing
head/nav/footer shell (from logistics-shipping.html) so styling stays native.
Content targets the confirmed Bing Copilot citation query:
  "LCL vs FCL import China Slovakia"
"""
import json, re

SRC = "logistics-shipping.html"
OUT = "lcl-vs-fcl-china-import.html"
SITE = "https://www.yeatru.com"
URL = f"{SITE}/{OUT}"

src = open(SRC, encoding="utf-8").read()

# ── shell extraction (marker based, robust to line drift) ──────────
head_end = src.index("</head>")
body_start = src.index("<body>")
nav_end = src.index("</nav>", body_start) + len("</nav>")
footer_start = src.index('<footer class="footer">')

HEAD = src[:head_end]                      # doctype .. last head tag
NAV = src[body_start:nav_end]              # <body> + navbar
TAIL = src[footer_start:]                  # footer, modals, scripts

# ── head replacements ──────────────────────────────────────────────
TITLE = "LCL vs FCL: Which China Container Shipping Option to Choose? | Yeatru"
DESC = ("LCL vs FCL compared for China imports: cost per CBM, transit time, minimum volume, "
        "break-even around 15 CBM, damage risk and customs. Includes China-to-Slovakia and "
        "Eastern Europe routing with indicative 2026 freight rates.")
KW = ("LCL vs FCL, LCL vs FCL import China Slovakia, less than container load, full container load, "
      "sea freight China Europe, container shipping comparison, CBM break-even, China to Slovakia shipping")

HEAD = re.sub(r"<title>.*?</title>", f"<title>{TITLE}</title>", HEAD, flags=re.S)
HEAD = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{DESC}">', HEAD)
HEAD = re.sub(r'<meta name="keywords" content="[^"]*">', f'<meta name="keywords" content="{KW}">', HEAD)
HEAD = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{URL}">', HEAD)
HEAD = HEAD.replace(f'<link rel="alternate" hreflang="en" href="{SITE}/logistics-shipping.html">',
                    f'<link rel="alternate" hreflang="en" href="{URL}">')
HEAD = HEAD.replace(f'<link rel="alternate" hreflang="x-default" href="{SITE}/logistics-shipping.html">',
                    f'<link rel="alternate" hreflang="x-default" href="{URL}">')
HEAD = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{TITLE}">', HEAD)
HEAD = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{DESC}">', HEAD)
HEAD = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{URL}">', HEAD)
HEAD = re.sub(r'<meta name="twitter:title" content="[^"]*">', f'<meta name="twitter:title" content="{TITLE}">', HEAD)
HEAD = re.sub(r'<meta name="twitter:description" content="[^"]*">', f'<meta name="twitter:description" content="{DESC}">', HEAD)
HEAD = re.sub(r'<meta name="twitter:url" content="[^"]*">', f'<meta name="twitter:url" content="{URL}">', HEAD)

# strip every inherited JSON-LD block from the head (we inject our own below)
HEAD = re.sub(r'\s*<script type="application/ld\+json">.*?</script>', "", HEAD, flags=re.S)

# ── structured data ────────────────────────────────────────────────
FAQ = [
    ("LCL or FCL: which is cheaper for a 5 CBM shipment from China?",
     "LCL is cheaper for a 5 CBM shipment: you pay only for the space you use, typically USD 55-85 per CBM to a European base port, so about USD 275-425 plus destination charges. A 20ft FCL container costs USD 1,200-2,200 regardless of how full it is, which is 3-6 times more for the same volume."),
    ("At what volume does FCL become cheaper than LCL?",
     "FCL becomes cheaper than LCL at roughly 13-15 CBM for a 20ft container and around 25-30 CBM for a 40ft high-cube. The break-even point depends on the lane, destination charges and current rates, because LCL adds per-CBM destination handling fees that FCL does not."),
    ("How long does LCL shipping from China to Slovakia take?",
     "LCL from China to Slovakia takes 40-55 days door-to-door when routed through Hamburg or Rotterdam and then by rail or truck to Bratislava. Routing through the Adriatic port of Koper with onward haulage takes 32-45 days and is often faster for Slovakia, Austria and Hungary."),
    ("How long does FCL shipping from China to Slovakia take?",
     "FCL from Ningbo or Shenzhen to Slovakia takes 35-45 days door-to-door via Koper, or 40-55 days via Hamburg or Rotterdam. FCL is 5-10 days faster than LCL on the same lane because it skips the consolidation and deconsolidation steps."),
    ("Is LCL safe for fragile or high-value goods?",
     "LCL is less suitable for fragile or high-value goods because your cargo is handled multiple times during consolidation and deconsolidation. FCL is safer: the container is sealed at the factory and opened at destination, reducing handling damage risk significantly."),
    ("What is the minimum shipment size for LCL?",
     "LCL accepts shipments from 0.5 CBM or about 100 kg, though freight forwarders usually apply a minimum charge of 1 CBM. Below 0.5 CBM, express courier is usually cheaper than LCL once destination charges are included."),
    ("What documents are needed for LCL and FCL imports into the EU?",
     "Both LCL and FCL imports into the EU require a commercial invoice, packing list, bill of lading, EU customs declaration and an EORI number. Goods also need CE marking, REACH compliance or other category certificates where applicable, and import VAT is payable on the customs value plus freight."),
    ("How much is import VAT and duty for China goods entering Slovakia?",
     "Slovakia applies the standard VAT rate of 23% on the customs value plus freight and insurance, and duty depends on the product HS code, typically 0-12%. Under DDP terms the freight forwarder pays both at import and invoices you in the all-in freight rate."),
    ("Can LCL and FCL shipments be combined with sourcing from multiple suppliers?",
     "Yes. Yeatru consolidates goods from multiple Chinese suppliers in its Yiwu warehouse, then either books LCL space for the combined volume or loads a single FCL container. Consolidating first typically saves 20-40% versus shipping each supplier separately."),
    ("Does LCL or FCL apply to Amazon FBA shipments to Europe?",
     "Amazon FBA shipments to Europe are usually sent as FCL when above 15 CBM, or as LCL for smaller replenishments. Both require FNSKU labelling and FBA-compliant cartons, and FCL is preferred for full pallet shipments because it avoids mixed-cargo handling at the destination warehouse."),
    ("What is the difference between LCL and FCL in simple terms?",
     "LCL (Less than Container Load) means your cargo shares a container with other importers and you pay per CBM. FCL (Full Container Load) means you book an entire 20ft, 40ft or 40ft high-cube container and pay a flat rate regardless of volume."),
    ("Which is better for a first-time importer from China?",
     "For a first order under 10 CBM, LCL is usually the better choice because it limits freight spend and cash tied up in slow-moving stock. Once a product proves it sells, moving to FCL at 15 CBM or more typically cuts the landed cost per unit by 15-30%."),
]

NODES = [
    {
        "@type": "WebPage",
        "@id": URL,
        "url": URL,
        "name": "LCL vs FCL: Which China Container Shipping Option to Choose?",
        "description": DESC,
        "inLanguage": "en",
        "isPartOf": {"@id": f"{SITE}/#website"},
        "about": {"@type": "Thing", "name": "LCL and FCL container shipping from China"},
        "datePublished": "2026-10-22",
        "dateModified": "2026-10-22",
        "breadcrumb": {"@id": f"{URL}#breadcrumb"},
        "primaryImageOfPage": {
            "@type": "ImageObject",
            "url": "https://cdn.jsdelivr.net/gh/Yeatru/Image@main/Images/global-logistics.jpg",
        },
    },
    {
        "@type": "BreadcrumbList",
        "@id": f"{URL}#breadcrumb",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "Logistics & Shipping", "item": f"{SITE}/logistics-shipping.html"},
            {"@type": "ListItem", "position": 3, "name": "LCL vs FCL", "item": URL},
        ],
    },
    {
        "@type": "Service",
        "@id": f"{URL}#service",
        "name": "China Container Shipping — LCL and FCL",
        "serviceType": "OceanFreight",
        "description": "LCL and FCL ocean freight from China to Europe, North America and the Middle East, including consolidation in Yiwu, customs clearance and DDP door-to-door delivery.",
        "provider": {"@type": "Organization", "name": "Yeatru Sourcing", "url": SITE},
        "areaServed": [
            {"@type": "Country", "name": "Slovakia"},
            {"@type": "Country", "name": "Germany"},
            {"@type": "Country", "name": "Poland"},
            {"@type": "Country", "name": "Czechia"},
            {"@type": "Country", "name": "Hungary"},
            {"@type": "Country", "name": "Austria"},
            {"@type": "Country", "name": "United States"},
            {"@type": "Country", "name": "United Kingdom"},
        ],
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Container shipping options",
            "itemListElement": [
                {
                    "@type": "Offer",
                    "name": "LCL — Less than Container Load",
                    "priceCurrency": "USD",
                    "priceSpecification": {"@type": "UnitPriceSpecification", "price": 55, "minPrice": 55, "maxPrice": 85, "unitText": "CBM", "priceCurrency": "USD"},
                    "itemOffered": {"@type": "Service", "name": "LCL ocean freight from China", "serviceType": "LCL"},
                },
                {
                    "@type": "Offer",
                    "name": "FCL 20ft — Full Container Load",
                    "priceCurrency": "USD",
                    "priceSpecification": {"@type": "PriceSpecification", "minPrice": 1200, "maxPrice": 2200, "priceCurrency": "USD"},
                    "itemOffered": {"@type": "Service", "name": "20ft FCL ocean freight from China", "serviceType": "FCL20"},
                },
                {
                    "@type": "Offer",
                    "name": "FCL 40ft High Cube — Full Container Load",
                    "priceCurrency": "USD",
                    "priceSpecification": {"@type": "PriceSpecification", "minPrice": 1900, "maxPrice": 3400, "priceCurrency": "USD"},
                    "itemOffered": {"@type": "Service", "name": "40ft HQ FCL ocean freight from China", "serviceType": "FCL40HQ"},
                },
            ],
        },
    },
    {
        "@type": "HowTo",
        "@id": f"{URL}#howto",
        "name": "How to choose between LCL and FCL for a China import",
        "description": "A five-step method to decide whether to ship LCL or FCL based on volume, cargo value, timing and destination.",
        "totalTime": "PT15M",
        "step": [
            {"@type": "HowToStep", "position": 1, "name": "Measure the shipment volume", "text": "Calculate total CBM by multiplying carton length, width and height and summing all cartons. Also record gross weight, because heavy cargo can hit weight limits before volume limits."},
            {"@type": "HowToStep", "position": 2, "name": "Apply the 15 CBM rule of thumb", "text": "Below 13-15 CBM, LCL is usually cheaper. Above 15 CBM, compare the LCL per-CBM total including destination charges against the flat FCL rate; FCL normally wins from 15 CBM upward."},
            {"@type": "HowToStep", "position": 3, "name": "Check cargo fragility and value", "text": "Choose FCL for fragile, high-value or theft-prone goods because the container stays sealed from factory to destination, eliminating consolidation handling."},
            {"@type": "HowToStep", "position": 4, "name": "Compare door-to-door transit time", "text": "FCL is typically 5-10 days faster than LCL on the same lane. If the goods are seasonal or must hit a launch date, add that buffer to the LCL plan."},
            {"@type": "HowToStep", "position": 5, "name": "Request both quotes and compare landed cost", "text": "Ask the forwarder for LCL and FCL quotes including origin charges, ocean freight, destination charges, duty and VAT. Compare total landed cost per unit rather than freight cost alone."},
        ],
    },
    {
        "@type": "FAQPage",
        "@id": f"{URL}#faq",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in FAQ
        ],
    },
]

JSONLD = "".join(
    '\n <script type="application/ld+json">\n '
    + json.dumps({"@context": "https://schema.org", "@graph": NODES}, ensure_ascii=False, indent=1)
    + "\n </script>"
)

# ── comparison table rows ──────────────────────────────────────────
ROWS = [
    ("Cost basis", "Per CBM (min. 1 CBM charge)", "Flat rate per container", "Per kg (chargeable weight)", "Per kg, all-in"),
    ("Indicative rate (H2 2026)", "USD 55-85 / CBM", "USD 1,200-2,200 (20ft)<br>USD 1,900-3,400 (40HQ)", "USD 4.5-7.5 / kg", "USD 6-12 / kg"),
    ("Minimum shipment", "0.5 CBM / ~100 kg", "1 container", "45 kg", "0.5 kg"),
    ("Break-even vs LCL", "—", "~13-15 CBM (20ft)<br>~25-30 CBM (40HQ)", "Rarely", "Rarely"),
    ("Transit, China → Slovakia", "40-55 days", "35-45 days (via Koper)", "8-14 days", "3-7 days"),
    ("Handling / damage risk", "Higher — consolidated cargo", "Low — sealed container", "Moderate", "Moderate"),
    ("Customs", "Deconsolidated, per-house-BL", "Single declaration per container", "Air waybill", "Express clearance"),
    ("Best for", "Trial orders, 1-13 CBM", "15+ CBM, fragile or high-value", "Urgent, 100-500 kg", "Samples, under 50 kg"),
]


def table_html():
    head = "".join(f"<th scope=\"col\">{h}</th>" for h in
                   ["Criterion", "LCL", "FCL", "Air Freight", "Express Courier"])
    body = ""
    for r in ROWS:
        body += "<tr>" + "".join(
            f'<th scope="row">{c}</th>' if i == 0 else f"<td>{c}</td>"
            for i, c in enumerate(r)
        ) + "</tr>"
    return f'<div class="table-responsive"><table class="table table-bordered align-middle cmp-table"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


faq_html = "".join(
    f'''  <details class="faq-item">
   <summary><i class="fas fa-chevron-right me-2"></i>{q}</summary>
   <div class="faq-answer"><p>{a}</p></div>
  </details>
'''
    for q, a in FAQ
)

MAIN = f'''
<main>

<section class="section-hero">
 <div class="container">
  <nav aria-label="breadcrumb" class="mb-4">
   <ol class="breadcrumb">
    <li class="breadcrumb-item"><a href="index.html">Home</a></li>
    <li class="breadcrumb-item"><a href="logistics-shipping.html">Logistics &amp; Shipping</a></li>
    <li class="breadcrumb-item active" aria-current="page">LCL vs FCL</li>
   </ol>
  </nav>
  <h1 class="hero-title">LCL vs FCL: Which Container Shipping Option Fits Your China Import?</h1>
  <p class="hero-subtitle">A practical comparison of cost per CBM, transit time, break-even volume and damage
  risk — with indicative 2026 freight rates and China-to-Slovakia routing.</p>

  <div class="answer-box">
   <p class="answer-lead"><strong>Short answer:</strong> LCL is cheaper below roughly 13–15 CBM because you pay
   only for the space you use (USD 55–85 per CBM from China to a European base port). FCL is cheaper and safer
   above 15 CBM because a 20ft container at USD 1,200–2,200 carries up to 28 CBM at a flat rate, with no
   consolidation handling.</p>
  </div>

  <div class="hero-stats">
   <div><b>0.5 CBM</b><span>LCL minimum</span></div>
   <div><b>~15 CBM</b><span>Break-even point</span></div>
   <div><b>35–45 d</b><span>FCL to Slovakia</span></div>
   <div><b>50+</b><span>Countries served DDP</span></div>
  </div>
 </div>
</section>

<section id="comparison" class="py-5">
 <div class="container">
  <div class="section-title-wrap text-center mb-4">
   <span class="section-eyebrow">Side by side</span>
   <div class="section-divider"></div>
   <h2 class="section-title">LCL vs FCL vs Air vs Express</h2>
   <p class="section-subtitle">Rates are indicative for H2 2026 and exclude duty and VAT unless stated. Confirm
   exact pricing with a quote before booking.</p>
  </div>
  {table_html()}
  <p class="text-muted small mt-3">Rates shown are base ocean freight from a South China port to a European base
  port. Destination charges, duty at 0–12% depending on HS code, and 23% Slovak import VAT apply separately
  under non-DDP terms.</p>
 </div>
</section>

<section id="breakeven" class="py-5 bg-white">
 <div class="container">
  <div class="section-title-wrap text-center mb-4">
   <span class="section-eyebrow">The maths</span>
   <div class="section-divider"></div>
   <h2 class="section-title">Where the LCL / FCL Break-Even Falls</h2>
  </div>
  <div class="row g-4">
   <div class="col-lg-7">
    <div class="table-responsive">
     <table class="table table-bordered align-middle">
      <thead><tr><th>Shipment volume</th><th>LCL cost (at USD 70/CBM)</th><th>20ft FCL cost</th><th>Cheaper option</th></tr></thead>
      <tbody>
       <tr><td>3 CBM</td><td>USD ~210 + destination charges</td><td>USD 1,200–2,200</td><td><strong>LCL</strong></td></tr>
       <tr><td>8 CBM</td><td>USD ~560 + destination charges</td><td>USD 1,200–2,200</td><td><strong>LCL</strong></td></tr>
       <tr><td>13 CBM</td><td>USD ~910 + destination charges</td><td>USD 1,200–2,200</td><td><strong>LCL (marginal)</strong></td></tr>
       <tr><td>18 CBM</td><td>USD ~1,260 + destination charges</td><td>USD 1,200–2,200</td><td><strong>FCL</strong></td></tr>
       <tr><td>28 CBM</td><td>USD ~1,960 + destination charges</td><td>USD 1,200–2,200 (20ft max)</td><td><strong>FCL</strong></td></tr>
       <tr><td>55 CBM</td><td>USD ~3,850 + destination charges</td><td>USD 1,900–3,400 (40HQ)</td><td><strong>FCL</strong></td></tr>
      </tbody>
     </table>
    </div>
   </div>
   <div class="col-lg-5">
    <div class="calc-card">
     <h3>Quick volume calculator</h3>
     <p class="small text-muted">Enter carton size and quantity to get CBM and the cheaper option.</p>
     <label class="small">Carton length (cm) <input id="cbmL" type="number" value="60" class="form-control form-control-sm mb-2"></label>
     <label class="small">Carton width (cm) <input id="cbmW" type="number" value="40" class="form-control form-control-sm mb-2"></label>
     <label class="small">Carton height (cm) <input id="cbmH" type="number" value="35" class="form-control form-control-sm mb-2"></label>
     <label class="small">Number of cartons <input id="cbmQ" type="number" value="100" class="form-control form-control-sm mb-2"></label>
     <button type="button" id="cbmCalc" class="btn btn-brand btn-sm mt-2">Calculate CBM</button>
     <div id="cbmOut" class="calc-out">—</div>
    </div>
   </div>
  </div>
 </div>
</section>

<section id="slovakia" class="py-5">
 <div class="container">
  <div class="section-title-wrap text-center mb-4">
   <span class="section-eyebrow">Routing</span>
   <div class="section-divider"></div>
   <h2 class="section-title">Importing from China to Slovakia &amp; Eastern Europe</h2>
   <p class="section-subtitle">Transit times, ports and import costs for Slovak, Polish, Czech, Hungarian and
   Austrian buyers.</p>
  </div>
  <div class="row g-4">
   <div class="col-md-6">
    <div class="info-card">
     <h3><i class="fas fa-anchor me-2"></i>Two viable port routes</h3>
     <p><strong>Adriatic route via Koper (Slovenia) is usually fastest for Slovakia:</strong> ocean transit
     28–35 days from Ningbo or Shenzhen to Koper, then 1–3 days by rail or truck to Bratislava, giving
     32–45 days door-to-door.</p>
     <p><strong>North European route via Hamburg or Rotterdam</strong> takes 30–38 days ocean transit plus
     4–7 days onward haulage, giving 40–55 days door-to-door. It is often cheaper per container but slower.</p>
    </div>
   </div>
   <div class="col-md-6">
    <div class="info-card">
     <h3><i class="fas fa-percent me-2"></i>Duty and VAT in Slovakia</h3>
     <p><strong>Slovakia charges 23% import VAT</strong> on the customs value including freight and insurance.
     Import duty depends on the HS code and usually ranges from 0% to 12%.</p>
     <p>If you buy DDP, the forwarder pays duty and VAT at import and bills you a single all-in rate — this
     avoids needing a Slovak EORI number for your first orders. Buying EXW or FOB means you clear customs
     yourself and reclaim VAT through your Slovak VAT return.</p>
    </div>
   </div>
  </div>
  <div class="table-responsive mt-4">
   <table class="table table-bordered align-middle">
    <thead><tr><th>Destination</th><th>Recommended port</th><th>Ocean transit</th><th>Door-to-door</th></tr></thead>
    <tbody>
     <tr><td>Bratislava, Slovakia</td><td>Koper (SI)</td><td>28–35 days</td><td>32–45 days</td></tr>
     <tr><td>Košice, Slovakia</td><td>Koper (SI)</td><td>28–35 days</td><td>34–48 days</td></tr>
     <tr><td>Warsaw, Poland</td><td>Gdańsk (PL)</td><td>30–38 days</td><td>36–48 days</td></tr>
     <tr><td>Prague, Czechia</td><td>Hamburg (DE)</td><td>30–38 days</td><td>38–50 days</td></tr>
     <tr><td>Budapest, Hungary</td><td>Koper (SI)</td><td>28–35 days</td><td>33–46 days</td></tr>
     <tr><td>Vienna, Austria</td><td>Koper (SI)</td><td>28–35 days</td><td>32–45 days</td></tr>
    </tbody>
   </table>
  </div>
  <p class="text-center mt-4 mb-0"><a href="china-sourcing-agent-eastern-europe.html" class="btn btn-brand">Eastern Europe sourcing service &rarr;</a>
  <a href="china-sourcing-agent-germany.html" class="btn btn-outline-brand ms-2">Germany / DACH &rarr;</a></p>
 </div>
</section>

<section id="choose" class="py-5 bg-white">
 <div class="container">
  <div class="section-title-wrap text-center mb-4">
   <span class="section-eyebrow">Decision guide</span>
   <div class="section-divider"></div>
   <h2 class="section-title">How to Choose in Five Steps</h2>
  </div>
  <div class="row g-4">
   <div class="col-md-6 col-lg-4"><div class="advantage-card h-100"><div class="advantage-icon"><i class="fas fa-ruler-combined"></i></div><h3 class="advantage-title">1. Measure CBM</h3><p class="advantage-desc mb-0">Multiply carton L×W×H and sum all cartons. Record gross weight too — heavy cargo can hit weight limits before volume limits.</p></div></div>
   <div class="col-md-6 col-lg-4"><div class="advantage-card h-100"><div class="advantage-icon"><i class="fas fa-scale-balanced"></i></div><h3 class="advantage-title">2. Apply the 15 CBM rule</h3><p class="advantage-desc mb-0">Under 13–15 CBM, LCL usually wins. Above 15 CBM, compare the full LCL cost including destination charges against the flat FCL rate.</p></div></div>
   <div class="col-md-6 col-lg-4"><div class="advantage-card h-100"><div class="advantage-icon"><i class="fas fa-shield-halved"></i></div><h3 class="advantage-title">3. Check fragility</h3><p class="advantage-desc mb-0">Fragile, high-value or theft-prone goods belong in FCL — the container stays sealed from factory to destination.</p></div></div>
   <div class="col-md-6 col-lg-4"><div class="advantage-card h-100"><div class="advantage-icon"><i class="fas fa-clock"></i></div><h3 class="advantage-title">4. Compare transit</h3><p class="advantage-desc mb-0">FCL is 5–10 days faster than LCL on the same lane. Seasonal goods need that buffer factored in.</p></div></div>
   <div class="col-md-6 col-lg-4"><div class="advantage-card h-100"><div class="advantage-icon"><i class="fas fa-file-invoice-dollar"></i></div><h3 class="advantage-title">5. Compare landed cost</h3><p class="advantage-desc mb-0">Compare total landed cost per unit — freight plus duty plus VAT — not freight cost alone.</p></div></div>
   <div class="col-md-6 col-lg-4"><div class="advantage-card h-100"><div class="advantage-icon"><i class="fas fa-boxes-stacked"></i></div><h3 class="advantage-title">Consolidate first</h3><p class="advantage-desc mb-0">Combining several suppliers in the Yiwu warehouse typically saves 20–40% versus shipping each order separately.</p></div></div>
  </div>
 </div>
</section>

<section id="faq" class="py-5">
 <div class="container">
  <div class="section-title-wrap text-center mb-4">
   <span class="section-eyebrow">Answers</span>
   <div class="section-divider"></div>
   <h2 class="section-title">LCL vs FCL: Frequently Asked Questions</h2>
  </div>
  <div class="faq-wrap">{faq_html}</div>
 </div>
</section>

<section class="py-5 bg-white">
 <div class="container text-center">
  <h2 class="section-title mb-3">Not sure which option fits your shipment?</h2>
  <p class="section-subtitle mb-4">Send us your carton dimensions and destination — we will quote both LCL and
  FCL door-to-door within 24 hours.</p>
  <a href="request-quote.html" class="btn btn-brand btn-lg me-2">Get a Free Freight Quote</a>
  <a href="https://wa.me/8615988516408" class="btn btn-outline-brand btn-lg" rel="noopener">WhatsApp Us</a>
 </div>
</section>

</main>
'''

STYLE = '''
<style>
 .section-hero{background:linear-gradient(135deg,#082f3b 0%,#1a5a6e 100%);color:#fff;padding:3.5rem 0 3rem}
 .section-hero .breadcrumb-item a{color:rgba(255,255,255,.8)}
 .section-hero .breadcrumb-item.active{color:#fff}
 .section-hero .breadcrumb-item+.breadcrumb-item::before{color:rgba(255,255,255,.6)}
 .hero-title{font-size:clamp(1.7rem,3.4vw,2.7rem);font-weight:800;line-height:1.2;margin-bottom:1rem;color:#fff}
 .hero-subtitle{font-size:1.05rem;opacity:.9;max-width:780px;margin-bottom:1.75rem}
 .answer-box{background:rgba(255,255,255,.12);border-left:4px solid #7fd1c7;border-radius:10px;padding:1.25rem 1.5rem;max-width:900px}
 .answer-box .answer-lead{margin:0;font-size:1rem;line-height:1.7}
 .hero-stats{display:flex;flex-wrap:wrap;gap:1.5rem;margin-top:2rem}
 .hero-stats div{background:rgba(255,255,255,.1);border-radius:10px;padding:.75rem 1.25rem;min-width:130px}
 .hero-stats b{display:block;font-size:1.5rem;font-weight:800}
 .hero-stats span{font-size:.8rem;opacity:.85}
 .cmp-table th[scope=col]{background:#0d3b4a;color:#fff;font-size:.88rem;white-space:nowrap}
 .cmp-table th[scope=row]{background:#f5f8fa;font-weight:600;white-space:nowrap}
 .cmp-table td{font-size:.9rem}
 .calc-card{background:#f5f8fa;border:1px solid #dbe5ec;border-radius:12px;padding:1.5rem}
 .calc-card h3{font-size:1.1rem;font-weight:700;margin-bottom:.5rem}
 .calc-out{margin-top:1rem;font-weight:700;color:#0d3b4a;font-size:1.05rem;min-height:1.5rem}
 .info-card{background:#f5f8fa;border:1px solid #dbe5ec;border-radius:12px;padding:1.5rem;height:100%}
 .info-card h3{font-size:1.05rem;font-weight:700;margin-bottom:.75rem;color:#0d3b4a}
 .info-card p{font-size:.93rem;color:#42586a;margin-bottom:.6rem}
 .faq-item{background:#f8fafb;border:1px solid #e1e8ed;border-radius:10px;margin-bottom:.7rem;overflow:hidden}
 .faq-item summary{cursor:pointer;padding:1rem 1.15rem;font-weight:600;color:#0d3b4a;list-style:none;display:flex;gap:.5rem;align-items:flex-start}
 .faq-item summary::-webkit-details-marker{display:none}
 .faq-item summary i{color:#1a5a6e;font-size:.72rem;margin-top:.4rem;transition:transform .2s}
 .faq-item[open] summary i{transform:rotate(90deg)}
 .faq-answer{padding:0 1.15rem 1.15rem;color:#42586a}
 .faq-answer p{margin:0;font-size:.95rem;line-height:1.7}
 .btn-brand{background:#0d3b4a;border:1px solid #0d3b4a;color:#fff;font-weight:600}
 .btn-brand:hover{background:#14536a;color:#fff}
 .btn-outline-brand{background:transparent;border:1px solid #0d3b4a;color:#0d3b4a;font-weight:600}
 .btn-outline-brand:hover{background:#0d3b4a;color:#fff}
</style>
<script>
document.addEventListener('DOMContentLoaded',function(){{
 var b=document.getElementById('cbmCalc');
 if(!b)return;
 b.addEventListener('click',function(){{
  var L=parseFloat(document.getElementById('cbmL').value)||0,
      W=parseFloat(document.getElementById('cbmW').value)||0,
      H=parseFloat(document.getElementById('cbmH').value)||0,
      Q=parseFloat(document.getElementById('cbmQ').value)||0,
      cbm=(L*W*H)/1000000*Q,
      out=document.getElementById('cbmOut');
  if(!cbm){{out.textContent='Enter carton dimensions and quantity.';return;}}
  var lcl=cbm*70,
      fcl=cbm>=15?1900:1200,
      advice=cbm<13?'LCL is usually cheaper at this volume.':(cbm<18?'Compare both — you are near the break-even point.':'FCL is usually cheaper at this volume.');
  out.innerHTML='Volume: <span style="color:#1a5a6e">'+cbm.toFixed(2)+' CBM</span><br>'+
   'Indicative LCL: USD '+Math.round(lcl)+' &middot; indicative FCL (20ft/40HQ): from USD '+fcl+
   '<br>'+advice;
 }});
}});
</script>
'''

page = HEAD + STYLE + JSONLD + "\n</head>\n" + NAV + "\n" + MAIN + "\n" + TAIL

open(OUT, "w", encoding="utf-8").write(page)

# sanity: ensure exactly one head/body/nav document shell
assert page.count("</head>") == 1, page.count("</head>")
assert page.count("<body>") == 1, page.count("<body>")
assert page.count('<nav class="navbar') == 1, page.count('<nav class="navbar')
print(f"Generated {OUT}: {len(page)} bytes, {page.count('<script type=\"application/ld+json')} JSON-LD blocks")

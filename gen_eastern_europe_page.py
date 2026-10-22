#!/usr/bin/env python3
"""Generate /china-sourcing-agent-eastern-europe.html — targets the confirmed
Bing Copilot citation query "LCL vs FCL import China Slovakia" and expands
country-page coverage to Slovakia, Poland, Czechia, Hungary, Austria, Slovenia.
Reuses the Germany page's head/nav/footer shell for native styling.
"""
import json

SRC = "china-sourcing-agent-germany.html"
OUT = "china-sourcing-agent-eastern-europe.html"
SITE = "https://www.yeatru.com"
URL = f"{SITE}/{OUT}"

src = open(SRC, encoding="utf-8").read()

head_end = src.index("</head>")
body_start = src.index("<body>")
nav_end = src.index("</nav>", body_start) + len("</nav>")
footer_start = src.index('<footer class="footer">')

HEAD = src[:head_end]
NAV = src[body_start:nav_end]
TAIL = src[footer_start:]

import re

TITLE = "China Sourcing Agent for Eastern Europe (SK, PL, CZ, HU, AT, SI) | Yeatru"
DESC = ("China sourcing agent for Slovakia, Poland, Czechia, Hungary, Austria and Slovenia: "
        "supplier sourcing, AQL 2.5 QC, LCL/FCL sea freight via Koper, Gdańsk or Hamburg, "
        "DDP door-to-door with duty and VAT handled. Free quote in 24 hours.")
KW = ("china sourcing agent eastern europe, china sourcing agent slovakia, LCL vs FCL import China Slovakia, "
      "china to slovakia shipping, china sourcing poland, china sourcing czechia, china sourcing hungary, "
      "DDP slovakia, koper port import, yiwu agent eastern europe")

HEAD = re.sub(r"<title>.*?</title>", f"<title>{TITLE}</title>", HEAD, flags=re.S)
HEAD = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{DESC}">', HEAD)
HEAD = re.sub(r'<meta name="keywords" content="[^"]*">', f'<meta name="keywords" content="{KW}">', HEAD)
HEAD = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{URL}">', HEAD)
HEAD = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{TITLE}">', HEAD)
HEAD = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{DESC}">', HEAD)
HEAD = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{URL}">', HEAD)
HEAD = re.sub(r'<meta name="twitter:title" content="[^"]*">', f'<meta name="twitter:title" content="{TITLE}">', HEAD)
HEAD = re.sub(r'<meta name="twitter:description" content="[^"]*">', f'<meta name="twitter:description" content="{DESC}">', HEAD)
HEAD = re.sub(r'<meta name="twitter:url" content="[^"]*">', f'<meta name="twitter:url" content="{URL}">', HEAD)

# Replace the inherited Germany FAQ / breadcrumb / service blocks with our own.
HEAD = re.sub(r'\s*<script type="application/ld\+json">.*?</script>', "", HEAD, flags=re.S)

FAQ = [
    ("Is LCL or FCL better for importing from China to Slovakia?",
     "LCL is cheaper below about 13-15 CBM and FCL is cheaper above it. A 20ft container from China to Koper costs USD 1,200-2,200 and carries up to 28 CBM, while LCL costs USD 55-85 per CBM, so a 30 CBM shipment in FCL typically costs 40-60% less than the same volume shipped LCL."),
    ("How long does shipping from China to Slovakia take?",
     "Door-to-door shipping from China to Bratislava takes 32-45 days via the Adriatic port of Koper, or 40-55 days via Hamburg or Rotterdam. Air freight takes 8-14 days and express courier 3-7 days."),
    ("Which port is best for importing into Slovakia, Czechia and Hungary?",
     "The port of Koper in Slovenia is usually the best choice for Slovakia, Czechia, Hungary and Austria because it is 1-3 days by rail or truck from Bratislava, Budapest, Prague and Vienna. Gdańsk is better for Poland and Hamburg suits destinations in western Czechia and Austria."),
    ("How much is import VAT in Slovakia, Poland, Czechia and Hungary?",
     "Import VAT in the region is 23% in Slovakia and Poland, 21% in Czechia, 27% in Hungary, 20% in Austria and 22% in Slovenia. VAT is charged on the customs value including freight and insurance, and it is recoverable if you are VAT-registered."),
    ("What import duty applies to Chinese goods entering the EU?",
     "Import duty depends on the product HS code and typically ranges from 0% to 12% of the customs value. Electronics often carry 0%, textiles 8-12%, and finished consumer goods usually 2-6.5%. Anti-dumping duties apply to specific categories such as e-bikes and ceramics."),
    ("Do I need an EORI number to import into Slovakia?",
     "Yes, an EU EORI number is required to clear customs as the importer of record. Under DDP terms the freight forwarder acts as importer of record and handles clearance, which lets you start importing before your own EORI is issued."),
    ("Can Yeatru consolidate goods from several Chinese suppliers for Eastern Europe?",
     "Yes. Yeatru consolidates goods from multiple suppliers in its 2,000 m² Yiwu warehouse, then ships them as one LCL lot or one FCL container to Koper, Gdańsk or Hamburg. Consolidation typically saves 20-40% compared with shipping each supplier separately."),
    ("What is the cheapest way to ship 2 CBM from China to Slovakia?",
     "For 2 CBM, LCL is the cheapest sea option at roughly USD 110-170 in ocean freight, though destination charges apply, and express courier may be cheaper if the cargo weighs under 50 kg. For 2 CBM of bulky goods, LCL via Koper is usually the lowest landed cost."),
    ("Does Yeatru handle customs clearance and delivery in Eastern Europe?",
     "Yes, Yeatru provides DDP door-to-door service covering export clearance in China, ocean or air freight, EU import clearance, duty and VAT payment, and final delivery to your address in Slovakia, Poland, Czechia, Hungary, Austria or Slovenia."),
    ("What certifications are required to sell products in the EU?",
     "Most consumer goods sold in the EU require CE marking where applicable, REACH compliance for chemicals and materials, and category-specific rules such as EN71 for toys, LFGB for food contact and WEEE registration for electronics. Yeatru verifies certificates before production."),
    ("How much does a China sourcing agent charge in Eastern Europe?",
     "Yeatru charges a service fee of 3-8% of the ex-factory order value with a minimum of USD 50 per order. There are no membership or setup fees, and the factory invoice is shared so the cost breakdown is transparent."),
    ("Can I visit the factory or the Yiwu warehouse before ordering?",
     "Yes. Clients are welcome to visit factories and the Yiwu warehouse, and Yeatru arranges itineraries, translation and factory meetings. Most partner factories are within two hours of Yiwu, and the warehouse is in Yiwu's Houzhai subdistrict."),
]

NODES = [
    {
        "@type": "WebPage",
        "@id": URL,
        "url": URL,
        "name": "China Sourcing Agent for Eastern Europe (SK, PL, CZ, HU, AT, SI)",
        "description": DESC,
        "inLanguage": "en",
        "isPartOf": {"@id": f"{SITE}/#website"},
        "about": {"@type": "Thing", "name": "China sourcing and container shipping for Eastern Europe"},
        "datePublished": "2026-10-22",
        "dateModified": "2026-10-22",
        "breadcrumb": {"@id": f"{URL}#breadcrumb"},
    },
    {
        "@type": "BreadcrumbList",
        "@id": f"{URL}#breadcrumb",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "Sourcing by Country", "item": f"{SITE}/china-sourcing-agent-europe.html"},
            {"@type": "ListItem", "position": 3, "name": "Eastern Europe", "item": URL},
        ],
    },
    {
        "@type": "ProfessionalService",
        "@id": f"{URL}#service",
        "name": "China Sourcing Agent for Eastern Europe",
        "serviceType": "ChinaSourcingAgent",
        "description": "End-to-end China sourcing for Eastern European importers: supplier verification, price negotiation, AQL 2.5 quality inspection, consolidation in Yiwu, and LCL/FCL sea freight via Koper, Gdańsk or Hamburg with DDP delivery.",
        "provider": {"@id": f"{SITE}/#organization"},
        "areaServed": [
            {"@type": "Country", "name": "Slovakia"},
            {"@type": "Country", "name": "Poland"},
            {"@type": "Country", "name": "Czechia"},
            {"@type": "Country", "name": "Hungary"},
            {"@type": "Country", "name": "Austria"},
            {"@type": "Country", "name": "Slovenia"},
        ],
        "url": URL,
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Eastern Europe sourcing packages",
            "itemListElement": [
                {"@type": "Offer", "name": "Standard sourcing fee",
                 "priceSpecification": {"@type": "PriceSpecification", "minPrice": "3", "maxPrice": "8", "priceCurrency": "USD", "unitText": "percent of order value"}},
                {"@type": "Offer", "name": "DDP sea freight (LCL)",
                 "priceSpecification": {"@type": "PriceSpecification", "minPrice": "55", "maxPrice": "85", "priceCurrency": "USD", "unitText": "CBM"}},
                {"@type": "Offer", "name": "DDP sea freight (FCL 20ft)",
                 "priceSpecification": {"@type": "PriceSpecification", "minPrice": "1200", "maxPrice": "2200", "priceCurrency": "USD"}},
            ],
        },
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

ROUTES = [
    ("Bratislava, Slovakia", "Koper (SI)", "28–35 days", "32–45 days", "23%"),
    ("Košice, Slovakia", "Koper (SI)", "28–35 days", "34–48 days", "23%"),
    ("Warsaw, Poland", "Gdańsk (PL)", "30–38 days", "36–48 days", "23%"),
    ("Prague, Czechia", "Hamburg (DE)", "30–38 days", "38–50 days", "21%"),
    ("Budapest, Hungary", "Koper (SI)", "28–35 days", "33–46 days", "27%"),
    ("Vienna, Austria", "Koper (SI)", "28–35 days", "32–45 days", "20%"),
    ("Ljubljana, Slovenia", "Koper (SI)", "28–35 days", "30–40 days", "22%"),
]
route_rows = "".join(
    f"<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td><td>{e}</td></tr>"
    for a, b, c, d, e in ROUTES
)

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

<section class="page-header py-5">
 <div class="container text-center">
  <span class="section-eyebrow">SLOVAKIA · POLAND · CZECHIA · HUNGARY · AUSTRIA · SLOVENIA</span>
  <div class="section-divider mx-auto"></div>
  <h1>China Sourcing Agent for Eastern Europe</h1>
  <p class="section-subtitle">Yeatru Sourcing is a Yiwu-based China sourcing agent serving importers in Slovakia,
  Poland, Czechia, Hungary, Austria and Slovenia. We handle supplier vetting, AQL 2.5 quality inspection,
  consolidation and LCL/FCL sea freight via Koper, Gdańsk or Hamburg with DDP door-to-door delivery.</p>
  <div class="d-flex flex-wrap justify-content-center gap-3 mt-4">
   <span class="badge" style="background:rgba(255,255,255,.12);color:#e2e8f0;border:1px solid rgba(255,255,255,.22);padding:.5rem 1rem;border-radius:999px;">Koper · Gdańsk · Hamburg</span>
   <span class="badge" style="background:rgba(255,255,255,.12);color:#e2e8f0;border:1px solid rgba(255,255,255,.22);padding:.5rem 1rem;border-radius:999px;">LCL / FCL comparison</span>
   <span class="badge" style="background:rgba(255,255,255,.12);color:#e2e8f0;border:1px solid rgba(255,255,255,.22);padding:.5rem 1rem;border-radius:999px;">DDP duty &amp; VAT included</span>
   <span class="badge" style="background:rgba(255,255,255,.12);color:#e2e8f0;border:1px solid rgba(255,255,255,.22);padding:.5rem 1rem;border-radius:999px;">AQL 2.5 inspection</span>
  </div>
 </div>
</section>

<section class="py-5">
 <div class="container">
  <nav aria-label="breadcrumb" class="mb-4">
   <ol class="breadcrumb">
    <li class="breadcrumb-item"><a href="index.html">Home</a></li>
    <li class="breadcrumb-item"><a href="china-sourcing-agent-europe.html">Europe</a></li>
    <li class="breadcrumb-item active" aria-current="page">Eastern Europe</li>
   </ol>
  </nav>

  <div class="answer-box-light mb-5">
   <p class="mb-0"><strong>Key facts for Eastern European buyers:</strong> sea freight from China to Bratislava
   takes <strong>32–45 days via Koper</strong>; LCL costs <strong>USD 55–85 per CBM</strong> and FCL
   <strong>USD 1,200–2,200 per 20ft container</strong>; import VAT is <strong>23% in Slovakia and Poland,
   21% in Czechia, 27% in Hungary, 20% in Austria and 22% in Slovenia</strong>; and Yeatru's sourcing fee is
   <strong>3–8% of the order value with a USD 50 minimum</strong>.</p>
  </div>

  <div class="section-title-wrap text-center mb-4">
   <span class="section-eyebrow">Routing</span>
   <div class="section-divider"></div>
   <h2 class="section-title">Transit Times and Ports by Destination</h2>
   <p class="section-subtitle">Indicative ocean transit and door-to-door times from South China ports. Confirm
   current schedules with a quote.</p>
  </div>
  <div class="table-responsive">
   <table class="table table-bordered align-middle">
    <thead><tr><th>Destination</th><th>Best port</th><th>Ocean transit</th><th>Door-to-door</th><th>Import VAT</th></tr></thead>
    <tbody>{route_rows}</tbody>
   </table>
  </div>
  <p class="text-center mt-3"><a href="lcl-vs-fcl-china-import.html" class="btn btn-primary">Full LCL vs FCL comparison &rarr;</a></p>
 </div>
</section>

<section class="py-5 bg-light">
 <div class="container">
  <div class="section-title-wrap text-center mb-4">
   <span class="section-eyebrow">What we do</span>
   <div class="section-divider"></div>
   <h2 class="section-title">One Partner from Factory to Your Door</h2>
  </div>
  <div class="row g-4">
   <div class="col-md-6 col-lg-4"><div class="card h-100 border-0 shadow-sm"><div class="card-body"><h3 class="h5 fw-bold">Supplier sourcing &amp; vetting</h3><p class="mb-0 text-muted">We shortlist 3–5 verified factories from our 75,000+ supplier network, compare quotes and audit the best options on site before you commit.</p></div></div></div>
   <div class="col-md-6 col-lg-4"><div class="card h-100 border-0 shadow-sm"><div class="card-body"><h3 class="h5 fw-bold">AQL 2.5 quality inspection</h3><p class="mb-0 text-muted">Every shipment is inspected to AQL 2.5 with a photo and video report before the balance payment is released. Pass rate is 99.2%.</p></div></div></div>
   <div class="col-md-6 col-lg-4"><div class="card h-100 border-0 shadow-sm"><div class="card-body"><h3 class="h5 fw-bold">Yiwu consolidation</h3><p class="mb-0 text-muted">Goods from multiple suppliers are consolidated in our 2,000 m² Yiwu warehouse, cutting freight 20–40% versus separate shipments.</p></div></div></div>
   <div class="col-md-6 col-lg-4"><div class="card h-100 border-0 shadow-sm"><div class="card-body"><h3 class="h5 fw-bold">LCL or FCL booking</h3><p class="mb-0 text-muted">We quote both options and recommend the cheaper one based on total landed cost, not freight cost alone.</p></div></div></div>
   <div class="col-md-6 col-lg-4"><div class="card h-100 border-0 shadow-sm"><div class="card-body"><h3 class="h5 fw-bold">EU compliance support</h3><p class="mb-0 text-muted">CE, REACH, EN71, LFGB and WEEE verification, plus EORI and DDP clearance so you can import without your own EORI on the first orders.</p></div></div></div>
   <div class="col-md-6 col-lg-4"><div class="card h-100 border-0 shadow-sm"><div class="card-body"><h3 class="h5 fw-bold">DDP door-to-door</h3><p class="mb-0 text-muted">Export clearance, ocean freight, EU import clearance, duty and VAT, and final delivery to your address — one all-in invoice.</p></div></div></div>
  </div>
 </div>
</section>

<section class="py-5">
 <div class="container">
  <div class="section-title-wrap text-center mb-4">
   <span class="section-eyebrow">FAQ</span>
   <div class="section-divider"></div>
   <h2 class="section-title">China to Eastern Europe: Frequently Asked Questions</h2>
  </div>
  <div>{faq_html}</div>
 </div>
</section>

<section class="py-5">
 <div class="container">
  <div class="section-title-wrap text-center mb-4">
   <span class="section-eyebrow">Related guides</span>
   <div class="section-divider"></div>
   <h2 class="section-title">Continue Reading</h2>
  </div>
  <div class="row g-3">
   <div class="col-md-4"><a href="lcl-vs-fcl-china-import.html" class="card h-100 border-0 shadow-sm text-decoration-none"><div class="card-body"><h3 class="h6 fw-bold text-primary">LCL vs FCL for China Imports</h3><p class="small text-muted mb-0">Cost per CBM, break-even at 15 CBM and Slovakia routing explained.</p></div></a></div>
   <div class="col-md-4"><a href="china-sourcing-agent-germany.html" class="card h-100 border-0 shadow-sm text-decoration-none"><div class="card-body"><h3 class="h6 fw-bold text-primary">Germany &amp; DACH Sourcing</h3><p class="small text-muted mb-0">CE / WEEE / REACH compliance and DDP to Hamburg, Munich and Vienna.</p></div></a></div>
   <div class="col-md-4"><a href="china-sourcing-agent-europe.html" class="card h-100 border-0 shadow-sm text-decoration-none"><div class="card-body"><h3 class="h6 fw-bold text-primary">Sourcing Across Europe</h3><p class="small text-muted mb-0">Country-by-country coverage for EU importers.</p></div></a></div>
  </div>
 </div>
</section>

<section class="py-5">
 <div class="container text-center">
  <h2 class="section-title mb-3">Get a quote for Slovakia, Poland or Czechia</h2>
  <p class="section-subtitle mb-4">Send your product specs and destination — we reply with supplier options and an LCL/FCL
  freight quote within 24 hours.</p>
  <a href="request-quote.html" class="btn btn-primary btn-lg me-2">Request a Free Quote</a>
  <a href="https://wa.me/8615988516408" class="btn btn-outline-primary btn-lg" rel="noopener">WhatsApp Us</a>
 </div>
</section>

</main>
'''

STYLE = '''
<style>
 .answer-box-light{background:#f1f7fa;border-left:4px solid #1a5a6e;border-radius:10px;padding:1.25rem 1.5rem;max-width:980px;margin-left:auto;margin-right:auto}
 .answer-box-light p{font-size:.98rem;line-height:1.75;color:#31505f}
 .faq-item{background:#f8fafb;border:1px solid #e1e8ed;border-radius:10px;margin-bottom:.7rem;overflow:hidden}
 .faq-item summary{cursor:pointer;padding:1rem 1.15rem;font-weight:600;color:#0d3b4a;list-style:none;display:flex;gap:.5rem;align-items:flex-start}
 .faq-item summary::-webkit-details-marker{display:none}
 .faq-item summary i{color:#1a5a6e;font-size:.72rem;margin-top:.4rem;transition:transform .2s}
 .faq-item[open] summary i{transform:rotate(90deg)}
 .faq-answer{padding:0 1.15rem 1.15rem;color:#42586a}
 .faq-answer p{margin:0;font-size:.95rem;line-height:1.7}
</style>
'''

page = HEAD + STYLE + JSONLD + "\n</head>\n" + NAV + "\n" + MAIN + "\n" + TAIL

open(OUT, "w", encoding="utf-8").write(page)

assert page.count("</head>") == 1
assert page.count("<body>") == 1
assert page.count('<nav class="navbar') == 1
print(f"Generated {OUT}: {len(page)} bytes, {page.count('<script type=\"application/ld+json')} JSON-LD, {len(FAQ)} FAQs")

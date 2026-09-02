"""Build free-quote blog. Content template as bytes to avoid Python string issues."""
import re, os, json
from datetime import date

TODAY = date.today().isoformat()
BASE = "https://www.yeatru.com"

ref_blog = 'blog-low-price-vs-procurement-expert.html'
with open(ref_blog, encoding='utf-8') as f:
    ref = f.read()

# Extract head, nav, footer
head_start = ref.index('<head>')
head_end = ref.index('</head>') + len('</head>')
head_template = ref[head_start:head_end]

nav_match = re.search(r'<nav[^>]*>.*?</nav>', ref, re.S)
nav = nav_match.group(0) if nav_match else ''

footer_match = re.search(r'<footer[^>]*>.*?</footer>', ref, re.S)
footer = footer_match.group(0) if footer_match else ''

# Load BODY from separate file
with open('freequote_body.tmpl.html', encoding='utf-8') as f:
    BODY = f.read()

TITLE = "Free China Sourcing Quotation — No Fees Until You Confirm an Order (2026)"
META_DESC = (
    "Get a free, no-obligation China sourcing quotation from Yeatru. "
    "Detailed pricing, MOQ, lead time, incoterms & shipping breakdown from 3,160+ audited factories. "
    "We earn 5-8% tiered commission only on confirmed orders — covers QC, consolidation, coordination, paperwork & operations."
)
META_KW = (
    "free china sourcing quotation, free quote china import, free yiwu quotation, "
    "china sourcing no upfront fee, 5-8% commission sourcing agent, "
    "china price comparison factory, free alibaba alternative quote, "
    "MOQ lead time incoterms breakdown, DDP FOB shipping estimate china"
)
URL = BASE + "/blog-free-quotation-china-sourcing.html"
IMAGE = "https://cdn.jsdelivr.net/gh/Yeatru/Image@main/Images/China%20Sourcing.jpg"
AUTHOR = "Yeatru Sourcing Team"
PUBLISHED = TODAY

BREADCRUMB_LD = json.dumps({
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
        {"@type":"ListItem","position":1,"name":"Home","item": BASE+"/"},
        {"@type":"ListItem","position":2,"name":"Blog","item": BASE+"/blog.html"},
        {"@type":"ListItem","position":3,"name":"Free China Sourcing Quotation","item": URL},
    ]
}, ensure_ascii=False, indent=2)

ARTICLE_LD = json.dumps({
    "@context": "https://schema.org",
    "@type": "BlogPosting",
    "headline": TITLE,
    "description": META_DESC,
    "url": URL,
    "image": IMAGE,
    "datePublished": PUBLISHED,
    "dateModified": PUBLISHED,
    "author": {"@type":"Organization","name":AUTHOR,"@id":BASE+"/#organization"},
    "publisher": {"@type":"Organization","name":"Yeatru Sourcing","@id":BASE+"/#organization"},
    "mainEntityOfPage": {"@type":"WebPage","@id":URL},
    "inLanguage": "en",
    "keywords": META_KW,
    "articleSection": "China Sourcing",
    "wordCount": 9200,
}, ensure_ascii=False, indent=2)

FAQ_LD = json.dumps({
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
        {"@type":"Question","name":"Is the quotation really free with no hidden costs?",
         "acceptedAnswer":{"@type":"Answer",
          "text":"100% free. Receiving a detailed quotation — unit prices, MOQ, lead time, logistics cost, incoterms breakdown, factory profiles, commission rate in writing — costs nothing. Zero deposit, zero credit card, zero consultation fee."}},
        {"@type":"Question","name":"How does a 5-8% commission model compare to paying per quote?",
         "acceptedAnswer":{"@type":"Answer",
          "text":"Other sourcing agents charge 50-300 USD per quote OR 250 USD/month retainer. With Yeatru you pay nothing upfront. Our 5-8% commission is deducted from the confirmed order value only — so incentives are perfectly aligned: we only earn when you win."}},
        {"@type":"Question","name":"What exactly does the 5-8% commission include?",
         "acceptedAnswer":{"@type":"Answer",
          "text":"Everything after quotation: 3-stage QC (pre-production, in-line, pre-shipment with photos), container consolidation & 30-day free warehouse, cross-factory coordination, PI/CI/PL/CO paperwork, 7x12h WhatsApp/email support, and our 25-person China team operations."}},
        {"@type":"Question","name":"How many factories do you compare for my product?",
         "acceptedAnswer":{"@type":"Answer",
          "text":"Typically 3 audited factories from our 3,160-factory verified database. We provide unit price, MOQ, lead time, certifications (CE/UL/FDA), and minimum 3 photos per factory for side-by-side comparison."}},
        {"@type":"Question","name":"What happens after I receive the quotation?",
         "acceptedAnswer":{"@type":"Answer",
          "text":"Nothing. You owe nothing and commit to nothing. If you approve the pricing and terms, we sign a simple service agreement and proceed. If not, no hard feelings and no invoice. Most clients approve within 3-7 days."}},
        {"@type":"Question","name":"What are the exact commission tiers?",
         "acceptedAnswer":{"@type":"Answer",
          "text":"Orders under USD 5,000: 7-8%. USD 5,000-20,000: 5-6%. Orders over USD 20,000: 4%. Full order management services are 3-4%. Full sourcing from scratch is 4-8%. Tiers are confirmed in writing before any order is placed."}},
        {"@type":"Question","name":"Can I visit the factory after receiving the quotation?",
         "acceptedAnswer":{"@type":"Answer",
          "text":"Yes. We can schedule factory visits in Zhejiang/Guangdong with 1-3 days notice. Audit reports (BSCI, SEDEX, ISO 9001, ISO 14001) available on request with no NDA."}},
        {"@type":"Question","name":"Are there minimum order values or minimum commission per order?",
         "acceptedAnswer":{"@type":"Answer",
          "text":"Minimum commission is 50 USD for Order Management Service and 100 USD per formal order for Full Sourcing Service. No minimum order value for quotations — we happily quote for 500 USD test orders to 500K USD FCL shipments."}},
    ]
}, ensure_ascii=False, indent=2)

ABOUT_LD = json.dumps({
    "@context": "https://schema.org",
    "@type": "WebPage",
    "@id": URL + "#webpage",
    "name": TITLE,
    "url": URL,
    "isPartOf": {"@id": BASE + "/#website"}
}, ensure_ascii=False, indent=2)

new_head = re.sub(r'<title>.*?</title>', '<title>' + TITLE + '</title>', head_template, count=1)
new_head = re.sub(r'<meta\s+name="description"\s+content="[^"]*"\s*>', '<meta name="description" content="' + META_DESC + '">', new_head, count=1)
new_head = re.sub(r'<meta\s+name="keywords"\s+content="[^"]*"\s*>', '<meta name="keywords" content="' + META_KW + '">', new_head, count=1)
new_head = re.sub(r'<link\s+rel="canonical"\s+href="[^"]*"\s*>', '<link rel="canonical" href="' + URL + '">', new_head, count=1)
new_head = re.sub(r'<script[^>]*type="application/ld\+json"[^>]*>.*?</script>', '', new_head, flags=re.S)

new_head = new_head.replace(
    '</head>',
    '\n<script type="application/ld+json">\n' + BREADCRUMB_LD + '\n</script>'
    '\n<script type="application/ld+json">\n' + ARTICLE_LD + '\n</script>'
    '\n<script type="application/ld+json">\n' + FAQ_LD + '\n</script>'
    '\n<script type="application/ld+json">\n' + ABOUT_LD + '\n</script>\n</head>'
)

page = new_head + '\n<body>' + nav + BODY + '\n' + footer + '\n</body>\n</html>'

fname = 'blog-free-quotation-china-sourcing.html'
with open(fname, 'w', encoding='utf-8') as f:
    f.write(page)

fsize = os.path.getsize(fname)
clean = re.sub(r'<[^>]+>', ' ', BODY)
approx_words = len(clean.split())

print("Created %s: %d bytes, approx %d words" % (fname, fsize, approx_words))

with open(fname, encoding='utf-8') as f:
    v = f.read()
lds = re.findall(r'<script[^>]*ld\+json[^>]*>(.*?)</script>', v, re.S)
print("\nJSON-LD blocks: %d" % len(lds))
for s in lds:
    try:
        obj = json.loads(s.strip())
        tname = obj.get('@type', '?') if isinstance(obj, dict) else '?'
        if isinstance(tname, list):
            tname = '/'.join(tname)
        print("  OK @type=%s" % tname)
    except Exception as e:
        print("  FAIL %s" % e)

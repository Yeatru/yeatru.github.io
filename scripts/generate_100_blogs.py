#!/usr/bin/env python3
"""
Generate 100 SEO/GEO-optimized blog posts for Yeatru Sourcing.
Reads topic data from blog_topics.py (list of TOPICS dicts) and renders
each into a full HTML blog post matching the existing site template.
"""
import os, json, html, re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://www.yeatru.com'
AUTHOR = 'Neil Liu'
PUBLISH = '2026-09-19'
AUTHOR_URL = f'{SITE}/about.html'
LINKEDIN = 'https://www.linkedin.com/in/neil-liu-398983257'

from blog_topics import TOPICS

NAV = open(os.path.join(REPO, 'blog.html'), encoding='utf-8').read()
NAV = NAV[NAV.find('<nav '):NAV.find('</nav>')+6]

FOOTER_RAW = open(os.path.join(REPO, 'blog.html'), encoding='utf-8').read()
FOOTER = FOOTER_RAW[FOOTER_RAW.find('<footer '):FOOTER_RAW.find('</footer>')+9]

SCRIPTS = ''' <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.4/dist/js/bootstrap.bundle.min.js?v=20260909k" defer></script>
 <script src="https://cdn.jsdelivr.net/npm/i18next@23.2.3/dist/umd/i18next.min.js?v=20260909k"></script>
 <script src="https://cdn.jsdelivr.net/npm/i18next-browser-languagedetector@7.0.1/dist/umd/i18nextBrowserLanguageDetector.min.js?v=20260909k"></script>
 <script src="i18n-svc1.js" defer></script>
<script src="i18n-svc2.js" defer></script>
<script src="i18n-svc3.js" defer></script>
<script src="i18n-misc.js" defer></script>
 <script src="app.js?v=20260918b" defer></script>'''

FLOAT = '''<div class="contact-float">
 <a href="https://wa.me/8615988516408?text=Hello%20Yeatru%20Sourcing" class="contact-float-btn whatsapp" target="_blank" rel="noopener noreferrer"><i class="fab fa-whatsapp"></i></a>
 <a href="mailto:info@yeatru.com" class="contact-float-btn email"><i class="fas fa-envelope"></i></a>
 <a href="https://t.me/YeatruSourcing" class="contact-float-btn telegram" target="_blank" rel="noopener noreferrer"><i class="fab fa-telegram"></i></a>
</div>'''

def esc(s): return html.escape(s, quote=True)

def render_article(t):
    slug = t['slug']
    url = f'{SITE}/{slug}.html'
    title = t['title']
    desc = t['desc']
    kw = t['kw']
    cat = t['cat']
    img = t['img']
    intro = t['intro']
    takeaways = t['takeaways']
    sections = t['sections']   # list of (h2, html_body)
    faqs = t['faqs']           # list of (q, a)
    related = t['related']     # list of slugs (existing blogs)

    # FAQ JSON-LD
    faq_json = json.dumps({"@context":"https://schema.org","@type":"FAQPage",
        "mainEntity":[{"@type":"Question","name":esc(q),"acceptedAnswer":{"@type":"Answer","text":esc(a)}} for q,a in faqs]})

    # Article JSON-LD
    article_json = json.dumps({"@context":"https://schema.org","@type":"Article",
        "headline":esc(title),"description":esc(desc),
        "author":{"@type":"Person","name":AUTHOR,"jobTitle":"Founder & Managing Director","url":AUTHOR_URL,"sameAs":[LINKEDIN]},
        "publisher":{"@type":"Organization","name":"Yeatru Sourcing","url":SITE,
            "logo":{"@type":"ImageObject","url":f"{SITE}/logo.svg","width":220,"height":60}},
        "datePublished":PUBLISH,"dateModified":PUBLISH,
        "image":{"@type":"ImageObject","url":f"{SITE}{img}","width":1200,"height":630},
        "mainEntityOfPage":{"@type":"WebPage","@id":url},
        "articleSection":cat,"keywords":kw,"inLanguage":"en-US"})

    breadcrumb_json = json.dumps({"@context":"https://schema.org","@type":"BreadcrumbList",
        "itemListElement":[
            {"@type":"ListItem","position":1,"name":"Home","item":f"{SITE}/"},
            {"@type":"ListItem","position":2,"name":"Blog","item":f"{SITE}/blog.html"},
            {"@type":"ListItem","position":3,"name":esc(title),"item":url}]})

    # HowTo JSON-LD (if sections look like steps, otherwise a generic how-to)
    howto_steps = [{"@type":"HowToStep","name":h2[:60],"text":re.sub('<[^>]+>','',body)[:200]} for h2,body in sections[:8]]
    howto_json = json.dumps({"@context":"https://schema.org","@type":"HowTo",
        "name":esc(title),"description":esc(desc),"step":howto_steps,"headline":esc(title)})

    blogposting_json = json.dumps({"@context":"https://schema.org","@type":"BlogPosting",
        "mainEntityOfPage":{"@type":"WebPage","@id":url},"headline":esc(title),"description":esc(desc),
        "image":[f"{SITE}{img}"],"datePublished":PUBLISH,"dateModified":PUBLISH,
        "author":{"@type":"Person","name":AUTHOR,"jobTitle":"Founder & Managing Director","url":AUTHOR_URL,"sameAs":[LINKEDIN]},
        "publisher":{"@id":f"{SITE}/#organization"},"keywords":kw,"articleSection":"China Sourcing Blog",
        "inLanguage":"en"})

    # Related articles cards
    rel_cards = ''
    for r in related:
        rslug = r if r.startswith('blog-') else f'blog-{r}'
        rel_cards += f'''<div class="col-lg-3 col-md-6">
 <a href="{rslug}.html" class="related-article-card">
 <div class="related-article-image">
 <img src="{img}" class="card-img-top object-fit-cover" alt="{esc(title)} related" loading="lazy" decoding="async" width="320" height="180">
 </div>
 <div class="related-article-content">
 <span class="related-article-category">{cat}</span>
 <h3 class="related-article-title">{esc(title)[:50]}</h3>
 </div>
 </a>
 </div>'''

    takeaways_html = '<aside class="article-takeaways"><h2>Key Takeaways</h2><ul>' + \
        ''.join(f'<li>{tk}</li>' for tk in takeaways) + '</ul></aside>'

    sections_html = ''.join(f'<h2>{h2}</h2>{body}' for h2,body in sections)

    faq_html = '<h2>Frequently Asked Questions</h2>' + \
        ''.join(f'<h3>{i}. {q}</h3><p>{a}</p>' for i,(q,a) in enumerate(faqs,1))

    html_out = f'''<!DOCTYPE html>
<html lang="en">
<head>
 <meta charset="UTF-8">
 <link rel="preconnect" href="https://fonts.googleapis.com?v=20260909k">
 <link rel="preconnect" href="https://fonts.gstatic.com?v=20260909k" crossorigin>
 <link href="https://fonts.googleapis.com/css2?v=20260909k&family=Inter:wght@400;500;600;700;800&family=Playfair+Display:wght@500;600;700&display=swap" rel="stylesheet">
 <meta name="viewport" content="width=device-width initial-scale=1.0">
 <title>{esc(title)}</title>
 <meta name="description" content="{esc(desc)}">
 <meta name="keywords" content="{esc(kw)}">
 <meta name="robots" content="index follow">
 <meta name="theme-color" content="#1665a9">
 <link rel="icon" type="image/svg+xml" href="/favicon.svg">
 <link rel="canonical" href="{url}">
 <link rel="alternate" hreflang="en" href="{url}">
 <link rel="alternate" hreflang="x-default" href="{url}">
 <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.4/dist/css/bootstrap.min.css?v=20260909k" media="print" onload="this.media='all'">
 <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
 <link rel="stylesheet" href="styles.css?v=20260918g">
 <meta property="og:type" content="article">
 <meta property="og:url" content="{url}">
 <meta property="og:site_name" content="Yeatru Sourcing">
 <meta property="og:title" content="{esc(title)}">
 <meta property="og:description" content="{esc(desc)}">
 <meta property="og:image" content="{SITE}{img}">
 <meta name="twitter:card" content="summary_large_image">
 <meta name="twitter:title" content="{esc(title)}">
 <meta name="twitter:description" content="{esc(desc)}">
 <meta name="twitter:image" content="{SITE}{img}">
 <script type="application/ld+json">{article_json}</script>
 <script type="application/ld+json">{breadcrumb_json}</script>
 <script type="application/ld+json">{howto_json}</script>
 <script type="application/ld+json">{faq_json}</script>
 <script type="application/ld+json">{blogposting_json}</script>
</head>
<body>
{NAV}

 <section class="page-header py-5">
 <div class="container text-center">
 <span class="section-eyebrow">{esc(cat.upper())}</span>
 <div class="section-divider mx-auto"></div>
 <h1 class="section-title">{esc(title)}</h1>
 <p class="section-subtitle">{esc(desc)}</p>
 </div>
 </section>

 <section class="article-body-section py-5">
 <div class="container">
 <div class="row justify-content-center">
 <div class="col-lg-8">
 <article class="article-content">
<div class="article-featured-image">
<img loading="lazy" src="{img}" alt="{esc(title)}" class="img-fluid rounded">
</div>
{takeaways_html}
{intro}
{sections_html}
{faq_html}
<h2>Conclusion</h2>
<p>{esc(desc)} For buyers serious about quality, compliance, and total landed cost — not just the lowest Alibaba quote — working with a verified China sourcing partner reduces risk and typically returns 12-28% in real savings. Get a free, no-obligation sourcing quote within 24 hours.</p>
<aside class="author-bio mt-5 pt-4 border-top">
 <div class="d-flex align-items-start gap-3 flex-wrap flex-sm-nowrap">
 <div>
 <h3 class="h5 mb-1">Neil Liu</h3>
 <p class="text-muted small mb-2"><strong>China Sourcing Expert</strong> · Yeatru Sourcing</p>
 <p class="mb-2">Neil Liu is the Founder &amp; Managing Director of Yeatru Sourcing, a Yiwu-based China sourcing agent with 14+ years of combined experience helping Amazon FBA sellers, retailers, and wholesale buyers find reliable suppliers, control product quality, and ship from China. Based in Yiwu — home to the world\'s largest small commodity market.</p>
 <div class="d-flex gap-2 flex-wrap">
 <a href="{LINKEDIN}" target="_blank" rel="noopener noreferrer" aria-label="Neil Liu on LinkedIn" class="btn btn-sm btn-outline-secondary"><i class="fab fa-linkedin-in"></i></a>
 </div>
 </div>
 </div>
</aside>
 </article>
 </div>
 </div>
 </div>
 </section>

 <section class="py-5 cta-section-dark">
 <div class="container">
 <div class="final-cta-box text-center">
 <span class="section-eyebrow">Get Started</span>
 <div class="section-divider mx-auto" style="margin: 0.75rem auto 1.5rem;"></div>
 <h2 class="section-title">Need Help With This?</h2>
 <p class="section-subtitle mb-4">Get a free, no-obligation sourcing quote from Yeatru Sourcing — verified factories, AQL 2.5 QC, and DDP shipping worldwide.</p>
 <a href="contact.html" class="btn btn-cta btn-lg"><i class="fas fa-comment-dots me-2"></i>Get a Free Quote</a>
 </div>
 </div>
 </section>

<section class="py-5 section-alt">
 <div class="container">
 <div class="section-title-wrap text-center mb-5">
 <span class="section-eyebrow">Continue Reading</span>
 <div class="section-divider"></div>
 <h2 class="section-title">Related Articles</h2>
 </div>
 <div class="row g-4">
{rel_cards}
 </div>
 </div>
</section>

{FOOTER}

{SCRIPTS}
{FLOAT}
</body>
</html>'''
    return html_out

def main():
    count = 0
    for t in TOPICS:
        out = render_article(t)
        path = os.path.join(REPO, f"{t['slug']}.html")
        with open(path, 'w', encoding='utf-8') as f:
            f.write(out)
        count += 1
    print(f"Generated {count} blog posts.")

if __name__ == '__main__':
    main()

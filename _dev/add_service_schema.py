#!/usr/bin/env python3
"""Add schema.org/Service JSON-LD to service pages that lack it.
Inserts a Service block after the existing BreadcrumbList JSON-LD.
"""
import re

SITE = "https://www.yeatru.com"

SERVICES = {
    "supplier-verification.html": {
        "name": "Supplier Verification Service",
        "serviceType": "SupplierVerification",
        "description": "On-site supplier verification including business license check, production capacity assessment, quality system review, and social compliance audit. We visit every factory before recommending it to you.",
        "areaServed": "Worldwide",
    },
    "factory-audit.html": {
        "name": "Factory Audit Service",
        "serviceType": "FactoryAudit",
        "description": "Comprehensive factory audit covering business license verification, production capacity, quality management system (ISO 9001), worker conditions, and export experience. Detailed audit report with photos provided.",
        "areaServed": "Worldwide",
    },
    "sample-order.html": {
        "name": "Sample Order Service",
        "serviceType": "SampleOrder",
        "description": "Product sample procurement service including sample production coordination, payment handling, quality check, and international shipping. Samples typically arrive within 3-15 business days.",
        "areaServed": "Worldwide",
    },
}


def breadcrumb_script_re():
    return re.compile(
        r'(<script type="application/ld\+json">\s*\{[^}]*"@type":\s*"BreadcrumbList".*?\}\s*</script>)',
        re.S,
    )


def process(fname, svc):
    h = open(fname, encoding="utf-8").read()
    # Already has Service? skip
    if '"@type": "Service"' in h:
        return f"SKIP {fname} (already has Service)"

    m = breadcrumb_script_re().search(h)
    if not m:
        return f"ERROR {fname} (no BreadcrumbList found)"

    service_json = {
        "@context": "https://schema.org",
        "@type": "Service",
        "@id": f"{SITE}/{fname}#service",
        "name": svc["name"],
        "serviceType": svc["serviceType"],
        "description": svc["description"],
        "provider": {
            "@type": "Organization",
            "name": "Yeatru Sourcing",
            "url": SITE,
        },
        "areaServed": svc["areaServed"],
        "url": f"{SITE}/{fname}",
        "offers": {
            "@type": "Offer",
            "name": "Service fee",
            "price": "50-2000",
            "priceCurrency": "USD",
            "description": "Transparent service fee from USD 50. Contact us for a custom quote.",
            "availability": "https://schema.org/InStock",
        },
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Yeatru Service Plans",
            "url": f"{SITE}/service-plans.html",
        },
    }
    import json as _json
    block = (
        '\n <script type="application/ld+json">\n'
        + _json.dumps(service_json, ensure_ascii=False, indent=2)
        + "\n </script>\n"
    )

    h = h[:m.end()] + block + h[m.end():]
    open(fname, "w", encoding="utf-8").write(h)
    return f"OK {fname}"


if __name__ == "__main__":
    for fname, svc in SERVICES.items():
        print(process(fname, svc))

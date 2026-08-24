#!/usr/bin/env python3
"""
Yeatru Sourcing - Daily SEO Monitor
每天运行一次，检查网站健康状态
用法: python3 daily-monitor.py
"""

import urllib.request, ssl, json, re, sys
from datetime import datetime

BASE_URL = "https://www.yeatru.com"
TIMEOUT = 15

ctx = ssl.create_default_context()

PAGES = [
    "/", "/faq.html", "/blog.html", "/about.html", "/contact.html",
    "/products.html", "/product-sourcing.html", "/quality-control.html",
    "/logistics-shipping.html", "/oem.html", "/supplier-verification.html",
    "/testimonials.html", "/service-plans.html", "/design-photography.html",
    "/price-negotiation.html", "/data.html",
    "/blog-alibaba-vs-agent.html", "/blog-amazon-supplier-guide.html",
    "/blog-first-time-china-sourcing.html", "/blog-yiwu-market-guide.html",
]

def check_page(path):
    """Check a single page for status code, meta tags, and key content."""
    result = {"url": f"{BASE_URL}{path}", "path": path}
    try:
        req = urllib.request.Request(
            f"{BASE_URL}{path}",
            headers={"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"}
        )
        resp = urllib.request.urlopen(req, timeout=TIMEOUT, context=ctx)
        html = resp.read().decode("utf-8")
        result["status"] = resp.status
        result["ok"] = True
        result["size"] = len(html)
        
        # Check meta description
        meta_desc = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', html)
        if meta_desc:
            desc = meta_desc.group(1)
            result["meta_desc_len"] = len(desc)
            if len(desc) < 140 or len(desc) > 175:
                result["meta_desc_warning"] = f"Length {len(desc)} (ideal: 150-165)"
        
        # Check canonical
        canonical = re.search(r'<link\s+rel="canonical"\s+href="([^"]*)"', html)
        if canonical:
            result["canonical"] = canonical.group(1)
        
        # Check for IndexNow meta
        if "IndexNow" in html:
            result["indexnow"] = True
        
        # Check for JSON-LD
        jsonld_count = html.count('application/ld+json')
        result["jsonld_count"] = jsonld_count
        
    except urllib.error.HTTPError as e:
        result["status"] = e.code
        result["ok"] = False
    except Exception as e:
        result["status"] = "ERR"
        result["ok"] = False
        result["error"] = str(e)
    
    return result

def check_sitemap():
    """Check sitemap accessibility and count URLs."""
    try:
        req = urllib.request.Request(
            f"{BASE_URL}/sitemap.xml",
            headers={"User-Agent": "Googlebot/2.1"}
        )
        resp = urllib.request.urlopen(req, timeout=TIMEOUT, context=ctx)
        body = resp.read().decode("utf-8")
        urls = len(re.findall(r"<loc>", body))
        return {"ok": True, "status": resp.status, "url_count": urls}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def check_robots():
    """Check robots.txt for proper configuration."""
    try:
        req = urllib.request.Request(
            f"{BASE_URL}/robots.txt",
            headers={"User-Agent": "Googlebot/2.1"}
        )
        resp = urllib.request.urlopen(req, timeout=TIMEOUT, context=ctx)
        body = resp.read().decode("utf-8")
        checks = {
            "allow_all": "Allow: /" in body,
            "indexnow_key": "cb82a7f9" in body,
            "ai_crawlers": any(bot in body for bot in ["GPTBot", "ClaudeBot", "PerplexityBot"]),
        }
        return {"ok": True, "status": resp.status, "checks": checks}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def main():
    print("=" * 60)
    print(f"🔍 Yeatru Sourcing — Daily SEO Monitor")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    
    # 1. Check sitemap
    print("\n📄 1. Sitemap")
    sitemap = check_sitemap()
    if sitemap["ok"]:
        print(f"   ✅ HTTP {sitemap['status']} | {sitemap['url_count']} URLs")
    else:
        print(f"   ❌ ERROR: {sitemap.get('error', 'unknown')}")
    
    # 2. Check robots
    print("\n🤖 2. Robots.txt")
    robots = check_robots()
    if robots["ok"]:
        for check, passed in robots["checks"].items():
            icon = "✅" if passed else "⚠️"
            print(f"   {icon} {check}: {'OK' if passed else 'WARNING'}")
    else:
        print(f"   ❌ ERROR: {robots.get('error', 'unknown')}")
    
    # 3. Check all pages
    print("\n🔗 3. Pages Status")
    results = []
    ok_count = 0
    warn_count = 0
    error_count = 0
    
    for page in PAGES:
        r = check_page(page)
        results.append(r)
        if r["ok"]:
            if "meta_desc_warning" in r:
                warn_count += 1
                print(f"   ⚠️  {r['status']} {page} — {r['meta_desc_warning']}")
            else:
                ok_count += 1
                print(f"   ✅  {r['status']} {page}")
        else:
            error_count += 1
            print(f"   ❌  {r.get('status', 'ERR')} {page}")
    
    print(f"\n   Summary: {ok_count} OK | {warn_count} Warning | {error_count} Error")
    
    # 4. Homepage deep check
    print("\n🏠 4. Homepage Details")
    home = next((r for r in results if r["path"] == "/"), None)
    if home and home["ok"]:
        print(f"   Status: {home['status']} ✅")
        print(f"   Size: {home.get('size', '?'):,} bytes")
        print(f"   Meta Desc: {home.get('meta_desc_len', '?')} chars")
        print(f"   JSON-LD blocks: {home.get('jsonld_count', '?')}")
        print(f"   IndexNow: {'✅' if home.get('indexnow') else '❌'}")
    
    # 5. Alert summary
    print("\n📋 5. Alert Summary")
    alerts = []
    if sitemap.get("url_count", 0) < 20:
        alerts.append("Sitemap has fewer than 20 URLs!")
    if error_count > 0:
        alerts.append(f"{error_count} pages returning errors!")
    if warn_count > 0:
        alerts.append(f"{warn_count} pages with meta description issues!")
    if robots["ok"] and not robots["checks"]["ai_crawlers"]:
        alerts.append("AI crawlers not configured in robots.txt!")
    
    if alerts:
        for a in alerts:
            print(f"   ⚠️  {a}")
    else:
        print("   ✅  All checks passed! Website is healthy.")
    
    print("\n" + "=" * 60)
    return 0 if not alerts else 1

if __name__ == "__main__":
    sys.exit(main())

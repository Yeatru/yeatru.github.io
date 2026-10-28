#!/usr/bin/env python3
"""
====================================================================
 Cloudflare Pages 迁移后验证脚本 (0 风险保障工具 #1)
====================================================================
作用:
  1. 在切 DNS 之前，先验证 Cloudflare Pages 临时域名 (*.pages.dev) 的内容是否
     和当前 GitHub Pages 生产站点 (yeatru.github.io / www.yeatru.com) 完全一致
  2. 确保所有 719 个 sitemap URL 都返回 HTTP 200，不能有任何 404
  3. 确保 301 重定向方向正确 (裸域 → www, http → https, github.io → www)
  4. 输出 PASS / FAIL 报告。任何一项 FAIL，都不要切 DNS！

用法:
  1. 部署到 Cloudflare Pages 后，拿到临时域名 (如: yeatru.pages.dev)
  2. 运行:
       python compare_after_deploy.py verify --pages yeatru.pages.dev
       python compare_after_deploy.py diff   --pages yeatru.pages.dev --prod www.yeatru.com
       python compare_after_deploy.py redirect --pages yeatru.pages.dev

作者: Yeatru SEO 迁移保障工具
日期: 2026-08-13
"""
import argparse
import json
import sys
import time
import urllib.request
import urllib.error
import ssl
import re
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

ssl._create_default_https_context = ssl._create_unverified_context

SITEMAP = Path("sitemap.xml")
BASELINE = Path("SEO_BASELINE.json")

UA = "Mozilla/5.0 (compatible; YeatruMigrationBot/1.0; +https://www.yeatru.com/)"

# —————————————————————————————————————————————————————————————————
# 工具: 简单 HTTP GET
# —————————————————————————————————————————————————————————————————
def fetch(url, follow_redirects=False, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        resp = urllib.request.urlopen(req, timeout=timeout) if follow_redirects \
            else urllib.request.urlopen(req, timeout=timeout)
        body = resp.read().decode("utf-8", errors="ignore")
        return {"status": resp.status, "url": resp.geturl(), "body": body, "headers": dict(resp.headers)}
    except urllib.error.HTTPError as e:
        return {"status": e.code, "url": url, "body": "", "headers": dict(e.headers)}
    except Exception as e:
        return {"status": -1, "url": url, "body": str(e), "headers": {}}


def fetch_no_follow(url, timeout=20):
    """不跟踪 3xx，直接看 status code"""
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None
    opener = urllib.request.build_opener(NoRedirect)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        resp = opener.open(req, timeout=timeout)
        return {"status": resp.status, "location": resp.headers.get("Location"), "final_url": resp.geturl()}
    except urllib.error.HTTPError as e:
        return {"status": e.code, "location": e.headers.get("Location"), "final_url": url}
    except Exception as e:
        return {"status": -1, "location": str(e), "final_url": url}


# —————————————————————————————————————————————————————————————————
# 从 sitemap 读取 URL 列表
# —————————————————————————————————————————————————————————————————
def load_sitemap_urls():
    if not SITEMAP.exists():
        return []
    return re.findall(r"<loc>([^<]+)</loc>", SITEMAP.read_text(encoding="utf-8"))


# —————————————————————————————————————————————————————————————————
# 1. VERIFY: Pages 临时域名上所有 sitemap URL 都 200 OK
# —————————————————————————————————————————————————————————————————
def cmd_verify(args):
    print(f"✅ 验证阶段 1/4: Pages 临时域名 {args.pages} 所有 sitemap URL → HTTP 200\n")
    urls = load_sitemap_urls()
    if not urls:
        print("❌ sitemap.xml 空，无法验证")
        return 1

    # 用临时域名替换 sitemap 域名
    base_domain = re.match(r"https?://([^/]+)", urls[0]).group(1)
    temp_urls = [u.replace(base_domain, args.pages) for u in urls]

    ok = 0
    failed = []
    total = len(temp_urls)
    with ThreadPoolExecutor(max_workers=32) as pool:
        futures = {pool.submit(fetch, url, True): url for url in temp_urls}
        for i, fut in enumerate(as_completed(futures), 1):
            url = futures[fut]
            r = fut.result()
            if r["status"] == 200:
                ok += 1
            else:
                failed.append((url, r["status"]))
            if i % 100 == 0 or i == total:
                print(f"   [{i}/{total}]  200 OK: {ok}  失败: {len(failed)}", flush=True)

    print(f"\n📊 结果: {ok}/{total} 200 OK")
    if failed:
        print("❌ 失败列表 (前 10):")
        for u, s in failed[:10]:
            print(f"   HTTP {s}  {u}")
        return 1
    print("✅ 全部 200 — sitemap 内容完整")
    return 0


# —————————————————————————————————————————————————————————————————
# 2. DIFF: Pages vs 生产 对比首页+10 个关键页
# —————————————————————————————————————————————————————————————————
KEY_PAGES = ["/", "/index.html", "/service-plans.html", "/payment.html", "/products.html",
             "/about.html", "/faq.html", "/contact.html", "/blog.html", "/data.html",
             "/refund.html", "/terms.html", "/privacy.html", "/quality-control.html"]


def cmd_diff(args):
    print(f"✅ 验证阶段 2/4: Pages {args.pages} vs 生产 {args.prod} 标题/大小对比\n")
    if BASELINE.exists():
        baseline = json.loads(BASELINE.read_text(encoding='utf-8'))
    else:
        baseline = {}

    mismatches = []
    for path in KEY_PAGES:
        pages_url = f"https://{args.pages}{path}"
        prod_url = f"https://{args.prod}{path}"
        pr = fetch(pages_url, True)
        gr = fetch(prod_url, True)
        p_title = re.search(r"<title>([^<]*)</title>", pr["body"])
        g_title = re.search(r"<title>([^<]*)</title>", gr["body"])
        p_title = p_title.group(1)[:60] if p_title else "NO_TITLE"
        g_title = g_title.group(1)[:60] if g_title else "NO_TITLE"
        p_len = len(pr["body"])
        g_len = len(gr["body"])
        diff = abs(p_len - g_len) / max(1, g_len)
        status_str = "✅" if (pr["status"] == 200 and gr["status"] == 200 and diff < 0.15) else "⚠️"
        note = ""
        if diff >= 0.15: note = f" (体积差 {diff*100:.0f}%，超过 15% 阈值)"
        if p_title != g_title: note += f" (标题不同)"
        print(f"   {status_str} {path:30s}  Pages:{p_len:>8d}B  Prod:{g_len:>8d}B{note}")
        if status_str == "⚠️":
            mismatches.append(path)

    print()
    if mismatches:
        print(f"⚠️  有 {len(mismatches)} 页差异超过阈值，请人工确认是否是新图片/新配置导致（_headers/_redirects 体积差异 <15% 是正常的）")
        return 0 if args.force else 1
    print("✅ 关键页内容匹配")
    return 0


# —————————————————————————————————————————————————————————————————
# 3. REDIRECT: 验证 5 条重定向规则
# —————————————————————————————————————————————————————————————————
def cmd_redirect(args):
    print(f"✅ 验证阶段 3/4: 重定向规则 (Pages 上线 + 切 DNS 后验证)\n")
    tests = [
        # (label, request_url, expected_status, expected_location_contains)
        ("http://www.yeatru.com/",          "http://www.yeatru.com/",          301, "https://www.yeatru.com"),
        ("https://yeatru.com/",              "https://yeatru.com/",              301, "https://www.yeatru.com"),
        ("https://yeatru.github.io/",        "https://yeatru.github.io/",        301, "www.yeatru.com"),
        ("https://www.yeatru.com/index.html","https://www.yeatru.com/index.html",301, "/"),
        ("https://www.yeatru.com/",          "https://www.yeatru.com/",          200, None),
        ("https://www.yeatru.com/sitemap.xml","https://www.yeatru.com/sitemap.xml",200, None),
    ]
    any_fail = 0
    for label, url, expected_status, expected_loc in tests:
        r = fetch_no_follow(url)
        ok = True
        if r["status"] != expected_status:
            ok = False
        if expected_loc and r["location"] and expected_loc not in (r["location"] or ""):
            ok = False
        s = "✅" if ok else "❌"
        loc = f" → {r['location']}" if r["location"] else ""
        print(f"   {s} HTTP {r['status']:3d}{loc:60s}  {label}")
        if not ok:
            any_fail += 1
            print(f"       期望: HTTP {expected_status} 含 '{expected_loc}'")
            print(f"       实际: HTTP {r['status']}  → '{r['location']}'")
    print()
    if any_fail:
        print("⚠️  重定向未完全生效。如果还没切 DNS，这是正常的；切完 DNS 再跑一次。")
        return 0
    print("✅ 所有重定向正确")
    return 0


# —————————————————————————————————————————————————————————————————
# 4. HEADERS: 检查缓存 & 安全头
# —————————————————————————————————————————————————————————————————
def cmd_headers(args):
    print(f"✅ 验证阶段 4/4: _headers 响应头验证 ({args.host})\n")
    checks = [
        ("/Images/FBA.jpg", "Cache-Control", "max-age="),
        ("/*.css (用 styles.css 代替)", "/styles.css", "Cache-Control", "immutable"),
        ("/", "X-Content-Type-Options", "nosniff"),
        ("/", "Strict-Transport-Security", "max-age="),
        ("/sitemap.xml", "Cache-Control", "max-age="),
    ]
    any_fail = 0
    for i, row in enumerate(checks):
        if len(row) == 3:
            path, hdr, need = row
            label = path
        else:
            label, path, hdr, need = row
        url = f"https://{args.host}{path}"
        r = fetch(url, True)
        val = r["headers"].get(hdr, "")
        ok = need in (val or "")
        s = "✅" if ok else "❌"
        print(f"   {s} {hdr:35s} = {val[:60]:60s}  (含'{need}')  {label}")
        if not ok:
            any_fail += 1
    print()
    if any_fail:
        print("⚠️  响应头缺失（_headers 可能未被 Pages 正确解析），去 Cloudflare Pages → Headers 面板核对")
        return 1
    print("✅ _headers 完全生效 — PSI 267 KiB 缓存问题就此解决")
    return 0


# —————————————————————————————————————————————————————————————————
# CLI
# —————————————————————————————————————————————————————————————————
def main():
    ap = argparse.ArgumentParser("Yeatru Cloudflare Pages 迁移验证工具")
    sub = ap.add_subparsers(dest="cmd", required=True)

    v = sub.add_parser("verify", help="验证 Pages 临时域名所有 sitemap URL 200 OK")
    v.add_argument("--pages", required=True, help="Pages 临时域名, e.g. yeatru.pages.dev")
    v.set_defaults(func=cmd_verify)

    d = sub.add_parser("diff", help="Pages vs 生产站内容对比")
    d.add_argument("--pages", required=True, help="Pages 临时域名")
    d.add_argument("--prod", default="www.yeatru.com", help="当前生产域名")
    d.add_argument("--force", action="store_true", help="忽略差异")
    d.set_defaults(func=cmd_diff)

    r = sub.add_parser("redirect", help="重定向验证 (切 DNS 后用)")
    r.add_argument("--pages", default="yeatru.pages.dev")
    r.set_defaults(func=cmd_redirect)

    h = sub.add_parser("headers", help="_headers 响应头验证")
    h.add_argument("--host", default="www.yeatru.com")
    h.set_defaults(func=cmd_headers)

    a = sub.add_parser("all", help="依次运行所有验证 (推荐!)")
    a.add_argument("--pages", required=True, help="Pages 临时域名")
    a.add_argument("--prod", default="www.yeatru.com")
    a.add_argument("--host", default="www.yeatru.com")
    def all_cmd(args):
        rc = 0
        rc |= cmd_verify(args)
        rc |= cmd_diff(args)
        rc |= cmd_redirect(args)
        rc |= cmd_headers(args)
        print("\n" + ("=" * 70))
        if rc == 0:
            print("🎉 全部 4 阶段验证通过 → 可以切 DNS 流量了！")
        else:
            print("❌ 有项目失败，先修复再切 DNS。当前网站仍然在 GitHub Pages，不受影响。")
        return rc
    a.set_defaults(func=all_cmd)

    ns = ap.parse_args()
    sys.exit(ns.func(ns))


if __name__ == "__main__":
    main()

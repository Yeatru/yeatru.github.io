#!/usr/bin/env python3
"""IndexNow 批量推送脚本 - 将 sitemap.xml 中所有 URL 提交给 Bing 即时索引"""

import xml.etree.ElementTree as ET
import urllib.request
import urllib.error
import json
import ssl
import time

INDEXNOW_KEY = "cb82a7f9-5e3d-4b8a-9c2e-1d5f7a3b9c8d"
HOST = "www.yeatru.com"
SITEMAP_FILE = "sitemap.xml"
API_URL = "https://www.bing.com/indexnow"
BATCH_SIZE = 100
SLEEP_BETWEEN_BATCHES = 1.5

def parse_sitemap(filepath):
    ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    tree = ET.parse(filepath)
    root = tree.getroot()
    urls = []
    for u in root.findall('s:url', ns):
        loc = u.find('s:loc', ns)
        if loc is not None and loc.text:
            urls.append(loc.text)
    return urls

def submit_batch(urls_batch):
    payload = json.dumps({
        "host": HOST,
        "key": INDEXNOW_KEY,
        "urlList": urls_batch
    }).encode('utf-8')
    req = urllib.request.Request(API_URL, data=payload, method='POST')
    req.add_header('Content-Type', 'application/json')
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
            return resp.status, resp.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8', errors='replace')[:200]
    except Exception as e:
        return None, str(e)

def main():
    print(f"📖 读取 {SITEMAP_FILE} ...")
    all_urls = parse_sitemap(SITEMAP_FILE)
    total = len(all_urls)
    print(f"✅ 发现 {total} 个 URL")

    static_count = sum(1 for u in all_urls if '?product=' not in u)
    product_count = total - static_count
    print(f"   - 静态页面: {static_count}")
    print(f"   - 产品页面: {product_count}")

    print(f"\n🚀 开始推送 IndexNow (批次大小: {BATCH_SIZE}) ...\n")

    success = 0
    failed = 0

    for i in range(0, total, BATCH_SIZE):
        batch = all_urls[i:i + BATCH_SIZE]
        batch_num = (i // BATCH_SIZE) + 1
        total_batches = (total + BATCH_SIZE - 1) // BATCH_SIZE

        print(f"  [{batch_num}/{total_batches}] 推送 {len(batch)} 个 URL ...", end=" ")

        status_code, response = submit_batch(batch)

        if status_code == 200:
            success += len(batch)
            print(f"✅ 成功 (HTTP 200)")
        elif status_code == 202:
            success += len(batch)
            print(f"✅ 已接受 (HTTP 202 - 处理中)")
        else:
            failed += len(batch)
            print(f"❌ 失败 (HTTP {status_code}): {response[:200]}")

        if i + BATCH_SIZE < total:
            time.sleep(SLEEP_BETWEEN_BATCHES)

    print(f"\n{'='*50}")
    print(f"📊 推送完成！")
    print(f"   成功/已接受: {success} 个")
    print(f"   失败:         {failed} 个")
    print(f"   总计:         {total} 个")
    print(f"\n💡 Bing 将在几分钟内开始爬取这些 URL")

if __name__ == "__main__":
    main()

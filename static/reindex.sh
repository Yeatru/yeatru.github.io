#!/usr/bin/env bash
# =============================================================================
# Yeatru Sourcing — Search Engine Reindexing Script
# =============================================================================
# Submits URLs to Google, Bing, IndexNow (Bing+Yandex+Seznam+Naver),
# and generates a sitemap ping. Use after major SEO fixes or content updates.
#
# USAGE:  bash reindex.sh [--mode=all|critical|products|blogs]
# KEY:    b8f3a7d2e91c4b6f8a3e5d7f2c9a1b4e  (IndexNow verification)
# =============================================================================

set -euo pipefail

SITE="https://www.yeatru.com"
INDEXNOW_KEY="b8f3a7d2e91c4b6f8a3e5d7f2c9a1b4e"
MODE="${1:---mode=all}"
MODE="${MODE#--mode=}"
MODE="${MODE:=all}"

echo "================================================"
echo " Yeatru Sourcing — Reindex & Resubmit"
echo " Mode: $MODE"
echo "================================================"
echo ""

# ── Build URL list ──────────────────────────────────────────────────────────
URLS=()

# Critical pages (always include)
CRITICAL=(
  "$SITE/"
  "$SITE/all-products.html"
  "$SITE/products.html"
  "$SITE/contact.html"
  "$SITE/about.html"
  "$SITE/faq.html"
  "$SITE/blog.html"
  "$SITE/sitemap.xml"
  "$SITE/testimonials.html"
  "$SITE/sourcing-agent-for-tiktok-shop-seller.html"
)

if [[ "$MODE" == "all" || "$MODE" == "critical" ]]; then
  URLS+=("${CRITICAL[@]}")
fi

if [[ "$MODE" == "all" || "$MODE" == "products" ]]; then
  echo "📦 Fetching product URLs from all-products.html..."
  PRODUCT_URLS=$(curl -sL "$SITE/all-products.html" 2>/dev/null \
    | grep -oE 'href="product-YCS-[^"]+\.html"' \
    | sed 's/href="//;s/"$//' \
    | sort -u \
    | while read -r p; do echo "$SITE/$p"; done)
  while IFS= read -r url; do
    [[ -n "$url" ]] && URLS+=("$url")
  done <<< "$PRODUCT_URLS"
  echo "   → $(echo "$PRODUCT_URLS" | wc -l) product URLs"
fi

if [[ "$MODE" == "all" || "$MODE" == "blogs" ]]; then
  echo "📝 Fetching blog URLs..."
  BLOG_URLS=$(curl -sL "$SITE/sitemap-static.xml" 2>/dev/null \
    | grep -oE 'https://www\.yeatru\.com/blog-[^<]+\.html' \
    | sort -u)
  while IFS= read -r url; do
    [[ -n "$url" ]] && URLS+=("$url")
  done <<< "$BLOG_URLS"
  echo "   → $(echo "$BLOG_URLS" | wc -l) blog URLs"
fi

# Deduplicate
URLS=($(printf '%s\n' "${URLS[@]}" | sort -u))
echo ""
echo "Total unique URLs to submit: ${#URLS[@]}"
echo ""

# ── 1. IndexNow (Bing + Yandex + Seznam + Naver) ────────────────────────────
# Key file must be at https://www.yeatru.com/$INDEXNOW_KEY.txt
echo "━━━ 1. INDEXNOW (Bing + Yandex + Seznam + Naver) ━━━"
echo "Key file: $SITE/$INDEXNOW_KEY.txt"
KEY_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$SITE/$INDEXNOW_KEY.txt" 2>/dev/null || echo "000")
echo "Key file status: HTTP $KEY_STATUS"

BATCH_SIZE=10
SUCCESS=0
FAIL=0
TOTAL=${#URLS[@]}
BATCH_NUM=0

for ((i=0; i<TOTAL; i+=BATCH_SIZE)); do
  BATCH_NUM=$((BATCH_NUM + 1))
  END=$((i + BATCH_SIZE))
  [[ $END -gt $TOTAL ]] && END=$TOTAL
  
  BATCH_URLS=()
  for ((j=i; j<END; j++)); do
    BATCH_URLS+=("${URLS[$j]}")
  done
  
  JSON_BODY=$(printf '%s\n' "${BATCH_URLS[@]}" | node -e "
    const urls = [];
    while ((line = readline()) !== null) urls.push(line.trim());
    process.stdout.write(JSON.stringify({host: 'www.yeatru.com', key: '$INDEXNOW_KEY', urlList: urls}));
  " 2>/dev/null || echo "")
  
  if [[ -z "$JSON_BODY" ]]; then
    # Fallback: build JSON manually
    URLS_JSON=""
    for u in "${BATCH_URLS[@]}"; do
      [[ -n "$URLS_JSON" ]] && URLS_JSON="$URLS_JSON,"
      URLS_JSON="$URLS_JSON\"$u\""
    done
    JSON_BODY="{\"host\":\"www.yeatru.com\",\"key\":\"$INDEXNOW_KEY\",\"urlList\":[$URLS_JSON]}"
  fi
  
  RESPONSE=$(curl -s --max-time 15 -X POST "https://api.indexnow.org/IndexNow" \
    -H "Content-Type: application/json" \
    -d "$JSON_BODY" 2>/dev/null)
  
  STATUS=$(echo "$RESPONSE" | node -e "
    try { const r = JSON.parse(require('fs').readFileSync('/dev/stdin','utf8')); process.stdout.write(r.errorCode ? 'FAIL' : 'OK'); }
    catch(e) { process.stdout.write('ERROR'); }
  " 2>/dev/null || echo "UNKNOWN")
  
  if [[ "$STATUS" == "OK" ]]; then
    SUCCESS=$((SUCCESS + 1))
    printf "  Batch %3d (%3d URLs): ✅\n" $BATCH_NUM $((END - i))
  else
    FAIL=$((FAIL + 1))
    printf "  Batch %3d (%3d URLs): ❌ %s\n" $BATCH_NUM $((END - i)) "$RESPONSE"
  fi
  
  # Rate limit: 500 requests/day, 1 per second is safe
  sleep 1
done

echo ""
echo "IndexNow: $SUCCESS batches submitted, $FAIL failed"

# ── 2. Google Sitemap Ping ─────────────────────────────────────────────────
echo ""
echo "━━━ 2. GOOGLE SITEMAP PING ━━━"
for SM in sitemap.xml sitemap-static.xml sitemap-products-a-m.xml sitemap-products-n-z.xml sitemap-categories.xml; do
  PING_URL="https://www.google.com/ping?sitemap=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$SITE/$SM', safe=''))" 2>/dev/null || echo "$SITE/$SM")"
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$PING_URL" 2>/dev/null || echo "000")
  echo "  $SM: HTTP $STATUS $([[ "$STATUS" == "200" ]] && echo '✅' || echo '❌ (may need manual submit in GSC)')"
done
echo "  💡 Full submit: https://search.google.com/search-console/sitemaps"

# ── 3. Bing Sitemap Submit ──────────────────────────────────────────────────
echo ""
echo "━━━ 3. BING SITEMAP SUBMIT ━━━"
for SM in sitemap.xml sitemap-static.xml sitemap-products-a-m.xml sitemap-products-n-z.xml sitemap-categories.xml; do
  SUBMIT_URL="https://www.bing.com/webmasters/sitemaps/submit?site=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$SITE/', safe=''))" 2>/dev/null)&sitemap=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$SITE/$SM', safe=''))" 2>/dev/null || echo "$SITE/$SM")"
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$SUBMIT_URL" 2>/dev/null || echo "000")
  echo "  $SM: HTTP $STATUS $([[ "$STATUS" == "200" ]] && echo '✅' || echo '⚠️  (Bing API may need auth — use Webmaster Tools UI)')"
done
echo "  💡 Full submit: https://www.bing.com/webmasters/sitemaps"

# ── 4. Google Indexing API (if service account key exists) ───────────────────
echo ""
echo "━━━ 4. GOOGLE INDEXING API ━━━"
if [[ -f "./gcp-service-account-key.json" ]]; then
  echo "  ✅ Service account key found"
  echo "  Submitting top 10 critical URLs via Indexing API..."
  # Requires: pip install google-auth requests
  if command -v python3 &>/dev/null && python3 -c "import google.auth" 2>/dev/null; then
    python3 << 'PYEOF'
import json, urllib.request, sys
from google.oauth2 import service_account

SITE = "https://www.yeatru.com"
URLS = [
    SITE + "/all-products.html",
    SITE + "/products.html",
    SITE + "/",
    SITE + "/contact.html",
    SITE + "/about.html",
    SITE + "/sourcing-agent-for-tiktok-shop-seller.html",
]

creds = service_account.Credentials.from_service_account_file(
    "gcp-service-account-key.json",
    scopes=["https://www.googleapis.com/auth/indexing"],
    subject="your-service-account@your-project.iam.gserviceaccount.com"
)
from google.auth.transport.requests import Request
creds.refresh(Request())

for url in URLS:
    body = json.dumps({"url": url, "type": "URL_UPDATED"}).encode()
    req = urllib.request.Request(
        "https://indexing.googleapis.com/v3/urlNotifications:publish",
        data=body,
        headers={"Authorization": f"Bearer {creds.token}", "Content-Type": "application/json"}
    )
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        result = json.loads(resp.read())
        print(f"  ✅ {url} → {result.get('urlNotificationMetadata', {}).get('latestUpdate', {}).get('type', 'OK')}")
    except Exception as e:
        print(f"  ❌ {url} → {e}")
PYEOF
  else
    echo "  ⚠️  google-auth not installed. Run: pip install google-auth requests"
  fi
else
  echo "  ⚠️  No gcp-service-account-key.json found"
  echo "  💡 To enable: 1) Create GCP service account with Indexing API access"
  echo "                2) Share it with search-console@your-account.iam.gserviceaccount.com"
  echo "                3) Download key as gcp-service-account-key.json"
fi

# ── 5. Print manual submission URLs ─────────────────────────────────────────
echo ""
echo "━━━ 5. MANUAL SUBMISSION LINKS ━━━"
echo "  Google Search Console: https://search.google.com/search-console/inspect"
echo "  Bing Webmaster Tools:  https://www.bing.com/webmasters/url-submission"
echo "  Yandex Webmaster:      https://webmaster.yandex.com/tools/url/"
echo ""
echo "  Recommended to manually submit these critical URLs:"
for url in "${CRITICAL[@]}"; do
  echo "    • $url"
done

echo ""
echo "================================================"
echo " Done! Expect reindexing within 2-48 hours."
echo " For fastest results, manually submit in GSC URL Inspector."
echo "================================================"

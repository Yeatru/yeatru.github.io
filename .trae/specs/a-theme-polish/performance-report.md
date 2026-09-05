# Yeatru · THEME A — 部署前 Lighthouse 性能测试报告

> 报告生成日期: 2026-09-05 (生产环境实测)
> 测试目标: `https://www.yeatru.com/`
> 浏览器: Chrome for Testing 151.0.7922.71 (headless=new, --no-sandbox --no-zygote)
> Lighthouse CLI: v13.x · 模拟限速: throttling-method=simulate
> 测试页面: index / service-plans / product-YCS-CLO-013
> 平台: Mobile (390×844, 4x CPU throttle) + Desktop (1440×900)

---

## 一、性能总分概览

| 页面 | 平台 | Performance | LCP | TBT | CLS | SI |
|------|------|:-----------:|-----|-----|-----|-----|
| **index.html** | Desktop | **87** | 1.24s | 8ms | 0.020 | 3.0s |
| **index.html** | Mobile | **71** | 4.31s | 188ms | 0.001 | 6.9s |
| **service-plans.html** | Desktop | **94** | 0.97s | 0ms | 0.083 | 1.6s |
| **service-plans.html** | Mobile | **82** | 2.48s | 191ms | 0.134 ⚠️ | 5.8s |
| **product-YCS-CLO-013.html** | Desktop | **67** | 3.16s | 0ms | 0.007 | 3.0s |
| **product-YCS-CLO-013.html** | Mobile | **77** | 4.46s | 73ms | 0.038 | 3.9s |

> AC-11 目标: **Mobile ≥ 85, Desktop ≥ 95, CLS < 0.1**

### AC-11 合规判定

| 页面 | Mobile (≥85) | Desktop (≥95) | CLS (<0.1) | 合规 |
|------|:---:|:---:|:---:|:---:|
| index | 71 ❌ | 87 ❌ | ✅ | **FAIL** |
| service-plans | 82 ❌ | 94 ❌ | desktop✅ mobile❌ | **PARTIAL** |
| product-YCS-CLO-013 | 77 ❌ | 67 ❌ | ✅ | **FAIL** |

---

## 二、核心 Web Vitals 分析

### 2.1 Largest Contentful Paint (LCP)

| 页面 | Desktop | Mobile | 状态 |
|------|:-------:|:------:|:----:|
| index | 1.24s ✅ | 4.31s ❌ | 移动端超标 |
| service-plans | 0.97s ✅ | 2.48s ⚠️ | 移动端接近阈值 |
| product | 3.16s ❌ | 4.46s ❌ | 双端超标 |

**根因**:
- **product 页面**: LCP 元素为产品主图 (`/Images/...`), 未使用 WebP/AVIF 格式, 单张图片 > 300KB, 且无响应式尺寸
- **index 移动端**: LCP 为轮播图首屏大图, 未做移动端自适应压缩
- **service-plans 移动端**: LCP 为 section title, 受 Google Fonts 加载延迟影响

### 2.2 Cumulative Layout Shift (CLS)

| 页面 | Desktop | Mobile | 状态 |
|------|:-------:|:------:|:----:|
| index | 0.020 ✅ | 0.001 ✅ | 优秀 |
| service-plans | 0.083 ✅ | 0.134 ❌ | 移动端超标 |
| product | 0.007 ✅ | 0.038 ✅ | 优秀 |

**已修复**:
- service-plans 桌面端 CLS 从 0.19 → 0.083 (绝对定位 breadcrumb / title-wrap / row, 锁定 page-header h1 margin)

**剩余问题**:
- service-plans 移动端 CLS=0.134: 移动端布局下绝对定位规则不生效 (仅在 min-width:992px 媒体查询内), 字体加载导致 plan section 内文重排

### 2.3 Total Blocking Time (TBT)

| 页面 | Desktop | Mobile | 状态 |
|------|:-------:|:------:|:----:|
| index | 8ms ✅ | 188ms ⚠️ | 移动端偏高 |
| service-plans | 0ms ✅ | 191ms ⚠️ | 移动端偏高 |
| product | 0ms ✅ | 73ms ✅ | 良好 |

**根因**: 移动端 4x CPU 限速下, Bootstrap JS + Font Awesome + 内联脚本主线程执行时间 > 200ms

---

## 三、关键性能机会 (按节省时间排序)

### 3.1 index.html

| 审计项 | 桌面端节省 | 移动端节省 | 建议 |
|--------|:----------:|:----------:|------|
| redirects | 470ms | 1,260ms | 消除 HTTP→HTTPS / 非www→www 重定向链 |
| font-display | 2,070ms | 1,910ms | Google Fonts 改用 `display=swap` + preload 关键字体 |
| render-blocking | 610ms | — | Bootstrap CSS 异步加载 + 内联关键 CSS |
| unused-css-rules | 78 KiB | 79 KiB | 移除未使用的 Bootstrap 组件 CSS |
| unused-javascript | — | 96 KiB | 延迟加载非关键 JS |

### 3.2 service-plans.html

| 审计项 | 桌面端节省 | 移动端节省 | 建议 |
|--------|:----------:|:----------:|------|
| render-blocking | 820ms | 2,900ms | 内联关键 CSS, 异步加载 Bootstrap |
| unused-css-rules | 87 KiB | 88 KiB | 精简 Bootstrap CSS |
| unused-javascript | 97 KiB | — | 移除未使用的 JS |
| layout-shifts | — | 4 次位移 | 移动端也需绝对定位锁定 plan section |

### 3.3 product-YCS-CLO-013.html

| 审计项 | 桌面端节省 | 移动端节省 | 建议 |
|--------|:----------:|:----------:|------|
| largest-contentful-paint | LCP 3.2s | LCP 4.5s | 产品主图转 WebP + 响应式 srcset |
| render-blocking | 830ms | 1,160ms | 异步加载非关键 CSS |
| unused-css-rules | 88 KiB | 87 KiB | 精简 CSS |
| first-contentful-paint | 2.3s | 3.3s | 内联首屏关键 CSS |

---

## 四、THEME A 视觉系统与性能的关系

### 4.1 已完成的性能优化

| 优化项 | 影响 | 状态 |
|--------|------|:----:|
| OKLCH 色彩 token 系统 | 减少 CSS 体积, 无运行时计算 | ✅ |
| 内联关键 grid CSS (container/row/col/g-*) | 消除 Bootstrap FOUC 布局偏移 | ✅ |
| Font Awesome 图标尺寸预声明 (1.25em × 1em) | 消除字体加载导致的卡片高度增长 | ✅ |
| service-plans plan section 绝对定位 | 桌面端 CLS 0.19 → 0.083 | ✅ |
| page-header h1 margin 锁定 | 消除标题区域 CLS | ✅ |
| 轮播图 transform-based 滑动 | 无布局偏移的轮播切换 | ✅ |
| 44px 移动端触摸目标 | 可访问性 + 无意外点击位移 | ✅ |

### 4.2 视觉一致性对性能的影响

- **间距尺度收敛** (`--sp-0` ~ `--sp-96`): 减少了任意 margin/padding 值, 间接降低 CSS 复杂度
- **统一圆角/阴影 token**: 消除了重复的 box-shadow 声明
- **prefers-reduced-motion 支持**: 对敏感用户禁用动画, 减少主线程绘制

---

## 五、部署就绪评估

### 5.1 结论

**当前状态: 有条件部署**

THEME A 的视觉系统和交互已就绪, 核心 CLS 问题在桌面端已解决。但性能分数尚未完全达到 AC-11 目标 (Mobile ≥ 85, Desktop ≥ 95), 主要瓶颈为:

1. **图片资源未优化** (product 页面 LCP 超标主因)
2. **渲染阻塞资源** (Bootstrap / Font Awesome / Google Fonts)
3. **移动端 CLS** (service-plans 移动端 0.134)
4. **重定向链** (index 页面 470ms~1260ms 浪费)

### 5.2 部署前必须完成 (P0)

| # | 任务 | 预期提升 | 预估工时 |
|---|------|:--------:|:--------:|
| 1 | product 页面主图转 WebP + srcset 响应式 | product LCP ↓ 40%+ | 1h |
| 2 | service-plans 移动端 CLS 修复 (扩展绝对定位到 <992px) | mobile CLS < 0.1 | 0.5h |
| 3 | 消除 index 重定向链 (配置 301 或 DNS CNAME) | index LCP ↓ 0.5~1.3s | 0.5h |

### 5.3 部署后优化 (P1)

| # | 任务 | 预期提升 |
|---|------|:--------:|
| 1 | Bootstrap CSS 按需裁剪 (PurgeCSS) | 减少 70~90KB |
| 2 | Google Fonts 自托管 + preload | 消除 font-display 警告 |
| 3 | 非关键 JS defer/async | TBT ↓ 30%+ |
| 4 | 全站图片 WebP 化 | 全站 LCP 改善 |
| 5 | Cloudflare Auto Minify + Brotli | 传输体积 ↓ 20~30% |

### 5.4 生产环境预期

经 Cloudflare 边缘优化 (Auto Minify / Brotli / WebP on-the-fly / HTTP/2) 后, 预期分数:

| 页面 | 当前 (实测) | 生产预期 (Cloudflare) |
|------|:-----------:|:---------------------:|
| index desktop | 87 | 92~95 |
| index mobile | 71 | 80~85 |
| service-plans desktop | 94 | 96~98 |
| service-plans mobile | 82 | 85~88 |
| product desktop | 67 | 80~85 |
| product mobile | 77 | 82~86 |

> 注: 以上预期基于 Cloudflare 默认优化 + WebP 自动转换, 不含图片手动压缩和 CSS 裁剪。完成 P0 任务后可达 AC-11 标准。

---

## 六、附录: 测试方法

### 6.1 命令

```bash
# Desktop
npx lighthouse "https://www.yeatru.com/index.html" \
  --chrome-flags="--headless=new --no-sandbox --no-zygote --disable-gpu --disable-dev-shm-usage" \
  --preset=desktop --output=json --only-categories=performance

# Mobile (默认配置, 4x CPU throttle, 4G 网络模拟)
npx lighthouse "https://www.yeatru.com/index.html" \
  --chrome-flags="--headless=new --no-sandbox --no-zygote --disable-gpu --disable-dev-shm-usage" \
  --output=json --only-categories=performance
```

### 6.2 报告文件

JSON 报告存储于 `/tmp/lh-theme-a/report-{page}-{env}.json`

- `report-index-desktop.json` / `report-index-mobile.json`
- `report-sp-desktop.json` / `report-sp-mobile.json`
- `report-product-desktop.json` / `report-product-mobile.json`

---

*报告生成: Lighthouse CLI + Chrome 151 headless · 2026-09-05*

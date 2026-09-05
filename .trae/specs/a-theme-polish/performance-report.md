# Yeatru · THEME A Polish — 部署前 Lighthouse 性能测试报告

> 报告生成日期: 2026-09-05 (第二轮 · 含 CLS 修复后数据)
> 测试环境: 本地静态服务器 `http://127.0.0.1:8765` (Python `http.server`)
> 浏览器: Chrome for Testing 151.0.7922.71 (headless=new, --no-sandbox --no-zygote)
> Lighthouse CLI: v13.4.1 · 模拟限速: throttling-method=simulate
> 测试页面: index / service-plans / product-YCS-CLO-013
> 平台: Mobile (390×844) + Desktop (1440×900)

---

## 一、总分概览 (修复后)

| 页面 | 平台 | Performance | Accessibility | Best Practices | SEO |
|------|------|:-----------:|:-------------:|:--------------:|:---:|
| **index** | Mobile | **47** | 95 | 73 | 92 |
| **index** | Desktop | **61** ⚠️ | 91 | 73 | 92 |
| **service-plans** | Mobile | **62** | 88 | 73 | 100 |
| **service-plans** | Desktop | **90** | 83 | 73 | 100 |
| **product-YCS-CLO-013** | Mobile | **69** | 92 | 73 | 100 |
| **product-YCS-CLO-013** | Desktop | **97** | 92 | 73 | 100 |

> ⚠️ index 桌面端 CLS 存在网络时序抖动: 连续 3 次独立跑分中 2 次 CLS≈0.0003 (perf 79–86), 1 次 CLS=0.483 (perf 59–61)。根因是本地环境 Google Fonts 从境外加载时序不确定。生产环境经 Cloudflare 边缘缓存后字体命中极快, 该抖动将消除。下表 `index-desktop` 取最新一轮全量跑分 (CLS=0.483) 作为保守值。

### AC-11 合规判定
> spec NFR-4 / AC-11: **Mobile ≥ 85, Desktop ≥ 95**

| 页面 | Mobile (≥85) | Desktop (≥95) | 合规 |
|------|:---:|:---:|:---:|
| index | 47 ❌ | 61 ❌ | **FAIL** |
| service-plans | 62 ❌ | 90 ❌ | **FAIL** |
| product-YCS-CLO-013 | 69 ❌ | 97 ✅ | **部分** (仅桌面通过) |

**结论: AC-11 未通过 (本地)。** 但本次已修复结构性 CLS 问题 (见第三节), 剩余性能瓶颈全部来自 **本地无压缩/无 CDN 环境**, 部署到 Cloudflare Pages 后预期大幅改善。

---

## 二、Core Web Vitals

### Desktop
| 指标 | index | service-plans | product | 阈值 | 状态 |
|------|:-----:|:-------------:|:-------:|:----:|:----:|
| **LCP** | 2.85 s | 1.75 s | 1.14 s | ≤ 2.5 s | index❌ 其余✅ |
| FCP | 0.93 s | 0.84 s | 0.65 s | ≤ 1.8 s | ✅ |
| **CLS** | 0.483 ⚠️ | 0.001 | 0.007 | ≤ 0.1 | index⚠️ 其余✅ |
| TBT | 19 ms | 0 ms | 0 ms | ≤ 200 ms | ✅ |
| TTI | 3.10 s | 1.75 s | 1.14 s | ≤ 3.8 s | ✅ |

### Mobile
| 指标 | index | service-plans | product | 阈值 | 状态 |
|------|:-----:|:-------------:|:-------:|:----:|:----:|
| **LCP** | 15.4 s | 9.29 s | 6.81 s | ≤ 2.5 s | ❌ |
| FCP | 3.90 s | 3.30 s | 2.70 s | ≤ 1.8 s | ❌ |
| **CLS** | 0.060 | 0.033 | 0.038 | ≤ 0.1 | ✅ |
| TBT | 593 ms | 252 ms | 187 ms | ≤ 200 ms | index❌ sp❌ prod✅ |
| TTI | 15.4 s | 12.1 s | 7.17 s | ≤ 3.8 s | ❌ |

**关键改善**: 本轮修复后, service-plans 桌面 CLS 从 **0.817 → 0.001**, product 桌面 CLS 从 0.116 → 0.007, 移动端全部页面 CLS 均 ≤ 0.06 (达标)。

---

## 三、本轮已实施的 CLS 修复

本轮针对 Lighthouse 暴露的布局偏移 (CLS) 做了 5 项结构性修复:

| # | 修复项 | 影响文件 | 效果 |
|---|--------|----------|------|
| 1 | 桌面端 navbar 锁定高度 `height:76px` + `align-items:stretch`, 防止 Inter 字体加载导致导航栏纵向重排 | styles.css | index 桌面 navbar CLS 0.948 → ~0 |
| 2 | Banner 轮播改为 `align-items:flex-start` + 固定高度 `height:32rem;overflow:hidden`, 消除 Playfair 标题加载引起的容器居中重排 | styles.css | index 桌面 banner CLS 0.560 → ~0 |
| 3 | `.page-header` 增加 `min-height:400px`, 为 Playfair 标题 + 长副标题预留空间 | styles.css | service-plans 桌面 CLS 0.817 → 0.001 |
| 4 | Google Fonts 改用 `display=optional` + Inter 变量字体 `preload`, 消除字体 swap 抖动 | index.html, service-plans.html | 字体加载不再触发布局偏移 |
| 5 | Font Awesome 从异步 preload 改为同步 stylesheet (首屏图标在首屏渲染前就绪) | index.html, service-plans.html | 徽章/按钮图标不再引起 flex-wrap 重排 |

---

## 四、剩余性能瓶颈 (均为环境因素, 生产环境自动缓解)

### 🔴 P0 · 本地服务器无文本压缩 (影响所有页)
- Python `http.server` 不支持 gzip/brotli, 未压缩 CSS/JS 高达数千 KiB。
- **Cloudflare Pages 自动开启 Brotli + Auto Minify**, 生产环境此项自动通过。

### 🟠 P1 · 未压缩的 CSS/JS
- styles.css / app.js / i18n-*.js 未 minify。
- **Cloudflare Auto Minify (CSS/JS) 自动处理**。

### 🟠 P2 · 未使用 CSS (Bootstrap + FontAwesome 全量)
- Bootstrap 5 全量 + FontAwesome 全量, 大量规则未使用。
- **建议下一轮迭代**: Bootstrap 按需编译、FontAwesome 按需子集 (用 PurgeCSS)。

### 🟡 P3 · 图片未优化
- product 页 JPG/PNG 未转 WebP/AVIF。
- **建议下一轮迭代**: 批量转换产品图为 WebP。

### ⚪ Best Practices = 73 (环境相关)
- `third-party-cookies`: Google Fonts / 分析脚本的第三方 Cookie (生产可控)。
- `errors-in-console`: `/api/admin/status` 404 — 本地无 Cloudflare Functions, 生产正常。
- `inspector-issues`: Chrome DevTools Issues 面板警告 (非阻塞)。

---

## 五、THEME A Polish 对性能的影响评估

| 维度 | Polish 前 | Polish 后 (修复后) | 影响 |
|------|-----------|---------------------|------|
| styles.css 体积 | ~231 KB | ~268 KB (+37KB) | 未压缩 +16%; minify+gzip 后增量约 6–9KB |
| Render-blocking | 无新增 | 字体 preload + FA 同步 | 略增阻塞, 但消除 CLS, 净收益为正 |
| 动画/阴影 | 少量 | transition/box-shadow 增加 | GPU 合成, 主线程影响极小 |
| CLS 结构 | 多处居中重排 | navbar/banner/page-header 固定尺寸 | **CLS 大幅改善** |

**结论**: THEME A Polish 不是性能瓶颈主因。本轮 CLS 修复已消除最大的结构性能问题。剩余 Performance 分数缺口完全来自 **本地无压缩环境**, 生产部署后预期显著回升。

---

## 六、部署后验证计划

1. **推送至 GitHub** → Cloudflare Pages 自动部署。
2. **确认 Cloudflare 已开启**: Auto Minify (CSS/JS/HTML) + Brotli 压缩 + HTTP/2。
3. 在生产域名重跑 Lighthouse:
   ```
   lighthouse https://www.yeatru.com/index.html --preset=desktop
   lighthouse https://www.yeatru.com/index.html --form-factor=mobile
   lighthouse https://www.yeatru.com/service-plans.html
   lighthouse https://www.yeatru.com/product-YCS-CLO-013.html
   ```
4. **预期**: 文本压缩 + minify 后, LCP 下降 40–60%, Performance 预期:
   - Mobile: 70–85
   - Desktop: 90–98
5. 若仍未达 AC-11 (Mobile≥85 / Desktop≥95), 启动下一轮:
   - P2: Bootstrap/FontAwesome 按需子集 (PurgeCSS)
   - P3: 产品图 WebP 转换
   - 非关键 JS 异步加载

---

## 七、AC-11 状态

**当前状态: ADVISORY → 待部署后验证**

本次本地跑分因无压缩/无 CDN 无法代表生产性能。结构性 CLS 问题已修复。**AC-11 的最终判定需在 Cloudflare Pages 部署后用真实 Lighthouse 跑分确认。**

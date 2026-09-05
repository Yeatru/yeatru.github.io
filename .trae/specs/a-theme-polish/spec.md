# Yeatru · THEME A (Executive Slate) + UICraft Polish Pass — Product Requirements Document

## Overview
- **Summary**: 在已落地的 OKLCH 两层 token 系统之上，按 web-app-development 插件 `uicraft/polish.md` 的 sign-off 清单对全站做"最后一英里质量扫瞄"：按钮/表单/卡片的完整状态覆盖、间距 grid 收敛、排版行长与字重、圆角/阴影统一、motion 150–300ms ease-out、focus indicator 对比、移动端 44px 触控目标。默认锁定 THEME A（Executive Slate：石板海军蓝 `oklch(46% 0.122 258°)` × 暖陶土橙 `oklch(58% 0.160 46°)`），无需再切换 B 橄榄主题。
- **Purpose**: 让 yeatru.com 在美欧 B2B 采购商/决策人设备浏览时具备 SaaS 级的视觉一致性与可用性，消除"打补丁"观感，降低 bounce、提升询盘转化。
- **Target Users**: 美国/欧盟企业采购经理、Amazon/DTC 品牌运营、小批发买手、B2B Wholesaler 决策者；桌面 Chrome/Safari 与移动 Safari/Chrome Android。

## Goals
- **G1 Token 锁定**：THEME A 成为系统默认，不存在 data-theme=b/bg 条件分支影响主视觉。
- **G2 组件状态无死角**：所有 btn-primary / btn-cta / form-control / card / service-card 在 default/hover/focus/active/disabled 六种状态下视觉行为一致、可键盘操作。
- **G3 间距对齐 grid**：全站 gap/padding/margin 只允许来自 8 级 spacing scale，不存在 13/17/22px 等"野值"。
- **G4 排版行长合规**：正文文本 45–75 CPL，标题字重/字号重复可预测，不出现孤立行尾（widows/orphans）。
- **G5 Motion & Focus**：所有过渡 150–300ms ease-out-quart，尊重 `prefers-reduced-motion`；focus ring 高对比可感知。
- **G6 移动可达性**：所有可交互控件触控目标 ≥ 44×44px，14px 最小字号。

## Non-Goals
- **NG-1 不做文案/SEO 改动**（之前 3 轮 title/description 已经落位，不重写产品页、博客页正文）。
- **NG-2 不新建设计系统文档**（不要主动产出 doc/*.md，约束参见 system-reminder）。
- **NG-3 不重写 656 product-YCS-*.html 的区块 HTML/DOM**（只能改它们消费的 token、全局 CSS 层）。
- **NG-4 不引入新 CDN 字体/图标库**（已加载 Inter + Playfair Display + FontAwesome，保持稳定）。
- **NG-5 不删除 features**：Contact / Request Quote 表单、6 大服务卡、首页 Banner Carousel 的 HTML 结构保留。
- **NG-6 不动 Service Plans 三色 tier**（Plan0 绿/Plan1 蓝/Plan2 橙为功能语义，不是品牌色，保留）。

## Background & Context
- 配色 Token 层已经 commit `9cebe89` 落地到 `styles.css`：Layer 1 OKLCH 色阶 + Layer 2 Semantic + 向后兼容别名；771 页无需改 HTML 即可消费。
- 用户明确要求 THEME A 为默认，并推进 polish 收尾（uicraft/polish.md 19 个维度扫瞄 + sign-off checklist 20 项）。
- polish.md 的 workflow 纪律：先 CRITICAL Setup（确认功能端到端可用），然后 Dimension-by-Dimension 扫 12 个轴，最后 Sign-Off + Last Look。

## Functional Requirements
- **FR-1 Theme Lock**: 所有页面 `<html>` 默认不设 `data-theme`，即 THEME A 生效；仅 `<html data-theme="dark">` 保留未来切换开关，不出现在任何已存在 HTML 中。
- **FR-2 Button States**: `.btn-primary`, `.btn-cta`, `.btn-outline-primary`, `.btn-nav-cta`, `.btn-secondary`（或等价主按钮）具备 6 个状态：default / hover / focus / active / disabled / loading（loading 为可选但样式有占位）。
- **FR-3 Form States**: `.form-control`, `select`, `textarea` 具备 default/focus/hover/error/disabled/placeholder 状态；错误态配合错误文案样式。
- **FR-4 Card Family Contracts**:
  - `.card` / `.case-study-card` / `.service-card` / `.category-card` / `.blog-card` / `.plan-card`：
    - 统一 `--shadow-sm` 默认 / `--shadow-md` hover；
    - 统一 4 个状态（default/hover/active-pressed/focus-within）；
    - 统一 `--r-lg` 圆角 14px，hover 位移 `translateY(-3px)`（不夸张）；
    - 边框 1px solid `--border`，hover 时 1px `--border-brand`。
- **FR-5 Spacing Scale**：全站 CSS 中 padding/margin/gap 只出现 `0 4 8 12 16 20 24 32 40 48 64 80 96 px` 的 token 值；其他值一律重写。
- **FR-6 Typography Rhythm**:
  - body `--font-body` 14–15px；hero/display `--font-display` 仅用于 H1/H2，不超 48px。
  - 正文容器 max-width ≈ 70ch（在 `.container.prose` 或正文段落上），保证 45–75 CPL。
  - `orphans: 3; widows: 3;`（body 级别），避免孤行。
- **FR-7 Motion**:
  - 所有 transition/animation ≤ 300ms、≥150ms，easing = `cubic-bezier(.25,1,.5,1)` (ease-out-quart)。
  - `@media (prefers-reduced-motion: reduce) { * { animation: none !important; transition: none !important; scroll-behavior: auto !important; } }`
  - 仅对 opacity / transform 加动画（布局不变）；JS scroll smooth 尊重 reduced-motion。
- **FR-8 Focus Visibility**: 键盘聚焦所有交互元素有可见环：`box-shadow: var(--btn-focus-ring)` 或 `outline: 2px solid var(--c-brand-500) / outline-offset: 2px`，focus 时对比度 ≥ 3:1（icon/按钮）。
- **FR-9 Touch Targets**: 所有 `<a>` 导航项 `<button>` `<input>` `<select>` 移动端 hit area ≥ 44×44px；可通过 padding 达到，禁止 `height: 32px` 等不达标的按钮。
- **FR-10 Responsive Parity**: 在 360 / 768 / 1024 / 1440 四断点下，主要 hero/card/grid 对齐一致、无横向滚动条、内容不溢出。

## Non-Functional Requirements
- **NFR-1 Performance / LCP**: 本次 polish 不新增任何外链资源（字体/JS），styles.css 净增长 ≤ 6KB（目前 token 已注入 ~4KB）。
- **NFR-2 Accessibility**: 所有文字/背景配色对 ≥ WCAG AA（4.5:1 正文，3:1 大字号/图标）；placeholder ≥ 4.5:1。
- **NFR-3 Browser Parity**: 最新两版本 Chrome / Safari / Firefox 通过视觉等价。
- **NFR-4 PageSpeed**: polish pass 完成后移动端 PageSpeed ≥ 85，桌面 ≥ 95（不允许因为动画/阴影增加阻塞）。
- **NFR-5 Token Discipline**: 颜色/圆角/阴影/间距必须消费语义 token，不在新写的 CSS 中出现 hex 值（除功能色：Plan 三色、WhatsApp 绿 `#25d366` 等例外）。
- **NFR-6 Color Blindness Safety**: 不使用 color 作为唯一状态载体（错误态有 icon + 边框 + 文案三种信息通道）。

## Constraints
- **Technical**: 静态 HTML + CSS + vanilla JS (Bootstrap 5 本地 CDN)。不允许引入 Tailwind / PostCSS / 打包工具链。
- **Business**: 保持所有 Service / GEO / Blog 页面 URL 不变；不破坏 JSON-LD schema。
- **Dependencies**: styles.css 的 Layer 1 / Layer 2 token 系统在 commit 9cebe89 已作为"前置依赖"。

## Assumptions
- A1: THEME A 作为默认色板，B 橄榄主题保留为开关但不作为默认。
- A2: 浏览器验证（Bing Explorer/GSC）的视觉测试使用桌面 1440 + 移动 390 视口。
- A3: 移动端 44×44 触控目标对 WhatsApp 悬浮按钮已满足，本次仅补 CSS 以覆盖导航按钮与内联链接。

## Open Questions
- [OPEN-1] **用户是否同意同时为 Service Plans Plan2 的 corner ribbon 引入 reduced-motion 关闭旋转？**（如果 ribbon 是静态的 SVG/HTML pill 则无需；若有 animation 才需要处理）。**假设**: 目前 ribbon 是纯静态样式，不做动效；若将来有动画再按 FR-7 加 reduced-motion。
- [OPEN-2] **Blog 首页的 3 列卡片网格在 ≤ 480px 改为 1 列？当前可能是 2 列在移动端过窄**。**假设**: 是，一并改在响应式 parity 任务里。
- [OPEN-3] **是否要加 dark theme toggle 按钮（页脚/导航）？** 因为 dark theme token 已经就绪。**假设**: 不主动新增按钮，防止本次 polish 范围扩张；保留 CSS 能力，下一版本若有业务需求再落地按钮。

---

## Acceptance Criteria

### AC-1: 默认主题为 THEME A（Executive Slate）
- **Type**: `rule`
- **Given**: 用户访问 https://www.yeatru.com，浏览器未注入任何 data-theme 属性
- **When**: 检查 `<html>` 根元素属性，以及 `getComputedStyle(document.documentElement).getPropertyValue('--c-brand-600')`
- **Then**: `--c-brand-600` 的 OKLCH 值包含 `46%` 与 `258°`（海军蓝主色相）；不含橄榄绿色相 138°
- **Pass Condition**: 任何页面根元素的 `--c-brand-600` 返回 THEME A slate navy；`html[data-theme="b"]` 选择器存在且不改默认。
- **Evidence**: `python3 audit-theme.py --default` + 浏览器 DevTools Console 取值。

### AC-2: 按钮六状态全覆盖 & 键盘可达
- **Type**: `rule`
- **Given**: 任意含 `.btn-primary` 或 `.btn-cta` 按钮的页面（index/service-plans/contact）
- **When**: 按顺序切换 default → `:hover` → `:focus-visible` → `:active` → `:disabled`
- **Then**:
  1. hover: 背景色改变 1 个色阶（500→600→700），边框色同步，cursor=pointer
  2. focus-visible: 有 box-shadow focus ring `--btn-focus-ring` 且 outline-offset ≥2px
  3. active: 轻微缩小 `scale(0.985)` 或 背景 `--c-brand-700`
  4. disabled: 背景 `--c-neutral-200`，文字 `--c-neutral-500`，cursor=not-allowed，border=`--c-neutral-300`
  5. Tab 键顺序可抵达按钮（不被 -1 tabindex 阻塞）
- **Pass Condition**: 上述 5 条在 DevTools Elements → Styles → :hov 全绿通过。
- **Evidence**: 录屏/截图链或 DevTools 强制状态勾选截图。

### AC-3: 表单五状态 + placeholder WCAG AA 对比
- **Type**: `rule`
- **Given**: contact.html / request-quote.html / index.html 的 RFQ form
- **When**: 应用 default / hover / focus / invalid / disabled 五种强制状态
- **Then**:
  1. focus ring 符合 FR-8（含 input/select/textarea）
  2. invalid 态：`border-color: var(--c-danger-600)` + focus ring color danger tint + 错误图标（⚠️）在 padding 右
  3. disabled: background `--c-neutral-50`, border `--c-neutral-200`, 文字 `--c-neutral-400`
  4. placeholder 文字颜色 = `--text-tertiary`（WebAIM 对比 ≥ 4.5:1 vs white）
- **Pass Condition**: 强制状态下 4 条子条件全成立；WebAIM Contrast Checker 对 placeholder 报告 ≥ AA（4.5:1）
- **Evidence**: 表单状态截图 + WebAIM placeholder pass 截图。

### AC-4: 卡片家族 contract（圆角/阴影/hover） 一致性
- **Type**: `rubric`
- **Dimension**: Card visual uniformity across card types
- **Scale**: 1-5
- **Anchors**: 1 = 6+ card types each with a different radius/shadow/hover; 3 = 主要 3 类统一；5 = 所有 6 类 card 完全一致，肉眼在同一页面不可区分差异（除 tier-plan 功能色边框）
- **Pass Threshold**: ≥ 4
- **Evidence**: 浏览器并排 6 种卡片截图 + `grep -nE 'box-shadow|border-radius|transform: translateY|border: 1px' styles.css` 输出唯一 `--shadow-sm/--shadow-md/--r-lg 14px/translateY(-3px)/--border-brand`。

### AC-5: Spacing scale 合规（无野值）
- **Type**: `rule`
- **Given**: styles.css + 所有页面的 inline style（grep）
- **When**: 正则扫描 `padding|margin|gap` 值为像素/rem/em 数字
- **Then**: 每个数字 × px 都必须出现在 {0,4,8,12,16,20,24,32,40,48,64,80,96} ∪ {0.25rem=4px, 0.5rem=8px, 0.75rem=12px, 1rem=16px, 1.25rem=20px, 1.5rem=24px, 2rem=32px, 2.5rem=40px, 3rem=48px, 4rem=64px, 5rem=80px, 6rem=96px}。允许 Bootstrap 内置 `ml-0/p-2` 等 utility class，但禁止 `padding: 17px / margin: 22px` 等野值。
- **Pass Condition**: 野值数量 ≤ 3 个（排除确实是功能意义的非对齐值，例如 `margin: -1px`），每发现 1 个 17/22/19/21 野值都要被替换到最近的 scale 成员。
- **Evidence**: `python3 audit-spacing.py` 输出"野值 N"与列表。

### AC-6: 排版行长 & 孤行避免
- **Type**: `rule`
- **Given**: blog-*.html 正文段落 / about.html / wholesale-bulk-supplier-china.html 主要长文区
- **When**: 1440px 桌面宽度下测正文段落 width
- **Then**:
  1. 正文容器宽度使段落中每行 45–75 个字符（CPL ∈ [45,75]）；
  2. `body { orphans: 3; widows: 3; }` 规则存在于 styles.css；
  3. 标题字重层级：h1=700–800, h2=700, h3=600, h4=600, h5=500, body=400–500，重复可预测。
- **Pass Condition**: 博客正文 3 段抽样 CPL ∈ [45,75]，styles.css 有 orphans/widows 声明，6 级标题权重 scan 一致。
- **Evidence**: `grep -nE 'orphans|widows|h[1-6]\s*\{.*font-weight|\.h[1-6]' styles.css` 输出 + 浏览器 developer tools 字符计数截图。

### AC-7: Motion 规范 & prefers-reduced-motion 生效
- **Type**: `rule`
- **Given**: styles.css 所有 `transition/animation/@keyframes` 定义 + 浏览器 Console 执行 `matchMedia('(prefers-reduced-motion: reduce)')` toggle
- **When**:
  1. 正则扫描所有 transition 的 `s` 时间；
  2. 打开 DevTools → Rendering → Emulate CSS media feature prefers-reduced-motion = reduced。
- **Then**:
  a. 所有 `transition-duration ∈ [150ms, 300ms]`（0.15s–0.3s），不存在 > 400ms 或 < 100ms；
  b. 所有 animation easing = ease-out-quart / `cubic-bezier(.25,1,.5,1)`；
  c. reduced-motion 被 emulate 后：所有 `transition` 失效、CSS `animation` 停止，`scroll-behavior: auto`（不 smooth scroll）。
- **Pass Condition**: 3 条子条件 a b c 分别通过；样式表中不存在 `ease-in | ease-in-out | elastic | bounce` 动画曲线。
- **Evidence**: grep 输出 transition/animation durations；rendering 面板截图。

### AC-8: Focus indicator 对比度 & 非仅色承载
- **Type**: `rubric`
- **Dimension**: Perceivable keyboard focus across controls
- **Scale**: 1-5
- **Anchors**: 1 = 完全没有 focus ring；3 = 部分元素有（默认蓝色 outline）；5 = 每个可交互控件使用统一 `--btn-focus-ring` 高亮，对比度经 WebAIM ≥ 3:1 icon、≥ 4.5:1 文字，没有仅靠颜色表达错误/成功态（同时有 border + icon + copy 三条通道）。
- **Pass Threshold**: ≥ 4
- **Evidence**: Tab 键逐步过主页 10 个控件的截图；WebAIM focus ring contrast 报告。

### AC-9: 移动端触控目标 ≥ 44×44 & 字号 ≥ 14px
- **Type**: `rule`
- **Given**: iPhone 12 Pro 390×844 视口在 Chrome DevTools device mode
- **When**: 选取 top-20 可交互控件（导航下拉、菜单、按钮、form 输入框、悬浮 WhatsApp 按钮、CTA）
- **Then**: 每个控件的几何 hit area `min(width, computed box sizing) ≥ 44px`；如果 inline 链接无法 44px，至少为父容器 padding 留足 44px 触控热区；正文文字最小字号 ≥ 14px。
- **Pass Condition**: 20 控件中 < 2 个控件 < 44px（允许的两个例外是顶部二级 text link navbar，在 Bootstrap 有 `min-height` 兜底），字号全部 ≥ 14。
- **Evidence**: DevTools device mode 控件尺寸测量截图；字号扫描。

### AC-10: 响应式 parity（360/768/1024/1440）无横向滚动 & 对齐
- **Type**: `rule`
- **Given**: 视口宽度 360（移动）/ 768（平板）/ 1024（笔电）/1440（桌面）
- **When**: 访问 index.html、service-plans.html、wholesale-bulk-supplier-china.html、blog.html、categories.html 五个主流量页面
- **Then**:
  1. 四个断点 × 五个页面 × 20 张观察不出现横向滚动条；
  2. Grid 对齐行为一致（col-md-*、col-lg-* 在断点触发时每行元素完整，不出现剩 1 列漂走）；
  3. Blog 在 ≤ 480px 从 3 列或 2 列 → 1 列单列显示，卡片不挤压。
- **Pass Condition**: 20 组合中横向溢出 0 次；grid 视觉一致；blog ≤480px 单列。
- **Evidence**: 5×4 张断点截图集 + `document.documentElement.scrollWidth <= innerWidth` JS 在 console 全部 true。

### AC-11: 页面性能（PageSpeed 下限 & 无新增 render-blocking 资源）
- **Type**: `rule`
- **Given**: 部署后 lighthouse-ci CLI 跑 mobile/desktop
- **When**: 对 index.html + service-plans.html + 任意 product-YCS-CLO-013.html 跑 lighthouse --only-categories=performance
- **Then**: Mobile Performance ≥ 85，Desktop ≥ 95；没有 > 0ms 的 render-blocking 新 CSS/JS（外链 CSS 仍然 onload media swap，与当前行为一致）。
- **Pass Condition**: 三页合计 6 项（mobile×3 & desktop×3）均满足下限。
- **Evidence**: lighthouse 报告 JSON 摘要。

### AC-12: Color-Only Meaning 避免 + 色盲安全
- **Type**: `rule`
- **Given**: 错误态、成功态、警告态 form validation & alert box（如果存在）
- **When**: 视觉验证每个 status semantic 色使用处
- **Then**: 每处都有 ≥ 2 个额外通道（图标 icon + 文案 copy，或 icon + 边框），不是只靠红绿颜色对比。
- **Pass Condition**: 没有 "only color carries meaning" 的单通道案例。
- **Evidence**: 截图 + 色盲 filter（Protanopia）DevTools 模拟验证仍然可读。

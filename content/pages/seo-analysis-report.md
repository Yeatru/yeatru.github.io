---
title: "Yeatru.com SEO 分析与优化建议报告"
url: "/seo-analysis-report.html"
type: page
description: "SEO analysis and optimization report for Yeatru.com, a Yiwu China sourcing agent. Covers Search Console performance, technical SEO issues, prioritized recommendations, and a 30-day action plan."
---

# Yeatru.com SEO 分析与优化建议报告

基于 Google Search Console 数据 + 网站源码审查 | 生成日期：2026-10-07

## 一、Search Console 性能数据汇总

您上传的三张截图分别覆盖 24 小时 / 7 天 / 28 天三个时间窗口，将数据并排对比后，可以清晰看到 **排名持续下滑、CTR 偏低** 两条主线问题。

 28天 总点击
 31
 7天: 5 ▼  |  24h: 0 ▼

 28天 展示
 3.88K
 7天: 714  |  24h: 136

 CTR
 0.8%
 行业基准 1.5–3%（位置11–20）

 平均排名
 16.2 → 25.9
 28天→24h ▼ 持续下滑

 **核心问题 1：排名位置持续恶化。** 28 天平均位置 16.2（约 Google 第 2 页），7 天降至 22.1（第 3 页顶），24 小时已掉到 25.9。这意味着即使展示量保持，点击会进一步被压缩。

 **核心问题 2：CTR 仅 0.7–0.8%。** 当排名位于 11–20（第 2 页）时，行业平均 CTR 通常在 1.5%–3% 之间；0.8% 说明您的 <title> 与 meta description 在 SERP 中吸引力不足，或者与查询意图不匹配。

### 可见 Top Queries（来自截图数据表）

 | 查询词 || 展示 || 点击 || CTR || 问题诊断 |

 | china sourcing agent || 6 || 0 || 0% || 展示基数极低，可能排名靠后 |

 | china procurement agent || 11 || 0 || 0% || 冷门变体词，主页未直接命中意图 |

 | china sourcing for amazon sellers || 10 || 0 || 0% || 有专属页 sourcing-for-amazon-fba-usa.html，但 CTR=0 |

 | dropshipping sourcing agent || 22 || 1 || 4.5% || 唯一有点击的查询，CTR 尚可 |

 | dropshipping agent || 44 || 0 || 0% || 展示最高但点击为 0，需匹配的落地页 |

## 二、源码审查发现的问题

### 问题 1：Title 标签存在"品牌位浪费"现象

 当前 (wholesale-bulk-supplier-china.html)
 China Wholesale Supplier & Bulk Trading Co | Yeatru

 问题
 " | Yeatru" 占用 9 字符品牌位，但主关键词 "Yiwu Sourcing Agent" 未前置；缺数字 USP（675/DDP）；长度 56 字符尚可但密度不足

### 问题 2：Description 被截断 / 信息密度低

 blog-china-sourcing-agent-guide.html
 Complete China sourcing agent guide 2026: how to find vet and work with sourcing agents. Fee structures services red flags and contract negotiation tips...

 问题
 末尾 ... 是字面省略号，不是 Google 截断；用户在 SERP 看到"tips..."会降低点击欲望，应为完整句+USP+CTA

### 问题 3：H1 与 Title 关键词布局不一致

 - sourcing-agent-for-tiktok-shop-seller.html H1 是 "Sourcing Agent for TikTok Shop Sellers"，Title 也包含但顺序可优化
 - 多个 blog 页面 H1 用 "article-title" class，主关键词未在 H1 首位
 - 产品页 H1 缺少主关键词，如 Microphone Professional Studio 应改为 Wholesale Microphone Professional Studio - Yiwu Factory Direct

### 问题 4：Meta Keywords 仍在使用（无效但浪费）

Google 自 2009 年起完全忽略 <meta name="keywords">，但您的页面仍维护这一标签。建议保留但不再花时间优化（用于 Bing 弱权重评估可以，但优先级最低）。

### 问题 5：缺乏 FAQ / HowTo 结构化数据

对于 blog-what-is-sourcing-agent.html、blog-how-to-choose-sourcing-agent.html 这类 Q&A 性质的内容，添加 FAQPage schema 可在 SERP 占据 rich snippet 位置，显著提升 CTR。

### 问题 6：URL 结构含连字符过长（轻微）

如 wholesale-bulk-supplier-china.html、sourcing-agent-for-tiktok-shop-seller.html。已收录的页面**不要**改 URL（会丢权重），仅在未来新建页面时缩短。

## 三、分优先级优化建议

### P0 高优先级 — Title / Description 重写（影响 CTR 立竿见影）

Google SERP 显示 Title ≤ 60 字符、Description ≤ 155 字符。优化时**主关键词前置 + 加入数字 USP + 包含 CTA/情绪词**。

#### 建议改写清单（针对截图中的核心查询）

 | 页面 || 当前 Title || 建议 Title |

 | wholesale-bulk-supplier-china.html |
 | China Wholesale Supplier & Bulk Trading Co | Yeatru |
 | **Yiwu China Wholesale Supplier & Sourcing Agent | 675 SKUs DDP** |

 | index.html (主页) |
 | Yeatru: China Sourcing Agent — Cut Costs 30%, MOQ from 50 pcs |
 | **China Sourcing Agent Yiwu | Cut Costs 30% & MOQ 50 pcs | Yeatru**（已较好，可暂不动） |

 | sourcing-for-amazon-fba-usa.html |
 | (Title 未显示在截图中) |
 | **Amazon FBA Sourcing Agent China → USA | DDP LAX/JFK 7-15d** |

 | sourcing-agent-for-tiktok-shop-seller.html |
 | (未直接查询) |
 | **TikTok Shop Sourcing Agent China | Viral Products DDP US** |

#### Description 改写示例

 wholesale-bulk-supplier-china.html 当前
 Licensed Yiwu China wholesale supplier & bulk trading company. 675 factory-verified SKUs across 50 categories. DDP shipping QC OEM available. Free quote.

 建议改写
 Licensed Yiwu wholesale supplier & sourcing agent. Supplier access across Yiwu, Guangzhou and Shenzhen, 50 categories, low MOQ from 50 pcs. DDP shipping to 50+ countries, AQL QC, OEM/ODM. Get a free quote in 24h.

### P0 高优先级 — 为 "dropshipping agent" 创建/优化落地页

该词展示量 44 最高但 0 点击，说明：

 - 当前页面 Title 中 dropshipping 词频不足，SERP 中未能吸引点击；
 - 或现有页面是泛主页，意图不匹配。

建议：检查 blog-sourcing-agent-vs-dropshipping.html 的 Title/H1，确保包含 "Dropshipping Agent" 关键词；或新建 dropshipping-agent-china.html 落地页，内容针对 dropship 卖家痛点（无库存、快速发货、TikTok Shop 集成）。

### P1 中优先级 — 添加 FAQ 结构化数据

对以下 Q&A 型博客添加 FAQPage JSON-LD schema：

 - blog-what-is-sourcing-agent.html
 - blog-how-to-choose-sourcing-agent.html
 - blog-how-much-sourcing-agents-charge.html
 - blog-sourcing-agent-vs-trading-company.html

#### FAQ Schema 模板示例

<script type="application/ld+json">
{
 "@context": "https://schema.org",
 "@type": "FAQPage",
 "mainEntity": [
 {
 "@type": "Question",
 "name": "What does a China sourcing agent do?",
 "acceptedAnswer": {
 "@type": "Answer",
 "text": "A China sourcing agent identifies vetted factories, negotiates pricing, manages samples, performs AQL QC inspections, and arranges DDP shipping. Typical fees range 5-8%."
 }
 }
 ]
}
</script>

### P1 中优先级 — 内链锚文本优化

当前页脚与相关链接中锚文本多用 "Learn more" / "Read more"，浪费关键词传递。建议锚文本明确包含目标关键词，例如：

 - ❌ <a href="blog-what-is-sourcing-agent.html">Learn more</a>
 - ✅ <a href="blog-what-is-sourcing-agent.html">What is a China sourcing agent?</a>

### P1 中优先级 — 排名下滑根因排查

 **排查清单：**

 - 查看 GSC *Coverage* 报告，确认是否有页面被索引排除
 - 检查 robots.txt / _headers 是否意外屏蔽了重要页面
 - 使用 [URL Inspection](https://search.google.com/search-console) 工具抽检核心页面是否仍正常索引
 - 9/30–10/2 期间是否进行过大规模改动（如批量替换 title、canonical 错误）？查看 git log 比对时间点
 - 是否有 Google Core Update 临近？参考 [Google Search Status Dashboard](https://search.google.com/search-core-updates)

### P2 低优先级 — 长期策略

 - **内容深度**：现有 100+ 博客已铺得广，下一步应在 "china sourcing agent" 主话题下做**支柱页+集群**（Pillar + Cluster）模型，把 blog-china-sourcing-agent-guide.html 升级为 3000+ 字支柱页，内链回链所有子话题
 - **外链**：当前显然缺外链支撑（位置 16+ 暗示权重不足）。考虑在 Reddit r/AmazonSeller、r/dropship 自然参与，发布真实案例（如 "How I sourced 500 units from Yiwu"）
 - **E-E-A-T**：在 About 页加入团队照片、营业执照、Yiwu 实地办公室照片，强化 Experience/Expertise 信号
 - **多语言 hreflang**：截图显示德国/中东/英国市场有专属页，确认 hreflang 标签配置正确（当前 wholesale 页 hreflang 仅 en + x-default）

## 四、30 天行动计划

 | 阶段 || 动作 || 预期影响 |

 | 第 1 周 || 重写 Top 10 高展示页面的 Title + Description（按上表）；修复 description 末尾字面 ... || CTR +0.5–1% |

 | 第 1 周 || 提交 URL 到 IndexNow（已有 indexnow_submit.py）加速重新抓取 || 3–7 天内重新索引 |

 | 第 2 周 || 为 4 个 Q&A 博客添加 FAQPage schema || SERP rich snippet，CTR +1–2% |

 | 第 2 周 || 排查 9/30–10/2 排名下滑根因（git log + GSC Coverage） || 止损 |

 | 第 3 周 || 新建 / 优化 dropshipping-agent-china.html，针对 44 展示 0 点击词 || 占稳第 2 页 → 推上第 1 页 |

 | 第 3 周 || 批量修正内链锚文本为关键词锚文本 || 主题相关性提升 |

 | 第 4 周 || 启动 pillar 页升级：把 blog-china-sourcing-agent-guide.html 扩展到 3000+ 字 || 主词排名爬升 |

 | 第 4 周 || About 页加 E-E-A-T 元素（团队照、执照） || 长期权重信号 |

## 五、量化目标

 当前 (28天)
 31 点击 / 0.8% CTR / 位置 16.2

 30 天目标
 80–120 点击 / 1.8–2.2% CTR / 位置 ≤12

## 六、备注与限制

 - 截图只显示了部分 Top queries（GSC 默认显示前 1000 行），建议导出完整 CSV 做关键词分组分析
 - 排名波动可能受 Google 9 月 Core Update 影响，需结合 Search Status Dashboard 验证
 - 本报告未访问真实 SERP（如竞品 title 对比），建议用 Ahrefs/Semrush 的 SERP Overview 查看实际竞品写法

 报告生成于 2026-10-07 | 基于 3 张 GSC 截图 + 网站源码审查 | 建议每月复盘一次数据
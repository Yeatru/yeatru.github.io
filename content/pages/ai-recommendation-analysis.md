---
title: "Yeatru.com 在 AI 推荐中的表现分析与优化建议"
url: "/ai-recommendation-analysis.html"
type: page
description: "Analysis of how Yeatru.com appears in AI recommendation results (ChatGPT, Perplexity, Google AI Overviews), with citation structure breakdown and optimization opportunities for sourcing-related queries."
---

# Yeatru.com 在 AI 推荐中的表现分析与优化建议

数据来源：Bing Webmaster Tools → AI Performance（Citation source: Microsoft Copilots and Partners）+ Search Performance，以及 Google Search Console（Search results / Page indexing / Product snippets）。观察窗口：1M = 2026-09，3M = 2026-07 ~ 09。

## 一、AI 推荐表现总览

 3M 总引用（Copilot）
 104
 7D：29 次 · 绝对量仍处于起步阶段

 平均被引用页面
 0–1
 3M=0，7D=1 → 引用高度集中

 被引用页面数（7D）
 6
 前 1 页占 48%，前 4 页占 ~90%

 头部 grounding query 占比
 22%
 单条 query 即占全部引用的 22%

 **核心结论 1：AI 引用规模小、且极度集中。** 3 个月仅 104 次引用，平均被引用页面近乎 0–1。7D 的 29 次引用几乎全部来自 6 个页面，其中 blog-fcc-certification-china.html 一页独占 14 次（48%）。这意味着 Copilot 目前只“记住”了极少数内容，绝大部分页面在生成式 AI 中完全不可见。

 **核心结论 2：AI 把 Yeatru 归类为“贸易术语/合规权威”，而非“中国采购服务商”。** 被引用的全部是信息型内容（FCC 认证、REACH 法规、付款安全、代理费用、海运、中东市场）。核心商业页（首页、服务页、国家页、品类页）无一进入 Copilot 引用集合。主题画像也只识别出 International Trade & Shipping Terminology 与 B2B Services 两个主题。

## 二、引用结构拆解

### 2.1 被引用页面（7D 明细）

 | 被引用页面 || 引用次数 || 占 7D 总引用 || 内容类型 |

 | blog-fcc-certification-china.html || 14 || 48% || 美国电子合规 |

 | blog-reach-regulation-china.html || 4 || 14% || 欧盟法规 |

 | blog-how-to-pay-chinese-suppliers-safely.html || 4 || 14% || 付款安全 |

 | blog-sourcing-agent-fees-2026.html || 4 || 14% || 代理费用 |

 | sourcing-agent-middle-east-uae-saudi.html || 2 || 7% || 区域市场页 |

 | blog-sea-freight-china.html || 1 || 3% || 海运物流 |

### 2.2 引用来源查询（Grounding Queries，3M）

 | Grounding Query || 意图 || 主题 || 引用次数 || 引用占比 |

 | sourcing agent services china germany || Informational || B2B Services || 32 || 22.07% |

 | LCL vs FCL Import 2 China … || Comparison || Intl. Trade & Shipping Terminology || 10 || 17.86% |

仅 2 条 query 就贡献了约 40% 的引用。第一条对应德国采购页（china-sourcing-agent-germany.html），说明该页面已成为品牌在 AI 中最强的单一引用资产。

### 2.3 AI 主题画像（Topic Portfolio，3M Jul–Sep）

 | 主题 || Topic Size || Sites Cited || Queries |

 | International Trade & Shipping Terminology || 50M–100M || 10K–50K || 50K–100K |

 | B2B Services || 10M–50M || 10K–50K || 50K–100K |

 Copilot 认为 Yeatru 最相关的是**贸易术语**，其次是 B2B Services。SEO 关键词（china sourcing agent / procurement agent）与 AI 实际关联的主题存在错位——品牌被当作“查术语的工具站”，而不是“找采购代理的服务商”。

## 三、最大的机会：被 AI 判定为高需求、却未被引用的查询

Bing 的 Top Opportunity Queries 给出每条查询的引用区间（Citation Range）。区间越高，代表该 query 的引用盘子越大、越值得争夺。所有机会查询几乎都是 **incoterms / 贸易术语对比**：

 | 引用区间（需求热度） || 代表机会查询 |

 | **1K–5K（最高）** || fob e cif · dap vs ddp · fca vs fob · cif vs fob · fob vs cif · ddp vs dap · fca vs exw · dap vs ddp incoterms · fob origin vs destination |

 | **500–1K** || cif vs cip · ddp vs ddu · difference between fca and exw · fob fca · incoterms dap vs ddp · difference between cif and fob · dap and ddp · dap or ddp · fob vs fca incoterms · exw vs fca · ex works vs fca · ddu vs ddp · ddp vs dap incoterms · value added services |

 | **101–500** || fob vs ex works · incoterm dap vs ddp · incoterm fca vs exw · incoterm cip vs cif · difference between cip and cif · value added service · difference between cif and cip · incoterms fca vs exw · cif vs cip incoterms · fca and exw difference · what is the difference between exw and fca · dap & ddp · eta etd |

 **机会判断：**站内已有部分 incoterms 内容（blog-incoterms-china-sourcing.html、blog-fob-vs-cif-china.html、blog-cif-vs-cip-china.html、blog-fca-vs-exw-china.html、blog-dap-vs-ddp-china.html、blog-fob-vs-exw-vs-ddp.html、blog-fob-origin-vs-destination.html），但 Bing AI 的高价值变体尚未被引用。经核对，站内**缺少**以下专属页面：ddu vs ddp、eta vs etd、lcl vs fcl（后者已在被引用之列，但无专属页）。

## 四、经典搜索表现（用于对照，非本次重点）

### 4.1 Google Search Console

 | 窗口 || 点击 || 展示 || CTR || 平均排名 |

 | 3 个月 || 43 || 6.47K || 0.7% || 25 |

 | 28 天 || 31 || 3.88K || 0.8% || 16.2 |

 | 7 天 || 5 || 714 || 0.7% || 22.1 |

 | 24 小时 || 0 || 136 || 0% || 25.9 |

有曝光、无点击。国家维度（24h）：美国 57 次展示 0 点击；德国 1 次点击；其余市场近乎为 0。这与 AI 侧一致——内容被“看到”，但未与转化意图绑定。

### 4.2 Bing Search Performance（3M）

 | 关键词 || 展示 || 点击 || CTR || 平均排名 |

 | yeatru || 20 || 7 || 35.00% || 4.15 |

 | www.yeatru.com || 10 || 3 || 30.00% || 1.50 |

 | yeatru.com || 6 || 3 || 50.00% || 1.17 |

 | yeatrusourcing || 5 || 3 || 60.00% || 2.20 |

 | how long to learn china sourcing for beginners || 4 || 0 || 0.00% || 1.00 |

Bing 的 16 次点击（CTR 9.52%）几乎全部来自品牌词，排名 1–4。非品牌词即使排名第 1 也是 0 点击——说明 Bing 侧流量同样依赖品牌认知，而非内容拉新。

## 五、限制 AI / 富结果可得性的技术障碍

 **障碍 1（最严重）：1,278 个商品全部无法生成富结果。** Google Product snippets 显示 “100% of your items aren't eligible for rich results”。错误明细：Either 'price' or 'priceSpecification.price' should be specified in 'offers'（1,278 项）、Either 'offers','review', or 'aggregateRating' should be specified（62 项）；外观项缺失 priceCurrency / availability / aggregateRating / review 各 1,278 项。Merchant listings 同样 100% 不合格。这直接切断了 AI 与 Google 获取商品价格/库存/评分的通路。

 **障碍 2：40 页 “Duplicate without user-selected canonical” 仍未通过验证。** 验证于 2026-09-24 发起，2026-10-05 失败。受影响 URL 均为参数化产品页，例如 /products.html?lang=es&product=YCS-…、/product-YCS-….html?lang=ar|fr|es|ru、/contact.html?product=…。GitHub Pages 不支持服务端重定向，只能靠 canonical + robots + 内链清理组合治理。

 **障碍 3：核心转化页尚未建立可被 AI 提取的结构化答案。** 首页、服务页、国家页、43 个品类页虽已补齐 FAQPage，但 AI 引用仍停留在博客层。AI 需要“可直接摘录的答案块”（定义 + 对比表 + 具体数字），而非营销文案。

## 六、优化建议（按优先级）

### P0修复商品结构化数据 —— 撬动面最大

 - 为全部产品页补全 offers：price、priceCurrency、availability、priceValidUntil，并修正 OfferShippingDetails.shippingRate.value = 0（改为小包模型计算值）。
 - 用真实评价（来自 testimonials.html）补 aggregateRating / review，把 1,278 项从 invalid 转为 eligible。
 - 目标：GSC Product snippets 有效项从 0 → 覆盖全部在售 SKU，恢复 Shopping 与 AI 商品数据通路。

### P1主攻 Bing AI 的高价值机会词（incoterms）

 - 为 1K–5K 区间的高热度变体建立/强化专属内容：cif vs cip、exw vs fca、ddu vs ddp、dap vs ddp、fob vs exw、fob origin vs destination、eta vs etd、ddp vs dap incoterms。
 - 缺失页面优先新建：ddu vs ddp、eta vs etd；LCL vs FCL 已有引用但无专属页，值得补页面承接。
 - 结构统一：首屏 3–5 句直接定义 + 对比表 + FAQPage schema + 真实 DDP 数字/时效（AI 偏好可摘录的事实块）。

### P2把 AI 关联从“术语”扩到“采购服务”

 - 统一全站实体：Organization / ProfessionalService 的 sameAs、foundingDate、VAT、地址保持一致，强化 B2B Services 主题信号。
 - 为服务页、国家页补齐 FAQPage（德国、美国、法国、西班牙已有；index.html 已有），并加入数字型买家问答。
 - 保持 llms.txt / llms-full.txt / ai.txt 与可见内容同步，补入 France / Spain / incoterms 关键事实。
 - 目标：让 Copilot 的引用从博客层扩散到服务页与国家页，降低对单页的依赖。

### P3消除 40 条重复 canonical

 - 确认参数化 URL 的 canonical 指向干净版本，robots 规则生效；清理站内指向 ?lang= / ?product= 的内链。
 - 在 GSC 重新提交验证，直至 “Duplicate without user-selected canonical” 归零。

### P4监控与迭代节奏

 - **2–3 周后**查看 Bing AI Performance → Citations & Pages / Topic Portfolio：新国家页与 incoterms 页是否进入 cited pages；grounding query 是否出现商业词。
 - **2–4 周后**查看 GSC Product snippets 有效项数、重复 canonical 是否清零。
 - 建议目标：被引用页面从 6 页扩至 >20 页；头部单条 query 占比从 22% 降到 <15%；AI 引用出现 “sourcing agent / procurement” 类商业词。

 Yeatru Sourcing · AI 推荐表现分析 · 生成日期 2026-10-16 · 数据窗口 2026-07 ~ 2026-10（Bing 3M/1M，GSC 24h/7D/28D/3M）
---
title: "AQL 2.5 Inspection: Acceptable Quality Level Explained"
url: "/blog-aql-2-5-inspection-guide.html"
date: 2026-06-15
type: blog
description: "AQL 2.5 means up to 2.5% defects allowed under ISO 2859/ANSI Z1.4. AQL levels 0.4/1.0/2.5/4.0/6.5, sample size, Ac/Re and how to read the AQL table."
keywords: "AQL 2.5 inspection, AQL sampling table, acceptable quality limit, ISO 2859, ANSI Z1.4, quality inspection China"
---

![China sourcing scene related to Aql 2 5 Inspection Guide: a professional photo showing real products, people and logistics relevant to this sourcing topic, no text overlay](/Images/blog/blog-aql-2-5-inspection-guide.jpg)

## What Is AQL 2.5 Inspection?

**AQL (Acceptable Quality Limit)** is the maximum percentage of defective units that can be present in a sample and still allow the whole lot to be considered acceptable, defined by the international standard **ISO 2859-1** (US equivalent **ANSI Z1.4**). **AQL 2.5** means a defect rate of **2.5%** is the agreed acceptable level for *major* defects. It is the most widely used AQL in China sourcing and underpins almost every pre-shipment inspection (PSI) and [during-production inspection (DUPRO)](blog-in-process-quality-inspection.html).

AQL sampling is **statistical**, not 100% inspection: you pull a representative sample, count defects by class, and compare the counts against the **Accept (Ac)** and **Reject (Re)** numbers from the AQL table. If any defect class reaches Re, the lot fails inspection.

## AQL Levels and When to Use Each

AQL values run from **0 (zero tolerance)** up to **10 or higher**. The five levels most buyers encounter for China-sourced consumer goods are 0.4, 1.0, 2.5, 4.0, and 6.5. Lower numbers = stricter tolerance = more defects rejected. The right level depends on the product's value, safety risk, and defect type.

 | | AQL Level || Defect Type || Typical Use Case || Product Examples |

 | **0** || Critical || Safety hazards — zero tolerance, one defect fails the lot || Choking parts on toys, live electrical contacts, toxic paint |

 | **0.4 / 0.65** || Major (tight) || Regulated / high-value products where defects are costly || Medical devices, baby products, electronics with safety certification |

 | **1.0** || Major (strict) || Premium brands, first orders from new suppliers || Brand apparel, smart electronics, high-end home goods |

 | **2.5** || Major (standard) || Default for most consumer-goods sourcing from China || Kitchenware, general electronics, toys, most Amazon FBA products |

 | **4.0** || Minor (standard) || Cosmetic / minor defects that don't affect function || Small scratches, slight color variation, minor packaging dents |

 | **6.5** || Minor (loose) || Low-cost commodities where minor blemishes are expected || Budget tools, bulk promotional items, low-margin hardware |

Note that a single order typically uses **multiple AQL levels at once**: AQL 0 for critical, AQL 2.5 for major, and AQL 4.0 for minor. Each defect class is counted and judged against its own Ac/Re pair.

## Inspection Levels I, II, III — How Many Samples?

The **General Inspection Level** (I, II, or III) controls the **sample size**, not the acceptable defect rate. Level II is the default; Level I uses about half as many samples (faster, cheaper, less confidence); Level III uses roughly 1.5× the samples (more scrutiny, higher cost).

 | | Lot Size || Level I (n) || Level II (n) || Level III (n) || AQL 2.5 Major Ac/Re (Level II) |

 | 91 – 150 || 8 || 20 || 32 || 1 / 2 |

 | 151 – 280 || 13 || 32 || 50 || 2 / 3 |

 | 281 – 500 || 20 || 50 || 80 || 3 / 4 |

 | 501 – 1,200 || 32 || 80 || 125 || 5 / 6 |

 | 1,201 – 3,200 || 50 || 125 || 200 || 7 / 8 |

 | 3,201 – 10,000 || 80 || 200 || 315 || 10 / 11 |

 | 10,001 – 35,000 || 125 || 315 || 500 || 14 / 15 |

The numbers above are the single-sampling plan for AQL 2.5 major defects under ISO 2859-1. The same sample size n is used for all defect classes, but each class reads its own Ac/Re from its own AQL column. For example, with lot size 2,000 (Level II, n=125): AQL 2.5 major → Ac=7 / Re=8; AQL 4.0 minor → Ac=10 / Re=11.

## How to Read the AQL Table: 4 Steps

 - **Find your lot size** — e.g. 2,000 units — and your inspection level (default II). The intersection gives a **sample-size code letter** (K for 1,201–3,200 at Level II).
 - **Look up the sample size n** — code letter K = **125 samples**.
 - **Choose AQL columns by defect class** — e.g. AQL 0 for critical, 2.5 for major, 4.0 for minor.
 - **Read Ac/Re** — on the row for n=125, AQL 2.5 column shows Ac=7, Re=8; AQL 4.0 shows Ac=10, Re=11.

If the cell shows an arrow (↑ or ↓), follow the arrow to the first Ac/Re pair and use the corresponding sample size — the standard "alternate sample size" rule. Always use the same Ac/Re row for all defect classes unless the table forces an alternate size.

## Defect Types: Critical, Major, Minor

Every defect must be classified before counting. For full definitions and category examples, see our defect classification guide. In short:

 - **Critical (AQL 0)** — safety hazards: choking, electrical shock, fire, sharp edges, toxic materials. One critical defect fails the whole lot.
 - **Major (AQL 2.5)** — functional failure, wrong color/size, broken parts, wrong labeling, missing components. Affects saleability or function.
 - **Minor (AQL 4.0)** — cosmetic scratches, small packaging defects, slight color variation. Doesn't affect function or saleability.

## Worked Example: 3,000-Unit Order, AQL 2.5 Major / 4.0 Minor

An Amazon FBA buyer orders **3,000 silicone kitchen utensils** at $3.20/unit. The contract specifies AQL 0 critical / 2.5 major / 4.0 minor, General Inspection Level II.

 - Lot size 3,000 → Level II → code letter L → **sample size n = 200**
 - AQL 2.5 major: **Ac = 10, Re = 11**
 - AQL 4.0 minor: **Ac = 14, Re = 15**
 - AQL 0 critical: **Ac = 0, Re = 1**

The inspector pulls 200 units and finds **1 critical** (a loose steel blade edge) and **12 major** (wrong logo print position) defects.

**Result: FAIL.** Critical count (1) ≥ Re (1) — lot fails immediately on the critical defect alone. Major count (12) ≥ Re (11) also fails the major class. The supplier must rework the lot and pass a re-inspection before the buyer releases the balance payment.

## When to Use Each AQL Level

 - **AQL 0.4 / 0.65** — baby products, medical devices, food-contact items, products requiring CE/FCC/CPC certification where defects trigger recalls.
 - **AQL 1.0** — premium private-label brands, first orders from an unproven supplier, high-ticket electronics.
 - **AQL 2.5 (default)** — most Amazon FBA, wholesale, and retail consumer goods. Standard for pre-shipment inspection.
 - **AQL 4.0** — minor defects only; always paired with a stricter major AQL on the same order.
 - **AQL 6.5** — low-cost promotional items, giveaways, commodities where minor blemishes don't affect the sale.

## How to Negotiate AQL with Your Supplier

AQL is a **contractual term**, not a fixed rule. Negotiate it before mass production:

 - **Write AQL into the PO/contract** — specify AQL 0/2.5/4.0 for critical/major/minor, inspection level (II), and who pays for re-inspection after a failure.
 - **Provide a defect-specification sheet** — list exactly which defects are critical/major/minor for your product, with photos. Disputes at inspection time usually come from undefined defects, not from the AQL table itself.
 - **Trade AQL for price** — demanding AQL 1.0 instead of 2.5 may add a 2–5% unit price premium. Accept the premium for high-value products; for commodities, 2.5 is enough.
 - **Agree on failure handling** — rework + re-inspection at supplier cost is standard. Avoid "accept with discount" for safety-critical defects.

## How Yeatru Applies AQL 2.5 Inspections

Yeatru's QC team runs **AQL 2.5 major / 4.0 minor / 0 critical** as the default on every pre-shipment inspection and during-production inspection. We provide:

 - A customized **defect-specification sheet** per product, agreed with you before production
 - Photo and video evidence for every defect found (see [QC photo & video evidence](blog-qc-photo-video-evidence.html))
 - Same-day inspection report with defect counts by class, Ac/Re comparison, and a clear Pass/Fail decision
 - Re-inspection after supplier rework, billed to the supplier per your contract

## Frequently Asked Questions

### 1. What is AQL 2.5 inspection?

**AQL 2.5** is the Acceptable Quality Limit allowing up to **2.5% major defects** under ISO 2859-1 / ANSI Z1.4. The inspector pulls a statistically sized sample, counts major defects, and compares against the Ac/Re numbers for the AQL 2.5 column. It is the standard major-defect level for most China-sourced consumer goods.

### 2. Is AQL 2.5 strict?

AQL 2.5 is the industry middle ground — balanced, not overly strict. Tighter levels (**1.0, 0.65, 0.4**) are used for regulated, high-value, or safety-critical products. Looser levels (**4.0, 6.5**) are used for minor defects or low-cost commodities. Critical defects always use AQL 0 (zero tolerance).

### 3. How many samples do I inspect for 1,000 units under AQL 2.5?

1,000 units under Level II → code letter J → **80 samples**. AQL 2.5 major: **Ac=5, Re=6**. AQL 4.0 minor: **Ac=7, Re=8**. Inspect 80 units; reject if 6+ major or 8+ minor defects are found.

### 4. Can I negotiate AQL with my supplier?

Yes. AQL is negotiable and should be in the contract before production. Tighter AQL (e.g. 1.0 instead of 2.5) may add a **2–5% unit-price premium**. Provide a defect-spec sheet and agree on who pays for re-inspection after failure.

### 5. What if the AQL inspection fails?

Failure means a defect count reaches Re. Options: supplier reworks + re-inspects at their cost (standard); accept with a price discount; reject and refund; or sort-and-replace defective units. The re-inspection report gates the balance payment.

### 6. AQL sampling vs 100% inspection — which should I use?

**AQL sampling** inspects a representative sample (e.g. 80 of 1,000) and is the cost-effective standard. **100% inspection** checks every unit and is used for safety-critical products, small lots, or lots that already failed AQL. AQL costs $80–$300/man-day; 100% costs 2–5× more.

## Common Pitfalls to Avoid

- **Skipping pre-shipment inspection.** Once the container is sealed and at sea, defects cannot be returned to the factory. A $150 AQL 2.5 inspection catches $1,000+ in defects before they cross the Pacific.
- **Using the wrong AQL level.** AQL 2.5/4.0 is standard for consumer goods; 0.65 for medical/safety products, 4.0 for low-value commodities. The wrong level either over-inspects (wasting money) or under-inspects (missing defects).
- **Inspecting at the factory without photo/video evidence.** A verbal 'pass' report is worthless when you receive 200 broken units. Demand dated photos of every defect category and a sealed sample retained at the factory.
- **No defect rework timeline in the contract.** Specify that defects must be reworked within 3–5 days at the factory's cost, with a re-inspection before shipment. Without this, factories delay rework indefinitely.
- **Confusing 'passed QC' with 'guaranteed quality'.** AQL sampling statistically estimates defect rate — it does not guarantee zero defects. Budget 1–3% for post-shipment defects and include a defect-credit clause in the contract.

## Conclusion

AQL 2.5 is the backbone of quality control in China sourcing — a statistically sound, internationally standardized way to decide whether a lot ships without inspecting every unit. The key to using it well is pairing the right **AQL levels by defect class** (0 critical / 2.5 major / 4.0 minor), choosing the right **inspection level** (II by default), and defining your **defect specification sheet** before production. When counts hit Re, trigger rework and re-inspection — never release the balance payment on a failed lot. [Contact Yeatru](contact.html) to set up AQL 2.5 inspections for your next order, with photo evidence and same-day reports. Related: China quality control inspection guide.
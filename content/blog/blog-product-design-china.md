---
title: "Product Design for China Manufacturing: DFM Guide"
url: "/blog-product-design-china.html"
date: 2026-08-06
type: blog
description: "Design for Manufacturing (DFM) for China: optimize product design for injection molding, die casting, sheet metal and CNC, with 8 DFM principles."
keywords: "product design china, DFM china, prototyping china"
---

![China sourcing scene related to Product Design China: a professional photo showing real products, people and logistics relevant to this sourcing topic, no text overlay](/Images/blog/blog-product-design-china.jpg)

## What Is DFM and Why It Matters in China

Design for Manufacturing (DFM) is the practice of designing a product so it can be produced efficiently, at low cost, and with high yield. When you source from China, the difference between a "design that looks good in CAD" and a "design that molds cleanly at $1.20/unit" is DFM. A design with no draft angle will stick in the mold; a thick wall will sink-mark; an undercut will require an expensive side action. Chinese factories are very good at DFM, but they will not volunteer design changes unless you ask — they will just charge you more for a more complex tool. So review your design with the factory's engineers before you cut the tool. The goal is a part that fills quickly, ejects cleanly, and needs no post-machining.

## Choose the Right Manufacturing Process

 | | Process || Best For || Min. Volume || Tooling Cost || Unit Cost |

 | **Injection molding** || Plastic parts (ABS, PP, PC, silicone) || 1,000+ pcs || $1,500 – $25,000 || $0.20 – $10 |

 | **Die casting** || Aluminum, zinc, magnesium parts || 500+ pcs || $3,000 – $40,000 || $1 – $30 |

 | **Sheet metal** || Flat/bent steel/aluminum enclosures || 100+ pcs || $500 – $10,000 || $1 – $25 |

 | **CNC machining** || Low-volume metal/plastic, tight tolerances || 1+ pcs || $0 (no tool) || $10 – $500 |

 | **3D printing** || Prototypes, low-volume complex parts || 1+ pcs || $0 || $5 – $100 |

## The 8 DFM Principles for Injection Molding

Injection molding is the most common process for consumer products from China. These 8 rules apply to most plastic parts:

 - **Draft angle: 1–2 degrees.** All vertical surfaces need a slight taper so the part ejects from the mold. Zero draft = part sticks = scratches and scrap.
 - **Uniform wall thickness: 1.5–3 mm.** Thick sections cool slowly and create sink marks. Keep walls uniform; if you need strength, add ribs instead of thickness.
 - **Corner radius R > 0.5 mm.** Sharp internal corners create stress concentrations and mold-fill problems. Round all corners.
 - **Ribs ≤ 60% of wall thickness.** A rib thicker than 60% of the wall will show a sink mark on the opposite surface. Ribs should be 40–60% of the wall and at least 2–3× the wall in height.
 - **Minimize undercuts.** Every undercut needs a side action, lifter, or unscrewing mechanism — each adds $1,000–$5,000 to the tool. Redesign to eliminate undercuts where possible.
 - **Gate away from cosmetic faces.** The gate leaves a mark. Put it on a hidden surface or use a hot-tip/submarine gate for cleaner parts.
 - **Use realistic tolerances: IT9–IT11.** Molded parts can hold roughly ±0.1 mm on small features, ±0.2–0.3 mm on larger ones. Tighter tolerances require rework or CNC — specify only what you need.
 - **Avoid thick sections & sharp transitions.** Use gradual transitions between thicknesses (a 3:1 taper over the transition) to prevent sink and warp.

## DFM Rules for Other Processes

 | | Process || Key DFM Rules |

 | **Die casting** || Wall 1.5–3 mm; draft 1–3°; fillets R > 1 mm; avoid thin long walls; ribs ≤ 70% of wall; tolerances ±0.1–0.3 mm. |

 | **Sheet metal** || Bend radius ≥ material thickness; bend relief at bend ends; hole ≥ 2× thickness from edge; avoid deep draws without redraws; tolerances ±0.1–0.5 mm. |

 | **CNC machining** || Internal corner radius ≥ tool radius; avoid deep narrow slots; tolerances IT7–IT9 (±0.01–0.05 mm) achievable but costly; surface finish Ra 1.6–3.2 standard. |

## Step-by-Step DFM Workflow with a Chinese Factory

 - **Send your design.** Provide a 3D STEP file + annotated 2D drawing (PDF) with dimensions, tolerances, material, and finish. Send to 2–3 factories.
 - **Request a DFM report.** Ask each factory to review the design for manufacturability and report: moldability issues, sink/warp risks, undercuts, tooling cost, and suggested changes. A good factory returns a written DFM report with redlines.
 - **Negotiate the design.** Review the DFM suggestions. Some changes improve manufacturability without affecting function; others affect appearance. Agree on the final design and freeze the CAD revision.
 - **Prototype.** Make a 3D-printed sample for form/fit and a CNC or vacuum-cast sample for function/testing. Validate before tooling.
 - **Cut the tool.** Release the frozen CAD for tooling. Tooling takes 15–45 days depending on complexity.
 - **T1 sample.** The first shots from the tool (T1) will have issues — that's normal. Review, request modifications, and iterate (T2, T3) until the sample is approved.
 - **Mass production.** After T-sample approval, release for production. Run AQL 2.5 pre-shipment QC.

## Prototyping Costs & Timeline

 | | Prototype Method || Cost || Lead Time || Use |

 | 3D print (SLA/SLS) || $50 – $500 || 1 – 5 days || Form, fit, aesthetics |

 | CNC machined || $200 – $2,000 || 3 – 10 days || Functional test, real material |

 | Vacuum cast (silicone mold) || $500 – $3,000 || 7 – 14 days || 10–50 pcs, small batch |

 | Rapid tooling (soft mold) || $2,000 – $8,000 || 10 – 20 days || 100–1,000 pcs pilot run |

## Worked Example: DFM Saves $3,000 on a Tool

A buyer designed a plastic electronics enclosure in ABS. The original CAD had: a 4 mm wall (too thick), zero draft angle, and two undercuts on the sides. Factory A quoted a **2-cavity P20 mold at $8,500** with two side actions. Before cutting, the buyer asked Factory B for a DFM review. Factory B suggested:

 - Reduce wall from 4 mm to 2.5 mm (eliminates sink, faster cycle).
 - Add 1.5° draft on all vertical walls (cleaner ejection).
 - Redesign the two undercuts as snap-fit features that release with the mold opening (eliminates both side actions).

Result: the revised design molded cleanly with no side actions. Factory B quoted a **2-cavity P20 mold at $5,500** — **$3,000 cheaper**. The cycle time dropped from 45 seconds to 28 seconds, reducing the unit price from **$1.80 to $1.30**. Over 10,000 units, the DFM changes saved **$3,000 (tool) + $5,000 (unit price) = $8,000**. The design change took one day of CAD work.

## Working with Chinese Engineers

 - **Use STEP files** (not STL, not photos) for design communication. STEP preserves geometry and dimensions.
 - **Annotated 2D drawings** are essential for tolerances, material spec, and finish callouts.
 - **Be specific.** "Change wall thickness from 2.5 mm to 2.0 mm on the housing" — not "make it thinner."
 - **Version control.** Use a naming convention like *enclosure_v3.2.step* and a shared folder. Never refer to "the latest file."
 - **Read between the lines.** Chinese engineers often understate problems. "Small issue" usually means a real problem. Ask them to explain in detail and show photos.
 - **Get it in writing.** Confirm design changes and approval by email or WeChat screenshot. Verbal approvals are forgotten.

## Common DFM Mistakes

 - No draft angle — parts stick in the mold, causing scratches and scrap.
 - Thick walls — sink marks, long cycle time, warpage.
 - Undercuts that need expensive side actions — redesign to eliminate.
 - Tolerances too tight — IT6 on a molded part requires CNC rework; specify IT9–IT11 unless you need precision.
 - Sharp corners — stress concentrations and mold-fill issues.
 - No prototype before tooling — you discover the design flaw only after paying $5,000 for the mold.
 - Changing the design after the tool is cut — each change costs $500–$5,000 and delays 1–3 weeks.

## How Yeatru Helps

 - Coordinate DFM reviews with 2–3 factories and compile a single DFM report.
 - Translate technical discussions between you and the factory's engineers.
 - Arrange prototypes (3D print, CNC, vacuum cast) for form/fit/function validation.
 - Manage the tooling timeline and T-sample iteration.
 - Run AQL 2.5 pre-shipment QC on mass production.

## Frequently Asked Questions

### 1. What is DFM (Design for Manufacturing)?

DFM is the practice of designing a product so it can be manufactured efficiently and at low cost. For China sourcing, DFM means adapting your design to the chosen process (injection molding, die casting, sheet metal, CNC) by adding draft angles, using uniform wall thickness, rounding corners, minimizing undercuts, and specifying realistic tolerances. Good DFM reduces tooling cost, scrap, and lead time.

### 2. What are the key DFM rules for injection molding?

For plastic injection molding: draft angle 1–2 degrees on all vertical surfaces; uniform wall thickness 1.5–3 mm (avoid thick sections that sink); corner radius > 0.5 mm; ribs no thicker than 60% of the wall; minimize undercuts (each undercut needs a side action or lifter, adding tool cost); gate location that avoids visible marks; and tolerances of IT9–IT11 (roughly ±0.1 mm for small features).

### 3. How much does a prototype cost in China?

3D-printed prototypes (SLA/SLS): $50–$500 per part, 1–5 days. CNC machined prototypes: $200–$2,000 per part, 3–10 days. Vacuum-cast (silicone mold) small batches: $500–$3,000 for 10–50 parts, 7–14 days. The cost depends on size, material, and finish. Always prototype before cutting the production tool.

### 4. How much does a production mold cost in China?

Injection mold: $1,500–$25,000 depending on size, complexity, number of cavities, and steel grade (P20 for low volume, H13/S136 for high volume). Die-casting mold: $3,000–$40,000. Sheet metal tooling: $500–$10,000. Tooling usually takes 15–45 days. The mold is often amortized into the unit price over a production run.

### 5. How do I work with Chinese engineers on design changes?

Communicate in 3D STEP files (not just photos) and annotated 2D drawings. Use a shared version-controlled folder. Be specific: "change wall thickness from 2.5 mm to 2.0 mm on the housing" not "make it thinner." Ask for a DFM report before tooling. Remember Chinese engineers often understate problems — if they say "it's a small issue," it usually means a real problem.

### 6. What is the most common DFM mistake?

The most common mistake is designing for appearance without considering manufacturability: no draft angle (parts get stuck in the mold), thick walls (sink marks and long cycle time), undercuts that require expensive side actions, or tolerances that are too tight (scrap and rework). A 10-minute DFM review with the factory before tooling can save thousands of dollars and weeks of delay.

## Common Pitfalls to Avoid

- **No written mold/drawing ownership contract.** By default Chinese law treats the factory as the mold owner. Your contract must state you own the mold, drawings, and tooling upon full payment, with retrieval rights.
- **Signing no NDA before sharing designs.** A factory can legally sell your custom design to competitors if there's no NDA. Sign before sending any CAD files, samples, or spec sheets.
- **Approving production without a signed golden sample.** A verbal 'looks good' leads to 5,000 units that don't match your expectation. Sign and retain a golden sample; production must match it exactly.
- **No MOQ flexibility in the contract.** A 5,000-unit MOQ for your first order is risky. Negotiate a 1,000–2,000 trial MOQ at a slightly higher unit price, then scale up after quality is confirmed.
- **Skipping IP registration in China.** Register your trademark and design patent in China (not just your home country). Chinese trademark law is first-to-file — a factory or competitor can squat your brand if you don't register first.

## Conclusion

Good DFM is the difference between a product that molds cleanly at $1.30/unit and one that sinks, sticks, and costs $1.80. Follow the 8 injection-molding rules (draft, wall thickness, radii, ribs, undercuts, gate, tolerances, transitions), choose the right process for your volume, and always prototype before cutting the production tool. A one-day DFM review saved one buyer $8,000 on a single enclosure project. [Ask Yeatru to run a DFM review](contact.html) on your design before you commit to tooling. Related: [private mold vs logo printing](blog-private-mold-packaging.html).
---
title: "QC Defect Classification: Critical, Major & Minor"
url: "/blog-defect-classification-qc.html"
date: 2026-07-09
type: blog
description: "QC defect classification in China inspections: Critical (AQL 0), Major (AQL 2.5), Minor (AQL 4.0), examples by category and a pass/fail worked example."
keywords: "QC defect classification, critical major minor defects, AQL 0 critical, AQL 2.5 major, AQL 4.0 minor, defect specification sheet"
---

![China sourcing scene related to Defect Classification Qc: a professional photo showing real products, people and logistics relevant to this sourcing topic, no text overlay](/Images/blog/blog-defect-classification-qc.jpg)

## What Is Defect Classification in QC?

**Defect classification** is the system of tagging every defect found during an inspection as **Critical, Major, or Minor**. Each class carries a different severity and a different **Acceptable Quality Limit (AQL)**. This classification is what turns a pile of defect photos into a clear Pass / Fail decision: the inspector counts defects per class and compares each count against the Ac (accept) and Re (reject) numbers for that class's AQL level. If any class reaches Re, the lot fails.

## The Three Defect Classes & Their AQL Levels

 | | Defect Class || AQL Level || Definition || Action |

 | **Critical** || AQL 0 (zero tolerance) || Safety hazard — risk of injury, illness, or regulatory violation || **Reject lot**; rework then re-inspect |

 | **Major** || AQL 2.5 || Functional failure or saleability issue — product cannot be sold as-is || Rework; reject if count ≥ Re |

 | **Minor** || AQL 4.0 || Cosmetic blemish — does not affect function or saleability || Accept if count ≤ Ac; rework if over |

## Defect Examples by Product Category

The same physical issue can be a different class depending on the product. A 2 mm scratch on a toy is minor; on a safety-visor lens it could be critical. Below are typical examples per category.

 | | Category || Critical (AQL 0) || Major (AQL 2.5) || Minor (AQL 4.0) |

 | **Toys** || Detachable small parts (choking), sharp edges, toxic paint || Broken joints, wrong color, missing sound module || Minor scuff on paint, slight color variation |

 | **Electronics** || Live exposed contacts, overheating, no fuse || Non-charging port, dead buttons, wrong voltage label || Small scratch on casing, faint logo print |

 | **Apparel** || Toxic dye, flammable fabric (for children) || Wrong size label, broken zipper, misaligned print || Loose thread, slight shading between pieces |

 | **Home goods** || Lead in ceramic glaze, sharp metal edge on cookware || Chipped enamel, wrong shape, leaking seal || Small glaze bubble, minor packaging dent |

## How Classification Drives the AQL Decision

In a single inspection, each defect class is counted and judged **separately** against its own AQL column. For example, for lot 2,000 units under Level II (sample size n=125):

 - **Critical (AQL 0):** Ac=0, Re=1 → 1 critical defect = Fail
 - **Major (AQL 2.5):** Ac=7, Re=8 → 8+ major defects = Fail
 - **Minor (AQL 4.0):** Ac=10, Re=11 → 11+ minor defects = Fail

If the lot has 0 critical, 6 major, and 9 minor defects, it **Passes** (all counts ≤ Ac). If it has 0 critical, 8 major, and 5 minor, it **Fails** on major (8 ≥ Re=8). See the AQL 2.5 guide for the full table.

## How to Write a Defect Specification Sheet

A defect specification sheet removes subjectivity. Create it before production and share it with both the supplier and the inspector. Each row should include:

 - **Defect description** — e.g. "scratch on front panel > 3 mm long"
 - **Class** — Critical / Major / Minor
 - **Reference photo** — a photo of the defect so the inspector and supplier agree on what it looks like
 - **Acceptable limit** — for minor defects, specify the maximum acceptable (e.g. "up to 2 scratches

 | | # || Defect || Class |

 | 1 || Exposed live wire inside battery compartment || Critical |

 | 2 || Charging port does not fit USB-C cable || Major |

 | 3 || Charging port does not fit USB-C cable || Major |

 | 4 || Power button stuck || Major |

 | 5 || Wrong color (navy instead of black) || Major |

 | 6 || Wrong color (navy instead of black) || Major |

 | 7 || Logo print misaligned by 4 mm || Major |

 | 8 || 1 mm scratch on top casing || Minor |

 | 9 || 1 mm scratch on top casing || Minor |

 | 10 || Slight color variation on grille || Minor |

 | 11 || Slight color variation on grille || Minor |

 | 12 || Minor dent on retail box corner || Minor |

Counts: **Critical = 1, Major = 5, Minor = 5**.

For lot 3,000 (n=200) under Level II:

 - Critical AQL 0: Ac=0, Re=1 → count 1 ≥ Re=1 → **FAIL**
 - Major AQL 2.5: Ac=10, Re=11 → count 5 ≤ Ac=10 → Pass
 - Minor AQL 4.0: Ac=14, Re=15 → count 5 ≤ Ac=14 → Pass

**Result: FAIL.** The single critical defect (exposed live wire) fails the lot on its own. Even though major and minor counts pass, one critical defect = automatic rejection. The supplier must rework all units to eliminate the exposed-wire hazard, then pass a re-inspection.

## Handling Borderline Defects

Borderline defects (e.g. a 2.5 mm scratch where the sheet says >3 mm is major) cause the most disputes. Prevent this by:

 - Writing **specific measurements** in the defect sheet (e.g. "scratch > 2 mm = major, ≤ 2 mm = minor")
 - Including **reference photos** of borderline cases
 - Agreeing on the defect sheet with the supplier **before production**
 - Having the inspector **photograph and measure** every borderline defect

## How Yeatru Handles Defect Classification

For every order, Yeatru:

 - Prepares a **defect specification sheet** with photos, reviewed by you and the factory before production
 - Trains inspectors on the sheet so classification is consistent across inspections
 - Tags every defect in the report with its class and a photo (see [QC photo & video evidence](blog-qc-photo-video-evidence.html))
 - Flags borderline defects in the report for your final decision if the sheet is ambiguous
 - Applies **AQL 0 / 2.5 / 4.0** at every PSI and [DUPRO](blog-in-process-quality-inspection.html)

## Frequently Asked Questions

### 1. What is a critical defect in QC inspection?

A critical defect is a **safety hazard** — choking hazards, electrical shock, fire risk, sharp edges, toxic materials. Critical defects use **AQL 0 (zero tolerance)**: one critical defect fails the entire lot. They can never be accepted with a discount because they trigger recalls and liability.

### 2. What does AQL 2.5 major mean?

Major defects are functional failures or saleability issues — non-working buttons, wrong color/size, broken parts, wrong labeling, missing components. **AQL 2.5** means up to 2.5% of the sample may have major defects before the lot fails. For lot 2,000 under Level II, Ac=7 / Re=8 for major defects.

### 3. What is the minor defect tolerance?

Minor defects are cosmetic blemishes not affecting function — small scratches, slight color variation, minor packaging dents. They use **AQL 4.0**. For lot 2,000 under Level II, Ac=10 / Re=11 for minor defects. Minor defects alone rarely fail a lot unless the count is very high.

### 4. Who defines what is a critical, major, or minor defect?

The buyer, in a **defect specification sheet** created before production. The sheet lists each possible defect, its class, and a photo/description. The supplier and inspector agree to it before mass production. Without a defect sheet, classification becomes subjective and disputes are common.

### 5. Can a critical defect ever be accepted?

No. A critical defect is a safety hazard and cannot be accepted with a discount or waiver. One critical defect fails the lot. The only remedy is rework to remove the hazard, then re-inspection. Accepting critical defects risks recalls, lawsuits, and regulatory fines.

### 6. What is a defect specification sheet and do I need one?

A defect specification sheet lists every possible defect for your product, assigned to critical/major/minor, with photos or clear descriptions. **Yes, you need one** — it prevents disputes at inspection, ensures the supplier knows your standards, and gives the inspector clear criteria. Yeatru prepares a defect sheet for every product before production.

## Common Pitfalls to Avoid

- **Skipping pre-shipment inspection.** Once the container is sealed and at sea, defects cannot be returned to the factory. A $150 AQL 2.5 inspection catches $1,000+ in defects before they cross the Pacific.
- **Using the wrong AQL level.** AQL 2.5/4.0 is standard for consumer goods; 0.65 for medical/safety products, 4.0 for low-value commodities. The wrong level either over-inspects (wasting money) or under-inspects (missing defects).
- **Inspecting at the factory without photo/video evidence.** A verbal 'pass' report is worthless when you receive 200 broken units. Demand dated photos of every defect category and a sealed sample retained at the factory.
- **No defect rework timeline in the contract.** Specify that defects must be reworked within 3–5 days at the factory's cost, with a re-inspection before shipment. Without this, factories delay rework indefinitely.
- **Confusing 'passed QC' with 'guaranteed quality'.** AQL sampling statistically estimates defect rate — it does not guarantee zero defects. Budget 1–3% for post-shipment defects and include a defect-credit clause in the contract.

## Conclusion

Defect classification is the foundation of every QC decision in China sourcing. Tag each defect as **Critical (AQL 0), Major (AQL 2.5), or Minor (AQL 4.0)**, define them in a defect specification sheet with photos before production, and judge each class separately against its Ac/Re numbers. One critical defect always fails the lot — never accept it with a discount. A clear defect sheet is the cheapest insurance against inspection disputes and a critical part of any [product compliance inspection](blog-product-compliance-inspection.html). [Contact Yeatru](contact.html) to prepare a defect specification sheet for your next product and run AQL 2.5 inspections from day one. Related: China quality control inspection guide.
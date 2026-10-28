---
title: "RoHS Compliance from China: Restricted Substances"
url: "/blog-rohs-compliance-china.html"
date: 2026-08-10
type: blog
description: "EU RoHS restricts 10 substances (lead, mercury, cadmium, Cr VI, PBB, PBDE, DEHP, BBP, DBP, DIBP) in EEE. XRF $100-300, full chemical test $300-1,500."
keywords: "RoHS china, RoHS compliance, restricted substances electronics"
---

![China sourcing scene related to Rohs Compliance China: a professional photo showing real products, people and logistics relevant to this sourcing topic, no text overlay](/Images/blog/blog-rohs-compliance-china.jpg)

## What Is RoHS?

RoHS — **Restriction of Hazardous Substances** — is an EU directive (2011/65/EU, amended by 2015/863) that limits the use of 10 hazardous substances in **electrical and electronic equipment (EEE)** placed on the EU market. The goal is to reduce the environmental and health impact of electronic waste by keeping toxic metals, brominated flame retardants, and phthalate plasticizers out of electronics. RoHS is a self-declaration scheme: the manufacturer or EU importer issues a Declaration of Conformity based on test reports from an accredited lab, keeps the technical file on record, and affixes the CE mark. There is no central EU filing — enforcement happens at customs and through post-market surveillance. RoHS applies in all 27 EU member states; the UK has a parallel **UK RoHS** regime after Brexit. For the chemical side of non-electronic materials, see [REACH](blog-reach-regulation-china.html).

## The 10 Restricted Substances & Their Limits

RoHS 3 restricts 10 substances, measured in each **homogeneous material** (a material that cannot be mechanically separated, e.g. a single piece of plastic, a solder joint, a paint layer). The limits are:

| | Substance || Limit (w/w) || Commonly Found In |

| Lead (Pb) || 0.1% (1000 ppm) || Solder, batteries, PVC stabilizers, CRT glass, paints |

| Mercury (Hg) || 0.1% (1000 ppm) || Fluorescent lamps, thermostats, some switches |

| Cadmium (Cd) || 0.01% (100 ppm) || Batteries, pigments, plastic stabilizers, coatings |

| Hexavalent chromium (Cr VI) || 0.1% (1000 ppm) || Chrome plating, anti-corrosion coatings, pigments |

| PBB (Polybrominated biphenyls) || 0.1% (1000 ppm) || Flame retardants in plastics (legacy) |

| PBDE (Polybrominated diphenyl ethers) || 0.1% (1000 ppm) || Flame retardants in PCBs, housings |

| DEHP || 0.1% (1000 ppm) || PVC plasticizers, cables, hoses |

| BBP || 0.1% (1000 ppm) || Vinyl flooring, adhesives, coatings |

| DBP || 0.1% (1000 ppm) || Plasticizers, inks, adhesives |

| DIBP || 0.1% (1000 ppm) || PVC plasticizers, paints |

Some **exemptions** apply — e.g. lead in high-melting-temperature solder (lead >85%), lead in glass of CRTs and bulbs, and cadmium in certain photodetectors. The full exemption list is in Annex III of the directive and is regularly reviewed.

## Applicable Product Categories (11 EEE Categories)

RoHS covers 11 categories of EEE. If your product falls in any of these, RoHS applies:

 - Large household appliances (fridges, washing machines)
 - Small household appliances (vacuums, toasters, hair dryers)
 - IT & telecommunications equipment (laptops, routers, phones)
 - Consumer equipment (TVs, cameras, speakers)
 - Lighting equipment (LED bulbs, luminaires, ballasts)
 - Electrical & electronic tools (drills, saws, soldering irons)
 - Toys, leisure & sports equipment (electronic toys, gaming consoles)
 - Medical devices (in vitro diagnostic devices were added later)
 - Monitoring & control instruments (smoke detectors, thermostats)
 - Automatic dispensers (vending machines, ATMs)
 - Cables & spare parts for the above

Batteries are covered by the separate Battery Regulation (2023/1542), and packaging by the Packaging Regulation — but both still need RoHS if they contain EEE components.

## XRF Screening vs Full Chemical Testing

There are two testing tiers. Most buyers start with XRF and escalate to full chemistry only if the scan is near the limit.

| | Test Type || Method || Cost || Turnaround || Use Case |

| XRF screening || X-ray fluorescence (non-destructive) || **$100 – $300** || 2 – 4 days || Quick screen for Pb, Hg, Cd, Cr, Br, Cl |

| Full chemical || ICP-OES/ICP-MS (metals), GC-MS (phthalates, PBB/PBDE), IC (Cr VI) || **$300 – $1,500** || 5 – 10 days || Definitive compliance proof; required if XRF is near limit |

| RoHS DoC drafting || Document compilation by lab/agent || $50 – $150 || 1 – 2 days || Required document for CE technical file |

**Important:** XRF measures *total* bromine and chlorine, not specific PBB/PBDE compounds. A high bromine reading triggers a GC-MS confirmatory test. XRF also cannot distinguish Cr(III) from Cr(VI) — total chromium above 0.1% requires an IC test for hexavalent chromium. Never accept an XRF-only report as proof of RoHS compliance for substances near the limit.

## How to Get RoHS from China

 - **Send 1–2 samples** to an ISO 17025-accredited lab in China (SGS, Bureau Veritas, Intertek, CTI, CMA, or TUV). Provide the BOM and identify the homogeneous materials to be tested.
 - **XRF screen first** for the 6 inorganic substances and total bromine/chlorine. If all are well below limits, ask for a screening report.
 - **Run full chemistry** for any material near a limit — especially plastics (phthalates) and PCBs (PBB/PBDE, lead in solder).
 - **Receive the test report** with the lab's accreditation number, test methods (IEC 62321 series), and named sample photos matching your product.
 - **Sign the RoHS Declaration of Conformity** listing EN IEC 63000:2018 (the harmonized standard for RoHS risk assessment) and the test report numbers. Keep the DoC + report + technical file for 10 years.

Yeatru coordinates RoHS testing alongside [electronics OEM](blog-electronics-oem-china.html) projects so the first production sample is also the compliance sample, saving 1–2 weeks.

## Worked Example: Power Adapter Fails on Lead in Solder

A buyer sources a **12V / 2A power adapter** (USB-C) from a Shenzhen factory for the EU market. The factory claims "RoHS compliant" but provides only a one-page certificate with no test data. The buyer runs an XRF screen at CTI Shenzhen.

**XRF result:** Solder on the PCB shows **0.2% lead (2000 ppm)** — above the 0.1% RoHS limit.

 - Root cause: factory used **leaded solder** (Sn63/Pb37) to save $0.03/unit
 - RoHS status: **FAIL** — product cannot be placed on the EU market
 - Action: factory must switch to **lead-free solder** (SAC305: Sn/Ag/Cu) and re-test
 - Re-test cost: $250 (XRF + ICP confirmatory on 3 solder joints)
 - Production impact: +$0.03/unit + 5-day production delay for solder changeover
 - Result: re-test shows **0.02% lead** (200 ppm) — **PASS**

Without the XRF screen, the 5,000-unit shipment would have been seized at Rotterdam, the Amazon EU listing suspended, and the buyer fined. The $250 test saved a $25,000 product recall.

## How to Spot Fake RoHS Certificates

RoHS fraud is one of the most common compliance scams in China electronics. Watch for:

 - **No test report number** — a certificate that says "RoHS compliant" but lists no lab, no test date, no report number.
 - **Copied report** — the test report is for a different model or a generic board, not your product. Always match the sample photo in the report to your unit.
 - **Lab without ISO 17025** — the issuing lab is not accredited; its report carries no legal weight. Verify the lab's accreditation number on the CNAS or ILAC website.
 - **XRF-only pass on plastics** — a factory that claims "pass" based on XRF for phthalates is lying; phthalates require GC-MS.

## RoHS vs REACH & UK RoHS Post-Brexit

RoHS is frequently confused with REACH, and Brexit added a UK variant:

 - **RoHS vs REACH:** RoHS covers only EEE and exactly 10 substances. REACH covers all goods and 240+ SVHCs. An electronic toy needs RoHS for its PCB and REACH for its plastic housing.
 - **UK RoHS:** After Brexit, Great Britain has its own UK RoHS (2012 regulations, amended) with the same 10 substances and limits. You need a **UK RoHS DoC** for GB, separate from the EU RoHS DoC. Northern Ireland remains under EU RoHS. UKCA marking requires UK RoHS compliance — see our [UKCA guide](blog-ukca-certification-china.html).

## How Yeatru Handles RoHS Compliance

Yeatru runs RoHS for every electronics and EEE order shipped to the EU and UK. Our service includes:

 - Product scope check (11 EEE categories) and exemption review before tooling
 - XRF screening + full chemical test coordination at ISO 17025 labs (SGS, BV, CTI, CMA)
 - RoHS DoC drafting and technical file compilation (kept on record for 10 years)
 - Bundling with CE (LVD/EMC/RED) and REACH to test once and cover all EU obligations
 - Pre-shipment verification that the production lot matches the tested sample (no silent material substitution)

See our product certifications guide for how RoHS stacks up against FCC, CE, UKCA, and FDA.

## Frequently Asked Questions

### 1. What is RoHS?

RoHS (Restriction of Hazardous Substances) is an EU directive that restricts the use of 10 hazardous substances in electrical and electronic equipment (EEE) placed on the EU market. The current version is RoHS 3 (Directive (EU) 2015/863 amending 2011/65/EU). It applies to all 11 EEE categories and is enforced at EU customs and through market surveillance.

### 2. What is the difference between RoHS 2 and RoHS 3?

RoHS 2 (Directive 2011/65/EU) restricted 6 substances: lead, mercury, cadmium, hexavalent chromium, PBB, and PBDE. RoHS 3 (Delegated Directive (EU) 2015/863) added 4 phthalates — DEHP, BBP, DBP, and DIBP — bringing the total to 10 restricted substances. Both are now part of the same recast directive; "RoHS 2" and "RoHS 3" are shorthand for the original and the phthalate amendment.

### 3. Is RoHS mandatory for electronics sold in the EU?

Yes. Any EEE placed on the EU market must comply with RoHS substance limits. Non-compliance leads to customs detention, product recall, and fines up to **€100,000+** depending on the member state. RoHS is also a prerequisite for CE marking on most electronic products.

### 4. What is the difference between RoHS and REACH?

RoHS applies only to Electrical and Electronic Equipment (EEE) and restricts exactly 10 substances. REACH applies to ALL goods (not just electronics) and covers 240+ SVHC substances plus Annex XVII restrictions. An electronic product needs both: RoHS for its internal components and REACH for its plastics, paint, and cables.

### 5. How much does a RoHS test cost in China?

XRF screening costs **$100–$300** and takes 2–4 business days. Full chemical confirmation (ICP, GC-MS, IC) costs **$300–$1,500** depending on the number of homogeneous materials and takes 5–10 business days. A RoHS compliance declaration (DoC) is typically included with the test report or costs $50–$150 separately.

### 6. Does RoHS apply in the UK after Brexit?

Yes, the UK has its own UK RoHS regime (UK RoHS 2012, amended) that mirrors EU RoHS 2 and 3 with the same 10 substances and limits. Products placed on the Great Britain market need a UK RoHS DoC; Northern Ireland follows EU RoHS. A CE mark with EU RoHS DoC is no longer sufficient for GB — you need UKCA plus UK RoHS.

## Common Pitfalls to Avoid

- **Using the supplier's test report without verification.** Many factories provide fake or expired CE/FCC reports. Verify the report number on the certification body's website before placing a bulk order.
- **Applying the wrong certification for the destination market.** CE for EU, FCC/CPC for US, UKCA for UK, RCM for Australia. Shipping CE-marked goods to the US = customs seizure and $10k+ fines.
- **No test report for the exact product variant.** A CE report for a red 220V version does not cover a blue 110V version. Each variant needs its own test or a report covering all variants.
- **Forgetting ongoing compliance.** Regulations change (e.g., EU GPSR replacing GPSD, US CPSC updates). A cert valid today may be invalid in 12 months. Track renewal dates and budget for re-testing.
- **Under-declaring product category to skip certification.** Listing a children's toy as 'home decoration' to avoid CPC is customs fraud. The buyer of record (you) carries the liability.

## Conclusion

RoHS compliance from China is straightforward once you know the 10 substances and the two-test process: start with a **$100–$300 XRF screen**, escalate to **$300–$1,500 full chemistry** for anything near the limit, then sign a DoC and keep the file for 10 years. The biggest risk is not the test cost — it is accepting a fake certificate and shipping a non-compliant lot to the EU, where a single detained container can cost more than the entire testing budget. Always verify the lab's ISO 17025 accreditation, match the report sample to your product, and re-test whenever the BOM or supplier changes. [Contact Yeatru](contact.html) for a RoHS test plan and lab referral — we'll scope the exact materials your product needs tested before you place the order. Related: China product certifications guide.
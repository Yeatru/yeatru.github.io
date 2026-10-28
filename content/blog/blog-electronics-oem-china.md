---
title: "Electronics OEM in China: PCBA, Certification, Compliance"
url: "/blog-electronics-oem-china.html"
date: 2026-07-10
type: blog
description: "Electronics OEM from China: PCB design, SMT assembly, MOQ 100-1,000+ pcs, PCB in 3-7 days, full product 30-60 days and FCC/CE/RoHS certification."
keywords: "electronics OEM china, PCBA china, electronic manufacturer"
---

![China sourcing scene related to Electronics Oem China: a professional photo showing real products, people and logistics relevant to this sourcing topic, no text overlay](/Images/blog/blog-electronics-oem-china.jpg)

## What Is Electronics OEM in China?

**Electronics OEM** (electronic original equipment manufacturing) is the process of designing and producing electronic products in China from idea to finished device. It covers: turning a concept into a schematic and PCB layout, fabricating the bare PCB, assembling components via **SMT (surface-mount technology)** or THT (through-hole), flashing firmware, building the enclosure, and getting the product certified (FCC/CE/RoHS). China — especially **Shenzhen and Dongguan** — has the world's densest electronics supply chain, making it the default location for hardware startups and established brands alike. Electronics OEM is a specialized branch of [OEM & private label manufacturing from China](blog-oem-private-label-china.html), with unique challenges around component authenticity, firmware IP, and compliance.

## The Electronics OEM Process (6 Stages)

- **Idea & schematic** — define the product's function, then create a circuit schematic and BOM (bill of materials).
- **PCB design (Gerber files)** — lay out the board in KiCad/Altium, then export **Gerber files**, pick-and-place coordinates, and a BOM with manufacturer part numbers.
- **PCB fabrication** — the factory etches, drills, and plates the bare PCB (3–7 days prototype, 7–12 days mass).
- **SMT/THT assembly** — a pick-and-place machine mounts components, then the board goes through reflow soldering (7–15 days).
- **Firmware & testing** — flash firmware, run ICT (in-circuit test) and functional test. 100% functional test is mandatory for electronics.
- **Enclosure & certification** — injection-mold the enclosure ($1,000–$15,000), then certify FCC/CE/RoHS before shipping.

## Electronics OEM Cost & Lead Time by Stage

| | Stage || Cost Range || Lead Time || Notes |

| PCB design (Gerber) || $500 – $5,000 (one-time) || 5 – 15 days || You or a design house; not the factory |

| Bare PCB (2-layer) || $0.10 – $0.50/pc || 3 – 7 days (proto) || Setup fee $50–$150 for small runs |

| Bare PCB (4-layer) || $0.40 – $1.20/pc || 5 – 10 days || Most consumer electronics use 4-layer |

| Bare PCB (6–8 layer) || $1.50 – $4.00/pc || 7 – 12 days || For dense boards with BGA chips |

| SMT assembly || $0.01 – $0.03 per component || 7 – 15 days || MOQ 100–1,000+ pcs; setup $150–$500 |

| Enclosure mold || $1,000 – $15,000 (one-time) || 15 – 35 days || Per part; 2-part enclosure = 2 molds |

| FCC/CE/RoHS cert || $1,000 – $8,000 || 2 – 6 weeks || Per product model; RoHS is cheaper |

## PCB Layer Cost Guide

Layer count is the biggest driver of bare PCB cost. More layers allow smaller boards and better signal integrity for high-speed circuits (Bluetooth, Wi-Fi, HDMI) but raise the price sharply.

| | Layers || Cost/pc (1,000 pcs) || Typical Use |

| 1 – 2 || **$0.10 – $0.50** || Simple LED boards, power supplies, toys |

| 4 || **$0.40 – $1.20** || Bluetooth speakers, chargers, remote controls |

| 6 – 8 || **$1.50 – $4.00** || Smart devices, Wi-Fi modules, dash cams |

| 10 – 20 || **$5.00 – $25.00** || Smartphones, tablets, high-end audio |

## Worked Example: Bluetooth Speaker PCB

Let's cost a 4-layer Bluetooth speaker PCB at 500 pcs, assembled in Shenzhen:

- 4-layer bare PCB (100×60 mm): **$0.80**/pc × 500 = **$400**
- SMT assembly (50 components, pick-and-place + reflow): **$1.20**/pc × 500 = **$600**
- Components (BOM: MCU, Bluetooth SoC, battery, speaker, passives): **$3.50**/pc × 500 = **$1,750**
- Firmware flashing & functional test: **$0.50**/pc × 500 = **$250**
- Enclosure injection mold (2-part, P20): **$3,000** (one-time)
- **Total (incl. mold): $6,000** → **$6.50/pc BOM** + $3,000 mold amortized
- At 5,000 pcs: $6.50 + ($3,000 ÷ 5,000) = **$7.10/pc**
- MOQ: 500 pcs (SMT line minimum)

Landed cost per pc (DDP US, ~$1.20 freight + 2.5% duty): $7.10 + $1.20 + $0.18 = **$8.48/pc**. At a $39.99 retail, that's a ~79% gross margin — strong for a branded Bluetooth speaker.

## Key Regions: Shenzhen vs Dongguan

- **Shenzhen** — the global electronics hub. Huaqiangbei component market, 1,000+ PCB factories, SMT houses, and certification labs all within 1 hour. Best for prototyping, small-batch runs, and fast iteration. 30–50% faster turnaround than other regions.
- **Dongguan** — adjacent to Shenzhen; stronger on mass production and mold/enclosure manufacturing. Lower labor costs than Shenzhen for high-volume runs (10,000+ pcs).

## How to Find Electronics OEM Factories

- **Huaqiangbei (Shenzhen)** — the world's largest electronics component market. Walk the malls (SEG, Huaqiang Electronics) to find component suppliers and small SMT houses.
- **Alibaba / Made-in-China** — filter by "PCBA" and "Verified Supplier"; ask for photos of the SMT line and component sourcing channels.
- **Sourcing agent** — Yeatru's Shenzhen office pre-screens PCB+assembly factories, verifies component sourcing, and handles [RFQ](blog-rfq-guide-china-sourcing.html) comparison.

## Common Mistakes to Avoid

- **Buying components from unknown stalls** — counterfeit ICs cause 30–50% of field failures. Use authorized distributors only.
- **No firmware IP protection** — sign an NDA and use firmware readout protection (lock bits). Without it, the factory can copy your firmware and sell to competitors. See [IP protection](blog-ip-protection-china-sourcing.html).
- **Skipping 100% functional test** — electronics have a natural 1–3% defect rate; AQL sampling misses dead boards. Require 100% power-on functional test.
- **Forgetting ESD protection** — unsoldered ICs damaged by static during assembly fail in the field. Confirm the SMT line is ESD-protected.
- **Certifying after production** — FCC/CE tests can fail on EMI; redesigning the board post-production costs $5,000+ and delays 4–8 weeks. Certify the prototype before mass production.

## Frequently Asked Questions

### 1. What is the electronics OEM process in China?

The electronics OEM process has 6 stages: (1) idea to schematic and Gerber files, (2) PCB fabrication (3–7 days), (3) SMT/THT component assembly (7–15 days), (4) firmware flashing and testing, (5) enclosure via injection mold, and (6) FCC/CE/RoHS certification. A full product from idea to shipping takes **30–60 days**.

### 2. How much does a PCB cost in China?

Bare PCB cost depends on layer count and panel size. 1–2 layer boards run **$0.10–$0.50** each at 1,000 pcs; 4-layer **$0.40–$1.20**; 6–8 layer **$1.50–$4.00**; 10+ layer **$5.00+**. Prototypes of 5–50 pcs cost $1–$5 each with a $50–$150 setup fee. Surface finish (ENIG vs HASL) and copper weight add cost.

### 3. What is the SMT assembly MOQ?

SMT assembly MOQ is typically **100–1,000+ pcs** per board, though some Shenzhen houses accept 10–50 pcs for prototypes at a premium. The real constraint is the BOM: many ICs have 1,000+ piece MOQ, so below that you pay a premium for partial reels or broker stock.

### 4. Why is Shenzhen the best place for electronics OEM?

Shenzhen has the world's densest electronics supply chain: Huaqiangbei component market, 1,000+ PCB factories, SMT houses, mold shops, and certification labs all within 1 hour. Turnaround is **30–50% faster** than other regions, and component availability is unmatched for prototyping and small-batch runs.

### 5. How do I avoid counterfeit electronic components?

Three steps: (1) buy from authorized distributors (DigiKey, Mouser, Arrow) or the factory's verified franchise, not unknown Huaqiangbei stalls; (2) require lot codes and date codes on the BOM and inspect them; (3) run an authenticity test (X-ray or decapsulation) on high-value ICs. A $2 counterfeit MCU can brick a $50 product and destroy your brand.

### 6. Do I need FCC certification for an OEM electronics product?

Yes, for any electronic product sold in the US that emits radio frequency (intentional radiator: FCC Part 15C; unintentional: Part 15B). CE is required for the EU, RoHS restricts hazardous substances in both markets. Certification costs **$1,000–$8,000** and takes 2–6 weeks. Use a lab with FCC/CE accreditation and get the test report number. See our FCC guide and CE guide.

## Common Pitfalls to Avoid

- **Using the supplier's test report without verification.** Many factories provide fake or expired CE/FCC reports. Verify the report number on the certification body's website before placing a bulk order.
- **Applying the wrong certification for the destination market.** CE for EU, FCC/CPC for US, UKCA for UK, RCM for Australia. Shipping CE-marked goods to the US = customs seizure and $10k+ fines.
- **No test report for the exact product variant.** A CE report for a red 220V version does not cover a blue 110V version. Each variant needs its own test or a report covering all variants.
- **Forgetting ongoing compliance.** Regulations change (e.g., EU GPSR replacing GPSD, US CPSC updates). A cert valid today may be invalid in 12 months. Track renewal dates and budget for re-testing.
- **Under-declaring product category to skip certification.** Listing a children's toy as 'home decoration' to avoid CPC is customs fraud. The buyer of record (you) carries the liability.

## Conclusion

Electronics OEM from China turns your idea into a finished device in 30–60 days, with PCB at $0.10–$25/pc, SMT assembly at $0.01–$0.03 per component, and FCC/CE/RoHS certification at $1,000–$8,000. Shenzhen's unmatched supply chain makes prototyping fast, but the real risks are counterfeit components, firmware IP theft, and certification failures caught too late. Buy from authorized distributors, protect your firmware, certify the prototype before mass production, and run 100% functional test. [Contact Yeatru](contact.html) for a free electronics OEM quote — we'll vet the PCB factory, verify component sourcing, and manage certification end-to-end. Related: [China product certifications guide](blog-product-certifications-china.html).
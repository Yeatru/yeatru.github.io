---
title: "FCC Certification from China: FCC ID & SDoC Guide (2026)"
url: "/blog-fcc-certification-china.html"
date: 2026-07-14
type: blog
description: "FCC ID vs SDoC for electronics shipped from China to the US: FCC Part 15/15C/18 rules, accredited labs, $1,500-8,000 costs and a 4-8 week timeline."
keywords: "FCC certification china, FCC ID china, US electronics compliance"
---

![China sourcing scene related to Fcc Certification China: a professional photo showing real products, people and logistics relevant to this sourcing topic, no text overlay](/Images/blog/blog-fcc-certification-china.jpg)

## What Is FCC Certification?

The Federal Communications Commission (FCC) regulates the **electromagnetic emissions** of electronic devices sold or imported into the United States. Any device that contains a digital clock or oscillator — essentially every modern electronic product — falls under **FCC Part 15** and must demonstrate that it does not cause harmful interference to radio communications. For products that intentionally transmit radio energy (Bluetooth, Wi-Fi, Zigbee, LoRa, cellular modules), the FCC requires a formal **FCC ID certification** reviewed by a Telecommunication Certification Body (TCB). For non-transmitting devices, the supplier can issue an **SDoC (Supplier's Declaration of Conformity)** based on accredited lab testing, without filing with the FCC. FCC compliance is not a quality certificate — it is a legal pass-key to enter the US market, enforced by US Customs and Border Protection (CBP) and the FCC's Enforcement Bureau.

## FCC ID vs SDoC: Which Path Does Your Product Need?

The single most important decision is whether your product is an **intentional radiator** (it deliberately transmits RF energy) or an **unintentional radiator** (it emits RF only as a byproduct of its digital circuitry, like a switching power supply).

| | Dimension || FCC ID (Certification) || SDoC (Self-Declaration) |

| Product type || Intentional radiators: Bluetooth, Wi-Fi, LoRa, RF remote, cellular, Zigbee || Unintentional radiators: power adapters, LED drivers, non-RF electronics, digital peripherals |

| FCC Part || Part 15C / 15E (and Part 15B for emissions) || Part 15 Subpart B only |

| Lab required || Yes — FCC-listed accredited lab (e.g. BACL, CMA, ITS) || Yes — ISO 17025 / FCC-listed lab test report |

| Filing with FCC || Yes — TCB grants an FCC ID in the FCC OET database || No filing — DoC + test report kept on file |

| Cost || **$1,500 – $8,000** || **$300 – $1,200** |

| Timeline || 4 – 8 weeks (test + TCB review) || 1 – 3 weeks (test + DoC) |

| Label on product || FCC ID number + Part 15 warning || No ID required; optional logo + DoC on file |

| US responsible party || Yes (grantee or US contact) || Yes — required contact on DoC |

If a product has both a transmitter and a non-transmitting function (e.g. a Bluetooth speaker), it needs **FCC ID** for the radio and must still meet Part 15B emissions — both are covered in the single FCC ID grant.

## FCC Parts Reference Table

Knowing which Part applies prevents applying the wrong compliance path. Below are the Parts most relevant to consumer electronics sourced from China.

| | FCC Part || Scope || Common Products || Compliance Path |

| Part 15 Subpart B || Unintentional radiators — conducted & radiated emission limits || Power adapters, chargers, LED bulbs, USB hubs, wired headphones || SDoC |

| Part 15C || Intentional radiators, licensed-exempt (≤1 GHz, e.g. 2.4 GHz ISM) || Bluetooth speakers, Wi-Fi routers, 2.4 GHz remotes, Zigbee hubs || FCC ID |

| Part 15E || Intentional radiators above 1 GHz & UWB || 5 GHz Wi-Fi, UWB tags, some 5G modules || FCC ID |

| Part 18 || Industrial, Scientific, Medical (ISM) equipment || Microwave ovens, induction heaters, diathermy devices || FCC ID / DoC |

| Part 15B (digital devices) || Class A (commercial) vs Class B (residential) emission limits || All digital devices — Class B is stricter || Under SDoC or FCC ID |

## How to Get an FCC ID from China (Step by Step)

Yeatru walks electronics buyers through this sequence every month. Using an FCC-listed Chinese lab avoids flying samples to the US.

 - **Classify the device** — identify all radio technologies (Bluetooth 5.x, Wi-Fi 6, etc.) and confirm the applicable Part. If the device uses a pre-certified module, you may only need to reference the module's FCC ID (modular approval), cutting cost.
 - **Engage an FCC-listed lab in China** — BACL (Shenzhen), CMA, ITS, or SGS. Confirm the lab is listed on the FCC's *Recognized Accredited Laboratories* roster before paying.
 - **Submit 2–3 engineering samples + technical dossier** — schematic, BOM, block diagram, user manual, label artwork, and the external photos. The lab runs radiated/conducted emissions, SAR (for body-worn transmitters), and spectrum tests.
 - **TCB reviews the test report** — a Telecommunication Certification Body (e.g. UL, TUV, BACL itself as TCB) audits the report against FCC rules and grants the **FCC ID** (Grantee code + Product code) within 1–3 weeks.
 - **Register & label** — the grant is published in the FCC ID database. The FCC ID must be printed permanently on the product (or packaging if too small), with the Part 15 warning statement.

For SDoC products, steps 1–3 (lab test) apply, then the importer signs a **Supplier's Declaration of Conformity** listing the standards tested and naming a US responsible party. No TCB or FCC filing is involved.

## Worked Example: FCC ID for a Shenzhen Bluetooth Speaker

A buyer sources a **Bluetooth 5.3 portable speaker** from a Shenzhen factory for Amazon US. The speaker has a Class 2 Bluetooth radio, a built-in 1500 mAh Li-ion battery, and a 5 W amplifier.

**Compliance path:** FCC ID under Part 15C (intentional radiator, 2.4 GHz ISM) + Part 15B emissions + [battery UN38.3](blog-battery-shipping-compliance.html) for transport.

 - Lab: BACL Shenzhen (FCC-listed) — test 2 samples
 - Tests: ANSI C63.4 radiated/conducted emissions, FCC 15.247 transmitter, SAR exempt (body-worn >5 mm)
 - Lab testing: **3 weeks, $2,200**
 - TCB review (BACL TCB): **2 weeks, $800**
 - FCC ID granted: **2AB12-SPK-V3**
 - Label: silk-screen "FCC ID: 2AB12-SPK-V3" + Part 15 warning on the bottom of the speaker
 - Total cost: **$3,500** · Total timeline: **6 weeks**

Without FCC ID, the first Amazon FBA shipment would be held by CBP and the listing suspended. With it, the buyer reuses the ID for all future production runs of the same model.

## FCC Label Requirements

The FCC ID label is enforced at the port of entry. Rules:

 - **FCC ID number** must be permanently affixed (silk-screen, etching, or durable label) — not a sticker that peels off.
 - Minimum **6-point** type, legible without magnification (except for very small devices).
 - Part 15 warning statement: *"This device complies with Part 15 of the FCC Rules. Operation is subject to the following two conditions: (1) this device may not cause harmful interference, and (2) this device must accept any interference received, including interference that may cause undesired operation."*
 - SDoC-only products do not need an FCC ID but must be able to produce the DoC and test report within 14 days of an FCC request.

## How Chinese Factories Fake FCC Certification

FCC fraud is common in the China electronics supply chain. Red flags:

 - **No test report** — factory offers a "CE/FCC/RoHS" one-page certificate with no lab accreditation number and no test data.
 - **Copied FCC ID** — the ID on the label belongs to a different manufacturer or a different model (verified in the FCC ID database).
 - **Wrong Part** — a Bluetooth transmitter labeled only with Part 15B (unintentional) — this is illegal because the radio is uncertified.
 - **Module abuse** — factory claims the Bluetooth module is pre-certified but modified the antenna or added a power amplifier, voiding the modular grant.

Always verify the FCC ID at **fcc.gov/oet/ea/fccid**, match the grantee name to your supplier, and request the original signed test report. Yeatru's [pre-shipment QC](blog-pre-shipment-inspection-china.html) includes FCC label verification as part of compliance checks.

## How Yeatru Handles FCC Compliance

Yeatru Sourcing coordinates FCC testing and certification for US-bound electronics out of Shenzhen and Yiwu. Our compliance service includes:

 - Product classification and path recommendation (FCC ID vs SDoC) — including whether a pre-certified module can be leveraged to save $1,000–$3,000
 - Liaison with FCC-listed labs (BACL, CMA, ITS, SGS) for test scheduling and sample management
 - TCB review coordination and FCC ID grant tracking in the OET database
 - FCC label artwork review and on-product label verification during [FBA prep](blog-amazon-fba-prep-china.html)
 - Integration with [electronics OEM](blog-electronics-oem-china.html) projects so certification and tooling run in parallel

For the EU side, we bundle FCC with CE (RED) and [RoHS](blog-rohs-compliance-china.html) to avoid testing the same hardware twice.

## Frequently Asked Questions

### 1. What is the difference between FCC ID and SDoC?

FCC ID is the certification path for **intentional radiators** (Bluetooth, Wi-Fi, RF transmitters) and requires testing at an FCC-accredited lab, a TCB review, and a registered FCC ID number on the product. SDoC (Supplier's Declaration of Conformity) is the self-declaration path for **unintentional radiators** (power supplies, non-RF electronics); no FCC filing is needed, but you keep a test report and DoC on file and name a US responsible party.

### 2. Is FCC certification mandatory to sell electronics in the US?

Yes. Any electronic device sold or imported into the US that falls under FCC Part 15 (unintentional radiators) or Part 15C/15E (intentional radiators) must comply. Non-compliance leads to **CBP detention**, FCC fines up to **$16,000 per violation per day**, and market removal. Customs checks the FCC ID label and can request the test report.

### 3. Can I self-certify under FCC SDoC from China?

Yes, for unintentional radiators under Part 15 Subpart B. The supplier or US importer issues a Supplier's Declaration of Conformity based on a test report from an FCC-listed/ISO 17025 lab, keeps both on file, and names a **US responsible party** (US-based address) for correspondence. No filing or fee to the FCC is required.

### 4. How much does an FCC ID cost from China?

FCC ID certification runs **$1,500–$8,000** depending on complexity: a simple Bluetooth module is $1,500–$3,000; a Wi-Fi router with multiple bands $3,000–$6,000; a complex 5G/SDR device $6,000–$8,000. Lab testing plus TCB review takes **4–8 weeks**. SDoC testing only costs $300–$1,200 and takes 1–3 weeks.

### 5. How do I check if an FCC ID is real and valid?

Look up the ID on the FCC ID database at **fcc.gov/oet/ea/fccid**. The first 3–5 characters are the grantee code; the rest is the product code. Verify the grantee name matches the supplier, check the granted equipment authorization, and confirm the model number matches your product. A missing or mismatched record means the ID is fake.

### 6. How do Chinese factories fake FCC certification?

Common fakes: no actual lab test (just a printed certificate), an FCC ID copied from another manufacturer's product, the wrong Part applied (e.g. Part 15B label on a Bluetooth transmitter), or a grantee code that belongs to an unrelated company. Always verify the ID in the FCC database and ask for the original test report with the lab's accreditation number.

## Common Pitfalls to Avoid

- **Using the supplier's test report without verification.** Many factories provide fake or expired CE/FCC reports. Verify the report number on the certification body's website before placing a bulk order.
- **Applying the wrong certification for the destination market.** CE for EU, FCC/CPC for US, UKCA for UK, RCM for Australia. Shipping CE-marked goods to the US = customs seizure and $10k+ fines.
- **No test report for the exact product variant.** A CE report for a red 220V version does not cover a blue 110V version. Each variant needs its own test or a report covering all variants.
- **Forgetting ongoing compliance.** Regulations change (e.g., EU GPSR replacing GPSD, US CPSC updates). A cert valid today may be invalid in 12 months. Track renewal dates and budget for re-testing.
- **Under-declaring product category to skip certification.** Listing a children's toy as 'home decoration' to avoid CPC is customs fraud. The buyer of record (you) carries the liability.

## Conclusion

FCC compliance from China comes down to one fork in the road: **FCC ID for intentional radiators** ($1,500–$8,000, 4–8 weeks, TCB-reviewed) or **SDoC for unintentional radiators** ($300–$1,200, 1–3 weeks, self-declared). Getting the path right — and verifying the FCC ID in the FCC database — is what separates a shipment that clears CBP from one that gets detained and fined. Whether you're launching a Bluetooth speaker, a Wi-Fi sensor, or a simple USB charger, start the FCC process **before** mass production so the label and grant are ready when your first container ships. [Contact Yeatru](contact.html) for an FCC path assessment and lab referral within 24 hours. Related: China product certifications guide.
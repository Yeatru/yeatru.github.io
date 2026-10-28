---
title: "How to Track a Shipment from China: Tracking Guide"
url: "/blog-tracking-china-shipment.html"
date: 2026-09-03
type: blog
description: "How to track a China shipment: tracking numbers by mode, tools (17track, AfterShip, MarineTraffic), status meanings and delay diagnosis."
keywords: "track shipment china, china package tracking, freight tracking"
---

![China sourcing scene related to Tracking China Shipment: a professional photo showing real products, people and logistics relevant to this sourcing topic, no text overlay](/Images/blog/blog-tracking-china-shipment.jpg)

## What Does "Tracking a China Shipment" Really Mean?

Tracking a China shipment means following a cargo's status from the moment it leaves your supplier's factory through export customs, the international leg (air or sea), destination import customs, and final delivery. Each mode — express, air, sea — uses a different tracking number format and a different tracking system, so the first step in any trace is **identifying which number you have**. The supplier, freight forwarder, and destination carrier each see only a slice of the journey; your job is to stitch those slices together and spot stalls early.

## Tracking Numbers by Mode

 | | Mode || Number Format || Example || Where to Track |

 | **Express (DHL, FedEx, UPS, SF)** || 10–12 digit alphanumeric || 1Z999AA10123456784 (UPS) || carrier site, 17track, AfterShip |

 | **China Post / ePacket** || RA / LA + 9 digits + CN || RA123456789CN || 17track, AfterShip, China Post |

 | **Air freight (MAWB)** || 3-digit carrier prefix + 8 digits || 074-12345678 (China Cargo) || cargo.airchina.com, Track-Trace |

 | **Air freight (HAWB)** || forwarder's house AWB || YT20260901234 || forwarder portal only |

 | **Sea FCL container** || 4 letters + 7 digits || MSKU1234567 || MarineTraffic, line portal |

 | **Sea LCL / BL** || Bill of Lading number || COSU61234567890 || line portal, forwarder portal |

If you booked through a freight forwarder under DDP, you usually get **only a HAWB or a forwarder reference**, not the MAWB or BL. That's fine — the forwarder's portal (or their WhatsApp support) is the single source of truth. See [DDP shipping from China](blog-ddp-shipping-china.html).

## Tracking Tools Compared

 | | Tool || Best For || Pros || Cons |

 | **17track.net** || Express, China Post, registered mail || Free, 2,000+ carriers, auto-detect || Limited detail on heavy freight |

 | **AfterShip** || Express, e-commerce orders || API, notifications, branded tracking page || Free tier limited; paid for volume |

 | **Airline cargo sites** || Air freight MAWB || Authoritative milestone data || One airline at a time |

 | **MarineTraffic / VesselFinder** || Sea containers & vessels || Live AIS vessel position, port calls || Containers need the container number |

 | **Shipping line portal** || Sea BL / container || Most accurate ETA, hold alerts || One line at a time (Maersk, MSC, COSCO…) |

 | **Forwarder portal** || DDP / consolidated shipments || Single pane of glass, handles HAWB || Only for that forwarder's shipments |

## How to Track a Shipment: 5 Steps

 - **Get the right number** — ask your supplier or forwarder for the carrier tracking number (express), MAWB (air), or BL + container number (sea). A forwarder reference alone may not be traceable on public sites.
 - **Enter it on the matching tracker** — waybills on 17track/AfterShip; MAWB on the airline's cargo site; container numbers on MarineTraffic or the shipping line's portal. If you don't know the carrier, paste the number into 17track — it auto-detects.
 - **Map milestones to expected transit** — express: 3–7 days; air: 5–12 days; sea FCL USWC: 18–25 days, USEC: 28–35 days, EU: 28–38 days. LCL adds 3–7 days for deconsolidation. See [sea freight](blog-sea-freight-china.html) and [air freight](blog-air-freight-china.html).
 - **Flag stalls early** — if the status hasn't changed for more than 5 business days, email the forwarder (not the supplier) with the number, expected ETA, and a clear question. The supplier only sees the origin handoff.
 - **Confirm delivery & inspect** — once it shows "out for delivery" or "delivered", be present to sign. Before signing the Proof of Delivery, count cartons against the BL and photograph any external damage — concealed damage claims are hard after signing.

## Common Statuses Decoded

 | | Status || Meaning || What to Do |

 | Picked up / Received || Cargo collected from supplier || Wait |

 | Customs clearance at origin || China export customs || Wait 1–3 days |

 | In transit / In air / On voyage || Mid-journey, no scan yet || Wait; this is normal for 5–15 days |

 | Arrived at destination || Entered destination country || Prepare import docs |

 | Customs clearance in progress || Import customs review || Have invoice, packing list, BL ready |

 | Held for inspection || Physical inspection ordered || Cooperate; provide certificates if asked |

 | Out for delivery || Last-mile carrier has it || Be available to sign |

 | Delivered || Signed for || Inspect within 24 hours; file claims fast |

## Why Tracking Gets Stuck (and How to Fix It)

A status that hasn't moved for 5+ business days usually falls into one of four buckets:

 - **Origin port congestion / peak season** — Aug–Oct is peak; vessels and flights are overbooked. Cargo may sit at the origin warehouse or port for 7–14 days waiting for the next available slot. *Fix:* ask the forwarder for the revised ETD/ETA; buffer your customer ETA by 2 weeks.
 - **Customs hold (origin or destination)** — customs wants documents (commercial invoice, packing list, BL, certificate of origin) or wants to inspect. *Fix:* email the requested docs within 24 hours; pay duty/VAT promptly. Most holds clear in 1–3 days once docs are received.
 - **Missing or incorrect documents** — a wrong HS code, mismatched invoice value, or missing certificate (FDA, FCC, CE) will stall customs. *Fix:* ask the forwarder exactly which document is missing and resend corrected copies. Pre-vet your docs before shipping to avoid this.
 - **Carrier exception** — weather, port strikes, vessel rerouting, or a mechanical delay. *Fix:* the carrier will issue a revised ETA; there's nothing to do but wait and inform your customer.

## Worked Example: "Customs Clearance in Progress" for 8 Days

An Amazon FBA seller in the US sees their sea FCL shipment stuck at "Customs clearance in progress — Port of Long Beach" for **8 days**. Here's how to resolve it:

 - **Day 1**: Email the freight forwarder's customs broker with the BL number and ask for the hold reason. Reply: "CBP is requesting a corrected commercial invoice — the unit price on the invoice ($3.20) does not match the declared value on the entry ($4.10)."
 - **Day 1**: Contact the Chinese supplier for a corrected invoice showing the actual paid unit price ($4.10) and the total paid. The supplier sends it within 4 hours.
 - **Day 2**: Forward the corrected invoice + proof of payment (bank wire confirmation) to the broker. The broker amends the entry and resubmits.
 - **Day 4**: Status updates to "Customs released." Container moves to the trucking queue.
 - **Day 6**: Delivered to the Amazon FBA warehouse. Total delay from hold: 6 days (down from an estimated 14+ days if the seller had waited).

The key: **don't wait for the system to move**. Proactively ask the broker for the exact missing document and supply it within 24 hours. Most customs holds are document problems, not cargo problems.

## Tracking by Mode: What to Expect

 - **Express ([DHL / FedEx / UPS](blog-express-courier-china.html))** — scans update every few hours; full door-to-door visibility. ETA is reliable ±1 day. If it stalls, call the carrier directly with the waybill.
 - **Air freight** — milestones update at handoff, origin customs, flight departure, arrival, destination customs. Middle of the flight has no scan (normal). Track with MAWB on the airline's cargo site.
 - **Sea FCL** — updates at container load, origin port gate-in, vessel departure, transshipment ports, destination port, rail/truck to door. Vessel position is visible on MarineTraffic by container number. Expect 5–10 day gaps between scans during the ocean leg.
 - **Sea LCL** — fewer public scans because your cargo shares a container. Use the forwarder's portal; they have visibility into the container your LCL is riding in.

## How Yeatru Tracks Your Shipments

Every Yeatru shipment gets a single forwarder reference and a dedicated portal link that aggregates express, air, and sea milestones in one place. You don't need to juggle 17track, MarineTraffic and the airline site — we pull them together. Our logistics team proactively monitors every shipment and flags stalls before they become delays. For DDP shipments, we handle customs clearance on your behalf and update you the moment cargo is released.

## Frequently Asked Questions

### 1. How do I track a shipment from China?

Find the tracking number: express waybill (10–12 digits), air MAWB (11 digits like 074-12345678), or sea BL + container number. Then enter it on the right tool: 17track/AfterShip for express, the airline's cargo tracker for MAWB, and MarineTraffic or the shipping line portal for containers.

### 2. What is the most reliable China tracking site?

For express and registered mail, **17track.net** and **AfterShip** are the most reliable multi-carrier trackers. For sea freight, **MarineTraffic.com**, VesselFinder, or the shipping line's own portal (Maersk, MSC, COSCO) give container-level ETA updates. For air freight, use the airline's cargo tracker.

### 3. Why is my China tracking number not updating?

Tracking can stall for 3–7 business days during origin port consolidation, customs inspection, peak-season backlog (Aug–Oct), or while waiting for the next vessel/flight. If a status stays unchanged for more than 5 business days, contact your freight forwarder or carrier for a revised ETA.

### 4. What does "customs clearance in progress" mean?

Your shipment has arrived in the destination country and is under import customs review. It may be held for document verification, physical inspection, or duty/VAT payment. Provide the requested documents (commercial invoice, packing list, BL, certificates) and pay duty promptly to clear it within 1–3 business days.

### 5. Can I track sea freight by BL number?

Yes. Use the shipping line's portal (Maersk, MSC, COSCO, Evergreen, etc.) or a third-party site like MarineTraffic.com or VesselFinder. Enter the container number (preferred) or the Bill of Lading number to see vessel position, ETD/ETA, and port calls.

### 6. How long does a China shipment take after it is shipped?

Express (DHL/FedEx/UPS): 3–7 business days door-to-door. Air freight: 5–12 days. Sea FCL to US West Coast: 18–25 days; to US East Coast: 28–35 days; to Europe: 28–38 days. LCL adds 3–7 days for deconsolidation at destination. Peak season (Aug–Oct) adds 5–10 days.

## Common Pitfalls to Avoid

- **Accepting a flat DDP rate without line items.** A real DDP quote breaks out freight, duty, VAT, clearance, and last-mile. A single per-kg number hides costs that surface as surprise invoices or low-quality service.
- **Choosing CIF for control of freight.** Under CIF the supplier picks the carrier and inflates freight by 15–25%. Choose FOB (you control the line) or DDP (all-in, your forwarder) — never CIF unless you have no other option.
- **No transit-time buffer for FBA restocks.** Sea freight from China runs 25–40 days + 5–7 days FBA receiving. Order 45–60 days before you need stock in FBA, not 30. Running out of stock kills your Amazon ranking.
- **Ignoring ISPM-15 for wooden pallets.** EU and US customs require heat-treated pallets with the IPPC stamp. Missing stamps = container detained, €400–$600 fumigation, 3–7 day delay.
- **No cargo insurance.** Freight forwarders' liability is limited to ~$2/kg by convention. For high-value cargo, buy separate all-risks insurance (0.3–0.5% of value) — it costs $50 and pays out $10,000.

## Conclusion

Tracking a China shipment is mostly about using the right number on the right tool, knowing what each status means, and proactively chasing stalls before they become delays. Express gives near-real-time scans; air and sea have gaps that are normal. The #1 cause of stuck tracking is a customs document hold — which you can usually resolve in 1–3 days by emailing the missing invoice, packing list or certificate. If you booked through a freight forwarder, their portal is your single source of truth; the supplier only sees the origin handoff. [Ship with Yeatru](contact.html) and get one tracking link that covers the full journey — plus a team that flags stalls before you have to. Related: [Incoterms EXW/FOB/DDP comparison](blog-incoterms-china-sourcing.html), [DDP door-to-door shipping guide](blog-china-ddp-shipping-agent.html), [China warehousing & consolidation](blog-warehousing-consolidation.html).
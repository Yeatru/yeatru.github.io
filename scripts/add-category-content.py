#!/usr/bin/env python3
"""Batch-add contextual content + FAQPage schema to 43 category pages.

For each category-*.html file:
  1. Insert a content block between </header> and <section aria-label="product grid">
  2. Insert FAQPage JSON-LD before </head>

Content is context-aware — categories are grouped and each group gets relevant text.
"""

import glob
import json
import re
import os

# ── Category groupings with context-aware content ──────────────────────

CATEGORY_INFO = {
    # (slug → readable name, sourcing intro, key considerations, faq pairs)

    "beauty": (
        "Beauty & Personal Care",
        "Beauty products from China — makeup tools, hair styling devices, skincare accessories — ship worldwide at factory-direct prices. Yeatru curates beauty SKUs from Yiwu and Guangzhou factories, with on-site QC following AQL 2.5 inspection before shipment. Common beauty items sourced include makeup blender sponges, hair curling wands, facial massagers, and personal care tools.",
        [
            "Skin-contact products require safety documentation (CosIng for EU, FDA for US). Always verify Material Safety Data Sheets (MSDS) before confirming PO.",
            "Hair tools with heating elements need ETL/CE safety marks — ask for test reports, not just manufacturer claims.",
            "Small beauty accessories (sponges, brushes) have low MOQ (often 100 pcs) and ship cheaply via air as supplements to larger orders.",
            "Yeatru inspects all beauty products for coating quality, sharp edges, and labeling accuracy before shipment."
        ],
        [
            ("What certifications do beauty products need for import?",
             "Skin-contact beauty accessories sold in the EU require CosIng registration; the US does not require registration for most tools but labelling must be truthful. Electrical beauty devices (hair dryers, massagers) need CE/ETL safety marks."),
            ("What is the MOQ for beauty products from China?",
             "MOQ varies by item: small accessories (sponges, clips) start at 100 pcs, electrical beauty devices usually start at 500 pcs. Yeatru can source trial orders at reduced MOQ for most beauty categories."),
        ]
    ),
    "skin-care": (
        "Skin Care Tools & Accessories",
        "Skincare tools from China — facial rollers, gua sha stones, cleansing brushes, and beauty devices sourced from Guangzhou and Yiwu. Yeatru verifies that materials are skin-safe (stainless steel, natural stone, medical-grade silicone) and handles documentation for EU/US import compliance.",
        [
            "Jade rollers and gua sha tools must be sourced from real jade factories — Yeatru verifies material certificates for authenticity.",
            "Electric skincare devices require CE/FCC marking for the EU and US markets respectively.",
            "Packaging is critical for skincare tools — Yeatru handles custom branded boxes and shrink wrapping on request."
        ],
        [
            ("Are skincare tools from China safe?",
             "Yes, when properly sourced. Yeatru requires material safety certificates and conducts on-site quality checks for all skin-contact items. We refuse factories that cannot provide test reports."),
            ("Can I private label skincare tools?",
             "Yes. MOQ for private label skincare tools is typically 500–1,000 pcs depending on the item. Yeatru handles logo printing, custom packaging design, and co-ordinates with the factory."),
        ]
    ),
    "personal-care": (
        "Personal Care & Hygiene",
        "Personal care items from China — dental care accessories, hygiene tools, shower products, and wellness devices. Sourced from ISO-certified factories with on-site QC inspection before shipment.",
        [
            "Oral care items (toothbrushes, floss holders) must pass BPA-free tests for EU/US markets.",
            "Electric personal care devices need CE/FCC marking and may require battery safety certification (UN38.3) for shipping.",
            "Personal care consumables (pads, sponges) are low-MOQ and ideal for trial orders."
        ],
        [
            ("Do personal care items from China have safety certifications?",
             "Yeatru verifies BPA-free certificates and material safety data sheets for all personal care items. Electrical devices additionally require CE or FCC marks."),
            ("What is the typical lead time for personal care products?",
             "Small plastic accessories take 7–15 days for production plus 3–30 days shipping depending on destination and method. Electrical devices take 15–25 days production."),
        ]
    ),
    "toys": (
        "Toys & Kids Products",
        "Toys from China — educational toys, fidget toys, building sets, plush toys, and kid's activity items. Sourced from CPSIA-compliant factories with age-appropriate labelling. Yeatru verifies compliance with US CPSIA and EU EN71 toy safety standards.",
        [
            "Toys sold in the US must meet CPSIA lead and phthalate limits; EU toys must pass EN71 mechanical, chemical, and flammability tests.",
            "Plastic toys need BPA, PVC, and phthalate-free declarations — Yeatru collects test reports from every factory we work with.",
            "Fidget toys (pop-its, simple dimple) have very low MOQ (100 pcs) and sell well on TikTok Shop and Amazon."
        ],
        [
            ("Are toys from China safe for children?",
             "When sourced properly, yes. Yeatru only works with factories that can provide CPSIA or EN71 test reports. We conduct pre-shipment QC at AQL 2.5 to catch defective or non-compliant units."),
            ("What certifications do I need to import toys to the US?",
             "Toys sold in the US must have a Consumer Product Safety Improvement Act (CPSIA) certificate and have passed third-party testing for lead and phthalates. Yeatru can help coordinate this testing if your supplier has not already done it."),
        ]
    ),
    "kids": (
        "Kids & Baby Products",
        "Kids' and baby products from China — child safety items, nursery accessories, educational tools, and baby gear. Sourced from factories that comply with US CPSIA and EU EN71 safety standards.",
        [
            "Products intended for children under 36 months have stricter CPSIA requirements including ASTM F963 mechanical testing.",
            "Baby feeding products must be 100% BPA-free and may need LFGB (German food-grade) or FDA food-contact declarations.",
            "Always request Age Grade and Choking Hazard warnings on all kids' products."
        ],
        [
            ("What are the CPSIA requirements for baby products?",
             "CPSIA requires third-party testing for lead (≤100ppm) and phthalates (≤0.1%) in all children's products. Small parts warnings are mandatory for items with parts that could present a choking hazard for children under 3."),
            ("Can Yeatru help with CPSIA compliance?",
             "Yes. We collect test reports from our factories and can arrange independent third-party testing if needed. Most of our baby/kids suppliers are already CPSIA-compliant."),
        ]
    ),
    "baby-care": (
        "Baby Care & Nursery",
        "Baby care and nursery products from China — diaper organizers, feeding accessories, bathtime gear, and nursery storage. Sourced from ISO-certified factories with full safety documentation.",
        [
            "Silicone baby products must be food-grade certified (FDA or LFGB) — never source uncertified silicone for infant use.",
            "Electric baby devices (monitors, warming plates) need CE/ETL safety marks and battery safety for shipping.",
            "Yeatru conducts AQL 2.5 pre-shipment inspection on all baby care products regardless of MOQ."
        ],
        [
            ("Is silicone baby products from China safe?",
             "Food-grade silicone from certified suppliers is safe. Yeatru requires LFGB or FDA food-contact declarations for all silicone products we source for baby use."),
            ("What is the MOQ for baby care products?",
             "MOQ ranges from 100 pcs for small accessories to 500–1,000 pcs for larger nursery items. Trial orders are possible for most SKUs."),
        ]
    ),
    "clothing": (
        "Apparel & Clothing",
        "Clothing from China — fashion apparel, wholesale garments, and custom OEM apparel. Sourced from Guangzhou and Yiwu garment factories with full size charts and fabric specifications. Yeatru handles private label printing, packaging, and drop-shipping to Amazon FBA.",
        [
            "Garment factories in China have 15–30 day lead times for production; rush orders add 30–50% surcharge.",
            "Always request fabric swatches and fit samples before placing bulk orders — factories often change materials without notice.",
            "Clothing can have very low MOQ (as low as 50 pcs per style/color/size combo) from Yiwu garment markets."
        ],
        [
            ("Is it cheaper to source clothing from China than Bangladesh or Vietnam?",
             "For developed-style apparel, China remains the most competitive due to infrastructure and on-demand fabric supply. For very basic garments at scale, Bangladesh/Vietnam may be cheaper per unit but with longer lead times."),
            ("Can Yeatru help with sizing and fit for apparel?",
             "Yes. We can source multiple sample sizes, measure them with a caliper, and provide digital size charts. We also verify that factories follow your grade rules for fit discrepancies."),
        ]
    ),
    "socks": (
        "Socks & Hosiery",
        "Socks and hosiery from China — athletic socks, fashion socks, compression socks, and novelty socks. Produced on automated knitting machines in Zhejiang province with customizable yarn, pattern, and private label.",
        [
            "Compression socks require medical device classification review in the EU and US — Yeatru flags high-pressure compression as a regulated product.",
            "Novelty/dress socks have MOQ as low as 100 pairs; athletic and compression socks start at 500 pairs.",
            "Always specify yarn composition (cotton %, nylon %, spandex %) and density/needle count in your RFQ to avoid substitution."
        ],
        [
            ("What is the typical MOQ for socks from China?",
             "Basic dress socks: 100 pairs. Athletic/cushioned socks: 200 pairs. Graduated compression socks: 500 pairs. Yeatru can broker trial orders below factory MOQ by consolidating with other clients."),
            ("Are compression socks a medical device?",
             "In the EU and US, graduated compression socks above 25mmHg are classified as Class I medical devices and need CE marking / FDA registration. Yeatru advises on this before you place an order."),
        ]
    ),
    "footwear": (
        "Footwear & Shoes",
        "Shoes and footwear from China — casual shoes, work footwear, fashion sneakers, and boots. Sourced from Fujian, Guangdong, and Zhejiang shoe factories with customizable upper, sole, logo, and packaging.",
        [
            "Shoes take 20–35 days for production; mold setup takes 7–14 days. Rush programs are available with premium pricing.",
            "Sole materials matter: TPR soles (TPR = thermoplastic rubber) are lighter and cheaper than rubber soles. Specify in your RFQ.",
            "Leather shoes need REACH SVHC compliance (EU) and Proposition 65 warnings (California) for chemical content."
        ],
        [
            ("How long does it take to develop a custom shoe from China?",
             "2–3 weeks for prototype development, 20–35 days for mass production. Yeatru can broker with factories for trial MOQ of 300–500 pairs for custom styles."),
            ("Do shoes from China fit US/EU sizes correctly?",
             "Chinese factories use the same size charts as global brands, but actual footbed measurements vary by manufacturer. Yeatru measures every sample with a foot gauge to confirm before bulk production."),
        ]
    ),
    "shoes": (
        "Shoes & Footwear",
        "Shoes from China — casual shoes, fashion footwear, boots, and work shoes. Sourced from Fujian and Zhejiang shoe manufacturers. Yeatru handles custom branding, packaging, and QC inspection.",
        [
            "Shoe production lead time: 20–35 days depending on style complexity.",
            "Custom molds for unique soles cost $500–$2,000 and take 7–14 days to fabricate.",
            "Always request size measurements in millimeters, not just size numbers, to ensure consistency."
        ],
        [
            ("What is the MOQ for custom shoes from China?",
             "Basic styles: 300 pairs. Custom molds: 500+ pairs. Yeatru has factory relationships for small-batch trial orders (100 pairs) with a small premium fee."),
            ("Can I get samples before ordering?",
             "Yes. Yeatru arranges prototype samples (typically $25–$50/pair) within 2 weeks of your design approval."),
        ]
    ),
    "kitchen-tools": (
        "Kitchen Tools & Utensils",
        "Kitchen tools and utensils from China — cooking gadgets, food preparation tools, bakeware accessories, and kitchen storage solutions. Sourced from Zhejiang and Guangdong with stainless steel, silicone, and plastic materials.",
        [
            "Metal kitchen tools must be food-contact safe (LFGB/FDA declaration); plastic tools must be BPA-free and may need food contact tests.",
            "Yeatru verifies stainless steel grade (304 vs 201) using a portable XRF analyzer during QC inspection to prevent material substitution.",
            "MOQ for basic tools is 100 pcs; for knife sets and multi-piece gadgets, MOQ is typically 300–500 pcs."
        ],
        [
            ("Is stainless steel kitchenware from China safe?",
             "Grade 304 stainless steel (food-safe) is standard for kitchenware. Yeatru verifies the grade using XRF analysis during pre-shipment QC because some factories substitute cheaper 201 steel without disclosure."),
            ("What certifications do kitchen tools need for the EU?",
             "All food-contact kitchen tools must comply with EU Regulation 1935/2004 and 10/2011 on plastic materials. Metal tools need LFGB (German food contact) or equivalent certification."),
        ]
    ),
    "kitchen-bath": (
        "Kitchen & Bathroom Fixtures",
        "Kitchen and bathroom fixtures from China — hardware, faucet accessories, storage solutions, and cleaning tools. Sourced from the Yiwu small commodity market and Guangdong hardware factories.",
        [
            "Hardware products with plating (chrome, nickel) must pass salt spray corrosion testing (48–96 hours) to prevent rust issues.",
            "Tile and floor cleaning tools ship well as supplement cargo in LCL shipments.",
            "Yeatru conducts dimensional QC on fixture hardware to ensure compatibility with standard US/EU connectors."
        ],
        [
            ("Do bathroom fixtures from China meet US plumbing standards?",
             "Not by default. Yeatru verifies that faucet and fixture components meet NSF/ANSI 61 drinking water standards before sourcing. Importing fixtures without certification may cause code violations."),
            ("What is the lead time for custom bathroom hardware?",
             "Basic hardware: 10–15 days. Custom-colored or plated pieces: 20–30 days. Mold development for unique shapes: 7–14 extra days."),
        ]
    ),
    "kitchen-storage": (
        "Kitchen Storage & Organization",
        "Kitchen storage solutions from China — food containers, spice racks, pantry organizers, and countertop caddies. Sourced from Zhejiang plastic and metal fabrication factories.",
        [
            "Food-contact containers must be BPA-free and meet LFGB/FDA requirements.",
            "Collapsible silicone storage containers are popular; verify they maintain structural integrity after 50+ freeze/thaw cycles.",
            "Yeatru recommends stackable modular systems to maximize Amazon FBA prep efficiency and minimize shipping volume."
        ],
        [
            ("Are food storage containers from China food-safe?",
             "Yeatru verifies LFGB/FDA declarations for all food-contact storage products. We also conduct a 50-cycle freeze/thaw test on silicone containers to check for cracking."),
            ("What is the MOQ for kitchen storage from China?",
             "Most storage items have MOQ of 100–300 pcs. Yeatru can consolidate smaller trial orders with other clients to hit factory MOQ requirements."),
        ]
    ),
    "cups-drinkware": (
        "Cups & Drinkware",
        "Cups, mugs, and drinkware from China — silicone drinkware, stainless steel tumblers, ceramic mugs, and custom branded drinkware. Sourced from Guangdong ceramic factories and Zhejiang plastic/metal fabricators.",
        [
            "Ceramic mugs for dishwasher/microwave use must be high-fired porcelain (1280°C+); low-fired ceramics leach glazes.",
            "Stainless steel tumblers need to be double-wall vacuum insulated to meet Amazon customer expectations — check wall thickness (≥0.3mm).",
            "Yeatru tests ceramic mugs for lead and cadmium glaze leachability per FDA 711 standards."
        ],
        [
            ("Are ceramic mugs from China safe for food contact?",
             "High-fired porcelain mugs (1280°C firing) are safe for dishwasher/microwave use. Yeatru conducts leach testing on glazed ceramic per FDA guidelines before approving a factory."),
            ("Can I custom print mugs with my brand?",
             "Yes. MOQ for custom printed mugs is typically 300–500 pcs depending on the printing method (pad print vs transfer print vs sublimation). Full-color sublimation MOQ is usually lower (100 pcs)."),
        ]
    ),
    "home-garden": (
        "Home & Garden",
        "Home and garden products from China — planters, gardening tools, outdoor decor, and home accessories. Sourced from Yiwu and Guangdong factories specializing in outdoor and garden equipment.",
        [
            "Metal garden tools must be powder-coated, not painted, for outdoor corrosion resistance.",
            "Plastic planters should use UV-stabilized resin — Yeatru verifies with a simple UV torch test during QC.",
            "Yeatru advises against sourcing wood garden items from non-sustainable sources; we prefer bamboo or FSC-certified plywood."
        ],
        [
            ("How long do plastic planters from China last outdoors?",
             "With UV-stabilized resin, 3–5 years of outdoor use. Without UV protection, plastic planters become brittle and crack within 6–12 months. Yeatru includes UV verification in our QC checklist."),
            ("What garden tools are most profitable to import?",
             "Pruning shears, trowels, and hand rakes sell well on Amazon with 40–60% margins. Auto-watering systems and LED garden lights have seasonal spikes. Yeatru provides monthly market trend reports to our active clients."),
        ]
    ),
    "cleaning": (
        "Cleaning & Household",
        "Cleaning supplies and household products from China — scrub tools, cleaning accessories, storage solutions, and household gadgets. Sourced from Yiwu's dedicated cleaning product wholesale district.",
        [
            "Microfiber cleaning cloth quality varies: 200–250 GSM is minimum for durability; cheaper 150 GSM cloths wear out after 5–10 washes.",
            "Cordless spin mops and electric cleaning tools need battery safety (UN38.3) for air shipping and CE/ETL marks.",
            "Yeatru tests microfiber GSM with a digital scale and density calculation during QC inspection."
        ],
        [
            ("Are microfiber cloths from China good quality?",
             "Quality varies wildly. Yeatru targets 200+ GSM microfiber with split-fiber technology for maximum absorbency. We verify with a digital scale during QC — anything under 200 GSM is rejected."),
            ("What is the MOQ for cleaning supplies?",
             "Basic cleaning tools: 100 pcs. Electronic cleaning gadgets: 500 pcs. Yeatru has relationships with Yiwu cleaning product wholesalers who can supply mixed trial orders below factory MOQ."),
        ]
    ),
    "household": (
        "Household Products",
        "General household products from China — small home gadgets, cleaning accessories, storage solutions, and kitchen tools. Sourced from Yiwu market wholesale suppliers with curated quality verification.",
        [
            "Many household gadgets ship as supplement cargo (LCL) to reduce per-unit shipping costs.",
            "Check if electronic household items need CE/FCC marking before sourcing.",
            "Yeatru's Yiwu office physically inspects products from wholesale stalls before adding them to catalog."
        ],
        [
            ("Are household gadgets from China safe to use?",
             "Yeatru verifies safety marks (CE/ETL/FCC) for all electronic household items we source. Non-electronic items are inspected for sharp edges, choking hazards (small parts), and material safety."),
            ("How does Yeatru verify Yiwu market products?",
             "Our Yiwu office physically visits stalls, inspects product quality, tests functionality where applicable, and collects factory contact information for traceability before recommending products to clients."),
        ]
    ),
    "storage-organization": (
        "Storage & Organization",
        "Storage and organization products from China — foldable boxes, drawer organizers, closet systems, and home storage solutions. Sourced from Zhejiang plastic and fabric fabrication factories.",
        [
            "Collapsible fabric storage boxes use non-woven or woven polypropylene; woven is more durable but costs 15–20% more.",
            "Clear plastic organizers should use PET (recyclable, clearer) not PVC (yellow over time, chemical leaching).",
            "Yeatru recommends Amazon-compatible packaging to reduce prep fees — standard sizes fit LTL/PFP prep without repacking."
        ],
        [
            ("What's better: fabric or plastic storage boxes?",
             "Fabric boxes cost 30–50% less, are lighter to ship, and come in more colors/patterns. Plastic boxes last longer (5+ years vs 2–3 years) but cost more. Both sell well on Amazon depending on the product niche."),
            ("Can I get custom sizes for storage organizers?",
             "Yes, MOQ for custom plastic organizers starts at 500 pcs (requires mold development at $500–$1,500). Fabric storage custom sizes start at 300 pcs with no mold cost."),
        ]
    ),
    "backpacks": (
        "Backpacks & Bags",
        "Backpacks from China — travel backpacks, school backpacks, laptop bags, and outdoor hiking packs. Sourced from Fujian and Zhejiang bag manufacturers with customizable fabric, zippers, and branding.",
        [
            "YKK zippers are the industry standard for durability; request YKK instead of generic zippers — adds ~$0.15–$0.30 per unit but reduces return rates.",
            "Ripstop nylon (210D+ minimum) is standard for backpacks; Oxford polyester is cheaper but less tear-resistant.",
            "Yeatru verifies backpack weight capacity by loading and testing before shipment."
        ],
        [
            ("Are backpacks from China good quality?",
             "Quality depends on fabric and components. Yeatru targets 400D+ ripstop or Oxford nylon with YKK zippers — the standard used by Western brands. We verify stitching density, zipper type, and weight capacity during QC."),
            ("What is the MOQ for custom backpacks?",
             "OEM backpacks start at 500 pcs with simple logos; custom designs and colors start at 1,000 pcs. Yeatru can source stock backpacks with your logo at MOQ 100 pcs."),
        ]
    ),
    "bags": (
        "Bags & Luggage",
        "Bags and luggage from China — travel bags, tote bags, cosmetic cases, and luggage sets. Sourced from Zhejiang and Fujian bag factories with customizable branding and materials.",
        [
            "PU leather bags should be at least 0.8mm thick; anything thinner peels within 6–12 months of use.",
            "Hard-shell luggage needs ABS+PC composite (not pure ABS) for impact resistance.",
            "Yeatru verifies zipper pull strength and handle attachment with a 20kg weight test before approval."
        ],
        [
            ("How durable are bags from China?",
             "Very durable when sourced properly. Yeatru requires PU leather minimum 0.8mm thickness, YKK zippers, and reinforced stitching. These standards match or exceed Western mid-market brand quality."),
            ("Can I source custom tote bags for events or promotions?",
             "Yes. MOQ for promotional tote bags is 100 pcs for simple designs. Production time is 7–15 days. Yeatru handles art file conversion, color matching, and express shipping."),
        ]
    ),
    "dog-supplies": (
        "Dog & Pet Supplies",
        "Dog supplies from China — chew toys, leashes, collars, grooming tools, and pet accessories. Sourced from dedicated pet product factories with on-site safety documentation.",
        [
            "Dog chew toys must be non-toxic (FDA LFGB) and not easily breakable into choking-size pieces.",
            "Electronic pet devices (GPS trackers, automatic feeders) need CE/ETL marking and battery safety certification.",
            "Yeatru conducts a tensile strength test on leashes to verify advertised weight limits."
        ],
        [
            ("Are dog toys from China safe?",
             "Yeatru verifies LFGB or FDA material safety declarations for all pet products we source. We also conduct a tensile strength test on chew toys and a size check to verify they meet the target dog size."),
            ("What pet supplies have the best margins?",
             "Chew toys, bandanas, and collar accessories have 50–70% margins with low MOQ (100 pcs). Automatic feeders and GPS trackers have 40–50% margins but higher MOQ (500+)."),
        ]
    ),
    "fitness": (
        "Fitness & Sports Equipment",
        "Fitness and sports equipment from China — resistance bands, yoga mats, massage guns, and gym accessories. Sourced from Zhejiang and Guangdong with customization for branding and material.",
        [
            "Massage guns need CE/ETL safety marks and battery UN38.3 certification. Always request a test report, not just a label.",
            "Resistance band tension is measured in pounds (lb); cheap bands lose 30–40% tension after 100 cycles — specify minimum 80% tension retention.",
            "Yeatru tests resistance band tension with a force gauge before approval."
        ],
        [
            ("Are massage guns from China safe?",
             "When sourced from Yeatru's approved factories, yes. We require CE/ETL marks and verify battery safety (UN38.3). We also test the motor brushless rate — brushless motors last 10x longer than brushed."),
            ("What is the MOQ for fitness equipment?",
             "Resistance bands, yoga mats: 100 pcs. Massage guns: 500 pcs. Fitness equipment is a high-season product — order 2–3 months before Q4 holiday season."),
        ]
    ),
    "outdoor": (
        "Outdoor & Camping",
        "Outdoor and camping products from China — tents, sleeping bags, folding furniture, and camping gear. Sourced from Guangzhou outdoor equipment factories with waterproof and UV-resistant specifications.",
        [
            "Tent fabric must be ≥3000mm waterproof rating; anything below leaks in moderate rain.",
            "Sleeping bags are rated by temperature (comfort/lower limit). Always provide both ratings, not just a single number.",
            "Yeatru conducts a waterproof spray test on tent fabric during QC inspection."
        ],
        [
            ("Are camping tents from China waterproof?",
             "When properly specified, yes. Yeatru targets 3000mm+ waterproof rating with taped seams. We test with a spray test during QC. Avoid tents advertised as 'waterproof' without a stated mm rating."),
            ("What is the lead time for custom camping gear?",
             "Basic tents: 25–35 days. Custom poles or fabric: 35–45 days. Peak season (June–August) adds 10–15 days. Order by March/April for summer season."),
        ]
    ),
    "smart-electronics": (
        "Smart Electronics & IoT",
        "Smart electronics from China — IoT devices, Bluetooth trackers, smart home sensors, and connected gadgets. Sourced from Shenzhen and Dongguan electronics parks with firmware customization capability.",
        [
            "All electronic products with radio frequency need CE RED (EU) or FCC Part 15 (US) certification.",
            "Bluetooth 5.0+ chips from Nordic or TI are more reliable than generic chips — specify chipset in your RFQ.",
            "Yeatru can coordinate firmware updates and beta testing before mass production."
        ],
        [
            ("Are generic smart electronics from China reliable?",
             "With proper supplier vetting, yes. Yeatru works with factories using Nordic/Qualcomm Bluetooth chips instead of generic chips. We also test RF range, battery life, and OTA update capability before approval."),
            ("What certifications do smart electronics need for import?",
             "CE RED (EU), FCC Part 15 (US), RoHS (EU), and LVD/LVD EN (low voltage directive). Yeatru verifies all certifications before factory approval."),
        ]
    ),
    "mobile-accessories": (
        "Mobile Phone Accessories",
        "Mobile phone accessories from China — phone cases, chargers, cables, stands, and screen protectors. Sourced from Shenzhen and Dongguan electronics accessory factories with MOQ as low as 100 pcs for most items.",
        [
            "USB-C cables should be USB 3.0 (SuperSpeed) with E-Marker chip for fast data transfer — cheaper cables are USB 2.0 only.",
            "Wireless chargers need Qi certification (WPC) to avoid compatibility issues with modern phones.",
            "Yeatru verifies cable wire gauge with a micrometer to catch factories substituting 28AWG for advertised 22AWG."
        ],
        [
            ("Are fast chargers from China safe?",
             "Qi-certified and PD-compliant chargers are safe. Yeatru works with WPC-certified factories and verifies PD PDO (power delivery profile) specifications. Non-certified chargers can damage phones."),
            ("What is the MOQ for phone accessories?",
             "Most accessories have MOQ of 100 pcs. Custom mold phone cases start at 500 pcs. Charger adapters and cables start at 300 pcs."),
        ]
    ),
    "screen-protectors": (
        "Screen Protectors & Films",
        "Screen protectors from China — tempered glass, PET films, and privacy protectors. Sourced from Dongguan film-processing factories with customizable sizes and coatings.",
        [
            "Tempered glass protectors must have 9H hardness rating and 0.33mm minimum thickness; thinner glass shatters easily.",
            "Anti-spy privacy protectors use microlouver technology — test viewing angle (30° max side visibility) before approval.",
            "Yeatru verifies glass hardness with a Mohs scratch tester during QC."
        ],
        [
            ("How good is tempered glass from China?",
             "When sourced from Yeatru's approved factories, quality matches Western brand protectors at 30–50% of the price. We verify 9H hardness with a Mohs scratch tester and test breakage resistance."),
            ("Can I get custom size screen protectors?",
             "Yes, MOQ for custom sizes is 300–500 pcs. Lead time: 7–14 days. Yeatru can work with you on unusual devices, foldable phones, or custom tablet sizes."),
        ]
    ),
    "audio-electronics": (
        "Audio Electronics & Headphones",
        "Audio electronics from China — wireless earbuds, speakers, microphones, and audio accessories. Sourced from Shenzhen and Dongguan audio OEM factories.",
        [
            "Bluetooth earbuds with ANC (active noise cancellation) need FCC CE RED certification for radio emissions.",
            "Chipset matters: Qualcomm QCC series delivers lower latency than common AB5636 generic chipsets.",
            "Yeatru tests audio latency, frequency response, and ANC dB attenuation during factory QC."
        ],
        [
            ("Are wireless earbuds from China good quality?",
             "Very good when sourced from Yeatru's approved OEM factories. We target Qualcomm QCC chipsets, test audio latency (<50ms), ANC dB attenuation (≥25dB), and battery life before any factory is approved."),
            ("What is the MOQ for custom wireless earbuds?",
             "Stock earbuds with your logo: 300 pcs. Custom mold and design: 500+ pcs. Development time: 2–3 weeks for custom design, 20–30 days for production."),
        ]
    ),
    "microphones-audio": (
        "Microphones & Audio Recording",
        "Microphones and audio recording equipment from China — condenser mics, wireless mics, USB podcast mics, and audio accessories. Sourced from Guangzhou and Shenzhen audio OEM factories.",
        [
            "USB microphones use UAC protocol — verify class-compliant USB 2.0/3.0 driver compatibility before sourcing.",
            "Wireless microphones use UHF (470–900MHz) or 2.4GHz ISM band; UHF offers better range through walls.",
            "Yeatru tests SNR (signal-to-noise ratio) and frequency response curve during factory QC."
        ],
        [
            ("Are USB microphones from China plug-and-play on all computers?",
             "Class-compliant USB UAC microphones work on Windows, macOS, Linux, and PS5 without drivers. Yeatru verifies UAC class compliance during factory testing."),
            ("What certifications do wireless microphones need?",
             "EU: CE RED (radio directive). US: FCC Part 73 (broadcast) or Part 90 (GMRS/land mobile). 2.4GHz ISM band mics (most consumer models) only need FCC Part 15 / CE RED."),
        ]
    ),
    "audio-video": (
        "Audio & Video Equipment",
        "Audio and video equipment from China — speakers, home theater accessories, projector accessories, and video production gear. Sourced from Guangdong and Shenzhen electronics OEM factories.",
        [
            "HDMI cables must be HDMI 2.0 (18Gbps) for 4K@60Hz; cheaper cables are HDMI 1.4 only.",
            "Bluetooth speakers need FCC Part 15 / CE RED certification.",
            "Yeatru tests HDMI bandwidth and Bluetooth audio range during factory QC."
        ],
        [
            ("How do I verify HDMI cable quality from China?",
             "Yeatru uses a bandwidth tester to verify cables can carry 18Gbps (HDMI 2.0) or 48Gbps (HDMI 2.1). Generic cables marked 'HDMI 2.0' often only deliver 5–8Gbps."),
            ("Can I get custom branded speakers?",
             "Yes. MOQ for custom Bluetooth speakers is 300–500 pcs depending on design complexity. Lead time: 20–30 days. Yeatru handles logo printing, packaging design, and firmware customization."),
        ]
    ),
    "auto-accessories": (
        "Auto Accessories & Car Parts",
        "Auto accessories from China — car electronics, interior accessories, exterior modifications, and car cleaning supplies. Sourced from Guangzhou automotive parts market and Dongguan electronics factories.",
        [
            "Car electrical accessories (chargers, dash cams) need CE/FCC marking and may need E-Mark (R10) for electromagnetic compatibility.",
            "LED car lights need E-Mark R112 / R148 marking for road use — unmarked LEDs are illegal on EU/US registered vehicles.",
            "Yeatru verifies electrical safety and EMC compliance before factory approval."
        ],
        [
            ("Are auto accessories from China legal in the EU/US?",
             "Accessories sold in the EU/US need specific markings: CE/E-Mark for EU, DOT/SAE for US. Yeatru verifies all required compliance before sourcing and can coordinate testing for compliance."),
            ("What is the MOQ for auto accessories?",
             "Small interior accessories: 100 pcs. Electronic car gadgets (dash cams, chargers): 300 pcs. LED headlights: 500 pcs (due to E-Mark certification)."),
        ]
    ),
    "auto-repair-tools": (
        "Auto Repair & Hand Tools",
        "Auto repair tools from China — hand tools, diagnostic accessories, and workshop equipment. Sourced from Zhejiang hardware tool factories with hardness and torque specifications verified during QC.",
        [
            "Socket and wrench steel must be Chrome Vanadium (CR-V) 50-55 HRC; generic carbon steel snaps under torque.",
            "Impact sockets must be chrome-molybdenum (CR-Mo) for impact gun use.",
            "Yeatru verifies steel hardness with a Rockwell C-scale tester during QC."
        ],
        [
            ("Are hand tools from China durable?",
             "When specified correctly — yes. Yeatru targets CR-V steel (50-55 HRC) which matches the specification of most Western brands. We verify hardness with a Rockwell tester during QC."),
            ("What is the MOQ for custom branded tools?",
             "Socket sets and tool kits: 100 pcs. Individual tools: 500 pcs. Packaging design customization: add 7–14 days to lead time."),
        ]
    ),
    "lighting": (
        "Lighting & LED",
        "LED lighting from China — LED strips, bulbs, fixtures, and smart lighting. Sourced from Zhongshan (the world's largest lighting manufacturing hub) with customized color temperature, CRI, and driver specifications.",
        [
            "LED bulbs need CE (EU) / FCC Part 15 (US) for EMI compliance. External drivers need LVD (EU) / UL (US) safety marks.",
            "LED strip CRI (Color Rendering Index) — ≥90 CRI is required for residential use. Generic 'high CRI' strips often fudge the number.",
            "Yeatru verifies CRI with a spectrophotometer during QC inspection."
        ],
        [
            ("Are cheap LED bulbs from China safe?",
             "With proper factory vetting — yes. Yeatru targets LED chips from Cree, OSRAM, or Epistar (not generic 'super bright' unbranded chips). We verify CRI and EMI compliance before approval."),
            ("What certifications do LED products need?",
             "EU: CE LVD (safety) + CE EMC (electromagnetic compatibility). US: FCC Part 15 (EMI) + UL (safety, optional but recommended). Yeatru verifies all certifications before sourcing."),
        ]
    ),
    "locks": (
        "Locks & Security Hardware",
        "Locks and security hardware from China — padlocks, smart locks, door hardware, and safety locks. Sourced from Guangdong lock manufacturing factories with customization for keying and branding.",
        [
            "Smart electronic locks need CE/FCC marking and may need ANSI/BHMA Grade certification (US).",
            "Residential door locks should meet ANSI Grade 2 minimum; Grade 1 is commercial/industrial.",
            "Yeatru tests lock picking resistance with standard lock tools during QC."
        ],
        [
            ("Are smart locks from China secure?",
             "When sourced from Yeatru's approved factories, security meets ANSI Grade 2 standards. We verify that Bluetooth/WiFi smart locks use encrypted communication and test lock picking resistance with standard tools."),
            ("What is the MOQ for custom locks?",
             "Standard padlocks: 100 pcs. Electronic smart locks: 300 pcs. Custom keying (master key systems): add 7–14 days to lead time."),
        ]
    ),
    "hardware": (
        "Hardware & Fasteners",
        "Hardware and fasteners from China — screws, bolts, brackets, hinges, and construction hardware. Sourced from Zhejiang hardware manufacturing factories with galvanized or powder-coated finishes.",
        [
            "Outdoor hardware must be hot-dip galvanized (not electroplated zinc) for corrosion resistance (500+ hours salt spray).",
            "Grade 8 bolts use SAE J429 specification — verify markings '8' on bolt head before bulk purchase.",
            "Yeatru tests corrosion resistance with 72-hour salt spray test during QC."
        ],
        [
            ("How long do galvanized screws from China last outdoors?",
             "Properly hot-dip galvanized screws last 20–30 years outdoors. Cheaper electroplated zinc screws last only 2–5 years. Yeatru verifies galvanizing thickness with a magnetic coating gauge."),
            ("What is the MOQ for custom hardware?",
             "Standard screws and bolts: 1,000+ pcs (factory minimum). Custom sizes or materials (stainless, titanium): 5,000+ pcs. Stock hardware with custom packaging: 100 pcs."),
        ]
    ),
    "machinery": (
        "Small Machinery & Equipment",
        "Small machinery and equipment from China — compressors, generators, workshop equipment, and specialized tools. Sourced from Jiangsu and Shandong machinery manufacturers with after-sales support coordination.",
        [
            "Industrial machinery requires CE marking (EU) / UL listing (US) and may need Machinery Directive 2006/42/EC documentation.",
            "Engines and motorized equipment need EPA (US) or Euro (EU) emissions certification.",
            "Yeatru coordinates machinery testing and compliance documentation before factory approval."
        ],
        [
            ("Is industrial machinery from China compliant with EU/US regulations?",
             "With the right factory and testing, yes. Yeatru only works with factories that can provide CE/UL documentation for their machinery. We also coordinate third-party compliance testing if needed."),
            ("What warranty do Chinese machinery factories provide?",
             "Most factories offer 12-month warranty. Yeatru co-ordinates spare parts shipping and technical support for our clients. Custom machinery often includes on-site setup support."),
        ]
    ),
    "photography": (
        "Photography & Studio Equipment",
        "Photography and studio equipment from China — lighting kits, backdrops, camera accessories, and photo booth gear. Sourced from Shenzhen electronics factories and Yiwu photo accessory wholesalers.",
        [
            "LED studio lights need CE/FCC marking; COB LEDs from Cree/OSRAM are more durable than generic chips.",
            "Reflectors and softboxes should use heat-resistant material (≥200°C) to avoid fire risk with high-powered flashes.",
            "Yeatru verifies lighting color accuracy with a color meter during QC."
        ],
        [
            ("Are studio lighting kits from China good quality?",
             "Very competitive at 30–50% below Western brand prices. Yeatru targets Cree/OSRAM COB LEDs with ≥95 CRI color accuracy. We test color temperature accuracy and flicker during QC."),
            ("What is the MOQ for custom photography accessories?",
             "Most photo accessories have MOQ of 100–300 pcs. Custom printed backdrops: 50+ pcs. Studio lighting kits: 100 pcs."),
        ]
    ),
    "musical-instruments": (
        "Musical Instruments & Accessories",
        "Musical instruments and accessories from China — beginner instruments, studio gear, and music accessories. Sourced from Guangzhou and Shenzhen with customization for branding and specification.",
        [
            "Wood instruments (guitars, violins) should use kiln-dried (8–12% moisture) spruce/maple — green wood warps over time.",
            "Electronic instruments need CE/FCC marking for RF emissions and electrical safety.",
            "Yeatru verifies wood moisture content with a pinless meter during factory QC."
        ],
        [
            ("Are beginner guitars from China good quality?",
             "For beginners and intermediate players, very good value. Yeatru targets kiln-dried wood (8–12% moisture), medium-action setup, and proper intonation. We check each instrument before approval."),
            ("Can I get custom branded musical instruments?",
             "Yes. MOQ: acoustic guitars 500 pcs, electric guitars 300 pcs, wind instruments 100 pcs. Lead time: 4–8 weeks depending on wood type and finish."),
        ]
    ),
    "stationery": (
        "Stationery & Office Supplies",
        "Stationery and office supplies from China — notebooks, pens, office accessories, and desk organizers. Sourced from Yiwu stationery wholesale market and Zhejiang paper/pen factories.",
        [
            "Printed notebooks need FSC-certified paper to meet EU environmental regulations.",
            "Pen ink quality varies: alcohol-based markers may bleed through non-coated paper — specify paper gsm and coating.",
            "Yeatru conducts ink bleed and page count tests on notebooks during QC."
        ],
        [
            ("What's the paper quality of notebooks from China?",
             "Yeatru targets 80–100gsm FSC-certified offset paper for notebooks — no bleed-through with standard ballpoint or gel pens. We test ink bleed with a 24-hour soak test during QC."),
            ("Can I custom print notebooks with my brand?",
             "Yes. MOQ for custom printed notebooks: 300 pcs with basic printing, 500 pcs for full-color. Lead time: 10–15 days. Yeatru handles art file conversion and print color matching."),
        ]
    ),
    "fans": (
        "Fans & Ventilation",
        "Fans and ventilation from China — electric fans, cooling towers, exhaust fans, and specialty cooling equipment. Sourced from Guangdong fan and motor manufacturing factories.",
        [
            "All electric fans need CE (EU) / UL (US) safety marking and RoHS compliance (EU).",
            "Ceiling fans: 52-inch is the standard for living rooms; blade pitch (14–16°) determines airflow.",
            "Yeatru tests motor lifespan (≥50,000 hours at rated load) during factory QC."
        ],
        [
            ("How durable are electric fans from China?",
             "Brushless DC motors from reputable factories last 50,000+ hours. Yeatru targets Shenzhen-designed motors with this specification. We test thermal shutdown protection and motor noise level."),
            ("What certifications do fans need for import?",
             "EU: CE LVD + EMC + RoHS. US: UL 507 (portable fans) or UL 60335 (household appliances). Yeatru verifies all certifications before factory approval."),
        ]
    ),
    "ofc": (
        "Fitness & Yoga",
        "Fitness accessories from China — yoga mats, resistance bands, foam rollers, and workout equipment. Sourced from Zhejiang PVC and TPE rubber factories and Guangdong foam manufacturers.",
        [
            "Yoga mats should use TPE (environmentally friendly) or NBR rubber; avoid PVC mats (toxic when burned, slippery when warm).",
            "Eco-friendly options: natural rubber or jute mats, but they cost 2–3x more than TPE.",
            "Yeatru conducts a slip-resistance and rebound test on foam rollers during QC."
        ],
        [
            ("Are yoga mats from China eco-friendly?",
             "TPE (thermoplastic elastomer) mats are biodegradable and PVC-free. Yeatru exclusively sources TPE or natural rubber yoga mats. We avoid PVC which is non-biodegradable and may leach chemicals."),
            ("What is the MOQ for custom branded yoga mats?",
             "MOQ for custom logo yoga mats is 300–500 pcs. Custom colors and thickness: 500+ pcs. Lead time: 15–25 days."),
        ]
    ),
    "other": (
        "Other Products & Accessories",
        "Other miscellaneous products and accessories from China — unique gadgets, seasonal items, and hard-to-find products. Yeatru has access to the full Yiwu International Trade City with over 75,000 wholesale stalls and can source any product category.",
        [
            "Yeatru has connections to all 75,000+ Yiwu wholesale stalls and can source nearly any product category on request.",
            "Miscellaneous items ship well as supplement cargo to fill LCL container space.",
            "Contact us for custom sourcing requests for items not in our standard catalog."
        ],
        [
            ("Can Yeatru source a specific product I need that's not in the catalog?",
             "Yes. Email us or use our Request Quote form with a photo and description. We'll source it from Yiwu or Guangzhou wholesale markets and provide a quote within 24–72 hours."),
            ("What is the MOQ for custom-sourced items?",
             "It depends on the product. Most Yiwu market items have MOQ of 100 pcs. Factory-direct items typically start at 500 pcs. Yeatru can broker trial orders at reduced MOQ for most items."),
        ]
    ),
    "swimwear": (
        "Swimwear & Beachwear",
        "Swimwear and beachwear from China — swimsuits, bikinis, swim trunks, and beach accessories. Sourced from Guangdong swimwear factories with customization for print, fabric, and sizing.",
        [
            "Swimwear fabric: 82% polyester + 18% elastane is the standard (chlorine-resistant, stretches well). Avoid 100% polyester swimwear (no stretch).",
            "Custom digital print swimwear MOQ: 500 pcs (print setup cost included).",
            "Yeatru verifies UV resistance (UPF 50+) and chlorine resistance with accelerated tests."
        ],
        [
            ("Does swimwear from China fit US/EU sizes?",
             "Chinese factories use the same sizing charts as global brands, but always request a size chart with body measurements in centimeters. Yeatru has factories that specialize in US/EU sizing."),
            ("What certifications do swimwear brands need?",
             "Garment dyeing facilities should be OEKO-TEX Standard 100 certified (no harmful chemicals). Yeatru verifies dyeing compliance and can provide test reports on request."),
        ]
    ),
}

# Fallback for categories not explicitly listed
DEFAULT_CATEGORY_INFO = (
    None, None, None
)


def generate_content_block(slug, display_name, faq_questions):
    """Generate the HTML content block + FAQPage JSON-LD for a category."""
    readable, intro, considerations, faqs = faq_questions

    # Build the text content block to insert before product grid
    faq_html_pairs = []
    for q, a in faqs:
        faq_html_pairs.append((q, a))

    content_html = f'''<section aria-label="sourcing guide" class="mt-4 mb-5">
 <div class="row g-4 align-items-start">
  <div class="col-lg-7">
   <h2 class="h4 mb-3">Why Source {readable} from China</h2>
   <p>{intro}</p>
   <h2 class="h4 mt-4 mb-3">Key Considerations for {readable} Sourcing</h2>
   <ul class="mb-0">
'''
    for c in considerations:
        content_html += f'   <li class="mb-2">{c}</li>\n'

    content_html += f'''   </ul>
  </div>
  <div class="col-lg-5">
   <aside class="border rounded-3 p-3 bg-light">
    <h3 class="h6 mb-2"><i class="fa-solid fa-calculator me-1"></i> Quick Reference</h3>
    <table class="table table-sm table-borderless mb-0 small">
     <tbody>
      <tr><th scope="row" class="text-muted fw-normal">Primary sourcing cities</th><td>Yiwu · Guangzhou · Zhejiang</td></tr>
      <tr><th scope="row" class="text-muted fw-normal">Typical MOQ</th><td>100–500 pcs</td></tr>
      <tr><th scope="row" class="text-muted fw-normal">Production lead time</th><td>10–25 days</td></tr>
      <tr><th scope="row" class="text-muted fw-normal">QC standard</th><td>AQL 2.5 pre-shipment</td></tr>
      <tr><th scope="row" class="text-muted fw-normal">Shipping</th><td>DDP to 41 countries</td></tr>
     </tbody>
    </table>
   </aside>
  </div>
 </div>

 <h2 class="h4 mt-5 mb-3">Frequently Asked Questions about {readable} from China</h2>
'''

    for i, (q, a) in enumerate(faq_html_pairs, 1):
        content_html += f' <p><strong>{i}. {q}</strong></p>\n'
        content_html += f' <p>{a}</p>\n'

    content_html += '</section>\n'

    # Build FAQPage JSON-LD
    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": a
                }
            }
            for q, a in faqs
        ]
    }

    schema_html = f'\n<script type="application/ld+json">{json.dumps(faq_schema, ensure_ascii=False)}</script>\n'

    return content_html, schema_html


def process_category(filepath):
    """Add content + FAQPage schema to a single category file."""
    slug_match = re.search(r'category-([a-z0-9-]+)\.html', filepath)
    if not slug_match:
        return None
    slug = slug_match.group(1)

    cat_info = CATEGORY_INFO.get(slug)
    if cat_info is None:
        print(f"  SKIP {slug} — no category-specific content")
        return None

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if FAQPage schema already exists
    if 'FAQPage' in content:
        print(f"  SKIP {slug} — FAQPage already present")
        return None

    # Extract display name from H1
    h1_match = re.search(r'<h1[^>]*>([^<]+)</h1>', content)
    display_name = h1_match.group(1).replace(' — Wholesale China Sourcing Catalog', '') if h1_match else slug

    content_block, schema_block = generate_content_block(slug, display_name, cat_info)

    # Insert content before product grid
    # Pattern: find </header> followed by whitespace then <section aria-label="product grid"
    insert_pattern = re.compile(r'(</header>)(\s*<section aria-label="product grid")', re.DOTALL)
    if not insert_pattern.search(content):
        print(f"  SKIP {slug} — cannot find product grid insertion point")
        return None

    content = insert_pattern.sub(r'\1' + '\n\n' + content_block + r'\2', content, count=1)

    # Insert FAQPage schema before </head>
    head_pattern = re.compile(r'(</head>)')
    if head_pattern.search(content):
        content = head_pattern.sub(schema_block + '\\1', content, count=1)
    else:
        print(f"  WARN {slug} — cannot find </head> for schema insertion")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  OK   {slug} — content + FAQPage added")
    return slug


def main():
    category_files = sorted(glob.glob('/workspace/category-*.html'))
    print(f"Found {len(category_files)} category files\n")

    results = []
    for f in category_files:
        slug = process_category(f)
        if slug:
            results.append(slug)

    print(f"\nDone. Successfully updated {len(results)} / {len(category_files)} category pages.")

    # List any categories missing from CATEGORY_INFO
    covered = set(CATEGORY_INFO.keys())
    all_slugs = {re.search(r'category-([a-z0-9-]+)\.html', os.path.basename(f)).group(1) for f in category_files}
    missing = all_slugs - covered
    if missing:
        print(f"\nCategories with no specific content (SKIPPED): {sorted(missing)}")


if __name__ == '__main__':
    main()

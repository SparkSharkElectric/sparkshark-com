"""
extract-copy-drafts.py — generates clean markdown copy drafts from build.py.

One .md file per page in /copy-drafts/. Edit those files; on return I'll merge
the edits back into build.py and regenerate the site.

Format per file:
  # TITLE (browser tab)
  # META DESCRIPTION (Google snippet)
  # H1
  # HERO SUBTITLE
  # INTRO
  # SECTIONS (h2 + bullets)
  # FAQ (Q/A pairs)
"""
import os, sys, re
from pathlib import Path

# import build.py to get the page definitions
sys.path.insert(0, str(Path(__file__).parent))
import build

OUT = Path(__file__).parent / "copy-drafts"
OUT.mkdir(exist_ok=True)

def write_draft(filename, lines):
    p = OUT / filename
    p.write_text("\n".join(lines), encoding="utf-8")
    print(f"  ✅ {filename}")

def strip_html(s):
    """Strip HTML tags for clean editing."""
    s = re.sub(r'<a[^>]*href="([^"]+)"[^>]*>([^<]+)</a>', r'\2 [\1]', s)
    s = re.sub(r'<strong>([^<]+)</strong>', r'**\1**', s)
    s = re.sub(r'<em>([^<]+)</em>', r'_\1_', s)
    s = re.sub(r'<[^>]+>', '', s)
    s = s.replace('&amp;', '&').replace('&mdash;', '—').replace('&rdquo;', '"').replace('&ldquo;', '"')
    return s.strip()


def draft_page(filename, slug, title, desc, h1, sub, intro, sections=None, faqs=None, notes=None):
    lines = [
        f"# COPY DRAFT — {slug}",
        f"# File: copy-drafts/{filename}",
        "",
        "<!-- INSTRUCTIONS -->",
        "<!-- Edit anything below. Keep the section headers (===) intact so I can re-merge cleanly. -->",
        "<!-- Lines starting with <!-- are comments and won't appear on the site. -->",
        "<!-- Bullets become <li>. **bold** stays bold. Links: word [https://url] format. -->",
        "<!-- When done, hand me the edited file(s) and I'll regenerate the site. -->",
        "",
    ]
    if notes:
        lines.append(f"<!-- NOTE: {notes} -->")
        lines.append("")

    lines.extend([
        "=== TITLE (browser tab — 50–60 chars ideal, max 60) ===",
        title,
        "",
        "=== META DESCRIPTION (Google snippet — 140–160 chars) ===",
        desc,
        "",
        "=== H1 (main page heading — visible on page) ===",
        h1,
        "",
    ])
    if sub:
        lines.extend([
            "=== HERO SUBTITLE (1–2 sentences under H1) ===",
            sub,
            "",
        ])
    if intro:
        lines.extend([
            "=== INTRO PARAGRAPH (lede paragraph at top of body) ===",
            intro,
            "",
        ])
    if sections:
        for h2, items in sections:
            lines.append(f"=== SECTION: {h2} ===")
            for it in items:
                clean = strip_html(it)
                lines.append(f"- {clean}")
            lines.append("")
    if faqs:
        lines.append("=== FAQ ===")
        for q, a in faqs:
            lines.append(f"Q: {q}")
            lines.append(f"A: {a}")
            lines.append("")
    write_draft(filename, lines)


# ============================================================================
# 1. HOMEPAGE
# ============================================================================
draft_page(
    "01-homepage.md",
    slug="/  (homepage)",
    title="Spark Shark Electric | Licensed Electrician in Moore & OKC | 24/7 Service",
    desc=f"Licensed residential electricians in Moore, OK and the Oklahoma City metro. 24/7 emergency service, flat-rate pricing, free safety inspection. Call {build.BRAND['phone_display']}.",
    h1="Residential Electricians in Oklahoma City & Moore",
    sub="Residential electrical help for Oklahoma City, Moore, and the OKC metro. Repairs, panels, generators, inspections, outlets, and emergency electrical issues — answered 24/7.",
    intro="",
    sections=[
        ("HERO TRUST POINTS (3 short bullets, shown on hero)", [
            "Flat-rate pricing",
            "Licensed Oklahoma electricians",
            "Available 24/7",
        ]),
        ("PROOF BAR (5 short proof statements between hero and emergency)", [
            "Licensed Oklahoma electricians",
            "Flat-rate pricing",
            "Background-checked team",
            "Written options before work begins",
            "Available 24/7",
        ]),
        ("EMERGENCY CALLOUT (above services grid)", [
            "Eyebrow: Electrical emergency?",
            "H2: Burning smell, hot panel, sparking outlet, or sudden power loss? Call now.",
        ]),
        ("SERVICES GRID HEADER", [
            "Eyebrow: Services",
            "H2: What we work on",
            "Subhead: Residential-only electrical work. We do this every day, in your neighborhood.",
        ]),
        ("SERVICES GRID — 8 cards (each = title + 1 sentence)", [
            "Electrical Panel Upgrades — Replace outdated panels and fuse boxes. Bring your home up to current code, safely.",
            "Generator Installation — Whole-home standby generators sized for your load. Permitted, professionally commissioned.",
            "Emergency Service — Burning smells, hot panels, sparking outlets — answered 24/7, dispatched to a licensed electrician.",
            "Repair & Service — Flickering lights, dead outlets, repeated breaker trips, GFCI faults. Diagnosed and fixed.",
            "Installation — Whole-home rewiring, new circuits, smart-home wiring, EV charger circuits.",
            "Safety Inspections — Full home electrical safety inspection. Free with every service visit.",
            "EV Charger Installation — Level 2 (240V) home EV charging stations. Permit-pulled, code-compliant.",
            "Lighting & Outlets — Indoor and outdoor lighting, ceiling fans, switches and outlets.",
        ]),
        ("WHY US HEADER", [
            "Eyebrow: Why us",
            "H2: How we work",
            "Subhead: Honest pricing, clean work, no surprises. The job you called for is the job we quote.",
        ]),
        ("WHY US — 4 numbered items (title + sentence)", [
            "1. Flat-rate pricing — Written estimate before any work begins. No trip charges, no diagnostic fees, no shop-supplies line item.",
            "2. Background-checked team — Licensed, background-checked electricians. No subcontractors for residential service work.",
            "3. Available 24/7 — We answer the phone any time, every day. Emergency service routed to a licensed electrician.",
            "4. Cleanliness guarantee — Property left cleaner than found. Technicians bring a shop vacuum to every job.",
        ]),
        ("SERVICE AREA (15 cities — chip row)", [
            "Eyebrow: Service area",
            "H2: OKC Metro & surrounding cities",
            "Subhead: Residential electrical service throughout the Oklahoma City metropolitan area.",
            "Cities: Oklahoma City · Moore · Norman · Edmond · Yukon · Mustang · Bethany · Midwest City · Del City · Choctaw · Newcastle · Piedmont · Nichols Hills · The Village · Warr Acres",
        ]),
        ("FINAL CTA", [
            "Headline: Need a residential electrician today?",
            "Subhead: Flat-rate pricing. Written options before work begins. Available 24/7.",
            "Primary button: Call (405) 436-4776",
            "Secondary button: Schedule Online (opens ServiceTitan scheduler)",
            "License footer: Oklahoma Electrical License #163603 · Licensed, bonded, insured · BBB Accredited since 2025",
        ]),
    ],
)


# ============================================================================
# 2. SERVICE PAGES — pull from build.SERVICE_PAGES
# ============================================================================
service_filenames = {
    "/electrical-panels/": "02-electrical-panels.md",
    "/generators/": "03-generators.md",
    "/services/emergency-electrician/": "04-emergency-electrician.md",
    "/electrical-repair-and-service/": "05-electrical-repair-and-service.md",
    "/electrical-installation/": "06-electrical-installation.md",
    "/electrical-inspection-services/": "07-electrical-inspection-services.md",
    "/smoke-detectors/": "08-smoke-detectors.md",
    "/switches-and-outlets/": "09-switches-and-outlets.md",
    "/electrician-for-outdoor-lighting/": "10-outdoor-lighting.md",
    "/ev-charger-installation/": "11-ev-charger-installation.md",
    "/smart-home-installation/": "12-smart-home-installation.md",
    "/ceiling-fans/": "13-ceiling-fans.md",
    "/indoor-lighting-installation/": "14-indoor-lighting-installation.md",
    "/residential-electrical-solutions/": "15-residential-electrical-solutions.md",
}

for sp in build.SERVICE_PAGES:
    fname = service_filenames.get(sp["path"], f"99-unknown-{sp['path'].strip('/').replace('/','-')}.md")
    notes = None
    if sp["path"] == "/services/emergency-electrician/":
        notes = "PRIORITY PAGE — currently #2 organic for 'emergency electrician Oklahoma City'. Edit with care; preserve keywords (emergency electrician, Moore, OKC, 24/7) for SEO."
    draft_page(
        fname,
        slug=sp["path"],
        title=sp["title"],
        desc=sp["desc"],
        h1=strip_html(sp["h1"]),
        sub=sp["sub"],
        intro=sp["intro"],
        sections=sp["sections"],
        faqs=sp.get("faqs"),
        notes=notes,
    )


# ============================================================================
# 3. INFO + LEGAL PAGES (hand-built copy)
# ============================================================================
draft_page(
    "16-services-index.md",
    slug="/services/",
    title="Electrical Services | Residential & Emergency | Spark Shark Electric",
    desc="Full list of residential electrical services in OKC and Moore — panels, generators, repair, installation, inspections, lighting, EV chargers, 24/7 emergency.",
    h1="Electrical Services",
    sub="Everything we do — residential-only, licensed, flat-rate priced, available 24/7 for emergencies.",
    intro="",
    sections=[
        ("(This page reuses the same SERVICES GRID + EMERGENCY CALLOUT + AREA CHIPS as homepage. Edit the homepage version of those — they share copy.)", [
            "No standalone copy on this page beyond the page hero (above)."
        ]),
    ],
)

draft_page(
    "17-about-us.md",
    slug="/about-us/",
    title="About Spark Shark Electric | Licensed OKC & Moore Electricians",
    desc="About Spark Shark Electric — licensed residential electrical contractor based in Moore, OK. License #163603, BBB Accredited, 24/7 service across the OKC metro.",
    h1="About Spark Shark Electric",
    sub="Residential electrical contractor based in Moore, Oklahoma. Licensed, bonded, insured, BBB Accredited, available 24/7.",
    intro="Spark Shark Electric is a licensed residential electrical contractor serving the Oklahoma City metro from a base in Moore. We focus exclusively on homes — not commercial, not industrial.",
    sections=[
        ("What we do, and what we don't", [
            "We do residential electrical work. Panels, generators, repair, installation, inspections, lighting, EV chargers, smart home, smoke detectors, ceiling fans. Same-day repair, 24/7 emergency. **That's it.**",
            "We don't do commercial buildings. We don't do industrial work. We don't do new ground-up construction directly. The focus is intentional — homes are what we do every day, in the neighborhoods we live in.",
        ]),
        ("Credentials", [
            "**Oklahoma Electrical License #163603** — issued by the Oklahoma Construction Industries Board. Licensed, bonded, insured.",
            "**BBB Accredited Business since July 2025.**",
            "**4.9 rating across 117+ reviews.**",
            "**Background-checked team.** Every technician on staff. No subcontractors for residential service work.",
        ]),
        ("How we price", [
            "Flat-rate. Written down before any work begins. No trip charge, no diagnostic fee, no shop-supplies line item. The job you called for is the job we quote. If something else needs to happen mid-job, we stop, write it up, and you decide.",
        ]),
        ("How to reach us", [
            "Call (405) 436-4776 any time, day or night.",
            "Email theteam@sparkshark.com.",
            "Or use the contact form — we'll respond same-day.",
        ]),
    ],
    notes="This page is a high-leverage copy edit — the place your voice differs most from generic competitors. Be opinionated.",
)

draft_page(
    "18-contact-us.md",
    slug="/contact-us/",
    title="Contact Spark Shark Electric | Free Estimates | Moore & OKC",
    desc="Contact Spark Shark Electric — call (405) 436-4776 24/7 or request service online. Free estimates. Licensed Oklahoma electrical contractor #163603.",
    h1="Contact us",
    sub="Call any time. Email any time. Or send a message — we'll respond same-day.",
    intro="",
    sections=[
        ("DIRECT CONTACT BLOCK", [
            "Phone heading: Phone",
            "Phone number: (405) 436-4776 (linked as tel:+14054364776)",
            "Phone subtext: Available 24/7. We answer the phone.",
            "Email heading: Email",
            "Email: theteam@sparkshark.com",
            "Service area heading: Service area",
            "Service area cities: Moore · Oklahoma City · Norman · Edmond · Yukon · Mustang · Bethany · Midwest City · Del City · Choctaw · Newcastle · Piedmont · Nichols Hills · The Village · Warr Acres",
            "License heading: License",
            "License text: Oklahoma Electrical License #163603 / Licensed, bonded, and insured / BBB Accredited",
        ]),
        ("REQUEST SERVICE FORM", [
            "Form heading: Request service",
            "Form fields: Name (required) · Phone (required) · Email (required) · City (optional) · Message (required, placeholder: 'Briefly describe the electrical issue or project...')",
            "Submit button: Request service",
            "Below button: Or skip the form: call (405) 436-4776 — we answer 24/7.",
            "NOTE: Form action endpoint pending Formspree form ID (Brock to provide before launch).",
        ]),
    ],
)

draft_page(
    "19-reviews.md",
    slug="/reviews/",
    title="Spark Shark Electric Reviews | 4.9 Stars | 117+ Reviews",
    desc="Spark Shark Electric customer reviews — 4.9 stars across 117+ reviews on Google, BBB, and Yelp. Licensed Oklahoma electricians serving the OKC metro.",
    h1="Reviews",
    sub="What homeowners across the OKC metro say about Spark Shark Electric.",
    intro="",
    sections=[
        ("RATING SUMMARY (centered, large)", [
            "Stars: ★★★★★",
            "Number: 4.9",
            "Subtext: across 117+ reviews",
            "Tagline: We don't game review counts. Every review is from a real Oklahoma homeowner. Read them on the platforms below — we link directly so you can verify.",
        ]),
        ("Read reviews on", [
            "Better Business Bureau — BBB Accredited Business since July 2025 [https://www.bbb.org/us/ok/moore/profile/electrical-contractors/spark-shark-electric-0995-90130075]",
            "Yelp [https://www.yelp.com/biz/spark-shark-electric-moore]",
            "Thumbtack [https://www.thumbtack.com/ok/oklahoma-city/electrical-repairs/spark-shark-electric/service/489603470823817221]",
            "Facebook [https://www.facebook.com/sparksharkelectric/]",
        ]),
        ("Why reviews matter to us", [
            "Reviews are a public, verifiable record of the work. We can claim flat-rate pricing, clean job sites, and no-upselling all day on a website — but customer reviews on third-party platforms are the actual evidence. Read them, and call when you're ready.",
        ]),
    ],
    notes="If review count or rating changes, update here AND in build.py BRAND constant (rating='4.9', review_count='117') — schema must match visible page.",
)

# FAQ page
faqs_main = [
    ("Do you offer emergency service?", "Yes. Spark Shark Electric is available 24/7 for electrical emergencies. Call (405) 436-4776 any time."),
    ("Are you licensed and insured?", "Yes. Oklahoma Electrical License #163603. Licensed, bonded, and insured. BBB Accredited."),
    ("Do you charge for estimates?", "No. Every estimate is free and written. We come out, look at the work, and put a flat-rate number in writing before any work begins."),
    ("Do you charge a trip fee or diagnostic fee?", "No. No trip charge, no diagnostic fee, no shop-supplies line item. The number you see is the number you pay."),
    ("What areas do you serve?", "Oklahoma City, Moore, Norman, Edmond, Yukon, Mustang, Bethany, Midwest City, Del City, Choctaw, Newcastle, Piedmont, Nichols Hills, The Village, and Warr Acres."),
    ("Do you do commercial work?", "No. Spark Shark Electric is a residential-only electrical contractor. We focus exclusively on homes."),
    ("Can you upgrade my electrical panel?", "Yes — service replacement, 100A→200A upgrades, sub-panels, code-compliance work. Same-day quote, permit pulled, inspection scheduled."),
    ("Do you install whole-home generators?", "Yes — Generac, Kohler, Briggs & Stratton. Sized to your load, gas line coordinated, automatic transfer switch installed and commissioned."),
    ("Can you install an EV charger?", "Yes — Level 2 (240V) home charging stations, any UL-listed brand. We pull the permit, run the dedicated circuit, install the station, and commission it."),
    ("How fast can you get out?", "Same-day for emergencies and most repair calls. Scheduled work is typically within a few days. We tell you the realistic schedule when you call."),
    ("Are you BBB Accredited?", "Yes — BBB Accredited Business since July 14, 2025."),
    ("How do I pay?", "Cash, check, or credit card. Financing available for larger jobs."),
    ("Do you offer a discount for veterans or first responders?", "Yes — automatic, no haggling. Active-duty military, veterans, and first responders."),
]
draft_page(
    "20-faq.md",
    slug="/frequently-asked-questions/",
    title="FAQ | Residential Electrician Questions | Spark Shark Electric",
    desc="Frequently asked questions for Spark Shark Electric — pricing, licensing, service area, emergency response, and what to expect from a residential electrical visit.",
    h1="Frequently asked questions",
    sub="Common questions homeowners ask before they call.",
    intro="",
    faqs=faqs_main,
    notes="13 Q&As. These also appear in JSON-LD schema for AI/voice search — keep accurate. The 5 homepage FAQs (in JSON-LD `@graph` FAQPage on every page) are a SUBSET; if you change those 5, also update build.py base_schema() FAQPage block.",
)

draft_page(
    "21-privacy-policy.md",
    slug="/privacy-policy/",
    title="Privacy Policy | Spark Shark Electric",
    desc="Privacy policy for Spark Shark Electric. How we collect, use, and protect your information. SMS opt-out instructions and your rights.",
    h1="Privacy Policy",
    sub="How we collect, use, and protect your information.",
    intro="This privacy policy describes how Spark Shark Electric collects, uses, and protects information when you visit sparkshark.com or contact us for service.",
    sections=[
        ("Information we collect", [
            "When you submit our contact form, request service, or call us, we collect the information you provide: name, phone number, email address, service address, and a description of the work. We use this information only to respond to your request and schedule service.",
        ]),
        ("SMS communications", [
            "If you opt in to text messaging from Spark Shark Electric, you'll receive appointment confirmations, service updates, and occasional service-related communications. Message and data rates may apply.",
        ]),
        ("SMS opt-out — DO NOT REMOVE 405-796-8111", [
            "**You can opt out at any time** by replying STOP, CANCEL, or UNSUBSCRIBE to 405-796-8111 and/or by emailing theteam@sparkshark.com. We will remove you from the list within 24 hours.",
        ]),
        ("How we use your information", [
            "We use the information you provide to: respond to your service request, schedule and dispatch a licensed electrician, confirm appointments, follow up after service, and send occasional service-related communications you've opted into. We do not sell, rent, or trade your personal information.",
        ]),
        ("Cookies & analytics", [
            "Our website may use cookies and standard analytics tools (such as Google Analytics) to understand site traffic. These tools collect non-identifying information like browser type, pages visited, and approximate location. You can disable cookies in your browser settings.",
        ]),
        ("Information security", [
            "We take reasonable steps to protect the information you provide. We do not store credit card numbers; payment is processed at the time of service through a secure payment processor.",
        ]),
        ("Third parties", [
            "We may use third-party services to operate the website (web hosting, email, contact-form processing, scheduling). These providers have access only to the information they need to perform their function and are obligated to keep it confidential.",
        ]),
        ("Your rights", [
            "You can request a copy of the information we have about you, ask us to correct it, or ask us to delete it. To make any of these requests, email theteam@sparkshark.com or call (405) 436-4776.",
        ]),
        ("Children", [
            "Our services and website are not directed to children under 13. We do not knowingly collect personal information from children.",
        ]),
        ("Changes to this policy", [
            "We may update this privacy policy from time to time. The 'last updated' date below reflects the most recent revision.",
        ]),
        ("Contact", [
            "For questions about this policy: email theteam@sparkshark.com or call (405) 436-4776.",
        ]),
        ("Footer", [
            "Last updated: 2026-05-08."
        ]),
    ],
    notes="DO NOT REMOVE the 405-796-8111 SMS opt-out reference in the SMS opt-out section. That's the legacy Flanco subscriber list opt-out path and removing it would break TCPA compliance. See project memory.",
)

draft_page(
    "22-terms-and-condition.md",
    slug="/terms-and-condition/",
    title="Terms and Conditions | Spark Shark Electric",
    desc="Terms and conditions for Spark Shark Electric — service agreements, warranty, payment terms, and use of sparkshark.com.",
    h1="Terms and Conditions",
    sub="Service terms, warranty, payment, and website use.",
    intro="",
    sections=[
        ("Service agreement", [
            "When you accept a written estimate from Spark Shark Electric, you authorize us to perform the work described, at the price quoted, in the time frame discussed. Changes to scope require a written change order signed by both parties before additional work proceeds.",
        ]),
        ("Pricing and payment", [
            "We charge flat-rate pricing. Estimates are written and provided before any work begins. There is no trip charge, no diagnostic fee, and no shop-supplies line item. Payment is due upon completion of the work unless other arrangements are made in writing. We accept cash, check, and major credit cards. Financing is available for larger jobs through approved third-party providers.",
        ]),
        ("Warranty", [
            "All workmanship is warranted for one year from the date of service. Parts and equipment we install carry the manufacturer's warranty (typically 1–10 years depending on product). If a covered issue arises, contact us at (405) 436-4776 and we will return at no charge.",
        ]),
        ("Permits and inspections", [
            "Where Oklahoma code requires permits and inspections, we pull the permit and schedule the inspection as part of the flat-rate price. Your project is not 'complete' until the inspection passes.",
        ]),
        ("Cancellation", [
            "You may cancel a scheduled appointment with at least 24 hours notice without charge. Cancellations within 24 hours of the scheduled time may be subject to a small fee at our discretion to cover dispatch and parts ordered.",
        ]),
        ("Limitation of liability", [
            "We carry liability insurance for our work. Our total liability for any claim arising from a service visit is limited to the amount paid for that service, except where applicable law provides otherwise.",
        ]),
        ("Use of sparkshark.com", [
            "Information on sparkshark.com is provided for general informational purposes and may not reflect the most current pricing, availability, or regulations. Nothing on the website constitutes a binding offer; written estimates are the only binding pricing.",
        ]),
        ("Governing law", [
            "These terms are governed by the laws of the State of Oklahoma. Any dispute arising under these terms will be resolved in the courts of Cleveland County, Oklahoma.",
        ]),
        ("Contact", [
            "Questions about these terms: theteam@sparkshark.com or (405) 436-4776.",
        ]),
        ("Footer", [
            "Last updated: 2026-05-08.",
        ]),
    ],
)


# ============================================================================
# 4. LOCATION PAGES (templated — same structure 10 cities + 1 index)
# ============================================================================
draft_page(
    "23-locations-index.md",
    slug="/locations-we-serve/",
    title="Areas We Serve | OKC Metro Cities | Spark Shark Electric",
    desc="Spark Shark Electric serves 15 cities across the Oklahoma City metro — Moore, OKC, Norman, Edmond, Yukon, Mustang, Bethany, Midwest City, Del City, and more.",
    h1="Areas we serve",
    sub="Residential electrical service across the OKC metro. 15 cities, same flat-rate pricing, same 24/7 phone.",
    intro="",
    sections=[
        ("Cities served (with separate landing pages)", [
            "Oklahoma City — /oklahoma-city/",
            "Moore — /moore/",
            "Norman — /locations-we-serve/norman/",
            "Edmond — /locations-we-serve/edmond/",
            "Yukon — /locations-we-serve/yukon/",
            "Mustang — /locations-we-serve/mustang/",
            "Bethany — /locations-we-serve/bethany/",
            "Midwest City — /locations-we-serve/midwest-city/",
            "Del City — /locations-we-serve/del-city/",
            "Newcastle — /locations-we-serve/newcastle/",
        ]),
        ("Cities served (no separate landing page yet)", [
            "Choctaw, Piedmont, Nichols Hills, The Village, Warr Acres — full service, no separate page yet",
        ]),
    ],
)

city_locations = [
    ("24-oklahoma-city.md", "/oklahoma-city/", "Oklahoma City"),
    ("25-moore.md", "/moore/", "Moore"),
    ("26-norman.md", "/locations-we-serve/norman/", "Norman"),
    ("27-edmond.md", "/locations-we-serve/edmond/", "Edmond"),
    ("28-yukon.md", "/locations-we-serve/yukon/", "Yukon"),
    ("29-mustang.md", "/locations-we-serve/mustang/", "Mustang"),
    ("30-bethany.md", "/locations-we-serve/bethany/", "Bethany"),
    ("31-midwest-city.md", "/locations-we-serve/midwest-city/", "Midwest City"),
    ("32-del-city.md", "/locations-we-serve/del-city/", "Del City"),
    ("33-newcastle.md", "/locations-we-serve/newcastle/", "Newcastle"),
]
for fname, path, city in city_locations:
    draft_page(
        fname,
        slug=path,
        title=f"{city} Electricians | Licensed, 24/7 | Spark Shark Electric",
        desc=f"Licensed residential electricians serving {city}, OK. Panel upgrades, generators, repair, 24/7 emergency. Call (405) 436-4776.",
        h1=f"{city} Electricians",
        sub=f"Licensed residential electrical service for {city} and the surrounding OKC metro. Available 24/7.",
        intro=f"We serve {city} every week. Same flat-rate pricing, same licensed team, same 24/7 phone — no zone surcharges, no separate dispatch fees.",
        sections=[
            (f"What we do for {city} homeowners (templated bullet list — feel free to localize)", [
                "Electrical panel upgrades — service replacement, 100A→200A, sub-panels.",
                "Whole-home generators — Generac, Kohler, sized to your load.",
                "Emergency electrical service — burning smells, hot panels, sparking outlets, partial power loss. 24/7.",
                "Electrical repair — flickering lights, dead outlets, breaker trips, GFCI faults.",
                "Installation — new circuits, rewires, smart-home, EV chargers.",
                "Safety inspections — free with any service call.",
            ]),
            (f"Why we cover {city} (currently templated — customize per city if helpful)", [
                f"We're a Moore-based residential electrical contractor. {city} is part of our standard service area — same flat-rate pricing, same response times, same licensed Oklahoma electricians. If you need an electrician in {city}, call (405) 436-4776.",
            ]),
        ],
        notes=f"Currently TEMPLATED across all 10 city pages. Customizing the 'Why we cover {city}' section with city-specific facts (neighborhoods, common house types, common electrical needs) is a high-leverage SEO move — but only if you actually have those facts. Leave templated if not.",
    )


# ============================================================================
# 5. BLOG POSTS (4 KEEP)
# ============================================================================
blog_drafts = [
    ("34-blog-power-out.md", "/2026/05/07/power-out-what-to-do-when-call-electrician/",
     "Power Out? What to Do & When to Call an Electrician | Spark Shark Electric",
     "Storm-and-outage guide for Oklahoma homeowners. What's safe to troubleshoot yourself, what isn't, and when to call a licensed electrician.",
     "Power Out? What to Do & When to Call an Electrician",
     "When the power goes out, the first question is always the same: is this an OG&E problem, or my problem? Here's how to tell — and what's safe to do while you figure it out."),
    ("35-blog-panel-upgrade-signs.md", "/2026/05/07/signs-you-need-electrical-panel-upgrade/",
     "6 Signs You Need an Electrical Panel Upgrade | Spark Shark Electric",
     "Six warning signs your electrical panel needs replacing — including breaker trips, fuse boxes, hot panels, and dangerous brand recalls.",
     "6 Signs You Need an Electrical Panel Upgrade",
     "Most homeowners don't think about their electrical panel until something goes wrong. By that point, the warning signs were usually present for months. Here are the six most common ones."),
    ("36-blog-winter-safety.md", "/2024/01/03/stay-powered-up-essential-electrical-winter-safety-tips/",
     "Essential Electrical Winter Safety Tips | Spark Shark Electric",
     "Winter electrical safety tips for Oklahoma homeowners — space heaters, holiday lights, ice storms, generators, and outage prep.",
     "Essential Electrical Winter Safety Tips",
     "Oklahoma winters bring three reliable electrical risks: ice storms that take down lines, space heaters that overload circuits, and the holiday-light habits we all keep forgetting are dangerous. Here's how to handle all three."),
    ("37-blog-generator-installation.md", "/2024/01/24/why-you-need-a-professional-for-generator-installation/",
     "Why You Need a Professional for Generator Installation | Spark Shark Electric",
     "What goes into a proper whole-home generator install — site prep, fuel, transfer switches, code, and the failure modes of cutting corners.",
     "Why You Need a Professional for Generator Installation",
     "Generator installs are one of those jobs where the difference between 'works' and 'works safely for fifteen years' is mostly invisible — until it isn't. Here's what a proper install actually involves."),
]
for fname, path, title, desc, h1, intro in blog_drafts:
    draft_page(
        fname,
        slug=path,
        title=title,
        desc=desc,
        h1=h1,
        sub="",
        intro=intro,
        sections=[
            ("FULL BODY (current draft — see live preview to view formatted version)", [
                f"Live preview: https://sparksharkelectric.github.io/sparkshark-com{path}",
                "The full body is in build.py inside build_blog_posts(). Edit there OR send me revised body text and I'll merge it.",
            ]),
        ],
        notes="To edit body text, send me a markdown version of the new body and I'll re-merge into build.py.",
    )


# ============================================================================
# 6. BLOGS INDEX
# ============================================================================
draft_page(
    "38-blogs-index.md",
    slug="/blogs/",
    title="Blog | Residential Electrical Tips | Spark Shark Electric",
    desc="Spark Shark Electric blog — practical residential electrical guidance for OKC metro homeowners. Panel upgrades, generators, safety, emergencies.",
    h1="Blog",
    sub="Practical electrical guidance for homeowners in the OKC metro.",
    intro="",
    sections=[
        ("Recent posts (4 KEEP — verbatim ports)", [
            "Power Out? What to Do & When to Call an Electrician — A storm-and-outage guide for OKC homeowners. What's safe to troubleshoot yourself, what isn't.",
            "6 Signs You Need an Electrical Panel Upgrade — The warning signs that mean it's time to replace your panel — and what happens if you don't.",
            "Why You Need a Professional for Generator Installation — Site prep, fuel, transfer switches, and the code requirements that make or break the install.",
            "Essential Electrical Winter Safety Tips — Seasonal advice for keeping your home safe during Oklahoma's winter weather.",
        ]),
    ],
)


# ============================================================================
# 7. INDEX (this file lists all drafts)
# ============================================================================
print()
print(f"\nGenerated drafts in /Users/brock/Projects/sparkshark-com/copy-drafts/")

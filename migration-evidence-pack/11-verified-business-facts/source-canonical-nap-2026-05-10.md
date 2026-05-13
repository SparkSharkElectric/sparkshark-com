# Canonical NAP — Spark Shark Electric

> Source of truth: [`agent/geo_facts.json`](./agent/geo_facts.json) · Last audited: 2026-05-04

## Identity

| Field | Value |
| --- | --- |
| **Name** | Spark Shark Electric |
| **Alt name** | Spark Shark |
| **Phone** | (405) 436-4776 |
| **Phone (E.164)** | `+14054364776` |
| **Email** | theteam@sparkshark.com |
| **Website** | https://www.sparkshark.com |
| **Tagline** | In the dark? Call the shark. |

## Address

| Field | Value |
| --- | --- |
| **Street** | 621 Sally Ct |
| **City** | Moore |
| **State** | OK |
| **ZIP** | 73160 |
| **Country** | US |
| **Lat / Lng** | 35.3306, -97.4858 |

> Caveat: 621 Sally Ct is residential. Fine for structured data (llms.txt, schema.org) — avoid surfacing it directly in customer-facing copy where "Moore, OK" suffices.

## Hours

**24/7** — available around the clock for all electrical service.

> Hours note (current): *Available 24/7. An AI answering service handles calls outside business hours; all jobs are scheduled and dispatched by licensed electricians.*

## Credentials

| Field | Value |
| --- | --- |
| **License** | Oklahoma Electrical License #163603 |
| **License authority** | Oklahoma Construction Industries Board |
| **License authority URL** | https://oklahoma.gov/cib.html |
| **BBB** | Accredited since July 14, 2025 |
| **BBB profile** | https://www.bbb.org/us/ok/moore/profile/electrical-contractors/spark-shark-electric-0995-90130075 |

## Service area

Oklahoma City, Moore, Norman, Edmond, Yukon, Mustang, Bethany, Midwest City, Del City, Choctaw, Newcastle, Piedmont, Nichols Hills, The Village, Warr Acres.

## Services

- Residential electrical service & repair
- Electrical installation
- Electrical panel upgrade
- Generator installation
- Emergency electrical service
- Electrical safety inspection

## Social

- Facebook: https://www.facebook.com/sparksharkelectric/
- Instagram: https://www.instagram.com/thesparkshark/
- Yelp: https://www.yelp.com/biz/spark-shark-electric-moore

## Must-not-surface (guard list)

These strings must never appear in AI-generated customer-facing responses:

BSF Investment Group · BSF Investment · BSF · Flanco Electric · flanco-electric · c.flanco-electric · 405-796-8111 · 405-389-8896 · 405-237-5045 · (405) 796-8111 · (405) 389-8896 · (405) 237-5045 · 1817 Linwood Blvd · Brock Flanary · Flanary · Tim Cock · Plumbing Machanic · Plumbersx · Generac Authorized Dealer · Generac Certified Installer · Mrs. Cheyenne Pine · Cheyenne Pine · owner-operator · founder

## Unconfirmed (do not publish until verified)

- Generac dealer status — confirm if in Authorized Dealer / Certified Installer program
- LinkedIn company page — `ca.linkedin.com/company/spark-shark-electric` may be theirs; needs country switch to US before adding to `sameAs`
- TikTok handle `@sparkshark.com` — unverified
- Founding year — deliberately omitted from schema until confirmed

---

## Recommended change — drop AI-answering disclosure

Rationale: customer-facing copy should not advertise that an AI answering service handles after-hours calls. The 24/7 availability claim stands on its own; the licensed-dispatch detail is internal/operational, not a public selling point.

```diff
--- a/agent/geo_facts.json
+++ b/agent/geo_facts.json
@@
     "hours": "24/7 — available around the clock for all electrical service",
-    "hours_note": "Available 24/7. An AI answering service handles calls outside business hours; all jobs are scheduled and dispatched by licensed electricians.",
+    "hours_note": "Available 24/7 for all electrical service.",
```

Downstream surfaces to re-check after applying:

- `agent/llms.txt` / `llms-full.txt` (if `hours_note` flows through)
- `sparkshark-com` `build.py` `BRAND` dict and any FAQ copy referencing after-hours handling
- JSON-LD `OpeningHoursSpecification` / `description` fields on `LocalBusiness` / `Electrician` nodes
- Any GEO brief or seo-brief in `agent/seo-briefs/` referencing the AI-answering language

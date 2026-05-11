# Deep Research Input Brief — Spark Shark Electric Vercel Migration

**Status:** Local-only. Not committed to git. Inherits `migration-evidence-pack/.gitignore: *`.
**Compiled:** 2026-05-10
**Anchored to main commit:** `ab80db2` — `docs: record Vercel preview validation` (PR #5)
**Evidence pack version:** **v3** (cleaned and rebuilt 2026-05-10 17:47; source: `migration-evidence-pack-cleaned-v3.zip`)
**Authority for cutover:** `docs/migration/launch-gate.md` (unchanged by this brief; **no gate statuses updated; no item marked Approved**).
**Purpose:** Single source of truth for the Deep Research inputs that will inform the v1.1 redirect map, tracking spec, and SEO/GEO posture. Hand this brief (and the v3 evidence pack referenced below) to ChatGPT / Gemini / Perplexity / Claude Research for parallel runs.

---

## 1. Migration summary

| Field | Value |
|---|---|
| Migration | WordPress (WP Engine) → Vercel |
| Production target host | Vercel |
| Production domain (post-cutover) | `https://www.sparkshark.com/` (apex `sparkshark.com` → www at Vercel domain level) |
| **Current DNS state** | **NOT cut over.** Still pointing at WP Engine. |
| Vercel preview alias (main) | `https://sparkshark-com-git-main-spark-shark-electric-2b2f3a3a.vercel.app` |
| Vercel technical foundation | **Green.** Build runs `BASE="" python3 build.py` per `vercel.json` `buildCommand`. Preview-validated 2026-05-10 (see §1.2). |
| Cutover authority | `docs/migration/launch-gate.md` — 9 Brock-owned items. The v3 evidence pack moves 7 items from **Not Provided** to **review-ready**, 1 item to **partially provided**, and 1 item to **deferred**. No gate status is changed by this brief; status changes happen only in `launch-gate.md` and only by Brock. |

### 1.1 Recent PRs

| PR | Subject | What it landed |
|---|---|---|
| **#3** `prelaunch: add Vercel config and DNS launch gate` | Core Vercel deploy contract | `vercel.json` (Option C `buildCommand`, 14 redirect entries, conservative HSTS, conservative asset cache); `docs/migration/launch-gate.md` (permanent repo memory of the Brock-Owned DNS Cutover Launch Gate, 9 gate items); `CLAUDE.md`, `README.md`, `build.py`, `extract-copy-drafts.py` doc + comment edits to switch the canonical hosting story to Vercel. |
| **#4** `prelaunch: use 301 status codes for Vercel redirects` | Redirect semantics correction | Replaced `"permanent": true` (HTTP 308) with `"statusCode": 301` on all 14 redirect entries in `vercel.json`. 308 preserves request method; 301 is what SEO migrations want. |
| **#5** `docs: record Vercel preview validation` | Preview validation memory | New `docs/migration/vercel-preview-validation.md` (248 lines) recording the first successful preview validation pass; +1 bullet to `docs/migration/launch-gate.md` Related-documents section. **Zero gate statuses changed.** |

### 1.2 Vercel preview validation — what's already proven

- All key paths return HTTP 200: `/`, `/css/site.css`, `/js/site.js`, `/img/logo.png`, `/sitemap.xml`, `/robots.txt`, plus 13 interior pages.
- `/sparkshark-com` leakage check: **0 matches** in production HTML — Option C build correctly produces root-relative asset paths.
- 11 safe-known redirects return **HTTP 301** with the expected `Location` header.
- Conservative security headers present: HSTS `max-age=31536000` (no preload, no includeSubDomains), X-Content-Type-Options, X-Frame-Options, Referrer-Policy, Permissions-Policy.
- Asset cache: `public, max-age=3600, must-revalidate` (conservative; filenames are not content-hashed).
- HTML cache: `public, max-age=0, must-revalidate`.
- `sitemap.xml` URL count: **40** (50 `index.html` files minus 10 redirect-stub URLs that `vercel.json` 301s — excluding stubs from the sitemap is correct).
- `robots.txt` returns 200, no Disallow rules, points to `https://www.sparkshark.com/sitemap.xml`.

Full record: `docs/migration/vercel-preview-validation.md`.

### 1.3 What DNS cutover would still require

DNS may not flip until **all 9 launch-gate items** are **Approved** or **Not Applicable** with written reason. Only Brock can mark items Approved or Not Applicable. This brief does not change any gate status; v3 evidence moves multiple items into review-ready territory, but reviewer approval is still required.

---

## 2. Evidence inventory by launch-gate item (v3 state)

Inventory reflects the v3 evidence pack. Reviewer notes are factual; **no item is marked Approved here.** Approval decisions happen only in `docs/migration/launch-gate.md` by Brock.

### Gate #1 — GSC Pages export — **Present / review-ready**
- **Files (v3):**
  - `04-google-search-console/01-performance-last-12-months/gsc-performance-pages-last-12-months.csv` (39 rows + header)
  - Sibling exports for Countries, Devices, Filters, Search appearance, daily Chart, and Queries (gate #2)
- **Reviewer note:** Filter window is now explicit in the filename (last 12 months). Pages export is machine-readable, sufficient for landing-page analysis. Reviewer must still confirm before Approved.

### Gate #2 — GSC Queries export — **Present / review-ready**
- **Files (v3):**
  - `04-google-search-console/01-performance-last-12-months/gsc-performance-queries-last-12-months.csv` (913 rows + header)
- **Reviewer note:** Substantial query data, 12-month window. Sufficient for query-share, opportunity, and ranking analysis. Reviewer must still confirm before Approved.

### Gate #3 — GSC Indexed / Not Indexed — **Present / review-ready**
- **Files (v3):**
  - `04-google-search-console/02-indexing-summary/` — `critical-issues-summary.csv`, `non-critical-issues-summary.csv`, `summary-chart.csv`, `summary-metadata.csv`
  - `04-google-search-console/03-indexed-pages/` — chart, metadata, and `urls.csv`
  - `04-google-search-console/04-crawled-currently-not-indexed/` — chart, metadata, and `urls.csv`
  - `04-google-search-console/05-discovered-currently-not-indexed/` — chart, metadata, and `urls.csv`
  - `04-google-search-console/06-screenshots/` — `gsc-page-indexing-summary.png`, `gsc-indexed-pages-page-2.png`, `gsc-404-urls.png`, `gsc-noindex-tag.png`, `gsc-crawled-currently-not-indexed-page-1.png`, `gsc-discovered-currently-not-indexed.png`, `gsc-pages-with-redirect-zero.png`, `gsc-duplicate-canonical-zero.png`
- **Reviewer note:** Strongest evidence area. Multi-bucket coverage with both CSV and screenshot. Indexing summary explicitly proves "Page with redirect = 0" and "Duplicate canonical = 0" on the legacy WP host. See §3 for the synthesis.

### Gate #4 — Google Business Profile screenshots — **Present / review-ready**
- **Files (v3):**
  - `05-google-business-profile/gbp-profile-overview-search-result.png`
  - `gbp-about-name-categories-description-phone.png`
  - `gbp-location-website-social-service-areas.png`
  - `gbp-hours-main-hours.png`, `gbp-hours-more-and-business-options.png`
  - `gbp-services-electrician-primary-page-1.png`, `gbp-services-electrician-primary-page-2.png`
  - `gbp-services-additional-categories-page-1.png`, `gbp-services-additional-categories-page-2.png`
  - `gbp-booking-link-servicetitan.png`
  - `README-gbp-evidence-review.md` (reviewer summary of observed facts)
- **Reviewer note:** 10 screenshots cover business name, primary + secondary categories, description, phone, website, public-location setting (service-area-only confirmed), service areas (10 cities listed), hours (24/7), services, and the ServiceTitan booking link. Synthesized facts appear in §4. Reviewer must still confirm before Approved.

### Gate #5 — Current DNS records screenshot — **Present / review-ready (needs reviewer confirmation before Approved)**
- **Files (v3):**
  - `12-launch-and-rollback/current-dns-before-cutover-page-1-a-ns-cname.png`
  - `current-dns-before-cutover-page-2-mx-txt-start.png`
  - `current-dns-before-cutover-page-3-txt-dmarc.png`
- **Reviewer note:** Three explicitly-labeled page screenshots of current DNS records (A / NS / CNAME, MX / TXT start, TXT / DMARC). Captures the pre-cutover baseline required for rollback. Reviewer must visually confirm completeness (all relevant record types captured, current/legible) before this gate is Approved.

### Gate #6 — WP Engine backup confirmation — **Present / review-ready (needs reviewer confirmation before Approved)**
- **Files (v3):**
  - `12-launch-and-rollback/wp-engine-backup-create-dialog.png`
  - `wp-engine-backup-created-toast.png`
  - `wp-engine-backup-confirmation-list.png`
- **Reviewer note:** Three explicitly-labeled WP Engine screenshots covering the backup-creation dialog, the success toast, and the resulting confirmation list. Captures the rollback prerequisite. Reviewer must visually confirm timestamp visibility and that the most recent backup is the one labeled here before this gate is Approved.

### Gate #7 — GA4 / GTM / Google Ads IDs — **Partially provided; implementation decision still unresolved**
- **Files (v3):**
  - `06-current-tracking/01-ga4-analytics-account-overview.png`
  - `02-ga4-account-property-list.png`
  - `05-ga4-data-streams.png`
  - `06-google-tag-manager-container-overview.png`
  - `08-tag-manager-account-overview.png`
  - `07-google-tags-list.png`
  - `03-google-ads-campaign-overview.png`
  - `04-local-services-ads-leads-overview.png`
  - `tracking-ids.md` (reviewer/decision file — observed access and open questions)
  - `README-tracking-evidence-review.md` (reviewer verdict)
- **Reviewer note:** 8 screenshots prove access to Google Analytics, GA4 data streams, Google Tag Manager, Google Tags list, Google Ads, and Local Services Ads. The `tracking-ids.md` companion file documents observed facts and unresolved questions. **Tracking implementation is not approved.** See §5 for the synthesis and the open questions list.

### Gate #8 — ServiceTitan scheduler test proof — **Deferred to a new session**
- **Files (v3):**
  - `06-current-tracking/servicetitan-scheduler-test-proof/DEFERRED_TO_NEW_SESSION.md` (explicit defer note)
  - `README-missing.md` (placeholder)
  - GBP booking-link evidence at `05-google-business-profile/gbp-booking-link-servicetitan.png` supports the broader ST integration story but does **not** by itself satisfy gate #8 — that gate still requires a test booking submitted from the Vercel preview, ST records the booking, then test is cancelled, with screenshots saved.
- **Reviewer note:** Cleanly marked deferred. Must be addressed in a separate session before DNS cutover.

### Gate #9 — Canonical NAP decision — **Present / review-ready**
- **Files (v3):**
  - `11-verified-business-facts/canonical-nap.md` (final decision file, 2026-05-10)
  - `source-canonical-nap-2026-05-10.md` (source/reasoning)
  - `source-geo_facts.json` (structured geo facts)
- **Reviewer note:** Brock's decision: **service-area-only public posture**. Public-facing geography uses `Moore, OK / Oklahoma City Metro` and the 10-city service area list. The internal/private address (`621 Sally Ct, Moore, OK 73160`) must not surface in customer-facing copy, paid ads, GBP copy, or schema unless Brock explicitly approves later. See §6 for the synthesis. Reviewer must still confirm before Approved.

---

## 3. GSC summary (synthesized from §2 gates #1–#3)

### 3.1 Coverage buckets (authoritative count, from `02-indexing-summary/gsc-indexing-critical-issues-summary.csv`)

| Bucket | GSC count | Source |
|---|---:|---|
| Not found (404) | **4** | Website |
| Excluded by 'noindex' tag | **1** | Website |
| Crawled — currently not indexed | **11** | Google systems |
| Discovered — currently not indexed | **9** | Google systems |
| Page with redirect | **0** | Website |
| Duplicate, Google chose different canonical than user | **0** | Google systems |

`gsc-indexing-non-critical-issues-summary.csv` has only the header row — no non-critical issues.

### 3.2 Indexed pages (from `03-indexed-pages/gsc-indexed-pages-urls.csv`)

Highlights:
- Homepage indexed (most-recent crawl 2026-05-04).
- Core service pages indexed: `/commercial-electrical-solutions/`, `/electrical-installation/`, `/services/emergency-electrician/`, `/residential-electrical-solutions/`, `/electrical-repair-and-service/`, `/indoor-lighting-installation/`, `/generators/`, `/services/`, `/industrial-electrical-solutions/`, `/electrical-panels/`.
- Footer pages indexed: `/contact-us/`, `/about-us/`, `/privacy-policy/`, `/terms-and-condition/`.
- Blog index indexed: `/blogs/`.
- **Legacy blog URLs indexed**, including:
  - 2 with the **`spark-shark` slug**, ARE covered by `vercel.json` 301s:
    - `/2023/12/28/empower-your-home-the-case-for-upgrading-your-electrical-panel-with-spark-shark/`
    - `/2024/01/24/why-you-should-hire-a-professional-for-electrical-installations/`
  - 2 with the **`flanco-electric` slug**, currently **NOT covered** by `vercel.json` 301s — candidates for v1.1 redirect promotion:
    - `/2023/12/29/powering-peace-of-mind-unveiling-the-benefits-of-a-home-generator-with-flanco-electric/`
    - `/2023/12/29/closing-the-deal-with-confidence-why-realtors-should-choose-flanco-electric-for-home-repairs/`
  - 1 slug-neutral: `/2024/01/24/why-you-need-a-professional-for-generator-installation/`
  - 1 slug-neutral: `/2024/01/03/stay-powered-up-essential-electrical-winter-safety-tips/`

### 3.3 Crawled — currently not indexed (per `04-crawled-currently-not-indexed/gsc-crawled-currently-not-indexed-urls.csv`)

GSC count: 11 (from §3.1). The cleaned URLs export captures the visible URLs; key patterns:

- **`flanco-electric`-slug legacy blog URLs (not covered by `vercel.json` 301s):**
  - `/2024/01/03/ground-fault-interrupters-the-power-of-gfi-outlets-by-flanco-electric/`
  - `/2024/01/12/join-our-team-flanco-electric-is-hiring-experienced-journeyman-electricians/`
  - `/2024/01/02/powering-tomorrow-a-comprehensive-guide-to-new-construction-wiring-with-flanco-electric/`
  - `/2024/01/01/power-up-your-new-year-the-case-for-whole-home-surge-protectors-with-flanco-electric/`
- **Unidentified blog slug:** `/2023/12/28/where-does-it-come-from/`
- **Legacy WP slugs:** `/our-residential-electrical-services/`, `/price/`
- **WordPress archive paths:** `/2023/12/`, `/2024/01/`
- **Real current pages, unexpectedly not-indexed:** `/electrical-inspection-services/`, `/reviews/`

### 3.4 Discovered — currently not indexed (per `05-discovered-currently-not-indexed/gsc-discovered-currently-not-indexed-urls.csv`)

GSC count: 9 (from §3.1). All visible URLs are real Spark Shark pages that Google has discovered but never crawled (last-crawled placeholder `1969-12-31`):

- `/ceiling-fans/`
- `/electrician-for-outdoor-lighting/`
- `/frequently-asked-questions/`
- `/locations-we-serve/`
- `/moore/`
- `/oklahoma-city/`
- `/smart-home-installation/`
- `/smoke-detectors/`
- `/switches-and-outlets/`

### 3.5 Performance — top pages by clicks (last 12 months, `gsc-performance-pages-last-12-months.csv`)

| URL | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| `/` | 158 | 6,973 | 2.27% | 28.35 |
| `/?utm_source=google&utm_medium=organic&utm_campaign=gmb_listing` | 72 | 7,238 | 0.99% | 4.70 |
| `/?utm_source=directory&utm_medium=referral&utm_campaign=directory_citation` | 25 | 4,311 | 0.58% | 3.44 |
| `/residential-electrical-solutions/` | 6 | 1,938 | 0.31% | 33.94 |
| `/terms-and-condition/` | 5 | 262 | 1.91% | 4.99 |
| `/2024/01/12/join-our-team-flanco-electric-is-hiring-experienced-journeyman-electricians/` | 3 | 16 | 18.75% | 9.06 |

**Observations** (not recommendations):
- Two UTM-tagged variants of `/` carry meaningful traffic (97 clicks combined) — relevant for canonicalization and any forced query-string handling on Vercel.
- A `flanco-electric`-slug legacy job-posting URL is in the top-6 clicked pages with **18.75% CTR at position 9** — high relative engagement, low absolute volume. Currently uncovered by `vercel.json` redirects.

### 3.6 Performance — top queries (913 rows in `gsc-performance-queries-last-12-months.csv`)

| Query | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| `spark shark electric` | 96 | 1,001 | 9.59% | 4.42 |
| `spark shark` | 12 | 343 | 3.50% | 7.44 |
| `sparkshark` | 7 | 187 | 3.74% | 4.21 |
| `electrician near me` | 3 | 497 | 0.60% | 4.04 |
| `spark shark electric reviews` | 3 | 170 | 1.76% | 6.36 |
| `electrician norman ok` | 1 | 393 | 0.25% | 12.12 |
| `commercial electrician oklahoma city` | 1 | 91 | 1.10% | 68.55 |
| `"electrical contractors and standby generator service providers near 64.667359, -150.444044"` | 0 | 3,806 | 0% | 1.00 |
| `electrician moore ok` | 0 | 812 | 0% | 15.83 |
| `generator installation oklahoma city` | 0 | 496 | 0% | 29.95 |

**Observations** (not recommendations):
- Brand-direct queries dominate clicks; non-brand discovery is shallow.
- The lat/lon query (3,806 impressions, 0 clicks, position 1) is a strange Maps-adjacent signal worth Deep Research scrutiny — that traffic isn't converting.
- High-value non-brand queries (`electrician moore ok`, `generator installation oklahoma city`, `commercial electrician oklahoma city`) all sit on page 2+ with 0 clicks — money queries that aren't ranking.

---

## 4. GBP summary (v3 — synthesized from `05-google-business-profile/README-gbp-evidence-review.md`)

| Field | Observed value |
|---|---|
| Business name | Spark Shark Electric |
| Primary category | Electrician |
| Secondary categories | Lighting contractor; Electrical repair shop; Electrical installation service |
| Phone | (405) 436-4776 |
| Website | https://www.sparkshark.com/ |
| Public location setting | **No public location** — service-area business (deliveries and home services only) |
| Service areas | Moore, Yukon, Edmond, Norman, Bethany, Del City, Newcastle, Midwest City, Mustang, Oklahoma City (10 cities) |
| Hours | Open 24 hours every day |
| Booking link | `book.servicetitan.com` |

**Deep Research implications:**
- GBP is already configured as service-area-only, which aligns with the NAP decision in §6.
- Service-area list on GBP matches the 10-city set in `canonical-nap.md` — internal-vs-external NAP is consistent.
- 24/7 hours is a marketing posture choice with operational implications (Deep Research should validate whether competitive listings reflect the same, and whether after-hours coverage materially affects ranking for `electrician near me` and similar queries).
- ServiceTitan booking link is present on the GBP card — Deep Research can treat the booking surface as an existing entity, not a future feature.

---

## 5. Tracking summary (v3 — synthesized from `06-current-tracking/tracking-ids.md` and `README-tracking-evidence-review.md`)

### 5.1 Observed evidence

- **Google Analytics:** "Spark Shark Analytics" account exists. GA4 property exists for Spark Shark / sparkshark.com.
- **GA4 data streams:** Two web streams visible:
  - `https://Sparkshark.com` — no data received in past 48 hours at time of screenshot (likely stale / case-variant duplicate)
  - `https://sparkshark.com` — receiving traffic in past 48 hours at time of screenshot (likely the canonical/active stream)
- **Google Tag Manager:** GTM account and a web container exist for sparkshark.com.
- **Google Tags:** Tags list shows multiple Google tags including GA- and Google Ads-shaped IDs.
- **Google Ads:** Account exists; campaigns currently **paused** at time of screenshot.
- **Local Services Ads:** Lead dashboard exists with historical leads.

### 5.2 What remains uncertain (for the implementation decision)

1. Exact active **GA4 Measurement ID** (`G-...`) from the canonical `https://sparkshark.com` web stream.
2. Disposition of the inactive case-variant stream (`https://Sparkshark.com`) — ignore, archive, or leave alone.
3. Exact **GTM Container ID** to install or preserve.
4. Deployment-layer decision: **GTM as single deployment layer** vs **direct gtag**.
5. **Google Ads conversion ID** (`AW-...`) and conversion label(s), if website conversion tracking is intended at launch.
6. **LSA tracking model:** does LSA rely on Google/GBP/LSA platform calls only, or does it need website event tracking?
7. Duplicate / stale Google tags to remove before launch.

### 5.3 Tracking implementation is NOT approved

This brief and the v3 evidence document **access** to Google Analytics, GTM, Google Ads, and LSA — not a tracking implementation. **Tracking installation in production HTML is not approved.** Deep Research outputs may produce a tracking *spec* (architecture, events, IDs to install where, dedup plan). The spec does not authorize installing tags. Tag install is a separate, scoped PR after Brock confirms the launch-IDs and the GTM-vs-gtag decision in launch-gate item #7.

---

## 6. Canonical NAP decision (v3 — captured at `11-verified-business-facts/canonical-nap.md`)

**Decision date:** 2026-05-10. **Decision owner:** Brock Flanary / Spark Shark Electric. **Status (per the file):** Provided for launch-gate review.

| Field | Decision |
|---|---|
| Business name | Spark Shark Electric |
| Alternate public name | Spark Shark |
| Phone | (405) 436-4776 |
| Website | https://www.sparkshark.com |
| Public address decision | **Service-area business / no public street address** |
| Public location wording | **Moore, OK / Oklahoma City Metro** |
| Primary service area (public) | Moore, Oklahoma City, Norman, Edmond, Yukon, Mustang, Newcastle, Bethany, Del City, Midwest City |
| Internal/private address | `621 Sally Ct, Moore, OK 73160` — **do NOT surface in customer-facing website copy, paid ads, GBP copy, schema, or public marketing unless Brock explicitly approves later.** |

**Deep Research implications:**
- Any audit of NAP consistency must treat the legal address as a private value, not a public NAP component.
- GBP is already configured to match the public service-area-only posture (§4) — public-side NAP is internally consistent.
- Schema `address` should reflect service-area-only posture; avoid emitting `streetAddress` on the public LocalBusiness/Electrician node. If a citation directory currently lists `621 Sally Ct` publicly, flag it for citation cleanup.
- Schema/website implication captured in the v3 NAP file: any public appearance of the street address must be intentional and approved.

---

## 7. Remaining blockers (before DNS may cut over)

Cross-referenced to `docs/migration/launch-gate.md` where applicable.

| # | Blocker | Tied to gate | State (v3) |
|---|---|---|---|
| 1 | Tracking implementation decision & exact launch-ID confirmation | Gate #7 | Partial — access proven; exact GA4 ID, GTM-vs-gtag decision, Ads conversion ID, and tag dedup still unresolved. |
| 2 | Contact form decision and fix | Not a gate item; called out in v4 plan §10 row 12 | Form action currently `REPLACE_WITH_FORM_ID` placeholder. Vendor decision (Formspree ID vs Vercel Function) pending. |
| 3 | ServiceTitan scheduler test proof | Gate #8 | Deferred to a new session per `06-current-tracking/servicetitan-scheduler-test-proof/DEFERRED_TO_NEW_SESSION.md`. |
| 4 | Final redirect map review (v1.1) | Drives a separate, scoped PR | `vercel.json` covers 14 known stubs. v3 GSC evidence (§3) confirms ≥3 `flanco-electric`-slug indexed/crawled URLs NOT covered. WordPress archive paths (`/2023/12/`, `/2024/01/`, `/our-residential-electrical-services/`, `/price/`) also uncovered. |
| 5 | Pre-launch Deep Research | This brief is the input | Not yet run. Outputs will land in `migration-evidence-pack/13-deep-research/`. |
| 6 | DNS / cutover runbook | Future doc | `docs/migration/cutover-runbook.md` is intentionally not yet authored — will be written when launch-gate is at least partially green. |
| 7 | Gate #5 reviewer confirmation | Gate #5 | DNS screenshots present and labeled; reviewer must confirm record-type completeness before Approved. |
| 8 | Gate #6 reviewer confirmation | Gate #6 | WP Engine backup screenshots present and labeled; reviewer must confirm timestamp visibility and identify the active backup before Approved. |

---

## 8. Research questions for Deep Research

These are the questions Deep Research (ChatGPT / Gemini / Perplexity / Claude Research) should answer using the v3 evidence pack plus their own web access.

### 8.1 Tracking architecture

1. Given that the new site has **zero analytics tags installed** today, what is the minimal-correct GA4 / GTM / Ads / Clarity (if any) architecture for a residential electrical service business that uses the ServiceTitan Scheduler Pro widget and a (currently broken) static contact form?
2. Should the analytics layer be **GTM-managed** (existing container) or **direct gtag** for a static HTML site generated by `build.py`? Concrete trade-offs.
3. Two GA4 web streams exist (`https://Sparkshark.com` no-data and `https://sparkshark.com` active, per §5). What's the correct disposition for each, and is there migration data continuity risk in archiving the inactive stream?
4. What event taxonomy should fire on this site? (phone-tap, scheduler-open, scheduler-submit, contact-form-submit, scroll-depth, page-time, location-page-engagement, etc.)
5. How should the existing `utm_source=google&utm_medium=organic&utm_campaign=gmb_listing` and `utm_source=directory&utm_medium=referral&utm_campaign=directory_citation` traffic (visible in §3.5) be classified and preserved in GA4?
6. What's the simplest, safest path to add Google Search Console verification (HTML meta vs DNS-TXT vs file upload) given that DNS hasn't moved yet and the site is currently still on WP?
7. Google Ads campaigns are currently paused (§5). Should the launch sequence resume Ads only after Vercel tracking is validated end-to-end, or is there an earlier safe point to resume?
8. LSA leads dashboard exists (§5). Does LSA require any website-side event integration, or is platform-side tracking sufficient?

### 8.2 Redirect sufficiency

1. Are the 14 `vercel.json` redirect entries sufficient to preserve link equity for every URL Google has currently indexed, crawled, or discovered (per §3.2–§3.4)?
2. Specifically: should the `flanco-electric`-slug legacy URLs (4–6 documented in §3.2 and §3.3) be added to `vercel.json` as 301s? If yes, what destinations best preserve topical relevance?
3. Should WordPress archive paths (`/2023/12/`, `/2024/01/`) and dead WP slugs (`/our-residential-electrical-services/`, `/price/`) be 301'd or 410'd? What's the rationale?
4. Are there `wp-content/`, `wp-admin/`, `feed`, `category/`, `tag/`, `author/`, or `sitemap_index.xml` patterns in any inbound backlink dataset that would warrant additional redirect rules?
5. For the lat/lon query at position 1 with 3,806 impressions and 0 clicks (§3.6), is this a known GBP / Maps phenomenon, and does it imply a redirect or schema action?

### 8.3 SEO / GEO risks

1. What's the realistic SEO risk profile of cutting over WP → Vercel for this specific URL set? Quantify expected ranking volatility based on the redirect map proposed in §8.2.
2. Given 9 real Spark Shark pages are **Discovered — currently not indexed** (§3.4), what's the most likely root cause: crawl budget, internal-link depth, sitemap configuration, content thinness, or something else? Which fix has the best expected ROI before cutover?
3. Top non-brand money queries (`electrician moore ok`, `generator installation oklahoma city`, `commercial electrician oklahoma city`) sit on page 2–7 with 0 clicks (§3.6). Is this a content / E-E-A-T issue, a backlink-velocity issue, or a local-SEO entity-graph issue? What's the highest-leverage pre-launch action?
4. How dependent is the new site's ranking on the GBP entity (now documented in §4)? What's the realistic impact of any GBP misalignment with the new NAP posture (§6)?
5. Does the service-area-only NAP posture (§6) introduce any specific SEO risks relative to a storefront NAP, given the OKC-metro competitive landscape?
6. 24/7 GBP hours posture (§4) — competitive context in the OKC residential electrical market? Does this materially affect ranking for emergency / `near me` queries?

### 8.4 Schema / NAP risks

1. The site emits a 4-node JSON-LD `@graph` (WebSite + Organization + LocalBusiness/Electrician + FAQPage) per page. Given the service-area-only NAP decision in §6, is the current schema correctly modeled? (Specifically: does it expose a `streetAddress` it shouldn't, or `areaServed` it should?)
2. Is `aggregateRating 4.8/117` defensible against current Google policy on schema-sourced ratings? What evidence trail should be preserved to support the 117 review count?
3. Is the SearchAction node correctly configured for a site with no on-site search bar?
4. What's the correct schema shape for the ServiceTitan Scheduler embed? Should the booking surface be modeled as `Reservation`, `Offer`, `Service.potentialAction`, or left unannotated?
5. Are there citation directories (Yelp, BBB, Networx, Thumbtack, ProvenExpert, Apple Maps, Bing Places) currently surfacing the legal `621 Sally Ct` address publicly? If so, which need to be updated for the service-area-only posture, and in what order?

### 8.5 Launch sequence

1. Given the launch-gate state (most items now review-ready; tracking partial; ST proof deferred), what is the minimum-viable evidence set Brock should advance next to unlock the earliest meaningful cutover? Order the remaining work by ROI-of-providing-it.
2. Should tracking be installed **before** DNS cutover (so pre-cutover data establishes a baseline), **during** cutover (so launch traffic is captured), or **after** cutover (so the cutover itself doesn't introduce additional change risk)? Recommendation with rationale.
3. What is the recommended order of operations among: (a) confirm GA4/GTM/Ads launch IDs, (b) install tracking via small scoped PR, (c) fix contact form, (d) ST scheduler smoke booking, (e) DNS cutover, (f) WP Engine decommissioning, (g) post-launch monitoring window?
4. What's the right monitoring window length (24h / 72h / 7d / 14d) for this size of site, given the URL set and the redirect coverage in §3?
5. Is there any operational reason to phase the cutover (apex first, www second, or vice versa) vs. flipping both simultaneously?

### 8.6 Rollback risk

1. What are the realistic rollback scenarios that would force a DNS revert in the first 24–72 hours post-cutover? Quantify the likelihood of each.
2. Given that WP Engine remains live throughout (per gate #6), what's the maximum time window in which a DNS rollback is operationally safe? What changes that window length?
3. Are there any post-cutover actions that, if taken too early, would make rollback functionally impossible (e.g. WP Engine teardown, GBP website-URL change, GSC property change)? List them with the earliest-safe-time for each.
4. If the cutover fails due to a Vercel-side build/deploy issue (not DNS), what's the fastest recovery path that does NOT require a DNS revert?
5. Is there a partial-rollback strategy (e.g. revert apex DNS but keep www on Vercel, or vice versa) that would preserve any production validation while restoring known-good service?

---

## What this brief does NOT authorize

- DNS cutover.
- Editing `vercel.json` (redirects, headers, buildCommand).
- Editing `docs/migration/launch-gate.md` or changing any gate status.
- Installing tracking tags in production HTML.
- Editing schema or `BRAND` dict in `build.py`.
- Updating GBP or any external citation.
- Modifying the ServiceTitan scheduler embed.
- Touching WordPress / WP Engine.
- Surfacing `621 Sally Ct` in any customer-facing copy.

Cutover authority lives entirely in `docs/migration/launch-gate.md`.

---

## Reference

- Launch gate (controlling document): `docs/migration/launch-gate.md`
- Preview validation record: `docs/migration/vercel-preview-validation.md`
- Vercel deploy contract: `vercel.json`
- Repo-level Claude rules: `CLAUDE.md`
- Evidence pack overview (v3): `migration-evidence-pack/README-local-evidence-pack.md`
- v3 evidence package status: `migration-evidence-pack/00_CURRENT_EVIDENCE_STATUS.md`
- v3 cleanup report: `migration-evidence-pack/00_EVIDENCE_REVIEW_AND_CLEANUP_REPORT.md`
- v3 file manifest: `migration-evidence-pack/00_FILE_MANIFEST.md`
- Deep Research workflow: `migration-evidence-pack/13-deep-research/README-deep-research-workflow.md`

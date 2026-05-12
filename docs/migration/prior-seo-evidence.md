# Prior SEO Evidence — Cumulative Notes

**Authored:** 2026-05-11
**Scope:** Captures what prior SEO vendors have told Spark Shark about the site's keyword targets, rankings, backlink profile, technical audit, and content gaps. Sourced from Brock's Gmail and Drive. Intent: inform migration redirect map, post-launch content priorities, and disavow / backlink-cleanup decisions.

**Status:** Living document. Three vendor eras to cover:
- §1 Strategy Zoo (current agency, started 2026-02-17) — **PARTIALLY CAPTURED** (email bodies done; 3 PDFs/CSV queued for the SEO Attachments Drive folder, then a follow-up read).
- §2 Coalition Technologies (prior agency, cancelled 2025-12-16) — **CAPTURED IN DETAIL** in `coalition-findings.md`. Section below is the executive summary; the standalone doc is canonical for Coalition.
- §3 Flanco-era off-page (BigThinkers Media, rachelhall001@gmail.com, 2023–2024) — **PENDING NEW SESSION** per Brock 2026-05-11. Large.

This doc is evidence only — it does not authorize migration actions. SOURCE-OF-TRUTH.md and launch-gate.md remain the authority for cutover.

---

## 0. Evidence index — files written this session

All four files live in `/Users/brock/Projects/sparkshark-com/docs/migration/`. Read them in this order if you're picking up cold:

| File | Scope | Authority |
|---|---|---|
| `prior-seo-evidence.md` (this doc) | Cross-vendor SEO evidence umbrella + Drive-folder convention + consolidated migration-impact summary | Index/summary |
| `coalition-findings.md` | Coalition Technologies engagement Oct–Dec 2025: link-building, copy batches, technical SEO changes, tracking installs, access handoffs, Oct 2025 campaign report, 12-attachment queue | Canonical for Coalition |
| `online-presence-inventory.md` | ~25 external surfaces (GBP, citations, social, reviews, tracking, schema, widgets, DNS) — what could break or drift at cutover | Canonical for online-presence inventory |
| `SOURCE-OF-TRUTH.md` / `launch-gate.md` / `cutover-runbook.md` | Pre-existing migration authority chain — NOT modified this session | Canonical for cutover |

---

## 1. Strategy Zoo (Joshua "Tobes" Tobler, SEO Account Manager)

Engaged 2026-02-17 via Morgan McKell. Tobes' team is the source of the most recent audit + roadmap.

### 1.1 Recommended target keywords (2026-03-02)

12 clusters, ~2,499 est. monthly volume aggregate. Five of the twelve require **new landing pages** — important for the redirect map and post-launch sitemap planning.

| # | Cluster | Est. Vol | Target URL | Page Status |
|---|---|---:|---|---|
| 1 | Generators | 684 | (no page) | **NEW PAGE NEEDED** |
| 2 | Electrician | 313 | `/` | exists |
| 3 | Generator Installation | 279 | `/generators/` | exists |
| 4 | Electrical Repairs | 260 | `/electrical-repair-and-service/` | exists |
| 5 | Emergency Electricians | 219 | `/emergency-electrician-services/` | exists |
| 6 | Surge Protectors | 145 | (no page) | **NEW PAGE NEEDED** |
| 7 | Generator Repairs | 143 | (no page) | **NEW PAGE NEEDED** |
| 8 | Circuit Breaker Replacements | 110 | (no page) | **NEW PAGE NEEDED** |
| 9 | Electrical Panel Upgrades | 97 | (no page) | **NEW PAGE NEEDED** |
| 10 | Electrical Services | 89 | `/services/` | exists |
| 11 | Electrical Panels | 85 | `/electrical-panels/` | exists |
| 12 | Electrical Inspections | 75 | `/electrical-inspection-services/` | exists |

Seth's revenue-driver overlay: "No Power" / emergency, Panel Upgrades, Repair work — should outrank Tobes' search-volume sort for prioritization.

### 1.2 Geographic scope (Seth-confirmed metro)

El Reno, Yukon, Mustang, Bethany, Piedmont, Moore, Norman, Newcastle, Tuttle, Del City, Midwest City, Harrah, Edmond, Nichols Hills, Oklahoma City. Tobes' note: Newcastle search volume is inflated by UK traffic; treat as smaller than it looks.

### 1.3 Current rankings (2026-03-03)

Attached as CSV: **`28698999_4349599_position_tracking_rankings_overview_20260303.csv`**. Not yet extracted — Gmail MCP has no attachment-download tool. To pull: Brock forwards to Drive, or exports from Gmail UI to the repo's evidence pack.

### 1.4 Roadmap deliverables (2026-03-19)

Two PDFs attached, both NOT extractable through current tooling:
- `Campaign Strategy Roadmap Summary - SparkShark.pdf`
- `Campaign Strategy Road Map - Spark Shark (Competitive Analysis).pdf`

Loom walkthroughs (publicly accessible URLs):
- v1: https://www.loom.com/share/542b6c382c4944038092ce97b375475c
- v2 (revised after Seth/Brock feedback): https://www.loom.com/share/48525caaafc141fd976b27989b70bbb0

Tobes' methodology (verbatim): "Identify top-ranking pages for each target keyword → Analyze those pages to discover **content & backlink gaps** → Reverse-engineer that data into actionable recommendations." Backlink + competitor numbers live ONLY in those two PDFs.

### 1.5 Site-audit findings explicitly named in email

- **NAP discrepancies** (Tobes flagged; Spark Shark has fought them "from day 1"). Tobes is fixing them and "building citations in the other directories." Cross-cutting concern for launch-gate Gate #9 (canonical NAP).
- **Thryv** under evaluation by Spark Shark for "listing dominance / NAP reinforcement / backlinks."
- **GBP**: Tobes proposed pointing GBP at a Moore landing page; Seth rejected ("we service the entire Metro"). GBP service-area decision still open — relevant to canonical-nap.md.
- **Duplicate post on site** (2026-04-16 audit): one duplicate found. Loom: https://www.loom.com/share/4e55745d022642de8e72c0d2a3970b0f. Should be resolved before cutover or flagged in post-launch cleanup.

### 1.6 Page-copy work in flight

- Moore electrical contractors page (first draft delivered 2026-04-18; follow-up 2026-04-27)
- Electrical Panel Upgrade expert-interview article (interview held 2026-04-14)

These are external WP-side content drafts. If Tobes is publishing into the legacy WP install (which is the same DB as the Flanco-era site per project memory), they need to be reconciled with the new static repo before cutover — risk of stale-content drift between WP and Vercel.

### 1.7 Vendor access granted (2026-03-05)

Tobes received access to: Google Analytics (`analyticsreportingteam@gmail.com` and `google-analytics-api-credentia@analytics-api-for-reporting.iam.gserviceaccount.com`), WordPress, Google Tag Manager, Google Business Profile, Google Search Console. Relevant to: tracking-ids.md (launch-gate Gate #7) and to the cutover playbook — analytics ownership transitions if GTM/GA4 is touched during migration.

---

## 2. Coalition Technologies (Jaco Cilliers) — EXECUTIVE SUMMARY

**Canonical detail:** `coalition-findings.md` (11 sections, written 2026-05-11). This section is just the migration-relevant headlines so you don't have to read the long doc to know the risks.

- **Engagement:** Oct 13 – Dec 16, 2025 (~9 weeks). $3,800/mo SEO + Local PPC retainer. Cancelled by Brock/Seth 2025-12-16; contractual final billable day Jan 15, 2026. Last Basecamp digest fired 2026-02-02 with 3 open to-dos still assigned to Brock/Seth.
- **The migration risk that matters:** Coalition shipped multiple live-WP features that **do not exist in the static repo**. If DNS flips as-is, all of them disappear silently:
  - ServiceTitan **DNI** snippet (init `2399891870`) — call-source attribution for Thumbtack/Yelp/GBP/Networx.
  - ServiceTitan **Web Scheduler** snippet (widget `087bee26-1d9f-41cf-9ed7-d03fdea9822f`).
  - **Embedded Contact Us form** (live 2025-11-20) with submission handler — separate from the Resend/Formspree pipeline in the static repo.
  - **HTML-embedded Privacy Policy + T&Cs with TCPA STOP/CANCEL/UNSUBSCRIBE language** (swapped from Termly hosted on 2025-10-24 specifically for ServiceTitan brand registration).
  - **Sticky main nav with Contact CTA** (2025-10-28).
  - **Copy Batches #4 and #5** (Nov 27 + Dec 26) — page-level edits across multiple service pages.
  - Announcement Bar (2026-01-06) — lower priority but visible UX.
- **Backlinks built:** No live referring domain ever named in Gmail. Strategy was author-bio/guest-byline. Conservative count 0–5; real number lives only in the Oct 2025 Campaign Report PDF (queued for Drive folder).
- **Open at cancellation:** `[Action Required] Update on Analytics & Tracking` Basecamp to-do — still OPEN at 2026-02-02. Likely contains the GA4/GTM/conversion-event config Coalition put on the live site. This is the single most important pre-flip recovery item for `tracking-ids.md` (Gate #7).
- **Access cleanup — 8 systems with possibly-still-active Coalition access:** WP admin, SEOPress Pro license, Termly login, ServiceTitan, **a mailbox @sparkshark.com**, Google Ads, GA4, GBP, GSC. Sweep against the Coalition contact roster (Jaco Cilliers, Caroline Giercyk, Maggie Chambers, Doug Drenkow, Joel Gerstman, Sierra Lee, Rebecca Fairbanks, anything `@coalitiontechnologies.com`).
- **October 2025 metrics (verbatim from email body):** Total Sessions 596 (▲284.52% MoM), Total New Users 477 (▲448.28% MoM). PPC last-30-days at cancellation: $13 avg CPC, $54 avg CPA, ~$2,150 Nov spend on a $3,000/mo approved budget.
- **12 attachments queued** for the SEO Attachments Drive folder — priority order in `coalition-findings.md` §11. Top three: Oct 2025 Campaign Report PDF, `Flanco Electric-Marketing-Strategy-01152025 (2).pdf` (likely contains the original SEO audit), Coalition Contract PDF (for IP/retention clauses).

---

## 3. Flanco-era off-page — PENDING NEW SESSION

Pre-rebrand SEO work pointing at `flancoelectricok.com`. Brock 2026-05-11: "flancoelectric scrape will need a new session" — do not start this in a session where Coalition or Strategy Zoo work is also being processed. Reason: data volume.

### 3.1 Known artifacts to start with

Drive holds (shared by external vendors, owned outside Spark Shark Google Workspace — readable through the current `flancoelectric@gmail.com`-scoped Drive MCP):

- **`Backlinks Report`** — Google Sheet, owner `bigthinkersmedia@gmail.com`, 2024-01-09, file ID `1InKeHtQW0x5ecIkKDcQqVLOR9PVEHx87k1iQLOSdx5o`. ~13 KB. Mostly PBN/spammy comment-blog links pointing at `flancoelectricok.com`. Disavow candidates.
- **`Mario Backlinks`** — Google Sheet, owner `bigthinkersmedia@gmail.com`, 2024-01-09, file ID `1aYB8eJDgDJSPkTPLmM-d0m3MfbsKfQIZkuJi5hviF6I`. ~7 KB. Same vendor, same pattern.
- **`OffPage Optimization - Flancoelectricok.com (18-Dec-2023)`** — Google Sheet, owner `rachelhall001@gmail.com`, file ID `1zIvXrlur2YQuZasE7h9a1gzGDSwFAsDSY-jiNw39oyc`. ~88 KB. Multi-tab: Website Details, Keywords, Approved Links, Profile Creation, Business Listing, Microblogging, Social Bookmarking, Link Wheel, Infographic Submission, Image Sharing, Blog Submission, Blog Promotion, Article Submission, Two Tiers, PPT Submission, PPT Promotion, Quora. Weekly ranking columns Oct–Dec 2023.

### 3.2 Searches to run in the new session

- Gmail: `from:bigthinkersmedia@gmail.com`, `from:rachelhall001@gmail.com`
- Gmail: `(flancoelectric OR flancoelectricok)` — anything mentioning the legacy brand
- Gmail: `(disavow OR "toxic links" OR "link audit" OR PBN)`
- Drive: search broadly for any sheet/doc shared by these two owners
- Possibly: ahrefs/semrush/moz exports if any made it to Brock's inbox

### 3.3 Why this matters for migration

Per project memory, sparkshark.com is the **same WP install + DB** as the prior Flanco site — Google still attributes the old backlink profile to the current domain. Toxic links from these PBN networks are an active SEO liability. Output of the Flanco session should be:

1. A consolidated `flanco-backlinks.csv` (or similar) listing every referring domain + anchor + status.
2. A `disavow.txt` candidate list for upload to GSC.
3. A decision whether to file the disavow **before** DNS cutover (preserves any clean-up effect) or **after** (less risky if classification is uncertain).

> Heads-up: data volume is unbounded — expect the scrape to produce multiple cache files in `/tmp` and to require subagent delegation. Start fresh, work in the same `docs/migration/` directory, append findings as `flanco-findings.md`.

---

## 4. Tooling decision — Drive folder for attachments

**Decided 2026-05-11:** the Gmail MCP we have (Google-hosted at `gmailmcp.googleapis.com`) deliberately omits attachment-bytes download. Rather than install a second local Gmail MCP and dance through Google Cloud OAuth, Brock will **manually forward / "Save to Drive" attachments** into one canonical Drive folder, and future Claude sessions read from that folder via the existing `claude.ai_Google_Drive` MCP.

**Canonical Drive folder:**

- **Folder ID:** `1DUKcmrQyK9RVpk3ySu-53zBsOTZaD2ae`
- **Share URL:** https://drive.google.com/drive/folders/1DUKcmrQyK9RVpk3ySu-53zBsOTZaD2ae?usp=drive_link
- **Created by:** Brock, 2026-05-11
- **Contents (as of 2026-05-11):** TBC — see "Access caveat" below.

**Access state — RESOLVED 2026-05-11:** the Drive MCP is scoped to `flancoelectric@gmail.com`. Brock shared the new `SEO Attachments` folder (owned by `brock@sparkshark.com`) with that account on 2026-05-11. `get_file_metadata` on the folder ID now returns valid metadata (owner: brock@sparkshark.com, title: "SEO Attachments", shared 2026-05-11T21:22Z). **Files inside the folder will be readable through `mcp__claude_ai_Google_Drive__read_file_content` once Brock drops them in.**

> If the folder ever appears inaccessible again in a future session, the fix is `Drive → folder → Share → add flancoelectric@gmail.com → Viewer`. Same fix worked 2026-05-11.

> Durable fix (deferred): reconnecting the Claude Drive MCP under `brock@sparkshark.com` would eliminate the share dance permanently. Do this post-migration; mid-migration disconnection risks losing visibility on the Flanco-era spreadsheets that are owned by external addresses but shared with `flancoelectric@gmail.com`.

**What to drop in the folder (for this migration cycle):**

| Source | Attachment | Email subject | Date |
|---|---|---|---|
| Tobes / Strategy Zoo | `Campaign Strategy Roadmap Summary - SparkShark.pdf` | Campaign Strategy Roadmap for Spark Shark | 2026-03-19 |
| Tobes / Strategy Zoo | `Campaign Strategy Road Map - Spark Shark (Competitive Analysis).pdf` | Campaign Strategy Roadmap for Spark Shark | 2026-03-19 |
| Tobes / Strategy Zoo | `28698999_4349599_position_tracking_rankings_overview_20260303.csv` | Re: Recommended Target Keywords for Spark Shark | 2026-03-03 |
| Coalition / Jaco | October 2025 Campaign Report (PDF + any chart images) | Spark Shark \| October 2025 Campaign Report | 2025-11-14 |
| Coalition / Jaco | Any link-building deliverables, audit PDFs, or report attachments | (various Basecamp threads) | 2025-10 → 2025-12 |

Gmail UI: open the email → click the attachment → "Add to Drive" → move into the folder above. Takes ~30 seconds per file.

> Note: there's an unrelated existing Drive folder titled "Spark Shark.zip (Unzipped Files)" owned by `flancoelectric@gmail.com` from 2025-03-24. That is NOT the same folder — it contains old Flanco-era assets. The new "SEO Attachments" folder should be in brock@sparkshark.com's Drive, not flancoelectric@gmail.com's.

What IS already extractable without Drive:
- All email body text (via `get_thread`).
- All Loom URLs (just text in body).
- All Drive-shared spreadsheets (legacy Flanco-era off-page work).

What is NOT extractable until Drive folder is populated:
- Tobes' two roadmap PDFs (the real audit + competitive analysis).
- Tobes' rankings CSV.
- Coalition's October 2025 campaign report + any binary deliverables.
- Inline screenshots embedded in email threads.

---

## 5. Consolidated migration-impact summary

This is the pull-up of items across all three evidence docs that **are not yet reflected in `launch-gate.md` or `cutover-runbook.md`** and that should be triaged before DNS flip. Source citation is in brackets so the next session can verify.

### 5.A Launch-blockers — WP-only features missing from the static repo

If we cut over today, these features that exist on the live WP site disappear. Each needs an engineering decision: port to `build.py` / `copy-drafts/`, defer, or accept loss.

| Feature | Live on WP? | In static repo? | Source |
|---|---|---|---|
| ServiceTitan **DNI** snippet (call-source attribution) | Yes (init `2399891870`, from `static.servicetitan.com/marketing-ads/dni.js`) | **No** | `coalition-findings.md` §5, `online-presence-inventory.md` §7 |
| ServiceTitan **Web Scheduler** (widget `087bee26-1d9f-41cf-9ed7-d03fdea9822f`) | Yes | Partially — verify static-repo embed matches Coalition's install exactly | `coalition-findings.md` §5 |
| **Embedded Contact Us form** (live 2025-11-20) | Yes | Different pipeline (Resend) — verify behavior parity + submission handler routing | `coalition-findings.md` §3 |
| **HTML-embedded Privacy Policy + T&Cs** with TCPA STOP/CANCEL/UNSUBSCRIBE language (for ServiceTitan brand registration compliance) | Yes (switched from Termly 2025-10-24) | Verify static repo's `/privacy-policy/` + `/terms-and-condition/` contain the TCPA-compliant text verbatim. The `405-796-8111` carve-out memory already covers part of this. | `coalition-findings.md` §3 |
| **Sticky main nav with Contact CTA** (2025-10-28) | Yes | Verify static repo's header has the sticky behavior + CTA | `coalition-findings.md` §3 |
| **Copy Batches #4 + #5** (Nov 27 + Dec 26 2025) — page-level copy edits | Yes | `copy-drafts/*.md` may pre-date these edits — diff each edited page | `coalition-findings.md` §3 |
| **Announcement Bar** (2026-01-06) | Yes | No | `coalition-findings.md` §3 |
| **SEOPress-generated per-page meta + schema** (titles, descriptions, JSON-LD) | Yes (WP plugin) | Static repo has its own 4-node @graph; any Coalition tuning between Nov 27 – Dec 16 must be exported from WP DB before flip or lost | `coalition-findings.md` §4 |
| **5 missing landing pages from Tobes' keyword plan** (Generators hub 684 vol, Surge Protectors 145, Generator Repairs 143, Circuit Breaker Replacements 110, Panel Upgrades 97) | Partially | If sitemap promises them at cutover, GSC will surface 404s | §1.1 above |

### 5.B Access cleanup — 8 systems with possibly-active Coalition access

Not in `launch-gate.md`. Should be a separate Brock-owned action.

1. WordPress admin (sparkshark.com on WP Engine)
2. SEOPress Pro license key
3. Termly.io login (rotate password)
4. ServiceTitan user accounts
5. **A mailbox `@sparkshark.com`** ← most surprising; audit Google Workspace users
6. Google Ads account
7. GA4 property
8. Google Business Profile manager + Google Search Console

Sweep names: Jaco Cilliers, Caroline Giercyk, Maggie Chambers, Doug Drenkow, Joel Gerstman, Sierra Lee, Rebecca Fairbanks, any `@coalitiontechnologies.com`. Also remove Coalition's Basecamp project access (or accept loss).

### 5.C Recoverable-only-from-Basecamp risks

- **`[Action Required] Update on Analytics & Tracking`** Basecamp to-do — still OPEN at 2026-02-02. Likely contains Coalition's final GA4/GTM/conversion-event config. **Recover before DNS flip or Gate #7 (`tracking-ids.md`) ships incomplete.** Best path: log into Basecamp before cancelled access cuts off, screenshot the to-do body.
- "Customer Reach Out" conversion-tracking break flagged 2025-11-18 — status at cancellation unknown.
- Local SEO "Sparkshark" misattribution flagged 2025-11-18 — status at cancellation unknown.

### 5.D NAP / GBP / citations (overlaps Gate #9)

- Tobes flagged NAP discrepancies are actively being fought; Strategy Zoo is updating citations and considering Thryv.
- GBP service-area decision (Moore-only vs full metro) still open between Tobes and Seth.
- Bing Places live as "Spark Shark Electric"; Apple Maps rejected (Case 18466826); Foursquare started not live; Facebook still on `/flancoelectric` handle.
- Duplicate post on legacy WP (2026-04-16 Tobes audit) — resolve before flip or note in post-launch cleanup.

### 5.E Toxic backlinks / disavow

- BigThinkers Media + rachelhall001 Flanco-era PBN spreadsheets (~100+ links from `*.tinyblogging.com`, `*.csublogs.com`, `*.suomiblog.com` patterns). No disavow filed.
- Coalition era contributed 0–5 confirmable legitimate links (real count in their Oct 2025 PDF, pending Drive folder population).
- **Pre-cutover decision needed:** ship `disavow.txt` before flip (cleanup applies to clean domain) or after (safer if classification uncertain). Resolved as part of the new-session Flanco scrape.

### 5.F Tracking ID handoffs (overlaps Gate #7)

- **Decision captured 2026-05-11 in `SOURCE-OF-TRUTH.md` §2 + `cutover-runbook.md`:** skip GTM entirely; use the unified Google Tag **`GT-NGS794C2`** (Site Kit-managed). Live-tag inspection of www.sparkshark.com found three tag IDs on the WP install:
  - `GTM-W7V4RS7C` — Coalition-era GTM container, abandoned.
  - `AW-17076116496` (conversion label `Hf8UCO6r84cZEN7Iyq0p`) — Google Ads, kept.
  - `GT-NGS794C2` — unified Google Tag, kept.
- ~~`GTM-TBCXCXGS` curl-verified on Vercel preview~~ — SUPERSEDED. `build.py:153` must be swapped from a GTM loader to a `gtag.js?id=GT-NGS794C2` loader before preview reverification.
- Strategy Zoo's Tobes has GA4 + GTM + GSC + GBP + WordPress access (granted 2026-03-05). His position-tracking will go blind on day one if his GA4 stream is not the one behind `GT-NGS794C2`. Verify before flip.
- New GSC reader 2026-05-05: `sparkshark-seo-reader@fluid-emissary-493106-s2.iam.gserviceaccount.com` (Spark Agent).
- Open GSC alert 2026-05-08: "Unparsable structured data issues" — investigate; source is current WP build, may resolve on cutover.
- **Live bug on WP (not a cutover blocker):** Google Ads phone-click conversion selector targets `tel:4054363776` (wrong digits) and isn't firing today. Vercel build emits `tel:+14054364776` (E.164), so any phone-click trigger added to `GT-NGS794C2` must use the new format. Separate Strategy Zoo ticket.

---

## 6. Session log

**2026-05-11 (this session):**
- Identified Tobes (Joshua Tobler, Strategy Zoo) as current SEO agency. Captured keyword clusters, current-rankings CSV reference, two roadmap PDFs (queued), Loom walkthroughs, NAP/GBP findings, page-copy work in flight.
- Ran online-presence inventory across ~25 surfaces → `online-presence-inventory.md`.
- Dug Coalition Technologies — 11-section deliverable → `coalition-findings.md`. Surfaced WP-only feature gap, 8-system access-cleanup need, "Analytics & Tracking" to-do open at cancellation, October 2025 metrics.
- Created Drive folder convention: `1DUKcmrQyK9RVpk3ySu-53zBsOTZaD2ae` ("SEO Attachments"). Folder shared with `flancoelectric@gmail.com` for Drive MCP visibility. Empty at session close.
- Updated this doc to serve as the umbrella index across all three evidence docs.

**Next session (Flanco-era scrape):**
- Start fresh per Brock 2026-05-11 ("flancoelectric scrape will need a new session").
- Read the three Drive spreadsheets in §3.1 above first.
- Run the searches in §3.2.
- Write `flanco-findings.md`.
- Produce `disavow.txt` candidate.

**Session after that (SEO Attachments read):**
- Read the Drive folder once Brock has populated it.
- Update `coalition-findings.md` §2 (real backlink count from Oct 2025 report PDF) and §7 (audit findings from `Flanco Electric-Marketing-Strategy-01152025 (2).pdf`).
- Update Tobes §1.3 + §1.4 with the real keyword rankings + competitive-analysis numbers.

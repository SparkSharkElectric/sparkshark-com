# Migration Action-Item Tracker — single ranked list

**Compiled:** 2026-05-12 (Phase 2 of the SoT §13 intake). **Authority:** this is a *consolidation*, not a new authority — `launch-gate.md` + `SOURCE-OF-TRUTH.md` + `cutover-runbook.md` remain canonical, and only Brock may write Gate Status cells.

**What this is:** every Action / Gap / Pending / Verify / TODO pulled out of the five 2026-05-11 evidence artifacts (`audits/migration-readiness/2026-05-11-2013utc-reverification.md`, `audits/site-hygiene/2026-05-11-technical.md` + `-plain-english.md`, `docs/migration/coalition-findings.md`, `docs/migration/online-presence-inventory.md`, `docs/migration/prior-seo-evidence.md`), de-duplicated against SoT §4 (Brock-owned queue) and §5 (Claude-owned queue), and ranked by: **A** = blocks DNS flip · **B** = blocks post-flip monitoring/attribution · **C** = optional / post-launch cleanup. Source is cited in brackets. Items already tracked in the launch gate are marked `[GATE #n]`.

> Triage note (Phase 1): none of the five artifacts contradicts SoT §1–§12. Two things to keep an eye on, neither a contradiction: (1) `prior-seo-evidence.md` §5.F and `online-presence-inventory.md` §5 say "the GA4 measurement ID is the stream behind `GT-NGS794C2`"; SoT §11 says the *live* GA4 is `G-QK02QH3SWY` (Brock-owned property `488680346`, currently behind `GTM-W7V4RS7C`) and explicitly leaves "verify `GT-NGS794C2` points at the same measurement ID" as an open step — so the two are consistent *if* that verification comes back equal. (2) There are now two disavow workstreams converging — the Ahrefs-surfaced 83-domain file built 2026-05-12 (`migration-evidence-pack/07-backlinks-and-citations/disavow-sparkshark.com.txt`) and the Flanco-era BigThinkers/rachelhall PBN set (pending the §3 Flanco scrape). They should be merged into one disavow.txt before either is filed.
>
> Commit-destination decision (Phase 1): the three `docs/migration/*.md` evidence files **stay in `docs/migration/`** for this cycle rather than moving to a `docs/migration/research/` subfolder — the canonical docs already reference them at those paths, and `prior-seo-evidence.md` tells the next Flanco session to write `flanco-findings.md` there too. Revisit the `research/` reorg once `flanco-findings.md` exists; move all four together then and update the reference paths in `SOURCE-OF-TRUTH.md` §9 + `cutover-runbook.md` §9 in the same PR. Audits stay in `audits/`.

---

## A — Blocks DNS flip

| # | Item | Owner | Source | Notes |
|---|---|---|---|---|
| A1 | **Fix the Vercel domain attachment** — `www.sparkshark.com` + apex must be attached to the `sparkshark-com` project, not the dispatcher project. | Brock (~10 min, Vercel UI) | re-verification audit "single next action"; [GATE — DOM-01/02] | Nothing else matters until this is right — DNS would route the marketing domain to the wrong project regardless. Paste `vercel domains ls` output afterward for confirmation. |
| A2 | **`build.py:153` GTM → `gtag.js?id=GT-NGS794C2` swap** — replace the GTM `<script>`+`<noscript>` with a unified-Google-Tag loader; rename `GTM_CONTAINER_ID` → `GOOGLE_TAG_ID`; refresh the doc comment; then reverify the preview alias. | Claude PR (single-file) | SoT §4 row 2, §11; cutover-runbook Risk 6; site-hygiene K1; online-presence §5; prior-seo §5.F | Closes the unowned `GTM-W7V4RS7C` payload as a side-effect. **Verify first** that `GT-NGS794C2` points at GA4 `G-QK02QH3SWY` (the owned live property) before shipping. |
| A3 | **Author `tracking-ids.md`** with: unified tag `GT-NGS794C2`, the GA4 measurement ID behind it (read `migration-evidence-pack/05-ga4-data-streams.png`, the `https://sparkshark.com` stream), Google Ads `AW-17076116496` + conversion label `Hf8UCO6r84cZEN7Iyq0p`. | Brock (~5 min decision capture) | [GATE #7]; SoT §4 row 2; coalition-findings §5; prior-seo §5.F | Then promote Gate #7 Status. |
| A4 | **Promote Gate #4 Status** (GBP screenshots) — 10 PNGs are on disk in `migration-evidence-pack/05-google-business-profile/`; Status is still `Not Provided`. | Brock (Status cell) | [GATE #4]; re-verification audit | Optionally do the field-by-field NAP cross-check on the 10 PNGs while you're in there. |
| A5 | **Promote Gate #9 Status** (canonical NAP) — `migration-evidence-pack/11-verified-business-facts/canonical-nap.md` exists, SAB-only decision, NAP frozen; Status still `Not Provided`. | Brock (Status cell) | [GATE #9]; re-verification audit; prior-seo §5.D | |
| A6 | **Gate #8 — ServiceTitan scheduler smoke booking** on the Vercel preview alias; replace `migration-evidence-pack/06-current-tracking/servicetitan-scheduler-test-proof/DEFERRED_TO_NEW_SESSION.md` with a real proof artifact. | Brock (~10 min) | [GATE #8]; re-verification audit | |
| A7 | **Port ServiceTitan DNI snippet to the static build** — `dni('init','2399891870')` from `static.servicetitan.com/marketing-ads/dni.js`, live on WP today, **not in the static repo**. Without it, call-source attribution (Thumbtack/Yelp/GBP/Networx) dies at flip. | Claude PR + Brock confirm | coalition-findings §5; online-presence §7; prior-seo §5.A | Goes in `<body>` per Brock's original email. |
| A8 | **Verify ServiceTitan Web Scheduler embed parity** — widget `087bee26-1d9f-41cf-9ed7-d03fdea9822f` is live on WP; confirm the static repo's embed (`ST_API_KEY`/`ST_SCHEDULER_ID` in `build.py`) matches Coalition's install exactly. | Claude (verify) | coalition-findings §5; prior-seo §5.A | The build already has *an* ST scheduler embed (`mwr2241pezdya33y00nyx0ok` / `sched_b2upae383kzlb9qjuhmqnyvt` per the re-verification audit) — confirm it's the right one. |
| A9 | **Verify Contact Us form parity** — Coalition shipped an embedded form on WP 2025-11-20 with its own submission handler; the static repo uses a different pipeline (Resend/Formspree per the cutover order). Confirm behavior + that submissions route somewhere monitored. | Brock decision + Claude verify | coalition-findings §3; online-presence §10; prior-seo §5.A; SoT cutover order step 6 | |
| A10 | **Verify Privacy Policy + T&Cs TCPA text is verbatim** — Coalition swapped from Termly to HTML-embedded policies on 2025-10-24 with STOP/CANCEL/UNSUBSCRIBE + message-types/frequency/HELP language for ServiceTitan brand registration. Confirm the static `/privacy-policy/` + `/terms-and-condition/` contain it. | Claude (verify) | coalition-findings §3; prior-seo §5.A | The `(405) 796-8111` carve-out memory covers part of this; this is the rest. |
| A11 | **Diff every page Coalition edited** — Copy Batches #4 (approved 2025-11-27) + #5 (approved 2025-12-26) plus sticky-nav+CTA (2025-10-28) and the Announcement Bar (2026-01-06) hit the live WP site; `copy-drafts/*.md` may pre-date them. Decide per page: port / defer / accept loss. | Claude verify + Brock decision | coalition-findings §3; prior-seo §5.A | |
| A12 | **Export SEOPress per-page meta + schema from WP** before flip — any title/description/JSON-LD Coalition tuned between 2025-11-27 and 2025-12-16 lives only in the WP DB. The static build has its own 4-node `@graph`; reconcile. | Brock/Claude | coalition-findings §4; prior-seo §5.A | Also: confirm the static site serves a sitemap equivalent to SEOPress's `/sitemap.xml` or GSC reports 0 indexable pages. |
| A13 | **Fix the `llms.txt` ↔ `llms-full.txt` rating drift** — `llms.txt` says `4.9`; `llms-full.txt`, the `BRAND` dict, and rendered JSON-LD say `4.8`. RANK-08 FAIL. | Claude PR (single-file, via `build.py`) | re-verification audit; site-hygiene K10 | |
| A14 | **Make the `llms.txt + schema self-check` GH Action green** — failing on spark-fsm PRs #136/#137/#142. | Claude/Brock | online-presence §9 | Must be green before flip. |
| A15 | **Investigate the GSC "Unparsable structured data issues" alert** (2026-05-08, 1 issue) — source is the current WP build; may resolve at cutover but confirm it isn't a pattern that will recur on the static build. | Claude/Brock | online-presence §5; prior-seo §5.F | |
| A16 | **Decide the 5 missing landing pages from Tobes' keyword plan** (Generators hub 684 vol, Surge Protectors 145, Generator Repairs 143, Circuit Breaker Replacements 110, Panel Upgrades 97) — if `sitemap.xml` will list them at cutover, GSC surfaces 404s. Either build stubs or keep them out of the sitemap until ready. | Brock decision | prior-seo §1.1, §5.A | |
| A17 | **Reconcile any Strategy-Zoo / Coalition WP-side content drafts in flight** — "Moore electrical contractors" page (draft 2026-04-18) + "Electrical Panel Upgrade" expert-interview article (interview 2026-04-14) may be publishing into the legacy WP install (same DB as the Flanco-era site). | Claude verify + Brock | prior-seo §1.6 | |
| A18 | **`scripts/cutover-smoke.sh`** — does not exist. CUT-02 FAIL. | Claude PR (single-file) | re-verification audit; SoT §5 | |
| A19 | **Typed-out DNS rollback values** in `migration-evidence-pack/12-launch-and-rollback/` — only screenshots exist. ROLL-03 FAIL; also SoT §2 Blocker #3. | Claude PR (single-file) | re-verification audit; SoT §2, §5 | Without these, post-cutover rollback is blind. |
| A20 | **Rollback trigger criteria** (when to roll DNS back) — documented? | Claude PR | SoT §5 | |
| A21 | **Make `secret-scan / gitleaks` + `pr-checks / guardrails` workflows green** on the spark-fsm cutover PRs (138–147) — failing on several. | Claude/Brock | online-presence §11 | Also: add a one-line gitleaks CI workflow to `sparkshark-com` to close SEC-01 for future audits (it currently has no `.gitleaks.toml`). |
| A22 | **Resolve the Vercel "1 domain needs configuration" warning** on team Spark Shark Electric (first seen 2026-04-29). | Brock | online-presence §11 | Likely the same root cause as A1. |

## B — Blocks post-flip monitoring / attribution

| # | Item | Owner | Source | Notes |
|---|---|---|---|---|
| B1 | **Recover the Coalition `[Action Required] Update on Analytics & Tracking` Basecamp to-do** before Coalition access cuts off — likely contains their final GA4/GTM/conversion-event config. | Brock | coalition-findings §5; prior-seo §5.C | Single most important pre-flip Basecamp recovery item. Log in, screenshot the to-do body. |
| B2 | **Verify the GA4 ↔ Google Ads conversion link via ServiceTitan** that Coalition wired during the wind-down (Seth completed it 2025-12-26) — confirm which GA4 property/measurement ID is on the WP site today and that it matches `tracking-ids.md` / `G-QK02QH3SWY`. | Brock/Claude | coalition-findings §5; prior-seo §5.F | |
| B3 | **"Customer Reach Out" conversion-tracking break** — Coalition flagged it 2025-11-18; status at cancellation unknown. | Brock | coalition-findings §5,§7; prior-seo §5.C | |
| B4 | **Google Ads phone-click conversion selector uses wrong digits** (`tel:4054363776`) and isn't firing today — separate Strategy Zoo ticket. The static build emits `tel:+14054364776` (E.164), so any phone-click trigger added to `GT-NGS794C2` must use the new format. | Brock (Strategy Zoo) | re-verification audit; prior-seo §5.F | Not a cutover blocker, but fix it so post-flip phone conversions actually count. |
| B5 | **Confirm Tobes' (Strategy Zoo) GA4 stream is the one behind `GT-NGS794C2`** — if not, his position-tracking goes blind on day one. | Brock | prior-seo §5.F | |
| B6 | **GSC pre-cutover baseline** — capture clicks/impressions/coverage screenshots before flip for drift detection. | Claude PR / Brock | SoT §5 | |
| B7 | **Screenshot Yelp + Thumbtack review counts/ratings** pre-flip for drift detection. | Brock | online-presence §4 | |
| B8 | **Confirm `flancoelectricok.com` has no live MX** and decide its renewal/redirect fate — could quietly leak link-equity if it expires; CertainPath billing still tags Brock as "Flanco Electric (aka Spark Shark) CP000283". | Brock | online-presence §8, gap #7,#8; prior-seo §3 | |

## C — Optional / post-launch cleanup

| # | Item | Owner | Source | Notes |
|---|---|---|---|---|
| C1 | **Merge the two disavow workstreams + file one `disavow.txt`** — the Ahrefs-surfaced 83-domain file (`migration-evidence-pack/07-backlinks-and-citations/disavow-sparkshark.com.txt`, built 2026-05-12) + the Flanco-era BigThinkers/rachelhall PBN set (`*.tinyblogging.com` / `*.csublogs.com` / `*.suomiblog.com` patterns; pending the §3 Flanco scrape). Decision: file before flip (cleanup applies to clean domain) or after (safer if classification uncertain). | Brock + Claude | online-presence §6; prior-seo §3,§5.E; backlinks `BACKLINK-SUMMARY.md` | The Ahrefs file is ready to upload as-is; merge once the Flanco scrape produces its list. |
| C2 | **Coalition access cleanup — sweep 8 systems** against the Coalition roster (Jaco Cilliers, Caroline Giercyk, Maggie Chambers, Doug Drenkow, Joel Gerstman, Sierra Lee, Rebecca Fairbanks, any `@coalitiontechnologies.com`): WP admin · SEOPress Pro license · **Termly login (rotate password)** · ServiceTitan users · **a mailbox `@sparkshark.com`** (audit Google Workspace) · Google Ads · GA4 · GBP + GSC. Remove their Basecamp project access too. | Brock | coalition-findings §8; prior-seo §5.B | Not in `launch-gate.md` — own it separately. |
| C3 | **Rotate WPE SSH keys post-launch** — `brock@sparkshark.com-wpengine`, `viktor-agent@sparkshark` (added 2026-05-07/08). (WPE Customer Portal password + Public API token already rotated 2026-05-12.) | Brock | online-presence §8 | |
| C4 | **Apple Maps / Business Connect decision** — Case 18466826 was rejected ("unable to verify"). Revive it or make the "skip iOS map coverage" decision explicit. | Brock | online-presence §2, gap #1; prior-seo §5.D | |
| C5 | **Facebook page** — still on `facebook.com/flancoelectric` (legacy handle); stale Drive-shared login `flancoelectricok@gmail.com / flancoelectric123` (rotate). Rename in place vs create new — affects the social-proof URL on the new site. | Brock | online-presence §3, gap #2 | |
| C6 | **Capture the Yelp profile URL** (known to exist; not recorded anywhere) — needed for the new-site footer/social row. Also audit whether a BBB profile under "Flanco Electric" needs renaming/closing, and stand up a LinkedIn *company* page. | Brock | online-presence §3,§4, gaps #3,#4,#5 | |
| C7 | **Cancel SEOPress PRO license** post-launch (owned by `brock@`, $/year). | Brock | online-presence §10, gap #9; prior-seo §1.6 | |
| C8 | **Find out what GoDaddy product was cancelled 2026-05-11** ("product removed" event, content unclear). | Brock | online-presence §8, gap #10 | |
| C9 | **ADR: service-page FAQPage duplication** — `build.py`'s schema generators emit two `FAQPage` blocks on service pages (one inside `@graph`, one standalone). Consolidate to one — but it touches a protected surface, so ADR-track, not a quick fix, not a launch blocker. | Claude (ADR) | site-hygiene K11 MEDIUM | |
| C10 | **Dedicated favicon set** — `build.py:365-366` points both `rel="icon"` and `rel="apple-touch-icon"` at the full `logo.png`. Generate `img/favicon-32.png` / `img/favicon-192.png` / `img/apple-touch-icon-180.png` (+ optional `img/site.webmanifest`); update `build.py`. Browsers cache favicons hard, so ideally ship this *before* the first post-cutover crawl. | Brock (art) + Claude PR | site-hygiene K8 HIGH | Listed in C only because it's not strictly a *blocker* — but it's the cheapest single-file PR and the §13 brief flags it as a top early candidate. Promote to A-tier in practice if there's time before flip. |
| C11 | **Save any `i0.wp.com` Photon-hotlinked image the static build doesn't replace** before the WP install is decommissioned (the new build self-hosts its images, so this is mostly already handled; the favicon was the exposed one — see C10). | Claude/Brock | site-hygiene K6 | |
| C12 | **Populate the "SEO Attachments" Drive folder** (`1DUKcmrQyK9RVpk3ySu-53zBsOTZaD2ae`) — Tobes' 2 roadmap PDFs + rankings CSV, Coalition's Oct 2025 campaign report PDF + Contract PDF + `Flanco Electric-Marketing-Strategy-01152025 (2).pdf`. Then a follow-up session reads them and updates `coalition-findings.md` §2/§7 + `prior-seo-evidence.md` §1.3/§1.4 with the real numbers. | Brock then Claude | prior-seo §0, §4; coalition-findings §11 | |
| C13 | **`Spark Shark.zip`** (48 MB, in `flancoelectric@gmail.com` Drive, id `1V4CsYs2QgMGR-Co6hUFkkrKaek3wracf`) — likely a brand-asset bundle; not opened. Open it if a favicon/logo source asset is needed for C10. | Brock/Claude | online-presence gap #14 | |
| C14 | **Add a heading-hierarchy check (and the other Section-K rules) to `qa.py`** — currently not enforced. | Claude PR | site-hygiene K4 | Future hardening, not a launch item. |

## Out of scope (per SoT §13 Phase 4 — flagged, not tracked here)

- **Flanco-era SEO scrape** — Brock requested a dedicated session; do NOT start it in a session also handling Coalition/Strategy-Zoo/backlink work. Output: `flanco-findings.md` + `disavow.txt` candidate (feeds C1). See `prior-seo-evidence.md` §3.
- **Coalition asset transfer-out** — Semrush + Google Ads MCC are Brock-owned business calls.
- **Strategy Zoo relationship decision** — 3 payment failures Apr 23–25, 2026; Brock-owned business call (affects who publishes GBP posts post-launch).
- **The backlink-capture workstream itself** — tracked separately in `migration-evidence-pack/07-backlinks-and-citations/BACKLINK-SUMMARY.md` + the `SESSION-N-HANDOFF.md` files; only its disavow output (C1) and review-drift screenshots (B7) surface here.

---

## Phase 3 — recommended PR sequence (recommend; do not execute without Brock `go`)

Per the "Surgical Patches Stay Single-File" rule, one scoped PR per change. Suggested order:

1. **`build.py:153` GTM → `gtag.js?id=GT-NGS794C2` swap** (A2) — unblocks Gate #7's code dependency, closes the unowned `GTM-W7V4RS7C` payload. Verify the measurement-ID equivalence (A2 note) first.
2. **Dedicated favicon set + `build.py:365-366` update** (C10) — cheapest single-file PR; closes the most-cached identity asset before the first post-cutover crawl. Needs the favicon art (C13) decided.
3. **`llms.txt` ↔ `llms-full.txt` 4.8/4.9 fix** (A13) — tiny single-file `build.py` fix; closes RANK-08.
4. **`scripts/cutover-smoke.sh` + typed-out DNS rollback values + rollback trigger criteria** (A18 + A19 + A20) — could be one PR or three; closes CUT-02 / ROLL-03 / SoT §2 Blocker #3.

Also queued by the broader migration plan (SoT §13): GA4 property `488680346` move to the Spark Shark Analytics account (SoT §4 row 7 + §11) — Brock-owned UI action, not a code PR.

---

*Compiled from the five 2026-05-11 evidence artifacts. When an item here disagrees with `launch-gate.md` / `SOURCE-OF-TRUTH.md` / `cutover-runbook.md`, prefer those.*

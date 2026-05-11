# sparkshark.com → Vercel Migration — Source of Truth

**Authored:** 2026-05-11
**Status:** Canonical. Supersedes every file listed in §10.
**Authority chain:** `docs/migration/launch-gate.md` controls DNS authority. This document summarizes state; it does not authorize cutover.

> This is the one place to look. If anything in another doc disagrees with this one, prefer the readiness audit at `audits/migration-readiness/2026-05-11.md` and flag the disagreement in the §12 footnote.

---

## 1. Verdict + score

- **Verdict:** **HARD NO-GO.** Two independent auto-fail triggers fire today.
- **Score:** **40 / 100** (capped). Raw category math would be 42; the cap is from the auto-fail triggers.

---

## 2. Top 3 blockers

| # | Blocker | Status | Owner |
|---|---|---|---|
| 1 | **Vercel custom-domain attachment is on the wrong team.** ~~`sparkshark.com` apex is attached to team `spark-shark-electric` and assigned to project `spark-fsm` (the dispatcher), not the marketing site. `www.sparkshark.com` has no project assignment.~~ **RESOLVED 2026-05-11.** `sparkshark.com` + `www.sparkshark.com` now aliased on `sparkshark-com` project (team `spark-shark-electric-2b2f3a3a`), `verified=true` via cross-team TXT challenge at `_vercel.sparkshark.com` (records remain in place permanently). Apex registration stays on team `spark-shark-electric` so the 4 FSM subdomain aliases (`ops/agent/field/portal.sparkshark.com`) on `spark-fsm` retain their parent — confirmed still verified + serving HTTP 200/307 post-claim. A records untouched (apex still `141.193.213.10/11` WP Engine, `www` still `CNAME @`). Zero live-traffic change; cutover still gated by `launch-gate.md`. | CLOSED | — |
| 2 | **Launch gate has 4 of 9 rows open.** Two need only a Status-cell promotion from existing evidence (Gate 4 GBP screenshots, Gate 9 Canonical NAP). Gate 7 (Tracking IDs) needs: (a) decision capture into `tracking-ids.md` — done as of 2026-05-11 (option 3, skip GTM, use unified Google Tag `GT-NGS794C2`), (b) `build.py:153` patch (swap GTM `<script>` + `<noscript>` for a `gtag.js?id=GT-NGS794C2` loader, rename `GTM_CONTAINER_ID` → `GOOGLE_TAG_ID`, refresh the doc comment above the var), (c) preview-alias reverification with the new tag in place, then (d) Status-cell promotion. Gate 8 needs a real new artifact — a ST scheduler smoke booking on the live alias. | OPEN | Brock (~90 min total) |
| 3 | **Cutover-day paperwork doesn't exist.** Four operational artifacts missing: `docs/migration/cutover-runbook.md` (closed by this commit), smoke script, typed-out DNS rollback values (only screenshots exist), rollback trigger criteria. | PARTIAL | Claude (~90 min across single-file PRs); `cutover-runbook.md` shipped 2026-05-11 |

---

## 3. What's verified ready

- **Site itself:** all 27 redirects in `vercel.json` return correct 301/308 + 200 after `-L`; all 21 GSC-indexed URLs resolve 200 (direct or via 301); 4-node `@graph` (WebSite + Organization + LocalBusiness/Electrician + FAQPage) intact on homepage; service pages add `BreadcrumbList` + `Service`; tel link consistent across 7-page sample (`tel:+14054364776`).
- **Contact form pipeline:** POST to `/api/contact-form/` returned `{"ok":true}` at 2026-05-11T16:23:10Z; Resend delivery id `5cb36ea7-…` to `theteam@sparkshark.com` confirmed.
- **ST scheduler embed:** renders on `/` and `/contact-us/` with `data-api-key` + `data-schedulerid` matching `build.py` exactly.
- **WP Engine redirect layer:** Web Rules / Rewrite Rules / Access Rules all confirmed EMPTY — `vercel.json` is the only redirect layer to worry about.
- **Production secrets:** `RESEND_API_KEY`, `CONTACT_FORM_TO`, `CONTACT_FORM_FROM` set on the `sparkshark-com` Vercel project, production scope, ~4h old as of the audit.
- **Rollback insurance (partial):** 3 paginated GoDaddy DNS screenshots present in `12-launch-and-rollback/`; WP Engine "Migration Backup 05-10-2026" created by `brock@sparkshark.com` confirmed in the backup list; legacy WP install remains live for rollback.
- **GSC verification (carries through cutover, CONFIRMED 2026-05-11):** Brock's GSC property `https://www.sparkshark.com/` is verified via **Domain name provider** (DNS TXT), token `1DyR8lUgOXiQHuidohciuTVNngFZ06Xr7MVAeGgWHKA` at apex `sparkshark.com`. GSC Settings → Ownership verification UI confirms "You are a verified owner · Domain name provider · Successfully verified." No HTML-tag / GA / GTM / Site Kit dependency. Only A records flip at cutover; TXT records stay at GoDaddy, so verification + data inflow continue unchanged. The HTML-meta verification (`Fgyo9Rue-...`) on the live WP homepage is a separate account per the `build.py:146-152` comment (Coalition-era) — not Brock's monitoring surface; benign at cutover. Alternate methods are listed as available but inactive: an HTML file (`google973f9f3bb8715119.html`, downloaded locally but never uploaded), an HTML tag (would use the same `1DyR8lUg...` token), GA-based, and GTM-based. The HTML-tag token is the value to paste into `build.py:154` as `GSC_VERIFICATION_VALUE` IF belt-and-suspenders is ever desired — not required.
- **Schema + content discipline:** `qa.py` enforces NAP + license + brand-misspellings + scaffolding leaks on every page; CI-blocked.
- **Stack truth:** static HTML built by `build.py` (Python stdlib), `BASE="" python3 build.py` per `vercel.json` buildCommand, `outputDirectory: "."`, `trailingSlash: true`. No Node toolchain. No `package.json`.

---

## 4. Brock-owned action queue (pre-flip)

Source: `migration-risk-defense-runbook-2026-05-11.html` Brock queue. Total time: ~37 minutes.

| # | Action | Closes | Defends Risk | Time |
|---|---|---|---|---|
| 1 | **Capture GBP screenshots.** 9 fields: name, address/SAB toggle, phone, website URL, primary category, secondary categories, services list, hours, business description. Save to `/migration-evidence-pack/05-google-business-profile/`. | Gate #4 | Risk 5 (GBP disconnect) | ~10 min |
| 2 | **Author `tracking-ids.md`.** Decision recorded 2026-05-11: **skip GTM entirely; use the unified Google Tag (`GT-NGS794C2`, Site Kit-managed)** observed live on www.sparkshark.com. Document: (a) the unified Google Tag ID `GT-NGS794C2`, (b) the active GA4 measurement ID behind it (read off `05-ga4-data-streams.png` for the `https://sparkshark.com` stream), (c) Google Ads `AW-17076116496` + conversion label `Hf8UCO6r84cZEN7Iyq0p` (both observed live). Note: the live WP site's phone-click conversion selector targets `tel:4054363776` (wrong digits) and isn't firing today — separate Strategy Zoo ticket, not a cutover blocker. Vercel build emits `tel:+14054364776` (E.164), so any unified-tag phone-click trigger must target the new format. **Follow-up code work:** `build.py:153` GTM `<script>` + `<noscript>` → `gtag.js?id=GT-NGS794C2` loader; rename `GTM_CONTAINER_ID` → `GOOGLE_TAG_ID`; refresh the doc comment block above the var; then reverify preview alias. | Gate #7 | Risk 6 (data corruption) | ~5 min decision capture (build.py patch is separate work) |
| 3 | **Run ST scheduler smoke booking.** Submit a test booking on the live alias `https://sparkshark-com-git-main-spark-shark-electric-2b2f3a3a.vercel.app` — **NOT** `spark-fsm.vercel.app` (that's the FSM dispatcher). Confirm it appears in ServiceTitan, then cancel. Screenshot before/after. Save to `/migration-evidence-pack/06-current-tracking/servicetitan-scheduler-test-proof/`. | Gate #8 | Risk 6 + booking pipeline | ~10 min |
| 4 | **Fill in `canonical-nap.md`.** Use template at `/migration-evidence-pack/11-verified-business-facts/canonical-nap-template.md`. Decisions: address vs SAB-only, phone in E.164, GBP URL, service-area list, citation-update priority list. | Gate #9 | Risk 5 | ~10 min |
| 5 | **Confirm GoDaddy auto-renew is ON** for sparkshark.com registration. | (Defense, no gate) | Risk 2 (registration lapse) | ~2 min |
| ~~6~~ | ~~**Confirm GSC verification method in the UI.**~~ **CLOSED 2026-05-11.** GSC Settings → Ownership verification screenshot confirms property `https://www.sparkshark.com/` is verified via **Domain name provider** (DNS TXT, token `1DyR8lUg...` at apex). No further pre-flip action needed; verification + data inflow survive the A-record flip automatically. | (Defense, no gate) | Risk 6 (GSC data inflow loss) | — |

> ~~**Implicit prerequisite to all of the above:** fix the Vercel domain attachment (Blocker #1, §2). The 5-item queue above assumes the domain lives on the right project. If DNS flips while the apex is still bound to `spark-fsm`, none of these mitigations save the launch.~~ **Prerequisite cleared 2026-05-11** — see Blocker #1 in §2 (now CLOSED). Apex + www verified on `sparkshark-com` project; cutover-day routing is safe.

---

## 5. Claude-owned action queue (pre-flip)

Source: `migration-risk-defense-runbook-2026-05-11.html` Claude queue.

1. **Capture pre-cutover GSC baseline.** Re-export GSC Performance for last 28 days (clicks/impressions/position) for top 10 pages and top 20 queries. Save into `/migration-evidence-pack/04-google-search-console/06-baseline-pre-cutover-2026-05-XX/`. Defends Risk 4 (fragmented signals) — gives an attribution surface if positions drift post-flip.
2. **Curl-verify redirect routing on the preview alias.** For each of the 27 redirects in `vercel.json`, confirm HTTP 301 (not 200) on the preview alias. Surfaces the orphan-HTML question — if any URL returns 200 with content instead of 301, the stale file should be removed before flipping DNS. Defends Risk 1.
3. **Curl-verify schema integrity on 3 critical pages.** For `/`, `/contact-us/`, `/electrical-panels/` on the preview alias: confirm the 4-node `@graph` is present and validates; ST scheduler embed renders; NAP strings exact-match `BRAND` dict. Defends Risk 4.
4. **Confirm `sitemap.xml` + `robots.txt` on the preview alias** match the production-intended URL set (`BASE=""`, root-relative, no `/sparkshark-com/` prefix anywhere).
5. **Consider adding redirects for `/2023/12/` and `/2024/01/`** archive listing URLs (currently 404 post-flip). Low priority — both URLs are "crawled, not indexed" in GSC. Could 301 to `/blogs/`. Worth one PR if everything else clears. Defends Risk 1.
6. **Confirm the four prepped sparkshark-com PRs** (#7 / #8 / #9 + spark-fsm PR #142 follow-ups) are merged into `main` and reflected on the preview alias before DNS flip. Per memory `project_cutover_2026_05_11`.

---

## 6. DNS-flip day-of sequence

Source: `migration-risk-defense-runbook-2026-05-11.html` "DNS-flip day-of". Do not start step 1 until §2 blockers are CLOSED and §4 + §5 queues are complete.

1. **Re-read `docs/migration/launch-gate.md`.** Every row Approved or Brock-written "Not Applicable: \<reason\>". If any row is still Not Provided / Provided-Not-Reviewed / Reviewed-Needs-Fix → **STOP**.
2. **Confirm WP Engine "Migration Backup 05-10-2026" is still listed** in the backup history. Gate #6 evidence remains valid only if the backup exists. ~1 min.
3. **Take the final pre-flip prod-state screenshot** of `www.sparkshark.com` (currently WP Engine). One full-page desktop screenshot, one mobile-UA capture. Save into `/migration-evidence-pack/12-launch-and-rollback/pre-flip-final-state-<UTC-timestamp>/`.
4. **Flip the GoDaddy A record** for `@` from `141.193.213.10` + `141.193.213.11` to the Vercel target (Vercel-supplied IP / CNAME from dashboard). Note exact UTC timestamp.
5. **Start the post-flip monitor immediately** (next section).

---

## 7. Post-flip 72-hour monitor

Source: `migration-risk-defense-runbook-2026-05-11.html` "Post-flip monitor".

| Window | Check | Pass criterion | If fails |
|---|---|---|---|
| 0 – 60 min | curl prod homepage + 5 service pages (panels, generators, EV, repair, install) | HTTP 200 · GTM container loads · NAP renders | Promote previous Vercel deploy or revert DNS |
| 0 – 60 min | Browser visit `www.sparkshark.com` on desktop + mobile | SSL valid · scheduler embed renders · contact form submits | If SSL: wait 10 min, recheck (Vercel cert issuance). Anything else: rollback. |
| 1 – 6 h | GSC URL Inspection on `/` + top 3 indexed pages | "URL is on Google" still true · new mobile screenshot acceptable | Use GSC "Request Indexing" on affected URLs |
| 6 – 24 h | GSC Coverage report | No spike in 404s or Crawled-Not-Indexed | Inspect newly-404 URLs; add redirects if any have inbound links |
| 24 – 72 h | GA4 / GTM real-time + sessions delta vs pre-flip baseline | Sessions within ±20% of pre-flip 24-h average | Drill into tag firing rate, page-view events |
| Day 1 – 7 | GSC Performance — top 10 URLs vs pre-flip baseline | Position drift < 5 spots, impressions > 50% of baseline | Investigate per-URL: schema, redirects, GBP sync |
| Day 7 – 30 | GBP insights + GA4 conversion events + Resend form deliveries | Lead-flow within ±25% of trailing 30 days | Full audit: pull new GSC export, re-run `qa.py`, schema validator pass |

---

## 8. Rollback playbook

Source: `migration-risk-defense-runbook-2026-05-11.html` "Rollback playbook".

| Scenario | Action | Recovery time |
|---|---|---|
| Vercel deploy serves broken content | Promote previous deploy from Vercel dashboard (Deployments → … → Promote to Production) | < 5 min |
| SSL cert not issued within 15 min of DNS flip | Wait 30 min total. If still not issued, contact Vercel support. | < 60 min |
| Site fundamentally broken; want WP back | Revert GoDaddy A record to `141.193.213.10` + `141.193.213.11` per Gate #5 screenshots. DNS TTL determines propagation (5–30 min). | 15 – 60 min |
| WP Engine site itself drifted during cutover | WP Engine portal → Backups → restore "Migration Backup 05-10-2026" (Gate #6 evidence). Then revert DNS as above. | 30 – 90 min |
| GSC shows mass-404 spike post-flip | Identify the 404'd URLs (GSC Coverage), add 301s to `vercel.json`, push to `main`, Vercel rebuilds. | < 30 min per URL set |

---

## 9. Where authoritative evidence lives

Paths only. Do not transcribe.

- **Launch gate (DNS authority):** `docs/migration/launch-gate.md`
- **Full readiness audit (per-category scoring, all evidence cited):** `audits/migration-readiness/2026-05-11.md`
- **Plain-English audit summary:** `audits/migration-readiness/2026-05-11-plain-english.md`
- **Seed-prompt vs current-truth diff:** `audits/migrate-day-decision/2026-05-11-seed-prompt-vs-current-truth-diff.md`
- **Cleanup + handoff manifest (ARCHIVE list, gap catalog):** `audits/migrate-day-decision/2026-05-11-cleanup-handoff-manifest.md`
- **Cutover runbook (newly promoted from HTML):** `docs/migration/cutover-runbook.md`
- **Vercel preview validation evidence:** `docs/migration/vercel-preview-validation.md`
- **Production config (redirects + headers + buildCommand):** `vercel.json`
- **Evidence pack (Brock-supplied):** `/Users/brock/Downloads/migration-evidence-pack 6/` — index at `00_CURRENT_EVIDENCE_STATUS.md`, manifest at `00_FILE_MANIFEST.md`, cleanup report at `00_EVIDENCE_REVIEW_AND_CLEANUP_REPORT.md`, deep-research brief at `13-deep-research/00_DEEP_RESEARCH_INPUT_BRIEF.md`
- **Vercel migration delta plan (background only):** `/Users/brock/.claude/plans/parallel-gliding-pancake.md`
- **Original HTML runbook (pre-conversion):** `/Users/brock/Projects/spark-fsm/audits/migration-risk-defense-runbook-2026-05-11.html`
- **Session-scoped memory (authoritative for cutover sub-tasks):** `/Users/brock/Library/Application Support/Claude/local-agent-mode-sessions/5c7680ce-9a80-46c8-a052-5c0fa27e570e/e93bec34-2ac9-47fe-a03f-fa9befd18a2e/spaces/058edfe0-0759-497c-b3bd-f801ad0a55c5/memory/` (`project_cutover_next_actions_2026_05_10_pt2.md`, `project_cutover_reality_check_2026_05_10.md`, `project_privacy_policy_405_796_8111.md`)

---

## 10. What this document supersedes

When Brock greenlights cleanup (separately approved — not in this session), the following files move to `spark-fsm/audits/_archive/2026-05-pre-cutover/`. They are listed here so a future reader knows this SoT is the canonical successor.

### Superseded "current" docs in `/Users/brock/Projects/spark-fsm/audits/`

- `migration-auditor-skill-proposal-2026-05-11.html` (skill is now installed at `~/.claude/skills/migration-auditor/`)
- `sparkshark-cutover-2026-05-11-autonomous-closeout.html`
- `sparkshark-cutover-2026-05-11-handoff.html`
- `sparkshark-cutover-next-actions-2026-05-10-pt2.html`
- `sparkshark-cutover-reality-check-2026-05-10.html`
- `sparkshark-pack-vs-live-diff-2026-05-10.html`
- `sparkshark-vercel-migration-status-2026-05-10.html`
- `sparkshark-session-handoff-2026-05-10.html`
- `sparkshark-session-handoff-2026-05-10-v2.html`
- `sparkshark-session-handoff-2026-05-10-v3.html`
- `sparkshark-session-handoff-2026-05-10-v4.html`
- `sparkshark-cutover-hardening-sprint-2026-05-10.html`
- `sparkshark-cutover-hardening-sprint-2026-05-10-v3.html`
- `sparkshark-cutover-hardening-sprint-2026-05-10-v4.html`
- `sparkshark-cutover-hardening-sprint-2026-05-10-v5.html`
- `security-sweep-2026-05-11-pre-cutover-handoff.html`
- `migration-risk-defense-runbook-2026-05-11.html` (content promoted to `docs/migration/cutover-runbook.md` in this commit)

### Older work (no longer migration-relevant) in `/Users/brock/Projects/spark-fsm/audits/`

- `2026-05-07-homepage-broken/` (folder)
- `2026-05-07-wp-fixes/` (folder)
- `2026-05-09-homepage-iterations/` (folder)
- `2026-05-10-gsc-pull/` (folder — useful but historical)
- `ui-snapshots/` (folder)
- `screenshots/` (folder)
- `2026-05-08-block-1-final.html`
- `2026-05-08-block-1-status.html`
- `2026-05-08-homepage-execution-master-handoff.html`
- `2026-05-08-sparkshark-homepage-audit.html`
- `sparkshark-rebuild-handoff-2026-05-08.html`
- `sparkshark-rebuild-handoff-2026-05-08-v2.html`
- `sparkshark-rebuild-research-2026-05-08.html`
- `sparkshark-conversion-recs-2026-05-09.html`
- `sparkshark-uiux-handoff-2026-05-08.html`
- `sparkshark-uiux-handoff-2026-05-09.html`
- `sparkshark-uiux-p0-patch-2026-05-09.html`
- `sparkshark-uiux-p1a-delta-2026-05-09.html`

### Reference research in `/Users/brock/Projects/sparkshark-com/` (recommended destination: `sparkshark-com/docs/research/`)

- `spark_shark_final_merged_seo_geo_research_document.md` (62 KB)
- `Perplexity Validation Report for Spark Shark SEO GEO Brief.md` (51 KB)

---

## 11. Analytics ownership picture (corrected 2026-05-11 ~18:45 CT after API-level reclaim)

Initial finding (during backlink audit) read as: "live GA4 `G-QK02QH3SWY` is locked behind an unowned third-party GTM." The deeper investigation (later same evening) corrected this — **the GA4 destination IS owned, only the GTM container layer is unowned.** Captured in full so the cutover plan reflects the real picture.

### What's actually live on www.sparkshark.com

- `GTM-W7V4RS7C` — Google Tag Manager container present in the live homepage `<noscript>` iframe + the `<script>` loader. **Brock does NOT own this container.** It is in someone else's GTM account (Coalition-era — prior marketing agency). Its `gtm.js?id=GTM-W7V4RS7C` payload references GA4 measurement ID `G-QK02QH3SWY`.
- `GT-NGS794C2` — unified Google Tag (via Site Kit) firing alongside the GTM container. This is the one §4 row 2 + cutover-runbook Risk 6 already decided to migrate to.
- `AW-17076116496` — Google Ads conversion account with label `Hf8UCO6r84cZEN7Iyq0p`. Visible separately.

### What Brock actually owns (confirmed 2026-05-11 evening)

| Asset | ID | Status |
|---|---|---|
| GTM account "Spark Shark" | `6296666179` | OWNED |
| GTM container | `GTM-TBCXCXGS` (under that account, target `sparkshark.com`) | OWNED but NOT deployed on the live site |
| GA4 account "Flanco Electric" | `347644522` | OWNED |
| GA4 property `488680346` "Spark Shark" (under Flanco account!) | — | **OWNED. THIS IS THE LIVE PROPERTY.** Data stream `G-QK02QH3SWY` tracks `https://www.sparkshark.com/`, created 2025-05-09. ~1.1K active users since creation. Service account `sparkshark-seo-reader@fluid-emissary-493106-s2.iam.gserviceaccount.com` granted Viewer via API on 2026-05-11 (UI add was blocked by a GA4 validation bug; bypassed via `accessBindings.create` v1alpha endpoint). |
| GA4 property `480290314` "Flanco Electric (Old)" | — | OWNED — data stream `G-4TFM61SQED` tracks `https://flancoelectricok.com` (the legacy Flanco domain, NOT sparkshark.com). Holds pre-rebrand history only. SA granted Viewer via same API. |
| GA4 account "Spark Shark Analytics" | `348668675` | OWNED |
| GA4 property `481482348` "Spark Shark" | — | OWNED — likely a setup artifact. Streams `G-JF1630186D` + `G-8SGD0GKF4F` for case-variant URIs; ~20 users in 90d. Not the live destination. SA has Viewer. |

**Corrected verdict:** the GA4 destination layer for live `www.sparkshark.com` traffic is `G-QK02QH3SWY` → property `488680346`, **owned by Brock.** All historical referral data is recoverable (and was extracted on 2026-05-11; see evidence file below). The only unowned layer is `GTM-W7V4RS7C` itself.

### Live property `488680346` — referral data extracted 2026-05-11

229 unique pageReferrer × source × medium rows since 2025-05-09. Top external referrers (non-self, non-debug, non-staging):

| Source | Sessions | Notes |
|---|---|---|
| facebook.com / m.facebook.com / l.facebook.com / lm.facebook.com | 93 total | Confirms `facebook.com/sparksharkelectric` as a real driver |
| yelp.com / m.yelp.com (+ ca/uk/admin variants) | 48 total | Confirms `yelp.com/biz/spark-shark-electric-moore` |
| google.com / directory referrals | 32 | GBP "Directions" link clicks etc. |
| chatgpt.com | 5 | **LLM referrals — new discovery, not in GSC** |
| claude.ai | 5 | **LLM referrals — new discovery, not in GSC** |
| national.lightning.force.com | 5 | Partner-platform / national contractor network (Salesforce) |
| goodleap.lightning.force.com | 4 | GoodLeap financing partner (Salesforce) |
| bluebbb.org | 4 | BBB variant — verify |
| l.instagram.com | 4 | Already counted via `instagram.com/thesparkshark` |
| moranalytics.com | 4 | New discovery — SEO analytics tool |
| hometalk.com | 1 | New discovery — DIY home community |
| featured.com | 1 | Confirmed via GA4 (already in WebSearch list) |
| linkedin.com | 1 | Confirmed via GA4 |
| mapquest.com | 1 | Confirmed via GA4 (already in GSC) |

Full export: `migration-evidence-pack/07-backlinks-and-citations/ga4-referrals-property-488680346-all-history.csv`.

### Cutover implication (re-stated correctly)

The `build.py:153` swap planned in §4 row 2 + cutover-runbook Risk 6 (GTM → `gtag.js?id=GT-NGS794C2` loader) retires the unowned `GTM-W7V4RS7C` from the live site. After that swap, the GA4 destination should remain `G-QK02QH3SWY` (Brock-owned property `488680346`) **provided the new `GT-NGS794C2` unified tag points at the same measurement ID**. Verify this before shipping the swap — pre-swap verification step is the same as in §4 row 2.

### Post-cutover follow-up

- Wire Brock-owned `GTM-TBCXCXGS` into the new Vercel build if a future tag-manager surface is desired. The §4-row-2 decision is "skip GTM, use gtag.js directly" — that decision still stands; the `GTM-TBCXCXGS` reclaim is just bookkeeping.
- Audit whether any third party (Coalition successor, etc.) still has crawl/data access via the old `GTM-W7V4RS7C` container. Cannot affect Brock's GA4 data going forward once the swap ships, but worth understanding the historical access footprint. Out of scope for cutover.

### Evidence

- `migration-evidence-pack/07-backlinks-and-citations/SESSION-2-HANDOFF.md` — full session-1 detail + session-2 plan
- `migration-evidence-pack/07-backlinks-and-citations/master-backlinks-working.csv` — referring domains + GA4-new-discovery rows
- `migration-evidence-pack/07-backlinks-and-citations/ga4-referrals-property-488680346-all-history.csv` — 229-row full export
- `~/.claude/projects/-Users-brock/memory/project_sparkshark_gtm_ga4_ownership.md` — auto-memory entry

---

## 12. Known discrepancies (footnote)

When sources disagreed, the readiness audit at `audits/migration-readiness/2026-05-11.md` was treated as authoritative.

1. **HTML runbook headline vs readiness audit verdict.** ~~The HTML runbook banner says "5 of 6 risks already structurally mitigated — remaining exposure is operational." The readiness audit (16:24 UTC) found a NEW material failure — Vercel custom-domain attachment on the wrong team (DOM-01 / DOM-02 FAIL) — which the HTML banner does not reflect (though it does flag the same concern in its "What this runbook does NOT cover" section). **Prefer the readiness audit:** the domain attachment is a second independent auto-fail trigger and Blocker #1 in §2 here.~~ **Discrepancy resolved 2026-05-11**: DOM-01/02 FAIL is now CLOSED — apex + www verified on `sparkshark-com` project via cross-team TXT claim. The HTML runbook's 5-of-6 reading is now accurate for the domain-attachment dimension.
2. **Diff doc memory-citation provenance.** The seed-prompt diff doc cites three memory files that the cleanup-handoff manifest's initial grep did not find at `~/.claude/projects/-Users-brock/memory/`. The manifest later corrected this — the citations are real and live in session-scoped storage (path in §9). Both views are reconciled here; the memories are authoritative for the sub-tasks they describe.
3. **Brock-owned queue scope.** ~~The HTML runbook's 5-item Brock queue (§4 above) predates the DOM-01/02 discovery. The Vercel domain-attachment fix is required before that queue is meaningful, but is not numbered inside the queue itself. It appears as Blocker #1 in §2 and as an explicit prerequisite note under §4. Future revisions of the runbook should fold it in as a numbered step.~~ **Moot 2026-05-11**: Blocker #1 is CLOSED; the 5-item Brock queue can be executed as written.
4. **"Coalition-era abandoned" vs "loaded but unowned" — GTM-W7V4RS7C characterization.** The cutover-runbook Risk 6 narrative calls `GTM-W7V4RS7C` "Coalition-era GTM container — abandoned." Session-1 backlink audit (2026-05-11 evening) found the container ID still present in the live homepage `<noscript>` iframe AND its `gtm.js` configuration still contains GA4 measurement ID `G-QK02QH3SWY`. **"Loaded but unowned"** is the more accurate framing — the container is being requested and parsed by every visitor, even if Coalition has not added new tags inside it for some time. The functional impact is the same (the GTM swap planned in §4 row 2 still resolves it), but the framing matters for the post-cutover access-audit follow-up in §11. Prefer the §11 framing.

---

*End of source-of-truth document. Do not edit gate-row Status cells from here — they live in `docs/migration/launch-gate.md` and only Brock may write `Approved` or `Not Applicable: <reason>`.*

# Migration risk defense — pre-flip runbook

**Authored:** 2026-05-11 (converted from `spark-fsm/audits/migration-risk-defense-runbook-2026-05-11.html`)
**Purpose:** Map the six catastrophic migration failure modes to current sparkshark.com → Vercel cutover state, identify remaining gaps, and sequence pre-flip + post-flip actions to close them.
**Read alongside:** `docs/migration/launch-gate.md` (DNS authority) and `docs/migration/SOURCE-OF-TRUTH.md` (verdict + score).
**Provenance:** Verified against the 2026-05-10 evidence pack (GSC indexed pages, GSC performance, GSC external backlinks), `sparkshark-com/vercel.json`, and `sparkshark-com/sitemap.xml`.

> **Headline verdict:** 5 of 6 risks already structurally mitigated. No authority page is being deleted. No domain change. NAP frozen. Schema preserved. Remaining exposure is operational, not architectural — tracking IDs, GBP snapshot, scheduler smoke booking, NAP doc, and two minor redirect-coverage items.
>
> **Caveat from `SOURCE-OF-TRUTH.md` §11:** the headline above predates the 16:24 UTC readiness audit, which found a NEW material failure — Vercel custom-domain attachment is on the wrong team. See `SOURCE-OF-TRUTH.md` Blocker #1.

---

## Risk-by-risk mapping

### Risk 1 — Bulk redirecting to homepage (soft-404s, authority loss)

**Verdict:** STRUCTURALLY SAFE · 2 minor gaps

- **What we did:** 27 redirects in `vercel.json`. Most are 1-to-1 to relevant pages (panel post → panel page, generator post → `/generators/`, GFI post → `/switches-and-outlets/`). The 4 redirects to `/` are deliberate: commercial & industrial pages (residential-only constraint per memory `project_spark_shark_residential_only_constraint`) and two generic Flanco-era posts that have no on-brand replacement.
- **Evidence:** External backlinks CSV shows only two URLs with incoming external links — homepage (26 from 15 sites) and `/electrical-installation/` (2 from 2 sites). Both preserved unchanged. No site that links to us would hit a soft-404.
- **Gap:** 5 orphan HTML files exist on disk under `/2024/01/` for URLs that have 301 redirects in `vercel.json`. Vercel's routing order means redirects should win, but verify via curl on the preview alias before cutover. Also, `/2023/12/` and `/2024/01/` archive listing URLs will 404 (no redirect) — low priority since both are "crawled, not indexed" in GSC.

### Risk 2 — Old domain SSL/registration lapse (broken 301 chain, link equity loss)

**Verdict:** NOT APPLICABLE

- **Why N/A:** Same domain (sparkshark.com), new host. No domain change, no certificate handoff, no redirect chain from an old domain to a new one. Vercel issues SSL on cutover; GoDaddy keeps registration.
- **Confirmation:** GoDaddy domain registration confirmed active in launch-gate #5 evidence. Gate #5 Approved.
- **Residual action:** Pre-flip: confirm GoDaddy domain auto-renew is ON. Post-flip: confirm Vercel-issued cert appears valid in browser within 1 hour of cutover.

### Risk 3 — Deleting high-performing authority pages

**Verdict:** NO PAGE DELETED

- **What we did:** Audited all 22 GSC-indexed URLs against the new sitemap + `vercel.json`. Every indexed URL is either preserved at the same path or 301-redirected to a topically relevant new page. The two highest-traffic legacy blog posts (118 impressions / 21 impressions) are KEEPs in the sitemap (priority 0.5–0.6).
- **Evidence:** `gsc-indexed-pages-urls.csv` + `gsc-performance-pages-last-12-months.csv`. Homepage carries 26 of the 28 incoming external links — preserved. `/electrical-installation/` carries the other 2 — preserved.
- **Gap:** None at the authority-page level. Blog-audit DROPs (memory `project_sparkshark_blog_audit_2026_05_08`) have already been cross-checked against this CSV — none of the 4 DROP candidates carry external backlinks.

### Risk 4 — Fragmenting signals (changing too many variables at once)

**Verdict:** MULTI-VARIABLE CHANGE — NEEDS BASELINE

- **What's changing:** Host (WP Engine → Vercel), HTML markup (full content rewrite), URL structure (mostly preserved, some redirects). Domain unchanged. NAP unchanged. Phone unchanged. License unchanged. Schema graph architecture unchanged (4-node `@graph`).
- **Mitigation:** Variables that *could* have moved were deliberately frozen (NAP, phone, schema, scheduler ID, license). Same-domain cutover keeps Google treating us as the same entity.
- **Gap:** **Pre-cutover ranking baseline.** If positions drop post-flip, multi-variable change makes attribution hard. Capture GSC Performance snapshot for the top 10 URLs (clicks, impressions, position) and top 20 queries *before* DNS flips, so we have a comparison surface.

### Risk 5 — Google Business Profile disconnection

**Verdict:** LOW STRUCTURAL RISK · GBP SNAPSHOT MISSING

- **What we did:** Address unchanged (Moore OK 73160). Phone unchanged ((405) 436-4776). Website URL unchanged. License unchanged. No GBP move, no merge, no category change. Risk surface is "did we accidentally desync NAP somewhere on the new site" not "did we move GBP."
- **Mitigation in code:** `build.py` BRAND dict is single source of truth for NAP. `qa.py` enforces phone / city / ZIP / license on every page (Quality Gate, CI-blocked).
- **Gap:** Gate item #4 (GBP screenshots) is **Not Provided**. If anything diverges post-flip we need the baseline to prove what changed. 9 fields required: name, address/SAB, phone, website, primary category, secondary categories, services, hours, business description.

### Risk 6 — Silent data corruption (analytics/attribution loss)

**Verdict:** STATIC SITE = LOW DATA RISK · TRACKING PARTIAL

- **What we did:** Static HTML, no database migration. No risk of numeric precision or date format drift. Tracking strategy decided 2026-05-11: **skip GTM, use the unified Google Tag (`GT-NGS794C2`, Site Kit-managed)** — the same tag already proxying GA4 + Ads on the live WP site. `build.py:153` currently hardcodes a different/unused GTM container (`GTM-TBCXCXGS`) and will be replaced with a `gtag.js?id=GT-NGS794C2` loader (variable renamed `GTM_CONTAINER_ID` → `GOOGLE_TAG_ID`, doc comment above the var refreshed) before the preview alias is reverified. Contact form pipeline end-to-end verified (Resend delivery confirmed).
- **Evidence:** Live www.sparkshark.com inspection 2026-05-11 found three tag IDs on the WP install: `GTM-W7V4RS7C` (Coalition-era GTM container — abandoned), `AW-17076116496` (Google Ads conversion account with label `Hf8UCO6r84cZEN7Iyq0p`), and `GT-NGS794C2` (unified Google Tag via Site Kit — kept). Brock chose option 3: consolidate on the unified Google Tag and skip GTM as a management plane. Form submission test logged with Resend message ID `5cb36ea7-0b7e-4aae-8dc2-d4da078374b5`.
- **Live bug noted (separate from migration):** The Google Ads phone-click conversion on the live WP site uses a `tel:4054363776` selector that does not match the actual `tel:4054364776` link — phone-click conversions are not firing today. File a Strategy Zoo ticket; do not block cutover on it. Forward note: the Vercel build emits `tel:+14054364776` (E.164), so any phone-click trigger added to the unified Google Tag must target the new format.
- **GSC verification (carries through cutover, CONFIRMED 2026-05-11):** Brock's GSC property `https://www.sparkshark.com/` is verified via **Domain name provider** (DNS TXT), token `1DyR8lUgOXiQHuidohciuTVNngFZ06Xr7MVAeGgWHKA` at apex `sparkshark.com`. GSC Settings → Ownership verification UI confirms "You are a verified owner · Domain name provider · Successfully verified." No HTML-tag / GA / GTM / Site Kit dependency. Only A records flip at cutover; TXT records stay at GoDaddy, so Brock's GSC data inflow continues unchanged. The HTML-meta verification (`Fgyo9Rue-...`) on the live WP homepage is a separate account per the `build.py:146-152` comment (Coalition-era) — not Brock's monitoring surface; benign at cutover. Alternate methods exist but are inactive: an HTML file (`google973f9f3bb8715119.html` downloaded locally, never uploaded) and an HTML tag (would use the same `1DyR8lUg...` token, available as belt-and-suspenders via `GSC_VERIFICATION_VALUE` in `build.py:154` — not required).
- **Gap:** Gate #7 (GA4 / GTM / Ads IDs) still **Not Provided** at the documentation layer — `tracking-ids.md` not authored. Gate #8 (ST scheduler test) still **Not Provided**. Gate #9 (canonical NAP doc) still **Not Provided**.

---

## Honest framing — "100% guarantee"

No cutover is 100% safe. The discipline isn't a guarantee, it's a defense in depth: pre-flip evidence (so you know what "good" looked like), pre-flip verification (so you know the new site behaves correctly), post-flip monitoring (so you catch drift in hours not weeks), and a rollback playbook (so you can restore the prior state if something goes catastrophically wrong). Each of the six failure modes above maps to at least one defense at each layer. If we run the runbook below, none of the six should produce a permanent loss.

---

## Pre-flip action queue

### Brock-owned (close the launch gate)

1. **Capture GBP screenshots.** Defends Risk 5. Closes Gate #4. 9 fields: name, address/SAB toggle, phone, website URL, primary category, secondary categories, services list, hours, business description. Save into `/migration-evidence-pack/05-google-business-profile/`. ~10 min.
2. **Author `tracking-ids.md`.** Defends Risk 6. Closes Gate #7. Decision captured 2026-05-11: **skip GTM, use the unified Google Tag (`GT-NGS794C2`, Site Kit-managed)** — chosen over GTM after the live-tag inspection found three competing IDs on the WP install. Document: (a) `GT-NGS794C2` (the unified Google Tag), (b) the active GA4 measurement ID behind it (read from `05-ga4-data-streams.png` — the `https://sparkshark.com` stream, not the case-variant), (c) Google Ads `AW-17076116496` + label `Hf8UCO6r84cZEN7Iyq0p`. **Follow-up code work:** swap `build.py:153` GTM `<script>` + `<noscript>` for a `gtag.js?id=GT-NGS794C2` loader, rename `GTM_CONTAINER_ID` → `GOOGLE_TAG_ID`, refresh the doc comment block above the var, then reverify the preview alias. ~5 min decision capture; build.py patch is separate work.
3. **Run ST scheduler smoke booking.** Defends Risk 6 + booking pipeline. Closes Gate #8. Submit a test booking from the live Vercel preview alias `sparkshark-com-git-main-spark-shark-electric-2b2f3a3a.vercel.app`, confirm it appears in ServiceTitan, then cancel it. Screenshot before/after. Save to `/migration-evidence-pack/06-current-tracking/servicetitan-scheduler-test-proof/`. ~10 min.
4. **Fill in `canonical-nap.md`.** Defends Risk 5. Closes Gate #9. Use the template at `/migration-evidence-pack/11-verified-business-facts/canonical-nap-template.md`. Decisions needed: address vs SAB-only, phone in E.164, GBP URL, service-area list, citation-update priority list. ~10 min.
5. **Confirm GoDaddy auto-renew is ON** for sparkshark.com registration. Defends Risk 2. ~2 min.
6. ~~**Confirm GSC verification method in the UI.**~~ **CLOSED 2026-05-11.** GSC Settings → Ownership verification screenshot confirms property `https://www.sparkshark.com/` is verified via **Domain name provider** (DNS TXT, token `1DyR8lUg...` at apex). No further pre-flip action needed.

### Claude-owned (verification + baseline capture)

1. **Capture pre-cutover GSC baseline.** Defends Risk 4. Re-export GSC Performance for last 28 days (clicks/impressions/position) for top 10 pages and top 20 queries. Save into `/migration-evidence-pack/04-google-search-console/06-baseline-pre-cutover-2026-05-XX/`. Done already for last-12-month window; need short-window snapshot to detect day-of drift.
2. **Curl-verify redirect routing on the preview alias.** Defends Risk 1. For each of the 27 redirects in `vercel.json`, confirm HTTP 301 (not 200) on the preview alias. Surfaces the orphan-HTML question — if any URL returns 200 with content instead of 301, the file should be removed from the static output before flipping DNS.

   ```bash
   for path in commercial-electrical-solutions industrial-electrical-solutions \
       2023/12/29/closing-the-deal-with-confidence-why-realtors-should-choose-spark-shark-for-home-repairs \
       2024/01/02/powering-tomorrow-a-comprehensive-guide-to-new-construction-wiring-with-spark-shark \
       our-residential-electrical-services projects fiancing price repair \
       2023/12/28/where-does-it-come-from; do
     code=$(curl -sI -o /dev/null -w "%{http_code}" \
       "https://sparkshark-com-git-main-spark-shark-electric-2b2f3a3a.vercel.app/${path}/")
     echo "$code  /${path}/"
   done
   ```
3. **Curl-verify schema integrity on 3 critical pages.** Defends Risk 4. For `/`, `/contact-us/`, `/electrical-panels/` on the preview alias: confirm the 4-node `@graph` (WebSite + Organization + LocalBusiness/Electrician + FAQPage) is present and validates. ServiceTitan scheduler embed renders. NAP strings exact-match BRAND dict.
4. **Confirm `sitemap.xml` + `robots.txt` on the preview alias** match the production-intended URL set (build-time `BASE=""`, root-relative URLs, no `/sparkshark-com/` prefix anywhere).
5. **Consider adding redirects for `/2023/12/` and `/2024/01/`** archive listing URLs (currently 404 post-flip). Defends Risk 1. Low priority — both URLs are "crawled, not indexed" in GSC, so authority impact is minimal. Could 301 to `/blogs/`. Worth one PR if everything else clears.
6. **Confirm the four prepped sparkshark-com PRs (#7 / #8 / #9 + spark-fsm PR #142 follow-ups)** are merged into `main` and reflected in the preview alias before DNS flip. Per memory `project_cutover_2026_05_11`.

---

## DNS-flip day-of

1. **Re-read `docs/migration/launch-gate.md`.** Every row Approved or Brock-written "Not Applicable: \<reason\>". If any row is still Not Provided / Provided-Not-Reviewed / Reviewed-Needs-Fix → **STOP**.
2. **Confirm WP Engine "Migration Backup 05-10-2026" is still listed** in the backup history. Gate #6 evidence remains valid only if the backup exists. ~1 min.
3. **Take the final pre-flip prod-state screenshot** of `www.sparkshark.com` (currently WP Engine). One full-page desktop screenshot, one mobile-UA capture. Save into `/migration-evidence-pack/12-launch-and-rollback/pre-flip-final-state-<UTC-timestamp>/`.
4. **Flip the GoDaddy A record** for `@` from `141.193.213.10` + `141.193.213.11` to the Vercel target. Note exact UTC timestamp. (Vercel-supplied target IP / CNAME from the dashboard.)
5. **Start the post-flip monitor immediately** (next section).

---

## Post-flip monitor — 72-hour window

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

## Rollback playbook

| Scenario | Action | Recovery time |
|---|---|---|
| Vercel deploy serves broken content | Promote previous deploy from Vercel dashboard (Deployments → … → Promote to Production) | < 5 min |
| SSL cert not issued within 15 min of DNS flip | Wait 30 min total. If still not issued, contact Vercel support. | < 60 min |
| Site fundamentally broken; want WP back | Revert GoDaddy A record to `141.193.213.10` + `141.193.213.11` per Gate #5 screenshots. DNS TTL determines propagation (5–30 min). | 15 – 60 min |
| WP Engine site itself drifted during cutover | WP Engine portal → Backups → restore "Migration Backup 05-10-2026" (Gate #6 evidence). Then revert DNS as above. | 30 – 90 min |
| GSC shows mass-404 spike post-flip | Identify the 404'd URLs (GSC Coverage), add 301s to `vercel.json`, push to `main`, Vercel rebuilds. | < 30 min per URL set |

---

## What this runbook does NOT cover

Out of scope — these are tracked elsewhere and need their own discipline:

- **Third-party citation updates** (BBB OKC alt-profile dedup, Networx Flanco-era listing takedown, MapQuest / CallUpContact NAP verification). Per backlinks audit — recommend a separate post-cutover task.
- **llms.txt + llms-full.txt regeneration** at build time. Already wired into `build.py`; verify they emit `BASE=""` paths in the Vercel build. (Open drift: `llms.txt` currently says `4.9` while `BRAND` + `llms-full.txt` say `4.8` — RANK-08 FAIL in readiness audit.)
- **Resend API key rotation** (open BLOCKER per `sparkshark-cutover-2026-05-11-autonomous-closeout.html` banner). Not a migration risk in the 6-failure-mode sense, but a security blocker that should be cleared before flip.
- **Vercel custom-domain attachment** — re-verify the domain is attached at the Vercel project level (and to the **`sparkshark-com`** project, not `spark-fsm`) before flipping DNS, or a 404 hits 100% of visitors. This is Blocker #1 in `SOURCE-OF-TRUTH.md` §2.

---

## Sources

- `sparkshark-com/vercel.json`
- `sparkshark-com/sitemap.xml`
- `sparkshark-com/docs/migration/launch-gate.md`
- `/Users/brock/Downloads/migration-evidence-pack 6/04-google-search-console/`
- `/Users/brock/Downloads/migration-evidence-pack 6/07-backlinks-and-citations/`
- Cross-references: `.claude/rules/seo-geo-verification.md`, `.claude/rules/leverage-suggestions.md`
- Memory entries: `project_cutover_2026_05_11`, `project_spark_shark_residential_only_constraint`, `project_cutover_reality_check_2026_05_10`

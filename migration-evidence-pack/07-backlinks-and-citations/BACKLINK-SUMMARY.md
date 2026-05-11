# Backlink Capture — Cumulative Summary (NOT final)

**Status as of 2026-05-11 evening:**
55 deduped rows in `master-backlinks-cumulative.csv` (committed alongside this doc) — covering Google Search Console (May 10 audit) + open-web WebSearch pass + Bing index probe + GA4 referrals from the live property + collision-filter rows.

**This is explicitly NOT a "final" list.** Major sources are still unrun (Ahrefs AWT, WP Engine access logs, Common Crawl). Final naming will only be applied when those run or are deliberately closed out. See §7 confidence statement.

**Sources consolidated:**
- ✅ Google Search Console (28 URLs / 17 domains) — Apr–May 2026 (May 10 manual export)
- ✅ Bing Webmaster API (`GetUrlLinks`) — index returned 0 inbound links as of session 1; re-check in 24–72h
- ✅ Open-web WebSearch pass (+10 Brock-owned/-referencing + 7 collision-filter rows)
- ✅ **GA4 referrals (property 488680346) — 229 pageReferrer rows since 2025-05-09.** Resolved 2026-05-11 evening: the SA was added via v1alpha `accessBindings.create` after UI grant was blocked by a Workspace validation bug. The live `G-QK02QH3SWY` measurement ID lives in this property (under Brock's Flanco Electric GA4 account 347644522, NOT under Spark Shark Analytics). Full export: `ga4-referrals-property-488680346-all-history.csv`. 9 new domain rows merged into the cumulative CSV; see §1.5.
- ⛔ **Ahrefs Webmaster Tools** — **NOT RUN.** Chrome MCP not connected. See "Blocked work" below.
- 🟡 Wayback CDX enrichment — **DEFERRED.** Attempted via both `cdx/search/cdx` and `/wayback/available` endpoints this session. archive.org returned timeouts on unfiltered CDX queries and empty `archived_snapshots` responses on `/wayback/available` for known-archived URLs (verified against `wikipedia.org/wiki/Oklahoma_City` as a baseline — returned empty, indicating a degraded backend). Reattempt in a future session when archive.org is healthy.
- ⛔ WP Engine access logs — **NOT RUN.** Pending API token rotation after 2026-05-11 leak.
- ⛔ Common Crawl Athena — **DEFERRED** per Brock decision.

---

## 1. Topline numbers (cumulative as of 2026-05-11 evening)

| Tier | Count | What it means |
|---|---|---|
| **P0** | 1 | Hard NAP/brand conflict — fix before DNS flip |
| **P1** | 8 | Verify NAP / claim profile before DNS flip |
| **P2** | 19 | Post-launch cleanup (claim, verify, refresh bio) — +4 from GA4 LLM/new-domain finds |
| **P3** | 19 | Co-citation noise + GA4 internal-platform referrers (Salesforce CRMs etc.) — monitor, no action |
| **IGNORE** | 7 | Other "Spark Shark" businesses (Canada / Wisconsin / California) — filter from any future scrape |
| **Total real backlinks (cumulative)** | **48** | (excludes IGNORE collisions) |
| Confirmed Brock-owned | 21 | |
| Confirmed not-owned | 17 | |
| Unknown | **10** | mostly GA4-derived (LLM referrals, partner CRMs) — need on-page verification to confirm "real" backlinks vs. paste-and-click referrers |

## 1.5. New domains from GA4 (added this session)

9 net-new referring domains from GA4 property 488680346 (live `G-QK02QH3SWY`), not previously in GSC/WebSearch:

| Domain | GA4 sessions | Tier | Notable |
|---|---|---|---|
| chatgpt.com | 5 | P2 | **LLM referral — new class of backlink** |
| claude.ai | 5 | P2 | **LLM referral — new class of backlink** |
| moranalytics.com | 4 | P2 | SEO analytics tool — verify the mention |
| bluebbb.org | 4 | P3 | BBB variant — verify it's not a scraper clone |
| hometalk.com | 1 | P2 | DIY home community |
| marketspacesales.com | 1 | P3 | Verify mention |
| national.lightning.force.com | 5 | P3 | Internal CRM (Salesforce) — referrer, not a public backlink |
| goodleap.lightning.force.com | 4 | P3 | GoodLeap financing partner CRM — same |
| servicetitan.lightning.force.com | 3 | P3 | ServiceTitan internal CRM — same |

**Evidence caveat:** GA4 captures Referer headers, which include both clicks from `<a href>` (real backlinks) AND paste-and-click navigations (no link on the source page). The five `P2` domains above are **candidate backlinks pending on-page verification** — open each, search the rendered DOM/source for `sparkshark.com`. Once a verified on-page link exists, promote `confirmed_brock_owned`/risk tier. Don't claim "real backlink" without that evidence.

GA4 also reconfirmed seven already-listed domains (facebook, yelp, mapquest, linkedin, featured.com etc.), strengthening the existing rows. Full domain rollup in `ga4-referrals-property-488680346-all-history.csv`.

---

## 2. Top 5 link equity assets (Brock-owned, high traffic potential)

1. **BBB Moore profile** — `bbb.org/us/ok/moore/profile/electrical-contractors/spark-shark-electric-0995-90130075` (P1). High-trust signal. Plus a duplicate OKC `addressId/134759` profile that needs to be reconciled (one BBB business, two addresses).
2. **Yelp** — `yelp.com/biz/spark-shark-electric-moore` (P1). High-value review platform; address 621 Sally Ct Moore matches Brock's. Claim if not already.
3. **Thumbtack** — `thumbtack.com/ok/oklahoma-city/electrical-repairs/spark-shark-electric/service/489603470823817221` (P1). Lead-gen platform; claim listing.
4. **Facebook Business page** — `facebook.com/sparksharkelectric/` (P1). Confirmed Brock-owned (OKC service area + 405-436-4776 + theteam@sparkshark.com per screenshot 2026-05-11).
5. **Instagram** — `instagram.com/thesparkshark/` (P1). Confirmed Brock-owned (OKC Family Owned + 405-436-4776 + sparkshark.com link per screenshot). **Not** `@sparksharkelectric` — that handle is the Ontario business.

Honorable mentions: Chamber of Commerce, MapQuest, Pinterest, X/Twitter, TikTok (`@sparkshark.com`), ProvenExpert, theorg, Featured.com Brock profile, agreatertown, LinkedIn personal.

---

## 3. Top 3 risks (must fix before DNS flip)

1. **`networx.com/c.flanco-electric` (P0).** Last seen 2025-11-09. Active Flanco-era citation under the prior brand name. Conflicts with the Spark Shark public NAP. **Request takedown or rebrand.**
2. **BBB duplicate addresses (P1).** Same Spark Shark business profiled at two distinct BBB URLs (`/moore/...` and `/oklahoma-city/...addressId/134759`). Reconcile to a single canonical address before launch so review signals aren't split.
3. **Apex profile validation gap (P1).** Of the 21 Brock-owned profiles, 9 carry NAP that is presumed-correct but not verified row-by-row in this audit (Mapquest, Chamber of Commerce, Pinterest, ProvenExpert, Twitter/X, TikTok, theorg, agreatertown, Featured). At least one phone/address-mismatch on a top result will degrade post-cutover trust signals. **Action:** open each, screenshot, fix in place where Brock controls login.

---

## 4. P0/P1/P2/P3 action list

### P0 — Before DNS flip (1)
- [ ] Request `networx.com/c.flanco-electric` takedown or rebrand to Spark Shark URL.

### P1 — Before DNS flip (8)
- [ ] Reconcile two BBB profiles into one canonical address.
- [ ] Verify NAP on `chamberofcommerce.com/business-directory/oklahoma/moore/electrician/2034210950-spark-shark-electric`.
- [ ] Verify NAP on `mapquest.com/us/oklahoma/spark-shark-electric-778761940`.
- [ ] Claim/verify Yelp listing at `yelp.com/biz/spark-shark-electric-moore`.
- [ ] Claim/verify Thumbtack listing at the long Spark Shark URL.
- [ ] Verify Facebook page bio links + featured info (already confirmed owned).
- [ ] Verify Instagram bio at `@thesparkshark` (already confirmed owned).

### P2 — Post-launch cleanup (15)
- [ ] Verify ownership and bio on Pinterest, ProvenExpert, theorg, agreatertown, Featured, TikTok.
- [ ] Verify Twitter/X profile (treat `twitter.com` + `x.com` as one — same `@The_Spark_Shark` account).
- [ ] Audit `uscity.net/listing/spark_shark_electric-12248252` — HTTP-only, request HTTPS upgrade.
- [ ] Audit two `best-electrician-moore.com` listicles for accurate Spark Shark mention.
- [ ] Audit `smartelectricalservices.net/business/spark-shark-electric-ok-91055/` (third-party directory).
- [ ] Verify/claim `callupcontact.com/b/businessprofile/Spark_Shark_Electric/9878135` (ownership unknown).
- [ ] Update LinkedIn personal at `linkedin.com/in/brock-flanary/` with current Spark Shark CEO title (per global-CLAUDE.md "Founder, CEO" rules — never "owner").
- [ ] Confirm `glassdoor.com/job-listing/...spark-shark-electric...` reflects current hiring state.

### P3 — Monitor only (15)
- [ ] No action on yellowpages.com category/competitor pages (co-citation noise, no Spark Shark profile).
- [ ] No action on superpages.com / dexknows.com generic category pages.
- [ ] No action on Medium / Reddit / Facebook group single-mention links.

### IGNORE — Filter from future scrapes (7)
Other Spark Shark businesses (Canada / Wisconsin / California). Cross-domain hit list maintained in the working CSV.

---

## 5. Blocked work — Brock-action required

### A. Chrome MCP for Ahrefs scrape — TOP-PRIORITY GAP
- **Symptom:** Session 2's #1 deliverable was the Ahrefs AWT scrape via `mcp__claude-in-chrome__*` tools. ToolSearch confirms those tools are NOT in the deferred tool list for this session.
- **Why it matters:** Free Ahrefs AWT typically surfaces 5–50× more referring URLs than GSC (~28 → potentially 100s–1000s). Without it the inventory is materially incomplete relative to what's discoverable.
- **Fix path A (preferred):** install/connect the claude-in-chrome browser extension and re-run this session. Reference: https://www.claude.com/product/claude-code (extension listing).
- **Fix path B (manual fallback):** Brock logs into `ahrefs.com/webmaster-tools` → Spark Shark site → **Backlinks** report → screenshot the table or paste rows into a CSV → drop file at `migration-evidence-pack/07-backlinks-and-citations/ahrefs-awt-manual.csv`. Repeat for **Referring Domains** report. Claude will dedup + merge into the master list.
- **Fix path C (not recommended):** Ahrefs CSV export requires the Lite plan ($129/mo). Skip unless multi-month link-monitoring is desired.

### B. GA4 service-account access on Flanco properties — ✅ RESOLVED 2026-05-11 evening
- **Original symptom:** SA returned 403 PERMISSION_DENIED on properties 480290314 + 488680346; UI add was blocked by a "doesn't match Google Account" Workspace validation bug.
- **Resolution:** bypassed via `POST /v1alpha/properties/{id}/accessBindings` using a Brock-authorized OAuth token (analytics.manage.users scope, obtained via OAuth Playground). Both adds returned HTTP 200; SA now has Viewer on all 3 of Brock's GA4 properties.
- **What we pulled:** 229 referral rows from property 488680346 (the LIVE property — stream `G-QK02QH3SWY` → `https://www.sparkshark.com/`, created 2025-05-09). Full export: `ga4-referrals-property-488680346-all-history.csv`. 9 net-new domains merged into the cumulative CSV (see §1.5).
- **Side benefit realized:** confirmed that `G-QK02QH3SWY` lives in Brock-owned property 488680346 (under the Flanco Electric account, NOT under Spark Shark Analytics). This closes most of the analytics-ownership concern in `docs/migration/SOURCE-OF-TRUTH.md` §11 — only the GTM container layer remains unowned, the GA4 destination is owned.
- **Note for future sessions:** if UI grant fails for an SA with a similar "doesn't match Google Account" error, use the v1alpha API path directly (v1beta returns 404 — accessBindings was kept at v1alpha).

### C. WP Engine API token rotation — NOT DONE
- **Symptom:** 1Password item `wp_engine` (vault SparkShark) last `updated_at` is 2026-05-02. The leak that triggered the rotation requirement happened 2026-05-11 (during this session's predecessor). Token has not been rotated.
- **What this blocks:** WP Engine Public API access for access-log retrieval (`GET /v1/installs/{id}/logs`), which would surface server-side referrer headers and complement the GSC/AWT picture with real inbound-traffic data.
- **Fix:** at `my.wpengine.com` → API Access → revoke the current token and generate a new one → update 1Password item `wp_engine` field `API_Token` (CONCEALED) and field `API Username` (the new UUID).
- **Standing reminder:** the leaked Customer Portal **password** also needs rotation per Brock's 2026-05-11 evening memory note.

### D. AWS Athena Common Crawl — deferred per Brock
- Status unchanged from session 1. ~$5-15 query; covers open-web inbound links beyond Ahrefs/GSC. Reopen when ready.

---

## 6. Files in this directory (artifact map)

```
master-backlinks-working.csv       # Mutable working log; rows appended as discovered
master-backlinks-cumulative.csv    # 55 deduped rows, normalized URLs; NOT "final" — Ahrefs + WPE + Athena still pending
ga4-referrals-property-488680346-all-history.csv  # 229 GA4 referral rows since 2025-05-09 (this session's add)
BACKLINK-SUMMARY.md                # This document
BACKLINK_RISK_FINDINGS.md          # May 10 GSC classification (source-of-truth for tiers)
gsc-link-summary-by-domain.csv     # Per-domain rollup with risk tier + recommended action
gsc-external-links-all-deduped.csv # Session 1 GSC export (28 URLs / 17 domains)
gsc-links-external-*.csv           # Raw GSC exports (preserved for audit trail)
gsc-links-internal-*.csv           # Internal-link exports (out of scope for backlink audit)
SESSION-2-HANDOFF.md               # Session 1→2 handoff doc (kept for trace)
```

Script artifacts (not committed; live in `/tmp/sparkshark-backlinks/`):
- `ga4_pull.py`, `ga4_check_all.py` — GA4 Data API pull scripts (rerun once access granted)
- `wayback_fast.py`, `wayback_v3.py` — Wayback enrichment attempts (deferred; reattempt when archive.org is healthy)
- `dedup_pipeline.py` — Normalization + dedup pipeline (idempotent; safe to rerun)

---

## 7. Confidence statement (updated 2026-05-11 evening)

This list is **cumulative across the sources we have reached so far** — GSC, Bing index, open-web search, and now the live GA4 property's referral history. It is **NOT final** and is **materially incomplete vs. what is discoverable** until at minimum:
1. Ahrefs Webmaster Tools data is captured (via Chrome MCP scrape OR manual UI export by Brock OR Lite-tier CSV export)
2. WP Engine access logs are pulled (after API token rotation)

**Evidence quality by row:**
- The 39 rows from GSC + WebSearch are **verified backlinks** — each is an external page known to contain an `<a href>` pointing to sparkshark.com (either via GSC's link graph or via WebSearch confirmation).
- The 9 new GA4-derived rows in §1.5 are **candidate backlinks** — they sent traffic to sparkshark.com with a non-empty `Referer` header, but on-page link presence has NOT been verified for any of them yet. The two LLM referrals (chatgpt.com, claude.ai) are highly likely to be real links (LLMs include URLs in answers) but should still be opened and confirmed. The partner-CRM rows (Salesforce Lightning) are referrers, not public-web backlinks.
- The 7 collision-filter rows are confirmed NOT-Brock's businesses (Ontario / Wisconsin / California Spark Sharks).

The Brock-owned vs. third-party split is high-confidence (handles cross-checked against NAP). The collision filter has caught 7 wrong-business hits so far; rerun against any new source.

**Floor / ceiling estimate:** treat the 48 real-backlink rows as the floor. Post-Ahrefs and post-WPE-log expansion typically lands between 80 and several hundred URLs for a local-service site like this. Final "no more sources to check" status will only be claimed once those two streams are either landed or deliberately closed out by Brock.

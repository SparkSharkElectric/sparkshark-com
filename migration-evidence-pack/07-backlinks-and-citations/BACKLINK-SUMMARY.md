# Backlink Capture — Final Summary

**Status as of 2026-05-11 (Session 2 close):**
46 deduped rows in `master-backlinks-final.csv` (committed alongside this doc) — covering Google Search Console (May 10 audit) + open-web WebSearch pass + Bing index probe + collision-filter rows.

**Sources consolidated:**
- ✅ Google Search Console (28 URLs / 17 domains) — Apr–May 2026
- ✅ Bing Webmaster API (`GetUrlLinks`) — index returned 0 inbound links as of session 1; re-check in 24–72h
- ✅ Open-web WebSearch pass (+10 Brock-owned/-referencing + 7 collision-filter rows)
- ⛔ **Ahrefs Webmaster Tools** — **NOT RUN this session.** Chrome MCP not connected. See "Blocked work" below.
- ⛔ **GA4 referrals (Flanco 480290314 + Spark Shark 488680346)** — **NOT RUN.** Service account returns HTTP 403 PERMISSION_DENIED on both. Grants either didn't apply or were made to a different SA email. See "Blocked work."
- 🟡 Wayback CDX enrichment — **DEFERRED.** Attempted via both `cdx/search/cdx` and `/wayback/available` endpoints this session. archive.org returned timeouts on unfiltered CDX queries and empty `archived_snapshots` responses on `/wayback/available` for known-archived URLs (verified against `wikipedia.org/wiki/Oklahoma_City` as a baseline — returned empty, indicating a degraded backend). Reattempt in a future session when archive.org is healthy.

---

## 1. Topline numbers

| Tier | Count | What it means |
|---|---|---|
| **P0** | 1 | Hard NAP/brand conflict — fix before DNS flip |
| **P1** | 8 | Verify NAP / claim profile before DNS flip |
| **P2** | 15 | Post-launch cleanup (claim, verify, refresh bio) |
| **P3** | 15 | Co-citation noise — monitor, no action |
| **IGNORE** | 7 | Other "Spark Shark" businesses (Canada / Wisconsin / California) — filter from any future scrape |
| **Total real backlinks** | **39** | (excludes IGNORE collisions) |
| Confirmed Brock-owned | 21 | |
| Confirmed not-owned | 17 | |
| Unknown | 1 | |

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

### B. GA4 service-account access on Flanco + Spark Shark #2 — verified 403 today
- **Symptom:** SA `sparkshark-seo-reader@fluid-emissary-493106-s2.iam.gserviceaccount.com` returns HTTP 403 PERMISSION_DENIED on both property 480290314 (Flanco Electric) and 488680346 (Spark Shark #2). Only property 481482348 (Spark Shark #1) is accessible. Confirmed via 3 retries spread over ~10 minutes; not a propagation delay.
- **What this blocks:** legacy referral history from the Flanco pre-rebrand window — would surface inbound traffic sources that may not appear in GSC's index (referring sites that don't host their own crawlable link). Also blocks confirmation of whether `G-QK02QH3SWY` lives on property 488680346.
- **Fix:** in Google Analytics → Admin → Property Access Management → on each of properties 480290314 + 488680346, **verify** the user added is exactly `sparkshark-seo-reader@fluid-emissary-493106-s2.iam.gserviceaccount.com` (not a different `@`-domain service account from another project), and role is **Viewer or higher**. After verification, send "retry" and Claude will pull + merge in <5 min.
- **Side benefit:** confirming whether `G-QK02QH3SWY` is on 488680346 closes the analytics-ownership gap documented in `docs/migration/SOURCE-OF-TRUTH.md` §11.

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
master-backlinks-final.csv         # SESSION 2 OUTPUT: 46 deduped rows, normalized URLs
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

## 7. Confidence statement

This list is **complete for the sources we can currently reach** (GSC + Bing index + open-web search). It is **materially incomplete vs. what's discoverable** until either Chrome MCP runs the Ahrefs scrape or Brock drops a manual Ahrefs export. Treat the current 39 real backlinks as the floor, not the ceiling — expect the post-Ahrefs total to land somewhere between 60 and several hundred URLs based on typical free-AWT coverage on local-service domains.

The Brock-owned vs. third-party split is high-confidence (handles cross-checked against confirmed social handles + NAP). The collision filter has caught 7 wrong-business hits so far; rerun against any new source.

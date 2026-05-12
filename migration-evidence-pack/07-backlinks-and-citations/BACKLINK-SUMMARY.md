# Backlink Capture — Cumulative Summary (NOT final)

**Status as of 2026-05-12 (Session 3 — Ahrefs AWT scrape landed):**
**145 rows / 129 unique referring domains** in `master-backlinks-cumulative.csv` — covering Google Search Console + open-web WebSearch + Bing index probe + GA4 referrals (live property 488680346 + Flanco-legacy property 480290314) + **Ahrefs Webmaster Tools (Site Explorer Backlinks + Referring Domains, scraped 2026-05-12)** + Wayback CDX enrichment pass.

**Headline from the Ahrefs pull:** Ahrefs' index for `sparkshark.com` is **dominated by junk** — not "5,000 editorial links," but **1,080 total backlinks of which ~895 come from just two scraper domains** linking pre-Spark-Shark *credit-repair / RSS* content still indexed at `sparkshark.com/archives/2008…2011/*`, plus **~75 throwaway SEO-PBN spam domains** (`.shop` / `.top` / `.click` / `.agency` / `seoexpress.*` / `rankvance*` etc.), almost all first-seen Sept 2025 → May 2026. **Ahrefs itself spam-flags 82 of the 90 referring domains.** Only ~5 net-new *plausibly-real* referring domains came out of it. → **Recommend building a Google Disavow file for these 82 domains as a post-launch task** (see §1.6 + new action list item). This is not a cutover blocker, but it changes the "link equity" story: there is very little of it, and a meaningful slice of the profile is mild reputational/SEO risk.

**This is still explicitly NOT a "final" list.** Naming stays "cumulative" because WP Engine access logs remain unrun (API-token rotation pending) and were not deliberately closed out. See §7.

**Sources consolidated:**
- ✅ Google Search Console (28 URLs / 17 domains) — Apr–May 2026 (May 10 manual export)
- ✅ Bing Webmaster API (`GetUrlLinks`) — index returned 0 inbound links (re-probed 2026-05-11, no change). Bing's index is empty for sparkshark.com.
- ✅ Open-web WebSearch pass (+10 Brock-owned/-referencing + 7 collision-filter rows)
- ✅ GA4 referrals — live property 488680346 (`G-QK02QH3SWY`, 229 rows since 2025-05-09) + Flanco-legacy property 480290314 (153 rows). 13 net-new domain rows total. Full exports: `ga4-referrals-property-488680346-all-history.csv`, `ga4-referrals-property-480290314-flanco-legacy.csv`.
- ✅ **Ahrefs Webmaster Tools — DONE 2026-05-12.** Scraped via Playwright MCP against Ahrefs' own `/v4/seBacklinks` + `/v4/seRefdomains` JSON endpoints (free-tier UI data; no paid API). Project `9816270` = verified `*.sparkshark.com/*` (subdomains, both protocols) — the superset of the `www.sparkshark.com` verified project (90 vs 71 referring domains). **1,000 of 1,080 URL-level backlinks** captured (free AWT hard-caps result offset at <1000; pulled traffic-DESC rows 0–999 + traffic-ASC rows 0–499 and de-duped by link-id, so the ~80 lowest-traffic rows we couldn't reach are more of the same two scraper domains). **All 90 referring domains** captured. Raw: `ahrefs-awt-backlinks-raw.json`, `ahrefs-awt-refdomains-raw.json`. CSVs: `ahrefs-awt-backlinks-scrape.csv` (1,000 rows, 29 cols), `ahrefs-awt-referring-domains-scrape.csv` (90 rows, 13 cols).
- ✅ **Wayback CDX enrichment — DONE 2026-05-12.** archive.org was healthy this session (CDX + `/wayback/available` both responsive, ~7–12 s). Ran exact-URL CDX (`statuscode:200`) against all 143 distinct referring URLs in the master. **Only 2 had any archived snapshot:** `networx.com/c.flanco-electric` (1 snapshot, 2025-01-18 — confirms the P0 Flanco-era citation existed) and the Thumbtack listing (2 snapshots, Jul–Oct 2025). The other 141 returned 0 — consistent with the AWT-discovered links being overwhelmingly brand-new spam and the directory/social deep-URLs not being archived. `wayback_*` columns populated where hit; `wayback_snapshot_count_200 = 0` where confirmed absent.
- ⛔ WP Engine access logs — **NOT RUN.** Blocked on WPE API-token rotation after the 2026-05-11 leak (1Password item `wp_engine`). Until then, server-side referrer headers are unavailable.
- ⛔ Common Crawl Athena — **DEFERRED** per Brock decision.

---

## 1. Topline numbers (cumulative as of 2026-05-12)

| Tier | Rows | What it means |
|---|---|---|
| **P0** | 1 | Hard NAP/brand conflict — fix before DNS flip (`networx.com/c.flanco-electric`) |
| **P1** | 8 | Verify NAP / claim profile before DNS flip |
| **P2** | 24 | Post-launch cleanup (claim, verify bio) + 4 Ahrefs-discovered "verify the mention" candidates |
| **P3** | 23 | Co-citation noise + GA4 internal-CRM referrers + Ahrefs feed-scraper junk — monitor, no action |
| **DISAVOW** | 82 | **NEW.** Ahrefs-surfaced spam link-scheme / PBN domains (75) + legacy credit-repair / RSS scrapers (`rss2.com`, `debt-reduction-solution.com`, `mu.nu`). Recommend a Google Disavow file post-launch. |
| **IGNORE** | 7 | Other "Spark Shark" businesses (Ontario / Wisconsin / California) — filter from any future scrape |
| **Total rows** | **145** | across **129 unique referring domains** |
| Real / actionable referring domains | **42** | i.e. non-DISAVOW, non-IGNORE (see §1.5 list) |
| Confirmed Brock-owned | 21 | unchanged |
| Confirmed not-owned | ~19 | |
| Unknown (need on-page verification) | ~14 | mostly GA4-derived + 4 Ahrefs candidates |

**Reality check on "link equity":** for a DR-1 site, this is about what you'd expect — a thin profile of directory/citation listings + social profiles + a few editorial mentions, sitting under a pile of automated spam. The Ahrefs pull did **not** materially expand the useful inventory; it mostly revealed the spam surge + the domain's pre-Flanco history.

## 1.5. The 42 real / actionable referring domains

`agreatertown.com · anationofmoms.com · bbb.org · best-electrician-moore.com · bluebbb.org · callupcontact.com · chamberofcommerce.com · chatgpt.com · claude.ai · coalitiontechnologies.com · dexknows.com · exchange.construction · facebook.com · featured.com · glassdoor.com · goodleap.lightning.force.com · hometalk.com · hypnosistacticsguide.com · mapquest.com · marketspacesales.com · medium.com · moranalytics.com · national.lightning.force.com · networx.com · pinterest.com · provenexpert.com · reddit.com · servicetitan.lightning.force.com · siteliner.com · smartelectricalservices.net · superpages.com · themusemark.com · theorg.com · thumbtack.com · tiktok.com · twitter.com · uscity.net · wpengine.com · x.com · yellowpages.com · yelp.com · yplocal.us`

(Note: several of these are themselves noise — `*.lightning.force.com` are partner-CRM referrers not public backlinks; `yellowpages.com/superpages/dexknows` are category pages not Spark Shark profiles; `siteliner.com/coalitiontechnologies.com/wpengine.com` are tool/agency/staging referrers. The genuinely-Brock-owned subset and the high-trust citation profiles are enumerated in §2.)

## 1.6. Ahrefs profile breakdown (the junk picture)

| Bucket | Domains | Backlinks | Notes |
|---|---|---|---|
| **`rss2.com`** | 1 | ~542 | Feed-republisher; scraped a feed titled "the spark shark" (first seen 2024-01) + old `sparkshark.com/archives/*`. Not editorial. |
| **`debt-reduction-solution.com`** | 1 | ~353 | Credit-repair PBN linking the pre-Flanco `sparkshark.com/archives/2008–2011/*` "credit repair" blog content. Spam-flagged. |
| **`mu.nu`** | 1 | 1 | Old blog-farm; spam-flagged; first seen 2020. |
| **SEO-PBN spam surge** | ~75 | ~150 | `.shop` / `.top` / `.click` / `.agency` / `.info` / `.online` / `.website` / `.space` / `.site` / `.store` TLDs; `seoexpress.*`, `rankvance*`, `*backlink*`, `*seolink*` patterns. Anchors like "before finding seoexpress.com I spent too much on…". Almost all first-seen Sept 2025 → May 2026 — this is the dashboard's "+51 referring domains in 30 days." |
| **Plausibly-real, Ahrefs-only** | ~5 | ~6 | `themusemark.com` ("common electrical emergencies and how to respond" — looks editorial), `anationofmoms.com`, `yplocal.us` (directory listing), `hypnosistacticsguide.com` (DR1, 2023), + a couple already in the master via other sources. **Tier P2 — open each, confirm the on-page link before treating as a real backlink.** |
| **Already in master** | 4 | — | `bbb.org`, `agreatertown.com`, `moranalytics.com`, `best-electrician-moore.com` — `source_set` updated to include `awt`. |

**Domain history confirmed via Wayback CDX (incidental finding):** `sparkshark.com` was an **online-poker / casino-affiliate spam site ~2006** (`/10-Best-Online-Casinos.html`, Texas-Holdem pages), then a **credit-repair affiliate blog ~2008–2011** (`/archives/.../credit-repair-myths-exposed/` etc.), before becoming Flanco Electric and then Spark Shark Electric. This is the root of the `rss2.com` + `debt-reduction-solution.com` link mass and is worth knowing for the post-launch disavow decision and for any "why does this domain have weird old indexed pages" question.

---

## 2. Top link-equity assets (Brock-owned / high-trust)

1. **BBB Moore profile** — `bbb.org/us/ok/moore/profile/electrical-contractors/spark-shark-electric-0995-90130075` (P1). DR 93 root. Plus a duplicate OKC `addressId/134759` profile that needs reconciling (one business, two addresses). Ahrefs confirms 2 live backlinks here.
2. **Yelp** — `yelp.com/biz/spark-shark-electric-moore` (P1). 621 Sally Ct Moore matches Brock's NAP. Claim if not already.
3. **Thumbtack** — `thumbtack.com/ok/oklahoma-city/electrical-repairs/spark-shark-electric/service/489603470823817221` (P1). Lead-gen platform; claim. (Wayback-archived Jul–Oct 2025.)
4. **Facebook Business page** — `facebook.com/sparksharkelectric/` (P1). Confirmed Brock-owned.
5. **Instagram** — `instagram.com/thesparkshark/` (P1). Confirmed Brock-owned. **Not** `@sparksharkelectric` (= the Ontario business).

Honorable mentions: Chamber of Commerce, MapQuest, Pinterest, X/Twitter, TikTok (`@sparkshark.com`), ProvenExpert, theorg, Featured.com (Brock profile), agreatertown, LinkedIn (personal).

---

## 3. Top risks (must fix before DNS flip)

1. **`networx.com/c.flanco-electric` (P0).** Last seen 2025-11-09 (GSC); Wayback-archived 2025-01-18. Active Flanco-era citation under the prior brand. Conflicts with the Spark Shark public NAP. **Request takedown or rebrand.**
2. **BBB duplicate addresses (P1).** Same business profiled at `/moore/...` and `/oklahoma-city/...addressId/134759`. Reconcile to one canonical address before launch.
3. **Apex profile validation gap (P1).** ~9 of the 21 Brock-owned profiles carry presumed-correct-but-unverified NAP (Mapquest, Chamber, Pinterest, ProvenExpert, Twitter/X, TikTok, theorg, agreatertown, Featured). Open each, screenshot, fix in place.

Not a cutover blocker but worth queuing: **the 82 spam/PBN/legacy-scraper domains → Google Disavow file** (Search Console → Disavow links tool, against `sc-domain:sparkshark.com`). The DISAVOW-tier rows in the CSV are the source list.

---

## 4. Action list

### P0 — Before DNS flip (1)
- [ ] Request `networx.com/c.flanco-electric` takedown or rebrand to a Spark Shark URL.

### P1 — Before DNS flip (8)
- [ ] Reconcile two BBB profiles into one canonical address.
- [ ] Verify NAP on `chamberofcommerce.com/.../spark-shark-electric`.
- [ ] Verify NAP on `mapquest.com/us/oklahoma/spark-shark-electric-778761940`.
- [ ] Claim/verify Yelp at `yelp.com/biz/spark-shark-electric-moore`.
- [ ] Claim/verify Thumbtack at the long Spark Shark URL.
- [ ] Verify Facebook page bio links + featured info (owned).
- [ ] Verify Instagram bio at `@thesparkshark` (owned).

### P2 — Post-launch cleanup (24)
- [ ] Verify ownership + bio on Pinterest, ProvenExpert, theorg, agreatertown, Featured, TikTok.
- [ ] Verify Twitter/X profile (treat `twitter.com` + `x.com` as one — `@The_Spark_Shark`).
- [ ] Audit `uscity.net/listing/...` — HTTP-only, request HTTPS upgrade.
- [ ] Audit `best-electrician-moore.com` listicles for accurate Spark Shark mention.
- [ ] Audit `smartelectricalservices.net/business/spark-shark-electric-ok-91055/`.
- [ ] Verify/claim `callupcontact.com/.../Spark_Shark_Electric/9878135` (ownership unknown).
- [ ] Update LinkedIn personal `linkedin.com/in/brock-flanary/` with current Spark Shark CEO title (never "owner").
- [ ] Confirm Glassdoor job listing reflects current hiring state.
- [ ] **NEW — Ahrefs "verify the mention" candidates:** open `themusemark.com` ("common electrical emergencies…"), `anationofmoms.com`, `yplocal.us`, `hypnosistacticsguide.com`; confirm whether a real on-page `<a href>` to sparkshark.com exists. Promote tier / ownership accordingly.
- [ ] Verify GA4 "candidate backlink" mentions: chatgpt.com, claude.ai, moranalytics.com, hometalk.com, marketspacesales.com.

### P3 — Monitor only (23)
- [ ] No action on yellowpages.com / superpages.com / dexknows.com category pages (co-citation noise).
- [ ] No action on Medium / Reddit / Facebook-group single-mention links.
- [ ] No action on `*.lightning.force.com` partner-CRM referrers, `siteliner.com`, `coalitiontechnologies.com`, `wpengine.com` staging — referrers, not public backlinks.
- [ ] Watch `rss2.com` — feed republisher; harmless but noisy. (Also a disavow candidate — see DISAVOW.)

### DISAVOW — Post-launch (82)
- [ ] Build a Google Disavow file from the `risk_tier=DISAVOW` rows in `master-backlinks-cumulative.csv` and submit it for `sc-domain:sparkshark.com`. Includes: ~75 SEO-PBN spam domains (`.shop`/`.top`/`.click`/`.agency`/`seoexpress.*`/`rankvance*`/etc.), `rss2.com`, `debt-reduction-solution.com`, `mu.nu`. Re-pull Ahrefs AWT every ~30–60 days during the cutover window and re-run this filter — the spam surge looked active as of May 2026.

### IGNORE — Filter from future scrapes (7)
Other Spark Shark businesses (Canada / Wisconsin / California).

---

## 5. Blocked / remaining work

### A. Ahrefs AWT scrape — ✅ DONE 2026-05-12
Scraped via Playwright MCP (`@playwright/mcp`, own persistent Chromium profile, Brock logged in once) against Ahrefs' `/v4/seBacklinks` + `/v4/seRefdomains` endpoints. Free-tier caps: result offset must stay <1000 per report (so 1,000 of 1,080 backlinks captured by combining traffic-DESC and traffic-ASC pages); referring-domains report has no such issue (all 90 captured). No paid API used. **Re-run procedure:** restart Claude Code in `/Users/brock/Projects/sparkshark-com`, ensure the `playwright` MCP is approved (the `.mcp.json` registering it was removed to `.mcp.json.removed-2026-05-11` — restore it or re-add `npx -y @playwright/mcp@latest`), navigate to `ahrefs.com` once to confirm the persisted login, then re-issue: dashboard → project 9816270 → it's all driven through the JSON API in `browser_evaluate` (see the merge/scrape scripts in `/tmp/` if still present, or just replay the input shapes documented in this session's transcript).

### B. GA4 service-account access — ✅ RESOLVED 2026-05-11
SA `sparkshark-seo-reader@…` has Viewer on all 3 of Brock's GA4 properties (added via `v1alpha accessBindings.create` after the UI grant hit a Workspace validation bug). Live `G-QK02QH3SWY` confirmed to live in Brock-owned property 488680346 (under the Flanco Electric GA4 account, not Spark Shark Analytics). See `docs/migration/SOURCE-OF-TRUTH.md` §11.

### C. WP Engine API token rotation — NOT DONE (blocks access-log retrieval)
1Password item `wp_engine` (vault SparkShark) — token + Customer Portal password both leaked 2026-05-11; not yet rotated. Fix: `my.wpengine.com` → API Access → revoke + regenerate → update `wp_engine` fields `API_Token` (CONCEALED) + `API Username`. Then `GET /v1/installs/{id}/logs` for last-90-days server-side referrers. **This is the last source between "cumulative" and "final."**

### D. AWS Athena Common Crawl — deferred per Brock (~$5–15 query).

---

## 6. Files in this directory (artifact map)

```
master-backlinks-cumulative.csv         # 145 rows / 129 unique referring domains. Canonical. NOT "final" (WPE logs pending).
master-backlinks-working.csv            # Mutable working log; rows appended as discovered (pre-Ahrefs state).
ahrefs-awt-backlinks-raw.json           # Ahrefs /v4/seBacklinks dump — 1,000 of 1,080 URL-level rows, 29 cols, JSON.
ahrefs-awt-refdomains-raw.json          # Ahrefs /v4/seRefdomains dump — all 90 referring domains, 13 cols, JSON.
ahrefs-awt-backlinks-scrape.csv         # CSV form of the above backlinks dump.
ahrefs-awt-referring-domains-scrape.csv # CSV form of the above refdomains dump.
ga4-referrals-property-488680346-all-history.csv   # 229 GA4 referral rows (live property), since 2025-05-09.
ga4-referrals-property-480290314-flanco-legacy.csv # 153 GA4 referral rows (Flanco-legacy property).
BACKLINK-SUMMARY.md                     # This document.
BACKLINK_RISK_FINDINGS.md               # May 10 GSC classification (source-of-truth for the original P0–P3 tiers).
gsc-link-summary-by-domain.csv          # Per-domain rollup with risk tier + recommended action.
gsc-external-links-all-deduped.csv      # Session 1 GSC export (28 URLs / 17 domains).
gsc-links-external-*.csv                # Raw GSC exports (audit trail).
gsc-links-internal-*.csv                # Internal-link exports (out of scope for backlink audit).
SESSION-2-HANDOFF.md                    # Session 1→2 handoff (kept for trace).
```

Scripts (not committed; live in `/tmp/`): `merge_awt.py` (Ahrefs → master merge + classification + collision filter), `wayback_enrich.py` (CDX enrichment), plus the GA4 + dedup helpers from prior sessions.

---

## 7. Confidence statement (updated 2026-05-12)

This list is **cumulative across the sources reached so far** — GSC, Bing index, open-web search, both relevant GA4 properties, **Ahrefs Webmaster Tools (full)**, and a Wayback CDX enrichment pass. It is **still NOT final**: the one remaining unreached source is **WP Engine server access logs** (blocked on API-token rotation), which would add real inbound-traffic referrer data. Common Crawl/Athena is deliberately deferred.

**Evidence quality by row:**
- The ~39 GSC + WebSearch rows are **verified backlinks** (external page known to contain an `<a href>` to sparkshark.com).
- The ~13 GA4-derived rows are **candidate backlinks** (non-empty Referer header; on-page link not yet confirmed for most). The two LLM referrals (chatgpt.com, claude.ai) are very likely real; the `*.lightning.force.com` rows are partner-CRM referrers, not public backlinks.
- The Ahrefs rows: the **82 DISAVOW-tier** are real links that *exist* but are spam/PBN/scraper junk (Ahrefs spam-flags them; we'd disavow them). The **4 "already in master"** strengthen existing rows. The **~4 P2 candidates** need on-page verification before counting.
- The 7 collision-filter / IGNORE rows are confirmed NOT-Brock's businesses.

**Floor / ceiling:** the *useful* editorial-and-citation backlink count is small — call it ~25–35 once the category-page / CRM-referrer / unverified noise is stripped out — and it is **unlikely to grow much**: Ahrefs (the deepest single source available for free) added essentially nothing real, and GSC's link graph is already captured. WP Engine logs may surface a handful more referrers. The bigger takeaway is the **82-domain spam tail** and the **domain's pre-Flanco history** — both post-launch cleanup items, neither a cutover blocker. "Final" naming will be applied only once the WPE-log stream is landed or Brock closes it out.

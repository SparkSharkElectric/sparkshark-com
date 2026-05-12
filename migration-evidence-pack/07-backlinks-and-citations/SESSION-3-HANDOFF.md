# Backlink Capture — Session 3 → 4 Handoff

> **SUPERSEDED 2026-05-12 — see `SESSION-4-HANDOFF.md`.** Session 4 executed the WPE access-log pull described below: the WPE source turned out to be exhausted (no 90-day archive — see `wpe-access-log-snapshot-2026-05-12.md`), it added nothing material, and `master-backlinks-cumulative.csv` was renamed → `master-backlinks-final.csv`. The workstream is **complete**. This file is kept for trace; the references to `master-backlinks-cumulative.csv` below are historical (it's now `master-backlinks-final.csv`).

**Written:** 2026-05-12. **Repo head at handoff:** `ae30f24` on `origin/main` (+ this handoff commit on top). Working tree is clean for this workstream — the only untracked files (`audits/`, `docs/migration/*-findings.md`, etc.) belong to other workstreams, not this one.

**Read order before acting:**
1. This file.
2. `BACKLINK-SUMMARY.md` — current state of everything (it's the live doc; §5.C is the WPE plan, §4 has the action lists).
3. `master-backlinks-cumulative.csv` — 145 rows / 129 unique referring domains, canonical.
4. Cross-doc: `../../docs/migration/SOURCE-OF-TRUTH.md` (still the canonical migration doc) — esp. §11 (analytics ownership) if anything analytics-adjacent comes up.

---

## 1) What Session 3 did (done, do not redo)

| # | Task | Result |
|---|---|---|
| 1 | **Ahrefs Webmaster Tools scrape** | Done via Playwright MCP against Ahrefs' `/v4/seBacklinks` + `/v4/seRefdomains` JSON endpoints (free-tier UI data; no paid API). Verified project `9816270` = `*.sparkshark.com/*` (subdomains, both protocols) — the superset of the `www` project. **All 1,080 URL-level backlinks + all 90 referring domains captured.** Raw: `ahrefs-awt-backlinks-raw.json`, `ahrefs-awt-refdomains-raw.json`. CSVs: `ahrefs-awt-backlinks-scrape.csv` (1,000 rows × 29 cols — the first pull; the extra 80 reachable via date-sorted pages are all from the same scraper/PBN domains and weren't separately re-exported), `ahrefs-awt-referring-domains-scrape.csv` (90 × 13). |
| 2 | **Merge into master** | 145 rows / 129 unique referring domains. 86 new domain rows; 4 existing (`bbb.org`, `agreatertown.com`, `moranalytics.com`, `best-electrician-moore.com`) got `+awt` appended to `source_set`. URL-normalized, brand-collision-filtered. Tier mix: P0 1 / P1 8 / P2 20 / P3 26 / IGNORE 7 / **DISAVOW 83**. |
| 3 | **Wayback CDX enrichment** | archive.org healthy this session; ran exact-URL CDX (`statuscode:200`) on all 143 distinct referring URLs. Only 2 archived (`networx.com/c.flanco-electric` 1 snap; Thumbtack listing 2 snaps). `wayback_*` columns populated; `=0` where confirmed absent. |
| 4 | **Disavow file** | `disavow-sparkshark.com.txt` — 83 `domain:` entries (79 SEO-PBN spam + 4 legacy/pre-Flanco junk: `rss2.com`, `debt-reduction-solution.com`, `mu.nu`, `hypnosistacticsguide.com`). Ready to upload at GSC → Disavow links tool for `sc-domain:sparkshark.com`. **Post-launch task — Brock uploads it; not done yet.** |
| 5 | **Verified the 4 Ahrefs "verify the mention" candidates** | On-page DOM check 2026-05-12: `anationofmoms.com` (DR55) + `themusemark.com` (DR49) = real dofollow links `"emergency electrician(al services)"` → `/services/emergency-electrician/` in long articles (guest-post pattern) → reclassified P2→P3 (monitor). `yplocal.us` (DR19) = dofollow YpLocal directory listing, NAP correct → P3. `hypnosistacticsguide.com` (DR1) = nofollow link to a dead pre-Flanco `/archives/2010/...` URL → reclassified P2→DISAVOW (now in the disavow file). |
| 6 | **`.mcp.json` restored** | The `playwright` MCP (`npx -y @playwright/mcp@latest`) is now committed in repo `.mcp.json`. The `.mcp.json.removed-2026-05-11` marker was deleted. |
| — | **WPE creds rotated** | 2026-05-12: WP Engine Customer Portal password + Public API token + username rotated; 1Password item `wp_engine` (vault SparkShark) updated. **This unblocks the access-log pull** — the last remaining backlink source. |

Commits: `40a324e` (AWT scrape + Wayback), `75ca42b` (restored `.mcp.json`), `ae30f24` (disavow file + candidate verification), + this handoff.

---

## 2) What Session 4 should do — PRIMARY: WP Engine access logs

This is **the one remaining source** between "cumulative" and "final" on the backlink list. The blocker (token rotation) is cleared.

**Inputs:**
- 1Password item `wp_engine` (vault SparkShark) — the **rotated** API token + API username/UUID. ⚠️ Type-based redaction only (CONCEALED + SSHKEY = redact; STRING/MENU/DATE = OK). A block-list filter leaked these in session 1 — don't repeat that.
- 1Password item `WP Engine SSH Key — flancoelectric (Spark Shark)` (`7baqqyeiyungknahpf44ah455m`) — SSH key + host + user; install name "flancoelectric". Fallback path if the API doesn't expose logs.
- The WP install ID — get it from `GET https://api.wpengineapi.com/v1/installs` (Basic auth: API username:token).

**Steps:**
1. **Confirm the log-retrieval mechanism.** The session-2 plan assumed `GET /v1/installs/{id}/logs` — verify that endpoint actually exists in the WP Engine Public API (`https://api.wpengineapi.com/v1/swagger`). If it doesn't (likely — WPE access logs are usually retrieved from the User Portal or via SSH), fall back to: **SSH to the install** (`ssh {user}@{host}` using the 1P SSH key) → access logs live under `~/sites/{install}/logs/` or `~/logs/` as `apache.access.log*` / nginx-style logs (gzipped, rotated). Or, last resort, Brock downloads them from `my.wpengine.com` → install → **Access Logs** and drops the file here.
2. **Pull last ~90 days** of access-log lines.
3. **Extract the `Referer` header field** from each line; drop self-referrals (`sparkshark.com`, `www.sparkshark.com`), drop empty/`-` referrers, drop obvious internal/CDN/monitoring referrers.
4. **Normalize** the referring URLs (strip `utm_*`/`fbclid`/`gclid`; collapse `www`/scheme; trailing-slash; lowercase host) — same function as in `/tmp/merge_awt.py` if it's still around, else re-implement (it's ~15 lines).
5. **Run the filters:** brand-collision (Ontario / Wisconsin / Elk Grove / Sacramento "Spark Sharks" — see SESSION-2-HANDOFF §3) + the spam/PBN classification (the `.shop`/`.top`/`.click`/`.agency`/`seoexpress.*`/`rankvance*` patterns from `/tmp/merge_awt.py`).
6. **Merge into `master-backlinks-cumulative.csv`** tagging `source_set=wpe-logs` (or append `+wpe-logs` to existing rows). For genuinely-new non-spam domains, classify P2/P3 with a "verify the mention" note. For new spam → DISAVOW (and regenerate `disavow-sparkshark.com.txt`).
7. **Refresh `BACKLINK-SUMMARY.md`** §1 topline + §1.x breakdown + §5.C + §7.
8. **If nothing else is outstanding** (WPE done, Athena deliberately deferred per Brock, Bing still empty), **rename `master-backlinks-cumulative.csv` → `master-backlinks-final.csv`** and update all references in the summary + this handoff. If you do rename, also update `docs/migration/SOURCE-OF-TRUTH.md` if it references the cumulative file.
9. **Report back for commit approval** — do NOT auto-commit/push in `sparkshark-com` unless Brock says so for this session (a push = a Vercel deploy; evidence-pack files don't change the built HTML, but the rule still stands).

**Reality-check expectation:** access logs may surface a *handful* more referrers (real social/forum/email clicks, more spam-bot referrers). Don't expect a big haul — Ahrefs (the deepest free source) added essentially nothing real, and GSC's link graph is captured. The useful editorial-and-citation backlink count is small (~25–35 after stripping noise) and that's not going to change much. If WPE logs add nothing material, that's a fine outcome — it just lets us stamp "final."

---

## 3) Carried-forward / post-launch items (not Session-4 critical, but track them)

- **[Brock] Upload `disavow-sparkshark.com.txt`** at Search Console → Disavow links tool → property `sc-domain:sparkshark.com`. Post-launch. Re-pull Ahrefs every ~30–60 days during the cutover window, regenerate, re-upload — the spam surge looked active as of May 2026.
- **[Brock] Verify GA4 "candidate backlink" mentions** that still need on-page confirmation: `chatgpt.com`, `claude.ai`, `hometalk.com`, `marketspacesales.com` (open each, search the rendered DOM/source for `sparkshark.com`).
- **P0/P1 pre-flip items** (unchanged from BACKLINK-SUMMARY §4): `networx.com/c.flanco-electric` takedown/rebrand; reconcile the two BBB profiles; verify NAP on Chamber/MapQuest; claim Yelp + Thumbtack; verify FB/IG bios.
- **Separate security follow-up bucket** (not WordPress): re-rotate the Cloudflare token (transcript-leak follow-up per `~/.claude/projects/-Users-brock/memory/project_security_followups.md`), rotate Voyage + Supabase `service_role`, delete `.zsh_history.pre-scrub` backup. Not part of this workstream — just noting it lives in the same "leaked-in-transcript" bucket.

---

## 4) Key facts that don't change (don't re-litigate)

- **Domain history:** `sparkshark.com` was an online-poker/casino-affiliate site ~2006, then a credit-repair affiliate blog ~2008–2011 (`/archives/...`), before Flanco Electric → Spark Shark Electric. This is the source of the `rss2.com` + `debt-reduction-solution.com` link mass. Confirmed via Wayback CDX.
- **Brand collisions:** other "Spark Shark" businesses exist in Barrie ON / Cambridge ON / Pewaukee WI / Elk Grove CA / Sacramento CA. Brock's confirmed handles: FB `facebook.com/sparksharkelectric`, IG `instagram.com/thesparkshark` (NOT `@sparksharkelectric` = Ontario), X `@The_Spark_Shark`, TikTok `@sparkshark.com`, Pinterest `sparksharkelectric`, LinkedIn `linkedin.com/in/brock-flanary`.
- **Bing's index is empty** for sparkshark.com (re-probed 2026-05-11). GSC API doesn't expose the Links report (UI-only export — already captured in the May 10 audit).
- **GA4:** live `G-QK02QH3SWY` is in Brock-owned property `488680346` (under the Flanco Electric GA4 account, not Spark Shark Analytics). SA `sparkshark-seo-reader@…` has Viewer on all 3 of Brock's GA4 properties.
- **Ahrefs re-run:** the `playwright` MCP is in repo `.mcp.json` now. To re-pull: `/mcp` to confirm it's approved → `app.ahrefs.com/dashboard` (persisted login) → drive via `browser_evaluate` against `/v4/seBacklinks` (aggregations: `GroupSimilarLinks` / `OneLinkPerDomain` / `AllLinks`; free-tier offset cap <1000 per report, work around with multiple sort directions) and `/v4/seRefdomains` (POST: `{se_params, params, best_links_filter, backlinks_params}`).
- **Commit/push policy in `sparkshark-com`:** push = Vercel deploy. Evidence-pack files don't change built HTML, but still get Brock's OK before pushing. DNS is not flipped — nothing goes live.

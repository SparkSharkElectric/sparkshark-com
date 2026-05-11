# sparkshark.com WP Redirect Audit — Findings

**Status:** Interim (autonomous-pass complete, intervention-batch pending)
**Audit date:** 2026-05-10
**Auditor:** Claude (per Brock — auto mode)
**Scope:** Read-only discovery. No edits to live WP, DNS, plugins, or vercel.json.
**Local-only:** This file inherits `migration-evidence-pack/.gitignore: *`. Do not commit.

---

## Executive Summary (read this first)

1. **Live WP is actively running Redirection plugin AND SEOPress redirections** — two redirect managers concurrently. Both have `_wp_old_slug` (WordPress core) handling 301s on top. Three independent surfaces could conflict.
2. **All 6 `flanco-electric`-slug URLs from Deep Research brief §3 currently 301 correctly** to their spark-shark-slug equivalents (via WP core's `_wp_old_slug` mechanism). **They are NOT in `vercel.json`'s 14 redirects yet.** On DNS cutover, all 6 will 404. Migration-critical.
3. **In-content Flanco residue is minimal** — 0 of 20 posts contain "flanco" in body content. 3 pages match a "flanco" search, but only **page 14118 (`indoor-lighting-installation`)** has a visible body-content link to a flanco-slug URL. Pages 3483 (`blogs`) and 3195 (`electrical-repair-and-service`) match via SEO-plugin meta only (not visible to readers). The rebrand-in-place cleanup is cleaner than expected on the surface; deeper residue (post_meta, taxonomy, options) is auth-gated.
4. **Live WP serves URLs case-insensitively** (`/About-Us/`, `/SERVICES/` both 200). Vercel will be case-sensitive — any uppercase bookmarks 404 post-cutover. Low risk (rare) but documented.
5. **Apex→www 301 returns `http://` in the Location header**, not `https://`. HSTS hides this from browsers; bots/crawlers degrade to HTTP first. WP Engine edge–level behavior, not WordPress. Will be auto-fixed by Vercel post-cutover. Current-state observation only.
6. **No catch-all 404 auto-redirect handler** — unknown URLs cleanly 404. Good baseline; matches GSC "Pages with redirect = 0" finding.
7. **Cloudflare is fronting sparkshark.com** but it's **WP Engine's bundled CDN edge** (WPEngine owns the 141.193.213.x IP range), NOT a separately-managed Cloudflare account. No Cloudflare console to audit; redirect rules — if any — live in the WP Engine User Portal, not Cloudflare. Memory note updated.

**Cutover-blocking gaps surfaced so far (autonomous pass):**

- **6 flanco-electric-slug URLs** must be added to `vercel.json` (1:1 mappings to their spark-shark-slug equivalents) — see "URL Parity" section below
- **Redirection plugin rule list** must be exported and ported to `vercel.json` (currently auth-gated; in intervention batch)
- **SEOPress redirections list** must be exported and merged (also auth-gated)

---

## Phase 1 — Live HTTP smoke test + sitemap sweep (autonomous, complete)

**Sweep stats** (71 URLs total — 21 root/probe variants + 50 sitemap URLs):
- 68 × HTTP 200 final
- 23 × HTTP 301 (apex→www, HTTP→HTTPS, vercel.json-aligned content redirects, _wp_old_slug)
- 4 × HTTP 404 (deliberate 404 probes + `/index.html`)
- **0 × HTTP 302/303/307/308** — clean. No SEO-leaking temporary redirects.

**Root-variant behavior:**

| URL | Hops | Final | Notes |
|---|---|---|---|
| `http://sparkshark.com` | 2 | 200 | http→https→www |
| `https://sparkshark.com/` | 1 | 200 | apex→www |
| `http://www.sparkshark.com` | 1 | 200 | http→https |
| `https://www.sparkshark.com` | 0 | 200 | canonical |

**Schema-downgrade quirk:** The apex→www 301 sends `Location: http://www.sparkshark.com/<path>` (not `https://`). HSTS preload handles real browsers; bots may follow to HTTP first. WP Engine edge–layer behavior. Vercel will replace this.

**Case behavior:** `/About-Us/` and `/SERVICES/` return 200 (case-insensitive). `/index.html` returns 404. `/index.php` returns 301 → homepage (2 hops).

**vercel.json mirror check** — both `/industrial-electrical-solutions/` and `/commercial-electrical-solutions/` 301 to `/` on the live WP, **matching the existing `vercel.json` entries**. Good — those two entries are validated against live behavior.

**Raw chain log:** `auto-run-2026-05-10/raw-tests-2026-05-10.txt` (~2151 lines)

---

## Phase 2 — DNS layer (autonomous, complete)

| Record | Value |
|---|---|
| NS | `ns77.domaincontrol.com.`, `ns78.domaincontrol.com.` (GoDaddy) |
| A (apex) | `141.193.213.10`, `141.193.213.11` (WPEngine owns this range; Cloudflare-edge serves) |
| AAAA | (none — no IPv6) |
| CNAME apex | (none) |
| CNAME www | `sparkshark.com.` |
| A (www, after CNAME flatten) | `141.193.213.10`, `141.193.213.11` |
| MX | Google Workspace (5×ASPMX.L.GOOGLE.COM + alts) |
| Registrar | GoDaddy.com, LLC |
| Status | ACTIVE, locked: clientDelete/Renew/Transfer/UpdateProhibited |
| Expiry | 2026-12-07 |

**Findings:**
- No DNS-level forwarding (A records hit WPE edge directly)
- No Cloudflare apex parking (the Cloudflare server header is WP Engine's bundled edge, not a separately-configured Cloudflare account)
- GoDaddy Forwarding-tab content is **unverified** — still on intervention batch (one screenshot)
- Domain locked at registrar (good — accidental transfer/renew blocked)

---

## Phase 3 — WP REST API discovery (autonomous, unauthenticated; auth-gated portions deferred)

**Live site identity:**
- Name: `Professional Electrician | Moore & Oklahoma City, OK | Spark Shark Electric`
- Home / URL: `https://www.sparkshark.com`

**Plugin/feature namespaces detected via `/wp-json/`:**

| Namespace | Plugin/feature | Redirect-capable? |
|---|---|---|
| `redirection/v1` | **Redirection plugin (john-godley)** | **YES — primary redirect surface** |
| `seopress/v1` | **SEOPress (SEO plugin)** | **YES — `/seopress/v1/redirections`** |
| `aios/v1/onboarding` | All in One SEO (AIOSEO) | Partial — only onboarding namespace visible. Likely installed but not fully configured. |
| `elementor/v1`, `elementor-ai/v1`, `elementor-one/v1` | Elementor page builder | No |
| `elementskit/v1/*` (megamenu, widget-builder, ajaxselect2, etc) | ElementsKit (Elementor add-on) | No |
| `jetpack/v4`, `jetpack-boost/v1`, `my-jetpack/v1`, `jetpack-boost-ds` | Jetpack + Jetpack Boost | No (cache/perf) |
| `google-site-kit/v1` | Google Site Kit | No |
| `bsf-custom-fonts/v1`, `custom-fonts/v1` | Brainstorm Force / Spectra family | No |
| `wpe/cache-plugin/v1` | WP Engine Page Cache | No (cache only) |
| `wpe_sign_on_plugin/v1` | WP Engine Sign On | No |
| `wsrw/v1` | WP Smart Resize Watermark (image upload) | No |
| `wp-block-editor/v1`, `wp-site-health/v1`, `wp-abilities/v1`, `wp/v2`, `oembed/1.0` | WP core | core canonical redirects only |
| `lc_internal_api/v1`, `lc_public_api/v1` | Unknown (LiteSpeed? LearnPress?) | Unknown — flag for screenshot review |

**Custom post types** — only standard WP + Elementor types. **No `srm_redirect`, no `wpcode`, no `code_snippets`** — Safe Redirect Manager, WPCode, and Code Snippets are **NOT installed**. Confirmed via `/wp/v2/types`.

**Endpoint auth probe** (unauthenticated):

| Endpoint | Status | Meaning |
|---|---|---|
| `/wp-json/redirection/v1/redirect` | **401** | Active, returns rules with admin auth |
| `/wp-json/redirection/v1/log` | 401 | Active, hit log with admin auth |
| `/wp-json/redirection/v1/404` | 401 | Active, 404 log with admin auth |
| `/wp-json/redirection/v1/export/all/csv` | 401 | Bulk export available with admin auth |
| `/wp-json/seopress/v1/redirections` | 401 | SEOPress redirections — also auth-gated |
| `/wp-json/aios/v1/onboarding` | 200 | Public onboarding endpoint (no rules surface) |

**Conclusion:** Two active WP redirect managers — Redirection AND SEOPress — both have rule lists behind admin auth. Manual screenshot/export needed (intervention batch). Possibility of duplicate-source conflict between the two.

---

## Phase 7c — In-content Flanco footprint (autonomous, unauthenticated scope)

**Posts (20 most recent, all spark-shark-slug):** **0 in-content Flanco mentions**. The rebrand-in-place cleaned post bodies.

**Pages (search "flanco" across all):** 3 hits:

| Page ID | Slug | Visible body mentions | Notes |
|---|---|---|---|
| 14118 | `indoor-lighting-installation` | **1** | A body-content `<a href>` link to `/2024/01/02/...-with-flanco-electric/` — internal link still pointing at a flanco-slug URL. Currently 301s via `_wp_old_slug` to the spark-shark-slug equivalent. After Vercel cutover, this internal link 404s unless flanco-slug URLs are in vercel.json. |
| 3483 | `blogs` | 0 | Matched via SEO-plugin meta only (SEOPress yoast title/description, etc.) — invisible to readers. Auth-gated deeper inspection. |
| 3195 | `electrical-repair-and-service` | 0 | Same — SEO-plugin meta match. |

**Deeper Flanco footprint (auth-gated, deferred):**
- `_wp_old_slug` post-meta entries (proves which flanco-slug URLs are live-resolving and gives a comprehensive list)
- SEOPress `_seopress_*` post-meta with flanco keywords
- `wp_options` for `blogname`, `blogdescription`, `wp_mail_from_name`, SEO plugin overrides
- Taxonomy term names/slugs containing flanco
- User display names / nicknames

These all require admin auth or SSH/WP-CLI. Deferred to intervention batch.

---

## Phase 7b — Citation directory probes (autonomous, where unblocked)

| Directory | HTTP status | Notes |
|---|---|---|
| Yelp (Flanco search) | 403 | Bot-blocked. Manual review needed. |
| Yelp (Spark Shark search) | 403 | Bot-blocked. Manual review needed. |
| BBB | 200 | Accessible — deeper content-level NAP probe possible. |
| Thumbtack | 200 (1 hop) | Accessible. |
| Networx | 403 | Bot-blocked. Manual review needed. |
| Angi | 403 | Bot-blocked. Manual review needed. |
| HomeAdvisor | 403 | Bot-blocked. Manual review needed. |
| Bing | 200 | Accessible. |
| ProvenExpert | 200 (1 hop) | Accessible. |
| Google search results | 200 | Accessible. |

**Conclusion:** 4 major directories (Yelp, Networx, Angi, HomeAdvisor) actively block crawler User-Agents. Brock manual NAP-residue review needed on each. The others can be content-probed in a follow-up pass if Brock confirms scope.

**SERP screenshots** (`flanco-search-screenshots/`) for `Flanco Electric`, `Flanco Electric Oklahoma City`, `Flanco Electric Moore OK` — still pending (intervention batch).

---

## URL Parity: Live WP sitemap vs `vercel.json` 14 redirects vs static replacement

**Live WP sitemap:** 50 URLs across `post-sitemap1.xml` (10 posts) + `page-sitemap1.xml` (40 pages — includes `locations-we-serve/*` subpages).

**Static replacement in `~/Projects/sparkshark-com/`:** Per repo directory list — homepage, ~15 service pages, ~9 city/location pages, blog posts, footer pages.

**Cutover-critical gaps (URLs that 200 on live WP but lack a 1:1 in static OR a `vercel.json` redirect):**

| Live URL | Currently | Static replacement? | `vercel.json` entry? | Action |
|---|---|---|---|---|
| `/2023/12/29/.../-with-flanco-electric/` (6 URLs) | 1-hop 301 → spark-shark slug via `_wp_old_slug` | No | **No** | **Add 6 explicit 301s to vercel.json** (1:1 to spark-shark slug). Migration-critical. |
| `/2023/12/29/.../-with-spark-shark/` (post-sitemap) | 200 | Probably yes (in repo) | Already in `vercel.json` | Verify static page matches. |
| `/locations-we-serve/<city>/` × 9 cities | 200 | Yes (each city has `locations-we-serve/<city>/index.html`) | None needed | Verify city pages render. |
| `/?p=<id>` (default WP perma) | 301 → permalink | No | None needed | WP-core handler; Vercel won't replicate. Low-risk — direct `?p=ID` URLs are rare in 2026 backlinks. |
| Uppercase URLs (`/About-Us/`) | 200 (WP case-insens) | 404 on Vercel (case-sens) | None | **Decision needed**: case-fold redirect in vercel.json, or accept 404 for uppercase bookmarks. Low traffic. |

**Static-only URLs** (in `~/Projects/sparkshark-com/` but not on live WP) — separate listing pending; needs a static-side inventory pass.

---

## Intervention Batch — items needed from Brock (Phase 9)

Brock returns these in ONE batch. After receipt, Phase 8b runs and closes the audit.

### 9a. Credential permission grant (blocking)

The plan's `allowedPrompts` listed "use 1Password CLI (op read) to fetch SparkShark vault credentials and SSH keys" — but Bash invocations of `op item get` against the WPE SSH key item AND the `wp_admin_app_password` item were both **denied at the permission layer** with reason "credential exploration beyond the audit's read-only HTTP/REST scope."

**Two paths:**
- **(A)** Brock approves `op item get` for vault SparkShark in this session (the audit is fully read-only — no edits, no plugin changes, no DB mutations). With this, Phases 4 (SSH/WP-CLI/DB), 7c-deep (auth-gated WP REST), and Redirection/SEOPress rule-list pulls all run autonomously and the audit closes today.
- **(B)** Brock manually exports/screenshots everything below.

### 9b. WP Admin browser screenshots (if path B)

| # | Location | Filename target |
|---|---|---|
| 1 | wp-admin → Plugins → Installed Plugins (filter: All) | `01-wp-admin-plugins-list-all-2026-05-10.png` |
| 2 | wp-admin → Plugins → Installed Plugins (filter: Active) | `02-wp-admin-plugins-list-active-2026-05-10.png` |
| 3 | wp-admin → Tools → Redirection → Redirects tab — list view | `redirection-redirects-list-2026-05-10.png` |
| 4 | Redirection → Import/Export → run **CSV export**, download | `redirection-export.csv` |
| 5 | Redirection → Import/Export → run **Apache export** | `redirection-export-apache.conf` |
| 6 | Redirection → Logs tab | `redirection-logs-2026-05-10.png` |
| 7 | Redirection → 404s tab | `redirection-404s-2026-05-10.png` |
| 8 | SEOPress → Pro → Redirections (if Pro) — list + export | `seopress-redirections-2026-05-10.png`, `seopress-export.csv` |
| 9 | SEOPress → SEO → Sitemaps (confirm naming pattern source) | `seopress-sitemaps-2026-05-10.png` |
| 10 | All in One SEO admin (any redirect manager? confirm AIOSEO status) | `aioseo-status-2026-05-10.png` |
| 11 | wp-admin → Settings → Permalinks | `wp-permalinks-2026-05-10.png` |
| 12 | wp-admin → Tools → Site Health → Info → WordPress Constants | `wp-site-health-constants-2026-05-10.png` |

### 9c. WP Engine User Portal screenshots (save to `wp-engine-redirect-rules/`)

| # | Location | Filename target |
|---|---|---|
| 1 | my.wpengine.com → sparkshark/flancoelectric install → Domains tab | `wpe-domains-2026-05-10.png` |
| 2 | Domains → Redirect Rules (if section present) | `wpe-redirect-rules-2026-05-10.png` |
| 3 | General → Force HTTPS state | `wpe-force-https-2026-05-10.png` |
| 4 | Cache → page cache TTL setting | `wpe-cache-2026-05-10.png` |
| 5 | Utilities or Tools — any "Redirects" or "Rules" sub-tab | `wpe-utilities-2026-05-10.png` |

### 9d. GoDaddy Forwarding tab (save to `wp-engine-redirect-rules/` or DNS subfolder)

| # | Location | Filename target |
|---|---|---|
| 1 | dcc.godaddy.com → My Products → DNS → sparkshark.com → **Forwarding** | `godaddy-forwarding-2026-05-10.png` |

### 9e. Google SERP screenshots (save to `flanco-search-screenshots/`)

| # | Query | Filename target |
|---|---|---|
| 1 | `Flanco Electric` | `serp-flanco-electric-2026-05-10.png` |
| 2 | `Flanco Electric Oklahoma City` | `serp-flanco-electric-okc-2026-05-10.png` |
| 3 | `Flanco Electric Moore OK` | `serp-flanco-electric-moore-2026-05-10.png` |
| 4 | `Spark Shark Electric` (for comparison) | `serp-spark-shark-electric-2026-05-10.png` |

### 9f. Citation directories blocked by bot-detection (manual review)

For each, view in a regular browser and capture: the URL the listing shows, displayed phone, displayed address (or service-area), and listing-displayed brand name. Save screenshots into `legacy-phone-address-evidence/`.

- Yelp listing (search "Spark Shark Electric Oklahoma City" + "Flanco Electric Oklahoma City")
- Networx provider profile
- Angi provider profile
- HomeAdvisor provider profile

### 9g. Backlinks — paid tool + Zoo-Local-style email *(saved for last per Brock's directive)*

- Brock names the paid SEO tool (Ahrefs / SEMrush / Moz / other) and either grants login or exports: "Referring domains" + "Backlinks" + "Top anchor text" CSVs into `migration-evidence-pack/07-backlinks-and-citations/`
- Brock forwards/pastes the **Zoo-Local-style email** content (vendor name + backlink-count claim) into `07-backlinks-and-citations/zoo-local-email-2026-05-10.md`

---

## Open Questions for Brock

1. **Permission grant decision:** path A (grant `op item get`) or path B (manual exports/screenshots)? Path A finishes the audit autonomously today.
2. **Case-insensitive URL handling:** keep uppercase URLs working via `vercel.json` case-fold rules, or accept post-cutover 404s on uppercase bookmarks? (Low traffic, but a policy call.)
3. **`lc_internal_api/v1` / `lc_public_api/v1`** — what is "LC"? Could be LiteSpeed Cache (would explain page-cache speed), LearnPress (unlikely for an electrical site), or something custom. The plugins list screenshot will resolve this.

---

## Files Generated (this audit, local-only)

- `auto-run-2026-05-10/raw-tests-2026-05-10.txt` — 2151-line curl chain log
- `auto-run-2026-05-10/sitemap-urls-clean.txt` — 50 URLs extracted from live sitemap
- `auto-run-2026-05-10/post-sitemap.xml`, `page-sitemap.xml` — raw live-WP sitemap files
- `auto-run-2026-05-10/flanco-slug-status.txt` — 6 flanco-slug URL probe results
- `auto-run-2026-05-10/flanco-residue-in-pages.txt` — REST inspection of 3 flanco-search-matching pages
- `auto-run-2026-05-10/citation-probes.txt` — 10 citation directory reachability probes
- This findings doc — `AUDIT_FINDINGS_2026-05-10.md`

# Backlink Risk Findings — GSC Links Audit (v5)

**Audit date:** 2026-05-10
**Working folder:** `/Users/brock/Downloads/migration-evidence-pack 5/07-backlinks-and-citations/`
**Source:** Google Search Console → Links exports for `https://www.sparkshark.com/`
**DNS status:** NOT cut over. Findings are migration-prep evidence only — no DNS, Vercel, WordPress, WP Engine, ServiceTitan, tracking, GSC, or 1Password actions taken.

---

## 1. Total raw exports found

12 raw GSC export CSVs, copied to `raw-gsc-links-exports/`:

| # | File | Bytes | Notes |
|---|------|------|-------|
| 1 | `https___www.sparkshark.com_-Latest links-2026-05-10.csv` | 2,203 | External, with `Last crawled` |
| 2 | `https___www.sparkshark.com_-More sample links-2026-05-10.csv` | 1,882 | External, no date column |
| 3 | `https___www.sparkshark.com_-Top linking sites-2026-05-10.csv` | 354 | External — site/linking-pages/target-pages |
| 4 | `https___www.sparkshark.com_-Top linking text-2026-05-10.csv` | 210 | External — anchor-text top 10 |
| 5 | `https___www.sparkshark.com_-Top target pages-2026-05-10.csv` | 130 | External — top targets (homepage + /electrical-installation/) |
| 6 | `https___www.sparkshark.com_-Top target pages-2026-05-10 (1).csv` | 656 | Internal — top linked pages with internal-link counts |
| 7 | `https___www.sparkshark.com_-Your pages linking to this page-2026-05-10.csv` | 1,794 | Internal drilldown #1 (homepage) |
| 8 | `https___www.sparkshark.com_-Your pages linking to this page-2026-05-10 (1).csv` | 1,725 | Internal drilldown #2 |
| 9 | `https___www.sparkshark.com_-Your pages linking to this page-2026-05-10 (2).csv` | 1,728 | Internal drilldown #3 |
| 10 | `https___www.sparkshark.com_-Your pages linking to this page-2026-05-10 (3).csv` | 1,783 | Internal drilldown — **byte-identical to (4)**; treated as 1 logical drilldown |
| 11 | `https___www.sparkshark.com_-Your pages linking to this page-2026-05-10 (4).csv` | 1,783 | Internal drilldown #4 |
| 12 | `https___www.sparkshark.com_-Your pages linking to this page-2026-05-10 (5).csv` | 1,770 | Internal drilldown #5 |

Effective unique drilldowns after MD5 dedupe: **5** internal target drilldowns (raw `(3)` excluded as a true duplicate of `(4)`).

---

## 2. Total unique external linking URLs

**28 unique external linking URLs** across 17 unique linking domains.
Source: `gsc-external-links-all-deduped.csv` (rows = 28).

Latest links and More sample links each contain the same 28 URLs — every external URL appears in **both** export files.

---

## 3. Total unique internal linking URLs

**28 unique internal linking pages** that link to one or more target pages on `sparkshark.com`.
Source: `gsc-internal-links-all-deduped.csv` (rows = 28).

Per-page coverage across the 5 unique drilldowns:
- Pages appearing in all 5 drilldowns: 18 (these are the high-internal-link service/blog pages)
- Pages appearing in 4 of 5: 5 (homepage, /about-us/, /blogs/, /contact-us/, /electrical-installation/)
- Pages appearing in 3 of 5: 1 (`/2024/01/24/why-you-need-a-professional-for-generator-installation/`)
- Pages appearing in 2 of 5: 1 (`/price/` — possibly removed/orphaned)

---

## 4. URLs matching flagged patterns

### 4a. `flanco` / `flancoelectric` (case-insensitive)

**External (1 URL):**
- `https://www.networx.com/c.flanco-electric` — last crawled 2025-11-09. **P0 — direct legacy-brand citation on a live third-party site.**

**Internal (4 URLs):** Sparkshark.com still has 4 published blog posts whose slugs reference Flanco Electric:
- `https://www.sparkshark.com/2023/12/29/closing-the-deal-with-confidence-why-realtors-should-choose-flanco-electric-for-home-repairs/`
- `https://www.sparkshark.com/2023/12/29/powering-peace-of-mind-unveiling-the-benefits-of-a-home-generator-with-flanco-electric/`
- `https://www.sparkshark.com/2024/01/03/ground-fault-interrupters-the-power-of-gfi-outlets-by-flanco-electric/`
- `https://www.sparkshark.com/2024/01/12/join-our-team-flanco-electric-is-hiring-experienced-journeyman-electricians/`

### 4b. `Spark Shark` / `SparkShark` / `spark` (case-insensitive)

**External (18 URLs containing "spark"):** Includes legitimate Spark Shark profiles AND false-positive lexical matches. Verified breakdown:
- True Spark Shark profile/citation pages (10): bbb.org × 2, callupcontact.com, chamberofcommerce.com, mapquest.com, provenexpert.com, smartelectricalservices.net, uscity.net, best-electrician-moore.com (brand-specific page), pinterest.com.
- Spark Shark social profiles (2): twitter.com/The_Spark_Shark, x.com/The_Spark_Shark.
- Brand mentions in third-party content (2): best-electrician-moore.com homepage, medium.com article.
- **False positives (3):** `yellowpages.com/oklahoma-city-ok/dr-sparks-dds` (dentist), `yellowpages.com/oklahoma-city-ok/hunzicker-lighting`, `dexknows.com/chickasha-ok/electrical-power-systems-maintenance`, `superpages.com/macomb-ok/generators` — these are competitor or generic-category pages where GSC's lexical match flagged "spark" but the page is not a Spark Shark citation.

**Internal:** `https://www.sparkshark.com/2023/12/28/empower-your-home-the-case-for-upgrading-your-electrical-panel-with-spark-shark/` (one blog post slug contains "spark-shark"; many other internal pages contain "spark" via the domain name itself).

### 4c. `BSF` (case-insensitive)

**Zero URLs.** No BSF / BSF Investment Group references appear in any export. `contains_bsf` is `false` on every row.

### 4d. Old `/2023/` or `/2024/` blog paths (internal)

**8 URLs** (all are sparkshark.com internal pages):
- `/2023/12/28/empower-your-home-the-case-for-upgrading-your-electrical-panel-with-spark-shark/`
- `/2023/12/29/closing-the-deal-with-confidence-why-realtors-should-choose-flanco-electric-for-home-repairs/`
- `/2023/12/29/powering-peace-of-mind-unveiling-the-benefits-of-a-home-generator-with-flanco-electric/`
- `/2024/01/03/ground-fault-interrupters-the-power-of-gfi-outlets-by-flanco-electric/`
- `/2024/01/03/stay-powered-up-essential-electrical-winter-safety-tips/`
- `/2024/01/12/join-our-team-flanco-electric-is-hiring-experienced-journeyman-electricians/`
- `/2024/01/24/why-you-need-a-professional-for-generator-installation/`
- `/2024/01/24/why-you-should-hire-a-professional-for-electrical-installations/`

### 4e. `/category/`, `/tag/`, `/author/`, `/wp-content/`

**Zero URLs.** No WordPress archive/taxonomy or asset paths appear in either external or internal exports. (Either these archive pages are not crawled, are noindex'd, or not surfaced in GSC's Top-N reports.)

### 4f. `/repair/`, `/finacing/` (typo per task spec), `/financing/`, `/projects/`, `/lander`

**Zero URLs.** None of these legacy WP slugs appear.

Note: `https://www.sparkshark.com/electrical-repair-and-service/` exists but is the current service slug, not a legacy `/repair/` path.

### 4g. `/price/` (notable separate finding)

**1 URL:** `https://www.sparkshark.com/price/` appears in only 2 of 5 internal drilldowns — significantly less than other service pages — suggesting it may be removed, unlinked from main nav, or orphaned. Worth confirming in the Vercel build.

---

## 5. Citation/directory sources found

12 unique citation/directory domains across 18 URLs (counts from `gsc-link-summary-by-domain.csv`):

| Domain | URLs | Migration priority |
|--------|------|--------------------|
| yellowpages.com | 10 | P3 ignore/monitor (co-citation noise; no Spark Shark profile detected) |
| bbb.org | 2 | P1 review before DNS (two profiles to reconcile) |
| best-electrician-moore.com | 2 | P2 post-launch cleanup |
| networx.com | 1 | **P0 redirect/citation risk (legacy `flanco-electric` slug)** |
| callupcontact.com | 1 | P2 post-launch cleanup |
| chamberofcommerce.com | 1 | P1 review before DNS |
| dexknows.com | 1 | P3 ignore/monitor |
| mapquest.com | 1 | P1 review before DNS |
| provenexpert.com | 1 | P2 post-launch cleanup |
| smartelectricalservices.net | 1 | P2 post-launch cleanup |
| superpages.com | 1 | P3 ignore/monitor |
| uscity.net | 1 | P2 post-launch cleanup |

---

## 6. Social/content sources found

5 domains across 5 URLs:

| Domain | URL | Type | Priority |
|--------|-----|------|----------|
| twitter.com | https://twitter.com/The_Spark_Shark | social/profile | P2 post-launch cleanup |
| x.com | https://x.com/The_Spark_Shark | social/profile (same account) | P2 post-launch cleanup |
| pinterest.com | https://www.pinterest.com/sparksharkelectric/ | social/profile | P2 post-launch cleanup |
| reddit.com | r/AskElectricians thread `1on2zvl` | content/forum | P3 ignore/monitor |
| medium.com | family-kids/holiday-hosting-electrical-tips article | content/blog | P3 ignore/monitor |

---

## 7. URLs that may influence the Vercel redirect map

Two distinct redirect-priority signals:

### 7a. External link equity — must survive redirects

GSC reports backlinks pointing to **2 target pages** on sparkshark.com (`gsc-links-external-top-target-pages.csv`):
1. `https://www.sparkshark.com/` — 26 incoming links, 15 linking sites → **must remain reachable** (homepage redirect must be 200, not 404 or generic).
2. `https://www.sparkshark.com/electrical-installation/` — 2 incoming links, 2 linking sites → **must remain reachable** (slug must exist on Vercel build, or have 301 to nearest equivalent).

### 7b. Internal-link equity — Flanco-slugged blog posts on sparkshark.com

These 4 URLs are currently published on the WP/WP Engine origin and internally linked. If kept after migration, they propagate the Flanco brand on the Spark Shark domain. If removed, they will 404 unless redirected:

- `/2023/12/29/closing-the-deal-with-confidence-why-realtors-should-choose-flanco-electric-for-home-repairs/`
- `/2023/12/29/powering-peace-of-mind-unveiling-the-benefits-of-a-home-generator-with-flanco-electric/`
- `/2024/01/03/ground-fault-interrupters-the-power-of-gfi-outlets-by-flanco-electric/`
- `/2024/01/12/join-our-team-flanco-electric-is-hiring-experienced-journeyman-electricians/`

Plus 4 non-Flanco 2023/2024 blog posts and `/price/` (orphan-suspect) — total **9 legacy paths** to confirm in the Vercel redirect map before DNS cutover.

---

## 8. URLs that may influence citation / NAP cleanup

### 8a. P0 (immediate cleanup before launch)

- **`https://www.networx.com/c.flanco-electric`** — third-party citation under the legacy Flanco brand. This is the single most important external NAP risk in the dataset because it actively presents a brand other than Spark Shark. Action: contact Networx to (a) update the listing slug + business name to Spark Shark Electric, or (b) remove the listing entirely and replace with a fresh Spark Shark listing.

### 8b. P1 (review and verify before DNS cutover)

These NAP-critical profiles influence map results, BBB lookups, and Chamber-of-Commerce panels. Verify name, address, phone, hours, website URL all show Spark Shark Electric:

- `https://www.bbb.org/us/ok/moore/profile/electrical-contractors/spark-shark-electric-0995-90130075`
- `https://www.bbb.org/us/ok/oklahoma-city/profile/electrical-contractors/spark-shark-electric-0995-90130075/addressId/134759` (reconcile duplicate-address entry)
- `https://www.mapquest.com/us/oklahoma/spark-shark-electric-778761940`
- `https://www.chamberofcommerce.com/business-directory/oklahoma/moore/electrician/2034210950-spark-shark-electric`

### 8c. P2 (post-launch cleanup)

Lower-traffic citation/profile pages — claim/verify after cutover stabilizes:
- best-electrician-moore.com (homepage + brand page)
- callupcontact.com profile
- provenexpert.com profile
- smartelectricalservices.net profile
- uscity.net profile (HTTP — request HTTPS)
- twitter.com / x.com Spark Shark profile
- pinterest.com Spark Shark profile

### 8d. P3 (ignore / monitor)

Co-citation noise — no NAP action available because these aren't actually Spark Shark profiles:
- All 10 yellowpages.com URLs (competitor/category pages)
- dexknows.com category page
- superpages.com category page
- medium.com article (third-party)
- reddit.com thread (third-party)

---

## 9. Items to include in Deep Research

1. **Networx Flanco citation cleanup playbook** — what's the standard process to update or remove a Networx listing? Contact path, expected response time, and whether GSC will recrawl quickly.
2. **BBB duplicate profile reconciliation** — both BBB profiles share the same business ID `0995-90130075` but have different city listings (Moore vs. OKC) and a separate `addressId/134759`. Determine whether these are intentional service-area duplicates or should be merged.
3. **Flanco-branded blog post strategy** — for the 4 published Flanco-named posts on sparkshark.com: rewrite under Spark Shark byline + redirect old URL, or delete + 301 to a topical Spark Shark equivalent? Decision affects redirect-map size and SEO equity.
4. **Yellow Pages presence gap** — Spark Shark Electric does not appear to have its own YellowPages business profile (only competitor/category pages link). Decide whether to claim/create one as part of citation outreach.
5. **`/price/` page status** — confirm whether this page is intentionally orphaned, deprecated, or simply moved. Decide whether to keep, redirect, or remove from sitemap.
6. **"Top linking text" signal review** — top 10 anchor text shows mostly URL-as-text (`https www sparkshark com`, `website`, `visit website`), not keyword-rich anchors. Worth a Deep Research item: should outreach explicitly request anchor-text updates for new citations?
7. **Third-party backlink-tool comparison** — Ahrefs / Semrush / Moz typically surface 5–20× more backlinks than GSC's truncated 28-row export. If any prior-vendor reports exist, they belong in `09-past-marketing-audits/incoming/`. (See section 10.)

---

## 10. What's still missing / nice-to-haves

- **Third-party backlink reports** — GSC's Links report is heavily sampled and capped. Ahrefs, Semrush, Moz, BrightLocal, Whitespark, or Yext exports from prior marketing vendors would reveal additional Flanco / BSF Investment Group / older Spark Shark references that GSC does not show. Path to drop them: `09-past-marketing-audits/incoming/`.
- **Legacy `flanco.com` / `flancoelectric.com` GSC property exports** — if a separate GSC property exists for any retired Flanco-era domain, exporting its Links report would surface 301-source URLs and more legacy citations.
- **Google Business Profile (GBP) inbound/citation report** — GBP has its own "Where customers find you" data. Not part of this folder; lives under `05-google-business-profile/` if exported.
- **Manual scan of the no-suffix vs. (1)/(2)/(4)/(5) drilldown identities** — the Top target pages (internal) shows 13 sparkshark.com pages with high internal-link counts (most are 26), but only 5 drilldown CSVs were exported. The other 8 high-link pages (e.g., `/about-us/`, `/blogs/`, `/contact-us/`, several service pages) do not have a drilldown CSV — additional GSC drilldowns would tighten the internal-link map.
- **Anchor-text drilldown** — Top linking text export only includes ranks 1–10. If the "Export external links" → "Top linking text" supports more rows, an extended export would reveal whether any anchor text still says "Flanco" or "Flanco Electric."
- **`/price/` confirmation** — see Deep Research item #5; status currently inferred from drilldown coverage, not from a live URL check.

---

## Cross-reference

- Per-URL labels: `gsc-external-links-all-deduped.csv`
- Per-internal-page labels: `gsc-internal-links-all-deduped.csv`
- Per-domain priority + recommended action: `gsc-link-summary-by-domain.csv`
- Audit script (reproducible): `_tools/gsc_audit.py`
- Raw GSC exports (12 files): `raw-gsc-links-exports/`

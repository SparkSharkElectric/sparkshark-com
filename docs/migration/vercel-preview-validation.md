# Vercel Preview Validation — Spark Shark Electric

> **STATUS: Historical.** Cutover completed 2026-05-14. Vercel is now serving production at sparkshark.com. This validation record is preserved as an archive of the pre-cutover acceptance check.

## 1. Purpose

This document records the first successful Vercel preview validation after moving the Spark Shark Electric marketing site toward Vercel production hosting. It records what was tested, what passed, which deployment was validated, and what still does not authorize DNS cutover.

DNS cutover remains gated by `docs/migration/launch-gate.md`, which still has 9 Brock-owned items in **Not Provided** status. Cutover authority lives entirely in the launch gate.

---

## 2. Current validated deployment

| Field | Value |
|---|---|
| Main Vercel alias | https://sparkshark-com-git-main-spark-shark-electric-2b2f3a3a.vercel.app |
| Main merge commit | `36ec345afb170d717561894fc53647fa95f50596` |
| PR #3 | Vercel config + DNS launch gate (`vercel.json`, `docs/migration/launch-gate.md`, doc updates) |
| PR #4 | Explicit 301 redirect correction (replaced `permanent: true` → `statusCode: 301`) |
| Validation date | 2026-05-10 |

---

## 3. What passed

### Asset and document fetches (all returned HTTP 200)

- `/` (homepage)
- `/css/site.css`
- `/js/site.js`
- `/img/logo.png`
- `/sitemap.xml`
- `/robots.txt`

### `/sparkshark-com` leakage check

- Returned **0 matches** in production-served HTML.
- Confirms `BASE=""` build under Vercel's `buildCommand` correctly produced root-relative asset paths.

### Conservative security headers present

| Header | Value |
|---|---|
| `Strict-Transport-Security` | `max-age=31536000` |
| `X-Content-Type-Options` | `nosniff` |
| `X-Frame-Options` | `SAMEORIGIN` |
| `Referrer-Policy` | `strict-origin-when-cross-origin` |
| `Permissions-Policy` | `camera=(), microphone=(), geolocation=(), interest-cohort=()` |

HSTS is intentionally conservative during migration: no `preload`, no `includeSubDomains`. Both belong in a follow-up hardening PR after launch is stable.

### Asset cache header

`/css/site.css`, `/js/site.js`, and `/img/logo.png` returned:

```
Cache-Control: public, max-age=3600, must-revalidate
```

Conservative on purpose. These filenames are not content-hashed; 1-year immutable on unhashed filenames would pin stale assets for clients. Revisit caching policy after `build.py` emits hashed filenames.

### Interior pages (all returned HTTP 200)

- `/`
- `/services/`
- `/about-us/`
- `/contact-us/`
- `/generators/`
- `/electrical-installation/`
- `/switches-and-outlets/`
- `/reviews/`
- `/moore/`
- `/oklahoma-city/`
- `/locations-we-serve/`
- `/locations-we-serve/norman/`
- `/locations-we-serve/edmond/`

### Redirects

Safe-known redirects returned **HTTP 301** with the expected `Location` header. See §4 for the table.

### Sitemap and robots

- `sitemap.xml` URL count: **40**.
- This is correct. The site has 50 `index.html` files; 10 of them are redirect stubs that are excluded from the sitemap because they live at the same paths that `vercel.json` redirects with HTTP 301. Excluding them prevents Google from crawling stub pages it should never see.
- `robots.txt` loads with HTTP 200 and points to `https://www.sparkshark.com/sitemap.xml`. No `Disallow` rules.

---

## 4. Redirect validation table

| Source | Expected destination | Observed status | Result |
|---|---|---|---|
| `/commercial-electrical-solutions/` | `/` | 301 | PASS |
| `/industrial-electrical-solutions/` | `/` | 301 | PASS |
| `/home-staging-2026-05-07/` | `/` | 301 | PASS |
| `/2023/12/29/closing-the-deal-with-confidence-why-realtors-should-choose-spark-shark-for-home-repairs/` | `/` | 301 | PASS |
| `/2024/01/02/powering-tomorrow-a-comprehensive-guide-to-new-construction-wiring-with-spark-shark/` | `/electrical-installation/` | 301 | PASS |
| `/2024/01/12/join-our-team-spark-shark-is-hiring-experienced-journeyman-electricians/` | `/` | 301 | PASS |
| `/2023/12/28/empower-your-home-the-case-for-upgrading-your-electrical-panel-with-spark-shark/` | `/2026/05/07/signs-you-need-electrical-panel-upgrade/` | 301 | PASS |
| `/2024/01/24/why-you-should-hire-a-professional-for-electrical-installations/` | `/electrical-installation/` | 301 | PASS |
| `/2023/12/29/powering-peace-of-mind-unveiling-the-benefits-of-a-home-generator-with-spark-shark/` | `/generators/` | 301 | PASS |
| `/2024/01/01/power-up-your-new-year-the-case-for-whole-home-surge-protectors-with-spark-shark/` | `/electrical-installation/` | 301 | PASS |
| `/2024/01/03/ground-fault-interrupters-the-power-of-gfi-outlets-by-spark-shark/` | `/switches-and-outlets/` | 301 | PASS |

**Note on entry count.** `vercel.json` contains 14 redirect entries because three sources (`/commercial-electrical-solutions`, `/industrial-electrical-solutions`, `/home-staging-2026-05-07`) include both slash and non-slash variants for safety. The terminal validation above checked the main slash variants and all passed as 301. The non-slash variants share the same rule structure and Vercel applies them identically.

---

## 5. What this does NOT approve

This document is preview-validation evidence. It is **not** a launch sign-off. None of the following are approved by this validation pass:

- Does **NOT** approve DNS cutover.
- Does **NOT** approve adding `sparkshark.com` or `www.sparkshark.com` as Vercel project domains.
- Does **NOT** approve WordPress / WP Engine decommissioning.
- Does **NOT** approve tracking readiness (GA4, GTM, Google Ads, GSC verification, Clarity).
- Does **NOT** approve contact form readiness (Formspree ID or Vercel Function decision still pending).
- Does **NOT** approve ServiceTitan booking flow on the Vercel preview.
- Does **NOT** approve NAP, schema, or final SEO readiness.

DNS cutover remains blocked by `docs/migration/launch-gate.md`.

---

## 6. Known remaining blockers

Items still required before DNS cutover can be considered:

- GSC Pages export (launch gate item #1)
- GSC Queries export (launch gate item #2)
- GSC Indexed / Not Indexed export (launch gate item #3)
- Google Business Profile screenshots (launch gate item #4)
- Current DNS records screenshot (launch gate item #5)
- WP Engine backup confirmation (launch gate item #6)
- GA4 / GTM / Google Ads IDs (launch gate item #7)
- ServiceTitan scheduler test proof (launch gate item #8)
- Canonical address decision (launch gate item #9)
- Contact form fix (Formspree ID or Vercel Function)
- Pre-launch Deep Research (uses GSC + backlink evidence)
- Final redirect inventory from GSC, crawl, and backlink evidence (drives v1.1 redirect map)

---

## 7. Re-validation commands

These are the exact terminal command blocks used. Use absolute paths for `curl`, `grep`, `awk`, `head`, `tr` because the validating shell's `PATH` was unreliable.

Set the alias once per shell session:

```bash
ALIAS="https://sparkshark-com-git-main-spark-shark-electric-2b2f3a3a.vercel.app"
```

### Quick 200 check (homepage + key assets + sitemap/robots)

```bash
for path in / /css/site.css /js/site.js /img/logo.png /sitemap.xml /robots.txt; do
  printf '%-20s ' "$path"
  /usr/bin/curl -sS -o /dev/null -w '%{http_code}\n' "${ALIAS}${path}"
done
```

### 200 check for interior pages

```bash
for path in / /services/ /about-us/ /contact-us/ /generators/ /electrical-installation/ /switches-and-outlets/ /reviews/ /moore/ /oklahoma-city/ /locations-we-serve/ /locations-we-serve/norman/ /locations-we-serve/edmond/; do
  printf '%-32s ' "$path"
  /usr/bin/curl -sS -o /dev/null -w '%{http_code}\n' "${ALIAS}${path}"
done
```

### Redirect 301 check (status + Location header)

```bash
for path in \
  /commercial-electrical-solutions/ \
  /industrial-electrical-solutions/ \
  /home-staging-2026-05-07/ \
  /2023/12/29/closing-the-deal-with-confidence-why-realtors-should-choose-spark-shark-for-home-repairs/ \
  /2024/01/02/powering-tomorrow-a-comprehensive-guide-to-new-construction-wiring-with-spark-shark/ \
  /2024/01/12/join-our-team-spark-shark-is-hiring-experienced-journeyman-electricians/ \
  /2023/12/28/empower-your-home-the-case-for-upgrading-your-electrical-panel-with-spark-shark/ \
  /2024/01/24/why-you-should-hire-a-professional-for-electrical-installations/ \
  /2023/12/29/powering-peace-of-mind-unveiling-the-benefits-of-a-home-generator-with-spark-shark/ \
  /2024/01/01/power-up-your-new-year-the-case-for-whole-home-surge-protectors-with-spark-shark/ \
  /2024/01/03/ground-fault-interrupters-the-power-of-gfi-outlets-by-spark-shark/; do
  status=$(/usr/bin/curl -sS -o /dev/null -w '%{http_code}' "${ALIAS}${path}")
  loc=$(/usr/bin/curl -sSI "${ALIAS}${path}" | /usr/bin/grep -i '^location:' | /usr/bin/tr -d '\r')
  printf '%-110s %s  %s\n' "$path" "$status" "$loc"
done
```

### Header / cache checks

```bash
/usr/bin/curl -sSI "${ALIAS}/" \
  | /usr/bin/grep -iE '^(strict-transport-security|x-content-type-options|x-frame-options|referrer-policy|permissions-policy|cache-control):' \
  | /usr/bin/tr -d '\r'

/usr/bin/curl -sSI "${ALIAS}/css/site.css" \
  | /usr/bin/grep -iE '^cache-control:' \
  | /usr/bin/tr -d '\r'
```

### Sitemap and robots checks

```bash
# Sitemap URL count (expect 40)
/usr/bin/curl -sS "${ALIAS}/sitemap.xml" \
  | /usr/bin/grep -oE '<loc>[^<]+</loc>' \
  | /usr/bin/awk 'END{print NR}'

# Sitemap first/last entries (smoke check)
/usr/bin/curl -sS "${ALIAS}/sitemap.xml" \
  | /usr/bin/grep -oE '<loc>[^<]+</loc>' \
  | /usr/bin/head -3

# robots.txt content
/usr/bin/curl -sS "${ALIAS}/robots.txt"
```

### Optional: `/sparkshark-com` leakage spot-check

```bash
/usr/bin/curl -sS "${ALIAS}/" | /usr/bin/grep -c '/sparkshark-com'    # expect 0
/usr/bin/curl -sS "${ALIAS}/services/" | /usr/bin/grep -c '/sparkshark-com'  # expect 0
```

---

## 8. Next recommended workstream

In order:

1. **Build the `migration-evidence-pack/` folder structure locally** (outside the repo, per `docs/migration/launch-gate.md`). Match the documented subfolders so paths in the gate items table line up with where evidence lands.
2. **Gather Brock-owned launch-gate evidence.** All 9 items in the gate are Brock-owned. Until each is **Approved** or **Not Applicable with written reason**, DNS cutover is blocked.
3. **Run pre-launch Deep Research using the actual evidence** (GSC Pages/Queries/Indexing + backlink data + GBP). Output: a defensible v1.1 redirect map and a tracking spec.
4. **Patch the final redirect map** in `vercel.json` based on the GSC and backlink evidence. Promote any §7b candidates that the data supports. Land as a separate, scoped PR.
5. **Fix tracking and contact form.** Tracking install (GSC verification meta, GA4/GTM, optional Clarity) and the contact form decision (Formspree ID vs Vercel Function) ship as discrete PRs.
6. **Only then prepare the DNS / cutover runbook** (`docs/migration/cutover-runbook.md`). The runbook's step 0 is a re-read of `docs/migration/launch-gate.md` and a re-confirmation that every item is Approved or Not Applicable with written reason.

DNS does not move until the gate is green.

---

**Authored:** 2026-05-10
**Validated against:** main commit `36ec345afb170d717561894fc53647fa95f50596`, Vercel main alias `https://sparkshark-com-git-main-spark-shark-electric-2b2f3a3a.vercel.app`
**Authority for DNS cutover:** `docs/migration/launch-gate.md` (unchanged by this document)

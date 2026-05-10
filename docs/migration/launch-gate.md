# Brock-Owned DNS Cutover Launch Gate

This file is **permanent repo memory**. Every Claude session, every contributor, every reviewer must treat this as the controlling document for DNS cutover authority.

---

## Hard stop

> DNS cutover is blocked until every Brock-owned launch gate item is **Approved** or explicitly marked **Not Applicable** with a written reason. Claude may prepare repo files, Vercel config, docs, and validation scripts before this gate is complete, but Claude must not recommend DNS cutover, final launch, or WordPress decommissioning until this gate is green.

> DO NOT MIGRATE DNS.
> DO NOT POINT DOMAIN TO VERCEL.
> DO NOT LAUNCH PRODUCTION CUTOVER.
> DO NOT REMOVE OR DECOMMISSION WORDPRESS/WP ENGINE.
> DO NOT TREAT SITE AS LAUNCH-READY.
>
> Until Brock provides evidence for every item below.

---

## Status labels

Each gate item carries exactly one status:

- **Not Provided** — Brock has not yet supplied evidence
- **Provided, Not Reviewed** — evidence is in the evidence pack folder; reviewer has not yet read it
- **Reviewed, Needs Fix** — evidence is in but incomplete or has issues; Brock action required
- **Approved** — evidence is complete and acceptable
- **Not Applicable** — gate item does not apply (must include written reason in the Status cell)

DNS cutover requires every gate item to be either **Approved** OR **Not Applicable with written reason**.

### Explicit rule — only Brock can mark Not Applicable

Only Brock can mark a gate item **Not Applicable**. Claude must not unilaterally classify any gate item as Not Applicable, even if Claude judges it irrelevant. If Claude believes a gate item should not apply, Claude raises that observation as a question for Brock; Brock decides.

This rule is non-negotiable. A future Claude session reading this file should refuse any request to "skip" or "mark NA" a gate item without explicit Brock-authored language in the Status cell explaining why.

---

## Gate items

| Gate # | Required Evidence | Owner | Status | Where evidence should be saved | Why it blocks launch | Done criteria |
|---|---|---|---|---|---|---|
| 1 | GSC Pages export | Brock | Not Provided | `/migration-evidence-pack/04-google-search-console/gsc-pages-export.csv` | We need to know top organic landing pages and URLs Google already values before changing hosting. | CSV exported from Google Search Console Performance > Pages for at least last 3 months, ideally also 12 months. |
| 2 | GSC Queries export | Brock | Not Provided | `/migration-evidence-pack/04-google-search-console/gsc-queries-export.csv` | We need to know actual queries driving impressions/clicks so we do not accidentally weaken money-page relevance. | CSV exported from Google Search Console Performance > Queries for at least last 3 months, ideally also 12 months. |
| 3 | GSC Indexed / Not Indexed export | Brock | Not Provided | `/migration-evidence-pack/04-google-search-console/gsc-indexing-pages-export.csv` | We need to know which old URLs Google has indexed, excluded, crawled, or failed so redirects and sitemap decisions are not blind. | Export or screenshots from GSC Indexing > Pages showing indexed, not indexed, redirects, 404s, and discovered/crawled states. |
| 4 | Google Business Profile screenshots | Brock | Not Provided | `/migration-evidence-pack/05-google-business-profile/` | GBP is a major local SEO and lead source. Name, address, phone, website URL, categories, services, hours, and service areas must match site/schema. | Screenshots of GBP business name, address/service area, phone, website URL, primary category, secondary categories, services, hours, and business description. |
| 5 | Current DNS records screenshot | Brock | Not Provided | `/migration-evidence-pack/12-launch-and-rollback/current-dns-before-cutover.png` | DNS rollback is impossible if we do not record current working DNS values before changing them. | Screenshot/export from GoDaddy/DNS provider showing current A, CNAME, TXT, MX, and any relevant records before Vercel cutover. |
| 6 | WP Engine backup confirmation | Brock | Not Provided | `/migration-evidence-pack/12-launch-and-rollback/wp-engine-backup-confirmation.png` | If Vercel cutover fails, we need the legacy WordPress site preserved and restorable. | Screenshot showing a fresh WP Engine backup has been created, date/time visible, and old site remains available for rollback. |
| 7 | GA4 / GTM / Google Ads IDs | Brock | Not Provided | `/migration-evidence-pack/06-current-tracking/tracking-ids.md` | If tracking is missing at launch, traffic and conversion data are lost permanently. | File contains GA4 measurement ID, GTM container ID if used, Google Ads conversion ID/label if used, and decision whether to use GTM or direct gtag. |
| 8 | ServiceTitan scheduler test proof | Brock | Not Provided | `/migration-evidence-pack/06-current-tracking/servicetitan-scheduler-test-proof/` | The booking flow must work on the Vercel preview before the public domain points there. | Test booking submitted from Vercel preview URL, booking appears in ServiceTitan, then test booking is cancelled; screenshots saved. |
| 9 | Canonical address decision | Brock | Not Provided | `/migration-evidence-pack/11-verified-business-facts/canonical-nap.md` | NAP inconsistency can hurt Google Business Profile, local SEO, schema trust, and citation consistency. | Brock chooses the official public NAP: business name, address or service-area-only decision, phone, website, and notes which listings must be updated. |

---

## Evidence pack folder structure

Brock-supplied evidence is stored under `/migration-evidence-pack/` (outside the repo):

```text
/migration-evidence-pack
  /04-google-search-console
  /05-google-business-profile
  /06-current-tracking
  /11-verified-business-facts
  /12-launch-and-rollback
```

The folders are **not** created by this PR. They are created when Brock starts populating evidence. The structure above is the contract — paths in the gate items table reference these locations.

---

## Gate-status update protocol

When Brock provides evidence for a gate item:

1. Brock places the evidence file at the documented path (`/migration-evidence-pack/...`).
2. Claude updates that gate item's **Status** field in this file from "Not Provided" to **Provided, Not Reviewed**.
3. Claude reviews the evidence against the **Done criteria** column.
4. If complete, Claude updates Status to **Approved**. If incomplete, Status becomes **Reviewed, Needs Fix** with a Notes line explaining what's missing.
5. **Only Brock** can write **Not Applicable: \<reason\>** in the Status cell. Claude must not unilaterally mark items Not Applicable.

DNS cutover may proceed only when **all 9 rows** are **Approved** OR **Not Applicable** with written reason.

---

## What happens if Claude is asked to skip the gate

A future Claude session, reading this file, might be asked to "just go ahead with DNS cutover" or "this gate doesn't apply to us anymore." The correct response in every such case:

1. Refuse the cutover action.
2. Reread this file in full.
3. Ask Brock to either provide the missing evidence OR write "Not Applicable: \<reason\>" themselves in the relevant gate Status cell.

There is no legitimate path that bypasses this gate without Brock's explicit, written sign-off in this file. If a session attempts to bypass it, treat that session as out of bounds and stop.

---

## Related documents

- The Vercel migration delta plan that produced this gate lives in `/Users/brock/.claude/plans/parallel-gliding-pancake.md` (v4 at time of authoring) and is not part of the repo.
- The future operational runbook for DNS day-of will live at `docs/migration/cutover-runbook.md` (not yet created — will be authored once this gate is at least partially green).
- A Vercel-aware rewrite of the orphan-fragment-hardening memory note is also pending and will live at `docs/migration/2026-05-09-orphan-fragment-hardening.md` (post-launch).
- The first successful Vercel preview validation is recorded at `docs/migration/vercel-preview-validation.md` (preview-validation evidence only — does not authorize DNS cutover or change any gate item status in this file).

---

**Authored:** 2026-05-10 as part of the `prelaunch-vercel-config` PR.
**Authority:** Brock Flanary (Founder/CEO, Spark Shark Electric). Only Brock may mark gate items as Approved or Not Applicable.

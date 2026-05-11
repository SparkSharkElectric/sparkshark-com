# Legacy Flanco / Spark Shark / BSF Entity Audit (Local)

**Status:** Local-only. Not committed to git. Inherits `migration-evidence-pack/.gitignore: *`.
**Created:** 2026-05-10
**Anchored to main commit:** `ab80db2`

This folder is **supplemental migration evidence**. It is not a launch-gate item on its own, but the evidence collected here informs the v1.1 redirect map (gate context #1–#3), the citation-cleanup map under gate #4, and the canonical NAP posture in gate #9. It is also the staging area for inputs that Deep Research will use to reason about legacy URL coverage and entity hygiene.

---

## Why this folder exists

The Vercel migration is also an **entity migration**. Three distinct names exist in public/legacy data:

- **Spark Shark Electric** — the public brand (always with the space). Customer-facing surface.
- **Flanco Electric** — the legacy brand name from the pre-rebrand era. Still surfaces in:
  - GSC-indexed and crawled URLs (e.g. `…-with-flanco-electric` blog slugs — see GSC summary §3 of `13-deep-research/00_DEEP_RESEARCH_INPUT_BRIEF.md`).
  - Older citations / directory listings.
  - Old Google search results.
  - Possibly old GBP / business profile content.
- **BSF Investment Group, LLC** — parent legal entity. Should appear only where legally required; not a customer-facing brand.

The mix of these entities in the wild creates two distinct risks:

1. **SEO link-equity loss** if legacy Flanco URLs and citations are not properly redirected / updated during the WP → Vercel cutover.
2. **Public NAP / entity confusion** if customers see Flanco branding, old phone numbers, or old addresses alongside the current Spark Shark Electric presence.

---

## Goal

- **Preserve useful Flanco-era SEO / link equity** by mapping every legacy Flanco URL or citation worth saving into an explicit 301 redirect in `vercel.json` (or, where redirects are not the right tool, into a documented citation-cleanup task).
- **Reduce public NAP / entity confusion** by inventorying every stale instance of Flanco branding, old phone numbers, and old physical-address references, and tracking each through cleanup.
- **Do NOT publicly promote Flanco.** The Flanco brand is a legacy artifact. The point of this folder is not to revive Flanco, but to migrate it cleanly out of the public surface while keeping the equity Google has already attributed to those URLs / entities.
- **Maintain canonical NAP discipline.** Per `11-verified-business-facts/canonical-nap.md`, the public posture is service-area-only with `Moore, OK / Oklahoma City Metro` wording. The internal/private street address must not surface in any customer-facing copy unless Brock explicitly approves later.

---

## Evidence to collect

Save artifacts under the documented subfolders below. Filename pattern is suggested, not enforced.

### `wp-engine-redirect-rules/`

- Screenshots / exports of any **WP Engine-level redirect rules** currently in place (the WP Engine User Portal lets you configure server-level redirects per environment).
- If WP Engine has a rules-export feature, save the export here in addition to the screenshots.
- Suggested filename: `wpe-redirect-rules-<environment>-2026-05-10.png` / `.csv` / `.json`.

### `wordpress-redirect-plugins/`

- Screenshots / exports from any WordPress redirect plugin currently active on the legacy site (e.g. Redirection, Yoast Premium redirects, Safe Redirect Manager, Rank Math redirects).
- Capture: plugin name + version, full rule list with source / destination / HTTP status, any 404 logs the plugin keeps.
- Suggested filename: `<plugin-name>-rules-2026-05-10.png` / `.csv`.

### `flanco-search-screenshots/`

- Google search results screenshots for the brand-name queries that exist in the wild:
  - `Flanco Electric`
  - `Flanco Electric Oklahoma City` / `Flanco Electric Moore OK`
  - `Spark Shark Electric` (for comparison — the current brand)
  - `BSF Investment Group` (for parent-entity exposure check — should be near zero)
- Capture: SERP top section (Knowledge Panel if any, Map Pack, top organic results), date-stamped.
- Suggested filename: `serp-flanco-electric-2026-05-10.png`, `serp-spark-shark-electric-2026-05-10.png`, `serp-bsf-investment-group-2026-05-10.png`.

### `legacy-phone-address-evidence/`

- Citation / directory listings that currently surface **stale NAP data**:
  - Old phone numbers (any number that is not `(405) 436-4776`).
  - Old / private physical address strings (anything other than the service-area-only public posture).
  - Old brand names (Flanco Electric variants, misspellings, missing spaces).
- Sources to spot-check (not exhaustive): Yelp, BBB, Networx, Thumbtack, ProvenExpert, Apple Maps, Bing Places, Nextdoor, Angi, HomeAdvisor, ServiceTitan booking-link surface.
- Save: screenshot of each listing with the stale value highlighted, plus a brief note on what's stale.
- Suggested filename: `<directory>-<flanco-or-old-nap-feature>-2026-05-10.png`.

### Cross-folder evidence (live where best fits)

- **GSC Links exports** (gate context #1–#3). External links and top linking sites are exported from GSC under Search Console → Links. Save those exports at `migration-evidence-pack/07-backlinks-and-citations/` (the sibling folder created with this audit). They feed both this audit and the broader backlink-coverage question.
- **Old Flanco URLs** indexed / crawled / discovered by Google: already captured in v3 GSC evidence at `04-google-search-console/03-indexed-pages/`, `…/04-crawled-currently-not-indexed/`, `…/05-discovered-currently-not-indexed/`. The Deep Research brief surfaces the specific `flanco-electric`-slug URLs not yet covered by `vercel.json` redirects.
- **Old GBP / business profile evidence** for Flanco: if any old Flanco GBP listing still exists (separate from the current Spark Shark Electric GBP), capture screenshots and save here under `flanco-search-screenshots/` or a new subfolder. If no separate Flanco listing exists, note that finding in this README's notes section.

---

## How this connects to the launch gate and downstream artifacts

- **`vercel.json` v1.1 redirect map.** Every legacy Flanco URL with measurable equity becomes a candidate `statusCode: 301` entry. Promotions happen in a separate, scoped PR after Deep Research review.
- **Launch-gate item #4 (GBP).** GBP evidence in `05-google-business-profile/` already aligns to the public Spark Shark Electric profile. This audit additionally probes whether any legacy Flanco GBP entity exists in the wild.
- **Launch-gate item #9 (canonical NAP).** Citation cleanup is downstream of the NAP decision in `11-verified-business-facts/canonical-nap.md`. The legacy phone/address evidence collected here becomes the input to the listings-update map.
- **Pre-launch Deep Research.** This audit's outputs feed the §8.2 (redirect sufficiency) and §8.4 (schema / NAP risks) questions in `13-deep-research/00_DEEP_RESEARCH_INPUT_BRIEF.md`.

---

## Hard rules

- This folder is **local-only**. The parent `migration-evidence-pack/.gitignore` (`*`) makes the folder invisible to git. **Do not commit anything here.**
- Do **not** publicly promote Flanco Electric. Anything Flanco-related in this folder is evidence of legacy footprint, not promotional material.
- Do **not** surface the private street address in any customer-facing copy. Per `canonical-nap.md`, the public posture is service-area-only.
- Do **not** edit WP Engine redirect rules, WordPress plugin rules, GBP settings, or any directory listing as part of evidence collection. **Evidence collection is observation-only.** Changes to those surfaces are separate, scoped tasks.
- Do **not** add domains to Vercel.
- **DNS cutover remains blocked** by `docs/migration/launch-gate.md`. This audit does not change any gate status.

---

## Notes section (fill as evidence is collected)

- Date of first audit pass:
- Reviewer:
- Number of WP Engine-level redirect rules observed:
- Number of WordPress plugin-level redirect rules observed:
- Distinct legacy phone numbers found:
- Distinct legacy physical-address strings found:
- Distinct directory / citation surfaces with stale NAP / brand:
- Open questions surfaced during audit:

---

## Reference

- Launch gate (controlling document): `docs/migration/launch-gate.md`
- Preview validation: `docs/migration/vercel-preview-validation.md`
- Vercel deploy contract: `vercel.json`
- Canonical NAP decision: `migration-evidence-pack/11-verified-business-facts/canonical-nap.md`
- Deep Research input brief: `migration-evidence-pack/13-deep-research/00_DEEP_RESEARCH_INPUT_BRIEF.md`
- Backlinks / citations sibling folder: `migration-evidence-pack/07-backlinks-and-citations/`
- Evidence-pack overview: `migration-evidence-pack/README-local-evidence-pack.md`

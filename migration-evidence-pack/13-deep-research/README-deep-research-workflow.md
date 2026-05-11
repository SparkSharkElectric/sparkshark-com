# Deep Research — Local Workflow

**Status:** Local-only. Not committed to git.
**Created:** 2026-05-10
**Anchored to main commit:** `ab80db2` (PR #5 — vercel-preview-validation doc landed)

This folder is the local destination for **Deep Research outputs** produced for the Spark Shark Electric Vercel migration. It is covered by the parent folder's `.gitignore` rule (`migration-evidence-pack/.gitignore: *`), so everything saved here is fully invisible to git.

---

## What lives here

Save the raw outputs and any working notes from the following research tools:

- **ChatGPT (Deep Research / GPT-5 deep mode / o-series tasks)**
- **Gemini (Deep Research / 2.x deep mode)**
- **Perplexity (Pro / Deep Research / Spaces)**
- **Claude Research (claude.ai Research mode)**

Suggested filename pattern (not enforced):

```
YYYY-MM-DD_<tool>_<topic>.md
YYYY-MM-DD_<tool>_<topic>.pdf
YYYY-MM-DD_<tool>_<topic>.txt
```

Examples:

```
2026-05-10_chatgpt_redirect-inventory.md
2026-05-10_gemini_local-seo-okc-electrician.md
2026-05-10_perplexity_backlink-audit.md
2026-05-10_claude_gsc-pages-analysis.md
```

Subfolders by tool are optional. Pick whichever organization helps you compare outputs side-by-side.

---

## Why these outputs matter to the migration

Deep Research outputs feed three Vercel-migration decisions, in this order:

1. **v1.1 redirect map.** GSC + backlink + crawl evidence promotes any §7b candidates from the original plan into `vercel.json`. Examples to validate against evidence:
   - `/locations-we-serve/bethany/` → `/locations-we-serve/`
   - `/category/...`, `/tag/...`, `/author/...` → `/`
   - `/wp-content/...`, `/wp-admin/...`, `/wp-login.php` → `/`
   - `/feed`, `/feed/`, `/rss` → `/blogs/`
   - `/sitemap_index.xml` → `/sitemap.xml`
2. **Tracking spec.** GA4 / GTM / Google Ads / Clarity install plan, including event taxonomy (phone-tap, scheduler-open, form-submit, lead-quality signals). Driven by launch-gate item #7.
3. **Local-SEO / GEO posture.** OKC-metro service-area shape, NAP consistency map (gate #9), GBP optimization opportunities (gate #4), and any competitive landscape findings worth noting before launch.

Outputs that don't tie to one of those three buckets are still welcome — they just won't drive a launch-gate decision.

---

## Hard rules

- This folder is **local-only**. Inherited gitignore from `migration-evidence-pack/.gitignore` (`*`) makes the folder invisible to git. **Do not commit anything here.**
- Do **not** copy raw research outputs into the repo (`docs/`, `copy-drafts/`, `CLAUDE.md`, etc.) unless Brock explicitly approves moving a *distilled* finding to a tracked location.
- DNS cutover remains **blocked** by `docs/migration/launch-gate.md`. Research outputs do not change gate status. Only Brock may mark gate items Approved or Not Applicable.
- ServiceTitan scheduler test proof (launch-gate item #8) is **deferred** — research outputs cannot substitute for the live booking-flow test on the Vercel preview.
- Tracking implementation in production HTML is **not approved**. Research can produce a *spec*; the spec does not authorize installing tags. Tag install is a separate, scoped PR after Brock approves the IDs in launch-gate item #7.

---

## Suggested workflow per research run

1. Pick a single research question. Tight scope beats sprawling prompts.
2. Run the same question through 2–4 tools (ChatGPT / Gemini / Perplexity / Claude) for cross-validation.
3. Save raw outputs here using the filename pattern above.
4. Write a short distillation note alongside (`YYYY-MM-DD_<topic>_distilled.md`) summarizing:
   - The question asked.
   - Which tools were consulted.
   - Where they agreed.
   - Where they disagreed (and which version you trust, with rationale).
   - Concrete next action for the migration (if any).
5. **If** the distilled finding feeds a tracked artifact (e.g. a new redirect entry in `vercel.json`), Brock decides whether to open a separate, scoped PR for that change. The distillation itself stays local.

---

## What this folder does NOT authorize

- DNS cutover.
- Editing `vercel.json` (redirects, headers, buildCommand).
- Editing the launch gate.
- Installing tracking tags in production HTML.
- Editing schema / `BRAND` dict in `build.py`.
- Updating GBP or any external citation.
- Modifying ServiceTitan scheduler embed.
- Touching WordPress / WP Engine.

Cutover authority lives entirely in `docs/migration/launch-gate.md`.

---

## Reference

- Launch gate (controlling document): `docs/migration/launch-gate.md`
- Preview validation record: `docs/migration/vercel-preview-validation.md`
- Local evidence-pack overview: `migration-evidence-pack/README-local-evidence-pack.md`
- Repo-level deploy contract: `vercel.json` (do not edit without explicit approval)
- Repo-level Claude rules: `CLAUDE.md`

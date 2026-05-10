# sparkshark-com

Public marketing site for **Spark Shark Electric** — sparkshark.com.

Static HTML. Production hosting is moving to **Vercel** (DNS cutover gated by `docs/migration/launch-gate.md`); a transitional GitHub Pages preview remains live during the migration window. No frameworks, no Node toolchain — `build.py` (Python stdlib) generates every page.

## Repo structure

- `index.html` — homepage
- `css/site.css` — design system + components
- `js/site.js` — minimal interactivity (mobile menu)
- `img/` — logo, mascot
- `[service-name]/index.html` — one directory per service page (clean URLs)
- `locations-we-serve/[city]/index.html` — city pages
- `2026/05/07/[slug]/index.html` — blog posts
- `build.py` — page generator (run if updating templates or content; templates are baked into pages once generated)
- `vercel.json` — Vercel deploy contract (buildCommand, redirects, headers)
- `docs/migration/launch-gate.md` — Brock-Owned DNS Cutover Launch Gate (gates DNS flip)
- `robots.txt`, `sitemap.xml`, `llms.txt`, `llms-full.txt`, `404.html`

## Editing pages

For most copy/markup work, edit the source in `copy-drafts/*.md` or `build.py`'s manifest, run `python3 build.py` locally, and commit the regenerated HTML. Vercel rebuilds with `BASE=""` automatically on push (~10–30s deploy); the github.io preview also republishes from the same push during the transitional window.

Direct hand-edits to generated `index.html` files are discouraged — they will be overwritten the next time `build.py` runs.

## Brand canon

- **Phone:** (405) 436-4776 (everywhere — `tel:+14054364776`)
- **Address:** Moore, OK 73160
- **License:** #163603
- **Rating:** 4.8/5 across 117+ reviews
- **BBB Accredited:** Since 2025-07-14

## Schema architecture

Every page emits one canonical 4-node `@graph` (WebSite + Organization + LocalBusiness/Electrician + FAQPage). Service pages additionally emit BreadcrumbList + Service. Blog posts emit BreadcrumbList + Article.

## Hosting

**Production target: Vercel.** Deploy contract in `vercel.json` — Vercel runs `BASE="" python3 build.py` at deploy time, so production HTML is always rebuilt from source rather than relying on whatever was committed. Custom domain (`www.sparkshark.com` primary, `sparkshark.com` apex auto-301) attached at the Vercel project level. **No `CNAME` file required.**

**Transitional preview: GitHub Pages.** The github.io preview at `sparksharkelectric.github.io/sparkshark-com/` remains live during the migration window. CI builds with default `BASE=/sparkshark-com` for that preview. Both hosts work in parallel until the GH preview is retired post-cutover.

**DNS cutover is blocked by `docs/migration/launch-gate.md`.** Until every gate item is Approved (or Not Applicable with written reason), the domain stays pointed at the legacy host. Only Brock may approve gate items.

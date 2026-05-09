# sparkshark-com

Public marketing site for **Spark Shark Electric** — sparkshark.com.

Static HTML hosted on GitHub Pages. No frameworks, no build step, no dependencies.

## Repo structure

- `index.html` — homepage
- `css/site.css` — design system + components
- `js/site.js` — minimal interactivity (mobile menu)
- `img/` — logo, mascot
- `[service-name]/index.html` — one directory per service page (clean URLs)
- `locations-we-serve/[city]/index.html` — city pages
- `2026/05/07/[slug]/index.html` — blog posts
- `build.py` — page generator (run if updating templates or content; templates are baked into pages once generated)
- `CNAME` — custom domain (Spark Shark Electric → www.sparkshark.com)
- `robots.txt`, `sitemap.xml`, `llms.txt`, `llms-full.txt`, `404.html`

## Editing pages

You can edit any HTML file directly through the GitHub web UI (pencil icon → edit → commit). GitHub Pages will auto-deploy in ~30 seconds.

For larger structural changes (new service page, design system updates), run `python3 build.py` locally and commit the regenerated files.

## Brand canon

- **Phone:** (405) 436-4776 (everywhere — `tel:+14054364776`)
- **Address:** Moore, OK 73160
- **License:** #163603
- **Rating:** 4.8/5 across 117+ reviews
- **BBB Accredited:** Since 2025-07-14

## Schema architecture

Every page emits one canonical 4-node `@graph` (WebSite + Organization + LocalBusiness/Electrician + FAQPage). Service pages additionally emit BreadcrumbList + Service. Blog posts emit BreadcrumbList + Article.

## Hosting

GitHub Pages, free tier. Custom domain via `CNAME` file at repo root.

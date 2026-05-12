# Site Hygiene Audit — 2026-05-11 — Plain English

**Verdict: Hygiene mostly clean, two fixable HIGHs.**

I checked the live WP site that sparkshark.com still serves today and the new Vercel build that's waiting to take over. Hygiene-side, the new build is in good shape — schema is correct for a takeover, no commented-out junk, no broken-link bleed, no publicly-served backup files at any standard path, brand spelling is clean. Two HIGH-severity items are worth closing before DNS flips: your favicon is just a downscaled version of the full logo (will look fuzzy in browser tabs and get cached aggressively by Google), and you've got two different Google Tag Manager containers wired in parallel — the WP container and the new Vercel container — and one of them quietly wins on cutover day.

This audit is decoupled from the migration-readiness verdict, which is still HARD NO-GO for separate reasons (Vercel domain attachment + open launch-gate paperwork). Hygiene-clean does not mean cutover-ready.

## Score: 76 / 100 — fix the two HIGHs, the rest is operational

## Top 3 things blocking a clean handoff

1. **The favicon is the full logo file, scaled down.** `build.py` points the browser-tab icon AND the iPhone home-screen icon at the same file: `/img/logo.png`. That file is your full color logo art. At 32×32 pixels it'll render as a blurry, hard-to-recognize square — which is what every browser tab and Google preview will show. Worse: browsers and Google cache favicons aggressively. Whatever icon the very first post-cutover crawl picks up is the one that sticks. Recommended fix: design a dedicated favicon (the shark icon, the lightning bolt, or a tight crop of the mascot) at 32×32 / 192×192 / 180×180 PNGs, drop them in `img/`, point `build.py` at them. One PR. About 30 minutes once you decide what the favicon should be.

2. **You have two Google Tag Manager containers wired to two different sites.** The live WP site uses `GTM-W7V4RS7C` plus your Google Ads conversion `AW-17076116496`. The new Vercel build uses a different container, `GTM-TBCXCXGS`. The day DNS flips, the Vercel container becomes the one that sees every visit — and unless you've copied your events, audiences, and Google Ads conversion wiring into it first, you start tracking from zero. This overlaps with Launch Gate #7 ("Tracking IDs") which is already open. Decision you owe: one container ID across both surfaces (and which one), or both retained with a documented purpose.

3. **Two FAQPage blocks on every service page is technically duplicate.** The new build generates one FAQPage inside the `@graph` and another standalone FAQPage on every service page. Google has been forgiving of this in the past, but the right answer is one. This touches the schema generators inside `build.py`, which is a protected surface, so the right path is an ADR question and a deliberate edit — not a quick fix.

## Top 3 things that are clean

1. **The site itself is in takeover-mode shape, schema-wise.** The new build emits a single 4-node `@graph` per page (WebSite + Organization + LocalBusiness/Electrician + FAQPage) with no `sameAs` links pointing at any Flanco-era social profiles. That's exactly what a takeover should look like. The old Yoast-generated schema on the WP site goes away the moment the WP install does.

2. **No publicly-served backup files at any standard path.** I probed 21 common attack surfaces — `backup.zip`, `db.sql`, `.env`, `wp-config.php.bak`, `/.git/`, and so on — against both the live WP site and the Vercel preview. Every probe returned 403 or 404. (A truly thorough sweep would need SFTP access to walk the full filesystem; that's a probe I couldn't run from this session.)

3. **No commented-out HTML, no Flanco bleed in the page bodies, clean heading hierarchy, no in-content links to staging or the old company name.** This is the boring stuff that often blows up on takeovers, and your new build is past it.

## What I'd do next

Start with the favicon. It's the cheapest fix (one PR, no schema-generator risk, no protected-surface touch) and it closes the most-cached identity asset before Google's first crawl on the new host. While you're picking the favicon art, also decide which GTM container survives — that closes both the hygiene HIGH and Launch Gate #7's tracking-decision blocker in one conversation. The FAQPage ADR can wait — it's a polish item, not a launch item.

Skip-warning: the migration-readiness audit from the same session is still HARD NO-GO because of the Vercel domain attachment + open launch-gate rows. Hygiene won't unblock that. Fix the domain attachment first; this audit's two HIGHs are next.

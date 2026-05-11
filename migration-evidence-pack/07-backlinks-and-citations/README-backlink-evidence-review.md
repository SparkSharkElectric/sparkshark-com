# Backlink Evidence Review — v5 Update

**Status:** Supplemental migration evidence. Not a DNS launch gate by itself, but important for redirect priority, authority preservation, and legacy Flanco/Spark Shark entity cleanup.  
**Updated:** 2026-05-10  
**Source:** Google Search Console → Links exports and screenshots.

## Files added in v5

- `gsc-links-external-latest-links-2026-05-10.csv`
- `gsc-links-external-more-sample-links-2026-05-10.csv`
- `gsc-links-external-all-links-deduped-2026-05-10.csv`
- `gsc-links-internal-your-pages-linking-to-homepage-2026-05-10.csv`
- `gsc-links-internal-your-pages-linking-to-page-export-1-2026-05-10.csv`
- `gsc-links-internal-your-pages-linking-to-page-export-2-2026-05-10.csv`
- `gsc-links-internal-your-pages-linking-to-page-export-4-2026-05-10.csv`
- `gsc-links-internal-your-pages-linking-to-page-export-5-2026-05-10.csv`
- `gsc-links-internal-your-pages-linking-deduped-2026-05-10.csv`

## External link dedupe result

- Latest links export rows: 28
- More sample links export rows: 28
- Unique external linking URLs after dedupe: 28
- Finding: Latest Links and More Sample Links appear to contain the same 28 unique external linking pages in this GSC export set. Keep both raw files as evidence, but use the deduped CSV for analysis.

## Notable external findings

- `www.networx.com/c.flanco-electric` appears in the external backlink set.
- Several directory/citation-style sites appear: YellowPages, BBB, best-electrician-moore.com, CallUpContact, ChamberOfCommerce, DexKnows, MapQuest, Networx, ProvenExpert, SmartElectricalServices, Superpages, USCity.
- Social/content sources include X/Twitter, Pinterest, Reddit, and Medium.

## Migration implication

Deep Research should use the deduped external links CSV to decide:
- which citation sources deserve cleanup
- whether any Flanco-era citation/backlink should be preserved, redirected, or ignored
- whether existing links to the homepage and `/electrical-installation/` require redirect-map changes
- whether citation/NAP cleanup should be prioritized before or after DNS cutover

## Remaining backlink nice-to-haves

- If tools like Ahrefs, Semrush, Moz, BrightLocal, Whitespark, or Yext reports exist from prior marketing companies, place them under `09-past-marketing-audits/incoming/`.
- GSC does not show every backlink. Third-party backlink/citation reports can reveal additional old Flanco/Spark Shark/BSF references.

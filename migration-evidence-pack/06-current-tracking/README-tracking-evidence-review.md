# Tracking Evidence Review — 2026-05-10

This folder now contains screenshots proving Spark Shark has Google Analytics, Google Tag Manager / Google Tags, Google Ads, and Local Services Ads access/screens.

## Current verdict

Gate #7 is **provided but needs implementation review**.

The evidence is enough to continue planning, but not enough to blindly install tracking on Vercel. The exact active IDs and deployment strategy need to be confirmed before code changes.

## Open tracking questions

1. Which GA4 web stream is the canonical stream for launch?
2. What is the exact GA4 Measurement ID (`G-...`) for that stream?
3. Is GTM the intended deployment layer, or should the site use direct `gtag`?
4. What are the Google Ads conversion ID and conversion labels, if website conversion tracking is active?
5. Are any old/duplicate Google tags present that should not be carried into launch?

## Do not do yet

- Do not install tracking code.
- Do not edit Vercel/domain settings.
- Do not launch DNS cutover.
- Do not assume the screenshots alone prove tracking is launch-ready.

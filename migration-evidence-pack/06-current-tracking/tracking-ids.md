# Tracking IDs — Spark Shark Electric

**Status:** Evidence provided, but final implementation decision still needs technical review before launch.
**Decision date:** 2026-05-10 evidence capture.

## Evidence captured

Screenshots in this folder document access to:

- Google Analytics account/property screens for Spark Shark
- GA4 data streams for Spark Shark / sparkshark.com
- Google Tag Manager account/container screens
- Google Tags list
- Google Ads overview
- Local Services Ads leads overview

## GA4

Evidence source files:

- `01-ga4-analytics-account-overview.png`
- `02-ga4-account-property-list.png`
- `05-ga4-data-streams.png`

Observed from screenshots:

- Analytics account: Spark Shark Analytics
- GA4 property/app shown for Spark Shark
- Two web streams are visible:
  - `https://Sparkshark.com` — no data received in past 48 hours at time of screenshot
  - `https://sparkshark.com` — receiving traffic in past 48 hours at time of screenshot

Needed before implementation:

- Confirm the active GA4 Measurement ID (`G-...`) from the active `https://sparkshark.com` web stream.
- Confirm whether the inactive/case-variant stream should be ignored, archived, or left alone.

## Google Tag Manager / Google Tags

Evidence source files:

- `06-google-tag-manager-container-overview.png`
- `07-google-tags-list.png`
- `08-tag-manager-account-overview.png`

Observed from screenshots:

- Tag Manager account exists for Spark Shark.
- A web container exists for sparkshark.com.
- Google Tags list shows multiple tags/IDs, including GA and Google Ads-looking IDs.

Needed before implementation:

- Confirm the exact GTM Container ID to install or preserve.
- Confirm whether launch should use GTM as the single deployment layer or direct gtag.
- Remove/avoid duplicate or stale tags before final launch if multiple Google tags are present.

## Google Ads / Local Services Ads

Evidence source files:

- `03-google-ads-campaign-overview.png`
- `04-local-services-ads-leads-overview.png`

Observed from screenshots:

- Google Ads account exists.
- Campaigns appear paused at time of screenshot.
- Local Services Ads lead dashboard exists and shows historical leads.

Needed before implementation:

- Confirm Google Ads conversion ID (`AW-...`) and conversion label(s) for website calls/forms, if used.
- Confirm whether LSA tracking relies on Google/GBP/LSA platform calls only or needs website event tracking.

## Tracking decision for launch

Recommended launch posture:

- Prefer **GTM as the deployment layer** if the existing GTM container is confirmed active and clean.
- Avoid installing multiple competing GA/GTM/gtag snippets directly in site HTML.
- Before DNS cutover, create a small tracking implementation PR and verify events on the Vercel preview.

## Launch-gate status interpretation

This file provides evidence for Gate #7 but should not be treated as fully approved until the exact active GA4 Measurement ID, GTM decision, and Google Ads conversion setup are confirmed.

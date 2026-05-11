# Tracking IDs (Local Template)

**Maps to launch-gate item #7** in `docs/migration/launch-gate.md`.

This file is local-only. **Do not commit.** Tracking IDs are sensitive identifiers — keep out of git history.

When filled in, save the populated copy at:

```
migration-evidence-pack/06-current-tracking/tracking-ids.md
```

(Replace the `-template` suffix; same gitignored folder, so the populated copy is also local-only.)

---

## Required fields

| Field | Value | Notes |
|---|---|---|
| GA4 Measurement ID | `G-XXXXXXXXXX` | Required if GA4 is in use |
| GTM Container ID | `GTM-XXXXXXX` | Optional — only if GTM is the chosen approach |
| Google Ads Conversion ID | `AW-XXXXXXXXXX` | Optional — only if Google Ads is running conversions |
| Google Ads Conversion Label | `XXXXXXXXX` | Paired with the conversion ID above |
| Microsoft Clarity ID | `xxxxxxxxxx` | Optional — only if Clarity is in use |
| Decision: GTM or direct gtag | `<GTM | direct gtag>` | Drives tag implementation strategy |

## Notes

- Date provided:
- Provided by:
- Source (where the IDs came from — GA admin / GTM admin / Ads UI / Clarity admin):
- Existing site already loads any of these tags? Yes / No — if yes, where:
- Any prior conversion data we want to preserve continuity for? Yes / No — details:
- Open questions:

---

## Done criteria (verbatim, from launch-gate item #7)

> File contains GA4 measurement ID, GTM container ID if used, Google Ads conversion ID/label if used, and decision whether to use GTM or direct gtag.

---

## What this evidence does NOT authorize

- Installing any tag in production HTML.
- Editing `build.py` to inject tracking.
- DNS cutover.

Tag installation is a separate, scoped PR after this evidence is **Approved** by Brock in `docs/migration/launch-gate.md`.

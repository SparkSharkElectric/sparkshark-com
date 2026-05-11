# Canonical NAP — Decision (Local Template)

**Maps to launch-gate item #9** in `docs/migration/launch-gate.md`.

This file is local-only. **Do not commit.** NAP decisions affect schema, GBP, and citations — record once, then propagate.

When filled in, save the populated copy at:

```
migration-evidence-pack/11-verified-business-facts/canonical-nap.md
```

(Replace the `-template` suffix; same gitignored folder.)

---

## Canonical NAP decision

| Field | Value | Notes |
|---|---|---|
| Business name | `Spark Shark Electric` | Public brand. Always with the space. |
| Public address OR service-area-only | `<address | service-area-only>` | If service-area-only, list service areas below |
| Phone number |  | E.164 format expected for schema; display format may differ |
| Website URL | `https://www.sparkshark.com/` | Primary canonical |
| GBP URL (if known) |  | Google Business Profile public URL |

## Service-area list (if applicable)

-

## Listings / citations that may need updating

- [ ] Google Business Profile
- [ ] Yelp
- [ ] BBB
- [ ] Networx
- [ ] Thumbtack
- [ ] ProvenExpert
- [ ] Apple Maps
- [ ] Bing Places
- [ ] Other:

## Notes

- Date decided:
- Decided by: Brock Flanary (Founder / CEO, Spark Shark Electric)
- Conflict observed pre-decision (e.g. Yelp + ProvenExpert vs BBB): 
- Schema impact (`build.py` BRAND dict, LocalBusiness/Electrician node, address, areaServed):
- Citation cleanup priority order:
- Open questions:

---

## Done criteria (verbatim, from launch-gate item #9)

> Brock chooses the official public NAP: business name, address or service-area-only decision, phone, website, and notes which listings must be updated.

---

## What this evidence does NOT authorize

- Editing the schema in `build.py`.
- Editing the `BRAND` dict in `build.py`.
- Updating any external listing.
- DNS cutover.

Schema and listing updates are separate, scoped tasks after this NAP decision is **Approved** by Brock in `docs/migration/launch-gate.md`.

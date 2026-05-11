# migration-evidence-pack — Evidence Pack (committed)

**Status:** Committed to the public `sparkshark-com` repo on 2026-05-11 with Brock's explicit written approval, overriding the original local-only `.gitignore` design. Repo will be flipped to private post-launch (Brock 2026-05-11). The "do not commit … unless Brock explicitly approves it in writing" rule below remains in force; this commit satisfies it.
**Created:** 2026-05-10
**Anchored to main commit:** `ab80db2` (PR #5 — vercel-preview-validation doc landed)

This folder is the destination for Brock-owned evidence required by the **Brock-Owned DNS Cutover Launch Gate**.

---

## Hard rules

- This folder was originally **local-only** via an inner `.gitignore` containing `*`. That `.gitignore` was removed on 2026-05-11 per Brock's explicit written approval so the evidence pack could be reviewed in the public repo during migration.
- Do **not** add new screenshots, exports, or tracking IDs that contain private credentials (GA4/GTM/Ads IDs, API keys, OAuth secrets, recovery codes, private keys). Templates (`tracking-ids-template.md`, `canonical-nap-template.md`) must remain unfilled in this public repo until the repo is flipped to private.
- Evidence here maps directly to gate items in `/Users/brock/Projects/sparkshark-com/docs/migration/launch-gate.md`.
- DNS cutover is **blocked** until every one of the 9 gate items is **Approved** OR **Not Applicable** with a written reason in the Status cell of `launch-gate.md`. **Only Brock** may mark gate items Approved or Not Applicable.

---

## Folder layout

```
migration-evidence-pack/
  .gitignore                                 ← ignores everything in this folder
  README-local-evidence-pack.md              ← this file

  04-google-search-console/                  ← Gate items #1, #2, #3
                                             # gsc-pages-export.csv
                                             # gsc-queries-export.csv
                                             # gsc-indexing-pages-export.csv

  05-google-business-profile/                ← Gate item #4
                                             # GBP screenshots: name, address/SAB,
                                             # phone, website, primary + secondary
                                             # categories, services, hours, description

  06-current-tracking/                       ← Gate items #7, #8
    tracking-ids-template.md                 # template for #7 — fill in, then save as
                                             # tracking-ids.md (still ignored)
    servicetitan-scheduler-test-proof/       # screenshots from #8 (ST scheduler test)

  11-verified-business-facts/                ← Gate item #9
    canonical-nap-template.md                # template for #9 — fill in, then save as
                                             # canonical-nap.md (still ignored)

  12-launch-and-rollback/                    ← Gate items #5, #6
    evidence-checklist.md                    # cutover-day evidence checklist
                                             # current-dns-before-cutover.png
                                             # wp-engine-backup-confirmation.png
```

---

## Evidence flow (per gate item)

1. Brock collects the evidence and saves it at the path documented in `launch-gate.md`'s **Where evidence should be saved** column.
2. Brock notifies Claude that the item has evidence.
3. Claude updates the Status cell in `launch-gate.md` from **Not Provided** → **Provided, Not Reviewed**.
4. Claude reviews the evidence against the **Done criteria** column.
5. Claude updates Status to:
   - **Approved** if complete, OR
   - **Reviewed, Needs Fix** with a Notes line explaining what's missing.
6. **Only Brock** may write **Not Applicable: <reason>** in a Status cell. Claude must not unilaterally classify any item as Not Applicable.

DNS cutover may proceed only when **all 9 rows** are **Approved** OR **Not Applicable** with written reason.

---

## Mapping: gate item → evidence path

| Gate # | Required evidence | Local path |
|---|---|---|
| 1 | GSC Pages export | `04-google-search-console/gsc-pages-export.csv` |
| 2 | GSC Queries export | `04-google-search-console/gsc-queries-export.csv` |
| 3 | GSC Indexed/Not Indexed export | `04-google-search-console/gsc-indexing-pages-export.csv` |
| 4 | GBP screenshots | `05-google-business-profile/` |
| 5 | Current DNS records screenshot | `12-launch-and-rollback/current-dns-before-cutover.png` |
| 6 | WP Engine backup confirmation | `12-launch-and-rollback/wp-engine-backup-confirmation.png` |
| 7 | GA4 / GTM / Google Ads IDs | `06-current-tracking/tracking-ids.md` |
| 8 | ServiceTitan scheduler test proof | `06-current-tracking/servicetitan-scheduler-test-proof/` |
| 9 | Canonical NAP decision | `11-verified-business-facts/canonical-nap.md` |

---

## What this folder does NOT authorize

This folder stores supporting evidence. It does **not** authorize any of the following:

- DNS cutover at GoDaddy.
- Vercel domain attachment (`www.sparkshark.com`, `sparkshark.com`).
- WordPress / WP Engine decommissioning.
- Tracking installation in production HTML (GA4, GTM, Google Ads, GSC verification, Clarity).
- Contact form fix (Formspree ID or Vercel Function decision).
- ServiceTitan smoke booking on the Vercel preview.
- Any treatment of the site as launch-ready.

Cutover authority lives entirely in `docs/migration/launch-gate.md`. This folder only stores the evidence that supports gate-item review.

---

## Reference

- Launch gate (controlling document): `docs/migration/launch-gate.md`
- Preview validation record: `docs/migration/vercel-preview-validation.md`
- Repo-level deploy contract: `vercel.json` (do not edit without explicit approval)
- Repo-level Claude rules: `CLAUDE.md`
